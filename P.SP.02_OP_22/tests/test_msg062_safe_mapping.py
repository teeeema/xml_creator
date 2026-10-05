import json
from pathlib import Path
import pytest

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.062"

FULLY_MAPPABLE_SET = {
    1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
    30, 31, 32, 33, 34, 35, 36, 37, 38, 39
}
SAFE_PARTIAL_SET = {4}
EXTERNAL_SET = {2, 3}
AMBIGUOUS_SET = {13}
ENGINE_UNSUPPORTED_SET = {18, 19}
SOURCE_CONFLICT_SET = set()
UNMAPPED_SET = EXTERNAL_SET | AMBIGUOUS_SET | ENGINE_UNSUPPORTED_SET


def _raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def _rules(code):
    p = f"{MESSAGE}.T81.REQ.{code}"
    return [r for r in _raw()["structured_rules"] if r["rule_id"] == p or r["rule_id"].startswith(p + ".") or r["rule_id"].startswith(p + "_")]


def _inventory(code):
    return next(item for item in _raw()["mapping_audit"]["inventory"] if item["requirement_code"] == str(code))


def test_expanded_normative_inventory_has_exactly_39_distinct_requirements():
    inventory = _raw()["mapping_audit"]["inventory"]
    codes = [int(item["requirement_code"]) for item in inventory]
    assert len(inventory) == 39
    assert len(set(codes)) == 39
    assert sorted(codes) == list(range(1, 40))
    assert _raw()["mapping_audit"]["expanded_requirement_count"] == 39
    assert _raw()["mapping_audit"]["captured_row_count"] == 16


def test_classification_counts_and_arithmetic_sum_to_39():
    audit = _raw()["mapping_audit"]
    counts = audit["classification_counts"]
    assert counts == {
        "FULLY_MAPPABLE": 33,
        "SAFE_PARTIAL": 1,
        "EXTERNAL": 2,
        "AMBIGUOUS": 1,
        "ENGINE_UNSUPPORTED": 2,
        "SOURCE_CONFLICT": 0,
    }
    assert sum(counts.values()) == 39
    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULLY_MAPPABLE_SET)
    assert audit["summary"]["SAFE_PARTIAL"] == sorted(SAFE_PARTIAL_SET)
    assert audit["summary"]["EXTERNAL"] == sorted(EXTERNAL_SET)
    assert audit["summary"]["AMBIGUOUS"] == sorted(AMBIGUOUS_SET)
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == sorted(ENGINE_UNSUPPORTED_SET)
    assert audit["summary"]["SOURCE_CONFLICT"] == sorted(SOURCE_CONFLICT_SET)


def test_unmapped_requirements_have_no_executable_structured_rules():
    for code in UNMAPPED_SET:
        assert not _rules(code), f"Expected no structured rules for unmapped REQ {code}"
        item = _inventory(code)
        assert item["mapping_status"] == "UNMAPPED"


def test_inherited_requirements_have_confirmed_three_hop_source_refs():
    for code in range(6, 30):
        item = _inventory(code)
        refs = item["source_refs"]
        assert len(refs) == 3, f"Expected 3-hop source refs for REQ {code}"
        assert refs[0]["table"] == "81"
        assert refs[1]["table"] == "44"
        assert refs[2]["table"] == "34"
        assert all(r["status"] == "CONFIRMED" for r in refs)


def test_req1_selection_cardinality():
    r = _rules(1)
    assert len(r) == 1
    assert r[0]["kind"] == "selection_cardinality"
    assert r[0]["min_occurs"] == 1
    assert r[0]["max_occurs"] == 1
    assert r[0]["selector"] == {"collection": "ipcdo:TrademarkApplicationDetails"}

    evaluator = StructuredRuleEvaluator()
    assert evaluator.evaluate(r[0], {}).status == RuleStatus.FAIL
    assert evaluator.evaluate(r[0], {"ipcdo:TrademarkApplicationDetails": [None]}).status == RuleStatus.PASS
    assert evaluator.evaluate(r[0], {"ipcdo:TrademarkApplicationDetails": [None, None]}).status == RuleStatus.FAIL


def test_req4_safe_partial_mapping():
    r = _rules(4)
    assert len(r) == 1
    assert r[0]["mapping_status"] == "PARTIAL"
    assert r[0]["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:TrademarkApplicationId"}, "state": "REQUIRED"}
    ]
    item = _inventory(4)
    assert item["classification"] == "SAFE_PARTIAL"
    assert item["mapping_status"] == "PARTIAL_EXECUTABLE"
    assert len(item["unmapped_remainder"]) == 4


def test_req5_argument_details_required():
    r = _rules(5)
    assert len(r) == 1
    rule = r[0]
    evaluator = StructuredRuleEvaluator()
    app = "ipcdo:TrademarkApplicationDetails"

    assert evaluator.evaluate(rule, {app: [None]}).status == RuleStatus.FAIL
    assert evaluator.evaluate(rule, {app: [None], f"{app}/ipcdo:ArgumentDetails": [""]}).status == RuleStatus.PASS


def test_req26_trademark_kind_code_or_name_condition():
    r = _rules(26)
    assert len(r) == 1
    rule = r[0]
    evaluator = StructuredRuleEvaluator()
    prefix = "ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkDetails"

    # With matching kind code
    vals_code = {
        prefix: [None],
        f"{prefix}/ipsdo:TrademarkKindCode": ["110"],
        f"{prefix}/ipsdo:TrademarkKindName": [None],
    }
    assert evaluator.evaluate(rule, vals_code).status == RuleStatus.PASS

    # With matching kind name
    vals_name = {
        prefix: [None],
        f"{prefix}/ipsdo:TrademarkKindCode": [None],
        f"{prefix}/ipsdo:TrademarkKindName": ["Словесный знак"],
    }
    assert evaluator.evaluate(rule, vals_name).status == RuleStatus.PASS

    # With invalid kind code and name
    vals_invalid = {
        prefix: [None],
        f"{prefix}/ipsdo:TrademarkKindCode": ["999"],
        f"{prefix}/ipsdo:TrademarkKindName": ["Неизвестный знак"],
    }
    assert evaluator.evaluate(rule, vals_invalid).status == RuleStatus.FAIL


def test_req27_conditional_picture_and_colour():
    r = _rules(27)
    assert len(r) == 1
    rule = r[0]
    evaluator = StructuredRuleEvaluator()
    prefix = "ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkDetails"

    # Verbal mark does not require picture/colour
    vals_verbal = {
        prefix: [None],
        f"{prefix}/ipsdo:TrademarkKindCode": ["110"],
        f"{prefix}/ipsdo:TrademarkKindName": ["Словесный знак"],
    }
    assert evaluator.evaluate(rule, vals_verbal).status == RuleStatus.PASS

    # Combined mark requires picture and colour
    vals_combined_incomplete = {
        prefix: [None],
        f"{prefix}/ipsdo:TrademarkKindCode": ["180"],
        f"{prefix}/ipsdo:TrademarkKindName": ["Комбинированный знак"],
    }
    assert evaluator.evaluate(rule, vals_combined_incomplete).status == RuleStatus.FAIL

    vals_combined_complete = {
        prefix: [None],
        f"{prefix}/ipsdo:TrademarkKindCode": ["180"],
        f"{prefix}/ipsdo:TrademarkKindName": ["Комбинированный знак"],
        f"{prefix}/ipsdo:TrademarkPicture": ["dGVzdA=="],
        f"{prefix}/ipsdo:TrademarkColourName": ["красный"],
    }
    assert evaluator.evaluate(rule, vals_combined_complete).status == RuleStatus.PASS


def test_req28_collective_mark_indicator():
    r = _rules(28)
    assert len(r) == 1
    evaluator = StructuredRuleEvaluator()
    prefix = "ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkDetails"
    assert evaluator.evaluate(r[0], {prefix: [None], f"{prefix}/ipsdo:CollectiveMarkIndicator": ["1"]}).status == RuleStatus.PASS
    assert evaluator.evaluate(r[0], {prefix: [None], f"{prefix}/ipsdo:CollectiveMarkIndicator": ["0"]}).status == RuleStatus.PASS
    assert evaluator.evaluate(r[0], {prefix: [None], f"{prefix}/ipsdo:CollectiveMarkIndicator": ["2"]}).status == RuleStatus.FAIL


def test_req30_trademark_claim_details():
    r = _rules(30)
    assert len(r) == 1
    rule = r[0]
    evaluator = StructuredRuleEvaluator()
    prefix = "ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkClaimDetails"

    valid = {
        prefix: [None],
        f"{prefix}/ipcdo:StakeholderDetails": [""],
        f"{prefix}/ipsdo:RequestId": ["REQ-001"],
        f"{prefix}/ipsdo:RequestDate": ["2026-09-30"],
    }
    assert evaluator.evaluate(rule, valid).status == RuleStatus.PASS

    missing = dict(valid)
    missing[f"{prefix}/ipsdo:RequestId"] = [None]
    assert evaluator.evaluate(rule, missing).status == RuleStatus.FAIL


def test_req31_stakeholder_details():
    r = _rules(31)
    assert len(r) == 1
    rule = r[0]
    evaluator = StructuredRuleEvaluator()
    prefix = "ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkClaimDetails/ipcdo:StakeholderDetails"

    valid = {
        prefix: [None],
        f"{prefix}/csdo:UnifiedCountryCode": ["RU"],
        f"{prefix}/csdo:SubjectName": ["ООО Заинтересованное лицо"],
        f"{prefix}/csdo:SubjectBriefName": ["ООО ЗЛ"],
        f"{prefix}/ccdo:SubjectAddressDetails": [""],
    }
    assert evaluator.evaluate(rule, valid).status == RuleStatus.PASS

    missing = dict(valid)
    missing[f"{prefix}/csdo:SubjectBriefName"] = [None]
    assert evaluator.evaluate(rule, missing).status == RuleStatus.FAIL


def test_req32_argument_details():
    r = _rules(32)
    assert len(r) == 1
    rule = r[0]
    evaluator = StructuredRuleEvaluator()
    prefix = "ipcdo:TrademarkApplicationDetails/ipcdo:ArgumentDetails"

    valid = {
        prefix: [None],
        f"{prefix}/csdo:DescriptionText": ["Доводы заявителя"],
        f"{prefix}/csdo:EventDate": ["2026-09-30"],
    }
    assert evaluator.evaluate(rule, valid).status == RuleStatus.PASS

    missing = dict(valid)
    missing[f"{prefix}/csdo:DescriptionText"] = [None]
    assert evaluator.evaluate(rule, missing).status == RuleStatus.FAIL


def test_req33_and_req34_forbidden_elements():
    evaluator = StructuredRuleEvaluator()
    r33 = _rules(33)
    assert len(r33) == 4
    for rule in r33:
        assert rule["kind"] == "selection_cardinality"
        assert rule["min_occurs"] == 0
        assert rule["max_occurs"] == 0
        col = rule["selector"]["collection"]
        assert evaluator.evaluate(rule, {}).status == RuleStatus.PASS
        assert evaluator.evaluate(rule, {col: [None]}).status == RuleStatus.FAIL

    r34 = _rules(34)
    assert len(r34) == 1
    assert r34[0]["kind"] == "selection_cardinality"
    assert r34[0]["min_occurs"] == 0
    assert r34[0]["max_occurs"] == 0
    assert evaluator.evaluate(r34[0], {}).status == RuleStatus.PASS
    assert evaluator.evaluate(r34[0], {"ipcdo:RefusalDetails": [None]}).status == RuleStatus.FAIL


def test_req35_and_req36_resource_item_status_dates():
    evaluator = StructuredRuleEvaluator()
    r35 = _rules(35)[0]
    r36 = _rules(36)[0]
    prefix = "ccdo:ResourceItemStatusDetails"
    start_field = f"{prefix}/ccdo:ValidityPeriodDetails/csdo:StartDateTime"
    end_field = f"{prefix}/ccdo:ValidityPeriodDetails/csdo:EndDateTime"

    valid = {
        prefix: [None],
        f"{prefix}/ccdo:ValidityPeriodDetails": [None],
        start_field: ["2026-09-30T10:00:00+03:00"],
        end_field: [None],
    }
    assert evaluator.evaluate(r35, valid).status == RuleStatus.PASS
    assert evaluator.evaluate(r36, valid).status == RuleStatus.PASS

    # Missing StartDateTime -> r35 fails
    no_start = dict(valid, **{start_field: [None]})
    assert evaluator.evaluate(r35, no_start).status == RuleStatus.FAIL

    # Present EndDateTime -> r36 fails
    with_end = dict(valid, **{end_field: ["2026-10-01T10:00:00+03:00"]})
    assert evaluator.evaluate(r36, with_end).status == RuleStatus.FAIL


def test_req37_38_39_signature_details():
    evaluator = StructuredRuleEvaluator()
    r37_pres = [r for r in _raw()["structured_rules"] if r["rule_id"] == f"{MESSAGE}.T81.REQ.37.PRESENCE"][0]
    r37_branch = [r for r in _raw()["structured_rules"] if r["rule_id"] == f"{MESSAGE}.T81.REQ.37.BRANCH"][0]
    r38 = _rules(38)[0]
    r39 = _rules(39)[0]

    sig = "ipcdo:TrademarkApplicationDetails/ipcdo:SignatureDetails"
    officer = f"{sig}/ipcdo:OfficerDetails"
    fullname = f"{sig}/ccdo:FullNameDetails"

    # Branch 1: OfficerDetails present, FullNameDetails absent
    vals_officer = {
        sig: [None],
        officer: [None],
        fullname: [None],
        f"{officer}/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
        f"{officer}/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
        f"{officer}/csdo:PositionName": ["Эксперт"],
        f"{officer}/ccdo:CommunicationDetails": [None],
    }
    assert evaluator.evaluate(r37_pres, vals_officer).status == RuleStatus.PASS
    assert evaluator.evaluate(r37_branch, vals_officer).status == RuleStatus.PASS
    assert evaluator.evaluate(r38, vals_officer).status == RuleStatus.PASS
    assert evaluator.evaluate(r39, vals_officer).status == RuleStatus.PASS

    # Branch 2: FullNameDetails present, OfficerDetails absent
    vals_fullname = {
        sig: [None],
        fullname: [None],
        f"{fullname}/csdo:LastName": ["Петров"],
    }
    assert evaluator.evaluate(r37_pres, vals_fullname).status == RuleStatus.PASS
    assert evaluator.evaluate(r37_branch, vals_fullname).status == RuleStatus.PASS
    assert evaluator.evaluate(r38, vals_fullname).status == RuleStatus.PASS

    # Mutual exclusion violation: both present -> r37_branch and r38 fail
    vals_conflict = {
        sig: [None],
        officer: [""],
        fullname: [""],
    }
    assert evaluator.evaluate(r37_branch, vals_conflict).status == RuleStatus.FAIL
    assert evaluator.evaluate(r38, vals_conflict).status == RuleStatus.FAIL

    # Officer missing required fields -> r39 fails
    vals_officer_bad = dict(vals_officer, **{f"{officer}/csdo:PositionName": [None]})
    assert evaluator.evaluate(r39, vals_officer_bad).status == RuleStatus.FAIL

    # Officer with communication details -> r39 fails
    vals_officer_comm = dict(vals_officer, **{f"{officer}/ccdo:CommunicationDetails": [""]})
    assert evaluator.evaluate(r39, vals_officer_comm).status == RuleStatus.FAIL
