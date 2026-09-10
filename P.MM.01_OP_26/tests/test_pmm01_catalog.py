from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

from eaeu_xml.core.errors import BodyValidationError, UnresolvedStructureVersionError
from eaeu_xml.decision5.models import LogicalAddress, ProcedureId, ProcedureInstance, TransactionInstance
from eaeu_xml.process_packages import EaeuXmlEngine, ProcessPackageLoader
from eaeu_xml.process_packages.body import GenerationMode, IssueSeverity
from eaeu_xml.services.identifier_service import IdentifierService
from eaeu_xml.services.message_factory import MessageFactory
from eaeu_xml.services.logical_address_builder import LogicalAddressBuilder
from eaeu_xml.services.xml_serializer import XmlSerializer


PACKAGE = Path(__file__).parents[1]


class Pmm01CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = ProcessPackageLoader.load(PACKAGE)

    def test_confirmed_inventory(self):
        self.assertEqual(self.package.process.process_code, "P.MM.01")
        self.assertEqual(self.package.profile.process_version, "1.1.0")
        self.assertEqual(len(self.package.procedures), 19)
        self.assertEqual(len(self.package.operations), 57)
        self.assertEqual(len(self.package.transactions), 19)
        self.assertEqual(len(self.package.messages), 28)
        self.assertEqual(len(self.package.structures), 8)

    def test_message_rules_audit_covers_all_messages(self):
        expected_has = {f"P.MM.01.MSG.{number:03d}" for number in
                        (1, 2, 3, 7, 10, 12, 14, 16, 19, 20, 21, 23, 24, 25, 27, 28)}
        expected_none = set(self.package.messages) - expected_has
        actual_has = {code for code, message in self.package.messages.items()
                      if message.message_rules_status == "HAS_SEPARATE_RULE_TABLE"}
        actual_none = {code for code, message in self.package.messages.items()
                       if message.message_rules_status == "NO_SEPARATE_RULE_TABLE"}
        self.assertEqual(actual_has, expected_has)
        self.assertEqual(actual_none, expected_none)
        self.assertEqual(set(self.package.rules), expected_has)
        self.assertEqual(len(actual_has), 16)
        self.assertEqual(len(actual_none), 12)
        self.assertTrue(all(message.message_rules_source_refs for message in self.package.messages.values()))

    def test_transaction_cross_references(self):
        for transaction in self.package.transactions.values():
            self.assertIn(transaction.procedure_code, self.package.procedures)
            self.assertIn(transaction.initiating_operation, self.package.operations)
            self.assertIn(transaction.responding_operation, self.package.operations)
            self.assertIn(transaction.initiating_message, self.package.messages)
            for code in transaction.response_messages:
                self.assertIn(code, self.package.messages)
            self.assertIn(transaction.initiating_participant,self.package.participants)
            self.assertIn(transaction.responding_participant,self.package.participants)

    def test_participants_are_source_traced_and_segment_is_not_participant_code(self):
        commission=self.package.participants["P.ACT.001"]
        authority=self.package.participants["P.MM.01.ACT.001"]
        self.assertEqual((commission.fixed_segment,commission.source_refs[0].table,commission.source_refs[0].page),("EEC","1",6))
        self.assertEqual((authority.segment_policy,authority.test_segment,authority.source_refs[0].page),("MEMBER_STATE_ISO_ALPHA2","RU",7))
        builder=LogicalAddressBuilder()
        ru=builder.build_common_process(segment="RU",process_code="P.MM.01",participant_code=authority.participant_code)
        by=builder.build_common_process(segment="BY",process_code="P.MM.01",participant_code=authority.participant_code)
        self.assertEqual(ru.participant_identifier.participant_code,by.participant_identifier.participant_code)
        self.assertNotEqual(ru.segment,by.segment)

    def test_generic_engine_contains_no_pmm01_participant_hardcode(self):
        engine_source=Path(__file__).parents[2]/"eaeu_xml/src/eaeu_xml"
        text="\n".join(path.read_text(encoding="utf-8") for path in engine_source.rglob("*.py"))
        for forbidden in ("EEC.ACT.001","RU.ACT.001","P.MM.01.ACT.001"):
            self.assertNotIn(forbidden,text)

    def test_message_structure_cross_references(self):
        for message in self.package.messages.values():
            selection = self.package.profile.structures[message.structure_id]
            if selection.active_version is not None:
                self.assertEqual(message.structure_version, selection.active_version)
                self.assertIn((message.structure_id, selection.active_version), self.package.structures)

    def test_base_structures_are_independently_unresolved(self):
        engine = EaeuXmlEngine(self.package)
        for structure_id in ("R.006", "R.007"):
            with self.assertRaises(UnresolvedStructureVersionError) as raised:
                engine.get_active_structure_version(structure_id)
            self.assertEqual(raised.exception.code, "UNRESOLVED_STRUCTURE_VERSION")
        self.assertEqual(engine.get_active_structure_version("R.HC.MM.01.007").version, "1.0.0")

    def test_transaction_017_alternative_responses(self):
        transaction = self.package.transactions["P.MM.01.TRN.017"]
        self.assertEqual(transaction.initiating_message, "P.MM.01.MSG.025")
        self.assertEqual(set(transaction.response_messages), {"P.MM.01.MSG.009", "P.MM.01.MSG.026"})

    def test_xsd_absence_and_conservative_package_status(self):
        self.assertFalse(self.package.xsd_available)
        self.assertEqual(self.package.process.status, "BODY_MODEL_CONFIRMED_WITH_EXTERNAL_CONFLICTS")

    def test_all_normative_structure_rows_have_explainable_coverage(self):
        expected = {
            "R.006": 10, "R.007": 11, "R.HC.MM.01.001": 405,
            "R.HC.MM.01.002": 23, "R.HC.MM.01.003": 39,
            "R.HC.MM.01.004": 11, "R.HC.MM.01.006": 42,
            "R.HC.MM.01.007": 14,
        }
        for structure in self.package.structures.values():
            self.assertEqual(structure.expected_normative_rows, expected[structure.structure_id])
            self.assertEqual(structure.imported_normative_rows, len(structure.fields))
            self.assertEqual(len({field.field_id for field in structure.fields}), len(structure.fields))
            duplicate_paths = {field.path for field in structure.fields if sum(other.path == field.path for other in structure.fields) > 1}
            if duplicate_paths:
                self.assertEqual(structure.structure_id, "R.HC.MM.01.001")
                self.assertEqual(len(duplicate_paths), 8)
                self.assertTrue(all(field.kind == "ATTRIBUTE" for field in structure.fields if field.path in duplicate_paths))
            self.assertEqual([field.order for field in structure.fields], list(range(1, len(structure.fields) + 1)))
            self.assertTrue(all(field.source_refs and field.datatype_text for field in structure.fields))

    def test_interpretation_audit_closes_field_ambiguities_without_hiding_external_dependencies(self):
        fields = [field for structure in self.package.structures.values() for field in structure.fields]
        self.assertEqual(len(fields), 555)
        self.assertEqual(sum(field.interpretation_status == "VERIFIED" for field in fields), 491)
        self.assertEqual(sum(field.interpretation_status == "NEEDS_EXTERNAL_SOURCE" for field in fields), 64)
        self.assertEqual(sum(field.interpretation_status == "NEEDS_NORMATIVE_INTERPRETATION" for field in fields), 0)
        self.assertTrue(all(field.reason_code == "EXTERNAL_CLASSIFIER_DATASET" for field in fields if field.interpretation_status == "NEEDS_EXTERNAL_SOURCE"))

    def test_pdf_extraction_regressions_restore_cardinality_names_attributes_and_arbitrary_xml(self):
        structure = self.package.structures[("R.HC.MM.01.001", "1.1.0")]
        fields = {field.field_id: field for field in structure.fields}
        self.assertEqual((fields["1"].min_occurs, fields["1"].max_occurs), (1, 1))
        self.assertEqual(fields["2.2.3.7"].xml_name, "DrugRegistrationSpecialProcedureCode")
        self.assertEqual(fields["2.4.3.2.4.1.2"].xml_name, "DosageUnitKindName")
        self.assertEqual(fields["2.4.3.2.4.2.4.3"].xml_name, "FunctionalPurposeCode")
        self.assertEqual(fields["2.4.11"].xml_name, "ControlListDetails")
        self.assertEqual(fields["2.6.13.1"].kind, "ARBITRARY_XML")
        self.assertEqual(len({field.path for field in structure.fields}), 405)

    def test_hierarchy_attributes_and_cardinality_are_structurally_valid(self):
        for structure in self.package.structures.values():
            fields = {field.field_id: field for field in structure.fields}
            for field in structure.fields:
                if field.parent:
                    self.assertIn(field.parent, fields)
                    seen = {field.field_id}; parent = field.parent
                    while parent:
                        self.assertNotIn(parent, seen); seen.add(parent)
                        parent = fields[parent].parent
                if field.kind == "ATTRIBUTE":
                    self.assertTrue(field.path.rsplit("/", 1)[-1].startswith("@"))
                if field.max_occurs is not None and field.min_occurs is not None:
                    self.assertLessEqual(field.min_occurs, field.max_occurs)

    def test_all_sixteen_message_rule_tables_and_rows_are_loaded(self):
        self.assertEqual(len(self.package.rules), 16)
        self.assertEqual(sum(len(rules.business_rules) for rules in self.package.rules.values()), 201)
        for code, rules in self.package.rules.items():
            self.assertIn(code, self.package.messages)
            self.assertTrue(rules.source_refs)
            self.assertTrue(all(rule.get("source_refs") for rule in rules.business_rules))

    def test_message_rule_interpretation_audit_is_reason_coded(self):
        rules = [rule for item in self.package.rules.values() for rule in item.business_rules]
        self.assertEqual(len(rules), 201)
        self.assertEqual(sum(rule.get("interpretation_status") == "VERIFIED" for rule in rules), 195)
        self.assertEqual(sum(rule.get("interpretation_status") == "NEEDS_EXTERNAL_SOURCE" for rule in rules), 1)
        self.assertEqual(sum(rule.get("interpretation_status") == "NEEDS_NORMATIVE_INTERPRETATION" for rule in rules), 0)
        conflicts = [rule for rule in rules if rule.get("interpretation_status") == "INTERNAL_NORMATIVE_CONFLICT"]
        self.assertEqual(len(conflicts), 5)
        self.assertEqual({rule["conflict_id"] for rule in conflicts}, {f"NORMATIVE_CONFLICT-{index:03d}" for index in range(1, 6)})
        self.assertTrue(all(rule.get("referenced_identifiers") and rule.get("conflict_details") for rule in conflicts))
        self.assertTrue(all(rule["source_refs"][0].get("page") for rule in conflicts))

    def test_normative_conflicts_block_only_affected_messages_explicitly(self):
        engine = EaeuXmlEngine(self.package)
        expected = {
            "P.MM.01.MSG.002": {"NORMATIVE_CONFLICT-001"},
            "P.MM.01.MSG.023": {"NORMATIVE_CONFLICT-002", "NORMATIVE_CONFLICT-003"},
            "P.MM.01.MSG.024": {"NORMATIVE_CONFLICT-004", "NORMATIVE_CONFLICT-005"},
        }
        for message_code, conflict_ids in expected.items():
            result = engine.validate_body(message_code, {}, mode=GenerationMode.TEST)
            actual = {issue.rule_id for issue in result.issues if issue.code == "NORMATIVE_CONFLICT"}
            self.assertEqual(actual, conflict_ids)
            with self.assertRaises(BodyValidationError) as raised:
                engine.build_body(message_code, {}, mode=GenerationMode.TEST)
            self.assertTrue(any(issue.code == "NORMATIVE_CONFLICT" for issue in raised.exception.issues))

    @staticmethod
    def _request_values():
        return {
            "EDocHeader": {
                "InfEnvelopeCode": "P.MM.01.MSG.025", "EDocCode": "R.HC.MM.01.004",
                "EDocId": "urn:uuid:00000000-0000-0000-0000-000000000001",
                "EDocDateTime": "2026-08-24T00:00:00",
            },
            "ApplicationId": "APP-1",
            "UnifiedCountryCode": {"#text": "RU", "@codeListId": "TEST-CLASSIFIER"},
        }

    def test_resolved_body_serializes_root_order_nesting_and_attribute(self):
        engine = EaeuXmlEngine(self.package)
        result = engine.validate_body("P.MM.01.MSG.025", self._request_values(), mode=GenerationMode.TEST)
        self.assertTrue(result.is_valid)
        self.assertTrue(any(issue.severity == IssueSeverity.WARNING for issue in result.issues))
        root = engine.build_body("P.MM.01.MSG.025", self._request_values(), mode=GenerationMode.TEST).serialize_xml_element()
        self.assertEqual(root.tag, "{urn:EEC:R:HC:MM:01:DrugRegistrationNumberRequestDetails:v1.1.0}DrugRegistrationNumberRequestDetails")
        country = list(root)[-1]
        self.assertEqual(country.text, "RU")
        self.assertEqual(country.attrib["codeListId"], "TEST-CLASSIFIER")

    def test_second_unambiguous_resolved_structure_serializes(self):
        engine = EaeuXmlEngine(self.package)
        values = {"EDocHeader": {
            "InfEnvelopeCode": "P.MM.01.MSG.007", "EDocCode": "R.HC.MM.01.007",
            "EDocId": "urn:uuid:00000000-0000-0000-0000-000000000002",
            "EDocDateTime": "2026-08-24T00:00:00",
        }}
        root = engine.build_body("P.MM.01.MSG.007", values, mode=GenerationMode.TEST).serialize_xml_element()
        self.assertEqual(root.tag, "{urn:EEC:R:HC:MM:01:DrugRegistrationStatusDetails:v1.0.0}DrugRegistrationStatusDetails")

    def test_r007_edoc_datetime_accepts_iso_local_and_offset_forms(self):
        engine=EaeuXmlEngine(self.package)
        for value in ("2026-08-24T15:24:00","2026-08-24T15:24:00+03:00"):
            values={"EDocHeader":{"InfEnvelopeCode":"P.MM.01.MSG.005","EDocCode":"R.007","EDocId":"00000000-0000-0000-0000-000000000005","EDocDateTime":value}}
            with self.subTest(value=value):self.assertTrue(engine.validate_body("P.MM.01.MSG.005",values,mode=GenerationMode.TEST).is_valid)

    def test_confirmed_arbitrary_xml_is_inserted_without_synthetic_wrapper(self):
        engine = EaeuXmlEngine(self.package)
        arbitrary = ET.Element("{urn:test:external}Payload")
        arbitrary.text = "content"
        values = {
            "EDocHeader": {
                "InfEnvelopeCode": "P.MM.01.MSG.024", "EDocCode": "R.HC.MM.01.002",
                "EDocId": "urn:uuid:00000000-0000-0000-0000-000000000003",
                "EDocDateTime": "2026-08-24T00:00:00",
            },
            "UnifiedCountryCode": {"#text": "RU", "@codeListId": "TEST-CLASSIFIER"},
            "ApplicationId": "APP-1", "DocCreationDate": "2026-08-24",
            "AnyDetails": {"*": arbitrary},
        }
        structure = engine.get_active_structure_version("R.HC.MM.01.002")
        root = engine.body_provider._serialize(structure, engine.body_provider._flatten(values))
        self.assertIsNotNone(root.find(".//{urn:test:external}Payload"))

    def test_body_integrates_with_decision5_message_factory_and_soap(self):
        engine = EaeuXmlEngine(self.package)
        payload = engine.build_body("P.MM.01.MSG.025", self._request_values(), mode=GenerationMode.TEST)
        ids = IdentifierService()
        procedure = ProcedureInstance("P.MM.01.PRC.017", ProcedureId.root(ids))
        transaction = TransactionInstance("P.MM.01.TRN.017", ids.new_conversation_id(), procedure)
        message = MessageFactory(ids).create_initial_application_message(
            transaction=transaction, process_code="P.MM.01", process_version="1.1.0",
            message_code="P.MM.01.MSG.025",
            to=LogicalAddressBuilder().build_common_process(segment="EEC",process_code="P.MM.01",participant_code="P.ACT.001"),
            reply_to=LogicalAddressBuilder().build_common_process(segment="RU",process_code="P.MM.01",participant_code="P.MM.01.ACT.001"), body_payload=payload,
        )
        xml = XmlSerializer().serialize_application(message)
        root = ET.fromstring(xml)
        body = root.find("{http://www.w3.org/2003/05/soap-envelope}Body")
        self.assertEqual(list(body)[0].tag, "{urn:EEC:R:HC:MM:01:DrugRegistrationNumberRequestDetails:v1.1.0}DrugRegistrationNumberRequestDetails")
        self.assertIn(engine.build_application_action("P.MM.01.TRN.017", "P.MM.01.MSG.025").serialize(), xml)


if __name__ == "__main__":
    unittest.main()
