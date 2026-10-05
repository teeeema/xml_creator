from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.042"
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
    status = f"{APP}/ipcdo:IPEntityStatusDetails"
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000042",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:IPDocKindName": "Ходатайство о преобразовании заявки на регистрацию товарного знака, знака обслуживания Евразийского экономического союза в заявку на регистрацию коллективного знака Евразийского экономического союза",
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-30",
        f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000042",
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
        trademark: [None],
        description: [""],
        f"{description}/csdo:DescriptionText": "Описание товарного знака",
        f"{trademark}/ipsdo:TrademarkKindCode": "110",
        f"{trademark}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{trademark}/ipsdo:CollectiveMarkIndicator": "1",
        goods: [None],
        f"{goods}/ipsdo:GoodsClassCode": "01",
        f"{goods}/ipsdo:GoodsClassName": "Класс 01",
        f"{goods}/ipsdo:GoodsName": "Товар",
        document: [None],
        f"{document}/ipsdo:IPDocKindCode": "00040",
        f"{document}/csdo:DocName": "Документ",
        f"{document}/csdo:DocId": "DOC-042",
        f"{document}/csdo:DocCreationDate": "2026-09-30",
        f"{document}/csdo:DescriptionText": "Основной прилагаемый документ",
        f"{document}/csdo:PageQuantity": "1",
        f"{document}/csdo:DocBinaryText": "QUJD",
        naming: [None],
        f"{naming}/ipsdo:ProofKindCode": "01",
        proof: [None],
        nested_document: [None],
        f"{nested_document}/ipsdo:IPDocKindCode": "00041",
        f"{nested_document}/csdo:DocName": "Документ",
        f"{nested_document}/csdo:DocId": "PROOF-042",
        f"{nested_document}/csdo:DocCreationDate": "2026-09-30",
        f"{nested_document}/csdo:DescriptionText": "Документ доказательства",
        f"{nested_document}/csdo:PageQuantity": "1",
        f"{nested_document}/csdo:DocBinaryText": "QUJD",
        status: [{}],
        f"{status}/csdo:StatusCode": "02",
        signature: [None],
        f"{signature}/csdo:DocCreationDate": "2026-09-30",
        officer: [None],
        officer_name: [None],
        f"{officer_name}/csdo:FirstName": "Петр",
        f"{officer_name}/csdo:LastName": "Петров",
        f"{officer}/csdo:PositionName": "Эксперт",
        "ccdo:ResourceItemStatusDetails": [None],
        validity: [None],
        f"{validity}/csdo:StartDateTime": "2026-09-30T14:01:00+03:00",
    }


def test_build_serialize_parse_extract_validate_roundtrip():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert not issues
    assert validation.is_valid, [(x.rule_id, x.message) for x in validation.issues]


def test_e2e_isolation_collective_mark_indicator_zero_fails_msg042():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues

    # Mutate to MSG041 value ("0")
    extracted[f"{APP}/ipcdo:TrademarkDetails/ipsdo:CollectiveMarkIndicator"] = ["0"]
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert not validation.is_valid
    failed_rule_ids = [iss.rule_id for iss in validation.issues]
    assert "P.SP.02.MSG.042.T60.REQ.30" in failed_rule_ids
    assert all(rid.startswith("P.SP.02.MSG.042.") for rid in failed_rule_ids)


def test_e2e_end_date_forbidden():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues

    # Add forbidden EndDateTime
    extracted["ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime"] = ["2026-10-01T14:01:00+03:00"]
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert not validation.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.042.T60.REQ.32" for iss in validation.issues)


def test_e2e_status_code_02_required():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues

    # Wrong status code
    extracted[f"{APP}/ipcdo:IPEntityStatusDetails/csdo:StatusCode"] = ["30"]
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert not validation.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.042.T60.REQ.5" for iss in validation.issues)
