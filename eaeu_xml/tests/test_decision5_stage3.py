from dataclasses import replace
from datetime import datetime, timedelta, timezone
from xml.etree import ElementTree as ET
import unittest

from eaeu_xml.core.enums import SignalKind, TimeoutKind, TimeoutOutcome, TransactionPattern, TransactionState
from eaeu_xml.core.errors import FaultValidationError, IntegrationOwnershipError, IntegrationValidationError, InvalidStateTransitionError, RetryNotAllowedError
from eaeu_xml.core.namespaces import NamespaceRegistry
from eaeu_xml.decision5.models import (AcceptTime, DummyBodyPayload, FaultAction, FaultReasonText, FaultSubcode, IntegrationMetadata, LogicalAddress, ProblemMessage, ProcedureId, ProcedureInstance, SignalError, SignalErrorCode, SignalPayload, SoapFault, TrackId, TransactionDefinition, TransactionInstance, TransactionParameters)
from eaeu_xml.services.fault_factory import FaultFactory
from eaeu_xml.services.identifier_service import IdentifierService
from eaeu_xml.services.message_factory import MessageFactory
from eaeu_xml.services.platform_context import IntegrationPlatformContext
from eaeu_xml.services.signal_factory import SignalFactory
from eaeu_xml.services.transaction_engine import RetryService, TransactionEngine
from eaeu_xml.services.xml_serializer import XmlSerializer
from eaeu_xml.decision5.validation.integration_validator import IntegrationOwnershipValidator


class Decision5Stage3Tests(unittest.TestCase):
    def setUp(self):
        self.ids = IdentifierService()
        procedure = ProcedureInstance("P.SP.03.PRC.001", ProcedureId.root(self.ids))
        self.transaction = TransactionInstance("P.SP.03.TRN.002", self.ids.new_conversation_id(), procedure)
        self.to = LogicalAddress.parse("EAEU://EEC/CP/P.SP.03/P.ACT.001")
        self.reply = LogicalAddress.parse("EAEU://RU/CP/P.SP.03/P.SP.03.ACT.002")
        self.message = MessageFactory(self.ids).create_initial_application_message(transaction=self.transaction, process_code="P.SP.03", process_version="0.1", message_code="P.CC.04.MSG.003", to=self.to, reply_to=self.reply, body_payload=DummyBodyPayload("payload"))

    def test_platform_integration(self):
        metadata = IntegrationMetadata(TrackId("urn:uuid:00000000-0000-4000-8000-000000000001"), AcceptTime(datetime(2026, 8, 20, tzinfo=timezone.utc)))
        root = ET.fromstring(XmlSerializer().serialize_application(IntegrationPlatformContext().enrich(self.message, metadata)))
        ns = NamespaceRegistry(); integration = root.find(f".//{{{ns.INT}}}Integration")
        self.assertEqual(integration.find(f"{{{ns.INT}}}TrackID").text, metadata.track_id.serialize())
        self.assertTrue(integration.find(f"{{{ns.INT}}}AcceptTime").text.endswith("Z"))

    def test_invalid_integration_values(self):
        for value in ("not-a-uri", "http://example.test/track", "urn:uuid:not-a-uuid"):
            with self.subTest(value=value), self.assertRaises(IntegrationValidationError): TrackId(value)
        with self.assertRaises(IntegrationValidationError): AcceptTime(datetime(2026, 1, 1))
        with self.assertRaises(IntegrationValidationError): AcceptTime(datetime(2026, 1, 1, tzinfo=timezone(timedelta(hours=3))))
        with self.assertRaises(IntegrationOwnershipError): IntegrationOwnershipValidator().validate_application_input(object())

    def test_signal_messages(self):
        for kind in (SignalKind.RECEIVED, SignalKind.ACCEPTED_FOR_PROCESSING):
            with self.subTest(kind=kind):
                signal = SignalFactory(self.ids).create(transaction=self.transaction, source_message=self.message, kind=kind, to=self.reply, reply_to=self.to)
                self.assertEqual(signal.header.action.signal_code, kind.value)
                self.assertNotEqual(signal.header.message_id, self.message.header.message_id)
                self.assertEqual(signal.header.relates_to.message_id, self.message.header.message_id)
                ET.fromstring(XmlSerializer().serialize_signal(signal))

    def test_error_signal_codes(self):
        for code in (*SignalErrorCode, "P.TEST.01.RULE.001"):
            error = SignalError(code, "Описание")
            payload = SignalPayload(SignalKind.ERROR, self.ids.new_signal_id(), datetime.now(timezone.utc), (error,))
            self.assertEqual(payload.errors[0].code, code)
        with self.assertRaises(Exception): SignalPayload(SignalKind.ERROR, self.ids.new_signal_id(), datetime.now(timezone.utc))
        with self.assertRaises(Exception): SignalPayload(SignalKind.RECEIVED, self.ids.new_signal_id(), datetime.now(timezone.utc), (SignalError(SignalErrorCode.DATA_ERROR, "Ошибка"),))
        signal = SignalFactory(self.ids).create(transaction=self.transaction, source_message=self.message, kind=SignalKind.ERROR, to=self.reply, reply_to=self.to, errors=(SignalError(SignalErrorCode.DATA_ERROR, "Ошибка данных"),))
        root = ET.fromstring(XmlSerializer().serialize_signal(signal)); ns = NamespaceRegistry()
        self.assertIsNotNone(root.find(f".//{{{ns.SIGNAL}}}ValidationError"))
        self.assertEqual(root.find(f".//{{{ns.SIGNAL}}}Code").text, "Common:DataError")

    def _fault(self, subcode=FaultSubcode.INVALID_HEADER, problem=None, wsa=False):
        body = SoapFault(subcode, (FaultReasonText("Некорректный заголовок", "ru"),), problem)
        return FaultFactory(self.ids).create(source_message=self.message, sender=self.to, fault=body, wsa_fault=wsa)

    def test_fault_header_and_xml_attributes(self):
        fault = self._fault(); self.assertNotEqual(fault.header.message_id, self.message.header.message_id)
        self.assertIsNone(fault.header.reply_to); self.assertIsNone(fault.header.fault_to)
        root = ET.fromstring(XmlSerializer().serialize_fault(fault)); ns = NamespaceRegistry()
        relates = root.find(f".//{{{ns.WSA}}}RelatesTo")
        self.assertEqual(relates.text, self.message.header.message_id.serialize())
        self.assertEqual(relates.attrib[f"{{{ns.INT}}}RelatesAction"], self.message.header.action.serialize())
        reason = root.find(f".//{{{ns.SOAP}}}Text")
        self.assertEqual(reason.attrib["{http://www.w3.org/XML/1998/namespace}lang"], "ru")
        self.assertIsNone(root.find(f".//{{{ns.INT}}}RelatesAction"))

    def test_fault_actions_and_codes(self):
        self.assertTrue(FaultAction(FaultAction.WSA).serialize().endswith("/fault"))
        self.assertTrue(FaultAction(FaultAction.GENERIC).serialize().endswith("/soap/fault"))
        self.assertEqual(FaultSubcode.INTERNAL_ERROR.soap_code, "soap:Receiver")
        self.assertEqual(FaultSubcode.DATA_ERROR.soap_code, "soap:Sender")

    def test_fault_reason_and_problem_message(self):
        with self.assertRaises(FaultValidationError): SoapFault(FaultSubcode.DATA_ERROR, (FaultReasonText("Error", "en"),))
        with self.assertRaises(FaultValidationError): SoapFault(FaultSubcode.DATA_ERROR, (FaultReasonText("Ошибка", "ru"), FaultReasonText("Другая", "ru")))
        fault = self._fault(FaultSubcode.DATA_ERROR, ProblemMessage(ET.fromstring("<bad><x /></bad>")))
        root = ET.fromstring(XmlSerializer().serialize_fault(fault)); ns = NamespaceRegistry()
        problem = root.find(f".//{{{ns.INT}}}ProblemMessage")
        self.assertEqual(ET.fromstring(problem.text).tag, "bad")

    def make_transaction(self, pattern, guaranteed=False, retries=1, receive=True):
        ids = IdentifierService()
        definition = TransactionDefinition(pattern, TransactionParameters(receive_confirmation_timeout=timedelta(seconds=1) if receive else None, processing_confirmation_timeout=timedelta(seconds=1) if guaranteed else None, response_timeout=timedelta(seconds=1), retry_count=retries), guaranteed)
        procedure = ProcedureInstance("P.SP.03.PRC.001", ProcedureId.root(ids))
        return ids, TransactionInstance("P.SP.03.TRN.002", ids.new_conversation_id(), procedure, definition=definition)

    def test_all_pattern_start_states(self):
        cases = ((TransactionPattern.MUTUAL_OBLIGATIONS, True, TransactionState.WAITING_RECEIVED), (TransactionPattern.QUESTION_RESPONSE, False, TransactionState.WAITING_RESPONSE), (TransactionPattern.REQUEST_RESPONSE, False, TransactionState.WAITING_RESPONSE), (TransactionPattern.REQUEST_RESPONSE, True, TransactionState.WAITING_RECEIVED), (TransactionPattern.REQUEST_CONFIRMATION, False, TransactionState.WAITING_RESPONSE), (TransactionPattern.REQUEST_CONFIRMATION, True, TransactionState.WAITING_RESPONSE), (TransactionPattern.NOTIFICATION, True, TransactionState.WAITING_RECEIVED), (TransactionPattern.INFORMATION_DISTRIBUTION, False, TransactionState.COMPLETED))
        for pattern, guaranteed, expected in cases:
            with self.subTest(pattern=pattern, guaranteed=guaranteed):
                _, transaction = self.make_transaction(pattern, guaranteed)
                self.assertIs(TransactionEngine().start_transaction(transaction), expected)

    def test_guaranteed_request_response_and_invalid_transition(self):
        _, transaction = self.make_transaction(TransactionPattern.REQUEST_RESPONSE, True)
        engine = TransactionEngine(); engine.start_transaction(transaction)
        self.assertIs(engine.receive_signal(transaction, SignalKind.RECEIVED), TransactionState.WAITING_PROCESSING)
        self.assertIs(engine.receive_signal(transaction, SignalKind.ACCEPTED_FOR_PROCESSING), TransactionState.WAITING_RESPONSE)
        self.assertIs(engine.receive_application_message(transaction), TransactionState.COMPLETED)
        with self.assertRaises(InvalidStateTransitionError): engine.receive_application_message(transaction)

    def test_notification_and_distribution_completion(self):
        _, notification = self.make_transaction(TransactionPattern.NOTIFICATION, True)
        engine = TransactionEngine(); engine.start_transaction(notification)
        self.assertIs(engine.receive_signal(notification, SignalKind.RECEIVED), TransactionState.COMPLETED)
        _, distribution = self.make_transaction(TransactionPattern.INFORMATION_DISTRIBUTION)
        self.assertIs(engine.start_transaction(distribution), TransactionState.COMPLETED)

    def test_request_confirmation_guaranteed_completion(self):
        _, transaction = self.make_transaction(TransactionPattern.REQUEST_CONFIRMATION, True)
        engine = TransactionEngine(); engine.start_transaction(transaction)
        self.assertIs(engine.receive_application_message(transaction), TransactionState.WAITING_RESPONSE_RECEIVED)
        self.assertIs(engine.send_signal(transaction, SignalKind.RECEIVED), TransactionState.COMPLETED)

    def test_mutual_obligations_full_sequence_and_rollback(self):
        _, transaction = self.make_transaction(TransactionPattern.MUTUAL_OBLIGATIONS, True)
        engine = TransactionEngine(); engine.start_transaction(transaction)
        self.assertIs(engine.receive_signal(transaction, SignalKind.RECEIVED), TransactionState.WAITING_PROCESSING)
        self.assertIs(engine.receive_signal(transaction, SignalKind.ACCEPTED_FOR_PROCESSING), TransactionState.WAITING_RESPONSE)
        self.assertIs(engine.receive_application_message(transaction), TransactionState.WAITING_RESPONSE_RECEIVED)
        self.assertIs(engine.send_signal(transaction, SignalKind.RECEIVED), TransactionState.WAITING_RESPONSE_PROCESSING)
        self.assertIs(engine.send_signal(transaction, SignalKind.ACCEPTED_FOR_PROCESSING), TransactionState.WAITING_FINAL_ERROR_WINDOW)
        self.assertIs(engine.handle_timeout(transaction, TimeoutKind.PROCESSING_CONFIRMATION), TimeoutOutcome.COMPLETE)
        _, failed = self.make_transaction(TransactionPattern.MUTUAL_OBLIGATIONS, True)
        engine.start_transaction(failed)
        self.assertIs(engine.receive_signal(failed, SignalKind.ERROR), TransactionState.ROLLBACK_REQUIRED)

    def test_timeout_and_retry_metadata(self):
        ids, transaction = self.make_transaction(TransactionPattern.QUESTION_RESPONSE, retries=1)
        engine = TransactionEngine(); engine.start_transaction(transaction)
        self.assertIs(engine.handle_timeout(transaction, TimeoutKind.RESPONSE), TimeoutOutcome.RETRY)
        transaction.retry_attempts = 1
        self.assertIs(engine.handle_timeout(transaction, TimeoutKind.RESPONSE), TimeoutOutcome.FAIL)
        self.transaction.definition = TransactionDefinition(TransactionPattern.QUESTION_RESPONSE, TransactionParameters(retry_count=1))
        record = self.transaction.message_history[0]
        retry = RetryService().retry_record(self.transaction, record, ids.new_message_id())
        self.assertNotEqual(retry.message_id, record.message_id); self.assertEqual(retry.retry_of, record.message_id)
        self.assertEqual(retry.attempt_number, 2); self.assertEqual(retry.action, record.action)
        with self.assertRaises(RetryNotAllowedError): RetryService().retry_record(self.transaction, record, ids.new_message_id())
        _, completed = self.make_transaction(TransactionPattern.INFORMATION_DISTRIBUTION)
        TransactionEngine().start_transaction(completed); completed.message_history.append(record)
        with self.assertRaises(RetryNotAllowedError): RetryService().retry_record(completed, record, ids.new_message_id())

    def test_invalid_transaction_parameters(self):
        with self.assertRaises(Exception): TransactionParameters(response_timeout=timedelta(0))
        with self.assertRaises(Exception): TransactionParameters(retry_count=-1)

    def test_ten_reference_xml_examples_are_well_formed(self):
        serializer = XmlSerializer()
        followup = MessageFactory(self.ids).create_followup_application_message(transaction=self.transaction, process_code="P.SP.03", process_version="0.1", message_code="P.CC.04.MSG.004", to=self.reply, reply_to=self.to, body_payload=DummyBodyPayload("followup"))
        enriched = IntegrationPlatformContext().enrich(self.message, IntegrationPlatformContext().create_metadata())
        rcv = SignalFactory(self.ids).create(transaction=self.transaction, source_message=self.message, kind=SignalKind.RECEIVED, to=self.reply, reply_to=self.to)
        prs = SignalFactory(self.ids).create(transaction=self.transaction, source_message=self.message, kind=SignalKind.ACCEPTED_FOR_PROCESSING, to=self.reply, reply_to=self.to)
        err = SignalFactory(self.ids).create(transaction=self.transaction, source_message=self.message, kind=SignalKind.ERROR, to=self.reply, reply_to=self.to, errors=(SignalError(SignalErrorCode.FATAL_ERROR, "Неустранимая ошибка"),))
        child = self.transaction.procedure_instance.start_child("P.SP.03.PRC.002", self.ids)
        nested_tx = TransactionInstance("P.SP.03.TRN.002", self.ids.new_conversation_id(), child)
        nested = MessageFactory(self.ids).create_initial_application_message(transaction=nested_tx, process_code="P.SP.03", process_version="0.1", message_code="P.CC.04.MSG.003", to=self.to, reply_to=self.reply, body_payload=DummyBodyPayload("nested"))
        retry = replace(self.message, header=replace(self.message.header, message_id=self.ids.new_message_id()))
        documents = (serializer.serialize_application(self.message), serializer.serialize_application(followup), serializer.serialize_application(enriched), serializer.serialize_signal(rcv), serializer.serialize_signal(prs), serializer.serialize_signal(err), serializer.serialize_fault(self._fault(wsa=True)), serializer.serialize_fault(self._fault()), serializer.serialize_application(nested), serializer.serialize_application(retry))
        self.assertEqual(len(documents), 10)
        for xml in documents: ET.fromstring(xml)


if __name__ == "__main__": unittest.main()
