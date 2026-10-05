from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.056"
AUTHORITY = "ipcdo:PatentAuthorityDetails"
PAYMENT = "ipcdo:IPPaymentDetails"
PARTY = f"{PAYMENT}/ipcdo:IPPartyDetails"
DOCUMENT = f"{PAYMENT}/ipcdo:AccompanyingDocumentsDetails"


def valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.03.003",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000056",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        AUTHORITY: [None],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": "RU",
        f"{AUTHORITY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{AUTHORITY}/csdo:AuthorityName": "Роспатент",
        f"{AUTHORITY}/ipsdo:OriginOfficeIndicator": "1",
        f"{AUTHORITY}/ccdo:SubjectAddressDetails": [""],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": "2",
        "ipsdo:TrademarkApplicationId": "2026/RU-000056",
        PAYMENT: [None],
        f"{PAYMENT}/csdo:EventDateTime": "2026-09-30T14:00:00+03:00",
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": "AP",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": "Заявитель",
        f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": "OR",
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": "RU",
        DOCUMENT: [None],
        f"{DOCUMENT}/ipsdo:IPDocKindCode": "07015",
        f"{DOCUMENT}/csdo:DocId": "DOC-056",
        f"{DOCUMENT}/csdo:DocCreationDate": "2026-09-30",
        f"{DOCUMENT}/csdo:DocBinaryText": "QQ==",
        f"{DOCUMENT}/csdo:DocBinaryText/@mediaTypeCode": "pdf",
    }


def test_build_serialize_parse_extract_validate_roundtrip():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    body = engine.build_body(MESSAGE, valid_values(), mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    result = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert result.is_valid, [(issue.rule_id, issue.message) for issue in result.issues]


def test_rules_are_message_isolated():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    ids = {rule["rule_id"] for rule in engine.rules[MESSAGE].structured_rules}
    assert ids and all(rule_id.startswith(f"{MESSAGE}.") for rule_id in ids)
