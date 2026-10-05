from copy import deepcopy
from pathlib import Path

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.001"
APP = "ipcdo:TrademarkApplicationDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
PATENT_AUTHORITY = f"{APP}/ipcdo:PatentAuthorityDetails"
PATENT_AUTHORITY_ADDRESS = f"{PATENT_AUTHORITY}/ccdo:SubjectAddressDetails"
ADDRESS = f"{APP}/ipcdo:CorrespondenceAddressDetails/ccdo:SubjectAddressDetails"
COMMUNICATION = f"{APP}/ipcdo:CorrespondenceAddressDetails/ccdo:CommunicationDetails"
TRADEMARK = f"{APP}/ipcdo:TrademarkDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
PRIORITY = f"{APP}/ipcdo:TrademarkPriorityDetails"
RESOURCE_STATUS = "ccdo:ResourceItemStatusDetails"
RESOURCE_VALIDITY = f"{RESOURCE_STATUS}/ccdo:ValidityPeriodDetails"

MAPPED_REQUIREMENTS = {
    "P.SP.02.MSG.001.REQ.001",
    "P.SP.02.MSG.001.REQ.002",
    "P.SP.02.MSG.001.REQ.003",
    "P.SP.02.MSG.001.REQ.006",
    "P.SP.02.MSG.001.REQ.007",
    "P.SP.02.MSG.001.REQ.008",
    "P.SP.02.MSG.001.REQ.009",
    "P.SP.02.MSG.001.REQ.010",
    "P.SP.02.MSG.001.REQ.011",
    "P.SP.02.MSG.001.REQ.012",
    "P.SP.02.MSG.001.REQ.023",
    "P.SP.02.MSG.001.REQ.024",
    "P.SP.02.MSG.001.REQ.025",
    "P.SP.02.MSG.001.REQ.028",
    "P.SP.02.MSG.001.REQ.029",
    "P.SP.02.MSG.001.REQ.030",
    "P.SP.02.MSG.001.REQ.031",
    "P.SP.02.MSG.001.REQ.034",
    "P.SP.02.MSG.001.REQ.035",
    "P.SP.02.MSG.001.REQ.036",
    "P.SP.02.MSG.001.REQ.037",
    "P.SP.02.MSG.001.REQ.038",
    "P.SP.02.MSG.001.REQ.039",
}


def _engine() -> EaeuXmlEngine:
    return EaeuXmlEngine.load_process(PACKAGE)


def _rules():
    return _engine().rules[MESSAGE].structured_rules


def _rule_values() -> dict[str, object]:
    return {
        APP: [None],
        f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-18",
        STATUS: [None],
        f"{STATUS}/csdo:StatusCode": "01",
        PATENT_AUTHORITY: [None],
        f"{PATENT_AUTHORITY}/csdo:UnifiedCountryCode": "RU",
        f"{PATENT_AUTHORITY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PATENT_AUTHORITY}/csdo:AuthorityName": "Национальное патентное ведомство",
        PATENT_AUTHORITY_ADDRESS: [None],
        f"{PATENT_AUTHORITY_ADDRESS}/csdo:AddressKindCode": "2",
        f"{PATENT_AUTHORITY_ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{PATENT_AUTHORITY_ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PATENT_AUTHORITY_ADDRESS}/csdo:CityName": "Москва",
        f"{PATENT_AUTHORITY_ADDRESS}/csdo:StreetName": "Тестовая",
        f"{PATENT_AUTHORITY_ADDRESS}/csdo:BuildingNumberId": "1",
        ADDRESS: [None],
        f"{ADDRESS}/csdo:AddressKindCode": "3",
        f"{ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{ADDRESS}/csdo:CityName": "Москва",
        f"{ADDRESS}/csdo:StreetName": "Тестовая",
        f"{ADDRESS}/csdo:BuildingNumberId": "1",
        COMMUNICATION: [None],
        f"{COMMUNICATION}/csdo:CommunicationChannelCode": "EM",
        f"{COMMUNICATION}/csdo:CommunicationChannelId": "test@example.test",
        TRADEMARK: [None],
        f"{TRADEMARK}/ipcdo:TMDescriptionDetails": [None],
        f"{TRADEMARK}/ipcdo:TMDescriptionDetails/csdo:DescriptionText": "Описание",
        f"{TRADEMARK}/ipsdo:TrademarkKindCode": "110",
        f"{TRADEMARK}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "1",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "01",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        PRIORITY: [None],
        f"{PRIORITY}/ipsdo:PriorityKindCode": "100",
        f"{PRIORITY}/ipsdo:PriorityKindName": "Приоритет",
        f"{PRIORITY}/ipsdo:PriorityDate": "2026-09-18",
        f"{PRIORITY}/csdo:UnifiedCountryCode": "RU",
        f"{PRIORITY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{APP}/ipsdo:ConsentToDataProcessingIndicator": "1",
        RESOURCE_STATUS: [None],
        RESOURCE_VALIDITY: [None],
        f"{RESOURCE_VALIDITY}/csdo:StartDateTime": "2026-09-18T12:00:00+03:00",
    }


def _evaluations(values: dict[str, object]):
    evaluator = StructuredRuleEvaluator()
    return evaluator.evaluate_all(_rules(), values)


def _statuses(values: dict[str, object], rule_id: str) -> list[RuleStatus]:
    return [
        item.status
        for item in _evaluations(values)
        if item.rule_id == rule_id
    ]


def _set(path: str, value: object):
    def mutate(values: dict[str, object]) -> None:
        values[path] = value

    return mutate


def _drop(path: str):
    def mutate(values: dict[str, object]) -> None:
        values.pop(path, None)

    return mutate


def test_msg001_structured_rules_are_linked_to_captured_requirements() -> None:
    rules = _engine().rules[MESSAGE]
    captured = {rule["rule_id"]: rule for rule in rules.business_rules}

    assert {rule["rule_id"] for rule in rules.structured_rules} == MAPPED_REQUIREMENTS
    for rule in rules.structured_rules:
        assert rule["rule_id"] in captured
        assert rule["source_refs"] == captured[rule["rule_id"]]["source_refs"]


def test_partial_mappings_are_explicitly_marked() -> None:
    partial_rule_ids = {
        "P.SP.02.MSG.001.REQ.003",
        "P.SP.02.MSG.001.REQ.030",
        "P.SP.02.MSG.001.REQ.038",
    }
    partial_rules = [rule for rule in _rules() if rule["rule_id"] in partial_rule_ids]

    assert {rule["rule_id"] for rule in partial_rules} == partial_rule_ids
    assert all(rule.get("mapping_status") == "PARTIAL" for rule in partial_rules)


def test_msg001_mapped_rules_pass_for_valid_values() -> None:
    evaluations = _evaluations(_rule_values())
    assert evaluations
    assert all(item.status is RuleStatus.PASS for item in evaluations)


def test_req003_passes_and_fails_on_required_application_id() -> None:
    values = _rule_values()
    assert _statuses(values, "P.SP.02.MSG.001.REQ.003") == [RuleStatus.PASS]

    values.pop(f"{APP}/ipsdo:TrademarkApplicationId")
    assert _statuses(values, "P.SP.02.MSG.001.REQ.003") == [RuleStatus.FAIL]


@pytest.mark.parametrize(
    "forbidden_field",
    [
        "ipsdo:TrademarkDecisionIndicator",
        "ipsdo:TrademarkApplicationId",
        "ipsdo:ApellationOfOriginEAEUId",
        "ipsdo:TrademarkRegRefusalReasonText",
    ],
)
def test_req030_rejects_each_confirmed_forbidden_goods_field(forbidden_field: str) -> None:
    values = _rule_values()
    assert _statuses(values, "P.SP.02.MSG.001.REQ.030") == [RuleStatus.PASS]

    values[f"{GOODS}/{forbidden_field}"] = "FORBIDDEN"
    assert _statuses(values, "P.SP.02.MSG.001.REQ.030") == [RuleStatus.FAIL]


def test_req030_passes_for_multiple_goods_without_forbidden_fields() -> None:
    values = _rule_values()
    values[GOODS] = [None, None]
    values[f"{GOODS}/ipsdo:GoodsClassCode"] = ["01", "02"]
    values[f"{GOODS}/ipsdo:GoodsClassName"] = ["Класс 01", "Класс 02"]
    values[f"{GOODS}/ipsdo:GoodsName"] = ["Товар 1", "Товар 2"]

    assert _statuses(values, "P.SP.02.MSG.001.REQ.030") == [RuleStatus.PASS]


def test_req030_rejects_one_invalid_goods_instance_from_multiple() -> None:
    values = _rule_values()
    values[GOODS] = [None, None]
    values[f"{GOODS}/ipsdo:GoodsClassCode"] = ["01", "02"]
    values[f"{GOODS}/ipsdo:GoodsClassName"] = ["Класс 01", "Класс 02"]
    values[f"{GOODS}/ipsdo:GoodsName"] = ["Товар 1", "Товар 2"]
    values[f"{GOODS}/ipsdo:TrademarkDecisionIndicator"] = [None, "1"]

    assert _statuses(values, "P.SP.02.MSG.001.REQ.030") == [RuleStatus.FAIL]


def test_req030_does_not_match_inconsistency_text_on_other_existing_paths() -> None:
    values = _rule_values()
    values[f"{APP}/ipsdo:InconsistencyText"] = "Не относится к GoodsBaseDetails"
    values[f"{APP}/ipcdo:TrademarkClaimDetails/ipsdo:InconsistencyText"] = "Отдельный реквизит"

    assert _statuses(values, "P.SP.02.MSG.001.REQ.030") == [RuleStatus.PASS]


def test_req038_requires_start_datetime_without_external_timestamp_comparison() -> None:
    values = _rule_values()
    assert _statuses(values, "P.SP.02.MSG.001.REQ.038") == [RuleStatus.PASS]

    values[f"{RESOURCE_VALIDITY}/csdo:StartDateTime"] = "2000-01-01T00:00:00+00:00"
    assert _statuses(values, "P.SP.02.MSG.001.REQ.038") == [RuleStatus.PASS]

    values.pop(f"{RESOURCE_VALIDITY}/csdo:StartDateTime")
    assert _statuses(values, "P.SP.02.MSG.001.REQ.038") == [RuleStatus.FAIL]


def test_req011_passes_and_fails_on_required_country_code() -> None:
    values = _rule_values()
    assert _statuses(values, "P.SP.02.MSG.001.REQ.011") == [RuleStatus.PASS]

    values.pop(f"{PATENT_AUTHORITY}/csdo:UnifiedCountryCode")
    assert _statuses(values, "P.SP.02.MSG.001.REQ.011") == [RuleStatus.FAIL]


@pytest.mark.parametrize(
    "missing_path",
    [
        f"{PATENT_AUTHORITY}/csdo:AuthorityName",
        f"{PATENT_AUTHORITY_ADDRESS}/csdo:AddressKindCode",
    ],
)
def test_req012_requires_authority_address_and_address_kind(missing_path: str) -> None:
    values = _rule_values()
    assert _statuses(values, "P.SP.02.MSG.001.REQ.012") == [RuleStatus.PASS]

    values.pop(missing_path)
    assert _statuses(values, "P.SP.02.MSG.001.REQ.012") == [RuleStatus.FAIL]


def test_req012_requires_subject_address_subtree() -> None:
    values = _rule_values()
    for path in list(values):
        if path == PATENT_AUTHORITY_ADDRESS or path.startswith(PATENT_AUTHORITY_ADDRESS + "/"):
            values.pop(path)

    assert _statuses(values, "P.SP.02.MSG.001.REQ.012") == [RuleStatus.FAIL]


def test_req012_address_kind_fixed_value_is_validation_only() -> None:
    values = _rule_values()
    values[f"{PATENT_AUTHORITY_ADDRESS}/csdo:AddressKindCode"] = "3"

    assert _statuses(values, "P.SP.02.MSG.001.REQ.012") == [RuleStatus.FAIL]
    assert values[f"{PATENT_AUTHORITY_ADDRESS}/csdo:AddressKindCode"] == "3"


@pytest.mark.parametrize(
    ("rule_id", "mutate"),
    [
        ("P.SP.02.MSG.001.REQ.001", _set(APP, [None, None])),
        ("P.SP.02.MSG.001.REQ.002", _set(f"{STATUS}/csdo:StatusCode", "02")),
        ("P.SP.02.MSG.001.REQ.003", _drop(f"{APP}/ipsdo:TrademarkApplicationId")),
        ("P.SP.02.MSG.001.REQ.006", _drop(f"{APP}/ipsdo:ApplicationReceiptDate")),
        ("P.SP.02.MSG.001.REQ.007", _set(f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId", "OTHER")),
        ("P.SP.02.MSG.001.REQ.008", _drop(f"{ADDRESS}/csdo:CityName")),
        ("P.SP.02.MSG.001.REQ.009", _set(f"{COMMUNICATION}/csdo:CommunicationChannelName", "Email")),
        ("P.SP.02.MSG.001.REQ.010", _set(f"{COMMUNICATION}/csdo:CommunicationChannelCode", "XX")),
        ("P.SP.02.MSG.001.REQ.011", _drop(f"{PATENT_AUTHORITY}/csdo:UnifiedCountryCode")),
        ("P.SP.02.MSG.001.REQ.012", _set(f"{PATENT_AUTHORITY_ADDRESS}/csdo:AddressKindCode", "3")),
        ("P.SP.02.MSG.001.REQ.023", _set(f"{ADDRESS}/csdo:AddressKindCode", "2")),
        ("P.SP.02.MSG.001.REQ.024", _set(f"{ADDRESS}/csdo:UnifiedCountryCode", "US")),
        ("P.SP.02.MSG.001.REQ.025", _drop(f"{TRADEMARK}/ipsdo:TrademarkKindName")),
        ("P.SP.02.MSG.001.REQ.028", _set(f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator", "true")),
        ("P.SP.02.MSG.001.REQ.029", _drop(f"{GOODS}/ipsdo:GoodsClassName")),
        ("P.SP.02.MSG.001.REQ.030", _set(f"{GOODS}/ipsdo:TrademarkDecisionIndicator", "1")),
        ("P.SP.02.MSG.001.REQ.031", _drop(f"{PRIORITY}/ipsdo:PriorityKindName")),
        ("P.SP.02.MSG.001.REQ.034", _set(f"{APP}/ipsdo:ConsentToDataProcessingIndicator", "0")),
        ("P.SP.02.MSG.001.REQ.035", _set(f"{APP}/ipcdo:SignatureDetails", [None])),
        ("P.SP.02.MSG.001.REQ.036", _set(f"{APP}/ipcdo:ComplaintDetails", [None])),
        ("P.SP.02.MSG.001.REQ.037", _set("ipcdo:RefusalDetails", [None])),
        ("P.SP.02.MSG.001.REQ.038", _drop(f"{RESOURCE_VALIDITY}/csdo:StartDateTime")),
        ("P.SP.02.MSG.001.REQ.039", _set(f"{RESOURCE_STATUS}/csdo:UpdateDateTime", "2026-09-18T12:00:00+03:00")),
    ],
)
def test_each_mapped_requirement_has_a_failing_case(rule_id, mutate) -> None:
    values = _rule_values()
    mutate(values)
    statuses = _statuses(values, rule_id)

    assert statuses
    assert RuleStatus.FAIL in statuses


def test_req025_requires_tm_description_container() -> None:
    values = _rule_values()
    values.pop(f"{TRADEMARK}/ipcdo:TMDescriptionDetails")
    values.pop(f"{TRADEMARK}/ipcdo:TMDescriptionDetails/csdo:DescriptionText")

    assert RuleStatus.FAIL in _statuses(values, "P.SP.02.MSG.001.REQ.025")


def test_for_each_rejects_one_invalid_repeatable_instance() -> None:
    values = _rule_values()
    values[GOODS] = [None, None]
    values[f"{GOODS}/ipsdo:GoodsClassCode"] = ["01", "02"]
    values[f"{GOODS}/ipsdo:GoodsClassName"] = ["Класс 01", None]
    values[f"{GOODS}/ipsdo:GoodsName"] = ["Товар 1", "Товар 2"]

    assert RuleStatus.FAIL in _statuses(values, "P.SP.02.MSG.001.REQ.029")


def test_qname_and_scoped_path_do_not_match_neighbors() -> None:
    values = _rule_values()
    values[f"{APP}/test:Container/csdo:UnifiedCountryCodeExtra"] = "US"
    values[f"{APP}/test:Container/csdo:UnifiedCountryCodeExtra/@codeListId"] = "WRONG"

    patent_address = f"{APP}/ipcdo:PatentAuthorityDetails/ccdo:SubjectAddressDetails"
    values[patent_address] = [None]
    values[f"{patent_address}/csdo:AddressKindCode"] = "2"
    values[f"{patent_address}/csdo:UnifiedCountryCode"] = "US"
    values[f"{patent_address}/csdo:UnifiedCountryCode/@codeListId"] = "ВОИС ST.3"
    values[f"{patent_address}/csdo:CityName"] = "New York"
    values[f"{patent_address}/csdo:StreetName"] = "Test Street"
    values[f"{patent_address}/csdo:BuildingNumberId"] = "1"

    assert all(item.status is RuleStatus.PASS for item in _evaluations(values))


def _generation_values() -> dict[str, object]:
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000001",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-18T12:00:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-18",
        f"{APP}/ipsdo:TrademarkApplicationId": "TEST-001",
        TRADEMARK: [None],
        f"{TRADEMARK}/ipcdo:TMDescriptionDetails": [None],
        f"{TRADEMARK}/ipcdo:TMDescriptionDetails/csdo:DescriptionText": "Описание",
        f"{TRADEMARK}/ipsdo:TrademarkKindCode": "110",
        f"{TRADEMARK}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "1",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "01",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        f"{APP}/ipsdo:ConsentToDataProcessingIndicator": "1",
        RESOURCE_STATUS: [None],
        RESOURCE_VALIDITY: [None],
        f"{RESOURCE_VALIDITY}/csdo:StartDateTime": "2026-09-18T12:00:00+03:00",
    }


def test_trn001_msg001_generation_then_structured_validation() -> None:
    engine = _engine()
    transaction = engine.get_transaction("P.SP.02.TRN.001")
    assert transaction.initiating_message == MESSAGE

    values = _generation_values()
    body = engine.build_body(MESSAGE, values, mode=GenerationMode.TEST)
    validation = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)

    assert validation.is_valid
    assert validation.is_complete
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    assert str(body.serialize_xml_element().tag).endswith("TrademarkRegistrationDetails")
    assert engine.build_application_action("P.SP.02.TRN.001", MESSAGE).serialize().endswith(f"/{MESSAGE}")
