from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.036"
APP = "ipcdo:TrademarkApplicationDetails"
DOC = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"


def _values():
    party = f"{APP}/ipcdo:IPPartyDetails"
    address = f"{party}/ccdo:SubjectAddressDetails"
    comm = f"{party}/ccdo:CommunicationDetails"
    trademark = f"{APP}/ipcdo:TrademarkDetails"
    description = f"{trademark}/ipcdo:TMDescriptionDetails"
    goods = f"{APP}/ipcdo:GoodsBaseDetails"
    return {
        "ccdo:EDocHeader": [None], "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002", "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000036",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00", APP: [None],
        f"{APP}/ipsdo:IPDocKindCode": "00036", f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-30", f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000036",
        party: [None], f"{party}/ipsdo:IPPartyKindCode": "AP", f"{party}/csdo:UnifiedCountryCode": "RU", f"{party}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3", f"{party}/ipsdo:IPSubjectName": "Заявитель", f"{party}/ipsdo:IPSubjectName/@nameRepresentationKindCode": "OR", f"{party}/ipsdo:IPSubjectName/@languageCode": "RU",
        address: [""], f"{address}/csdo:AddressKindCode": "2", f"{address}/csdo:UnifiedCountryCode": "RU", f"{address}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3", f"{address}/csdo:CityName": "Москва", f"{address}/csdo:StreetName": "Тестовая", f"{address}/csdo:BuildingNumberId": "1",
        comm: [""], f"{comm}/csdo:CommunicationChannelCode": "EM", f"{comm}/csdo:CommunicationChannelId": "applicant@example.test",
        trademark: [None], description: [""], f"{description}/csdo:DescriptionText": "Описание", f"{trademark}/ipsdo:TrademarkKindCode": "110", f"{trademark}/ipsdo:TrademarkKindName": "Словесный знак", f"{trademark}/ipsdo:CollectiveMarkIndicator": "0",
        goods: [None], f"{goods}/ipsdo:GoodsClassCode": "01", f"{goods}/ipsdo:GoodsClassName": "Класс 01", f"{goods}/ipsdo:GoodsName": "Товар",
        DOC: [None], f"{DOC}/ipsdo:IPDocKindCode": "00036", f"{DOC}/csdo:DocId": "DOC-036", f"{DOC}/csdo:DocCreationDate": "2026-09-30", f"{DOC}/csdo:DescriptionText": "Документ согласия", f"{DOC}/csdo:PageQuantity": "1", f"{DOC}/csdo:DocBinaryText": "QUJD",
        RESOURCE: [None], VALIDITY: [None], f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T14:01:00+03:00",
    }


def test_msg036_build_serialize_parse_extract_validate_roundtrip():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = _values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    extracted, extraction_issues = engine.body_provider._values_from_element(structure, parsed)
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    rebuilt = engine.build_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    reparsed = ET.fromstring(ET.tostring(rebuilt.serialize_xml_element(), encoding="utf-8"))
    reextracted, reissues = engine.body_provider._values_from_element(structure, reparsed)
    assert not extraction_issues
    assert not reissues
    assert validation.is_valid, [(item.rule_id, item.message) for item in validation.issues]
    assert validation.is_complete
    assert extracted == reextracted
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    assert "ipcdo:RefusalDetails" not in extracted
