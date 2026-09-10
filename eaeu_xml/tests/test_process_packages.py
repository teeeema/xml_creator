from pathlib import Path
from tempfile import TemporaryDirectory
import json
import shutil
import unittest

from eaeu_xml.core.errors import ProcessBodyNotImplementedError, ProcessPackagePathError, ProcessPackageValidationError, UnresolvedStructureVersionError
from eaeu_xml.process_packages.body import StructuredProcessBodyProvider
from eaeu_xml.process_packages.body import GenerationMode
from xml.etree import ElementTree as ET
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.loader import ProcessPackageLoader


FIXTURE = Path(__file__).parent / "fixtures/P.TEST.01"
VERSION_FIXTURE = Path(__file__).parent / "fixtures/P.VERSION.01"
SP02_FIXTURE = Path(__file__).parents[2] / "P.SP.02_OP_22"


class ProcessPackageTests(unittest.TestCase):
    def copy_fixture(self) -> tuple[TemporaryDirectory, Path]:
        temporary = TemporaryDirectory(); target = Path(temporary.name) / "arbitrary-location"
        shutil.copytree(FIXTURE, target)
        return temporary, target

    @staticmethod
    def rewrite(path: Path, mutate) -> None:
        data = json.loads(path.read_text(encoding="utf-8")); mutate(data)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def test_load_valid_package_and_source_refs(self):
        package = ProcessPackageLoader.load(FIXTURE)
        self.assertEqual(package.process.process_code, "P.TS.01")
        self.assertEqual(len(package.procedures), 1); self.assertEqual(len(package.transactions), 1)
        self.assertEqual(len(package.messages), 2); self.assertEqual(len(package.structures), 2)
        self.assertEqual(package.process.source_refs[0].source_id, "TEST-001")
        self.assertFalse(package.classifiers_available); self.assertFalse(package.xsd_available)
        self.assertIsNone(package.messages["P.TS.01.MSG.001"].embedded_structures)

    def test_sp02_one_of_embedded_structures_and_rules_load(self):
        package = ProcessPackageLoader.load(SP02_FIXTURE)
        for code in ("P.SP.02.MSG.003", "P.SP.02.MSG.031", "P.SP.02.MSG.059"):
            message = package.messages[code]
            self.assertEqual(message.structure_id, "R.010")
            self.assertEqual(message.embedded_structures.selection, "ONE_OF")
            self.assertEqual(message.embedded_structures.structures, ("R.IP.SP.02.002", "R.IP.SP.02.007"))
        self.assertEqual(package.rules["P.SP.02.MSG.003"].business_rules[0]["applies_to_structure"], "R.010")

    def test_unknown_embedded_structure_is_rejected(self):
        temporary, target = self.copy_fixture()
        try:
            self.rewrite(target / "messages.yaml", lambda data: data["messages"][0].update(
                embedded_structures={"selection": "ONE_OF", "structures": ["R.TEST.001", "R.UNKNOWN"]}))
            with self.assertRaisesRegex(ProcessPackageValidationError, "R.UNKNOWN"):
                ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_one_of_requires_at_least_two_embedded_structures(self):
        temporary, target = self.copy_fixture()
        try:
            self.rewrite(target / "messages.yaml", lambda data: data["messages"][0].update(
                embedded_structures={"selection": "ONE_OF", "structures": ["R.TEST.001"]}))
            with self.assertRaisesRegex(ProcessPackageValidationError, "минимум 2"):
                ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_unknown_embedded_structure_selection_is_rejected(self):
        temporary, target = self.copy_fixture()
        try:
            self.rewrite(target / "messages.yaml", lambda data: data["messages"][0].update(
                embedded_structures={"selection": "ALL_OF", "structures": ["R.TEST.001", "R.TEST.001"]}))
            with self.assertRaisesRegex(ProcessPackageValidationError, "Неизвестный selection"):
                ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_message_rules_status_requires_matching_file_and_source(self):
        package = ProcessPackageLoader.load(FIXTURE)
        self.assertEqual(package.messages["P.TS.01.MSG.001"].message_rules_status, "HAS_SEPARATE_RULE_TABLE")
        self.assertEqual(package.messages["P.TS.01.MSG.002"].message_rules_status, "NO_SEPARATE_RULE_TABLE")
        temporary, target = self.copy_fixture()
        try:
            (target / "message_rules/P.TS.01.MSG.001.yaml").unlink()
            with self.assertRaisesRegex(ProcessPackageValidationError, "YAML правил отсутствует"):
                ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_unverified_message_rules_status_is_rejected(self):
        temporary, target = self.copy_fixture()
        try:
            self.rewrite(target / "messages.yaml", lambda data: data["messages"][1].update(message_rules_status="NEEDS_VERIFICATION"))
            with self.assertRaisesRegex(ProcessPackageValidationError, "требует проверки"):
                ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_invalid_path_and_explicit_path_required(self):
        with self.assertRaises(ProcessPackagePathError): ProcessPackageLoader.load(Path("does-not-exist"))
        with self.assertRaises(ProcessPackagePathError): ProcessPackageLoader.load(str(FIXTURE))
        with self.assertRaises(TypeError): ProcessPackageLoader.load()

    def test_placeholder_definition_is_explicit_test_resolution_only(self):
        temporary,target=self.copy_fixture()
        try:
            profile=target/"version_profiles/current.yaml"; structure=target/"structures/R.TEST.001/2.0.0.yaml"
            self.rewrite(profile,lambda data:data["structures"]["R.TEST.001"].update(active_version=None))
            self.rewrite(structure,lambda data:data.update(version="Y.Y.Y",namespace="urn:test:payload:vY.Y.Y",imported_namespaces={"model":"urn:test:model:vX.X.X"}))
            engine=EaeuXmlEngine.load_process(target)
            resolution=engine.resolve_structure("R.TEST.001",mode=GenerationMode.TEST)
            self.assertTrue(resolution.uses_version_placeholders); self.assertEqual(resolution.placeholder_versions,("Y.Y.Y","X.X.X"))
            self.assertEqual(resolution.definition.namespace,"urn:test:payload:vY.Y.Y")
            with self.assertRaises(UnresolvedStructureVersionError):engine.resolve_structure("R.TEST.001",mode=GenerationMode.STRICT)
            # A concrete selection wins independently and is never replaced by a placeholder.
            self.rewrite(profile,lambda data:data["structures"]["R.TEST.001"].update(active_version="1.0.0"))
            concrete=EaeuXmlEngine.load_process(target).resolve_structure("R.TEST.001",mode=GenerationMode.TEST)
            self.assertEqual(concrete.definition.namespace,"urn:test:structure:v1.0.0"); self.assertFalse(concrete.uses_version_placeholders)
            self.assertNotIn("v1.0.0",resolution.definition.namespace)
        finally:temporary.cleanup()

    def test_process_manifest_is_required(self):
        temporary, target = self.copy_fixture()
        try:
            (target / "process.yaml").unlink()
            with self.assertRaises(ProcessPackagePathError): ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_unknown_procedure_is_rejected(self):
        temporary, target = self.copy_fixture()
        try:
            self.rewrite(target / "transactions.yaml", lambda data: data["transactions"][0].update(procedure_code="P.TS.01.PRC.999"))
            with self.assertRaises(ProcessPackageValidationError): ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_normative_procedure_without_transaction_is_allowed(self):
        temporary, target = self.copy_fixture()
        try:
            self.rewrite(target / "procedures.yaml", lambda data: data["procedures"].append({
                "procedure_code": "P.TS.01.PRC.002", "name": "Portal procedure", "status": "CONFIRMED",
                "source_refs": [{"source_id": "TEST-002", "document": "TEST_FIXTURE_ONLY", "location": "portal", "status": "TEST_ONLY"}],
            }))
            package = ProcessPackageLoader.load(target)
            self.assertIn("P.TS.01.PRC.002", package.procedures)
        finally: temporary.cleanup()

    def test_procedure_with_transaction_is_allowed(self):
        package = ProcessPackageLoader.load(FIXTURE)
        self.assertEqual(package.transactions["P.TS.01.TRN.001"].procedure_code, "P.TS.01.PRC.001")

    def test_unknown_initiating_and_response_messages_are_rejected(self):
        for field, value in (("initiating_message", "P.TS.01.MSG.999"), ("response_messages", ["P.TS.01.MSG.999"])):
            temporary, target = self.copy_fixture()
            try:
                self.rewrite(target / "transactions.yaml", lambda data, f=field, v=value: data["transactions"][0].update({f: v}))
                with self.assertRaises(ProcessPackageValidationError): ProcessPackageLoader.load(target)
            finally: temporary.cleanup()

    def test_unknown_structure_and_unavailable_active_version_are_rejected(self):
        temporary, target = self.copy_fixture()
        try:
            self.rewrite(target / "messages.yaml", lambda data: data["messages"][0].update(structure_id="R.UNKNOWN"))
            with self.assertRaises(ProcessPackageValidationError): ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_message_structure_id_must_be_a_string_or_null(self):
        temporary, target = self.copy_fixture()
        try:
            self.rewrite(target / "messages.yaml", lambda data: data["messages"][0].update(structure_id=["R.TEST.001"]))
            with self.assertRaisesRegex(ProcessPackageValidationError, "structure_id должен быть строкой или null"):
                ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_invalid_namespace_is_rejected(self):
        temporary, target = self.copy_fixture()
        try:
            structure = target / "structures/R.TEST.001/2.0.0.yaml"
            self.rewrite(structure, lambda data: data.update(namespace="not a URI"))
            with self.assertRaises(ProcessPackageValidationError): ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_orphan_structure_is_rejected(self):
        temporary, target = self.copy_fixture()
        try:
            source = target / "structures/R.TEST.001/2.0.0.yaml"
            orphan = target / "structures/R.TEST.002/2.0.0.yaml"
            orphan.parent.mkdir()
            shutil.copy(source, orphan)
            self.rewrite(orphan, lambda data: data.update(structure_id="R.TEST.002"))
            with self.assertRaises(ProcessPackageValidationError): ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_message_rules_cannot_reference_unknown_message(self):
        temporary, target = self.copy_fixture()
        try:
            rules = target / "message_rules/P.TS.01.MSG.001.yaml"
            self.rewrite(rules, lambda data: data.update(message_code="P.TS.01.MSG.999"))
            with self.assertRaises(ProcessPackageValidationError): ProcessPackageLoader.load(target)
        finally: temporary.cleanup()
        temporary, target = self.copy_fixture()
        try:
            self.rewrite(target / "version_profiles/current.yaml", lambda data: data["structures"].update({"R.TEST.001": "9.9.9"}))
            with self.assertRaises(ProcessPackageValidationError): ProcessPackageLoader.load(target)
        finally: temporary.cleanup()

    def test_multiple_versions_are_isolated_and_profile_selects_one(self):
        engine = EaeuXmlEngine.load_process(FIXTURE)
        self.assertEqual(engine.structures[("R.TEST.001", "1.0.0")].namespace, "urn:test:structure:v1.0.0")
        self.assertEqual(engine.get_active_structure_version("R.TEST.001").version, "2.0.0")
        self.assertEqual(engine.get_structure("P.TS.01.MSG.001").version, "2.0.0")

    def test_per_structure_active_versions_are_independent(self):
        engine = EaeuXmlEngine.load_process(VERSION_FIXTURE)
        self.assertEqual(engine.get_active_structure_version("R.006").version, "1.0.0")
        self.assertEqual(engine.get_active_structure_version("R.007").version, "2.0.0")

    def test_changing_r006_does_not_change_r007(self):
        temporary = TemporaryDirectory(); target = Path(temporary.name) / "version-fixture"
        try:
            shutil.copytree(VERSION_FIXTURE, target)
            self.rewrite(target / "version_profiles/current.yaml", lambda data: data["structures"]["R.006"].update(active_version="3.0.0"))
            engine = EaeuXmlEngine.load_process(target)
            self.assertEqual(engine.get_active_structure_version("R.006").version, "3.0.0")
            self.assertEqual(engine.get_active_structure_version("R.007").version, "2.0.0")
        finally: temporary.cleanup()

    def test_changing_r007_does_not_change_r006(self):
        temporary = TemporaryDirectory(); target = Path(temporary.name) / "version-fixture"
        try:
            shutil.copytree(VERSION_FIXTURE, target)
            self.rewrite(target / "version_profiles/current.yaml", lambda data: data["structures"]["R.007"].update(active_version="4.0.0"))
            engine = EaeuXmlEngine.load_process(target)
            self.assertEqual(engine.get_active_structure_version("R.006").version, "1.0.0")
            self.assertEqual(engine.get_active_structure_version("R.007").version, "4.0.0")
        finally: temporary.cleanup()

    def test_null_active_version_is_valid_but_unresolved_on_access(self):
        temporary = TemporaryDirectory(); target = Path(temporary.name) / "version-fixture"
        try:
            shutil.copytree(VERSION_FIXTURE, target)
            self.rewrite(target / "version_profiles/current.yaml", lambda data: data["structures"]["R.006"].update(active_version=None))
            engine = EaeuXmlEngine.load_process(target)
            self.assertEqual(engine.get_active_structure_version("R.007").version, "2.0.0")
            with self.assertRaises(UnresolvedStructureVersionError) as raised:
                engine.get_active_structure_version("R.006")
            self.assertEqual(raised.exception.code, "UNRESOLVED_STRUCTURE_VERSION")
        finally: temporary.cleanup()

    def test_message_rules_and_source_references_load(self):
        engine = EaeuXmlEngine.load_process(FIXTURE)
        rules = engine.rules["P.TS.01.MSG.001"]
        self.assertEqual(rules.fixed_values["Items/@code"], "FIXED")
        self.assertEqual(rules.source_refs[0].document, "TEST_FIXTURE_ONLY")

    def test_legacy_metadata_fields_remain_optional(self):
        package = ProcessPackageLoader.load(FIXTURE)
        self.assertIsNone(package.structures[("R.TEST.001", "2.0.0")].fields[0].identifier)
        rules = package.rules["P.TS.01.MSG.001"]
        self.assertIsNone(rules.source_text)
        self.assertIsNone(rules.normalized_field_reference)

    def test_loader_preserves_identifier_and_rule_text_metadata(self):
        temporary, target = self.copy_fixture()
        try:
            structure = target / "structures/R.TEST.001/2.0.0.yaml"
            self.rewrite(structure, lambda data: data["fields"][0].update(identifier="M.TEST.001"))
            rules = target / "message_rules/P.TS.01.MSG.001.yaml"
            self.rewrite(rules, lambda data: data.update(source_text="literal", normalized_field_reference="TestPayload/Items"))
            package = ProcessPackageLoader.load(target)
            self.assertEqual(package.structures[("R.TEST.001", "2.0.0")].fields[0].identifier, "M.TEST.001")
            self.assertEqual(package.rules["P.TS.01.MSG.001"].source_text, "literal")
            self.assertEqual(package.rules["P.TS.01.MSG.001"].normalized_field_reference, "TestPayload/Items")
        finally:
            temporary.cleanup()

    def test_engine_accessors_and_decision5_action(self):
        engine = EaeuXmlEngine.load_process(FIXTURE)
        self.assertEqual(engine.get_transaction("P.TS.01.TRN.001").procedure_code, "P.TS.01.PRC.001")
        self.assertEqual(engine.get_message("P.TS.01.MSG.002").direction, "RESPONSE")
        action = engine.build_application_action("P.TS.01.TRN.001", "P.TS.01.MSG.001")
        self.assertEqual(action.serialize(), "int://CP/P.TS.01/1.0/P.TS.01.PRC.001/P.TS.01.TRN.001/P.TS.01.MSG.001")

    def test_default_body_provider_is_structured_and_data_driven(self):
        engine = EaeuXmlEngine.load_process(FIXTURE)
        self.assertIsInstance(engine.body_provider, StructuredProcessBodyProvider)

    def test_structured_body_serializes_order_repeatables_and_attributes(self):
        engine = EaeuXmlEngine.load_process(FIXTURE)
        body = engine.build_body("P.TS.01.MSG.001", {"Items": {"Name": ["A", "B"]}}, mode=GenerationMode.TEST)
        root = body.serialize_xml_element()
        self.assertEqual(root.tag, "{urn:test:structure:v2.0.0}TestPayload")
        items = list(root)[0]
        self.assertEqual(items.attrib, {"code": "FIXED"})
        self.assertEqual([child.text for child in items], ["A", "B"])

    def test_repeatable_complex_elements_keep_values_and_attributes_aligned(self):
        engine = EaeuXmlEngine.load_process(FIXTURE)
        body = engine.build_body("P.TS.01.MSG.001", {"Items": [
            {"Name": "A", "@code": "FIXED"}, {"Name": "B", "@code": "FIXED"}
        ]}, mode=GenerationMode.TEST)
        items = list(body.serialize_xml_element())
        self.assertEqual([(item.attrib["code"], list(item)[0].text) for item in items], [("FIXED", "A"), ("FIXED", "B")])

    def test_body_validation_aggregates_required_forbidden_and_fixed_errors(self):
        engine = EaeuXmlEngine.load_process(FIXTURE)
        result = engine.validate_body("P.TS.01.MSG.001", {"Items": {"@code": "WRONG"}, "Note": "x"}, mode=GenerationMode.TEST)
        codes = {issue.code for issue in result.issues}
        self.assertTrue({"MIN_OCCURS", "FORBIDDEN_FIELD", "FIXED_VALUE_MISMATCH"}.issubset(codes))

    def test_fixture_loads_from_arbitrary_location(self):
        temporary, target = self.copy_fixture()
        try: self.assertEqual(EaeuXmlEngine.load_process(target).process.process_code, "P.TS.01")
        finally: temporary.cleanup()

    def test_engine_has_no_specific_process_hardcode(self):
        source = Path(__file__).parents[1] / "src/eaeu_xml"
        text = "\n".join(path.read_text(encoding="utf-8") for path in source.rglob("*.py"))
        self.assertNotIn("P.MM.01", text)
        self.assertNotIn("R.007", text)


if __name__ == "__main__": unittest.main()
