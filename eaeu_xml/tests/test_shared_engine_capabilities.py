import base64

import pytest

from eaeu_xml.core.errors import ProcessPackageValidationError
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator
from eaeu_xml.process_packages.validator import ProcessPackageValidator


def test_typed_date_compares_as_date_and_rejects_invalid_values():
    evaluator = StructuredRuleEvaluator()
    rule = {"kind": "comparison", "left": "a", "right": "b", "operator": "LT", "value_type": "DATE"}

    assert evaluator.evaluate(rule, {"a": "2026-02-01", "b": "2026-10-01"}).status is RuleStatus.PASS
    assert evaluator.evaluate(rule, {"a": "2026-12-01", "b": "2026-02-01"}).status is RuleStatus.FAIL
    assert evaluator.evaluate(rule, {"a": "2026-02-30", "b": "2026-03-01"}).status is RuleStatus.FAIL
    assert evaluator.evaluate(rule, {"a": None, "b": "2026-03-01"}).status is RuleStatus.FAIL

    lexical = {"kind": "comparison", "left": "a", "right": "b", "operator": "LT"}
    assert evaluator.evaluate(lexical, {"a": "10", "b": "2"}).status is RuleStatus.PASS


def test_validator_enables_date_and_decimal_without_accepting_unknown_type():
    validator = ProcessPackageValidator()
    for value_type in ("DATE", "DATETIME", "DECIMAL"):
        validator._validate_structured_rule(
            {"kind": "comparison", "left": "A", "right": "B", "operator": "EQ", "value_type": value_type},
            "TEST.MSG",
        )

    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule(
            {"kind": "comparison", "left": "A", "right": "B", "operator": "EQ", "value_type": "UNKNOWN"},
            "TEST.MSG",
        )
    assert exc.value.code == "INVALID_COMPARISON_TYPE"


def test_decimal_comparison_is_numeric_and_invalid_decimal_fails():
    evaluator = StructuredRuleEvaluator()
    rule = {"kind": "comparison", "left": "a", "right": "b", "operator": "GE", "value_type": "DECIMAL"}
    assert evaluator.evaluate(rule, {"a": "10", "b": "2"}).status is RuleStatus.PASS
    assert evaluator.evaluate(rule, {"a": "2", "b": "10"}).status is RuleStatus.FAIL
    assert evaluator.evaluate(rule, {"a": "not-a-number", "b": "10"}).status is RuleStatus.FAIL


def _conditional_cross_instance_rule():
    return {
        "kind": "cross_instance_comparison",
        "when": {"field": "Enabled", "operator": "EQ", "value": "1"},
        "operator": "EQ",
        "left": {
            "selector": {"collection": "Rows", "where": {"field": "Role", "operator": "EQ", "value": "A"}},
            "field": "Id",
        },
        "right": {
            "selector": {"collection": "Rows", "where": {"field": "Role", "operator": "EQ", "value": "B"}},
            "field": "Id",
        },
    }


def test_conditional_cross_instance_true_valid_true_invalid_and_false():
    evaluator = StructuredRuleEvaluator()
    rule = _conditional_cross_instance_rule()
    values = {"Enabled": "1", "Rows": [None, None], "Rows/Role": ["A", "B"], "Rows/Id": ["X", "X"]}
    assert evaluator.evaluate(rule, values).status is RuleStatus.PASS

    values["Rows/Id"] = ["X", "Y"]
    assert evaluator.evaluate(rule, values).status is RuleStatus.FAIL

    assert evaluator.evaluate(rule, {"Enabled": "0"}).status is RuleStatus.PASS


def test_conditional_cross_instance_missing_or_multiple_instances_fail_when_condition_applies():
    evaluator = StructuredRuleEvaluator()
    rule = _conditional_cross_instance_rule()
    assert evaluator.evaluate(rule, {"Enabled": "1"}).status is RuleStatus.FAIL

    values = {
        "Enabled": "1",
        "Rows": [None, None, None],
        "Rows/Role": ["A", "A", "B"],
        "Rows/Id": ["X", "X", "X"],
    }
    assert evaluator.evaluate(rule, values).status is RuleStatus.FAIL
    ProcessPackageValidator()._validate_structured_rule(rule, "TEST.MSG")


def _set_rule(**extra):
    return {
        "kind": "set_equivalence",
        "left": {"selector": {"collection": "Left"}, "field": "Code"},
        "right": {"selector": {"collection": "Right"}, "field": "Code"},
        **extra,
    }


def test_set_equivalence_is_order_independent_and_ignores_duplicates():
    evaluator = StructuredRuleEvaluator()
    values = {
        "Left": [None, None, None],
        "Left/Code": ["A", "A", "B"],
        "Right": [None, None],
        "Right/Code": ["B", "A"],
    }
    assert evaluator.evaluate(_set_rule(), values).status is RuleStatus.PASS
    values["Right/Code"] = ["B", "C"]
    assert evaluator.evaluate(_set_rule(), values).status is RuleStatus.FAIL


def test_set_equivalence_distinguishes_missing_from_empty():
    evaluator = StructuredRuleEvaluator()
    assert evaluator.evaluate(_set_rule(), {"Left": [], "Right": []}).status is RuleStatus.PASS
    assert evaluator.evaluate(_set_rule(), {"Right": []}).status is RuleStatus.FAIL
    assert evaluator.evaluate(_set_rule(), {}).status is RuleStatus.FAIL
    assert evaluator.evaluate(_set_rule(allow_both_missing=True), {}).status is RuleStatus.PASS


def test_set_equivalence_rejects_missing_member_field():
    evaluator = StructuredRuleEvaluator()
    values = {"Left": [None], "Left/Code": [None], "Right": [None], "Right/Code": ["A"]}
    assert evaluator.evaluate(_set_rule(), values).status is RuleStatus.FAIL
    ProcessPackageValidator()._validate_structured_rule(_set_rule(), "TEST.MSG")


def test_calendar_month_relation_supports_signed_offsets_and_year_rollover():
    evaluator = StructuredRuleEvaluator()
    next_month = {
        "kind": "comparison",
        "left": "current",
        "right": "previous",
        "operator": "EQ",
        "value_type": "CALENDAR_MONTH",
        "offset_months": 1,
    }
    assert evaluator.evaluate(next_month, {"current": "2027-01-01", "previous": "2026-12-31"}).status is RuleStatus.PASS
    assert evaluator.evaluate(next_month, {"current": "2026-02-01", "previous": "2026-01-31T23:59:59+03:00"}).status is RuleStatus.PASS
    assert evaluator.evaluate(next_month, {"current": "2026-03-01", "previous": "2026-01-31"}).status is RuleStatus.FAIL

    previous_month = {**next_month, "left": "previous", "right": "current", "offset_months": -1}
    assert evaluator.evaluate(previous_month, {"current": "2027-01-15", "previous": "2026-12-01"}).status is RuleStatus.PASS
    assert evaluator.evaluate(next_month, {"current": "bad", "previous": "2026-12-01"}).status is RuleStatus.FAIL


def test_validator_rejects_invalid_calendar_month_offset():
    validator = ProcessPackageValidator()
    validator._validate_structured_rule(
        {
            "kind": "comparison",
            "left": "A",
            "right": "B",
            "operator": "EQ",
            "value_type": "CALENDAR_MONTH",
            "offset_months": -1,
        },
        "TEST.MSG",
    )
    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule(
            {
                "kind": "comparison",
                "left": "A",
                "right": "B",
                "operator": "EQ",
                "value_type": "CALENDAR_MONTH",
                "offset_months": True,
            },
            "TEST.MSG",
        )
    assert exc.value.code == "INVALID_CALENDAR_MONTH_OFFSET"


def _relative_selector():
    return {
        "collection": "Reports",
        "relative_to_context": {
            "candidate_field": "EventDate",
            "context_field": "EventDate",
            "value_type": "CALENDAR_MONTH",
            "offset_months": -1,
        },
    }


def test_context_relative_selector_is_order_independent_and_stays_with_siblings():
    evaluator = StructuredRuleEvaluator()
    values = {
        "Reports": [None, None, None],
        "Reports/EventDate": ["2026-03-20", "2026-01-10", "2026-02-05"],
        "Reports/Amount": ["30", "10", "20"],
    }
    contexts = evaluator._contexts_for_path("Reports", values)
    march = contexts[0]
    january = contexts[1]
    selected = evaluator._select_contexts(_relative_selector(), values, context=march)
    assert [item.fields["Amount"] for item in selected] == ["20"]
    assert evaluator._select_contexts(_relative_selector(), values, context=january) == []


def test_context_relative_selector_duplicate_match_is_deterministic_failure_for_unique_operand():
    evaluator = StructuredRuleEvaluator()
    values = {
        "Reports": [None, None, None],
        "Reports/EventDate": ["2026-03-20", "2026-02-05", "2026-02-28"],
        "Reports/Amount": ["30", "20", "20"],
    }
    rule = {
        "kind": "for_each",
        "selector": {"collection": "Reports", "position": 1},
        "assertions": [
            {
                "kind": "comparison",
                "left": {"field": "Amount"},
                "operator": "GE",
                "right": {"selector": _relative_selector(), "field": "Amount"},
                "value_type": "DECIMAL",
            }
        ],
    }
    assert evaluator.evaluate(rule, values).status is RuleStatus.FAIL
    ProcessPackageValidator()._validate_structured_rule(rule, "TEST.MSG")


def test_relative_selector_is_rejected_without_outer_rule_context():
    validator = ProcessPackageValidator()
    with pytest.raises(ProcessPackageValidationError) as exc:
        validator._validate_structured_rule(
            {
                "kind": "cross_instance_comparison",
                "operator": "EQ",
                "left": {"selector": _relative_selector(), "field": "Amount"},
                "right": {"selector": {"collection": "Reports", "position": 1}, "field": "Amount"},
            },
            "TEST.MSG",
        )
    assert exc.value.code == "INVALID_RELATIVE_SELECTOR"


def _aggregate_rule():
    return {
        "kind": "aggregate_comparison",
        "left": {"selector": {"collection": "Reports/Total"}, "value_field": "#text", "aggregation": "VALUE"},
        "operator": "EQ",
        "right": {"selector": {"collection": "Reports/Parts"}, "value_field": "#text", "aggregation": "SUM"},
    }


def test_context_scoped_aggregate_passes_per_parent_and_detects_cross_parent_compensation():
    evaluator = StructuredRuleEvaluator()
    rule = {"kind": "for_each", "selector": {"collection": "Reports"}, "assertions": [_aggregate_rule()]}
    values = {
        "Reports": [None, None],
        "Reports/Total": ["3", "7"],
        "Reports/Parts": [["1", "2"], ["3", "4"]],
    }
    assert evaluator.evaluate(rule, values).status is RuleStatus.PASS

    values["Reports/Total"] = ["4", "6"]
    assert evaluator.evaluate(rule, values).status is RuleStatus.FAIL
    ProcessPackageValidator()._validate_structured_rule(rule, "TEST.MSG")


def test_context_scoped_aggregate_keeps_sum_zero_semantics_and_fails_invalid_decimal():
    evaluator = StructuredRuleEvaluator()
    rule = {"kind": "for_each", "selector": {"collection": "Reports"}, "assertions": [_aggregate_rule()]}
    assert evaluator.evaluate(
        rule,
        {"Reports": [None], "Reports/Total": ["0"], "Reports/Parts": [[]]},
    ).status is RuleStatus.PASS
    assert evaluator.evaluate(
        rule,
        {"Reports": [None], "Reports/Total": ["0"], "Reports/Parts": [["bad"]]},
    ).status is RuleStatus.FAIL
    assert evaluator.evaluate(
        rule,
        {"Reports": [None], "Reports/Parts": [["0"]]},
    ).status is RuleStatus.FAIL


def test_document_scope_aggregate_behavior_remains_available():
    evaluator = StructuredRuleEvaluator()
    rule = {
        "kind": "aggregate_comparison",
        "left": {"selector": {"collection": "Total"}, "value_field": "#text", "aggregation": "VALUE"},
        "operator": "EQ",
        "right": {"selector": {"collection": "Parts"}, "value_field": "#text", "aggregation": "SUM"},
    }
    assert evaluator.evaluate(rule, {"Total": "10", "Parts": ["4", "6"]}).status is RuleStatus.PASS
    assert evaluator.evaluate(rule, {"Total": "9", "Parts": ["4", "6"]}).status is RuleStatus.FAIL


def _binary_length_rule(operator="LE", byte_length=4):
    return {"kind": "decoded_binary_length", "target": "Payload", "operator": operator, "byte_length": byte_length}


def test_decoded_binary_length_measures_bytes_not_encoded_text():
    evaluator = StructuredRuleEvaluator()
    encoded = base64.b64encode(b"abcd").decode("ascii")
    assert len(encoded) > 4
    assert evaluator.evaluate(_binary_length_rule("EQ", 4), {"Payload": encoded}).status is RuleStatus.PASS
    assert evaluator.evaluate(_binary_length_rule("LT", 4), {"Payload": encoded}).status is RuleStatus.FAIL


def test_decoded_binary_length_handles_zero_boundary_whitespace_and_invalid_base64():
    evaluator = StructuredRuleEvaluator()
    assert evaluator.evaluate(_binary_length_rule("EQ", 0), {"Payload": ""}).status is RuleStatus.PASS
    assert evaluator.evaluate(_binary_length_rule("LE", 3), {"Payload": "YWJj\n"}).status is RuleStatus.PASS
    assert evaluator.evaluate(_binary_length_rule("LE", 3), {"Payload": "not valid !!!"}).status is RuleStatus.FAIL
    ProcessPackageValidator()._validate_structured_rule(_binary_length_rule("LE", 3), "TEST.MSG")
