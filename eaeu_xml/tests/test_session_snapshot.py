from dataclasses import replace
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from eaeu_xml.application import (
    EaeuXmlApplication, SESSION_SNAPSHOT_VERSION, SessionMessageSnapshot,
    SessionPersistenceService, SessionSnapshotError, SessionSnapshotValidator,
    TransactionSessionSnapshot,
    normalize_session_path,
)
from eaeu_xml.core.enums import MessageKind, SignalKind, TransactionPattern, TransactionState
from eaeu_xml.decision5.models import (
    DummyBodyPayload, FaultReasonText, FaultSubcode, LogicalAddress, ProcedureId,
    ProcedureInstance, SoapFault, TransactionDefinition, TransactionInstance,
    TransactionParameters,
)
from eaeu_xml.services.fault_factory import FaultFactory
from eaeu_xml.services.identifier_service import IdentifierService
from eaeu_xml.services.message_factory import MessageFactory
from eaeu_xml.services.signal_factory import SignalFactory
from eaeu_xml.services.transaction_engine import RetryService


ROOT = Path(__file__).parents[2]


class SessionSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.app = EaeuXmlApplication(ROOT)
        self.service = SessionPersistenceService()

    def tearDown(self):
        self.temp.cleanup()

    def test_session_filename_normalization_uses_canonical_suffix_once(self):
        expected = self.root / "test.eaeusession.json"
        self.assertEqual(normalize_session_path(self.root / "test"), expected)
        self.assertEqual(normalize_session_path(self.root / "test.eaeusession"), expected)
        self.assertEqual(normalize_session_path(self.root / "test.eaeusession.json"), expected)
        self.assertNotIn(".eaeusession.json.json", str(expected))

    def _request_response_snapshot(self):
        session = self.app.start_transaction("P.MM.01", "P.MM.01.TRN.004", seed=9)
        request = session.generate_initial_message()
        response = session.generate_response("P.MM.01.MSG.006")
        self.assertTrue(request.success and response.success)
        return session, request, response, session.create_snapshot()

    def test_transaction_session_snapshot_json_roundtrip(self):
        session, request, response, snapshot = self._request_response_snapshot()
        path = self.root / "session.eaeusession.json"
        self.service.save(snapshot, path)
        restored = self.service.load(path)
        self.assertEqual(restored, snapshot)
        self.assertEqual(restored.session_snapshot_version, SESSION_SNAPSHOT_VERSION)
        self.assertEqual([item.message_id for item in restored.history],
                         [request.metadata["message_id"], response.metadata["message_id"]])
        self.assertEqual(restored.history[1].relates_to, restored.history[0].message_id)
        self.assertEqual(restored.procedure_id, request.metadata["procedure_id"])
        self.assertEqual(restored.conversation_id, request.metadata["conversation_id"])
        self.assertTrue(SessionSnapshotValidator().validate(restored).continue_ready)
        hook_path = self.root / "session-hook.eaeusession.json"
        session.save_snapshot(hook_path)
        self.assertEqual(len(self.service.load(hook_path).history), 2)

    def test_trn004_actions_state_and_history_are_preserved(self):
        _, request, response, snapshot = self._request_response_snapshot()
        self.assertEqual(snapshot.transaction_pattern, "QUESTION_RESPONSE")
        self.assertEqual(snapshot.current_state, "COMPLETED")
        self.assertEqual(len(snapshot.history), 2)
        self.assertEqual(snapshot.history[0].action, request.metadata["action"])
        self.assertEqual(snapshot.history[1].action, response.metadata["action"])
        self.assertNotEqual(snapshot.history[0].message_id, snapshot.history[1].message_id)

    def _core_transaction(self):
        ids = IdentifierService()
        definition = TransactionDefinition(TransactionPattern.QUESTION_RESPONSE,
            TransactionParameters(response_timeout=timedelta(minutes=1), retry_count=1))
        procedure = ProcedureInstance("P.SP.03.PRC.001", ProcedureId.root(ids))
        transaction = TransactionInstance("P.SP.03.TRN.002", ids.new_conversation_id(), procedure,
                                          definition=definition)
        to = LogicalAddress.parse("EAEU://EEC/CP/P.SP.03/P.ACT.001")
        reply = LogicalAddress.parse("EAEU://RU/CP/P.SP.03/P.SP.03.ACT.002")
        message = MessageFactory(ids).create_initial_application_message(
            transaction=transaction, process_code="P.SP.03", process_version="1.0.0",
            message_code="P.CC.04.MSG.003", to=to, reply_to=reply,
            body_payload=DummyBodyPayload("payload"))
        return ids, transaction, message, to, reply

    def test_retry_attempt_chain_is_not_lost(self):
        ids, transaction, _, _, _ = self._core_transaction()
        transaction.state = TransactionState.ACTIVE
        RetryService().retry_record(transaction, transaction.message_history[0], ids.new_message_id())
        snapshot = TransactionSessionSnapshot.from_transaction(transaction, process_code="P.SP.03",
            process_version="1.0.0", transaction_pattern="QUESTION_RESPONSE",
            transaction_parameters={"response_timeout": "PT1M", "retry_count": 1})
        result = SessionSnapshotValidator().validate(snapshot)
        self.assertFalse(result.errors)
        self.assertEqual(snapshot.history[1].attempt_number, 2)
        self.assertEqual(snapshot.history[1].retry_of, snapshot.history[0].message_id)
        self.assertNotEqual(snapshot.history[1].message_id, snapshot.history[0].message_id)

    def test_notification_snapshot_has_no_synthetic_response(self):
        session = self.app.start_transaction("P.MM.01", "P.MM.01.TRN.011")
        result = session.generate_initial_message()
        snapshot = session.create_snapshot()
        self.assertTrue(result.success)
        self.assertEqual(snapshot.transaction_pattern, "NOTIFICATION")
        self.assertEqual(len(snapshot.history), 1)
        self.assertIsNone(snapshot.history[0].relates_to)

    def test_signal_history_roundtrip(self):
        ids, transaction, message, to, reply = self._core_transaction()
        SignalFactory(ids).create(transaction=transaction, source_message=message,
                                  kind=SignalKind.RECEIVED, to=reply, reply_to=to)
        snapshot = TransactionSessionSnapshot.from_transaction(transaction, process_code="P.SP.03",
            process_version="1.0.0", transaction_pattern="QUESTION_RESPONSE")
        restored_path = self.root / "signal.eaeusession.json"
        self.service.save(snapshot, restored_path)
        restored = self.service.load(restored_path)
        self.assertEqual(restored.history[1].message_kind, "SIGNAL")
        self.assertEqual(restored.history[1].signal_kind, "P.MSG.RCV")
        self.assertEqual(restored.history[1].relates_to, restored.history[0].message_id)

    def test_fault_correlation_including_relates_action(self):
        _, transaction, message, to, _ = self._core_transaction()
        fault = FaultFactory().create(source_message=message, sender=to,
            fault=SoapFault(FaultSubcode.INVALID_HEADER,
                            (FaultReasonText("Некорректный заголовок", "ru"),)))
        snapshot = TransactionSessionSnapshot.from_transaction(transaction, process_code="P.SP.03",
            process_version="1.0.0", transaction_pattern="QUESTION_RESPONSE")
        record = SessionMessageSnapshot(
            sequence_number=2, message_code=None, direction="SENT",
            action=fault.header.action.serialize(), message_id=fault.header.message_id.serialize(),
            relates_to=fault.header.relates_to.message_id.serialize(),
            relates_action=fault.header.relates_to.relates_action,
            created_at=datetime.now(timezone.utc).isoformat(), attempt_number=1,
            retry_of=None, message_kind=MessageKind.TECHNICAL_FAULT.value,
            fault_kind=fault.header.action.serialize(), procedure_id=snapshot.procedure_id,
            conversation_id=snapshot.conversation_id,
        )
        snapshot = replace(snapshot, history=(*snapshot.history, record), current_state="FAILED")
        self.assertTrue(SessionSnapshotValidator().validate(snapshot).continue_ready)
        path = self.root / "fault.eaeusession.json"
        self.service.save(snapshot, path)
        self.assertEqual(self.service.load(path).history[-1].relates_action,
                         snapshot.history[0].action)

    def test_corrupted_unknown_version_and_missing_fields_are_blocked(self):
        path = self.root / "bad.eaeusession.json"
        for payload, code in (("{bad", "SESSION_SNAPSHOT_INVALID_JSON"),
                              (json.dumps({"session_snapshot_version": 999}), "UNSUPPORTED_SESSION_SNAPSHOT_VERSION"),
                              (json.dumps({"session_snapshot_version": 1}), "SESSION_SNAPSHOT_SCHEMA_INVALID")):
            path.write_text(payload, encoding="utf-8")
            with self.subTest(code=code), self.assertRaises(SessionSnapshotError) as raised:
                self.service.load(path)
            self.assertEqual(raised.exception.code, code)

    def test_missing_history_broken_links_duplicate_and_attempts_are_rejected(self):
        _, _, _, snapshot = self._request_response_snapshot()
        unknown = "urn:uuid:00000000-0000-4000-8000-000000000099"
        cases = (
            (replace(snapshot, history=()), "SESSION_HISTORY_REQUIRED"),
            (replace(snapshot, history=(snapshot.history[0], replace(snapshot.history[1], relates_to=unknown))), "BROKEN_RELATES_TO"),
            (replace(snapshot, history=(snapshot.history[0], replace(snapshot.history[1], retry_of=unknown))), "BROKEN_RETRY_OF"),
            (replace(snapshot, history=(snapshot.history[0], replace(snapshot.history[1], message_id=snapshot.history[0].message_id))), "DUPLICATE_MESSAGE_ID"),
        )
        for candidate, code in cases:
            with self.subTest(code=code):
                self.assertIn(code, SessionSnapshotValidator().validate(candidate).errors)

    def test_process_version_mismatch_is_readable_but_not_continue_ready(self):
        _, _, _, snapshot = self._request_response_snapshot()
        result = SessionSnapshotValidator().validate(snapshot, current_process_version="9.9.9")
        self.assertIn("PROCESS_VERSION_MISMATCH", result.errors)
        self.assertFalse(result.continue_ready)
        path = self.root / "readable.eaeusession.json"
        self.service.save(snapshot, path)
        self.assertEqual(self.service.load(path).process_version, snapshot.process_version)

    def test_invalid_direction_action_identifiers_and_stale_timing_are_not_ready(self):
        _, _, _, snapshot = self._request_response_snapshot()
        cases = (
            (replace(snapshot, history=(replace(snapshot.history[0], direction="UNKNOWN"), *snapshot.history[1:])), "MESSAGE_HISTORY_INVALID"),
            (replace(snapshot, history=(replace(snapshot.history[0], action="invalid"), *snapshot.history[1:])), "ACTION_OR_MESSAGE_TYPE_INVALID"),
            (replace(snapshot, history=(replace(snapshot.history[0], procedure_id="urn:uuid:00000000-0000-4000-8000-000000000099"), *snapshot.history[1:])), "MESSAGE_PROCEDURE_ID_MISMATCH"),
            (replace(snapshot, current_state="UNKNOWN"), "SESSION_IDENTIFIER_OR_STATE_INVALID"),
        )
        for candidate, code in cases:
            with self.subTest(code=code):
                result = SessionSnapshotValidator().validate(candidate)
                self.assertIn(code, result.errors)
                self.assertFalse(result.continue_ready)
        old = "2020-01-01T00:00:00+00:00"
        stale = replace(snapshot, current_state="WAITING_RESPONSE",
                        transaction_parameters={"response_timeout": "PT1M"},
                        history=tuple(replace(item, created_at=old) for item in snapshot.history))
        result = SessionSnapshotValidator().validate(stale)
        self.assertTrue(any(item.startswith("TIMING_REVALIDATION_REQUIRED") for item in result.warnings))
        self.assertFalse(result.continue_ready)

    def test_atomic_replace_failure_preserves_previous_snapshot(self):
        _, _, _, snapshot = self._request_response_snapshot()
        path = self.root / "atomic.eaeusession.json"
        self.service.save(snapshot, path)
        previous = path.read_bytes()
        with patch("eaeu_xml.application.session_snapshot.os.replace", side_effect=OSError("disk failure")):
            with self.assertRaises(OSError):
                self.service.save(replace(snapshot, updated_at=datetime.now(timezone.utc).isoformat()), path)
        self.assertEqual(path.read_bytes(), previous)
        self.assertEqual(list(self.root.glob("*.tmp")), [])

    def test_legacy_draft_remains_non_restorable_body_draft(self):
        with tempfile.TemporaryDirectory() as directory:
            app = EaeuXmlApplication(ROOT, drafts_root=Path(directory))
            path = Path(directory) / "legacy.eaeudraft.json"
            document = app.save_draft(path, process_code="P.MM.01",
                transaction_code="P.MM.01.TRN.004", message_code="P.MM.01.MSG.005",
                values={}, session_metadata={"conversation_id": "legacy", "session_restorable": False})
            loaded = app.load_draft(path)
            self.assertEqual(document.draft_version, 1)
            self.assertTrue(any(item.startswith("SESSION_RESTART_REQUIRED") for item in loaded.warnings))
            self.assertFalse(document.session_metadata["session_restorable"])


if __name__ == "__main__":
    unittest.main()
