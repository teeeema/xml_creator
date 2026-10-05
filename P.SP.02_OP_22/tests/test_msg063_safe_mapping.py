import json
from pathlib import Path
import pytest

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.063"

FULLY_MAPPABLE_SET = {1}
SAFE_PARTIAL_SET = {4}
EXTERNAL_SET = {2, 3}
AMBIGUOUS_SET = set()
ENGINE_UNSUPPORTED_SET = set()
SOURCE_CONFLICT_SET = set()
UNMAPPED_SET = EXTERNAL_SET | AMBIGUOUS_SET | ENGINE_UNSUPPORTED_SET


def _raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def _rules(code):
    p = f"{MESSAGE}.T82.REQ.{code}"
    return [r for r in _raw()["structured_rules"] if r["rule_id"] == p or r["rule_id"].startswith(p + ".") or r["rule_id"].startswith(p + "_")]


def _inventory(code):
    return next(item for item in _raw()["mapping_audit"]["inventory"] if item["requirement_code"] == str(code))


def test_expanded_normative_inventory_has_exactly_4_distinct_requirements():
    inventory = _raw()["mapping_audit"]["inventory"]
    codes = [int(item["requirement_code"]) for item in inventory]
    assert len(inventory) == 4
    assert len(set(codes)) == 4
    assert sorted(codes) == [1, 2, 3, 4]
    assert _raw()["mapping_audit"]["expanded_requirement_count"] == 4
    assert _raw()["mapping_audit"]["captured_row_count"] == 4


def test_classification_counts_and_arithmetic_sum_to_4():
    audit = _raw()["mapping_audit"]
    counts = audit["classification_counts"]
    assert counts == {
        "FULLY_MAPPABLE": 1,
        "SAFE_PARTIAL": 1,
        "EXTERNAL": 2,
        "AMBIGUOUS": 0,
        "ENGINE_UNSUPPORTED": 0,
        "SOURCE_CONFLICT": 0,
    }
    assert sum(counts.values()) == 4
    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULLY_MAPPABLE_SET)
    assert audit["summary"]["SAFE_PARTIAL"] == sorted(SAFE_PARTIAL_SET)
    assert audit["summary"]["EXTERNAL"] == sorted(EXTERNAL_SET)
    assert audit["summary"]["AMBIGUOUS"] == sorted(AMBIGUOUS_SET)
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == sorted(ENGINE_UNSUPPORTED_SET)
    assert audit["summary"]["SOURCE_CONFLICT"] == sorted(SOURCE_CONFLICT_SET)


def test_provenance_and_source_refs():
    for item in _raw()["mapping_audit"]["inventory"]:
        refs = item["source_refs"]
        assert len(refs) >= 1
        for ref in refs:
            assert ref["document"] == "ОП_22.pdf"
            assert ref["table"] == "82"
            assert ref["status"] == "CONFIRMED"
            assert ref["page"] in (820, 821)


def test_external_and_unmapped_requirements_have_documented_dependencies():
    for code in UNMAPPED_SET:
        inv = _inventory(code)
        assert inv["mapping_status"] == "UNMAPPED"
        assert inv["external_dependency"] is not None
        assert len(inv["unmapped_remainder"]) > 0


def test_safe_partial_requirements_have_safe_fragment_and_remainder():
    for code in SAFE_PARTIAL_SET:
        inv = _inventory(code)
        assert inv["mapping_status"] == "EXECUTABLE"
        assert inv["safe_fragment"] is not None
        assert len(inv["unmapped_remainder"]) > 0
        assert inv["external_dependency"] is not None


def test_structured_rules_match_executable_requirements():
    structured_rules = _raw()["structured_rules"]
    assert len(structured_rules) == 2
    rule_ids = {r["rule_id"] for r in structured_rules}
    assert "P.SP.02.MSG.063.T82.REQ.1" in rule_ids
    assert "P.SP.02.MSG.063.T82.REQ.4" in rule_ids


def test_req1_selection_cardinality_rule():
    rules = _rules(1)
    assert len(rules) == 1
    r = rules[0]
    assert r["kind"] == "selection_cardinality"
    assert r["selector"]["collection"] == "ipcdo:TrademarkApplicationDetails"
    assert r["min_occurs"] == 1
    assert r["max_occurs"] == 1

    ev = StructuredRuleEvaluator()
    # 1 instance -> PASS
    res1 = ev.evaluate(r, {"ipcdo:TrademarkApplicationDetails": [None]})
    assert res1.status is RuleStatus.PASS

    # 0 instances -> FAIL
    res0 = ev.evaluate(r, {"ipcdo:TrademarkApplicationDetails": []})
    assert res0.status is RuleStatus.FAIL

    # 2 instances -> FAIL
    res2 = ev.evaluate(r, {"ipcdo:TrademarkApplicationDetails": [None, None]})
    assert res2.status is RuleStatus.FAIL


def test_req4_safe_partial_presence_rule():
    rules = _rules(4)
    assert len(rules) == 1
    r = rules[0]
    assert r["kind"] == "for_each"
    assert r["selector"]["collection"] == "ipcdo:TrademarkApplicationDetails"
    assert r["mapping_status"] == "PARTIAL"
    assert len(r["assertions"]) == 1
    assert r["assertions"][0]["kind"] == "presence"
    assert r["assertions"][0]["target"]["field"] == "ipsdo:TrademarkApplicationId"
    assert r["assertions"][0]["state"] == "REQUIRED"

    ev = StructuredRuleEvaluator()
    # With ID -> PASS
    res_pass = ev.evaluate(r, {
        "ipcdo:TrademarkApplicationDetails": [None],
        "ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId": ["2026/RU-000001"],
    })
    assert res_pass.status is RuleStatus.PASS

    # Without ID -> FAIL
    res_fail = ev.evaluate(r, {
        "ipcdo:TrademarkApplicationDetails": [None],
        "ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId": [None],
    })
    assert res_fail.status is RuleStatus.FAIL
