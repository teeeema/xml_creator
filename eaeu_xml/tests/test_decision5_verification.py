from dataclasses import replace
from pathlib import Path
from xml.etree import ElementTree as ET
import unittest

from eaeu_xml.core.errors import CorrelationError, FaultValidationError, IdentifierValidationError, SignalValidationError
from eaeu_xml.core.namespaces import NamespaceRegistry
from eaeu_xml.decision5.models import ConversationId, FaultReasonText, FaultSubcode, RelatesTo, SoapFault
from eaeu_xml.decision5.validation.correlation_validator import CorrelationValidator
from eaeu_xml.services.fault_factory import FaultFactory
from eaeu_xml.services.identifier_service import IdentifierService
from eaeu_xml.services.xml_serializer import XmlSerializer
from eaeu_xml.verification import Decision5RuleCoverage
import test_decision5_stage3


class Decision5VerificationTests(unittest.TestCase):
    def setUp(self):
        test_decision5_stage3.Decision5Stage3Tests.setUp(self)
    def test_every_confirmed_rule_has_source_implementation_and_test(self):
        root = Path(__file__).parents[1]
        coverage = Decision5RuleCoverage.build(root)
        self.assertEqual(coverage.summary, {"total_rules": 45, "verified": 45, "unresolved": 0, "mismatches": 0, "missing_tests": 0})

    def test_fault_rejects_reused_id_missing_or_wrong_correlation(self):
        body = SoapFault(FaultSubcode.INTERNAL_ERROR, (FaultReasonText("Ошибка", "ru"),))
        fault = FaultFactory(self.ids).create(source_message=self.message, sender=self.to, fault=body)
        serializer = XmlSerializer()
        cases = (
            replace(fault, header=replace(fault.header, message_id=self.message.header.message_id)),
            replace(fault, header=replace(fault.header, relates_to=None)),
            replace(fault, header=replace(fault.header, relates_to=RelatesTo(self.message.header.message_id, "wrong"))),
        )
        for item in cases:
            with self.subTest(item=item), self.assertRaises(FaultValidationError): serializer.serialize_fault(item)

    def test_signal_structure_matches_appendix_5_sequence(self):
        signal = __import__("eaeu_xml.services.signal_factory", fromlist=["SignalFactory"]).SignalFactory(self.ids).create(
            transaction=self.transaction, source_message=self.message,
            kind=__import__("eaeu_xml.core.enums", fromlist=["SignalKind"]).SignalKind.RECEIVED,
            to=self.reply, reply_to=self.to,
        )
        root = ET.fromstring(XmlSerializer().serialize_signal(signal)); ns = NamespaceRegistry()
        receipt = root.find(f".//{{{ns.SIGNAL}}}DeliveryReceipt")
        self.assertEqual([child.tag for child in receipt], [f"{{{ns.SIGNAL}}}SignalId", f"{{{ns.SIGNAL}}}DateTime"])
        with self.assertRaises(SignalValidationError):
            XmlSerializer().serialize_signal(replace(signal, header=replace(signal.header, relates_to=None)))

    def test_negative_identifier_and_correlation_matrix(self):
        with self.assertRaises(IdentifierValidationError): ConversationId.parse("bad")
        initial = self.transaction.message_history[0]
        self.transaction.message_history.append(replace(initial, sequence_number=2, relates_to=initial.message_id))
        with self.assertRaises(CorrelationError): CorrelationValidator().validate_history(self.transaction)
        self.transaction.message_history[:] = [replace(initial, relates_to=initial.message_id)]
        with self.assertRaises(CorrelationError): CorrelationValidator().validate_history(self.transaction)

    def test_fault_subcode_is_closed_and_attributes_are_not_elements(self):
        with self.assertRaises(ValueError): FaultSubcode("int:Invented")
        fault = FaultFactory(self.ids).create(source_message=self.message, sender=self.to, fault=SoapFault(FaultSubcode.DATA_ERROR, (FaultReasonText("Ошибка", "ru"),)))
        root = ET.fromstring(XmlSerializer().serialize_fault(fault)); ns = NamespaceRegistry()
        self.assertIsNone(root.find(f".//{{{ns.INT}}}RelatesAction"))
        self.assertIsNone(root.find(".//lang"))


if __name__ == "__main__": unittest.main()
