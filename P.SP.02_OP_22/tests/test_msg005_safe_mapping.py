from copy import deepcopy
from pathlib import Path

import pytest

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.005"
STRUCTURE = "R.IP.SP.02.002"
APP = "ipcdo:TrademarkApplicationDetails"
PATENT = f"{APP}/ipcdo:PatentAuthorityDetails"
PATENT_ADDRESS = f"{PATENT}/ccdo:SubjectAddressDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
PARTY_ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
PARTY_COMM = f"{PARTY}/ccdo:CommunicationDetails"
CORR_ADDRESS = f"{APP}/ipcdo:CorrespondenceAddressDetails/ccdo:SubjectAddressDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
TMDESC = f"{TM}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
CLAIM = f"{APP}/ipcdo:TrademarkClaimDetails"
STAKE = f"{CLAIM}/ipcdo:StakeholderDetails"
STAKE_ADDRESS = f"{STAKE}/ccdo:SubjectAddressDetails"
ARGUMENT = f"{APP}/ipcdo:ArgumentDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"

INHERITED_FULL = {"6", "7", "8", "9", "10", "11", "12", "14", "15", "21", "22", "23", "24", "25", "28", "29"}
INHERITED_PARTIAL = {"26"}
DIRECT_FULL = {"1", "5", "30", "31", "32", "34", "35", "36", "37"}
DIRECT_PARTIAL = {"4"}
INTENTIONALLY_UNMAPPED = {"2", "3", "13", "16", "17", "18", "19", "20", "27", "33"}


def _engine() -> EaeuXmlEngine:
    return EaeuXmlEngine.load_process(PACKAGE)


def _rules():
    return _engine().rules[MESSAGE].structured_rules


def _rules_for_code(code: str):
    direct_id = f"{MESSAGE}.REQ.{code}"
    result = []
    for rule in _rules():
        if rule["rule_id"] == direct_id:
            result.append(rule)
            continue
        refs = rule.get("source_refs", [])
        if len(refs) >= 2 and refs[1].get("item") == code:
            result.append(rule)
    return result


def _statuses(code: str, values: dict[str, object]) -> list[RuleStatus]:
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(rule, values).status for rule in _rules_for_code(code)]


def _base_values() -> dict[str, object]:
    return {
        APP: [None],
        f"{APP}/ipsdo:TrademarkApplicationId": "APP-005",
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-18",
        PATENT: [None],
        f"{PATENT}/csdo:UnifiedCountryCode": "RU",
        f"{PATENT}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PATENT}/csdo:AuthorityName": "Патентное ведомство",
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
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": ["ВОИС ST.3", "ВОИС ST.3", "ВОИС ST.3"],
        f"{PARTY}/ipsdo:IPSubjectName": ["Applicant", "Attorney", "Representative"],
        PARTY_ADDRESS: ["", "", ""],
        f"{PARTY_ADDRESS}/csdo:AddressKindCode": ["2", "2", "2"],
        f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode": ["RU", "RU", "RU"],
        f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode/@codeListId": ["ВОИС ST.3", "ВОИС ST.3", "ВОИС ST.3"],
        f"{PARTY_ADDRESS}/csdo:CityName": ["Москва", "Москва", "Москва"],
        f"{PARTY_ADDRESS}/csdo:StreetName": ["Тестовая", "Тестовая", "Тестовая"],
        f"{PARTY_ADDRESS}/csdo:BuildingNumberId": ["1", "2", "3"],
        PARTY_COMM: ["", "", ""],
        f"{PARTY_COMM}/csdo:CommunicationChannelCode": ["EM", "TE", "FX"],
        f"{PARTY_COMM}/csdo:CommunicationChannelId": ["ap@example.test", "+100000000", "+100000001"],
        f"{PARTY}/ipsdo:PatentAttorneyId": [None, "PA-1", None],
        CORR_ADDRESS: [""],
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
        f"{TM}/ipsdo:CollectiveMarkIndicator": "0",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "01",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        CLAIM: [None],
        STAKE: [""],
        f"{CLAIM}/ipsdo:RequestId": "REQ-005",
        f"{CLAIM}/ipsdo:RequestDate": "2026-09-18",
        f"{STAKE}/csdo:UnifiedCountryCode": "RU",
        f"{STAKE}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{STAKE}/csdo:SubjectName": "Заинтересованное лицо",
        f"{STAKE}/csdo:SubjectBriefName": "ЗЛ",
        STAKE_ADDRESS: [""],
        f"{STAKE_ADDRESS}/csdo:AddressKindCode": "2",
        f"{STAKE_ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{STAKE_ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{STAKE_ADDRESS}/csdo:CityName": "Москва",
        f"{STAKE_ADDRESS}/csdo:StreetName": "Тестовая",
        f"{STAKE_ADDRESS}/csdo:BuildingNumberId": "20",
        ARGUMENT: [""],
        f"{ARGUMENT}/csdo:DescriptionText": "Доводы заявителя",
        f"{ARGUMENT}/csdo:EventDate": "2026-09-18",
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-18T12:00:00+03:00",
    }


def test_mapping_scope_status_and_intentionally_unmapped_requirements() -> None:
    rules = _rules()
    assert len(rules) == 33
    assert all(rule.get("applies_to_structure") == STRUCTURE for rule in rules)

    inherited_items = {
        rule["source_refs"][1]["item"]
        for rule in rules
        if len(rule.get("source_refs", [])) == 2
    }
    direct_codes = {
        rule["rule_id"].rsplit(".", 1)[-1]
        for rule in rules
        if rule["rule_id"].startswith(f"{MESSAGE}.REQ.")
    }
    assert inherited_items == INHERITED_FULL | INHERITED_PARTIAL
    assert direct_codes == DIRECT_FULL | DIRECT_PARTIAL
    assert INTENTIONALLY_UNMAPPED.isdisjoint(inherited_items | direct_codes)

    for code in INHERITED_FULL:
        assert all(rule.get("mapping_status") == "INHERITED" for rule in _rules_for_code(code))
    for code in INHERITED_PARTIAL | DIRECT_PARTIAL:
        assert all(rule.get("mapping_status") == "PARTIAL" for rule in _rules_for_code(code))


def test_inherited_provenance_has_table39_and_exact_table34_requirement() -> None:
    for code in INHERITED_FULL | INHERITED_PARTIAL:
        rules = _rules_for_code(code)
        assert rules
        for rule in rules:
            assert [ref["source_id"] for ref in rule["source_refs"]] == [
                "22OP-RULE-P.SP.02.MSG.005-T39-6-29",
                f"22OP-RULE-P.SP.02.MSG.001-{code}",
            ]


def test_all_executable_fragments_pass_for_valid_values() -> None:
    evaluations = StructuredRuleEvaluator().evaluate_all(_rules(), _base_values())
    assert evaluations
    assert all(item.status is RuleStatus.PASS for item in evaluations), evaluations


@pytest.mark.parametrize(
    ("code", "mutator"),
    [
        ("1", lambda v: v.__setitem__(APP, [None, None])),
        ("4", lambda v: v.pop(f"{APP}/ipsdo:TrademarkApplicationId")),
        ("5", lambda v: v.__setitem__(f"{APP}/ipcdo:SignatureDetails", [None])),
        ("6", lambda v: v.pop(f"{APP}/ipsdo:ApplicationReceiptDate")),
        ("7", lambda v: v.__setitem__(f"{PARTY}/csdo:UnifiedCountryCode/@codeListId", ["WRONG", "ВОИС ST.3", "ВОИС ST.3"])),
        ("8", lambda v: v.__setitem__(f"{PARTY_ADDRESS}/csdo:BuildingNumberId", [None, "2", "3"])),
        ("9", lambda v: v.__setitem__(f"{PARTY_COMM}/csdo:CommunicationChannelName", ["Email", None, None])),
        ("10", lambda v: v.__setitem__(f"{PARTY_COMM}/csdo:CommunicationChannelCode", ["XX", "TE", "FX"])),
        ("11", lambda v: v.pop(f"{PATENT}/csdo:UnifiedCountryCode")),
        ("12", lambda v: v.__setitem__(f"{PATENT_ADDRESS}/csdo:AddressKindCode", "3")),
        ("14", lambda v: v.__setitem__(f"{PARTY}/ipsdo:IPPartyKindCode", ["AP", "AP", "RE"])),
        ("15", lambda v: v.__setitem__(f"{PARTY}/csdo:UnifiedCountryCode", [None, "RU", "RU"])),
        ("21", lambda v: v.__setitem__(f"{PARTY}/ipsdo:PatentAttorneyId", [None, None, None])),
        ("22", lambda v: v.__setitem__(PARTY_COMM, ["", "", None])),
        ("23", lambda v: v.__setitem__(f"{CORR_ADDRESS}/csdo:AddressKindCode", "2")),
        ("24", lambda v: v.__setitem__(f"{CORR_ADDRESS}/csdo:UnifiedCountryCode", "US")),
        ("25", lambda v: v.pop(f"{TM}/ipsdo:TrademarkKindName")),
        ("26", lambda v: v.__setitem__(f"{TM}/ipsdo:TrademarkKindCode", "999")),
        ("28", lambda v: v.__setitem__(f"{TM}/ipsdo:CollectiveMarkIndicator", "2")),
        ("29", lambda v: v.pop(f"{GOODS}/ipsdo:GoodsName")),
        ("30", lambda v: v.pop(f"{CLAIM}/ipsdo:RequestDate")),
        ("31", lambda v: v.pop(ARGUMENT)),
        ("32", lambda v: v.pop(f"{STAKE}/csdo:SubjectBriefName")),
        ("34", lambda v: v.__setitem__(f"{APP}/ipcdo:ComplaintDetails", [None])),
        ("35", lambda v: v.__setitem__("ipcdo:RefusalDetails", [None])),
        ("36", lambda v: v.pop(f"{VALIDITY}/csdo:StartDateTime")),
        ("37", lambda v: v.__setitem__(f"{VALIDITY}/csdo:EndDateTime", "2026-09-19T12:00:00+03:00")),
    ],
)
def test_every_executable_requirement_has_pass_and_fail_case(code, mutator) -> None:
    valid = _base_values()
    statuses = _statuses(code, valid)
    assert statuses and all(status is RuleStatus.PASS for status in statuses)

    invalid = deepcopy(valid)
    mutator(invalid)
    assert RuleStatus.FAIL in _statuses(code, invalid)


def test_req26_checks_allowed_sets_independently_not_code_name_pairing() -> None:
    values = _base_values()
    values[f"{TM}/ipsdo:TrademarkKindCode"] = "110"
    values[f"{TM}/ipsdo:TrademarkKindName"] = "Комбинированный знак"
    assert _statuses("26", values) == [RuleStatus.PASS]

    values[f"{TM}/ipsdo:TrademarkKindName"] = "Неизвестный знак"
    assert _statuses("26", values) == [RuleStatus.FAIL]


def test_req25_each_executable_fragment_has_a_failing_case() -> None:
    evaluator = StructuredRuleEvaluator()
    rules = _rules_for_code("25")
    assert len(rules) == 3
    for rule in rules:
        values = _base_values()
        collection = rule.get("selector", {}).get("collection")
        if rule["kind"] == "selection_cardinality" and collection == TM:
            values.pop(TM)
        elif rule["kind"] == "selection_cardinality" and collection == TMDESC:
            values.pop(TMDESC)
            values.pop(f"{TMDESC}/csdo:DescriptionText")
        else:
            values.pop(f"{TM}/ipsdo:TrademarkKindName")
        assert evaluator.evaluate(rule, values).status is RuleStatus.FAIL


def test_req29_cardinality_fragment_rejects_missing_goods() -> None:
    rule = next(rule for rule in _rules_for_code("29") if rule["kind"] == "selection_cardinality")
    values = _base_values()
    for path in list(values):
        if path == GOODS or path.startswith(GOODS + "/"):
            values.pop(path)
    assert StructuredRuleEvaluator().evaluate(rule, values).status is RuleStatus.FAIL


def test_req30_contains_only_three_confirmed_fields() -> None:
    rule = _rules_for_code("30")[0]
    assert rule["selector"] == {"collection": CLAIM}
    assert [assertion["target"]["field"] for assertion in rule["assertions"]] == [
        "ipcdo:StakeholderDetails",
        "ipsdo:RequestId",
        "ipsdo:RequestDate",
    ]


def test_req34_forbids_exactly_four_direct_children() -> None:
    expected = {
        f"{APP}/ipcdo:TrademarkNationalApplicationDetails",
        f"{APP}/ipcdo:ApplicantChangeDetails",
        f"{APP}/ipcdo:ComplaintDetails",
        f"{APP}/ipcdo:ApplicantComplainResponseDetails",
    }
    rules = _rules_for_code("34")
    assert {rule["selector"]["collection"] for rule in rules} == expected
    assert all(rule["min_occurs"] == 0 and rule["max_occurs"] == 0 for rule in rules)


def test_req33_has_no_executable_mapping() -> None:
    assert _rules_for_code("33") == []
