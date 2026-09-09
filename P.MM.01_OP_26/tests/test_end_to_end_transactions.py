from pathlib import Path
import unittest
from uuid import UUID
from xml.etree import ElementTree as ET

from eaeu_xml.core.errors import UnresolvedStructureVersionError
from eaeu_xml.core.namespaces import NamespaceRegistry
from eaeu_xml.decision5.models import ConversationId, MessageId, ProcedureId, ProcedureInstance, TransactionInstance
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.services.message_factory import MessageFactory
from eaeu_xml.services.logical_address_builder import LogicalAddressBuilder
from eaeu_xml.services.xml_serializer import XmlSerializer


PACKAGE = Path(__file__).parents[1]
EXAMPLES = PACKAGE / "examples/p_mm_01"


class FixedIdentifierService:
    def __init__(self, start: int) -> None:
        self.next_value = start

    def _uuid(self) -> UUID:
        value = UUID(int=self.next_value); self.next_value += 1
        return value

    def new_procedure_component(self) -> UUID: return self._uuid()
    def new_conversation_id(self) -> ConversationId: return ConversationId(self._uuid())
    def new_message_id(self) -> MessageId: return MessageId(self._uuid())


def sample_value(field):
    datatype = (field.datatype or "").lower()
    if field.kind == "ARBITRARY_XML": return ET.Element("{urn:test:external}Payload")
    if "indicator" in datatype: return True
    if "datetime" in datatype: return "2026-08-24T00:00:00"
    if datatype.endswith("datetype"): return "2026-08-24"
    if "quantity" in datatype or "integer" in datatype: return 1
    if "unifiedcountry" in datatype: return "RU"
    return "TEST"


def minimal_values(engine: EaeuXmlEngine, message_code: str) -> dict:
    structure = engine.get_structure(message_code,mode=GenerationMode.TEST)
    parents = {field.parent for field in structure.fields if field.parent}
    included: set[str] = set(); values = {}
    for field in sorted(structure.fields, key=lambda item: item.order):
        required = ((field.parent is None) or (field.parent in included)) and (field.min_occurs or 0) > 0
        if not required: continue
        included.add(field.field_id)
        value = None if field.field_id in parents else sample_value(field)
        values[field.path] = [value] * field.min_occurs if field.min_occurs and field.min_occurs > 1 else value
    message = engine.get_message(message_code)
    suffix = int(message_code.rsplit(".", 1)[-1])
    for field in structure.fields:
        if field.xml_name == "InfEnvelopeCode": values[field.path] = message_code
        elif field.xml_name == "EDocCode": values[field.path] = message.structure_id
        elif field.xml_name == "EDocId": values[field.path] = f"00000000-0000-0000-0000-{suffix:012d}"
    return values


class Pmm01EndToEndTransactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = EaeuXmlEngine.load_process(PACKAGE)
        builder=LogicalAddressBuilder()
        cls.to = builder.build_common_process(segment="EEC",process_code="P.MM.01",participant_code="P.ACT.001")
        cls.reply = builder.build_common_process(segment="RU",process_code="P.MM.01",participant_code="P.MM.01.ACT.001")

    def assert_catalog(self, transaction_code, procedure_code, initiating, responses):
        transaction = self.engine.get_transaction(transaction_code)
        self.assertEqual(transaction.procedure_code, procedure_code)
        self.assertEqual(transaction.initiating_message, initiating)
        self.assertEqual(set(transaction.response_messages), set(responses))
        return transaction

    def test_trn004_placeholder_test_xml_and_strict_block(self):
        self.assert_catalog("P.MM.01.TRN.004", "P.MM.01.PRC.007", "P.MM.01.MSG.005", ["P.MM.01.MSG.006"])
        action = self.engine.build_application_action("P.MM.01.TRN.004", "P.MM.01.MSG.005")
        self.assertEqual(action.serialize(), "int://CP/P.MM.01/1.1.0/P.MM.01.PRC.007/P.MM.01.TRN.004/P.MM.01.MSG.005")
        self.assertIn(("R.007", "Y.Y.Y"), self.engine.structures)
        self.assertEqual(self.engine.build_application_action("P.MM.01.TRN.004", "P.MM.01.MSG.006").message_code, "P.MM.01.MSG.006")
        request_xml,response_xml=self.run_resolved_branch("P.MM.01.TRN.004","P.MM.01.PRC.007","P.MM.01.MSG.005","P.MM.01.MSG.006",400)
        for xml in (request_xml,response_xml):
            self.assertIn("vY.Y.Y",xml); self.assertIn("vX.X.X",xml)
        for message_code in ("P.MM.01.MSG.005","P.MM.01.MSG.006"):
            with self.assertRaises(UnresolvedStructureVersionError) as raised:
                self.engine.get_structure(message_code,mode=GenerationMode.STRICT)
            self.assertEqual(raised.exception.code, "UNRESOLVED_STRUCTURE_VERSION")
        self.assertEqual(self.engine.get_transaction("P.MM.01.TRN.004").initiating_participant,"P.MM.01.ACT.001")
        self.assertEqual(self.engine.get_transaction("P.MM.01.TRN.004").responding_participant,"P.ACT.001")

    def run_resolved_branch(self, transaction_code, procedure_code, request_code, response_code, seed):
        ids = FixedIdentifierService(seed)
        procedure = ProcedureInstance(procedure_code, ProcedureId.root(ids))
        transaction = TransactionInstance(transaction_code, ids.new_conversation_id(), procedure)
        factory = MessageFactory(ids); serializer = XmlSerializer()
        request_values = minimal_values(self.engine, request_code)
        response_values = minimal_values(self.engine, response_code)
        request_edoc_id = next(value for path, value in request_values.items() if path.endswith("/EDocId"))
        response_structure = self.engine.get_structure(response_code,mode=GenerationMode.TEST)
        response_ref_path = next((field.path for field in response_structure.fields if field.xml_name == "EDocRefId"), None)
        if response_ref_path: response_values[response_ref_path] = request_edoc_id
        self.assertTrue(self.engine.validate_body(request_code, request_values, mode=GenerationMode.TEST).is_valid)
        self.assertTrue(self.engine.validate_body(response_code, response_values, mode=GenerationMode.TEST).is_valid)
        request = factory.create_initial_application_message(
            transaction=transaction, process_code="P.MM.01", process_version="1.1.0",
            message_code=request_code, to=self.to, reply_to=self.reply,
            body_payload=self.engine.build_body(request_code, request_values, mode=GenerationMode.TEST),
        )
        response = factory.create_followup_application_message(
            transaction=transaction, process_code="P.MM.01", process_version="1.1.0",
            message_code=response_code, to=self.reply, reply_to=self.to,
            body_payload=self.engine.build_body(response_code, response_values, mode=GenerationMode.TEST),
        )
        request_resolution=self.engine.resolve_structure(self.engine.get_message(request_code).structure_id,mode=GenerationMode.TEST)
        response_resolution=self.engine.resolve_structure(self.engine.get_message(response_code).structure_id,mode=GenerationMode.TEST)
        def serialize(envelope,resolution):
            prefixes=tuple(prefix for prefix,namespace in resolution.definition.imported_namespaces.items() if any(token in namespace for token in resolution.placeholder_versions))
            return serializer.serialize_application(envelope,placeholder_versions=resolution.placeholder_versions,placeholder_structure_id=resolution.definition.structure_id,placeholder_model_prefixes=prefixes)
        request_xml=serialize(request,request_resolution)
        response_xml=serialize(response,response_resolution)
        request_root, response_root = ET.fromstring(request_xml), ET.fromstring(response_xml)
        ns = NamespaceRegistry(); soap_body = f"{{{ns.SOAP}}}Body"
        self.assertEqual(request_root.tag, f"{{{ns.SOAP}}}Envelope")
        self.assertEqual(response_root.tag, f"{{{ns.SOAP}}}Envelope")
        request_structure=self.engine.get_structure(request_code,mode=GenerationMode.TEST)
        self.assertEqual(list(request_root.find(soap_body))[0].tag, f"{{{request_structure.namespace}}}{request_structure.root_element}")
        self.assertEqual(list(response_root.find(soap_body))[0].tag, f"{{{response_structure.namespace}}}{response_structure.root_element}")
        self.assertNotEqual(response.header.message_id, request.header.message_id)
        self.assertEqual(response.header.relates_to.message_id, request.header.message_id)
        self.assertEqual(response.header.procedure_id, request.header.procedure_id)
        self.assertEqual(response.header.conversation_id, request.header.conversation_id)
        self.assertEqual(request.header.action.serialize(), self.engine.build_application_action(transaction_code, request_code).serialize())
        self.assertEqual(response.header.action.serialize(), self.engine.build_application_action(transaction_code, response_code).serialize())
        self.assertIsNone(request.header.relates_to)
        self.assertEqual(request.header.to.serialize(),"EAEU://EEC/CP/P.MM.01/P.ACT.001")
        self.assertEqual(request.header.reply_to.address.serialize(),"EAEU://RU/CP/P.MM.01/P.MM.01.ACT.001")
        self.assertEqual(response.header.to.serialize(),"EAEU://RU/CP/P.MM.01/P.MM.01.ACT.001")
        if response_ref_path:
            edoc_ref = response_root.find(f".//{{{response_structure.imported_namespaces['csdo']}}}EDocRefId")
            self.assertEqual(edoc_ref.text, request_edoc_id)
            self.assertNotEqual(edoc_ref.text, response.header.relates_to.message_id.serialize())
        return request_xml, response_xml

    def test_trn005_both_response_branches_generate_in_test(self):
        self.assert_catalog("P.MM.01.TRN.005", "P.MM.01.PRC.008", "P.MM.01.MSG.007", ["P.MM.01.MSG.008", "P.MM.01.MSG.009"])
        self.run_resolved_branch("P.MM.01.TRN.005", "P.MM.01.PRC.008", "P.MM.01.MSG.007", "P.MM.01.MSG.008", 500)
        _,negative=self.run_resolved_branch("P.MM.01.TRN.005","P.MM.01.PRC.008","P.MM.01.MSG.007","P.MM.01.MSG.009",550)
        self.assertIn("ProcessingResultDetails:vY.Y.Y",negative)

    def test_trn006_both_response_branches_generate_in_test(self):
        self.assert_catalog("P.MM.01.TRN.006", "P.MM.01.PRC.009", "P.MM.01.MSG.010", ["P.MM.01.MSG.011", "P.MM.01.MSG.009"])
        self.run_resolved_branch("P.MM.01.TRN.006", "P.MM.01.PRC.009", "P.MM.01.MSG.010", "P.MM.01.MSG.011", 600)
        _,negative=self.run_resolved_branch("P.MM.01.TRN.006","P.MM.01.PRC.009","P.MM.01.MSG.010","P.MM.01.MSG.009",650)
        self.assertIn("ProcessingResultDetails:vY.Y.Y",negative)

    def test_eight_reference_artifacts_are_present_and_valid(self):
        expected = {
            "TRN004_MSG005.xml", "TRN004_MSG006.xml", "TRN005_MSG007.xml", "TRN005_MSG008.xml",
            "TRN005_MSG009.xml", "TRN006_MSG010.xml", "TRN006_MSG011.xml", "TRN006_MSG009.xml",
        }
        self.assertEqual({path.name for path in EXAMPLES.iterdir() if path.is_file()}, expected)
        for path in EXAMPLES.glob("*.xml"):
            root = ET.parse(path).getroot()
            self.assertEqual(root.tag, "{http://www.w3.org/2003/05/soap-envelope}Envelope")
        ns = {"soap": "http://www.w3.org/2003/05/soap-envelope", "wsa": "http://www.w3.org/2005/08/addressing", "int": "urn:EEC:Interaction:v1.0"}
        for request_name, response_name in (("TRN005_MSG007.xml", "TRN005_MSG008.xml"), ("TRN006_MSG010.xml", "TRN006_MSG011.xml")):
            request = ET.parse(EXAMPLES / request_name).getroot(); response = ET.parse(EXAMPLES / response_name).getroot()
            request_id = request.findtext("soap:Header/wsa:MessageID", namespaces=ns)
            response_id = response.findtext("soap:Header/wsa:MessageID", namespaces=ns)
            self.assertNotEqual(request_id, response_id)
            self.assertEqual(response.findtext("soap:Header/wsa:RelatesTo", namespaces=ns), request_id)
            self.assertEqual(response.findtext("soap:Header/int:ProcedureID", namespaces=ns), request.findtext("soap:Header/int:ProcedureID", namespaces=ns))
            self.assertEqual(response.findtext("soap:Header/int:ConversationID", namespaces=ns), request.findtext("soap:Header/int:ConversationID", namespaces=ns))


if __name__ == "__main__": unittest.main()
