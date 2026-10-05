from pathlib import Path
from xml.etree import ElementTree as ET
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.038"
APP = "ipcdo:TrademarkApplicationDetails"

def values():
    party = f"{APP}/ipcdo:IPPartyDetails"
    address = f"{party}/ccdo:SubjectAddressDetails"
    communication = f"{party}/ccdo:CommunicationDetails"
    trademark = f"{APP}/ipcdo:TrademarkDetails"
    description = f"{trademark}/ipcdo:TMDescriptionDetails"
    goods = f"{APP}/ipcdo:GoodsBaseDetails"
    document = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
    naming = f"{APP}/ipcdo:NamingAbilityProofDetails"
    proof = f"{naming}/ipcdo:ProofDocTextDetails"
    nested_document = f"{proof}/ipcdo:AccompanyingDocumentsDetails"
    signature = f"{APP}/ipcdo:SignatureDetails"
    officer = f"{signature}/ipcdo:OfficerDetails"
    officer_name = f"{officer}/ccdo:FullNameDetails"
    validity = "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails"
    priority = f"{APP}/ipcdo:TrademarkPriorityDetails"
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000038",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:IPDocKindName": "Документ, подтверждающий приоритет товарного знака",
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-30",
        f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000038",
        party: [None],
        f"{party}/ipsdo:IPPartyKindCode": "AP",
        f"{party}/csdo:UnifiedCountryCode": "RU",
        f"{party}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{party}/ipsdo:IPSubjectName": "Заявитель",
        address: [""],
        f"{address}/csdo:AddressKindCode": "2",
        f"{address}/csdo:UnifiedCountryCode": "RU",
        f"{address}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{address}/csdo:CityName": "Москва",
        f"{address}/csdo:StreetName": "Тестовая",
        f"{address}/csdo:BuildingNumberId": "1",
        communication: [""],
        f"{communication}/csdo:CommunicationChannelCode": "EM",
        f"{communication}/csdo:CommunicationChannelId": "applicant@example.test",
        trademark: [None], description: [""],
        f"{description}/csdo:DescriptionText": "Описание товарного знака",
        f"{trademark}/ipsdo:TrademarkKindCode": "110",
        f"{trademark}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{trademark}/ipsdo:CollectiveMarkIndicator": "0",
        goods: [None],
        f"{goods}/ipsdo:GoodsClassCode": "01", f"{goods}/ipsdo:GoodsClassName": "Класс 01", f"{goods}/ipsdo:GoodsName": "Товар",
        document: [None],
        f"{document}/ipsdo:IPDocKindCode": "00038", f"{document}/csdo:DocName": "Документ",
        f"{document}/csdo:DocId": "DOC-038", f"{document}/csdo:DocCreationDate": "2026-09-30",
        f"{document}/csdo:DescriptionText": "Основной прилагаемый документ", f"{document}/csdo:PageQuantity": "1", f"{document}/csdo:DocBinaryText": "QUJD",
        naming: [None], f"{naming}/ipsdo:ProofKindCode": "01", proof: [None], nested_document: [None],
        f"{nested_document}/ipsdo:IPDocKindCode": "00039", f"{nested_document}/csdo:DocName": "Документ",
        f"{nested_document}/csdo:DocId": "PROOF-038", f"{nested_document}/csdo:DocCreationDate": "2026-09-30",
        f"{nested_document}/csdo:DescriptionText": "Документ доказательства", f"{nested_document}/csdo:PageQuantity": "1", f"{nested_document}/csdo:DocBinaryText": "QUJD",
        priority: [None], f"{priority}/ipsdo:PriorityKindCode": "P", f"{priority}/ipsdo:PriorityDate": "2026-01-01",
        f"{priority}/csdo:UnifiedCountryCode": "RU", f"{priority}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        signature: [None], f"{signature}/csdo:DocCreationDate": "2026-09-30", officer: [None], officer_name: [None],
        f"{officer_name}/csdo:FirstName": "Петр", f"{officer_name}/csdo:LastName": "Петров", f"{officer}/csdo:PositionName": "Эксперт",
        "ccdo:ResourceItemStatusDetails": [None], validity: [None], f"{validity}/csdo:StartDateTime": "2026-09-30T14:01:00+03:00",
    }

def test_build_serialize_parse_extract_validate_roundtrip():
    engine=EaeuXmlEngine.load_process(PACKAGE); structure=engine.get_structure(MESSAGE,mode=GenerationMode.TEST); original=values()
    body=engine.build_body(MESSAGE,original,mode=GenerationMode.TEST); parsed=ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted,issues=engine.body_provider._values_from_element(structure,parsed); validation=engine.validate_body(MESSAGE,extracted,mode=GenerationMode.TEST)
    assert not issues
    assert validation.is_valid, [(x.rule_id,x.message) for x in validation.issues]
