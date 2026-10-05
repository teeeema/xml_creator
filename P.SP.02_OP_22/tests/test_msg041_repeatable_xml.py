from pathlib import Path

import pytest

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.041"
APP = "ipcdo:TrademarkApplicationDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
SIGNATURE = f"{APP}/ipcdo:SignatureDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"

def rule(code, suffix=""):
    engine = EaeuXmlEngine.load_process(PACKAGE)
    rule_id = f"{MESSAGE}.T59.REQ.{code}{suffix}"
    return next(r for r in engine.rules[MESSAGE].structured_rules if r["rule_id"] == rule_id)

def test_req1_zero_one_two_cardinality():
    ev = StructuredRuleEvaluator()
    r = rule(1)
    assert ev.evaluate(r, {APP: []}).status is RuleStatus.FAIL
    assert ev.evaluate(r, {APP: [{}]}).status is RuleStatus.PASS
    assert ev.evaluate(r, {APP: [{},{}]}).status is RuleStatus.FAIL

def test_req5_direct_status_owner_value_and_attribute():
    ev = StructuredRuleEvaluator()
    r = rule(5)
    status = f"{APP}/ipcdo:IPEntityStatusDetails"
    valid = {APP:[{}], status:[{}], f"{status}/csdo:StatusCode":"02"}
    assert ev.evaluate(r, valid).status is RuleStatus.PASS
    assert ev.evaluate(r, {APP:[{}]}).status is RuleStatus.FAIL
    assert ev.evaluate(r, dict(valid, **{f"{status}/csdo:StatusCode":"01"})).status is RuleStatus.FAIL
    assert ev.evaluate(r, dict(valid, **{f"{status}/csdo:StatusCode/@codeListId":"x"})).status is RuleStatus.FAIL
    wrong_owner = {APP:[{}], f"{APP}/csdo:StatusCode":"02"}
    assert ev.evaluate(r, wrong_owner).status is RuleStatus.FAIL

def test_req27_same_parent_prevents_cross_parent_satisfaction():
    ev = StructuredRuleEvaluator()
    values = {
        TM:[{},{}],
        f"{TM}/ipsdo:TrademarkKindCode":["140","110"],
        f"{TM}/ipsdo:TrademarkPicture":[None,"picture"],
        f"{TM}/ipsdo:TrademarkColourName":[None,"red"],
    }
    assert ev.evaluate(rule(27), values).status is RuleStatus.FAIL
    values[f"{TM}/ipsdo:TrademarkPicture"] = ["picture",None]
    values[f"{TM}/ipsdo:TrademarkColourName"] = ["red",None]
    assert ev.evaluate(rule(27), values).status is RuleStatus.PASS

@pytest.mark.parametrize("bad_index", [None,0,1])
def test_req30_repeatable_trademark_owner_matrix(bad_index):
    ev = StructuredRuleEvaluator()
    vals = {TM:[{},{}], f"{TM}/ipsdo:CollectiveMarkIndicator":["0","0"]}
    if bad_index is not None:
        vals[f"{TM}/ipsdo:CollectiveMarkIndicator"][bad_index] = "1"
    expected = RuleStatus.PASS if bad_index is None else RuleStatus.FAIL
    assert ev.evaluate(rule(30), vals).status is expected

def test_req30_wrong_owner_indicator_does_not_satisfy():
    ev = StructuredRuleEvaluator()
    vals = {TM:[{}], f"{APP}/ipsdo:CollectiveMarkIndicator":"0"}
    assert ev.evaluate(rule(30), vals).status is RuleStatus.FAIL

def test_req31_start_required_and_wrong_owner_rejected():
    ev = StructuredRuleEvaluator()
    start = rule(31)
    valid = {RESOURCE:[{}], f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:StartDateTime":"2026-09-30T12:00:00+03:00"}
    assert ev.evaluate(start, valid).status is RuleStatus.PASS
    assert ev.evaluate(start, {RESOURCE:[{}]}).status is RuleStatus.FAIL
    wrong = {RESOURCE:[{}], f"{RESOURCE}/csdo:StartDateTime":"2026-09-30T12:00:00+03:00"}
    assert ev.evaluate(start, wrong).status is RuleStatus.FAIL

def test_req32_end_forbidden_under_governed_owner():
    ev = StructuredRuleEvaluator()
    end = rule(32)
    assert ev.evaluate(end, {RESOURCE:[{}]}).status is RuleStatus.PASS
    bad = {RESOURCE:[{}], f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:EndDateTime":"2026-10-01T12:00:00+03:00"}
    assert ev.evaluate(end, bad).status is RuleStatus.FAIL

def test_req33_34_same_signature_mutual_exclusion():
    ev = StructuredRuleEvaluator()
    r33 = rule(33, ".BRANCH")
    r34 = rule(34)
    split = {
        SIGNATURE:[{},{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails":[{},None],
        f"{SIGNATURE}/ccdo:FullNameDetails":[None,{}],
    }
    assert ev.evaluate(r33, split).status is RuleStatus.PASS
    assert ev.evaluate(r34, split).status is RuleStatus.PASS
    conflict = dict(split, **{f"{SIGNATURE}/ccdo:FullNameDetails":[{},None]})
    assert ev.evaluate(r33, conflict).status is RuleStatus.FAIL

@pytest.mark.parametrize("missing", ["last","first","position","communication"])
def test_req35_officer_fields_and_forbidden_communication(missing):
    ev = StructuredRuleEvaluator()
    officer = f"{SIGNATURE}/ipcdo:OfficerDetails"
    vals = {
        SIGNATURE:[{}], officer:[{}],
        f"{officer}/ccdo:FullNameDetails/csdo:LastName":"A",
        f"{officer}/ccdo:FullNameDetails/csdo:FirstName":"B",
        f"{officer}/csdo:PositionName":"P",
    }
    if missing == "last":
        vals.pop(f"{officer}/ccdo:FullNameDetails/csdo:LastName")
    elif missing == "first":
        vals.pop(f"{officer}/ccdo:FullNameDetails/csdo:FirstName")
    elif missing == "position":
        vals.pop(f"{officer}/csdo:PositionName")
    else:
        vals[f"{officer}/ccdo:CommunicationDetails"] = [{}]
    assert ev.evaluate(rule(35), vals).status is RuleStatus.FAIL
