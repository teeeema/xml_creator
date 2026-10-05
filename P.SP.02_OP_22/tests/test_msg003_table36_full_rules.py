from pathlib import Path

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.003"
STRUCTURE_002 = "R.IP.SP.02.002"
STRUCTURE_007 = "R.IP.SP.02.007"

APP = "ipcdo:TrademarkApplicationDetails"
GOODS_TRADEMARK_ID = f"{APP}/ipcdo:GoodsBaseDetails/ipsdo:TrademarkId"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
REFUSAL = "ipcdo:RefusalDetails"
RESOURCE_STATUS = "ccdo:ResourceItemStatusDetails"
RESOURCE_VALIDITY = f"{RESOURCE_STATUS}/ccdo:ValidityPeriodDetails"

RULE_IDS = {
    "P.SP.02.MSG.003.T36.REQ.2",
    "P.SP.02.MSG.003.T36.REQ.5",
    "P.SP.02.MSG.003.T36.REQ.31",
    "P.SP.02.MSG.003.T36.REQ.33",
}


def _engine() -> EaeuXmlEngine:
    return EaeuXmlEngine.load_process(PACKAGE)


def _rules():
    return _engine().rules[MESSAGE].structured_rules


def _rule(rule_id: str):
    return next(rule for rule in _rules() if rule["rule_id"] == rule_id)


def _status(rule_id: str, values: dict[str, object]) -> RuleStatus:
    return StructuredRuleEvaluator().evaluate(_rule(rule_id), values).status


def _sample_value(field):
    datatype = (field.datatype or "").lower()
    if "indicatortype" in datatype:
        return True
    if "datetimetype" in datatype:
        return "2026-09-18T12:00:00+03:00"
    if datatype.endswith("datetype"):
        return "2026-09-18"
    if "quantity" in datatype or "integer" in datatype:
        return 1
    return "TEST"


def _minimal_values(structure):
    included: set[str] = set()
    children = {field.parent for field in structure.fields if field.parent}
    values = {}
    for field in sorted(structure.fields, key=lambda item: item.order):
        if not field.min_occurs:
            continue
        if field.parent and field.parent not in included:
            continue
        included.add(field.field_id)
        if field.kind == "ATTRIBUTE" or field.field_id not in children:
            values[field.path] = _sample_value(field)
        else:
            values[field.path] = None
    return values


def _embedded_values_for_build(structure_id: str, structure):
    values = _minimal_values(structure)
    if structure_id == STRUCTURE_002:
        trademark = f"{APP}/ipcdo:TrademarkDetails"
        goods = f"{APP}/ipcdo:GoodsBaseDetails"
        values[trademark] = None
        values[f"{trademark}/ipcdo:TMDescriptionDetails"] = None
        values[f"{trademark}/ipcdo:TMDescriptionDetails/csdo:DescriptionText"] = "TEST"
        values[f"{trademark}/ipsdo:TrademarkKindCode"] = "110"
        values[f"{trademark}/ipsdo:TrademarkKindName"] = "TEST"
        values[f"{trademark}/ipsdo:CollectiveMarkIndicator"] = "1"
        values[goods] = None
        values[f"{goods}/ipsdo:GoodsClassCode"] = "01"
        values[f"{goods}/ipsdo:GoodsClassName"] = "TEST"
        values[f"{goods}/ipsdo:GoodsName"] = "TEST"
        values[f"{goods}/ipsdo:TrademarkApplicationId"] = "APP-001"
        values[f"{goods}/ipsdo:TrademarkRegRefusalReasonText"] = "TEST"
        values[REFUSAL] = None
        values[f"{REFUSAL}/csdo:EventDate"] = "2026-09-18"
        values[f"{REFUSAL}/csdo:DescriptionText"] = "TEST"
        values[RESOURCE_VALIDITY] = None
        values[f"{RESOURCE_VALIDITY}/csdo:EndDateTime"] = "2026-09-18T12:00:00+03:00"
    elif structure_id == STRUCTURE_007:
        root = "ipcdo:UnifiedRegisterRecordsDetails"
        party = f"{root}/ipcdo:IPPartyDetails"
        address = f"{party}/ccdo:SubjectAddressDetails"
        communication = f"{party}/ccdo:CommunicationDetails"
        goods = f"{root}/ipcdo:GoodsBaseDetails"
        validity = f"{root}/ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails"
        values.update({
            f"{root}/ipsdo:RegistrationDate": "2026-09-18",
            f"{root}/csdo:DocValidityDate": "2027-09-18",
            f"{root}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
            f"{root}/ipsdo:TrademarkId": "2026/RU-000001",
            party: None,
            f"{party}/ipsdo:IPPartyKindCode": "RH",
            f"{party}/csdo:UnifiedCountryCode": "RU",
            f"{party}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            f"{party}/ipsdo:IPSubjectName": "Правообладатель",
            address: None,
            f"{address}/csdo:AddressKindCode": "2",
            f"{address}/csdo:UnifiedCountryCode": "RU",
            f"{address}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            f"{address}/csdo:CityName": "Москва",
            f"{address}/csdo:StreetName": "Тестовая",
            f"{address}/csdo:BuildingNumberId": "1",
            communication: None,
            f"{communication}/csdo:CommunicationChannelCode": "EM",
            f"{communication}/csdo:CommunicationChannelId": "test@example.test",
            goods: None,
            f"{goods}/ipsdo:GoodsClassName": "Класс 01",
            f"{goods}/ipsdo:GoodsName": "Товар",
            f"{goods}/ipsdo:TrademarkDecisionIndicator": True,
            f"{goods}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
            validity: None,
            f"{validity}/csdo:StartDateTime": "2026-09-18T12:00:00+03:00",
        })
    return values


def test_only_requested_table36_rules_are_machine_mapped() -> None:
    rules = _engine().rules[MESSAGE]
    captured = {rule["rule_id"]: rule for rule in rules.business_rules}
    requested = [rule for rule in rules.structured_rules if rule["rule_id"] in RULE_IDS]

    assert {rule["rule_id"] for rule in requested} == RULE_IDS
    for rule in requested:
        assert rule["applies_to_structure"] == STRUCTURE_002
        assert rule["source_refs"] == captured[rule["rule_id"]]["source_refs"]


def test_t36_req2_forbids_trademark_id() -> None:
    rule_id = "P.SP.02.MSG.003.T36.REQ.2"
    assert _status(rule_id, {}) is RuleStatus.PASS
    assert _status(rule_id, {GOODS_TRADEMARK_ID: "TM-001"}) is RuleStatus.FAIL


def test_t36_req5_requires_event_date_status_20_and_no_code_list_id() -> None:
    rule_id = "P.SP.02.MSG.003.T36.REQ.5"
    valid = {
        STATUS: [None],
        f"{STATUS}/csdo:EventDate": "2026-09-18",
        f"{STATUS}/csdo:StatusCode": "20",
    }
    assert _status(rule_id, valid) is RuleStatus.PASS

    missing_event_date = dict(valid)
    missing_event_date.pop(f"{STATUS}/csdo:EventDate")
    assert _status(rule_id, missing_event_date) is RuleStatus.FAIL

    wrong_status = dict(valid)
    wrong_status[f"{STATUS}/csdo:StatusCode"] = "01"
    assert _status(rule_id, wrong_status) is RuleStatus.FAIL

    with_classifier = dict(valid)
    with_classifier[f"{STATUS}/csdo:StatusCode/@codeListId"] = "TEST"
    assert _status(rule_id, with_classifier) is RuleStatus.FAIL


def test_t36_req31_requires_refusal_details() -> None:
    rule_id = "P.SP.02.MSG.003.T36.REQ.31"
    assert _status(rule_id, {REFUSAL: [None]}) is RuleStatus.PASS
    assert _status(rule_id, {}) is RuleStatus.FAIL


def test_t36_req33_requires_end_datetime_in_resource_validity_period() -> None:
    rule_id = "P.SP.02.MSG.003.T36.REQ.33"
    valid = {
        RESOURCE_STATUS: [None],
        RESOURCE_VALIDITY: [None],
        f"{RESOURCE_VALIDITY}/csdo:EndDateTime": "2026-09-18T12:00:00+03:00",
    }
    assert _status(rule_id, valid) is RuleStatus.PASS

    missing_end = dict(valid)
    missing_end.pop(f"{RESOURCE_VALIDITY}/csdo:EndDateTime")
    assert _status(rule_id, missing_end) is RuleStatus.FAIL


@pytest.mark.parametrize(
    ("structure_id", "expected_rule_ids"),
    [
        (STRUCTURE_002, RULE_IDS),
        (STRUCTURE_007, set()),
    ],
)
def test_table36_rules_apply_only_to_embedded_002(structure_id, expected_rule_ids) -> None:
    engine = _engine()
    container = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    embedded = engine.resolve_structure(structure_id, mode=GenerationMode.TEST).definition
    container_values = _minimal_values(container)
    embedded_values = _embedded_values_for_build(structure_id, embedded)

    body = engine.build_body(
        MESSAGE,
        container_values,
        mode=GenerationMode.TEST,
        embedded_structure_id=structure_id,
        embedded_values=embedded_values,
    )
    payload = list(body.serialize_xml_element())[-1]
    validation_values = dict(container_values)
    validation_values["*"] = payload
    result = engine.validate_body(MESSAGE, validation_values, mode=GenerationMode.TEST)

    assert result.is_valid, [(issue.code, issue.field_path, issue.message) for issue in result.issues]
    evaluated_rule_ids = {evaluation.rule_id for evaluation in result.rule_evaluations}
    assert expected_rule_ids <= evaluated_rule_ids
    if structure_id == STRUCTURE_007:
        assert RULE_IDS.isdisjoint(evaluated_rule_ids)
