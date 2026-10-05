from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.005"
TRANSACTION = "P.SP.02.TRN.004"
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
PARTY_ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
PARTY_COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
TMDESC = f"{TM}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
CLAIM = f"{APP}/ipcdo:TrademarkClaimDetails"
STAKE = f"{CLAIM}/ipcdo:StakeholderDetails"
STAKE_ADDRESS = f"{STAKE}/ccdo:SubjectAddressDetails"
ARGUMENT = f"{APP}/ipcdo:ArgumentDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"


def _engine() -> EaeuXmlEngine:
    return EaeuXmlEngine.load_process(PACKAGE)


def _generation_values() -> dict[str, object]:
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000005",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-18T12:00:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-18",
        f"{APP}/ipsdo:TrademarkApplicationId": "APP-005",
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": "AP",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": "Заявитель",
        f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": "OR",
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": "RU",
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
        f"{STAKE_ADDRESS}/csdo:BuildingNumberId": "2",
        ARGUMENT: [""],
        f"{ARGUMENT}/csdo:DescriptionText": "Доводы заявителя",
        f"{ARGUMENT}/csdo:EventDate": "2026-09-18",
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-18T12:00:00+03:00",
    }


def _round_trip_and_validate(values):
    engine = _engine()
    body = engine.build_body(MESSAGE, values, mode=GenerationMode.TEST)
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    parsed = ET.fromstring(serialized)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    extracted, extraction_issues = engine.body_provider._values_from_element(structure, parsed)
    assert not extraction_issues
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    return engine, parsed, extracted, validation


def test_msg005_full_build_serialize_parse_structural_and_structured_validation_passes() -> None:
    engine, parsed, extracted, validation = _round_trip_and_validate(_generation_values())

    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.initiating_message == MESSAGE
    assert parsed.tag == f"{{{engine.get_structure(MESSAGE, mode=GenerationMode.TEST).namespace}}}TrademarkRegistrationDetails"
    assert extracted[f"{APP}/ipsdo:TrademarkApplicationId"] == "APP-005"
    assert extracted[f"{ARGUMENT}/csdo:DescriptionText"] == "Доводы заявителя"
    assert validation.is_valid, [(issue.code, issue.rule_id, issue.field_path, issue.message) for issue in validation.issues]
    assert validation.is_complete
    assert validation.rule_evaluations
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(f"/{MESSAGE}")


def test_msg005_representative_invalid_round_trip_fails_structured_validation() -> None:
    engine = _engine()
    body = engine.build_body(MESSAGE, _generation_values(), mode=GenerationMode.TEST)
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    parsed = ET.fromstring(serialized)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)

    kind_tag = f"{{{structure.imported_namespaces['ipsdo']}}}TrademarkKindCode"
    kind = next(element for element in parsed.iter() if element.tag == kind_tag)
    kind.text = "999"

    reparsed = ET.fromstring(ET.tostring(parsed, encoding="utf-8"))
    extracted, extraction_issues = engine.body_provider._values_from_element(structure, reparsed)
    assert not extraction_issues
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)

    assert not validation.is_valid
    assert any(
        issue.code == "STRUCTURED_RULE_FAILED" and issue.rule_id == "P.SP.02.MSG.005.T39.REQ.6_29"
        for issue in validation.issues
    )
    assert any(
        item.rule_id == "P.SP.02.MSG.005.T39.REQ.6_29" and item.status is RuleStatus.FAIL
        for item in validation.rule_evaluations
    )
