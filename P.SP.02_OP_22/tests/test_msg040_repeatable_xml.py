from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.040"
APP = "ipcdo:TrademarkApplicationDetails"
SIGNATURE = f"{APP}/ipcdo:SignatureDetails"


def rule(code, suffix=""):
    engine = EaeuXmlEngine.load_process(PACKAGE)
    rule_id = f"{MESSAGE}.T58.REQ.{code}{suffix}"
    return next(item for item in engine.rules[MESSAGE].structured_rules if item["rule_id"] == rule_id)


def test_req1_exactly_one_application():
    evaluator = StructuredRuleEvaluator()
    r = rule(1)
    assert evaluator.evaluate(r, {APP: []}).status is RuleStatus.FAIL
    assert evaluator.evaluate(r, {APP: [{}]}).status is RuleStatus.PASS
    assert evaluator.evaluate(r, {APP: [{}, {}]}).status is RuleStatus.FAIL


def test_status_is_scoped_to_direct_application_owner():
    r = rule(5)
    evaluator = StructuredRuleEvaluator()
    valid = {APP: [{}], f"{APP}/ipcdo:IPEntityStatusDetails": [{}], f"{APP}/ipcdo:IPEntityStatusDetails/csdo:StatusCode": "30"}
    assert evaluator.evaluate(r, valid).status is RuleStatus.PASS
    assert evaluator.evaluate(r, {APP: [{}]}).status is RuleStatus.FAIL
    wrong = dict(valid, **{f"{APP}/ipcdo:IPEntityStatusDetails/csdo:StatusCode": "21"})
    assert evaluator.evaluate(r, wrong).status is RuleStatus.FAIL
    listed = dict(valid, **{f"{APP}/ipcdo:IPEntityStatusDetails/csdo:StatusCode/@codeListId": "status"})
    assert evaluator.evaluate(r, listed).status is RuleStatus.FAIL


def test_signature_branches_and_officers_stay_with_their_signature():
    evaluator = StructuredRuleEvaluator()
    r30 = rule(30, ".BRANCH")
    r31 = rule(31)
    r32 = rule(32)
    conflicting = {SIGNATURE: [{}, {}], f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, None], f"{SIGNATURE}/ccdo:FullNameDetails": [None, {}]}
    assert evaluator.evaluate(r30, conflicting).status is RuleStatus.PASS
    assert evaluator.evaluate(r31, conflicting).status is RuleStatus.PASS
    same_parent_conflict = dict(conflicting, **{f"{SIGNATURE}/ccdo:FullNameDetails": [{}, None]})
    assert evaluator.evaluate(r30, same_parent_conflict).status is RuleStatus.FAIL
    officer = {SIGNATURE: [{}], f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, {}], f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["A", None], f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["B", "C"], f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["P", "P"]}
    assert evaluator.evaluate(r32, officer).status is RuleStatus.FAIL


def test_both_validity_dates_are_required_in_their_resource_owner():
    evaluator = StructuredRuleEvaluator()
    start, end = rule(33), rule(34)
    path = "ccdo:ResourceItemStatusDetails"
    valid = {path: [{}], f"{path}/ccdo:ValidityPeriodDetails/csdo:StartDateTime": "2026-01-01T00:00:00+03:00", f"{path}/ccdo:ValidityPeriodDetails/csdo:EndDateTime": "2026-01-02T00:00:00+03:00"}
    assert evaluator.evaluate(start, valid).status is RuleStatus.PASS
    assert evaluator.evaluate(end, valid).status is RuleStatus.PASS
    assert evaluator.evaluate(start, {path: [{}], f"{path}/ccdo:ValidityPeriodDetails/csdo:EndDateTime": "x"}).status is RuleStatus.FAIL
    assert evaluator.evaluate(end, {path: [{}], f"{path}/ccdo:ValidityPeriodDetails/csdo:StartDateTime": "x"}).status is RuleStatus.FAIL
    wrong_owner = {path: [{}], "ipcdo:TrademarkApplicationDetails/csdo:StartDateTime": "x", "ipcdo:TrademarkApplicationDetails/csdo:EndDateTime": "x"}
    assert evaluator.evaluate(start, wrong_owner).status is RuleStatus.FAIL
    assert evaluator.evaluate(end, wrong_owner).status is RuleStatus.FAIL


def test_req27_requires_conditional_fields_in_the_same_trademark_parent():
    evaluator = StructuredRuleEvaluator()
    trademark = f"{APP}/ipcdo:TrademarkDetails"
    values = {
        trademark: [{}, {}],
        f"{trademark}/ipsdo:TrademarkKindCode": ["110", "140"],
        f"{trademark}/ipsdo:TrademarkPicture": [None, "picture"],
        f"{trademark}/ipsdo:TrademarkColourName": [None, "colour"],
    }
    assert evaluator.evaluate(rule(27), values).status is RuleStatus.PASS
    values[f"{trademark}/ipsdo:TrademarkPicture"] = ["picture", None]
    assert evaluator.evaluate(rule(27), values).status is RuleStatus.FAIL
