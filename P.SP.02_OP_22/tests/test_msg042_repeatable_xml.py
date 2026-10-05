from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.042"
APP = "ipcdo:TrademarkApplicationDetails"
SIGNATURE = f"{APP}/ipcdo:SignatureDetails"
TRADEMARK = f"{APP}/ipcdo:TrademarkDetails"


def rule(code, suffix=""):
    engine = EaeuXmlEngine.load_process(PACKAGE)
    rule_id = f"{MESSAGE}.T60.REQ.{code}{suffix}"
    return next(item for item in engine.rules[MESSAGE].structured_rules if item["rule_id"] == rule_id)


def test_req1_exactly_one_application():
    evaluator = StructuredRuleEvaluator()
    r = rule(1)
    assert evaluator.evaluate(r, {APP: []}).status is RuleStatus.FAIL
    assert evaluator.evaluate(r, {APP: [{}]}).status is RuleStatus.PASS
    assert evaluator.evaluate(r, {APP: [{}, {}]}).status is RuleStatus.FAIL


def test_req4_application_id_presence():
    evaluator = StructuredRuleEvaluator()
    r = rule(4)
    assert evaluator.evaluate(r, {APP: [{}]}).status is RuleStatus.FAIL
    assert evaluator.evaluate(r, {APP: [{}], f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000042"}).status is RuleStatus.PASS


def test_req5_status_is_scoped_to_direct_application_owner():
    r = rule(5)
    evaluator = StructuredRuleEvaluator()
    valid = {
        APP: [{}],
        f"{APP}/ipcdo:IPEntityStatusDetails": [{}],
        f"{APP}/ipcdo:IPEntityStatusDetails/csdo:StatusCode": "02",
    }
    assert evaluator.evaluate(r, valid).status is RuleStatus.PASS
    assert evaluator.evaluate(r, {APP: [{}]}).status is RuleStatus.FAIL
    wrong = dict(valid, **{f"{APP}/ipcdo:IPEntityStatusDetails/csdo:StatusCode": "21"})
    assert evaluator.evaluate(r, wrong).status is RuleStatus.FAIL
    wrong_30 = dict(valid, **{f"{APP}/ipcdo:IPEntityStatusDetails/csdo:StatusCode": "30"})
    assert evaluator.evaluate(r, wrong_30).status is RuleStatus.FAIL
    listed = dict(valid, **{f"{APP}/ipcdo:IPEntityStatusDetails/csdo:StatusCode/@codeListId": "status"})
    assert evaluator.evaluate(r, listed).status is RuleStatus.FAIL
    # Wrong owner status cannot satisfy REQ5
    wrong_owner = {
        APP: [{}],
        "other:IPEntityStatusDetails": [{}],
        "other:IPEntityStatusDetails/csdo:StatusCode": "02",
    }
    assert evaluator.evaluate(r, wrong_owner).status is RuleStatus.FAIL


def test_req30_collective_mark_indicator_equals_one():
    evaluator = StructuredRuleEvaluator()
    r = rule(30)
    # Exact value "1" -> PASS
    valid = {TRADEMARK: [{}], f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "1"}
    assert evaluator.evaluate(r, valid).status is RuleStatus.PASS

    # Value "0" (as used in MSG041) -> FAIL (critical isolation)
    msg041_val = {TRADEMARK: [{}], f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "0"}
    assert evaluator.evaluate(r, msg041_val).status is RuleStatus.FAIL

    # Other values -> FAIL
    other_val = {TRADEMARK: [{}], f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "2"}
    assert evaluator.evaluate(r, other_val).status is RuleStatus.FAIL

    # Wrong owner indicator cannot satisfy REQ30
    wrong_owner = {
        TRADEMARK: [{}],
        "other:TrademarkDetails/ipsdo:CollectiveMarkIndicator": "1",
    }
    assert evaluator.evaluate(r, wrong_owner).status is RuleStatus.FAIL


def test_validity_dates_req31_and_req32():
    evaluator = StructuredRuleEvaluator()
    start_rule = rule(31)
    end_rule = rule(32)
    path = "ccdo:ResourceItemStatusDetails"

    # StartDateTime present, EndDateTime absent -> both PASS
    valid = {
        path: [{}],
        f"{path}/ccdo:ValidityPeriodDetails/csdo:StartDateTime": "2026-09-30T14:00:00+03:00",
    }
    assert evaluator.evaluate(start_rule, valid).status is RuleStatus.PASS
    assert evaluator.evaluate(end_rule, valid).status is RuleStatus.PASS

    # Missing StartDateTime -> REQ31 FAIL
    missing_start = {path: [{}]}
    assert evaluator.evaluate(start_rule, missing_start).status is RuleStatus.FAIL

    # Wrong owner StartDateTime -> REQ31 FAIL
    wrong_owner_start = {
        path: [{}],
        "other:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime": "2026-09-30T14:00:00+03:00",
    }
    assert evaluator.evaluate(start_rule, wrong_owner_start).status is RuleStatus.FAIL

    # EndDateTime present in governed owner -> REQ32 FAIL
    with_end = dict(valid, **{f"{path}/ccdo:ValidityPeriodDetails/csdo:EndDateTime": "2026-10-01T14:00:00+03:00"})
    assert evaluator.evaluate(end_rule, with_end).status is RuleStatus.FAIL


def test_req33_35_signature_branches_and_officers_same_parent():
    evaluator = StructuredRuleEvaluator()
    r33_pres = rule(33, ".PRESENCE")
    r33_branch = rule(33, ".BRANCH")
    r34 = rule(34)
    r35 = rule(35)

    # 0 signatures -> FAIL
    assert evaluator.evaluate(r33_pres, {SIGNATURE: []}).status is RuleStatus.FAIL

    # Distinct signatures: one with OfficerDetails, one with FullNameDetails -> PASS
    separate = {
        SIGNATURE: [{}, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, None],
        f"{SIGNATURE}/ccdo:FullNameDetails": [None, {}],
    }
    assert evaluator.evaluate(r33_pres, separate).status is RuleStatus.PASS
    assert evaluator.evaluate(r33_branch, separate).status is RuleStatus.PASS
    assert evaluator.evaluate(r34, separate).status is RuleStatus.PASS

    # Mutual exclusion violation within same signature -> FAIL
    same_parent_conflict = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ccdo:FullNameDetails": [{}],
    }
    assert evaluator.evaluate(r33_branch, same_parent_conflict).status is RuleStatus.FAIL
    assert evaluator.evaluate(r34, same_parent_conflict).status is RuleStatus.FAIL

    # OfficerDetails required fields (REQ 35)
    valid_officer = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Петров"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Петр"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
    }
    assert evaluator.evaluate(r35, valid_officer).status is RuleStatus.PASS

    # Missing LastName -> FAIL
    missing_last = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": [None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Петр"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
    }
    assert evaluator.evaluate(r35, missing_last).status is RuleStatus.FAIL

    # CommunicationDetails forbidden in OfficerDetails -> FAIL
    with_comm = dict(valid_officer, **{f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:CommunicationDetails": [{}]})
    assert evaluator.evaluate(r35, with_comm).status is RuleStatus.FAIL

    # Repeatable officers: one good, one bad -> FAIL
    mixed_officers = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["А", None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Б", "В"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["П", "П"],
    }
    assert evaluator.evaluate(r35, mixed_officers).status is RuleStatus.FAIL


def test_req27_requires_conditional_fields_in_same_trademark_parent():
    evaluator = StructuredRuleEvaluator()
    r27 = rule(27)

    # Valid: matching kind with picture and colour in the same TrademarkDetails
    values = {
        TRADEMARK: [{}, {}],
        f"{TRADEMARK}/ipsdo:TrademarkKindCode": ["110", "140"],
        f"{TRADEMARK}/ipsdo:TrademarkPicture": [None, "picture_data"],
        f"{TRADEMARK}/ipsdo:TrademarkColourName": [None, "красный"],
    }
    assert evaluator.evaluate(r27, values).status is RuleStatus.PASS

    # Missing picture when kind is 140 -> FAIL
    missing_pic = {
        TRADEMARK: [{}],
        f"{TRADEMARK}/ipsdo:TrademarkKindCode": ["140"],
        f"{TRADEMARK}/ipsdo:TrademarkColourName": ["красный"],
    }
    assert evaluator.evaluate(r27, missing_pic).status is RuleStatus.FAIL

    # Cross-parent mismatch: picture in parent 0, kind 140 in parent 1 -> FAIL
    cross_parent = {
        TRADEMARK: [{}, {}],
        f"{TRADEMARK}/ipsdo:TrademarkKindCode": ["110", "140"],
        f"{TRADEMARK}/ipsdo:TrademarkPicture": ["picture_data", None],
        f"{TRADEMARK}/ipsdo:TrademarkColourName": [None, "красный"],
    }
    assert evaluator.evaluate(r27, cross_parent).status is RuleStatus.FAIL


def test_inherited_table44_cardinalities_and_fields():
    evaluator = StructuredRuleEvaluator()

    # REQ 14: AP party cardinality 1..1
    r14 = rule(14)
    party = f"{APP}/ipcdo:IPPartyDetails"
    assert evaluator.evaluate(r14, {party: []}).status is RuleStatus.FAIL
    assert evaluator.evaluate(r14, {party: [{}], f"{party}/ipsdo:IPPartyKindCode": ["AP"]}).status is RuleStatus.PASS
    assert evaluator.evaluate(r14, {party: [{}, {}], f"{party}/ipsdo:IPPartyKindCode": ["AP", "AP"]}).status is RuleStatus.FAIL

    # REQ 25: TrademarkDetails cardinality 1..*
    r25_card = rule(25, ".CARDINALITY")
    assert evaluator.evaluate(r25_card, {TRADEMARK: []}).status is RuleStatus.FAIL
    assert evaluator.evaluate(r25_card, {TRADEMARK: [{}]}).status is RuleStatus.PASS
    assert evaluator.evaluate(r25_card, {TRADEMARK: [{}, {}]}).status is RuleStatus.PASS
