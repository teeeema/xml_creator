from copy import deepcopy
from pathlib import Path

import pytest

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.004"
STRUCTURE = "R.IP.SP.02.002"
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
PARTY_ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
PARTY_COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
TMDESC = f"{TM}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
DOC = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
CLAIM = f"{APP}/ipcdo:TrademarkClaimDetails"
STAKE = f"{CLAIM}/ipcdo:StakeholderDetails"
STAKE_ADDRESS = f"{STAKE}/ccdo:SubjectAddressDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"

INHERITED_FULL = {"6", "7", "8", "9", "10", "11", "12", "14", "15", "21", "22", "23", "24", "25", "28", "29"}
INHERITED_PARTIAL = {"26"}
DIRECT_FULL = {"1", "5", "30", "31", "32", "33", "34", "35", "36", "37"}
DIRECT_PARTIAL = {"4"}
INTENTIONALLY_UNMAPPED = {"2", "3", "13", "16", "17", "18", "19", "20", "27"}


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
        f"{APP}/ipsdo:TrademarkApplicationId": "APP-001",
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-18",
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": "AP",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": "Заявитель",
        PARTY_ADDRESS: [""],
        f"{PARTY_ADDRESS}/csdo:AddressKindCode": "2",
        f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY_ADDRESS}/csdo:CityName": "Москва",
        f"{PARTY_ADDRESS}/csdo:StreetName": "Тестовая",
        f"{PARTY_ADDRESS}/csdo:BuildingNumberId": "1",
        PARTY_COMM: [""],
        f"{PARTY_COMM}/csdo:CommunicationChannelCode": "EM",
        f"{PARTY_COMM}/csdo:CommunicationChannelId": "test@example.test",
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
        DOC: [None],
        f"{DOC}/ipsdo:IPDocKindName": "Приложение",
        f"{DOC}/csdo:DocId": "DOC-1",
        f"{DOC}/csdo:DocCreationDate": "2026-09-18",
        f"{DOC}/csdo:DescriptionText": "Описание документа",
        f"{DOC}/csdo:PageQuantity": 1,
        CLAIM: [None],
        STAKE: [""],
        f"{CLAIM}/ipsdo:RequestId": "REQ-1",
        f"{CLAIM}/ipsdo:RequestDate": "2026-09-18",
        f"{CLAIM}/ipsdo:InconsistencyText": "Описание несоответствия",
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
        f"{STAKE_ADDRESS}/csdo:BuildingNumberId": "1",
        STATUS: [None],
        f"{STATUS}/csdo:EventDate": "2026-09-18",
        f"{STATUS}/csdo:StatusCode": "02",
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-18T12:00:00+03:00",
    }


def test_mapping_scope_status_and_intentionally_unmapped_requirements() -> None:
    rules = _rules()
    assert rules
    assert all(rule.get("applies_to_structure") == STRUCTURE for rule in rules)

    inherited_items = {
        rule["source_refs"][1]["item"]
        for rule in rules
        if len(rule.get("source_refs", [])) == 2
    }
    assert inherited_items == INHERITED_FULL | INHERITED_PARTIAL

    direct_codes = {
        rule["rule_id"].rsplit(".", 1)[-1]
        for rule in rules
        if rule["rule_id"].startswith(f"{MESSAGE}.REQ.")
    }
    assert direct_codes == DIRECT_FULL | DIRECT_PARTIAL
    assert INTENTIONALLY_UNMAPPED.isdisjoint(inherited_items | direct_codes)

    for code in INHERITED_FULL:
        assert all(rule.get("mapping_status") == "INHERITED" for rule in _rules_for_code(code))
    for code in INHERITED_PARTIAL | DIRECT_PARTIAL:
        assert all(rule.get("mapping_status") == "PARTIAL" for rule in _rules_for_code(code))


def test_inherited_provenance_has_table38_and_exact_table34_requirement() -> None:
    for code in INHERITED_FULL | INHERITED_PARTIAL:
        rules = _rules_for_code(code)
        assert rules
        for rule in rules:
            assert [ref["source_id"] for ref in rule["source_refs"]] == [
                "22OP-RULE-P.SP.02.MSG.004-6-29",
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
        ("14", lambda v: (v.__setitem__(PARTY, [None, None]), v.__setitem__(f"{PARTY}/ipsdo:IPPartyKindCode", ["AP", "AP"]))),
        ("25", lambda v: v.pop(f"{TM}/ipsdo:TrademarkKindName")),
        ("28", lambda v: v.__setitem__(f"{TM}/ipsdo:CollectiveMarkIndicator", "true")),
        ("31", lambda v: v.pop(f"{CLAIM}/ipsdo:RequestId")),
        ("32", lambda v: v.pop(f"{STAKE}/csdo:SubjectBriefName")),
        ("33", lambda v: v.__setitem__(f"{APP}/ipcdo:ArgumentDetails", [None])),
        ("34", lambda v: v.__setitem__("ipcdo:RefusalDetails", [None])),
        ("35", lambda v: v.__setitem__(f"{STATUS}/csdo:StatusCode", "01")),
        ("36", lambda v: v.pop(f"{VALIDITY}/csdo:StartDateTime")),
        ("37", lambda v: v.__setitem__(f"{VALIDITY}/csdo:EndDateTime", "2026-09-19T12:00:00+03:00")),
    ],
)
def test_targeted_full_rules_have_pass_and_fail_cases(code, mutator) -> None:
    valid = _base_values()
    statuses = _statuses(code, valid)
    assert statuses and all(status is RuleStatus.PASS for status in statuses)

    invalid = deepcopy(valid)
    mutator(invalid)
    assert RuleStatus.FAIL in _statuses(code, invalid)


def test_req26_partial_checks_code_and_name_allowed_sets_independently() -> None:
    valid = _base_values()
    assert _statuses("26", valid) == [RuleStatus.PASS]

    bad_code = deepcopy(valid)
    bad_code[f"{TM}/ipsdo:TrademarkKindCode"] = "999"
    assert _statuses("26", bad_code) == [RuleStatus.FAIL]

    bad_name = deepcopy(valid)
    bad_name[f"{TM}/ipsdo:TrademarkKindName"] = "Неизвестный знак"
    assert _statuses("26", bad_name) == [RuleStatus.FAIL]

    # No code/name pair equivalence is asserted: both independently allowed values pass.
    independent_allowed_values = deepcopy(valid)
    independent_allowed_values[f"{TM}/ipsdo:TrademarkKindCode"] = "110"
    independent_allowed_values[f"{TM}/ipsdo:TrademarkKindName"] = "Комбинированный знак"
    assert _statuses("26", independent_allowed_values) == [RuleStatus.PASS]


def test_req30_direct_document_scope_is_exact() -> None:
    rules = _rules_for_code("30")
    assert len(rules) == 1
    assert rules[0]["selector"] == {"collection": DOC}


def test_req33_forbids_all_five_direct_children() -> None:
    forbidden = [
        "TrademarkNationalApplicationDetails",
        "ApplicantChangeDetails",
        "ComplaintDetails",
        "ApplicantComplainResponseDetails",
        "ArgumentDetails",
    ]
    assert len(_rules_for_code("33")) == 5
    for child in forbidden:
        values = _base_values()
        values[f"{APP}/ipcdo:{child}"] = [None]
        assert RuleStatus.FAIL in _statuses("33", values)


def test_req6_requires_application_receipt_date() -> None:
    values = _base_values()
    assert _statuses("6", values) == [RuleStatus.PASS]
    values.pop(f"{APP}/ipsdo:ApplicationReceiptDate")
    assert _statuses("6", values) == [RuleStatus.FAIL]


def test_req25_each_executable_fragment_has_a_failing_case() -> None:
    evaluator = StructuredRuleEvaluator()
    rules = _rules_for_code("25")
    assert len(rules) == 3

    for rule in rules:
        values = _base_values()
        kind = rule["kind"]
        collection = rule.get("selector", {}).get("collection")
        if kind == "selection_cardinality" and collection == TM:
            values.pop(TM)
        elif kind == "selection_cardinality" and collection == TMDESC:
            values.pop(TMDESC)
            values.pop(f"{TMDESC}/csdo:DescriptionText")
        elif kind == "for_each":
            values.pop(f"{TM}/ipsdo:TrademarkKindName")
        else:
            raise AssertionError(rule)
        assert evaluator.evaluate(rule, values).status is RuleStatus.FAIL


def test_req29_cardinality_fragment_rejects_missing_goods() -> None:
    rules = [rule for rule in _rules_for_code("29") if rule["kind"] == "selection_cardinality"]
    assert len(rules) == 1
    values = _base_values()
    for path in list(values):
        if path == GOODS or path.startswith(GOODS + "/"):
            values.pop(path)
    assert StructuredRuleEvaluator().evaluate(rules[0], values).status is RuleStatus.FAIL
