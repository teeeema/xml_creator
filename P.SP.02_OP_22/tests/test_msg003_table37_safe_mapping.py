from pathlib import Path

import pytest

from eaeu_xml.core.errors import BodyValidationError
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.003"
STRUCTURE_002 = "R.IP.SP.02.002"
STRUCTURE_007 = "R.IP.SP.02.007"

ROOT = "ipcdo:UnifiedRegisterRecordsDetails"
AUTHORITY = f"{ROOT}/ipcdo:PatentAuthorityDetails"
PARTY = f"{ROOT}/ipcdo:IPPartyDetails"
PARTY_ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
PARTY_COMMUNICATION = f"{PARTY}/ccdo:CommunicationDetails"
TRADEMARK = f"{ROOT}/ipcdo:TrademarkDetails"
DESCRIPTION = f"{TRADEMARK}/ipcdo:TMDescriptionDetails"
ELEMENT = f"{DESCRIPTION}/ipcdo:TMElementDetails"
GOODS = f"{ROOT}/ipcdo:GoodsBaseDetails"
STATUS = f"{ROOT}/ipcdo:IPEntityStatusDetails"
RESOURCE_STATUS = f"{ROOT}/ccdo:ResourceItemStatusDetails"
RESOURCE_VALIDITY = f"{RESOURCE_STATUS}/ccdo:ValidityPeriodDetails"

FULL_IDS = {
    "P.SP.02.MSG.003.T37.REQ.1",
    "P.SP.02.MSG.003.T37.REQ.2",
    "P.SP.02.MSG.003.T37.REQ.6",
    "P.SP.02.MSG.003.T37.REQ.7",
    "P.SP.02.MSG.003.T37.REQ.8",
    "P.SP.02.MSG.003.T37.REQ.9",
    "P.SP.02.MSG.003.T37.REQ.10",
    "P.SP.02.MSG.003.T37.REQ.11",
    "P.SP.02.MSG.003.T37.REQ.12",
    "P.SP.02.MSG.003.T37.REQ.13",
    "P.SP.02.MSG.003.T37.REQ.14",
    "P.SP.02.MSG.003.T37.REQ.15",
    "P.SP.02.MSG.003.T37.REQ.17",
    "P.SP.02.MSG.003.T37.REQ.20",
    "P.SP.02.MSG.003.T37.REQ.21",
    "P.SP.02.MSG.003.T37.REQ.22",
}
PARTIAL_IDS = {
    "P.SP.02.MSG.003.T37.REQ.3",
    "P.SP.02.MSG.003.T37.REQ.16",
}
SKIPPED_IDS = {
    "P.SP.02.MSG.003.T37.REQ.4",
    "P.SP.02.MSG.003.T37.REQ.5",
    "P.SP.02.MSG.003.T37.REQ.18",
    "P.SP.02.MSG.003.T37.REQ.19",
}
TABLE36_IDS = {
    "P.SP.02.MSG.003.T36.REQ.1",
    "P.SP.02.MSG.003.T36.REQ.2",
    "P.SP.02.MSG.003.T36.REQ.5",
    "P.SP.02.MSG.003.T36.REQ.6_29",
    "P.SP.02.MSG.003.T36.REQ.30",
    "P.SP.02.MSG.003.T36.REQ.31",
    "P.SP.02.MSG.003.T36.REQ.32",
    "P.SP.02.MSG.003.T36.REQ.33",
}


def _engine() -> EaeuXmlEngine:
    return EaeuXmlEngine.load_process(PACKAGE)


def _rules():
    return _engine().rules[MESSAGE].structured_rules


def _rules_for(rule_id: str):
    return [rule for rule in _rules() if rule["rule_id"] == rule_id]


def _statuses(rule_id: str, values: dict[str, object]) -> list[RuleStatus]:
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(rule, values).status for rule in _rules_for(rule_id)]


def _assert_pass(rule_id: str, values: dict[str, object]) -> None:
    statuses = _statuses(rule_id, values)
    assert statuses
    assert all(status is RuleStatus.PASS for status in statuses)


def _assert_fail(rule_id: str, values: dict[str, object]) -> None:
    statuses = _statuses(rule_id, values)
    assert statuses
    assert RuleStatus.FAIL in statuses


def _full_cases():
    address_valid = {
        PARTY_ADDRESS: [None],
        f"{PARTY_ADDRESS}/csdo:AddressKindCode": "2",
        f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY_ADDRESS}/csdo:CityName": "Москва",
        f"{PARTY_ADDRESS}/csdo:StreetName": "Тестовая",
        f"{PARTY_ADDRESS}/csdo:BuildingNumberId": "1",
    }
    communication_valid = {
        PARTY_COMMUNICATION: [None],
        f"{PARTY_COMMUNICATION}/csdo:CommunicationChannelCode": "EM",
        f"{PARTY_COMMUNICATION}/csdo:CommunicationChannelId": "test@example.test",
    }
    description_valid = {
        DESCRIPTION: [None],
        f"{DESCRIPTION}/csdo:DescriptionText": "Описание",
        ELEMENT: "",
        f"{ELEMENT}/ipsdo:TrademarkCFECode": "01.01.01",
        f"{ELEMENT}/csdo:DesignationName": "TEST",
        f"{ELEMENT}/ipsdo:TMLocalizedName": "TEST",
        f"{ELEMENT}/ipsdo:TMTransliterationName": "TEST",
    }
    return [
        (
            "P.SP.02.MSG.003.T37.REQ.1",
            {ROOT: [None], f"{ROOT}/ipsdo:RegistrationDate": "2026-09-18", f"{ROOT}/csdo:DocValidityDate": "2027-09-18"},
            {ROOT: [None], f"{ROOT}/csdo:DocValidityDate": "2027-09-18"},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.2",
            {ROOT: [None], f"{ROOT}/ipsdo:TrademarkApplicationId": "2026/RU-000001"},
            {ROOT: [None]},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.6",
            {f"{PARTY}/csdo:UnifiedCountryCode": "RU", f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3"},
            {f"{PARTY}/csdo:UnifiedCountryCode": "RU", f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "OTHER"},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.7",
            address_valid,
            {key: value for key, value in address_valid.items() if not key.endswith("/csdo:CityName")},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.8",
            communication_valid,
            {**communication_valid, f"{PARTY_COMMUNICATION}/csdo:CommunicationChannelName": "Email"},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.9",
            {PARTY_COMMUNICATION: [None], f"{PARTY_COMMUNICATION}/csdo:CommunicationChannelCode": "EM"},
            {PARTY_COMMUNICATION: [None], f"{PARTY_COMMUNICATION}/csdo:CommunicationChannelCode": "XX"},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.10",
            {
                AUTHORITY: [None],
                f"{AUTHORITY}/csdo:UnifiedCountryCode": "RU",
                f"{AUTHORITY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
                f"{AUTHORITY}/csdo:AuthorityName": "Роспатент",
                f"{AUTHORITY}/csdo:AuthorityBriefName": "Роспатент",
            },
            {
                AUTHORITY: [None],
                f"{AUTHORITY}/csdo:UnifiedCountryCode": "RU",
                f"{AUTHORITY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
                f"{AUTHORITY}/csdo:AuthorityName": "Роспатент",
            },
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.11",
            {PARTY: [None], f"{PARTY}/ipsdo:IPPartyKindCode": "RH"},
            {PARTY: [None, None], f"{PARTY}/ipsdo:IPPartyKindCode": ["RH", "RH"]},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.12",
            {
                PARTY: [None],
                f"{PARTY}/csdo:UnifiedCountryCode": "RU",
                f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
                f"{PARTY}/ipsdo:IPSubjectName": "Правообладатель",
                PARTY_ADDRESS: "",
                f"{PARTY_ADDRESS}/csdo:AddressKindCode": "2",
                PARTY_COMMUNICATION: "",
                f"{PARTY_COMMUNICATION}/csdo:CommunicationChannelId": "test@example.test",
            },
            {
                PARTY: [None],
                f"{PARTY}/csdo:UnifiedCountryCode": "RU",
                f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
                f"{PARTY}/ipsdo:IPSubjectName": "Правообладатель",
                PARTY_ADDRESS: "",
                f"{PARTY_ADDRESS}/csdo:AddressKindCode": "2",
            },
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.13",
            {PARTY_ADDRESS: [None], f"{PARTY_ADDRESS}/csdo:AddressKindCode": "2"},
            {PARTY_ADDRESS: [None], f"{PARTY_ADDRESS}/csdo:AddressKindCode": "3"},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.14",
            {
                TRADEMARK: [None],
                f"{TRADEMARK}/ipsdo:TrademarkPicture": "IMAGE",
                f"{TRADEMARK}/ipsdo:TrademarkKindName": "Словесный",
                f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "0",
                DESCRIPTION: "",
                f"{DESCRIPTION}/csdo:DescriptionText": "Описание",
            },
            {
                TRADEMARK: [None],
                f"{TRADEMARK}/ipsdo:TrademarkPicture": "IMAGE",
                f"{TRADEMARK}/ipsdo:TrademarkKindName": "Словесный",
                f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "0",
            },
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.15",
            description_valid,
            {key: value for key, value in description_valid.items() if not key.endswith("/ipsdo:TrademarkCFECode")},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.17",
            {GOODS: [None], f"{GOODS}/ipsdo:GoodsName": "Товар"},
            {GOODS: [None], f"{GOODS}/ipsdo:TrademarkId": "2026/RU-000001"},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.20",
            {STATUS: [None], f"{STATUS}/csdo:EventDate": "2026-09-18", f"{STATUS}/csdo:StatusCode": "01"},
            {STATUS: [None], f"{STATUS}/csdo:EventDate": "2026-09-18", f"{STATUS}/csdo:StatusCode": "20"},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.21",
            {},
            {f"{ROOT}/ipsdo:TechnicalErrorText": "Ошибка"},
        ),
        (
            "P.SP.02.MSG.003.T37.REQ.22",
            {RESOURCE_STATUS: [None], RESOURCE_VALIDITY: [None], f"{RESOURCE_VALIDITY}/csdo:StartDateTime": "2026-09-18T12:00:00+03:00"},
            {RESOURCE_STATUS: [None], RESOURCE_VALIDITY: [None]},
        ),
    ]


@pytest.mark.parametrize(("rule_id", "valid", "invalid"), _full_cases())
def test_each_full_table37_rule_has_pass_and_fail(rule_id, valid, invalid) -> None:
    _assert_pass(rule_id, valid)
    _assert_fail(rule_id, invalid)


def test_table37_mapping_scope_provenance_and_skips() -> None:
    engine = _engine()
    captured = {rule["rule_id"]: rule for rule in engine.rules[MESSAGE].business_rules}
    mapped = [rule for rule in engine.rules[MESSAGE].structured_rules if ".T37." in rule["rule_id"]]
    mapped_ids = {rule["rule_id"] for rule in mapped}

    assert mapped_ids == FULL_IDS | PARTIAL_IDS
    assert SKIPPED_IDS.isdisjoint(mapped_ids)
    assert all(rule["applies_to_structure"] == STRUCTURE_007 for rule in mapped)
    for rule in mapped:
        assert rule["source_refs"] == captured[rule["rule_id"]]["source_refs"]


def test_table37_selectors_and_relative_qnames_exist_in_007_structure() -> None:
    structure = _engine().resolve_structure(STRUCTURE_007, mode=GenerationMode.TEST).definition
    paths = {field.path for field in structure.fields}
    qnames = {
        f"{field.namespace_prefix}:{field.xml_name}"
        for field in structure.fields
        if field.namespace_prefix and field.xml_name
    }

    for rule in [item for item in _rules() if ".T37." in item["rule_id"]]:
        selector = rule["selector"]
        if "collection" in selector:
            base_paths = [selector["collection"]]
            assert selector["collection"] in paths
        else:
            assert selector["qname"] in qnames
            base_paths = [path for path in paths if path.split("/")[-1] == selector["qname"]]
            assert base_paths

        where = selector.get("where")
        if where:
            assert any(f"{base}/{where['field']}" in paths for base in base_paths)

        for assertion in rule.get("assertions", []):
            operand = assertion.get("target") or assertion.get("left")
            if not isinstance(operand, dict) or "field" not in operand:
                continue
            relative = operand["field"]
            assert any(f"{base}/{relative}" in paths for base in base_paths), (rule["rule_id"], relative)


def test_req3_partial_checks_only_direct_trademark_id_and_no_external_lookup() -> None:
    rule_id = "P.SP.02.MSG.003.T37.REQ.3"
    rules = _rules_for(rule_id)
    assert len(rules) == 1
    rule = rules[0]
    assert rule["mapping_status"] == "PARTIAL"
    assert rule["selector"] == {"collection": ROOT}
    assert rule["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:TrademarkId"}, "state": "REQUIRED"}
    ]
    assert "evaluation_status" not in rule

    valid = {ROOT: [None], f"{ROOT}/ipsdo:TrademarkId": "2026/RU-000001", "external:TrademarkId": "2026/RU-000001"}
    _assert_pass(rule_id, valid)
    _assert_fail(rule_id, {ROOT: [None]})


def test_req16_partial_checks_only_confirmed_local_goods_fields() -> None:
    rule_id = "P.SP.02.MSG.003.T37.REQ.16"
    rules = _rules_for(rule_id)
    assert len(rules) == 2
    assert all(rule["mapping_status"] == "PARTIAL" for rule in rules)
    assert all("GoodsClassCode" not in str(rule) for rule in rules)

    valid = {
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        f"{GOODS}/ipsdo:TrademarkDecisionIndicator": "1",
        f"{GOODS}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
    }
    _assert_pass(rule_id, valid)

    invalid = dict(valid)
    invalid.pop(f"{GOODS}/ipsdo:GoodsName")
    _assert_fail(rule_id, invalid)


def test_req16_does_not_check_source_conflict_goods_class_code() -> None:
    values = {
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        f"{GOODS}/ipsdo:TrademarkDecisionIndicator": "1",
        f"{GOODS}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
        f"{GOODS}/ipsdo:GoodsClassCode": None,
    }
    _assert_pass("P.SP.02.MSG.003.T37.REQ.16", values)


def test_repeatable_goods_rejects_one_invalid_instance() -> None:
    values = {
        GOODS: [None, None],
        f"{GOODS}/ipsdo:GoodsClassName": ["Класс 01", "Класс 02"],
        f"{GOODS}/ipsdo:GoodsName": ["Товар 1", None],
        f"{GOODS}/ipsdo:TrademarkDecisionIndicator": ["1", "1"],
        f"{GOODS}/ipsdo:TrademarkApplicationId": ["2026/RU-000001", "2026/RU-000002"],
    }
    _assert_fail("P.SP.02.MSG.003.T37.REQ.16", values)
    values[f"{GOODS}/ipsdo:GoodsName"] = ["Товар 1", "Товар 2"]
    _assert_pass("P.SP.02.MSG.003.T37.REQ.16", values)


def test_repeatable_addresses_reject_one_wrong_instance() -> None:
    values = {
        PARTY_ADDRESS: [None, None],
        f"{PARTY_ADDRESS}/csdo:AddressKindCode": ["2", "3"],
    }
    _assert_fail("P.SP.02.MSG.003.T37.REQ.13", values)
    values[f"{PARTY_ADDRESS}/csdo:AddressKindCode"] = ["2", "2"]
    _assert_pass("P.SP.02.MSG.003.T37.REQ.13", values)


def test_generic_country_rule_rejects_one_wrong_instance() -> None:
    country = f"{PARTY}/csdo:UnifiedCountryCode"
    values = {country: ["RU", "BY"], f"{country}/@codeListId": ["ВОИС ST.3", "OTHER"]}
    _assert_fail("P.SP.02.MSG.003.T37.REQ.6", values)
    values[f"{country}/@codeListId"] = ["ВОИС ST.3", "ВОИС ST.3"]
    _assert_pass("P.SP.02.MSG.003.T37.REQ.6", values)


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


def _embedded_007_values(structure):
    values = _minimal_values(structure)
    values.update(
        {
            f"{ROOT}/ipsdo:RegistrationDate": "2026-09-18",
            f"{ROOT}/csdo:DocValidityDate": "2027-09-18",
            f"{ROOT}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
            f"{ROOT}/ipsdo:TrademarkId": "2026/RU-000001",
            PARTY: None,
            f"{PARTY}/ipsdo:IPPartyKindCode": "RH",
            f"{PARTY}/csdo:UnifiedCountryCode": "RU",
            f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            f"{PARTY}/ipsdo:IPSubjectName": "Правообладатель",
            PARTY_ADDRESS: None,
            f"{PARTY_ADDRESS}/csdo:AddressKindCode": "2",
            f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode": "RU",
            f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            f"{PARTY_ADDRESS}/csdo:CityName": "Москва",
            f"{PARTY_ADDRESS}/csdo:StreetName": "Тестовая",
            f"{PARTY_ADDRESS}/csdo:BuildingNumberId": "1",
            PARTY_COMMUNICATION: None,
            f"{PARTY_COMMUNICATION}/csdo:CommunicationChannelCode": "EM",
            f"{PARTY_COMMUNICATION}/csdo:CommunicationChannelId": "test@example.test",
            GOODS: None,
            f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
            f"{GOODS}/ipsdo:GoodsName": "Товар",
            f"{GOODS}/ipsdo:TrademarkDecisionIndicator": True,
            f"{GOODS}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
            RESOURCE_VALIDITY: None,
            f"{RESOURCE_VALIDITY}/csdo:StartDateTime": "2026-09-18T12:00:00+03:00",
        }
    )
    return values


def _embedded_002_values(structure):
    values = _minimal_values(structure)
    app = "ipcdo:TrademarkApplicationDetails"
    trademark = f"{app}/ipcdo:TrademarkDetails"
    goods = f"{app}/ipcdo:GoodsBaseDetails"
    values.update(
        {
            f"{app}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
            f"{app}/ipsdo:ApplicationReceiptDate": "2026-09-18",
            trademark: None,
            f"{trademark}/ipcdo:TMDescriptionDetails": None,
            f"{trademark}/ipcdo:TMDescriptionDetails/csdo:DescriptionText": "TEST",
            f"{trademark}/ipsdo:TrademarkKindCode": "110",
            f"{trademark}/ipsdo:TrademarkKindName": "TEST",
            f"{trademark}/ipsdo:CollectiveMarkIndicator": "1",
            goods: None,
            f"{goods}/ipsdo:GoodsClassCode": "01",
            f"{goods}/ipsdo:GoodsClassName": "TEST",
            f"{goods}/ipsdo:GoodsName": "TEST",
            f"{goods}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
            f"{goods}/ipsdo:TrademarkRegRefusalReasonText": "TEST",
            "ipcdo:RefusalDetails": None,
            "ipcdo:RefusalDetails/csdo:EventDate": "2026-09-18",
            "ipcdo:RefusalDetails/csdo:DescriptionText": "TEST",
            "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails": None,
            "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime": "2026-09-18T12:00:00+03:00",
        }
    )
    return values


def _build_and_validate(structure_id: str, embedded_values: dict[str, object]):
    engine = _engine()
    container = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    container_values = _minimal_values(container)
    try:
        body = engine.build_body(
            MESSAGE,
            container_values,
            mode=GenerationMode.TEST,
            embedded_structure_id=structure_id,
            embedded_values=embedded_values,
        )
    except BodyValidationError as error:
        pytest.fail(
            str([(issue.code, issue.field_path, issue.rule_id, issue.message) for issue in error.issues])
        )
    payload = list(body.serialize_xml_element())[-1]
    validation_values = dict(container_values)
    validation_values["*"] = payload
    return engine, container, payload, engine.validate_body(MESSAGE, validation_values, mode=GenerationMode.TEST)


def test_007_roundtrip_preserves_required_party_paths() -> None:
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE_007, mode=GenerationMode.TEST).definition
    values = _embedded_007_values(structure)
    element = engine.body_provider._serialize(structure, values)
    extracted, issues = engine.body_provider._values_from_element(structure, element)

    assert not issues
    for path in (
        PARTY,
        f"{PARTY}/csdo:UnifiedCountryCode",
        f"{PARTY}/ipsdo:IPSubjectName",
        PARTY_ADDRESS,
        f"{PARTY_ADDRESS}/csdo:AddressKindCode",
        f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode",
        f"{PARTY_ADDRESS}/csdo:CityName",
        f"{PARTY_ADDRESS}/csdo:StreetName",
        f"{PARTY_ADDRESS}/csdo:BuildingNumberId",
        PARTY_COMMUNICATION,
        f"{PARTY_COMMUNICATION}/csdo:CommunicationChannelId",
    ):
        assert path in extracted, (path, extracted)

    evaluator = StructuredRuleEvaluator()
    req7 = _rules_for("P.SP.02.MSG.003.T37.REQ.7")[0]
    req8 = _rules_for("P.SP.02.MSG.003.T37.REQ.8")[0]
    assert evaluator.select(req7["selector"], extracted, all=True) == [
        {
            "#text": "",
            "csdo:AddressKindCode": "2",
            "csdo:UnifiedCountryCode": "RU",
            "csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            "csdo:CityName": "Москва",
            "csdo:StreetName": "Тестовая",
            "csdo:BuildingNumberId": "1",
        }
    ]
    assert evaluator.select(req8["selector"], extracted, all=True) == [
        {
            "#text": "",
            "csdo:CommunicationChannelCode": "EM",
            "csdo:CommunicationChannelId": "test@example.test",
        }
    ]


def test_end_to_end_msg003_r010_to_007_executes_table37() -> None:
    engine = _engine()
    embedded = engine.resolve_structure(STRUCTURE_007, mode=GenerationMode.TEST).definition
    engine, container, payload, result = _build_and_validate(STRUCTURE_007, _embedded_007_values(embedded))

    assert container.structure_id == "R.010"
    assert payload.tag == f"{{{embedded.namespace}}}{embedded.root_element}"
    assert result.is_valid, [(issue.code, issue.field_path, issue.rule_id, issue.message) for issue in result.issues]
    evaluated = {item.rule_id for item in result.rule_evaluations}
    assert FULL_IDS | PARTIAL_IDS <= evaluated
    assert TABLE36_IDS.isdisjoint(evaluated)


def test_table37_is_excluded_from_002_and_table36_still_executes() -> None:
    engine = _engine()
    embedded = engine.resolve_structure(STRUCTURE_002, mode=GenerationMode.TEST).definition
    _, _, _, result = _build_and_validate(STRUCTURE_002, _embedded_002_values(embedded))

    assert result.is_valid, [(issue.code, issue.field_path, issue.rule_id, issue.message) for issue in result.issues]
    evaluated = {item.rule_id for item in result.rule_evaluations}
    assert (FULL_IDS | PARTIAL_IDS).isdisjoint(evaluated)
    assert TABLE36_IDS <= evaluated
