import copy
import json
from pathlib import Path

import pytest

from all_transactions_matrix import test_values as _matrix_test_values
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).parents[1]
RULES_DIR = PACKAGE / "message_rules"
BASELINE_159 = PACKAGE.parent / "codex_reports" / "OP26_P_MM_01" / "mapped_structured_rules.json"

SAFE_IMPLEMENTED_IDS = {
    "OP26.P_MM_01.P.MM.01.MSG.001.REQ.034",
    "OP26.P_MM_01.P.MM.01.MSG.002.REQ.006",
    *{f"OP26.P_MM_01.P.MM.01.MSG.002.REQ.{number:03d}" for number in range(51, 61)},
    *{f"OP26.P_MM_01.P.MM.01.MSG.002.REQ.{number:03d}" for number in range(62, 84)},
    "OP26.P_MM_01.P.MM.01.MSG.002.REQ.085",
    "OP26.P_MM_01.P.MM.01.MSG.003.REQ.008",
    "OP26.P_MM_01.P.MM.01.MSG.007.REQ.003",
    "OP26.P_MM_01.P.MM.01.MSG.010.REQ.002",
    "OP26.P_MM_01.P.MM.01.MSG.016.REQ.001",
    "OP26.P_MM_01.P.MM.01.MSG.019.REQ.004",
    "OP26.P_MM_01.P.MM.01.MSG.020.REQ.004",
    "OP26.P_MM_01.P.MM.01.MSG.021.REQ.009",
    "OP26.P_MM_01.P.MM.01.MSG.023.REQ.007",
    "OP26.P_MM_01.P.MM.01.MSG.024.REQ.004",
    "OP26.P_MM_01.P.MM.01.MSG.028.REQ.005#A",
}

RECLASSIFIED_BLOCKED_IDS = {
    "OP26.P_MM_01.P.MM.01.MSG.001.REQ.046",
    "OP26.P_MM_01.P.MM.01.MSG.002.REQ.013",
    "OP26.P_MM_01.P.MM.01.MSG.002.REQ.050",
    "OP26.P_MM_01.P.MM.01.MSG.002.REQ.061",
    "OP26.P_MM_01.P.MM.01.MSG.002.REQ.086",
    "OP26.P_MM_01.P.MM.01.MSG.014.REQ.002",
    "OP26.P_MM_01.P.MM.01.MSG.020.REQ.011",
}


def _all_rules():
    rules = []
    for path in sorted(RULES_DIR.glob("P.MM.01.MSG.*.yaml")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        rules.extend(payload.get("structured_rules", []))
    return rules


def _safe_rules():
    return [rule for rule in _all_rules() if rule.get("rule_id") in SAFE_IMPLEMENTED_IDS]


def _field_path(context_path, field):
    if field == "#text":
        return context_path
    return f"{context_path}/{field}" if context_path else field


def _set_atomic_condition(values, context_path, condition, truth):
    path = _field_path(context_path, condition["field"])
    operator = condition["operator"]
    expected = condition.get("value")
    if operator == "EQ":
        values[path] = expected if truth else "__INVALID__"
    elif operator == "NE":
        if truth:
            values[path] = "__PRESENT__" if expected is None else "__DIFFERENT__"
        else:
            values[path] = expected
    elif operator == "IN":
        values[path] = next(iter(expected)) if truth else "__INVALID__"
    elif operator == "NOT_IN":
        values[path] = "__VALID__" if truth else next(iter(expected))
    else:
        raise AssertionError(f"Unsupported test condition operator: {operator}")


def _set_condition(values, context_path, condition, truth=True):
    if "any" in condition:
        items = condition["any"]
        if truth:
            _set_condition(values, context_path, items[0], True)
        else:
            for item in items:
                _set_condition(values, context_path, item, False)
        return
    if "all" in condition:
        items = condition["all"]
        if truth:
            for item in items:
                _set_condition(values, context_path, item, True)
        else:
            _set_condition(values, context_path, items[0], False)
        return
    if "not" in condition:
        _set_condition(values, context_path, condition["not"], not truth)
        return
    _set_atomic_condition(values, context_path, condition, truth)


def _materialize_selector(values, selector):
    parent = selector.get("parent")
    if parent:
        parent_path = parent["collection"]
        values[parent_path] = "__PARENT__"
        if parent.get("where"):
            _set_condition(values, parent_path, parent["where"], True)
    collection = selector["collection"]
    values[collection] = "__CONTEXT__"
    if selector.get("where"):
        _set_condition(values, collection, selector["where"], True)
    return collection


def _set_target(values, context_path, target, present, value="__VALUE__"):
    field = target.get("field") if isinstance(target, dict) else target
    path = _field_path(context_path, field)
    if present:
        values[path] = value
    else:
        values.pop(path, None)


def _apply_assertion(values, context_path, assertion, valid):
    kind = assertion["kind"]
    if kind == "condition":
        _set_condition(values, context_path, assertion["condition"], valid)
        return
    if kind == "fixed_value":
        _set_target(
            values,
            context_path,
            assertion["target"],
            True,
            assertion.get("value") if valid else "__INVALID__",
        )
        return
    if kind == "presence":
        required = assertion["state"] == "REQUIRED"
        _set_target(values, context_path, assertion["target"], required == valid)
        return
    if kind == "conditional_presence":
        _set_condition(values, context_path, assertion["condition"], True)
        required = assertion["state"] == "REQUIRED"
        _set_target(values, context_path, assertion["target"], required == valid)
        return
    raise AssertionError(f"Unsupported assertion in SAFE52 test vector: {kind}")


def _vectors(rule):
    kind = rule["kind"]
    positive = {}
    if kind == "for_each":
        context = _materialize_selector(positive, rule["selector"])
        for assertion in rule["assertions"]:
            _apply_assertion(positive, context, assertion, True)
        negative = copy.deepcopy(positive)
        _apply_assertion(negative, context, rule["assertions"][0], False)
        return positive, negative
    if kind == "conditional_presence":
        context = _materialize_selector(positive, rule["scope"])
        _set_condition(positive, context, rule["condition"], True)
        required = rule["state"] == "REQUIRED"
        _set_target(positive, context, rule["target"], required)
        negative = copy.deepcopy(positive)
        _set_target(negative, context, rule["target"], not required)
        return positive, negative
    raise AssertionError(f"Unsupported SAFE52 rule kind: {kind}")


def test_safe52_scope_is_exactly_45_implemented_and_7_reclassified_blocked():
    rules = _all_rules()
    present_ids = {rule.get("rule_id") for rule in rules}
    assert len(SAFE_IMPLEMENTED_IDS) == 45
    assert SAFE_IMPLEMENTED_IDS <= present_ids
    assert RECLASSIFIED_BLOCKED_IDS.isdisjoint(present_ids)


def test_preexisting_159_canonical_rules_are_preserved():
    baseline = json.loads(BASELINE_159.read_text(encoding="utf-8"))
    baseline_ids = {
        rule["rule_id"]
        for rules in baseline.values()
        for rule in rules
    }
    current_ids = {rule["rule_id"] for rule in _all_rules()}
    assert len(baseline_ids) == 159
    assert baseline_ids <= current_ids
    assert len(current_ids) == 204


@pytest.mark.parametrize("rule", _safe_rules(), ids=lambda rule: rule.get("production_rule_id"))
def test_each_safe52_mapping_has_positive_and_negative_runtime_proof(rule):
    evaluator = StructuredRuleEvaluator()
    positive, negative = _vectors(rule)
    assert evaluator.evaluate(rule, positive).status is RuleStatus.PASS
    assert evaluator.evaluate(rule, negative).status is RuleStatus.FAIL


def test_each_safe52_mapping_has_confirmed_source_trace():
    rules = _safe_rules()
    assert {rule["rule_id"] for rule in rules} == SAFE_IMPLEMENTED_IDS
    assert all(rule.get("source_refs") for rule in rules)
    assert all(ref.get("status") == "CONFIRMED" for rule in rules for ref in rule["source_refs"])
    assert all(ref.get("page") for rule in rules for ref in rule["source_refs"])


@pytest.mark.parametrize(
    "message_code,rule_ids",
    [
        (
            "P.MM.01.MSG.023",
            [
                "OP26.P_MM_01.P.MM.01.MSG.023.REQ.001",
                "OP26.P_MM_01.P.MM.01.MSG.023.REQ.006",
                "OP26.P_MM_01.P.MM.01.MSG.023.REQ.009",
            ],
        ),
        (
            "P.MM.01.MSG.024",
            [
                "OP26.P_MM_01.P.MM.01.MSG.024.REQ.003",
                "OP26.P_MM_01.P.MM.01.MSG.024.REQ.008",
                "OP26.P_MM_01.P.MM.01.MSG.024.REQ.010",
            ],
        ),
    ],
)
def test_runtime6_generic_fixture_now_satisfies_local_rules(message_code, rule_ids):
    engine = EaeuXmlEngine.load_process(PACKAGE)
    result = engine.validate_body(
        message_code,
        _matrix_test_values(engine, message_code),
        mode=GenerationMode.TEST,
    )
    statuses = {evaluation.rule_id: evaluation.status for evaluation in result.rule_evaluations}
    assert {rule_id: statuses[rule_id] for rule_id in rule_ids} == {
        rule_id: RuleStatus.PASS for rule_id in rule_ids
    }


def test_msg024_other_file_code_uses_normative_0199_literal():
    rules = [
        rule
        for rule in _all_rules()
        if rule.get("rule_id") == "OP26.P_MM_01.P.MM.01.MSG.024.REQ.009"
    ]
    assert len(rules) == 1
    condition = rules[0]["assertions"][0]["condition"]
    assert condition["value"] == "0199"
