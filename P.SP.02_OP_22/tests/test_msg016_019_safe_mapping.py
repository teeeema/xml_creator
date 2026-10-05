from copy import deepcopy
from pathlib import Path

import pytest

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
STRUCTURE = "R.IP.SP.02.007"
ROOT = "ipcdo:UnifiedRegisterRecordsDetails"
STATUS = f"{ROOT}/ipcdo:IPEntityStatusDetails"
PARTY = f"{ROOT}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{ROOT}/ipcdo:TrademarkDetails"
DESC = f"{TM}/ipcdo:TMDescriptionDetails"
ELEMENT = f"{DESC}/ipcdo:TMElementDetails"
GOODS = f"{ROOT}/ipcdo:GoodsBaseDetails"
DOC = f"{ROOT}/ipcdo:AccompanyingDocumentsDetails"
TRANSFORM = f"{ROOT}/ipcdo:TransformationDetails"
RESOURCE = f"{ROOT}/ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"

MESSAGES = ("P.SP.02.MSG.016", "P.SP.02.MSG.017", "P.SP.02.MSG.018", "P.SP.02.MSG.019")
TABLES = {
    "P.SP.02.MSG.016": "49",
    "P.SP.02.MSG.017": "50",
    "P.SP.02.MSG.018": "51",
    "P.SP.02.MSG.019": "52",
}
INHERITED_CORE = {str(number) for number in range(6, 18)}


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _rules(message):
    return _engine().rules[message].structured_rules


def _rules_for(message, rule_id):
    return [rule for rule in _rules(message) if rule["rule_id"] == rule_id]


def _status(message, rule_id, values):
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(rule, values).status for rule in _rules_for(message, rule_id)]


def _base(message):
    kinds = ["RH"]
    if message == "P.SP.02.MSG.017":
        kinds.append("UE")
    count = len(kinds)
    values = {
        ROOT: [None],
        f"{ROOT}/ipsdo:TrademarkId": "TM-1",
        f"{ROOT}/ipsdo:IPDocKindCode": "12345",
        STATUS: [None],
        f"{STATUS}/csdo:EventDate": "2026-09-24",
        f"{STATUS}/csdo:StatusCode": "05" if message == "P.SP.02.MSG.019" else "03",
        PARTY: [None] * count,
        f"{PARTY}/ipsdo:IPPartyKindCode": kinds,
        f"{PARTY}/csdo:UnifiedCountryCode": ["RU"] * count,
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": ["ВОИС ST.3"] * count,
        f"{PARTY}/ipsdo:IPSubjectName": ["Правообладатель"] * count,
        ADDRESS: [""] * count,
        f"{ADDRESS}/csdo:AddressKindCode": ["2"] * count,
        f"{ADDRESS}/csdo:UnifiedCountryCode": ["RU"] * count,
        f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId": ["ВОИС ST.3"] * count,
        f"{ADDRESS}/csdo:CityName": ["Москва"] * count,
        f"{ADDRESS}/csdo:StreetName": ["Тестовая"] * count,
        f"{ADDRESS}/csdo:BuildingNumberId": [str(i + 1) for i in range(count)],
        COMM: [""] * count,
        f"{COMM}/csdo:CommunicationChannelCode": ["EM"] * count,
        f"{COMM}/csdo:CommunicationChannelId": [f"u{i}@example.test" for i in range(count)],
        TM: [None],
        f"{TM}/ipsdo:TrademarkPicture": "IMAGE",
        f"{TM}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TM}/ipsdo:CollectiveMarkIndicator": "1" if message == "P.SP.02.MSG.017" else "0",
        DESC: "",
        f"{DESC}/csdo:DescriptionText": "Описание",
        ELEMENT: "",
        f"{ELEMENT}/ipsdo:TrademarkCFECode": "01.01.01",
        f"{ELEMENT}/csdo:DesignationName": "TEST",
        f"{ELEMENT}/ipsdo:TMLocalizedName": "TEST",
        f"{ELEMENT}/ipsdo:TMTransliterationName": "TEST",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        f"{GOODS}/ipsdo:TrademarkDecisionIndicator": True,
        f"{GOODS}/ipsdo:TrademarkApplicationId": "APP-1",
        RESOURCE: [None],
    }
    if message in {"P.SP.02.MSG.016", "P.SP.02.MSG.017"}:
        values[TRANSFORM] = [None]
        values[f"{TRANSFORM}/ipsdo:TransformationKindName"] = "Преобразование"
        values[f"{TRANSFORM}/ipsdo:IPObjectId"] = "TM-1"
        values[f"{TRANSFORM}/csdo:EventDate"] = "2026-09-24"
    if message == "P.SP.02.MSG.017":
        values[DOC] = [None]
    if message == "P.SP.02.MSG.018":
        values[VALIDITY] = [None]
        values[f"{VALIDITY}/csdo:StartDateTime"] = "2026-09-24T12:00:00+03:00"
    if message == "P.SP.02.MSG.019":
        values[VALIDITY] = [None]
        values[f"{VALIDITY}/csdo:EndDateTime"] = "2026-09-24T12:00:00+03:00"
    return values


@pytest.mark.parametrize("message", MESSAGES)
def test_mapping_scope_and_inherited_dual_provenance(message):
    rules = _rules(message)
    assert rules
    assert all(rule.get("applies_to_structure") == STRUCTURE for rule in rules)
    inherited = [rule for rule in rules if len(rule.get("source_refs", [])) == 2]
    inherited_items = {rule["source_refs"][1]["item"] for rule in inherited}
    assert INHERITED_CORE <= inherited_items
    table = TABLES[message]
    for rule in inherited:
        current, original = rule["source_refs"]
        assert current["source_id"] == f"22OP-RULE-{message}-T{table}-6-19"
        assert original["source_id"] == f"22OP-RULE-P.SP.02.MSG.003-T37-{original['item']}"


@pytest.mark.parametrize("message", MESSAGES)
def test_inherited_qname_selectors_are_scoped_under_register_record(message):
    inherited = [rule for rule in _rules(message) if len(rule.get("source_refs", [])) == 2]
    qname_rules = [rule for rule in inherited if "qname" in rule.get("selector", {})]
    assert qname_rules
    assert all(rule["selector"].get("under") == ROOT for rule in qname_rules)


@pytest.mark.parametrize("message", MESSAGES)
def test_req16_stays_partial_and_does_not_invent_conflicting_goods_class_code(message):
    table = TABLES[message]
    rules = _rules_for(message, f"{message}.T{table}.REQ.6_19")
    req16 = [rule for rule in rules if rule["source_refs"][1]["item"] == "16"]
    assert len(req16) == 2
    assert all(rule.get("mapping_status") == "PARTIAL" for rule in req16)
    assert all("GoodsClassCode" not in str(rule) for rule in req16)


@pytest.mark.parametrize("message", MESSAGES)
def test_all_mapped_rules_accept_representative_valid_values(message):
    evaluations = StructuredRuleEvaluator().evaluate_all(_rules(message), _base(message))
    failed = [(item.rule_id, item.status.value) for item in evaluations if item.status is not RuleStatus.PASS]
    assert evaluations and not failed, failed


@pytest.mark.parametrize("message", MESSAGES)
def test_req1_checks_local_trademark_id_only_and_is_partial(message):
    rule = _rules_for(message, f"{message}.REQ.1")
    assert len(rule) == 1 and rule[0].get("mapping_status") == "PARTIAL"
    assert _status(message, f"{message}.REQ.1", _base(message)) == [RuleStatus.PASS]
    invalid = _base(message)
    invalid.pop(f"{ROOT}/ipsdo:TrademarkId")
    assert _status(message, f"{message}.REQ.1", invalid) == [RuleStatus.FAIL]


@pytest.mark.parametrize("message", ("P.SP.02.MSG.016", "P.SP.02.MSG.017", "P.SP.02.MSG.019"))
def test_document_kind_conditions_use_only_top_level_record_fields(message):
    valid = _base(message)
    assert _status(message, f"{message}.REQ.4", valid) == [RuleStatus.PASS]
    invalid = deepcopy(valid)
    invalid[f"{ROOT}/ipsdo:IPDocKindName"] = "Не должно быть при коде"
    assert _status(message, f"{message}.REQ.4", invalid) == [RuleStatus.FAIL]


def test_msg018_document_kind_conditions_are_req20_21_and_exact_fallback_name():
    message = "P.SP.02.MSG.018"
    valid = _base(message)
    assert _status(message, f"{message}.REQ.20", valid) == [RuleStatus.PASS]
    fallback = deepcopy(valid)
    fallback.pop(f"{ROOT}/ipsdo:IPDocKindCode")
    fallback[f"{ROOT}/ipsdo:IPDocKindName"] = (
        "Заявление о внесении изменений в сведения Единого реестра товарных знаков, "
        "знаков обслуживания Евразийского экономического союза"
    )
    assert _status(message, f"{message}.REQ.21", fallback) == [RuleStatus.PASS]
    fallback[f"{ROOT}/ipsdo:IPDocKindName"] = "Другое наименование"
    assert _status(message, f"{message}.REQ.21", fallback) == [RuleStatus.FAIL]


def test_msg017_specializes_collective_mark_inherited_requirements():
    message = "P.SP.02.MSG.017"
    rules = _rules(message)
    inherited_18 = [rule for rule in rules if len(rule.get("source_refs", [])) == 2 and rule["source_refs"][1]["item"] == "18"]
    inherited_19 = [rule for rule in rules if len(rule.get("source_refs", [])) == 2 and rule["source_refs"][1]["item"] == "19"]
    assert len(inherited_18) == 1 and inherited_18[0]["kind"] == "selection_cardinality"
    assert inherited_18[0].get("mapping_status") == "INHERITED"
    assert len(inherited_19) == 1 and inherited_19[0]["kind"] == "selection_cardinality"
    assert inherited_19[0].get("mapping_status") == "PARTIAL"
    assert _status(message, f"{message}.REQ.21", _base(message)) == [RuleStatus.PASS]


@pytest.mark.parametrize("message", ("P.SP.02.MSG.018", "P.SP.02.MSG.019"))
def test_collective_mark_requirements_remain_conditional_partial_when_not_fixed_to_one(message):
    table = TABLES[message]
    inherited = [
        rule
        for rule in _rules_for(message, f"{message}.T{table}.REQ.6_19")
        if rule["source_refs"][1]["item"] in {"18", "19"}
    ]
    assert len(inherited) == 2
    assert all(rule["kind"] == "conditional_presence" for rule in inherited)
    assert all(rule.get("mapping_status") == "PARTIAL" for rule in inherited)


def test_msg016_does_not_map_collective_only_req18_19_because_indicator_is_fixed_zero():
    message = "P.SP.02.MSG.016"
    inherited_items = {
        rule["source_refs"][1]["item"]
        for rule in _rules(message)
        if len(rule.get("source_refs", [])) == 2
    }
    assert {"18", "19"}.isdisjoint(inherited_items)
    assert _status(message, f"{message}.REQ.21", _base(message)) == [RuleStatus.PASS]
