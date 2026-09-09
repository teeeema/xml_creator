import json
from pathlib import Path
import unittest

from eaeu_xml.process_packages import ProcessPackageLoader, ProcessRegistry
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.body import GenerationMode


PACKAGE = Path(__file__).parents[1]
ROOT = PACKAGE.parent


class Ds01CatalogTests(unittest.TestCase):
    @staticmethod
    def msg001_fixture():
        engine = EaeuXmlEngine.load_process(PACKAGE); structure = engine.get_structure("P.DS.01.MSG.001", mode=GenerationMode.TEST)
        values = {}
        for field in structure.fields:
            if field.kind == "ATTRIBUTE": values[field.path] = "AAA" if field.xml_name == "currencyCode" else ("0" if field.xml_name == "scaleNumber" else "ID")
            elif field.min_occurs:
                dtype = field.datatype or ""; values[field.path] = ("2024-01-02T00:00:00" if "DateTime" in dtype else "2024-01-02" if "DateType" in dtype else True if "Indicator" in dtype else "0.00" if "PaymentAmount" in dtype else "AA" if "CountryCode" in dtype else "x")
        by = {field.field_id: field.path for field in structure.fields}; values.update({by['3']:[None],by['3.5']:[None],by['3.5']+'/ds01sdo:DailyInfoIndicator':[True],by['3.2']:'2024-01-02',by['3.1']:'2024-01-01'})
        for base, amount in [('3.5.9','DistributableDutyAmount'),('3.5.10','TransferDistributedDutyAmount'),('3.5.12','StopTransferDistributedDutyAmount')]:
            path=by[base]; values.update({path:[None,None],path+'/ds01sdo:TotalAmountIndicator':[True,False],path+'/csdo:UnifiedCountryCode':[None,'AA'],path+'/ds01sdo:'+amount:['10.00','10.00']})
        return engine, by, values
    @classmethod
    def setUpClass(cls):
        cls.package = ProcessPackageLoader.load(PACKAGE)

    def test_package_and_registry_discovery(self):
        self.assertEqual(self.package.process.process_code, "P.DS.01")
        self.assertEqual(self.package.profile.profile_id, "current")
        registry = ProcessRegistry(ROOT)
        self.assertEqual(registry.get_process("P.DS.01").process.process_code, "P.DS.01")

    def test_unique_codes_and_cross_references(self):
        for values in (self.package.procedures, self.package.operations, self.package.transactions, self.package.messages):
            self.assertEqual(len(values), len(set(values)))
        for transaction in self.package.transactions.values():
            self.assertIn(transaction.procedure_code, self.package.procedures)
            self.assertIn(transaction.initiating_operation, self.package.operations)
            self.assertIn(transaction.responding_operation, self.package.operations)
            self.assertIn(transaction.initiating_message, self.package.messages)
            for code in transaction.response_messages:
                self.assertIn(code, self.package.messages)
        for message in self.package.messages.values():
            self.assertIn(message.structure_id, self.package.profile.structures)
            selection = self.package.profile.structures[message.structure_id]
            self.assertIn((message.structure_id, selection.active_version), self.package.structures)

    def test_confirmed_entities_have_sources_and_rules_match_messages(self):
        entities = [self.package.process, *self.package.procedures.values(), *self.package.operations.values(),
                    *self.package.participants.values(), *self.package.transactions.values(), *self.package.messages.values()]
        self.assertTrue(all(entity.source_refs for entity in entities))
        for code, rules in self.package.rules.items():
            self.assertIn(code, self.package.messages)
            self.assertEqual(rules.structure_id, self.package.messages[code].structure_id)

    def test_structure_field_trees_and_unresolved_versions(self):
        report = self.package.structures[("R.FP.DS.01.001", "1.0.0")]
        protocol = self.package.structures[("R.FP.DS.01.003", "1.0.0")]
        self.assertEqual(len(report.fields), 70)
        self.assertEqual(len(protocol.fields), 15)
        self.assertEqual((report.namespace, report.root_element, report.version),
                         ("urn:EEC:R:FP:DS:01:ChargedDistributedReport:v1.0.0", "ChargedDistributedReport", "1.0.0"))
        self.assertEqual((protocol.namespace, protocol.root_element, protocol.version),
                         ("urn:EEC:R:FP:DS:01:VerificationProtocol:v1.0.0", "VerificationProtocol", "1.0.0"))
        self.assertEqual(report.fields[7].xml_name, "ReportCountryCode")
        self.assertEqual(report.fields[7].datatype, "csdo:UnifiedCountryCodeType")
        self.assertEqual(report.fields[7].namespace_prefix, "ds01sdo")
        self.assertEqual(report.fields[9].max_occurs, None)
        self.assertEqual(report.fields[14].max_occurs, 2)
        self.assertEqual(report.fields[15].parent, "3.5")
        self.assertEqual(protocol.fields[7].datatype, "csdo:UnifiedCountryCodeType")
        self.assertEqual(self.package.profile.structures["R.006"].active_version, "Y.Y.Y")
        self.assertEqual(self.package.structures[("R.006", "Y.Y.Y")].imported_namespaces["ccdo"],
                         "urn:EEC:M:ComplexDataObjects:vX.X.X")

    def test_structure_metadata_and_field_integrity(self):
        for structure in (self.package.structures[("R.FP.DS.01.001", "1.0.0")],
                          self.package.structures[("R.FP.DS.01.003", "1.0.0")]):
            ids = {field.field_id for field in structure.fields}
            paths = [field.path for field in structure.fields]
            self.assertEqual(len(paths), len(set(paths)))
            self.assertTrue(all(field.source_refs and field.datatype for field in structure.fields))
            self.assertTrue(all(not field.parent or field.parent in ids for field in structure.fields))
        report = self.package.structures[("R.FP.DS.01.001", "1.0.0")]
        for field in report.fields:
            if field.xml_name in {"currencyCode", "currencyCodeListId", "scaleNumber"}:
                self.assertIn(report.fields[field.order - 1].parent, {x.field_id for x in report.fields})
        self.assertEqual(next(x for x in report.fields if x.field_id == "3.5.9.3").xml_name, "UnifiedCountryCode")

    def test_complete_message_rule_ranges(self):
        expected = {"P.DS.01.MSG.001": 34, "P.DS.01.MSG.002": 38,
                    "P.DS.01.MSG.004": 2, "P.DS.01.MSG.005": 23,
                    "P.DS.01.MSG.006": 14}
        for code, count in expected.items():
            rules = self.package.rules[code].business_rules
            self.assertEqual(len(rules), count)
            self.assertTrue(all(rule.get("source_refs") for rule in rules))

    def test_country_code_rules_keep_literal_and_normalized_references(self):
        rules = [rule for item in self.package.rules.values() for rule in item.business_rules]
        mismatches = [rule for rule in rules if "csdo:CountryCode" in rule.get("source_text", "")]
        self.assertTrue(mismatches)
        self.assertTrue(all("csdo:UnifiedCountryCode" in rule.get("normalized_field_reference", "") for rule in mismatches))

    def test_normative_structure_identifiers_are_loaded_without_rule_codes(self):
        structures = (self.package.structures[("R.FP.DS.01.001", "1.0.0")],
                      self.package.structures[("R.FP.DS.01.003", "1.0.0")])
        elements = [field for structure in structures for field in structure.fields if field.kind == "ELEMENT"]
        attributes = [field for structure in structures for field in structure.fields if field.kind == "ATTRIBUTE"]
        self.assertEqual(len(elements), 75)
        self.assertTrue(all(field.identifier for field in elements))
        self.assertEqual(len(attributes), 10)
        self.assertTrue(all(field.identifier is None for field in attributes))
        self.assertTrue(all(not field.identifier.startswith("P.DS.01.MSG.") for field in elements))
        self.assertTrue(all(any(ref.source_id.startswith("49OP-IDENTIFIER-") for ref in field.source_refs) for field in elements))

    def test_msg001_is_fully_classified_with_traceable_operations(self):
        rules = self.package.rules["P.DS.01.MSG.001"]
        self.assertEqual(len(rules.business_rules), 34)
        self.assertTrue(all(rule.get("source_text") and rule.get("classification") for rule in rules.business_rules))
        known = {rule["rule_id"] for rule in rules.business_rules}
        self.assertTrue(all(rule.get("rule_id") in known for rule in rules.structured_rules))

    def test_msg001_external_rules_are_explicitly_incomplete(self):
        rules = self.package.rules["P.DS.01.MSG.001"]
        results = StructuredRuleEvaluator().evaluate_all(rules.structured_rules, {})
        external = [item for item in results if item.status in {RuleStatus.NOT_EVALUATED_EXTERNAL_CONTEXT, RuleStatus.NOT_EVALUATED_EXTERNAL_REFERENCE}]
        self.assertEqual(len(external), 14)
        self.assertTrue(all(item.status is not RuleStatus.PASS for item in external))

    def test_msg001_executable_rules_have_deterministic_validation_fixture(self):
        rules = self.package.rules["P.DS.01.MSG.001"]
        report = self.package.structures[("R.FP.DS.01.001", "1.0.0")]
        by_id = {field.field_id: field.path for field in report.fields}
        values = {by_id['3']: [None], by_id['3.5']: [None], by_id['3.5'] + '/ds01sdo:DailyInfoIndicator': [True],
                  by_id['3.2']: '2024-01-02', by_id['3.1']: '2024-01-01'}
        for base, amount in [('3.5.9','DistributableDutyAmount'), ('3.5.10','TransferDistributedDutyAmount'), ('3.5.12','StopTransferDistributedDutyAmount')]:
            path = by_id[base]; values[path] = [None, None]
            values[path + '/ds01sdo:TotalAmountIndicator'] = [True, False]
            values[path + '/csdo:UnifiedCountryCode'] = [None, 'AA']
            values[path + '/ds01sdo:' + amount] = ['10.00', '10.00']
        results = StructuredRuleEvaluator().evaluate_all(rules.structured_rules, values)
        executable = {rule['rule_id'] for rule in rules.business_rules if rule['classification'] == 'EXECUTABLE'}
        got = {item.rule_id for item in results if item.rule_id in executable}
        self.assertEqual(got, executable)
        self.assertTrue(all(item.status is RuleStatus.PASS for item in results if item.rule_id in executable))
        self.assertEqual(sum(item.status is RuleStatus.NOT_EVALUATED_EXTERNAL_CONTEXT for item in results), 1)
        self.assertEqual(sum(item.status is RuleStatus.NOT_EVALUATED_EXTERNAL_REFERENCE for item in results), 13)

    def test_msg001_body_validation_and_mutations(self):
        engine, by, values = self.msg001_fixture(); result = engine.validate_body("P.DS.01.MSG.001", values, mode=GenerationMode.TEST)
        self.assertTrue(result.is_valid); self.assertFalse(result.is_complete); self.assertEqual(sum(x.status is RuleStatus.PASS for x in result.rule_evaluations),20)
        for path, value in [(by['3.5']+'/ds01sdo:DailyInfoIndicator',[True,False]), (by['3.5.9']+'/csdo:UnifiedCountryCode',['AA','AA']), (by['3.5.9']+'/ds01sdo:DistributableDutyAmount',['9.00','10.00']), (by['3.5.2'],'0.001')]:
            changed=dict(values); changed[path]=value; self.assertFalse(engine.validate_body("P.DS.01.MSG.001",changed,mode=GenerationMode.TEST).is_valid)

    def test_message_rules_are_separate_from_structure_cardinality(self):
        report = self.package.structures[("R.FP.DS.01.001", "1.0.0")]
        self.assertEqual(report.fields[9].path, "ChargedDistributedReport/ds01cdo:ChargedDistributedDutyReportDetails")
        self.assertEqual(report.fields[9].max_occurs, None)
        self.assertEqual(self.package.rules["P.DS.01.MSG.001"].structure_id, "R.FP.DS.01.001")
        self.assertEqual(self.package.rules["P.DS.01.MSG.001"].field_usage, {})


if __name__ == "__main__":
    unittest.main()
