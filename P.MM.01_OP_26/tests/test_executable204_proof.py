import copy
import csv
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from all_transactions_matrix import test_values as _test_values
from eaeu_xml.core.errors import BodyValidationError
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).parents[1]
BLOCKED_MATRIX = (
    PACKAGE.parent
    / "codex_reports"
    / "OP26_P_MM_01"
    / "BLOCKER_RECOVERY_2"
    / "OP26_BLOCKER35_MATRIX.csv"
)


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _rule_cases():
    engine = _engine()
    return tuple(
        (message_code, rule)
        for message_code, message_rules in sorted(engine.rules.items())
        for rule in message_rules.structured_rules
    )


RULE_CASES = _rule_cases()


def _canonical_cases():
    grouped = defaultdict(list)
    for message_code, rule in RULE_CASES:
        grouped[(message_code, rule["rule_id"])].append(rule)
    return tuple((message_code, canonical_id, tuple(rules)) for (message_code, canonical_id), rules in sorted(grouped.items()))


CANONICAL_CASES = _canonical_cases()

REAL_XML_BLOCKED_MESSAGES = {
    "P.MM.01.MSG.002",
    "P.MM.01.MSG.023",
    "P.MM.01.MSG.024",
}


def _field_path(context_path, field):
    if field == "#text":
        return context_path
    if not context_path or field == context_path or field.startswith(context_path + "/"):
        return field
    return f"{context_path}/{field}"


def _different_value(expected):
    if expected is None:
        return "__PRESENT__"
    if isinstance(expected, bool):
        return not expected
    if isinstance(expected, (int, float)):
        return expected + 1
    return "__INVALID__" if expected != "__INVALID__" else "__DIFFERENT__"


def _set_atomic_condition(values, context_path, condition, truth):
    path = _field_path(context_path, condition["field"])
    operator = condition["operator"]
    expected = condition.get("value")

    if operator == "EQ":
        values[path] = expected if truth else _different_value(expected)
    elif operator == "NE":
        values[path] = _different_value(expected) if truth else expected
    elif operator == "IN":
        values[path] = expected[0] if truth else "__INVALID__"
    elif operator == "NOT_IN":
        values[path] = "__VALID__" if truth else expected[0]
    elif operator == "LE":
        values[path] = expected if truth else expected + 1
    else:
        raise AssertionError(f"Unsupported OP26 proof condition operator: {operator}")


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
            assertion.get("value") if valid else _different_value(assertion.get("value")),
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
    if kind == "conditional_fixed_value":
        _set_condition(values, context_path, assertion["condition"], True)
        _set_target(
            values,
            context_path,
            assertion["target"],
            True,
            assertion.get("value") if valid else _different_value(assertion.get("value")),
        )
        return
    raise AssertionError(f"Unsupported OP26 proof assertion kind: {kind}")


def _vectors(rule):
    kind = rule["kind"]
    positive = {}

    if kind == "presence":
        required = rule["state"] == "REQUIRED"
        _set_target(positive, "", rule["target"], required)
        negative = copy.deepcopy(positive)
        _set_target(negative, "", rule["target"], not required)
        return positive, negative

    if kind == "selection_cardinality":
        assert rule.get("min_occurs") == 1 and rule.get("max_occurs") == 1
        _materialize_selector(positive, rule["selector"])
        return positive, {}

    if kind in {"conditional_presence", "conditional_fixed_value"}:
        context = _materialize_selector(positive, rule["scope"])
        _set_condition(positive, context, rule["condition"], True)
        if kind == "conditional_presence":
            required = rule["state"] == "REQUIRED"
            _set_target(positive, context, rule["target"], required)
            negative = copy.deepcopy(positive)
            _set_target(negative, context, rule["target"], not required)
        else:
            _set_target(positive, context, rule["target"], True, rule["value"])
            negative = copy.deepcopy(positive)
            _set_target(negative, context, rule["target"], True, _different_value(rule["value"]))
        return positive, negative

    if kind == "for_each":
        context = _materialize_selector(positive, rule["selector"])
        for assertion in rule["assertions"]:
            _apply_assertion(positive, context, assertion, True)

        evaluator = StructuredRuleEvaluator()
        for assertion in rule["assertions"]:
            negative = copy.deepcopy(positive)
            _apply_assertion(negative, context, assertion, False)
            if evaluator.evaluate(rule, negative).status is RuleStatus.FAIL:
                return positive, negative
        raise AssertionError(f"No deterministic negative vector found for {rule['production_rule_id']}")

    raise AssertionError(f"Unsupported OP26 proof rule kind: {kind}")


def _blocked_ids():
    with BLOCKED_MATRIX.open(encoding="utf-8-sig", newline="") as handle:
        return {row["canonical_requirement_id"] for row in csv.DictReader(handle)}


def test_executable204_inventory_is_exact_and_disjoint_from_blocked35():
    executable_ids = {rule["rule_id"] for _, rule in RULE_CASES}
    blocked_ids = _blocked_ids()
    assert len(RULE_CASES) == 252
    assert len(executable_ids) == 204
    assert len(blocked_ids) == 35
    assert executable_ids.isdisjoint(blocked_ids)
    assert len(executable_ids | blocked_ids) == 239


@pytest.mark.parametrize(
    "message_code,rule",
    RULE_CASES,
    ids=[rule["production_rule_id"] for _, rule in RULE_CASES],
)
def test_each_production_rule_has_source_positive_and_negative_proof(message_code, rule):
    del message_code
    assert rule.get("source_refs")
    assert all(ref.get("status") == "CONFIRMED" for ref in rule["source_refs"])

    positive, negative = _vectors(rule)
    evaluator = StructuredRuleEvaluator()
    assert evaluator.evaluate(rule, positive).status is RuleStatus.PASS
    assert evaluator.evaluate(rule, negative).status is RuleStatus.FAIL


@pytest.mark.parametrize(
    "message_code,canonical_id,rules",
    CANONICAL_CASES,
    ids=[canonical_id for _, canonical_id, _ in CANONICAL_CASES],
)
def test_each_executable_requirement_has_runtime_proof(message_code, canonical_id, rules):
    engine = _engine()
    values = _test_values(engine, message_code)
    validation = engine.validate_body(message_code, values, mode=GenerationMode.TEST)
    evaluations = [item for item in validation.rule_evaluations if item.rule_id == canonical_id]

    assert len(evaluations) == len(rules)
    assert all(item.status is RuleStatus.PASS for item in evaluations)


@pytest.mark.parametrize(
    "message_code,canonical_id,rules",
    CANONICAL_CASES,
    ids=[canonical_id for _, canonical_id, _ in CANONICAL_CASES],
)
def test_each_executable_requirement_has_real_xml_proof_or_explicit_gap(message_code, canonical_id, rules):
    del canonical_id, rules
    engine = _engine()
    values = _test_values(engine, message_code)

    if message_code in REAL_XML_BLOCKED_MESSAGES:
        with pytest.raises(BodyValidationError) as exc_info:
            engine.build_body(message_code, values, mode=GenerationMode.TEST)
        issue_codes = {issue.code for issue in exc_info.value.issues}
        assert "NORMATIVE_CONFLICT" in issue_codes
        return

    body = engine.build_body(message_code, values, mode=GenerationMode.TEST)
    xml_element = body.serialize_xml_element()
    xml_bytes = ET.tostring(xml_element, encoding="utf-8")
    reparsed = ET.fromstring(xml_bytes)
    structure = engine.get_structure(message_code, mode=GenerationMode.TEST)
    assert reparsed.tag == f"{{{structure.namespace}}}{structure.root_element}"
