from copy import deepcopy
from pathlib import Path

import pytest

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
STRUCTURE = "R.IP.SP.02.002"
APP = "ipcdo:TrademarkApplicationDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
TMDESC = f"{TM}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
PARTY_ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
PARTY_COMM = f"{PARTY}/ccdo:CommunicationDetails"
PATENT = f"{APP}/ipcdo:PatentAuthorityDetails"
PATENT_ADDRESS = f"{PATENT}/ccdo:SubjectAddressDetails"
CORR_ADDRESS = f"{APP}/ipcdo:CorrespondenceAddressDetails/ccdo:SubjectAddressDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
DOC = f"{APP}/ipcdo:AccompanyingDocumentsDetails"

MESSAGES = ("P.SP.02.MSG.011", "P.SP.02.MSG.013", "P.SP.02.MSG.014")
TABLE = {"P.SP.02.MSG.011": "44", "P.SP.02.MSG.013": "46", "P.SP.02.MSG.014": "47"}
INHERITED = {"6", "7", "8", "9", "10", "11", "12", "14", "15", "21", "22", "23", "24", "25", "26", "28", "29"}
DIRECT = {
    "P.SP.02.MSG.011": {"1", "4", "5", "30", "31", "32"},
    "P.SP.02.MSG.013": {"1", "4", "5", "30", "31", "32"},
    "P.SP.02.MSG.014": {"1", "3", "31", "32"},
}
UNMAPPED = {
    "P.SP.02.MSG.011": {"2", "3", "13", "16", "17", "18", "19", "20", "27"},
    "P.SP.02.MSG.013": {"2", "3", "13", "16", "17", "18", "19", "20", "27"},
    "P.SP.02.MSG.014": {"2", "4", "5", "13", "16", "17", "18", "19", "20", "27", "30"},
}
PAIRS = {
    "110": "Словесный знак",
    "120": "Буквенный знак",
    "130": "Цифровой знак",
    "140": "Изобразительный знак",
    "150": "Объемный знак",
    "160": "Знак, представляющий собой цвет",
    "170": "Знак, представляющий собой сочетание цветов",
    "180": "Комбинированный знак",
}


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _rules(message):
    return _engine().rules[message].structured_rules


def _rules_for_code(message, code):
    direct_id = f"{message}.REQ.{code}"
    result = []
    for rule in _rules(message):
        if rule["rule_id"] == direct_id:
            result.append(rule)
            continue
        refs = rule.get("source_refs", [])
        if len(refs) == 2 and refs[1].get("item") == code:
            result.append(rule)
    return result


def _statuses(message, code, values):
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(rule, values).status for rule in _rules_for_code(message, code)]


def _base(message):
    status = "30" if message == "P.SP.02.MSG.013" else "02"
    indicator = "1" if message == "P.SP.02.MSG.011" else "0"
    values = {
        APP: [None],
        f"{APP}/ipsdo:TrademarkApplicationId": "APP-TEST",
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-24",
        STATUS: [None],
        f"{STATUS}/csdo:StatusCode": status,
        PATENT: [None],
        f"{PATENT}/csdo:UnifiedCountryCode": "RU",
        f"{PATENT}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PATENT}/csdo:AuthorityName": "Ведомство",
        PATENT_ADDRESS: [""],
        f"{PATENT_ADDRESS}/csdo:AddressKindCode": "2",
        f"{PATENT_ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{PATENT_ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PATENT_ADDRESS}/csdo:CityName": "Москва",
        f"{PATENT_ADDRESS}/csdo:StreetName": "Тестовая",
        f"{PATENT_ADDRESS}/csdo:BuildingNumberId": "1",
        PARTY: [None, None, None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["AP", "PA", "RE"],
        f"{PARTY}/csdo:UnifiedCountryCode": ["RU", "RU", "RU"],
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": ["ВОИС ST.3"] * 3,
        f"{PARTY}/ipsdo:IPSubjectName": ["Applicant", "Attorney", "Representative"],
        PARTY_ADDRESS: ["", "", ""],
        f"{PARTY_ADDRESS}/csdo:AddressKindCode": ["2", "2", "2"],
        f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode": ["RU", "RU", "RU"],
        f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode/@codeListId": ["ВОИС ST.3"] * 3,
        f"{PARTY_ADDRESS}/csdo:CityName": ["Москва"] * 3,
        f"{PARTY_ADDRESS}/csdo:StreetName": ["Тестовая"] * 3,
        f"{PARTY_ADDRESS}/csdo:BuildingNumberId": ["1", "2", "3"],
        PARTY_COMM: ["", "", ""],
        f"{PARTY_COMM}/csdo:CommunicationChannelCode": ["EM", "TE", "FX"],
        f"{PARTY_COMM}/csdo:CommunicationChannelId": ["a@test", "+1", "+2"],
        f"{PARTY}/ipsdo:PatentAttorneyId": [None, "PA-1", None],
        CORR_ADDRESS: [None],
        f"{CORR_ADDRESS}/csdo:AddressKindCode": "3",
        f"{CORR_ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{CORR_ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{CORR_ADDRESS}/csdo:CityName": "Москва",
        f"{CORR_ADDRESS}/csdo:StreetName": "Почтовая",
        f"{CORR_ADDRESS}/csdo:BuildingNumberId": "10",
        TM: [None],
        TMDESC: [None],
        f"{TMDESC}/csdo:DescriptionText": "Описание",
        f"{TM}/ipsdo:TrademarkKindCode": "110",
        f"{TM}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TM}/ipsdo:CollectiveMarkIndicator": indicator,
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "01",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        RESOURCE: [None],
        VALIDITY: [None],
    }
    if message == "P.SP.02.MSG.011":
        values[f"{VALIDITY}/csdo:StartDateTime"] = "2026-09-24T12:00:00+03:00"
    if message == "P.SP.02.MSG.013":
        values[f"{VALIDITY}/csdo:EndDateTime"] = "2026-09-24T13:00:00+03:00"
        values[DOC] = [None]
        values[f"{DOC}/csdo:DocId"] = "D-1"
        values[f"{DOC}/csdo:DocCreationDate"] = "2026-09-24"
        values[f"{DOC}/csdo:DescriptionText"] = "Описание"
        values[f"{DOC}/csdo:PageQuantity"] = "1"
    if message == "P.SP.02.MSG.014":
        values[f"{STATUS}/csdo:EventDate"] = "2026-09-24"
        values[f"{STATUS}/csdo:DocId"] = "D-14"
        values[f"{STATUS}/ipsdo:IPDocReceiptDate"] = "2026-09-24"
        values[f"{STATUS}/csdo:DescriptionText"] = "Изменение"
    return values


@pytest.mark.parametrize("message", MESSAGES)
def test_mapping_inventory_and_dual_provenance(message):
    rules = _rules(message)
    assert rules and all(rule.get("applies_to_structure") == STRUCTURE for rule in rules)
    inherited = {rule["source_refs"][1]["item"] for rule in rules if len(rule.get("source_refs", [])) == 2}
    direct = {rule["rule_id"].rsplit(".", 1)[-1] for rule in rules if rule["rule_id"].startswith(f"{message}.REQ.")}
    assert inherited == INHERITED
    assert direct == DIRECT[message]
    assert UNMAPPED[message].isdisjoint(inherited | direct)
    range_id = f"22OP-RULE-{message}-T{TABLE[message]}-6-29"
    for code in INHERITED:
        for rule in _rules_for_code(message, code):
            assert [ref["source_id"] for ref in rule["source_refs"]] == [range_id, f"22OP-RULE-P.SP.02.MSG.001-{code}"]
            assert rule.get("mapping_status") == "INHERITED"


@pytest.mark.parametrize("message", MESSAGES)
def test_all_safe_rules_pass_valid_values(message):
    evaluations = StructuredRuleEvaluator().evaluate_all(_rules(message), _base(message))
    failed = [(item.rule_id, item.status.value) for item in evaluations if item.status is not RuleStatus.PASS]
    assert evaluations and not failed, failed


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("code,name", list(PAIRS.items())[:2])
def test_req26_exact_pairing_passes_and_wrong_normative_name_fails(message, code, name):
    valid = _base(message)
    valid[f"{TM}/ipsdo:TrademarkKindCode"] = code
    valid[f"{TM}/ipsdo:TrademarkKindName"] = name
    assert all(status is RuleStatus.PASS for status in _statuses(message, "26", valid))
    invalid = deepcopy(valid)
    invalid[f"{TM}/ipsdo:TrademarkKindName"] = "Комбинированный знак" if name != "Комбинированный знак" else "Словесный знак"
    assert RuleStatus.FAIL in _statuses(message, "26", invalid)


def test_req26_has_all_eight_exact_conditional_pairs():
    rules = _rules_for_code("P.SP.02.MSG.011", "26")
    conditional = [rule for rule in rules if rule["kind"] == "conditional_fixed_value"]
    assert len(conditional) == 8
    assert {
        (rule["condition"]["value"], rule["value"])
        for rule in conditional
    } == set(PAIRS.items())


def test_msg013_req30_is_partial_and_does_not_invent_code_name_one_of():
    rules = _rules_for_code("P.SP.02.MSG.013", "30")
    assert len(rules) == 1 and rules[0]["mapping_status"] == "PARTIAL"
    assertions = rules[0]["assertions"]
    assert {a["target"]["field"] for a in assertions} == {
        "csdo:DocId", "csdo:DocCreationDate", "csdo:DescriptionText", "csdo:PageQuantity"
    }


def test_message_isolation_direct_semantics():
    msg011 = _base("P.SP.02.MSG.011")
    assert all(s is RuleStatus.PASS for s in _statuses("P.SP.02.MSG.011", "5", msg011))
    assert RuleStatus.FAIL in _statuses("P.SP.02.MSG.013", "5", msg011)
    assert _statuses("P.SP.02.MSG.011", "30", msg011) == [RuleStatus.PASS]

    msg013 = _base("P.SP.02.MSG.013")
    assert all(s is RuleStatus.PASS for s in _statuses("P.SP.02.MSG.013", "5", msg013))
    assert RuleStatus.FAIL in _statuses("P.SP.02.MSG.011", "5", msg013)
    assert _statuses("P.SP.02.MSG.013", "32", msg013) == [RuleStatus.PASS]
    assert _statuses("P.SP.02.MSG.014", "3", msg013) == [RuleStatus.FAIL]

    msg014 = _base("P.SP.02.MSG.014")
    assert all(s is RuleStatus.PASS for s in _statuses("P.SP.02.MSG.014", "31", msg014))
    assert _statuses("P.SP.02.MSG.014", "3", msg014) == [RuleStatus.PASS]
    missing = deepcopy(msg014)
    missing.pop(f"{STATUS}/csdo:DocId")
    assert _statuses("P.SP.02.MSG.011", "5", missing) == [RuleStatus.PASS, RuleStatus.PASS]
    assert RuleStatus.FAIL in _statuses("P.SP.02.MSG.014", "32", missing)


def test_msg011_isolated_from_existing_msg010_indicator():
    values = _base("P.SP.02.MSG.011")
    assert _statuses("P.SP.02.MSG.011", "30", values) == [RuleStatus.PASS]
    assert _statuses("P.SP.02.MSG.010", "30", values) == [RuleStatus.FAIL]


def test_msg013_has_no_direct_start_datetime_rule():
    assert not any(
        rule["rule_id"] == "P.SP.02.MSG.013.REQ.32"
        and "StartDateTime" in str(rule)
        for rule in _rules("P.SP.02.MSG.013")
    )
