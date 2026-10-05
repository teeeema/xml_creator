import json
from pathlib import Path

from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.054"
AUTHORITY = "ipcdo:PatentAuthorityDetails"
PAYMENT_AUTHORITY = "ipcdo:IPPaymentDetails/ipcdo:PatentAuthorityDetails"


def _rules(code):
    data = json.loads(
        (PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8")
    )
    prefix = f"{MESSAGE}.T72.REQ.{code}"
    return [r for r in data["structured_rules"] if r["rule_id"] == prefix or r["rule_id"].startswith(prefix + ".")]


def _statuses(code, values):
    evaluator = StructuredRuleEvaluator()
    rules = _rules(code)
    assert rules
    return [evaluator.evaluate(rule, values).status for rule in rules]


def _pass(code, values):
    assert all(status is RuleStatus.PASS for status in _statuses(code, values))


def _fail(code, values):
    assert RuleStatus.FAIL in _statuses(code, values)


def _authority_values(kind="2"):
    return {
        AUTHORITY: [{}],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": ["RU"],
        f"{AUTHORITY}/csdo:AuthorityName": ["Роспатент"],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails": [{}],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": [kind],
    }


def test_req1_req2_req3_direct_patent_authority_scope():
    values = _authority_values()
    _pass(1, values)
    _pass(2, values)
    _pass(3, values)

    no_country = dict(values)
    del no_country[f"{AUTHORITY}/csdo:UnifiedCountryCode"]
    _fail(1, no_country)

    no_name = dict(values)
    del no_name[f"{AUTHORITY}/csdo:AuthorityName"]
    _fail(2, no_name)

    no_address = dict(values)
    del no_address[f"{AUTHORITY}/ccdo:SubjectAddressDetails"]
    del no_address[f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode"]
    _fail(3, no_address)

    _fail(3, _authority_values(kind="1"))


def test_nested_payment_authority_and_wrong_qname_do_not_satisfy_direct_owner():
    values = _authority_values()
    del values[f"{AUTHORITY}/csdo:UnifiedCountryCode"]
    values[f"{PAYMENT_AUTHORITY}/csdo:UnifiedCountryCode"] = ["RU"]
    _fail(1, values)

    wrong_qname = _authority_values()
    del wrong_qname[f"{AUTHORITY}/csdo:UnifiedCountryCode"]
    wrong_qname[f"{AUTHORITY}/wrong:UnifiedCountryCode"] = ["RU"]
    _fail(1, wrong_qname)


def test_req4_req5_legal_action_local_branches_and_four_value_membership():
    header = {"ccdo:EDocHeader": [{}]}
    approved_name = _rules(5)[1]["assertions"][0]["right_value"][0]

    code_branch = {**header, "ipsdo:IPLegalActionKindCode": "external-code"}
    _pass(4, code_branch)
    _pass(5, code_branch)

    both = {**code_branch, "ipsdo:IPLegalActionKindName": approved_name}
    _fail(4, both)

    name_branch = {**header, "ipsdo:IPLegalActionKindName": approved_name}
    _pass(5, name_branch)

    bad_name = {**header, "ipsdo:IPLegalActionKindName": "неразрешенное значение"}
    _fail(5, bad_name)

    _fail(5, header)


def test_req6_is_root_only_and_req7_forbids_exact_root_fields():
    _pass(6, {"ipsdo:TrademarkApplicationId": "APP-054"})
    _fail(6, {"ipcdo:IPPaymentDetails/ipsdo:TrademarkApplicationId": "APP-054"})

    base = {"ccdo:EDocHeader": [{}]}
    _pass(7, base)
    forbidden = [
        "ipsdo:ApellationOfOriginApplicationId",
        "csdo:DocId",
        "ipcdo:IPPaymentDetails",
        "ipsdo:DutyPaymentIndicator",
        "csdo:PaymentAmount",
    ]
    for field in forbidden:
        _fail(7, {**base, field: "present"})

    _pass(7, {**base, "ipcdo:IPPaymentDetails/csdo:DocId": "nested-only"})

