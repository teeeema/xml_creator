from dataclasses import replace
from xml.etree import ElementTree as ET
import unittest

from pathlib import Path

from eaeu_xml.core.errors import (
    ActionValidationError, AddressValidationError, ForbiddenHeaderFieldError,
    IdentifierValidationError, MissingRequiredHeaderFieldError, ProcedureIdError, CorrelationError,
)
from eaeu_xml.core.namespaces import NamespaceRegistry
from eaeu_xml.decision5.models import (
    ApplicationAction, ConversationId, DummyBodyPayload, EndpointReference, LogicalAddress,
    MessageId, ProcedureId, ProcedureInstance, TransactionInstance,
)
from eaeu_xml.decision5.models.address import ServiceResourceId
from eaeu_xml.decision5.validation.header_validator import HeaderValidator
from eaeu_xml.services.identifier_service import IdentifierService
from eaeu_xml.services.message_factory import MessageFactory
from eaeu_xml.services.xml_serializer import XmlSerializer


class Decision5CoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ids = IdentifierService()
        self.procedure = ProcedureInstance("P.SP.03.PRC.001", ProcedureId.root(self.ids))
        self.transaction = TransactionInstance("P.SP.03.TRN.002", self.ids.new_conversation_id(), self.procedure)
        self.to = LogicalAddress.parse("EAEU://EEC/CP/P.SP.03/P.ACT.001")
        self.reply = LogicalAddress.parse("EAEU://RU/CP/P.SP.03/P.SP.03.ACT.002")
        self.factory = MessageFactory(self.ids)

    def _initial(self):
        return self.factory.create_initial_application_message(
            transaction=self.transaction, process_code="P.SP.03", process_version="0.1",
            message_code="P.CC.04.MSG.003", to=self.to, reply_to=self.reply,
            body_payload=DummyBodyPayload("initial & payload"),
        )

    def test_namespaces_match_decision_5_table_1(self) -> None:
        namespaces = NamespaceRegistry()
        self.assertEqual(namespaces.SOAP, "http://www.w3.org/2003/05/soap-envelope")
        self.assertEqual(namespaces.WSA, "http://www.w3.org/2005/08/addressing")
        self.assertEqual(namespaces.INT, "urn:EEC:Interaction:v1.0")

    def test_envelope_namespace_declarations_are_grouped_and_one_per_line(self):
        class Payload:
            def serialize_xml_element(self):
                ET.register_namespace("payload","urn:test:payload:vY.Y.Y"); ET.register_namespace("model","urn:test:model:vX.X.X")
                root=ET.Element("{urn:test:payload:vY.Y.Y}Root"); ET.SubElement(root,"{urn:test:model:vX.X.X}Value").text="TEST"; return root
        message=self.factory.create_initial_application_message(transaction=self.transaction,process_code="P.SP.03",process_version="0.1",
            message_code="P.CC.04.MSG.003",to=self.to,reply_to=self.reply,body_payload=Payload())
        xml=XmlSerializer().serialize_application(message); start=xml.index("<soap:Envelope"); opening=xml[start:xml.index(">",start)]
        for prefix in ("soap","wsa","int","payload","model"):
            self.assertRegex(opening,rf"(?m)^    xmlns:{prefix}=")
        self.assertIn('xmlns:int="urn:EEC:Interaction:v1.0"\n\n    xmlns:',opening)

    def test_placeholder_comment_is_data_driven_positioned_and_well_formed(self):
        message=self._initial(); serializer=XmlSerializer()
        xml=serializer.serialize_application(message,placeholder_versions=("Y.Y.Y",))
        self.assertIn("Y.Y.Y — версия структуры электронного документа",xml)
        self.assertIn("X.X.X — версия базисной модели данных",xml)
        self.assertIn("Коллегии ЕЭК от 25.10.2016 № 122",xml)
        envelope_end=xml.index(">",xml.index("<soap:Envelope")); comment=xml.index("<!--",envelope_end); header=xml.index("<soap:Header",comment)
        self.assertLess(envelope_end,comment); self.assertLess(comment,header); ET.fromstring(xml)
        concrete=serializer.serialize_application(message)
        self.assertNotIn("normative placeholders",concrete); self.assertNotIn("TEST ONLY:",concrete); ET.fromstring(concrete)

    def test_message_and_conversation_ids_are_uuid_uris(self) -> None:
        first, second = self.ids.new_message_id(), self.ids.new_message_id()
        self.assertNotEqual(first, second)
        self.assertEqual(MessageId.parse(first.serialize()), first)
        conversation = self.ids.new_conversation_id()
        self.assertEqual(ConversationId.parse(conversation.serialize()), conversation)
        self.assertTrue(first.serialize().startswith("urn:uuid:"))

    def test_invalid_identifier_uri_is_rejected(self) -> None:
        for value in ("not-a-uuid", "urn:uuid:not-a-uuid"):
            with self.assertRaises(IdentifierValidationError):
                MessageId.parse(value)

    def test_nested_procedure_id_is_immutable_and_roundtrips(self) -> None:
        root = self.procedure.procedure_id
        child = root.child(self.ids)
        grandchild = child.child(self.ids)
        self.assertEqual((root.depth, child.depth, grandchild.depth), (1, 2, 3))
        self.assertEqual(grandchild.parent(), child)
        self.assertEqual(ProcedureId.parse(grandchild.serialize()), grandchild)
        self.assertEqual(root.depth, 1)

    def test_damaged_procedure_chain_is_rejected(self) -> None:
        with self.assertRaises(ProcedureIdError):
            ProcedureId.parse("urn:uuid:00000000-0000-0000-0000-000000000000//bad")

    def test_child_procedure_instance_keeps_parent(self) -> None:
        child = self.procedure.start_child("P.SP.03.PRC.002", self.ids)
        self.assertIs(child.parent, self.procedure)
        self.assertEqual(child.procedure_id.parent(), self.procedure.procedure_id)

    def test_cp_ca_sr_address_roundtrip(self) -> None:
        values = (
            "EAEU://RU/CP/P.SP.03/P.SP.03.ACT.002/AUTH-1",
            "EAEU://RU/CA/AUTH-1",
            "EAEU://EEC/SR/gate",
        )
        for value in values:
            self.assertEqual(LogicalAddress.parse(value).serialize(), value)
        sr = LogicalAddress.parse(values[-1])
        self.assertIsInstance(sr.participant_identifier, ServiceResourceId)
        self.assertTrue(sr.participant_identifier.identifier_validated)

    def test_segment_membership_is_not_inferred_from_syntax(self) -> None:
        address = LogicalAddress.parse("EAEU://ZZ/CA/AUTH")
        self.assertTrue(address.syntax_valid)
        self.assertFalse(address.membership_validated)

    def test_invalid_addresses_are_rejected(self) -> None:
        for value in ("http://RU/CA/A", "EAEU://RUS/CA/A", "EAEU://RU/XX/A", "EAEU://RU/CP/ONE"):
            with self.assertRaises(AddressValidationError):
                LogicalAddress.parse(value)

    def test_action_build_parse_and_serialize(self) -> None:
        action = ApplicationAction.build(
            process_code="P.SP.03", process_version="0.1", procedure_code="P.SP.03.PRC.001",
            transaction_code="P.SP.03.TRN.002", message_code="P.CC.04.MSG.003",
        )
        expected = "int://CP/P.SP.03/0.1/P.SP.03.PRC.001/P.SP.03.TRN.002/P.CC.04.MSG.003"
        self.assertEqual(action.serialize(), expected)
        self.assertEqual(ApplicationAction.parse(expected), action)

    def test_malformed_or_inconsistent_action_is_rejected(self) -> None:
        with self.assertRaises(ActionValidationError):
            ApplicationAction.parse("int://CP/bad")
        with self.assertRaises(ActionValidationError):
            ApplicationAction("P.SP.03", "0.1", "P.XX.01.PRC.001", "P.SP.03.TRN.002", "P.CC.04.MSG.003")

    def test_initial_and_followup_correlation(self) -> None:
        initial = self._initial()
        followup = self.factory.create_followup_application_message(
            transaction=self.transaction, process_code="P.SP.03", process_version="0.1",
            message_code="P.CC.04.MSG.004", to=self.reply, reply_to=self.to,
            body_payload=DummyBodyPayload("follow-up"),
        )
        self.assertIsNone(initial.header.relates_to)
        self.assertEqual(followup.header.relates_to.message_id, initial.header.message_id)
        self.assertNotEqual(followup.header.message_id, initial.header.message_id)
        self.assertEqual(followup.header.procedure_id, initial.header.procedure_id)
        self.assertEqual(followup.header.conversation_id, initial.header.conversation_id)
        self.assertEqual(len(self.transaction.message_history), 2)

    def test_forbidden_application_headers_raise_domain_errors(self) -> None:
        message = self._initial()
        with self.assertRaises(ForbiddenHeaderFieldError):
            HeaderValidator().validate_application(replace(message.header, from_=EndpointReference(self.reply)))
        with self.assertRaises(ForbiddenHeaderFieldError):
            HeaderValidator().validate_application(replace(message.header, fault_to=EndpointReference(self.reply)))
        with self.assertRaises(ForbiddenHeaderFieldError):
            HeaderValidator().validate_application(replace(message.header, integration=object()))
        with self.assertRaises(MissingRequiredHeaderFieldError):
            HeaderValidator().validate_application(replace(message.header, to=None))

    def test_transaction_state_rejects_invalid_initial_and_followup_calls(self) -> None:
        with self.assertRaises(CorrelationError):
            self.factory.create_followup_application_message(
                transaction=self.transaction, process_code="P.SP.03", process_version="0.1",
                message_code="P.CC.04.MSG.004", to=self.reply, reply_to=self.to,
                body_payload=DummyBodyPayload("bad"),
            )
        self._initial()
        with self.assertRaises(CorrelationError):
            self._initial()

    def test_source_registry_contains_traceability_fields(self) -> None:
        source = Path(__file__).parents[1] / "src/eaeu_xml/decision5/rules/source_rules.yaml"
        text = source.read_text(encoding="utf-8")
        self.assertEqual(text.count("rule_id:"), 45)
        for key in ("entity:", "condition:", "status:", "description:", "source_document:", "source_paragraph:", "notes:"):
            self.assertGreaterEqual(text.count(key), 21)

    def test_soap_serialization_is_well_formed_and_deterministic(self) -> None:
        message = self._initial()
        serializer = XmlSerializer()
        first = serializer.serialize_application(message)
        second = serializer.serialize_application(message)
        self.assertEqual(first, second)
        root = ET.fromstring(first)
        ns = NamespaceRegistry()
        self.assertEqual(root.tag, f"{{{ns.SOAP}}}Envelope")
        self.assertIsNotNone(root.find(f"{{{ns.SOAP}}}Header"))
        self.assertIsNotNone(root.find(f"{{{ns.SOAP}}}Body"))
        self.assertNotIn("<wsa:From>", first)
        self.assertNotIn("<wsa:FaultTo>", first)
        self.assertLess(first.index("<wsa:To>"), first.index("<wsa:ReplyTo>"))
        self.assertLess(first.index("<wsa:MessageID>"), first.index("<wsa:Action>"))
        self.assertIn("initial &amp; payload", first)
        self.assertIn("<test:Payload>", first)

    def test_followup_xml_contains_relates_to_in_normative_order(self) -> None:
        initial = self._initial()
        followup = self.factory.create_followup_application_message(
            transaction=self.transaction, process_code="P.SP.03", process_version="0.1",
            message_code="P.CC.04.MSG.004", to=self.reply, reply_to=self.to,
            body_payload=DummyBodyPayload("next"),
        )
        xml = XmlSerializer().serialize_application(followup)
        self.assertIn(initial.header.message_id.serialize(), xml)
        self.assertLess(xml.index("<wsa:RelatesTo>"), xml.index("<wsa:Action>"))
        self.assertNotIn("RelatesAction", xml)


if __name__ == "__main__":
    unittest.main()
