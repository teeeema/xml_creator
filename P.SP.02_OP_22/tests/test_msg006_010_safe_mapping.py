from copy import deepcopy
from pathlib import Path

import pytest

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
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
DOC = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
PRIORITY = f"{APP}/ipcdo:TrademarkPriorityDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
NATIONAL = f"{APP}/ipcdo:TrademarkNationalApplicationDetails"
NAMING = f"{APP}/ipcdo:NamingAbilityProofDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"

MESSAGES = (
    "P.SP.02.MSG.006",
    "P.SP.02.MSG.007",
    "P.SP.02.MSG.009",
    "P.SP.02.MSG.010",
)
TABLE = {
    "P.SP.02.MSG.006": "40",
    "P.SP.02.MSG.007": "41",
    "P.SP.02.MSG.009": "42",
    "P.SP.02.MSG.010": "43",
}
INHERITED_FULL = {"6", "7", "8", "9", "10", "11", "12", "14", "15", "21", "22", "23", "24", "25", "28", "29"}
INHERITED_PARTIAL = {"26"}
DIRECT_FULL = {
    "P.SP.02.MSG.006": {"1", "5", "30", "31", "32", "33", "34", "35"},
    "P.SP.02.MSG.007": {"1", "5", "32", "33", "34"},
    "P.SP.02.MSG.009": {"1", "5", "30", "31", "32"},
    "P.SP.02.MSG.010": {"1", "5", "30", "31", "32"},
}
DIRECT_PARTIAL = {
    "P.SP.02.MSG.006": {"4"},
    "P.SP.02.MSG.007": {"4", "30", "31"},
    "P.SP.02.MSG.009": {"4"},
    "P.SP.02.MSG.010": {"4"},
}
UNMAPPED_COMMON = {"2", "3", "13", "16", "17", "18", "19", "20", "27"}


def _engine() -> EaeuXmlEngine:
    return EaeuXmlEngine.load_process(PACKAGE)


def _rules(message: str):
    return _engine().rules[message].structured_rules


def _rules_for_code(message: str, code: str):
    direct_id = f"{message}.REQ.{code}"
    result = []
    for rule in _rules(message):
        if rule["rule_id"] == direct_id:
            result.append(rule)
            continue
        refs = rule.get("source_refs", [])
        if len(refs) >= 2 and refs[1].get("item") == code:
            result.append(rule)
    return result


def _statuses(message: str, code: str, values: dict[str, object]) -> list[RuleStatus]:
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(rule, values).status for rule in _rules_for_code(message, code)]


def _common_values() -> dict[str, object]:
    return {
        APP: [None],
        f"{APP}/ipsdo:TrademarkApplicationId": "APP-TEST",
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-22",
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
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-22T12:00:00+03:00",
    }


def _base_values(message: str) -> dict[str, object]:
    values = _common_values()
    if message == "P.SP.02.MSG.006":
        values[NAMING] = [None]
        values[DOC] = [None]
        values[f"{DOC}/ipsdo:IPDocKindCode"] = "DOC"
        values[f"{DOC}/csdo:DocId"] = "DOC-006"
        values[f"{DOC}/csdo:DocCreationDate"] = "2026-09-22"
        values[f"{DOC}/csdo:DescriptionText"] = "Описание"
        values[f"{DOC}/csdo:PageQuantity"] = "1"
        values[f"{DOC}/csdo:DocBinaryText"] = "QQ=="
    elif message == "P.SP.02.MSG.007":
        values[PRIORITY] = [None]
        values[f"{PRIORITY}/ipsdo:PriorityKindCode"] = "01"
        values[f"{PRIORITY}/ipsdo:PriorityDate"] = "2026-09-01"
        values[f"{PRIORITY}/csdo:UnifiedCountryCode"] = "RU"
        values[f"{PRIORITY}/csdo:UnifiedCountryCode/@codeListId"] = "ВОИС ST.3"
        values[DOC] = [None]
        values[f"{DOC}/csdo:DocName"] = "Документ"
        values[f"{DOC}/csdo:DocId"] = "DOC-007"
        values[f"{DOC}/csdo:DocCreationDate"] = "2026-09-22"
        values[f"{DOC}/csdo:DescriptionText"] = "Описание"
        values[f"{DOC}/csdo:PageQuantity"] = "1"
    elif message == "P.SP.02.MSG.009":
        values[STATUS] = [None]
        values[f"{STATUS}/csdo:StatusCode"] = "21"
        values[NATIONAL] = [None]
        values[f"{VALIDITY}/csdo:EndDateTime"] = "2026-09-23T12:00:00+03:00"
    elif message == "P.SP.02.MSG.010":
        values[STATUS] = [None]
        values[f"{STATUS}/csdo:StatusCode"] = "02"
    return values


@pytest.mark.parametrize("message", MESSAGES)
def test_mapping_inventory_status_scope_and_dual_provenance(message: str) -> None:
    rules = _rules(message)
    assert rules
    assert all(rule.get("applies_to_structure") == STRUCTURE for rule in rules)

    inherited_items = {
        rule["source_refs"][1]["item"]
        for rule in rules
        if len(rule.get("source_refs", [])) == 2
    }
    direct_codes = {
        rule["rule_id"].rsplit(".", 1)[-1]
        for rule in rules
        if rule["rule_id"].startswith(f"{message}.REQ.")
    }
    assert inherited_items == INHERITED_FULL | INHERITED_PARTIAL
    assert direct_codes == DIRECT_FULL[message] | DIRECT_PARTIAL[message]
    assert UNMAPPED_COMMON.isdisjoint(inherited_items | direct_codes)

    table = TABLE[message]
    current_range = f"22OP-RULE-{message}-T{table}-6-29"
    for code in INHERITED_FULL | INHERITED_PARTIAL:
        code_rules = _rules_for_code(message, code)
        assert code_rules
        for rule in code_rules:
            assert [ref["source_id"] for ref in rule["source_refs"]] == [
                current_range,
                f"22OP-RULE-P.SP.02.MSG.001-{code}",
            ]
            assert rule["source_refs"][0]["item"] == "6-29"
            assert rule["source_refs"][1]["item"] == code
            expected = "PARTIAL" if code == "26" else "INHERITED"
            assert rule.get("mapping_status") == expected

    for code in DIRECT_PARTIAL[message]:
        assert all(rule.get("mapping_status") == "PARTIAL" for rule in _rules_for_code(message, code))


@pytest.mark.parametrize("message", MESSAGES)
def test_all_new_executable_fragments_pass_valid_values(message: str) -> None:
    evaluations = StructuredRuleEvaluator().evaluate_all(_rules(message), _base_values(message))
    assert evaluations
    assert all(item.status is RuleStatus.PASS for item in evaluations), evaluations


def _mutate_common(code: str, values: dict[str, object]) -> None:
    if code == "6":
        values.pop(f"{APP}/ipsdo:ApplicationReceiptDate")
    elif code == "7":
        values[f"{PARTY}/csdo:UnifiedCountryCode/@codeListId"] = ["WRONG", "ВОИС ST.3", "ВОИС ST.3"]
    elif code == "8":
        values[f"{PARTY_ADDRESS}/csdo:BuildingNumberId"] = [None, "2", "3"]
    elif code == "9":
        values[f"{PARTY_COMM}/csdo:CommunicationChannelName"] = ["Email", None, None]
    elif code == "10":
        values[f"{PARTY_COMM}/csdo:CommunicationChannelCode"] = ["XX", "TE", "FX"]
    elif code == "11":
        values.pop(f"{PATENT}/csdo:UnifiedCountryCode")
    elif code == "12":
        values[f"{PATENT_ADDRESS}/csdo:AddressKindCode"] = "3"
    elif code == "14":
        values[f"{PARTY}/ipsdo:IPPartyKindCode"] = ["AP", "AP", "RE"]
    elif code == "15":
        values[f"{PARTY}/csdo:UnifiedCountryCode"] = [None, "RU", "RU"]
    elif code == "21":
        values[f"{PARTY}/ipsdo:PatentAttorneyId"] = [None, None, None]
    elif code == "22":
        values[PARTY_COMM] = ["", "", None]
    elif code == "23":
        values[f"{CORR_ADDRESS}/csdo:AddressKindCode"] = "2"
    elif code == "24":
        values[f"{CORR_ADDRESS}/csdo:UnifiedCountryCode"] = "US"
    elif code == "25":
        values.pop(f"{TM}/ipsdo:TrademarkKindName")
    elif code == "26":
        values[f"{TM}/ipsdo:TrademarkKindCode"] = "999"
    elif code == "28":
        values[f"{TM}/ipsdo:CollectiveMarkIndicator"] = "2"
    elif code == "29":
        values.pop(f"{GOODS}/ipsdo:GoodsName")
    else:
        raise AssertionError(code)


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("code", sorted(INHERITED_FULL | INHERITED_PARTIAL, key=int))
def test_each_inherited_safe_requirement_has_pass_and_fail_case(message: str, code: str) -> None:
    valid = _base_values(message)
    valid_statuses = _statuses(message, code, valid)
    assert valid_statuses and all(status is RuleStatus.PASS for status in valid_statuses)

    invalid = deepcopy(valid)
    _mutate_common(code, invalid)
    assert RuleStatus.FAIL in _statuses(message, code, invalid)


def _remove(path: str):
    return lambda values: values.pop(path)


def _remove_subtree(path: str):
    def mutator(values: dict[str, object]) -> None:
        for key in list(values):
            if key == path or key.startswith(path + "/"):
                values.pop(key)

    return mutator


DIRECT_FAIL_CASES = [
    ("P.SP.02.MSG.006", "1", lambda v: v.__setitem__(APP, [None, None])),
    ("P.SP.02.MSG.006", "4", _remove(f"{APP}/ipsdo:TrademarkApplicationId")),
    ("P.SP.02.MSG.006", "5", lambda v: v.__setitem__(f"{APP}/ipcdo:SignatureDetails", [None])),
    ("P.SP.02.MSG.006", "30", _remove(f"{DOC}/csdo:DocBinaryText")),
    ("P.SP.02.MSG.006", "31", _remove(NAMING)),
    ("P.SP.02.MSG.006", "33", lambda v: v.__setitem__("ipcdo:RefusalDetails", [None])),
    ("P.SP.02.MSG.006", "34", _remove(f"{VALIDITY}/csdo:StartDateTime")),
    ("P.SP.02.MSG.006", "35", lambda v: v.__setitem__(f"{VALIDITY}/csdo:EndDateTime", "2026-09-23T12:00:00+03:00")),
    ("P.SP.02.MSG.007", "1", lambda v: v.__setitem__(APP, [None, None])),
    ("P.SP.02.MSG.007", "4", _remove(f"{APP}/ipsdo:TrademarkApplicationId")),
    ("P.SP.02.MSG.007", "5", _remove_subtree(PRIORITY)),
    ("P.SP.02.MSG.007", "30", _remove(f"{PRIORITY}/csdo:UnifiedCountryCode")),
    ("P.SP.02.MSG.007", "31", _remove(f"{PRIORITY}/ipsdo:PriorityKindCode")),
    ("P.SP.02.MSG.007", "32", _remove(f"{DOC}/csdo:DocName")),
    ("P.SP.02.MSG.007", "33", _remove(f"{VALIDITY}/csdo:StartDateTime")),
    ("P.SP.02.MSG.007", "34", lambda v: v.__setitem__(f"{VALIDITY}/csdo:EndDateTime", "2026-09-23T12:00:00+03:00")),
    ("P.SP.02.MSG.009", "1", lambda v: v.__setitem__(APP, [None, None])),
    ("P.SP.02.MSG.009", "4", _remove(f"{APP}/ipsdo:TrademarkApplicationId")),
    ("P.SP.02.MSG.009", "5", lambda v: v.__setitem__(f"{STATUS}/csdo:StatusCode", "02")),
    ("P.SP.02.MSG.009", "30", _remove(NATIONAL)),
    ("P.SP.02.MSG.009", "31", _remove(f"{VALIDITY}/csdo:StartDateTime")),
    ("P.SP.02.MSG.009", "32", _remove(f"{VALIDITY}/csdo:EndDateTime")),
    ("P.SP.02.MSG.010", "1", lambda v: v.__setitem__(APP, [None, None])),
    ("P.SP.02.MSG.010", "4", _remove(f"{APP}/ipsdo:TrademarkApplicationId")),
    ("P.SP.02.MSG.010", "5", lambda v: v.__setitem__(f"{STATUS}/csdo:StatusCode", "21")),
    ("P.SP.02.MSG.010", "30", lambda v: v.__setitem__(f"{TM}/ipsdo:CollectiveMarkIndicator", "1")),
    ("P.SP.02.MSG.010", "31", _remove(f"{VALIDITY}/csdo:StartDateTime")),
    ("P.SP.02.MSG.010", "32", lambda v: v.__setitem__(f"{VALIDITY}/csdo:EndDateTime", "2026-09-23T12:00:00+03:00")),
]


@pytest.mark.parametrize(("message", "code", "mutator"), DIRECT_FAIL_CASES)
def test_direct_safe_requirements_have_pass_and_fail_case(message, code, mutator) -> None:
    valid = _base_values(message)
    statuses = _statuses(message, code, valid)
    assert statuses and all(status is RuleStatus.PASS for status in statuses)

    invalid = deepcopy(valid)
    mutator(invalid)
    assert RuleStatus.FAIL in _statuses(message, code, invalid)


@pytest.mark.parametrize(
    "forbidden",
    [
        f"{APP}/ipcdo:TrademarkNationalApplicationDetails",
        f"{APP}/ipcdo:ApplicantChangeDetails",
        f"{APP}/ipcdo:ComplaintDetails",
        f"{APP}/ipcdo:ApplicantComplainResponseDetails",
        f"{APP}/ipcdo:TrademarkClaimDetails",
    ],
)
def test_msg006_req32_forbids_each_exact_direct_child(forbidden: str) -> None:
    rules = _rules_for_code("P.SP.02.MSG.006", "32")
    assert {rule["selector"]["collection"] for rule in rules} == {
        f"{APP}/ipcdo:TrademarkNationalApplicationDetails",
        f"{APP}/ipcdo:ApplicantChangeDetails",
        f"{APP}/ipcdo:ComplaintDetails",
        f"{APP}/ipcdo:ApplicantComplainResponseDetails",
        f"{APP}/ipcdo:TrademarkClaimDetails",
    }
    values = _base_values("P.SP.02.MSG.006")
    values[forbidden] = [None]
    assert RuleStatus.FAIL in _statuses("P.SP.02.MSG.006", "32", values)


@pytest.mark.parametrize("message", ("P.SP.02.MSG.009", "P.SP.02.MSG.010"))
def test_status_code_list_id_is_forbidden(message: str) -> None:
    values = _base_values(message)
    values[f"{STATUS}/csdo:StatusCode/@codeListId"] = "STATUS-LIST"
    assert RuleStatus.FAIL in _statuses(message, "5", values)


def test_message_isolation_for_status_end_date_national_application_documents_and_indicator() -> None:
    msg009 = _base_values("P.SP.02.MSG.009")
    assert all(status is RuleStatus.PASS for status in _statuses("P.SP.02.MSG.009", "5", msg009))
    assert RuleStatus.FAIL in _statuses("P.SP.02.MSG.010", "5", msg009)

    msg010 = _base_values("P.SP.02.MSG.010")
    assert all(status is RuleStatus.PASS for status in _statuses("P.SP.02.MSG.010", "5", msg010))
    assert RuleStatus.FAIL in _statuses("P.SP.02.MSG.009", "5", msg010)

    msg006 = _base_values("P.SP.02.MSG.006")
    msg006[NATIONAL] = [None]
    assert RuleStatus.FAIL in _statuses("P.SP.02.MSG.006", "32", msg006)
    assert all(status is RuleStatus.PASS for status in _statuses("P.SP.02.MSG.009", "30", _base_values("P.SP.02.MSG.009")))

    doc006 = _base_values("P.SP.02.MSG.006")
    doc006.pop(f"{DOC}/csdo:DocBinaryText")
    assert RuleStatus.FAIL in _statuses("P.SP.02.MSG.006", "30", doc006)
    doc007 = _base_values("P.SP.02.MSG.007")
    assert f"{DOC}/csdo:DocBinaryText" not in doc007
    assert _statuses("P.SP.02.MSG.007", "32", doc007) == [RuleStatus.PASS]

    inherited_only = _base_values("P.SP.02.MSG.009")
    inherited_only[f"{TM}/ipsdo:CollectiveMarkIndicator"] = "1"
    assert all(status is RuleStatus.PASS for status in _statuses("P.SP.02.MSG.009", "28", inherited_only))
    exact_zero = _base_values("P.SP.02.MSG.010")
    exact_zero[f"{TM}/ipsdo:CollectiveMarkIndicator"] = "1"
    assert _statuses("P.SP.02.MSG.010", "28", exact_zero) == [RuleStatus.PASS]
    assert _statuses("P.SP.02.MSG.010", "30", exact_zero) == [RuleStatus.FAIL]


def test_msg008_is_not_created() -> None:
    assert not (PACKAGE / "message_rules" / "P.SP.02.MSG.008.yaml").exists()
    assert "P.SP.02.MSG.008" not in _engine().rules
