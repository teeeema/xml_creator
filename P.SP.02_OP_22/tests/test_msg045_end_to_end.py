from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.045"
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMMUNICATION = f"{PARTY}/ccdo:CommunicationDetails"
TRADEMARK = f"{APP}/ipcdo:TrademarkDetails"
DESCRIPTION = f"{TRADEMARK}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
SIGNATURE = f"{APP}/ipcdo:SignatureDetails"
OFFICER = f"{SIGNATURE}/ipcdo:OfficerDetails"
OFFICER_NAME = f"{OFFICER}/ccdo:FullNameDetails"
VALIDITY = "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails"


def valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000045",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-30",
        f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000045",
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": "AP",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": "Заявитель",
        ADDRESS: [""],
        f"{ADDRESS}/csdo:AddressKindCode": "2",
        f"{ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{ADDRESS}/csdo:CityName": "Москва",
        f"{ADDRESS}/csdo:StreetName": "Тестовая",
        f"{ADDRESS}/csdo:BuildingNumberId": "1",
        COMMUNICATION: [""],
        f"{COMMUNICATION}/csdo:CommunicationChannelCode": "EM",
        f"{COMMUNICATION}/csdo:CommunicationChannelId": "applicant@example.test",
        TRADEMARK: [None],
        DESCRIPTION: [""],
        f"{DESCRIPTION}/csdo:DescriptionText": "Описание товарного знака",
        f"{TRADEMARK}/ipsdo:TrademarkKindCode": "110",
        f"{TRADEMARK}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "1",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "01",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        STATUS: [{}],
        f"{STATUS}/csdo:StatusCode": "02",
        f"{STATUS}/csdo:EventDate": "2026-09-30",
        f"{STATUS}/csdo:DocId": "DOC-045",
        f"{STATUS}/ipsdo:IPDocReceiptDate": "2026-09-30",
        f"{STATUS}/csdo:DescriptionText": "Внесение изменений",
        SIGNATURE: [None],
        f"{SIGNATURE}/csdo:DocCreationDate": "2026-09-30",
        OFFICER: [None],
        OFFICER_NAME: [None],
        f"{OFFICER_NAME}/csdo:FirstName": "Петр",
        f"{OFFICER_NAME}/csdo:LastName": "Петров",
        f"{OFFICER}/csdo:PositionName": "Эксперт",
        "ccdo:ResourceItemStatusDetails": [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T14:01:00+03:00",
    }


def test_build_serialize_parse_extract_validate_roundtrip():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    parsed = ET.fromstring(serialized)
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues, f"Extraction issues: {issues}"
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert validation.is_valid, [(x.rule_id, x.message) for x in validation.issues]


def test_e2e_req1_cardinality():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # 2 applications -> FAIL
    extracted_two = dict(extracted, **{APP: ["", ""]})
    val_two = engine.validate_body(MESSAGE, extracted_two, mode=GenerationMode.TEST)
    assert not val_two.is_valid
    failed_ids = [iss.rule_id for iss in val_two.issues if iss.rule_id]
    assert "P.SP.02.MSG.045.T63.REQ.1" in failed_ids
    assert all(rid.startswith("P.SP.02.MSG.045.") for rid in failed_ids)


def test_e2e_req3_root_resource_end_datetime_forbidden():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Add forbidden root EndDateTime
    extracted["ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime"] = ["2026-10-01T14:00:00+03:00"]
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert not validation.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.045.T63.REQ.3" for iss in validation.issues)


def test_e2e_req31_status_code_02_and_no_codelist():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # StatusCode != 02 -> FAIL
    extracted_wrong_code = dict(extracted, **{f"{STATUS}/csdo:StatusCode": ["30"]})
    val_code = engine.validate_body(MESSAGE, extracted_wrong_code, mode=GenerationMode.TEST)
    assert not val_code.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.045.T63.REQ.31" for iss in val_code.issues)

    # StatusCode with codeListId -> FAIL
    extracted_with_codelist = dict(extracted, **{f"{STATUS}/csdo:StatusCode/@codeListId": ["test_list"]})
    val_list = engine.validate_body(MESSAGE, extracted_with_codelist, mode=GenerationMode.TEST)
    assert not val_list.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.045.T63.REQ.31" for iss in val_list.issues)


def test_e2e_req32_status_descendants_required():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    for field in ["csdo:EventDate", "csdo:DocId", "ipsdo:IPDocReceiptDate", "csdo:DescriptionText"]:
        extracted_missing = dict(extracted)
        del extracted_missing[f"{STATUS}/{field}"]
        val = engine.validate_body(MESSAGE, extracted_missing, mode=GenerationMode.TEST)
        assert not val.is_valid
        assert any(iss.rule_id == "P.SP.02.MSG.045.T63.REQ.32" for iss in val.issues)


def test_e2e_req27_same_trademark_parent():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Change kind to 140 without picture -> FAIL
    extracted_140 = dict(extracted, **{f"{TRADEMARK}/ipsdo:TrademarkKindCode": "140"})
    val = engine.validate_body(MESSAGE, extracted_140, mode=GenerationMode.TEST)
    assert not val.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.045.T63.REQ.27" for iss in val.issues)


def test_e2e_req33_35_signature_behavior():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Conflict: OfficerDetails + FullNameDetails in same signature -> FAIL
    extracted_conflict = dict(extracted, **{
        f"{SIGNATURE}/ccdo:FullNameDetails": [""],
        f"{SIGNATURE}/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
        f"{SIGNATURE}/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
    })
    val = engine.validate_body(MESSAGE, extracted_conflict, mode=GenerationMode.TEST)
    assert not val.is_valid
    failed_ids = [iss.rule_id for iss in val.issues if iss.rule_id]
    assert "P.SP.02.MSG.045.T63.REQ.33.BRANCH" in failed_ids
    assert "P.SP.02.MSG.045.T63.REQ.34" in failed_ids


def test_e2e_message_isolation():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Validate against MSG040 (which requires StatusCode == 30) -> FAIL
    val_msg040 = engine.validate_body("P.SP.02.MSG.040", extracted, mode=GenerationMode.TEST)
    assert not val_msg040.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.040.T58.REQ.5" for iss in val_msg040.issues)
    assert all(iss.rule_id.startswith("P.SP.02.MSG.040.") for iss in val_msg040.issues if iss.rule_id)
