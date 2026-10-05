import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from eaeu_xml.core.errors import ProcessPackageValidationError
from eaeu_xml.process_packages.body import BodyValidationResult, GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.loader import ProcessPackageLoader
from eaeu_xml.process_packages.rules_engine import RuleEvaluation, RuleStatus, StructuredRuleEvaluator


FIXTURE = Path(__file__).parent / "fixtures/P.TEST.01"
PROJECT_ROOT = Path(__file__).parents[2]
PDS01 = PROJECT_ROOT / "P.DS.01_OP_49"


class StructuredRuleTests(unittest.TestCase):
    def setUp(self):
        self.e = StructuredRuleEvaluator()
        self.p = "Groups"
        self.v = {
            "Groups": [None, None],
            "Groups/Flag": [True, False],
            "Groups/Amount": ["1.20", "0.80"],
            "Groups/Country": ["AA", None],
        }

    def test_selector_eq_ne_and_cardinality_backward_compatible(self):
        daily = {"collection": self.p, "where": {"field": "Flag", "operator": "EQ", "value": True}}
        monthly = {"collection": self.p, "where": {"field": "Flag", "operator": "NE", "value": True}}
        self.assertEqual(len(self.e.select(daily, self.v)), 1)
        self.assertEqual(len(self.e.select(monthly, self.v)), 1)
        self.assertEqual(self.e.evaluate({"kind": "selection_cardinality", "selector": daily, "min_occurs": 1, "max_occurs": 1}, self.v).status, RuleStatus.PASS)
        self.assertEqual(self.e.evaluate({"kind": "selection_cardinality", "selector": daily, "min_occurs": 0, "max_occurs": 0}, self.v).status, RuleStatus.FAIL)

    def test_in_not_in_pass_fail_and_invalid_rhs(self):
        values = {"Code": "A"}
        self.assertEqual(self.e.evaluate({"kind": "comparison", "left": "Code", "operator": "IN", "right_value": ["A", "B"]}, values).status, RuleStatus.PASS)
        self.assertEqual(self.e.evaluate({"kind": "comparison", "left": "Code", "operator": "IN", "right_value": ["B", "C"]}, values).status, RuleStatus.FAIL)
        self.assertEqual(self.e.evaluate({"kind": "comparison", "left": "Code", "operator": "NOT_IN", "right_value": ["B", "C"]}, values).status, RuleStatus.PASS)
        self.assertEqual(self.e.evaluate({"kind": "comparison", "left": "Code", "operator": "NOT_IN", "right_value": ["A", "C"]}, values).status, RuleStatus.FAIL)
        self.assertEqual(self.e.evaluate({"kind": "comparison", "left": "Code", "operator": "IN", "right_value": "ABC"}, values).status, RuleStatus.FAIL)
        self.assertEqual(self.e.evaluate({"kind": "comparison", "left": "Code", "operator": "IN", "right_value": [1, 2]}, values).status, RuleStatus.FAIL)

    def test_recursive_all_any_not_and_old_leaf_condition(self):
        context = self.e._select_contexts({"collection": self.p}, self.v)[0]
        old = {"field": "Flag", "operator": "EQ", "value": True}
        nested = {
            "all": [
                old,
                {"any": [
                    {"field": "Country", "operator": "EQ", "value": "AA"},
                    {"not": {"field": "Country", "operator": "EQ", "value": "ZZ"}},
                ]},
                {"not": {"field": "Country", "operator": "EQ", "value": "BB"}},
            ]
        }
        self.assertTrue(self.e.evaluate_condition(old, context, self.v))
        self.assertTrue(self.e.evaluate_condition(nested, context, self.v))
        nested["all"][2] = {"not": {"field": "Country", "operator": "EQ", "value": "AA"}}
        self.assertFalse(self.e.evaluate_condition(nested, context, self.v))

    def test_conditional_presence_and_aggregate_backward_compatible(self):
        rule = {"kind": "conditional_presence", "scope": {"collection": self.p}, "condition": {"field": "Flag", "operator": "EQ", "value": True}, "target": {"field": "Country"}, "state": "FORBIDDEN"}
        self.assertEqual(self.e.evaluate(rule, self.v).status, RuleStatus.FAIL)
        total = {"collection": self.p, "where": {"field": "Flag", "operator": "EQ", "value": True}}
        parts = {"collection": self.p, "where": {"field": "Flag", "operator": "EQ", "value": False}}
        rule = {"kind": "aggregate_comparison", "left": {"selector": total, "value_field": "Amount", "aggregation": "VALUE"}, "operator": "EQ", "right": {"selector": parts, "value_field": "Amount", "aggregation": "SUM"}}
        self.assertEqual(self.e.evaluate(rule, self.v).status, RuleStatus.FAIL)

    def test_conditional_fixed_value_is_validation_only(self):
        rule = {
            "kind": "conditional_fixed_value",
            "scope": {"collection": self.p},
            "condition": {"field": "Flag", "operator": "EQ", "value": True},
            "target": {"field": "Country"},
            "value": "AA",
        }
        self.assertEqual(self.e.evaluate(rule, self.v).status, RuleStatus.PASS)
        wrong = dict(rule, value="BB")
        self.assertEqual(self.e.evaluate(wrong, self.v).status, RuleStatus.FAIL)
        missing = dict(self.v, **{"Groups/Country": [None, None]})
        self.assertEqual(self.e.evaluate(rule, missing).status, RuleStatus.FAIL)
        self.assertEqual(missing["Groups/Country"], [None, None])

    def test_for_each_zero_one_many_and_one_invalid(self):
        rule = {
            "kind": "for_each",
            "selector": {"collection": "Items"},
            "assertions": [{"kind": "comparison", "left": {"field": "Code"}, "operator": "IN", "right_value": ["A", "B"]}],
        }
        self.assertEqual(self.e.evaluate(rule, {}).status, RuleStatus.PASS)
        self.assertEqual(self.e.evaluate(rule, {"Items": [None], "Items/Code": ["A"]}).status, RuleStatus.PASS)
        self.assertEqual(self.e.evaluate(rule, {"Items": [None, None], "Items/Code": ["A", "B"]}).status, RuleStatus.PASS)
        self.assertEqual(self.e.evaluate(rule, {"Items": [None, None], "Items/Code": ["A", "X"]}).status, RuleStatus.FAIL)

    def test_qname_selector_matches_full_segments_on_different_paths(self):
        values = {
            "Root/A/csdo:UnifiedCountryCode": "RU",
            "Root/A/csdo:UnifiedCountryCode/@codeListId": "COUNTRY",
            "Root/B/csdo:UnifiedCountryCode": "KZ",
            "Root/B/csdo:UnifiedCountryCode/@codeListId": "COUNTRY",
            "Root/B/csdo:UnifiedCountryCodeExtra": "SHOULD_NOT_MATCH",
            "Root/C/csdo:UnifiedCountryCode": "BY",
            "Root/C/csdo:UnifiedCountryCode/@codeListId": "OTHER",
        }
        selected = self.e.select({"qname": "csdo:UnifiedCountryCode", "under": "Root"}, values)
        self.assertEqual(len(selected), 3)
        rule = {"kind": "for_each", "selector": {"qname": "csdo:UnifiedCountryCode", "under": "Root/A"}, "assertions": [{"kind": "fixed_value", "target": {"field": "@codeListId"}, "value": "COUNTRY"}]}
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.PASS)
        rule["selector"] = {"qname": "csdo:UnifiedCountryCode", "under": "Root"}
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.FAIL)

    def test_qname_selector_repeatable_instances(self):
        values = {
            "Root/Items": [None, None],
            "Root/Items/csdo:UnifiedCountryCode": ["RU", "KZ"],
            "Root/Items/csdo:UnifiedCountryCode/@codeListId": ["COUNTRY", "COUNTRY"],
        }
        selector = {"qname": "csdo:UnifiedCountryCode"}
        self.assertEqual(len(self.e.select(selector, values)), 2)
        rule = {"kind": "for_each", "selector": selector, "assertions": [{"kind": "fixed_value", "target": {"field": "@codeListId"}, "value": "COUNTRY"}]}
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.PASS)

    def test_nested_repeatable_instances_preserve_parent_child_indexes(self):
        values = {
            "Groups": [None, None],
            "Groups/Items": [[None, None], [None]],
            "Groups/Items/Code": [["A", "B"], ["C"]],
        }
        selector = {"collection": "Groups/Items"}
        self.assertEqual([item["Code"] for item in self.e.select(selector, values)], ["A", "B", "C"])
        rule = {"kind": "for_each", "selector": selector, "assertions": [{"kind": "comparison", "left": {"field": "Code"}, "operator": "IN", "right_value": ["A", "B", "C"]}]}
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.PASS)
        invalid = dict(values, **{"Groups/Items/Code": [["A", "X"], ["C"]]})
        self.assertEqual(self.e.evaluate(rule, invalid).status, RuleStatus.FAIL)
        empty_nested = dict(values, **{"Groups/Items": [[], [None]], "Groups/Items/Code": [[], ["C"]]})
        self.assertEqual(len(self.e.select(selector, empty_nested)), 1)

    def test_synthetic_req_007_to_010_024_028_equivalents(self):
        values = {
            "Body/A/csdo:UnifiedCountryCode": "RU",
            "Body/A/csdo:UnifiedCountryCode/@codeListId": "COUNTRY",
            "Body/ccdo:SubjectAddressDetails": [None],
            "Body/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["1"],
            "Body/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode": ["RU"],
            "Body/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode/@codeListId": ["COUNTRY"],
            "Body/ccdo:SubjectAddressDetails/csdo:CityName": ["Moscow"],
            "Body/ccdo:CommunicationDetails": [None, None],
            "Body/ccdo:CommunicationDetails/csdo:CommunicationChannelCode": ["TE", "EM"],
            "Body/ccdo:CommunicationDetails/csdo:CommunicationChannelId": ["1", "a@example.test"],
            "Body/ccdo:CommunicationDetails/csdo:CommunicationChannelName": [None, None],
            "Body/Addresses": [None, None],
            "Body/Addresses/csdo:UnifiedCountryCode": ["RU", "AM"],
            "Body/Addresses/csdo:UnifiedCountryCode/@codeListId": ["COUNTRY", "COUNTRY"],
            "Body/CollectiveMarkIndicator": "1",
        }
        rules = [
            # REQ.007
            {"kind": "for_each", "selector": {"qname": "csdo:UnifiedCountryCode"}, "assertions": [{"kind": "fixed_value", "target": {"field": "@codeListId"}, "value": "COUNTRY"}]},
            # REQ.008
            {"kind": "for_each", "selector": {"qname": "ccdo:SubjectAddressDetails"}, "assertions": [
                {"kind": "presence", "target": {"field": "csdo:AddressKindCode"}, "state": "REQUIRED"},
                {"kind": "presence", "target": {"field": "csdo:UnifiedCountryCode"}, "state": "REQUIRED"},
                {"kind": "presence", "target": {"field": "csdo:CityName"}, "state": "REQUIRED"},
            ]},
            # REQ.009
            {"kind": "for_each", "selector": {"qname": "ccdo:CommunicationDetails"}, "assertions": [
                {"kind": "presence", "target": {"field": "csdo:CommunicationChannelCode"}, "state": "REQUIRED"},
                {"kind": "presence", "target": {"field": "csdo:CommunicationChannelId"}, "state": "REQUIRED"},
                {"kind": "presence", "target": {"field": "csdo:CommunicationChannelName"}, "state": "FORBIDDEN"},
            ]},
            # REQ.010
            {"kind": "for_each", "selector": {"qname": "ccdo:CommunicationDetails"}, "assertions": [{"kind": "comparison", "left": {"field": "csdo:CommunicationChannelCode"}, "operator": "IN", "right_value": ["TE", "EM", "FX"]}]},
            # REQ.024
            {"kind": "for_each", "selector": {"collection": "Body/Addresses"}, "assertions": [{"kind": "comparison", "left": {"field": "csdo:UnifiedCountryCode"}, "operator": "IN", "right_value": ["AM", "BY", "KZ", "KG", "RU"]}]},
            # REQ.028, with no bool/string coercion.
            {"kind": "comparison", "left": "Body/CollectiveMarkIndicator", "operator": "IN", "right_value": ["1", "0"]},
        ]
        for rule in rules:
            self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.PASS, rule)
        boolean_value = dict(values, **{"Body/CollectiveMarkIndicator": True})
        self.assertEqual(self.e.evaluate(rules[-1], boolean_value).status, RuleStatus.FAIL)

    def test_body_integration_executes_for_each_without_generation_side_effects(self):
        temporary = TemporaryDirectory()
        target = Path(temporary.name) / "fixture"
        try:
            shutil.copytree(FIXTURE, target)
            rules_path = target / "message_rules/P.TS.01.MSG.001.yaml"
            data = json.loads(rules_path.read_text())
            data["structured_rules"] = [{
                "rule_id": "TEST.FOR_EACH",
                "kind": "for_each",
                "selector": {"collection": "Items"},
                "assertions": [{"kind": "presence", "target": {"field": "Name"}, "state": "REQUIRED"}],
            }]
            rules_path.write_text(json.dumps(data))
            engine = EaeuXmlEngine.load_process(target)
            result = engine.validate_body("P.TS.01.MSG.001", {"Items": [{"Name": "A"}]}, mode=GenerationMode.TEST)
            self.assertTrue(result.is_valid)
            self.assertEqual(result.rule_evaluations[0].status, RuleStatus.PASS)
            self.assertNotIn("Items/Name", engine.rules["P.TS.01.MSG.001"].fixed_values)
        finally:
            temporary.cleanup()

    def test_malformed_dsl_is_rejected_by_package_validator(self):
        malformed = [
            {"kind": "comparison", "left": "Items/Name", "operator": "IN", "right_value": "A"},
            {"kind": "for_each", "selector": {"collection": "Items", "qname": "Items"}, "assertions": [{"kind": "presence", "target": {"field": "Name"}, "state": "REQUIRED"}]},
            {"kind": "for_each", "selector": {"collection": "Items"}, "assertions": []},
            {"kind": "conditional_fixed_value", "scope": {"collection": "Items"}, "condition": {"all": []}, "target": {"field": "Name"}, "value": "A"},
            {"kind": "comparison", "left": "Items/Name", "operator": "UNKNOWN", "right_value": "A"},
        ]
        for rule in malformed:
            with self.subTest(rule=rule):
                temporary = TemporaryDirectory()
                target = Path(temporary.name) / "fixture"
                try:
                    shutil.copytree(FIXTURE, target)
                    rules_path = target / "message_rules/P.TS.01.MSG.001.yaml"
                    data = json.loads(rules_path.read_text())
                    data["structured_rules"] = [rule]
                    rules_path.write_text(json.dumps(data))
                    with self.assertRaises(ProcessPackageValidationError):
                        ProcessPackageLoader.load(target)
                finally:
                    temporary.cleanup()

    def test_pds01_existing_structured_rules_still_load_and_evaluate(self):
        package = ProcessPackageLoader.load(PDS01)
        rules = package.rules["P.DS.01.MSG.001"].structured_rules
        self.assertGreater(len(rules), 20)
        self.assertIn("selection_cardinality", {rule["kind"] for rule in rules})
        self.assertIn("conditional_presence", {rule["kind"] for rule in rules})
        self.assertIn("aggregate_comparison", {rule["kind"] for rule in rules})

    def test_external_unsupported_and_completeness_statuses(self):
        self.assertEqual(self.e.evaluate({"evaluation_status": "EXTERNAL_CONTEXT_REQUIRED"}, {}).status, RuleStatus.NOT_EVALUATED_EXTERNAL_CONTEXT)
        self.assertEqual(self.e.evaluate({"kind": "unknown"}, {}).status, RuleStatus.UNSUPPORTED_RULE)
        self.assertTrue(BodyValidationResult((), (RuleEvaluation("x", RuleStatus.PASS, "x"),)).is_complete)
        self.assertFalse(BodyValidationResult((), (RuleEvaluation("x", RuleStatus.NOT_EVALUATED_EXTERNAL_CONTEXT, "x"),)).is_complete)
        self.assertFalse(BodyValidationResult((), (RuleEvaluation("x", RuleStatus.UNSUPPORTED_RULE, "x"),)).is_complete)

    def test_parent_context_filtering_order_ab(self):
        values = {
            "Apps": [None, None],
            "Apps/Status": ["01", "02"],
            "Apps/Parties": [[None], [None]],
            "Apps/Parties/Country": [["RU"], ["KZ"]],
        }
        selector = {
            "collection": "Apps/Parties",
            "parent": {
                "collection": "Apps",
                "where": {"field": "Status", "operator": "EQ", "value": "01"},
            },
        }
        selected = self.e.select(selector, values)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["Country"], "RU")

        rule = {
            "kind": "for_each",
            "selector": selector,
            "assertions": [{"kind": "fixed_value", "target": {"field": "Country"}, "value": "RU"}],
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.PASS)

    def test_parent_context_filtering_order_ba(self):
        values = {
            "Apps": [None, None],
            "Apps/Status": ["02", "01"],
            "Apps/Parties": [[None], [None]],
            "Apps/Parties/Country": [["KZ"], ["RU"]],
        }
        selector = {
            "collection": "Apps/Parties",
            "parent": {
                "collection": "Apps",
                "where": {"field": "Status", "operator": "EQ", "value": "01"},
            },
        }
        selected = self.e.select(selector, values)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["Country"], "RU")

        rule = {
            "kind": "for_each",
            "selector": selector,
            "assertions": [{"kind": "fixed_value", "target": {"field": "Country"}, "value": "RU"}],
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.PASS)

    def test_parent_context_no_cross_parent_repair(self):
        values = {
            "Apps": [None, None],
            "Apps/Status": ["01", "02"],
            "Apps/Parties": [[None], [None]],
            "Apps/Parties/Country": [["INVALID"], ["RU"]],
        }
        rule = {
            "kind": "for_each",
            "selector": {
                "collection": "Apps/Parties",
                "parent": {
                    "collection": "Apps",
                    "where": {"field": "Status", "operator": "EQ", "value": "01"},
                },
            },
            "assertions": [{"kind": "fixed_value", "target": {"field": "Country"}, "value": "RU"}],
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.FAIL)

    def test_parent_context_sibling_isolation(self):
        values = {
            "Apps": [None, None],
            "Apps/Status": ["01", "02"],
            "Apps/Parties": [[None], [None]],
            "Apps/Parties/Country": [["RU"], ["INVALID"]],
        }
        rule = {
            "kind": "for_each",
            "selector": {
                "collection": "Apps/Parties",
                "parent": {
                    "collection": "Apps",
                    "where": {"field": "Status", "operator": "EQ", "value": "01"},
                },
            },
            "assertions": [{"kind": "fixed_value", "target": {"field": "Country"}, "value": "RU"}],
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.PASS)

    def test_parent_context_multiple_children(self):
        values = {
            "Apps": [None, None],
            "Apps/Status": ["01", "02"],
            "Apps/Parties": [[None, None, None], [None]],
            "Apps/Parties/Country": [["RU", "BY", "KZ"], ["AM"]],
        }
        selector = {
            "collection": "Apps/Parties",
            "parent": {
                "collection": "Apps",
                "where": {"field": "Status", "operator": "EQ", "value": "01"},
            },
        }
        selected = self.e.select(selector, values)
        self.assertEqual(len(selected), 3)
        self.assertEqual([item["Country"] for item in selected], ["RU", "BY", "KZ"])

        rule_pass = {
            "kind": "for_each",
            "selector": selector,
            "assertions": [
                {"kind": "comparison", "left": {"field": "Country"}, "operator": "IN", "right_value": ["RU", "BY", "KZ"]}
            ],
        }
        self.assertEqual(self.e.evaluate(rule_pass, values).status, RuleStatus.PASS)

        rule_fail = {
            "kind": "for_each",
            "selector": selector,
            "assertions": [
                {"kind": "comparison", "left": {"field": "Country"}, "operator": "IN", "right_value": ["RU", "BY"]}
            ],
        }
        self.assertEqual(self.e.evaluate(rule_fail, values).status, RuleStatus.FAIL)

    def test_parent_context_invalid_ancestry_fails_safely(self):
        values = {
            "Apps": [None],
            "Apps/Parties": [[None]],
            "Apps/Parties/Country": [["RU"]],
            "Other": [None],
        }
        selector = {
            "collection": "Apps/Parties",
            "parent": {
                "collection": "Other",
            },
        }
        with self.assertRaises(ValueError):
            self.e.select(selector, values)

        rule = {
            "kind": "for_each",
            "selector": selector,
            "assertions": [{"kind": "presence", "target": {"field": "Country"}, "state": "REQUIRED"}],
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.FAIL)

    def test_condition_assertion_inclusive_or_truth_table(self):
        rule = {
            "kind": "for_each",
            "selector": {"collection": "Items"},
            "assertions": [
                {
                    "kind": "condition",
                    "condition": {
                        "any": [
                            {"field": "Code", "operator": "IN", "value": ["110", "120"]},
                            {"field": "Name", "operator": "IN", "value": ["Word", "Letter"]},
                        ]
                    },
                }
            ],
        }

        # TT: Code valid, Name valid -> PASS
        values_tt = {"Items": [None], "Items/Code": ["110"], "Items/Name": ["Word"]}
        self.assertEqual(self.e.evaluate(rule, values_tt).status, RuleStatus.PASS)

        # TF: Code valid, Name invalid -> PASS
        values_tf = {"Items": [None], "Items/Code": ["110"], "Items/Name": ["Other"]}
        self.assertEqual(self.e.evaluate(rule, values_tf).status, RuleStatus.PASS)

        # FT: Code invalid, Name valid -> PASS
        values_ft = {"Items": [None], "Items/Code": ["999"], "Items/Name": ["Word"]}
        self.assertEqual(self.e.evaluate(rule, values_ft).status, RuleStatus.PASS)

        # FF: Code invalid, Name invalid -> FAIL
        values_ff = {"Items": [None], "Items/Code": ["999"], "Items/Name": ["Other"]}
        self.assertEqual(self.e.evaluate(rule, values_ff).status, RuleStatus.FAIL)

        # Missing / Missing: Code None, Name None -> FAIL
        values_missing = {"Items": [None], "Items/Code": [None], "Items/Name": [None]}
        self.assertEqual(self.e.evaluate(rule, values_missing).status, RuleStatus.FAIL)

    def test_cross_instance_comparison_match(self):
        values = {
            "Apps": [None, None],
            "Apps/Status": ["01", "02"],
            "Apps/SourceId": ["APP-100", None],
            "Apps/AppId": [None, "APP-100"],
        }
        rule = {
            "kind": "cross_instance_comparison",
            "operator": "EQ",
            "left": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "01"}},
                "field": "SourceId",
            },
            "right": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "02"}},
                "field": "AppId",
            },
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.PASS)

    def test_cross_instance_comparison_mismatch(self):
        values = {
            "Apps": [None, None],
            "Apps/Status": ["01", "02"],
            "Apps/SourceId": ["APP-100", None],
            "Apps/AppId": [None, "APP-999"],
        }
        rule = {
            "kind": "cross_instance_comparison",
            "operator": "EQ",
            "left": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "01"}},
                "field": "SourceId",
            },
            "right": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "02"}},
                "field": "AppId",
            },
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.FAIL)

    def test_cross_instance_comparison_reversed_order(self):
        values = {
            "Apps": [None, None],
            "Apps/Status": ["02", "01"],
            "Apps/SourceId": [None, "APP-100"],
            "Apps/AppId": ["APP-100", None],
        }
        rule = {
            "kind": "cross_instance_comparison",
            "operator": "EQ",
            "left": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "01"}},
                "field": "SourceId",
            },
            "right": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "02"}},
                "field": "AppId",
            },
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.PASS)

    def test_cross_instance_comparison_missing_left_role(self):
        values = {
            "Apps": [None],
            "Apps/Status": ["02"],
            "Apps/SourceId": [None],
            "Apps/AppId": ["APP-100"],
        }
        rule = {
            "kind": "cross_instance_comparison",
            "operator": "EQ",
            "left": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "01"}},
                "field": "SourceId",
            },
            "right": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "02"}},
                "field": "AppId",
            },
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.FAIL)

    def test_cross_instance_comparison_missing_right_role(self):
        values = {
            "Apps": [None],
            "Apps/Status": ["01"],
            "Apps/SourceId": ["APP-100"],
            "Apps/AppId": [None],
        }
        rule = {
            "kind": "cross_instance_comparison",
            "operator": "EQ",
            "left": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "01"}},
                "field": "SourceId",
            },
            "right": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "02"}},
                "field": "AppId",
            },
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.FAIL)

    def test_cross_instance_comparison_duplicate_left_role(self):
        values = {
            "Apps": [None, None, None],
            "Apps/Status": ["01", "01", "02"],
            "Apps/SourceId": ["APP-100", "APP-100", None],
            "Apps/AppId": [None, None, "APP-100"],
        }
        rule = {
            "kind": "cross_instance_comparison",
            "operator": "EQ",
            "left": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "01"}},
                "field": "SourceId",
            },
            "right": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "02"}},
                "field": "AppId",
            },
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.FAIL)

    def test_cross_instance_comparison_duplicate_right_role(self):
        values = {
            "Apps": [None, None, None],
            "Apps/Status": ["01", "02", "02"],
            "Apps/SourceId": ["APP-100", None, None],
            "Apps/AppId": [None, "APP-100", "APP-100"],
        }
        rule = {
            "kind": "cross_instance_comparison",
            "operator": "EQ",
            "left": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "01"}},
                "field": "SourceId",
            },
            "right": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "02"}},
                "field": "AppId",
            },
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.FAIL)

    def test_cross_instance_comparison_missing_left_field(self):
        values = {
            "Apps": [None, None],
            "Apps/Status": ["01", "02"],
            "Apps/SourceId": [None, None],
            "Apps/AppId": [None, "APP-100"],
        }
        rule = {
            "kind": "cross_instance_comparison",
            "operator": "EQ",
            "left": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "01"}},
                "field": "SourceId",
            },
            "right": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "02"}},
                "field": "AppId",
            },
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.FAIL)

    def test_cross_instance_comparison_missing_right_field(self):
        values = {
            "Apps": [None, None],
            "Apps/Status": ["01", "02"],
            "Apps/SourceId": ["APP-100", None],
            "Apps/AppId": [None, None],
        }
        rule = {
            "kind": "cross_instance_comparison",
            "operator": "EQ",
            "left": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "01"}},
                "field": "SourceId",
            },
            "right": {
                "selector": {"collection": "Apps", "where": {"field": "Status", "operator": "EQ", "value": "02"}},
                "field": "AppId",
            },
        }
        self.assertEqual(self.e.evaluate(rule, values).status, RuleStatus.FAIL)


if __name__ == "__main__":
    unittest.main()
