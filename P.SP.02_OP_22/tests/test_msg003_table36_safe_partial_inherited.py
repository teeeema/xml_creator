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
PATENT_AUTHORITY = f"{APP}/ipcdo:PatentAuthorityDetails"
PATENT_AUTHORITY_ADDRESS = f"{PATENT_AUTHORITY}/ccdo:SubjectAddressDetails"
ADDRESS = f"{APP}/ipcdo:CorrespondenceAddressDetails/ccdo:SubjectAddressDetails"
COMMUNICATION = f"{APP}/ipcdo:CorrespondenceAddressDetails/ccdo:CommunicationDetails"
TRADEMARK = f"{APP}/ipcdo:TrademarkDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
NESTED_ACCOMPANYING = (
    f"{APP}/ipcdo:NamingAbilityProofDetails/ipcdo:ProofDocTextDetails/"
    "ipcdo:AccompanyingDocumentsDetails"
)

REQ1 = "P.SP.02.MSG.003.T36.REQ.1"
REQ6_29 = "P.SP.02.MSG.003.T36.REQ.6_29"
REQ30 = "P.SP.02.MSG.003.T36.REQ.30"
REQ32 = "P.SP.02.MSG.003.T36.REQ.32"
NEW_RULE_IDS = {REQ1, REQ6_29, REQ30, REQ32}
INHERITED_ITEMS = {"6", "7", "8", "9", "10", "11", "12", "23", "24", "25", "28", "29"}


def _engine() -> EaeuXmlEngine:
    return EaeuXmlEngine.load_process(PACKAGE)


def _rules():
    return _engine().rules[MESSAGE].structured_rules


def _rule(rule_id: str):
    matches = [rule for rule in _rules() if rule["rule_id"] == rule_id]
    assert len(matches) == 1
    return matches[0]


def _rules_for_id(rule_id: str):
    return [rule for rule in _rules() if rule["rule_id"] == rule_id]


def _table34_item(rule) -> str | None:
    for ref in rule.get("source_refs", []):
        if ref.get("table") == "34":
            return ref.get("item")
    return None


def _inherited_rules(item: str):
    return [
        rule
        for rule in _rules()
        if rule["rule_id"] == REQ6_29 and _table34_item(rule) == item
    ]


def _evaluate(rule, values: dict[str, object]) -> RuleStatus:
    return StructuredRuleEvaluator().evaluate(rule, values).status


def _inherited_statuses(item: str, values: dict[str, object]) -> list[RuleStatus]:
    return [_evaluate(rule, values) for rule in _inherited_rules(item)]


def _valid_inherited_values() -> dict[str, object]:
    return {
        APP: [None],
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-18",
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
        f"{TRADEMARK}/ipsdo:TrademarkKindCode": "110",
        f"{TRADEMARK}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "1",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "01",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
    }


def _semantic(rule):
    ignored = {"rule_id", "mapping_status", "applies_to_structure", "source_refs"}
    return {key: value for key, value in rule.items() if key not in ignored}


def test_req1_partial_requires_only_application_id() -> None:
    rule = _rule(REQ1)
    assert rule["mapping_status"] == "PARTIAL"
    assert rule["applies_to_structure"] == STRUCTURE_002
    assert rule["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ipsdo:TrademarkApplicationId"},
            "state": "REQUIRED",
        }
    ]

    valid = {APP: [None], f"{APP}/ipsdo:TrademarkApplicationId": "APP-001"}
    assert _evaluate(rule, valid) is RuleStatus.PASS
    assert _evaluate(rule, {APP: [None]}) is RuleStatus.FAIL


def test_inherited_rules_preserve_table34_semantics_and_dual_provenance() -> None:
    engine = _engine()
    inherited = [rule for rule in engine.rules[MESSAGE].structured_rules if rule["rule_id"] == REQ6_29]
    assert {_table34_item(rule) for rule in inherited} == INHERITED_ITEMS

    for item in sorted(INHERITED_ITEMS, key=int):
        inherited_for_item = _inherited_rules(item)
        originals = [
            rule
            for rule in engine.rules["P.SP.02.MSG.001"].structured_rules
            if rule["rule_id"] == f"P.SP.02.MSG.001.REQ.{int(item):03d}"
        ]
        assert [_semantic(rule) for rule in inherited_for_item] == [_semantic(rule) for rule in originals]
        for rule in inherited_for_item:
            assert rule["mapping_status"] == "INHERITED"
            assert rule["applies_to_structure"] == STRUCTURE_002
            assert [ref["table"] for ref in rule["source_refs"]] == ["36", "34"]
            assert rule["source_refs"][0]["item"] == "6-29"
            assert rule["source_refs"][1]["item"] == item


def test_all_inherited_safe_fragments_pass_for_valid_values() -> None:
    values = _valid_inherited_values()
    rules = [rule for rule in _rules() if rule["rule_id"] == REQ6_29]
    assert rules
    assert all(_evaluate(rule, values) is RuleStatus.PASS for rule in rules)


@pytest.mark.parametrize(
    ("item", "path", "value", "remove"),
    [
        ("6", f"{APP}/ipsdo:ApplicationReceiptDate", None, True),
        ("7", f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId", "OTHER", False),
        ("8", f"{ADDRESS}/csdo:CityName", None, True),
        ("9", f"{COMMUNICATION}/csdo:CommunicationChannelName", "Email", False),
        ("10", f"{COMMUNICATION}/csdo:CommunicationChannelCode", "XX", False),
        ("11", f"{PATENT_AUTHORITY}/csdo:UnifiedCountryCode", None, True),
        ("12", f"{PATENT_AUTHORITY_ADDRESS}/csdo:AddressKindCode", "3", False),
        ("23", f"{ADDRESS}/csdo:AddressKindCode", "2", False),
        ("24", f"{ADDRESS}/csdo:UnifiedCountryCode", "US", False),
        ("25", f"{TRADEMARK}/ipsdo:TrademarkKindName", None, True),
        ("28", f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator", "true", False),
        ("29", f"{GOODS}/ipsdo:GoodsClassName", None, True),
    ],
)
def test_each_inherited_safe_requirement_has_a_failing_case(item, path, value, remove) -> None:
    values = _valid_inherited_values()
    if remove:
        values.pop(path)
    else:
        values[path] = value
    assert RuleStatus.FAIL in _inherited_statuses(item, values)


def test_inherited_req29_rejects_one_bad_repeatable_goods_instance() -> None:
    values = _valid_inherited_values()
    values[GOODS] = [None, None]
    values[f"{GOODS}/ipsdo:GoodsClassCode"] = ["01", "02"]
    values[f"{GOODS}/ipsdo:GoodsClassName"] = ["Класс 01", None]
    values[f"{GOODS}/ipsdo:GoodsName"] = ["Товар 1", "Товар 2"]
    assert RuleStatus.FAIL in _inherited_statuses("29", values)

    values[f"{GOODS}/ipsdo:GoodsClassName"] = ["Класс 01", "Класс 02"]
    assert all(status is RuleStatus.PASS for status in _inherited_statuses("29", values))


def test_req30_partial_checks_only_two_confirmed_goods_fields() -> None:
    rule = _rule(REQ30)
    assert rule["mapping_status"] == "PARTIAL"
    assert {assertion["target"]["field"] for assertion in rule["assertions"]} == {
        "ipsdo:TrademarkApplicationId",
        "ipsdo:TrademarkRegRefusalReasonText",
    }

    valid = {
        GOODS: [None, None],
        f"{GOODS}/ipsdo:TrademarkApplicationId": ["APP-1", "APP-2"],
        f"{GOODS}/ipsdo:TrademarkRegRefusalReasonText": ["Причина 1", "Причина 2"],
        f"{APP}/ipsdo:InconsistencyText": "Поле существует вне GoodsBaseDetails",
    }
    assert _evaluate(rule, valid) is RuleStatus.PASS

    invalid = dict(valid)
    invalid[f"{GOODS}/ipsdo:TrademarkRegRefusalReasonText"] = ["Причина 1", None]
    assert _evaluate(rule, invalid) is RuleStatus.FAIL


@pytest.mark.parametrize(
    "forbidden_field",
    [
        "ipcdo:TrademarkNationalApplicationDetails",
        "ipcdo:ApplicantChangeDetails",
        "ipcdo:TrademarkClaimDetails",
        "ipcdo:ComplaintDetails",
        "ipcdo:AccompanyingDocumentsDetails",
    ],
)
def test_req32_forbids_only_direct_children(forbidden_field: str) -> None:
    rules = _rules_for_id(REQ32)
    assert len(rules) == 5
    assert all(rule["mapping_status"] == "PARTIAL" for rule in rules)
    values = {f"{APP}/{forbidden_field}": [None]}
    statuses = [_evaluate(rule, values) for rule in rules]
    assert statuses.count(RuleStatus.FAIL) == 1


def test_req32_nested_accompanying_document_is_not_a_false_positive() -> None:
    rules = _rules_for_id(REQ32)
    direct_paths = {rule["selector"]["collection"] for rule in rules}
    assert all("DecisionOnComplaintText" not in path for path in direct_paths)
    assert direct_paths == {
        f"{APP}/ipcdo:TrademarkNationalApplicationDetails",
        f"{APP}/ipcdo:ApplicantChangeDetails",
        f"{APP}/ipcdo:TrademarkClaimDetails",
        f"{APP}/ipcdo:ComplaintDetails",
        f"{APP}/ipcdo:AccompanyingDocumentsDetails",
    }
    values = {NESTED_ACCOMPANYING: [None]}
    assert all(_evaluate(rule, values) is RuleStatus.PASS for rule in rules)


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
        values["ipcdo:RefusalDetails"] = None
        values["ipcdo:RefusalDetails/csdo:EventDate"] = "2026-09-18"
        values["ipcdo:RefusalDetails/csdo:DescriptionText"] = "TEST"
        validity = "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails"
        values[validity] = None
        values[f"{validity}/csdo:EndDateTime"] = "2026-09-18T12:00:00+03:00"
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


@pytest.mark.parametrize("structure_id", [STRUCTURE_002, STRUCTURE_007])
def test_new_table36_rules_execute_only_for_embedded_002(structure_id: str) -> None:
    engine = _engine()
    new_rules = [rule for rule in engine.rules[MESSAGE].structured_rules if rule["rule_id"] in NEW_RULE_IDS]
    assert new_rules
    assert all(rule["applies_to_structure"] == STRUCTURE_002 for rule in new_rules)

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
    evaluated = {evaluation.rule_id for evaluation in result.rule_evaluations}

    if structure_id == STRUCTURE_002:
        assert NEW_RULE_IDS <= evaluated
    else:
        assert NEW_RULE_IDS.isdisjoint(evaluated)
