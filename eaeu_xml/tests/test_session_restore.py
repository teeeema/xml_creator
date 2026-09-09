from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest

from eaeu_xml.application import (
    EaeuXmlApplication, SessionRestoreStatus, TransactionSessionLifecycleService,
    TransactionSessionRestoreService,
)
from eaeu_xml.core.enums import SignalKind
from eaeu_xml.decision5.models import FaultReasonText, FaultSubcode, SoapFault


ROOT = Path(__file__).parents[2]


class SessionRestoreTests(unittest.TestCase):
    def setUp(self):
        self.app = EaeuXmlApplication(ROOT)
        self.restore = TransactionSessionRestoreService(self.app)

    def _request_snapshot(self):
        session = self.app.start_transaction("P.MM.01", "P.MM.01.TRN.004", seed=41)
        request = session.generate_initial_message()
        self.assertTrue(request.success)
        return session, request, session.create_snapshot()

    def test_simple_restore_and_runtime_snapshot_invariant(self):
        _, _, snapshot = self._request_snapshot()
        result = self.restore.restore(snapshot)
        self.assertIs(result.status, SessionRestoreStatus.RESTORABLE)
        self.assertTrue(result.continue_ready)
        self.assertEqual(result.session.create_snapshot(), snapshot)
        self.assertEqual(result.session.transaction.procedure_instance.procedure_id.serialize(), snapshot.procedure_id)
        self.assertEqual(result.session.transaction.conversation_id.serialize(), snapshot.conversation_id)
        self.assertEqual([item.message_id.serialize() for item in result.session.transaction.message_history],
                         [item.message_id for item in snapshot.history])

    def test_trn004_restore_then_response_preserves_request_correlation(self):
        _, request, snapshot = self._request_snapshot()
        restored = TransactionSessionRestoreService(EaeuXmlApplication(ROOT)).restore(snapshot)
        response = restored.session.generate_response("P.MM.01.MSG.006")
        self.assertTrue(response.success)
        self.assertNotEqual(response.metadata["message_id"], request.metadata["message_id"])
        self.assertEqual(response.metadata["relates_to"], request.metadata["message_id"])
        self.assertEqual(response.metadata["procedure_id"], request.metadata["procedure_id"])
        self.assertEqual(response.metadata["conversation_id"], request.metadata["conversation_id"])
        self.assertEqual(restored.session.transaction.message_history[0].message_id.serialize(), request.metadata["message_id"])

    def test_retry_after_restore_extends_existing_chain(self):
        session, _, _ = self._request_snapshot()
        attempt2 = session.retry()
        snapshot = session.create_snapshot()
        restored = self.restore.restore(snapshot)
        self.assertTrue(restored.continue_ready)
        attempt3 = restored.session.retry()
        ids = [item.message_id.serialize() for item in restored.session.transaction.message_history]
        self.assertEqual(len(ids), 3)
        self.assertEqual(len(set(ids)), 3)
        self.assertEqual(attempt3.retry_of, attempt2.message_id)
        self.assertEqual(attempt3.attempt_number, 3)

    def test_notification_restore_and_next_signal(self):
        session = self.app.start_transaction("P.MM.01", "P.MM.01.TRN.011")
        initial = session.generate_initial_message()
        snapshot = session.create_snapshot()
        restored = self.restore.restore(snapshot)
        self.assertTrue(restored.continue_ready)
        self.assertEqual(len(restored.session.transaction.message_history), 1)
        source = restored.session.historical_application_message(initial.metadata["message_id"])
        signal = restored.session.create_signal(source, SignalKind.RECEIVED)
        self.assertNotEqual(signal.header.message_id.serialize(), initial.metadata["message_id"])
        self.assertEqual(signal.header.relates_to.message_id.serialize(), initial.metadata["message_id"])
        self.assertEqual(restored.session.transaction.state.value, "COMPLETED")
        self.assertEqual(restored.session.create_snapshot().history[-1].signal_kind, "P.MSG.RCV")

    def test_mutual_obligations_signal_history_restores_then_advances(self):
        session = self.app.start_transaction("P.MM.01", "P.MM.01.TRN.008")
        initial = session.generate_initial_message()
        source = session.historical_application_message(initial.metadata["message_id"])
        first_signal = session.create_signal(source, SignalKind.RECEIVED)
        snapshot = session.create_snapshot()
        restored = self.restore.restore(snapshot)
        self.assertTrue(restored.continue_ready)
        self.assertEqual(restored.session.transaction.state.value, "WAITING_PROCESSING")
        restored_source = restored.session.historical_application_message(initial.metadata["message_id"])
        second_signal = restored.session.create_signal(restored_source, SignalKind.ACCEPTED_FOR_PROCESSING)
        self.assertNotEqual(second_signal.header.message_id, first_signal.header.message_id)
        self.assertEqual(restored.session.transaction.state.value, "WAITING_RESPONSE")
        signals = [item for item in restored.session.create_snapshot().history if item.signal_kind]
        self.assertEqual([item.signal_kind for item in signals], ["P.MSG.RCV", "P.MSG.PRS"])

    def test_fault_after_restore_uses_core_factory_correlation(self):
        _, request, snapshot = self._request_snapshot()
        restored = self.restore.restore(snapshot)
        source = restored.session.historical_application_message(request.metadata["message_id"])
        sender = source.header.reply_to.address
        fault = restored.session.create_fault(source, sender,
            SoapFault(FaultSubcode.INVALID_HEADER,
                      (FaultReasonText("Некорректный заголовок", "ru"),)))
        item = restored.session.create_snapshot().history[-1]
        self.assertNotEqual(item.message_id, request.metadata["message_id"])
        self.assertEqual(item.relates_to, request.metadata["message_id"])
        self.assertEqual(item.relates_action, request.metadata["action"])
        self.assertEqual(fault.header.relates_to.relates_action, request.metadata["action"])
        fault_snapshot = restored.session.create_snapshot()
        fault_restored = self.restore.restore(fault_snapshot)
        self.assertTrue(fault_restored.continue_ready)
        self.assertEqual(fault_restored.session.create_snapshot(), fault_snapshot)

    def test_process_version_and_transaction_definition_mismatch(self):
        _, _, snapshot = self._request_snapshot()
        version = self.restore.restore(replace(snapshot, process_version="9.9.9",
            history=tuple(replace(item, action=item.action.replace("/1.1.0/", "/9.9.9/")) for item in snapshot.history)))
        self.assertIs(version.status, SessionRestoreStatus.PROCESS_VERSION_MISMATCH)
        transaction_code = "P.MM.01.TRN.999"
        missing = replace(snapshot, transaction_code=transaction_code,
            history=tuple(replace(item, action=item.action.replace("P.MM.01.TRN.004", transaction_code)) for item in snapshot.history))
        self.assertIs(self.restore.restore(missing).status, SessionRestoreStatus.TRANSACTION_NOT_FOUND)

    def test_unknown_message_action_and_direction_are_blocked(self):
        session, _, _ = self._request_snapshot()
        response = session.generate_response("P.MM.01.MSG.006")
        self.assertTrue(response.success)
        snapshot = session.create_snapshot()
        unknown_code = "P.MM.01.MSG.999"
        unknown = replace(snapshot, history=(snapshot.history[0], replace(snapshot.history[1],
            message_code=unknown_code, action=snapshot.history[1].action.replace("P.MM.01.MSG.006", unknown_code))))
        self.assertIs(self.restore.restore(unknown).status, SessionRestoreStatus.MESSAGE_DEFINITION_MISMATCH)
        direction = replace(snapshot, history=(replace(snapshot.history[0], direction="RECEIVED"), *snapshot.history[1:]))
        self.assertIs(self.restore.restore(direction).status, SessionRestoreStatus.DIRECTION_INVALID)

    def test_state_replay_and_semantic_relates_to_mismatch_are_blocked(self):
        session, _, snapshot = self._request_snapshot()
        self.assertIs(self.restore.restore(replace(snapshot, current_state="COMPLETED")).status,
                      SessionRestoreStatus.STATE_INVALID)
        original_id = snapshot.history[0].message_id
        session.retry()
        response = session.generate_response("P.MM.01.MSG.006")
        self.assertTrue(response.success)
        with_response = session.create_snapshot()
        bad = replace(with_response, history=(*with_response.history[:-1],
            replace(with_response.history[-1], relates_to=original_id)))
        self.assertIs(self.restore.restore(bad).status, SessionRestoreStatus.CORRELATION_INVALID)

    def test_broken_retry_predecessor_semantics_is_blocked(self):
        session, _, _ = self._request_snapshot()
        session.retry()
        session.retry()
        snapshot = session.create_snapshot()
        bad = replace(snapshot, history=(*snapshot.history[:-1], replace(snapshot.history[-1],
            retry_of=snapshot.history[0].message_id, attempt_number=2)))
        self.assertIs(self.restore.restore(bad).status, SessionRestoreStatus.RETRY_INVALID)

    def test_incompatible_signal_and_fault_history_is_blocked(self):
        session = self.app.start_transaction("P.MM.01", "P.MM.01.TRN.011")
        initial = session.generate_initial_message()
        source = session.historical_application_message(initial.metadata["message_id"])
        session.create_signal(source, SignalKind.RECEIVED)
        signal_snapshot = session.create_snapshot()
        signal = replace(signal_snapshot, history=(*signal_snapshot.history[:-1],
            replace(signal_snapshot.history[-1], signal_kind="P.MSG.PRS",
                    action=signal_snapshot.history[-1].action.replace("P.MSG.RCV", "P.MSG.PRS"))))
        self.assertIn(self.restore.restore(signal).status,
                      {SessionRestoreStatus.STATE_INVALID, SessionRestoreStatus.SIGNAL_INVALID})

        request_session, request, _ = self._request_snapshot()
        source = request_session.historical_application_message(request.metadata["message_id"])
        request_session.create_fault(source, source.header.reply_to.address,
            SoapFault(FaultSubcode.INVALID_HEADER,
                      (FaultReasonText("Некорректный заголовок", "ru"),)))
        fault_snapshot = request_session.create_snapshot()
        fault = replace(fault_snapshot, history=(*fault_snapshot.history[:-1],
            replace(fault_snapshot.history[-1], relates_action="wrong")))
        self.assertIn(self.restore.restore(fault).status,
                      {SessionRestoreStatus.SNAPSHOT_INVALID, SessionRestoreStatus.FAULT_INVALID})

    def test_timing_revalidation_never_returns_usable_session(self):
        _, _, snapshot = self._request_snapshot()
        old = "2020-01-01T00:00:00+00:00"
        stale = replace(snapshot, history=tuple(replace(item, created_at=old) for item in snapshot.history))
        result = self.restore.restore(stale)
        self.assertIs(result.status, SessionRestoreStatus.TIMING_REVALIDATION_REQUIRED)
        self.assertFalse(result.continue_ready)
        self.assertIsNone(result.session)

    def test_legacy_draft_file_is_not_a_session_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy.eaeudraft.json"
            self.app.save_draft(path, process_code="P.MM.01", transaction_code="P.MM.01.TRN.004",
                message_code="P.MM.01.MSG.005", values={},
                session_metadata={"session_restorable": False})
            result = self.restore.restore_path(path)
            self.assertIs(result.status, SessionRestoreStatus.SNAPSHOT_INVALID)
            loaded = self.app.load_draft(path)
            self.assertTrue(any(item.startswith("SESSION_RESTART_REQUIRED") for item in loaded.warnings))

    def test_lifecycle_service_separates_new_from_restore(self):
        lifecycle = TransactionSessionLifecycleService(self.app)
        new = lifecycle.create_new("P.MM.01", "P.MM.01.TRN.004")
        new.generate_initial_message()
        snapshot = new.create_snapshot()
        restored = lifecycle.restore_existing(snapshot)
        self.assertTrue(restored.continue_ready)
        self.assertEqual(restored.session.transaction.conversation_id, new.transaction.conversation_id)
        another = lifecycle.create_new("P.MM.01", "P.MM.01.TRN.004")
        self.assertNotEqual(another.transaction.conversation_id, new.transaction.conversation_id)
        self.assertNotEqual(another.transaction.procedure_instance.procedure_id,
                            new.transaction.procedure_instance.procedure_id)


if __name__ == "__main__":
    unittest.main()
