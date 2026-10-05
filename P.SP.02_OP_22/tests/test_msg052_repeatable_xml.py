from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.052"
R = "ipcdo:UnifiedRegisterRecordsDetails"
STATUS = f"{R}/ipcdo:IPEntityStatusDetails"
CANCEL = f"{R}/ipcdo:RegistrationCancellationDetails"
COMPLAINT = f"{CANCEL}/ipcdo:ComplaintInvalidateProtectionTrademarkDetails"
SIG = f"{R}/ipcdo:SignatureDetails"
OFFICER = f"{SIG}/ipcdo:OfficerDetails"
CANCEL_LITERAL = "Решение об аннулировании регистрации товарного знака, знака обслуживания Евразийского экономического союза"
NEW_LITERAL = "решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении всех заявленных товаров и (или) услуг"

def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)

def _rules(code, suffix=""):
    rid = f"{MESSAGE}.T70.REQ.{code}{suffix}"
    return [r for r in _engine().rules[MESSAGE].structured_rules if r["rule_id"] == rid or r["rule_id"].startswith(rid + ".")]

def _statuses(code, values, suffix=""):
    ev = StructuredRuleEvaluator()
    rules = _rules(code, suffix)
    assert rules
    return [ev.evaluate(r, values).status for r in rules]

def _pass(code, values, suffix=""):
    assert all(s is RuleStatus.PASS for s in _statuses(code, values, suffix))

def _fail(code, values, suffix=""):
    assert RuleStatus.FAIL in _statuses(code, values, suffix)

def role_values(statuses):
    n = len(statuses)
    return {
        R: [{} for _ in statuses],
        f"{STATUS}/csdo:StatusCode": list(statuses),
        f"{STATUS}/csdo:EventDate": ["2026-09-30"] * n,
        f"{R}/ipsdo:TrademarkId": [f"TM-{i}" for i in range(n)],
    }

def test_req1_cardinality_0_1_2_3():
    _fail(1, {R: []})
    _pass(1, {R: [{}]})
    _pass(1, {R: [{}, {}]})
    _fail(1, {R: [{}, {}, {}]})

def test_req2_status04_exactly_one_and_details():
    _fail(2, role_values(["01"]))
    _pass(2, role_values(["04"]))
    _pass(2, role_values(["01", "04"]))
    _pass(2, role_values(["04", "01"]))
    _fail(2, role_values(["04", "04"]))
    missing_date = role_values(["01", "04"])
    missing_date[f"{STATUS}/csdo:EventDate"] = ["2026-09-30", None]
    _fail(2, missing_date, ".DETAILS")
    with_list = role_values(["04"])
    with_list[f"{STATUS}/csdo:StatusCode/@codeListId"] = ["LIST"]
    _fail(2, with_list, ".DETAILS")

def test_req4_new_registration_role_is_order_independent():
    for statuses in (["01", "04"], ["04", "01"]):
        values = role_values(statuses)
        _pass(4, values)
    bad = role_values(["04", "01"])
    bad[f"{STATUS}/csdo:EventDate"] = ["2026-09-30", None]
    _fail(4, bad)

def test_req5_and_req20_trademark_id_stay_with_role_owner():
    values = role_values(["04", "01"])
    _pass(5, values)
    _pass(20, values)
    bad_cancel = dict(values)
    bad_cancel[f"{R}/ipsdo:TrademarkId"] = [None, "NEW"]
    _fail(5, bad_cancel)
    _pass(20, bad_cancel)
    bad_new = dict(values)
    bad_new[f"{R}/ipsdo:TrademarkId"] = ["OLD", None]
    _pass(5, bad_new)
    _fail(20, bad_new)

def test_req23_cancellation_details_do_not_leak_between_records():
    values = role_values(["04", "01"])
    values[CANCEL] = [{}, None]
    values[COMPLAINT] = [{}, None]
    values[f"{COMPLAINT}/ipsdo:CancellationRegistrationTrademarkCode"] = ["A", None]
    values[f"{COMPLAINT}/ipsdo:SolutionCancellationRegistrationTrademarkCode"] = ["B", None]
    _pass(23, values)
    leaked = role_values(["04", "01"])
    leaked[CANCEL] = [None, {}]
    leaked[COMPLAINT] = [None, {}]
    leaked[f"{COMPLAINT}/ipsdo:CancellationRegistrationTrademarkCode"] = [None, "A"]
    leaked[f"{COMPLAINT}/ipsdo:SolutionCancellationRegistrationTrademarkCode"] = [None, "B"]
    _fail(23, leaked)

def test_req25_28_document_kind_rules_are_role_scoped_and_exact():
    values = role_values(["04", "01"])
    values[f"{R}/ipsdo:IPDocKindCode"] = ["CANCEL-CODE", "NEW-CODE"]
    _pass(25, values)
    _pass(27, values)
    values_no_code = role_values(["04", "01"])
    values_no_code[f"{R}/ipsdo:IPDocKindName"] = [CANCEL_LITERAL, NEW_LITERAL]
    _pass(26, values_no_code)
    _pass(28, values_no_code)
    wrong_case = dict(values_no_code)
    wrong_case[f"{R}/ipsdo:IPDocKindName"] = [CANCEL_LITERAL, NEW_LITERAL[0].upper() + NEW_LITERAL[1:]]
    _fail(28, wrong_case)
    cross_role_name = dict(values_no_code)
    cross_role_name[f"{R}/ipsdo:IPDocKindName"] = [NEW_LITERAL, CANCEL_LITERAL]
    _fail(26, cross_role_name)
    _fail(28, cross_role_name)

def test_req29_31_signatures_preserve_same_parent_semantics():
    base = role_values(["04", "01"])
    base[SIG] = [{}, {}]
    base[OFFICER] = [{}, None]
    base[f"{OFFICER}/ccdo:FullNameDetails/csdo:LastName"] = ["Иванов", None]
    base[f"{OFFICER}/ccdo:FullNameDetails/csdo:FirstName"] = ["Иван", None]
    base[f"{OFFICER}/csdo:PositionName"] = ["Эксперт", None]
    base[f"{SIG}/ccdo:FullNameDetails"] = [None, {}]
    _pass(29, base)
    _pass(30, base)
    _pass(31, base)
    both = dict(base)
    both[f"{SIG}/ccdo:FullNameDetails"] = [{}, {}]
    _fail(29, both, ".BRANCH")
    missing_position = dict(base)
    missing_position[f"{OFFICER}/csdo:PositionName"] = [None, None]
    _fail(31, missing_position)

def test_inherited_req16_and_req17_repeatable_goods_alignment():
    goods = f"{R}/ipcdo:GoodsBaseDetails"
    valid = {
        goods: [{}, {}],
        f"{goods}/ipsdo:GoodsClassCode": ["09", "42"],
        f"{goods}/ipsdo:GoodsClassName": ["A", "B"],
        f"{goods}/ipsdo:GoodsName": ["a", "b"],
        f"{goods}/ipsdo:TrademarkDecisionIndicator": ["1", "1"],
        f"{goods}/ipsdo:TrademarkApplicationId": ["APP", "APP"],
    }
    _pass(16, valid)
    _pass(17, valid)
    bad = dict(valid)
    bad[f"{goods}/ipsdo:GoodsClassCode"] = ["09", None]
    _fail(16, bad)
    forbidden = dict(valid)
    forbidden[f"{goods}/ipsdo:TrademarkId"] = [None, "TM"]
    _fail(17, forbidden)
