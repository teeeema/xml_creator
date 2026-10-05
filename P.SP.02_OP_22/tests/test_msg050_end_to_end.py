from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.050"
R007 = "ipcdo:UnifiedRegisterRecordsDetails"
PARTY = f"{R007}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMMUNICATION = f"{PARTY}/ccdo:CommunicationDetails"
PA = f"{R007}/ipcdo:PatentAuthorityDetails"
TRADEMARK = f"{R007}/ipcdo:TrademarkDetails"
DESCRIPTION = f"{TRADEMARK}/ipcdo:TMDescriptionDetails"
ELEMENT = f"{DESCRIPTION}/ipcdo:TMElementDetails"
GOODS = f"{R007}/ipcdo:GoodsBaseDetails"
STATUS = f"{R007}/ipcdo:IPEntityStatusDetails"
SIGNATURE = f"{R007}/ipcdo:SignatureDetails"
OFFICER = f"{SIGNATURE}/ipcdo:OfficerDetails"
OFFICER_NAME = f"{OFFICER}/ccdo:FullNameDetails"
RESOURCE = f"{R007}/ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
EXACT_DOC_NAME = (
    "Ходатайство об отказе от исключительного права на товарный знак, "
    "знак обслуживания Евразийского экономического союза"
)


def valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.007",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000050",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        R007: [None],
        f"{R007}/ipsdo:TrademarkId": "2026/RU-000050",
        f"{R007}/ipsdo:IPDocKindCode": "00050",
        STATUS: [{}],
        f"{STATUS}/csdo:StatusCode": "05",
        f"{STATUS}/csdo:EventDate": "2026-09-30",
        PA: [None],
        f"{PA}/csdo:UnifiedCountryCode": "RU",
        f"{PA}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PA}/csdo:AuthorityName": "Роспатент",
        f"{PA}/csdo:AuthorityBriefName": "ФИПС",
        f"{PA}/ipsdo:OriginOfficeIndicator": "1",
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": "RH",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": "Правообладатель",
        ADDRESS: [""],
        f"{ADDRESS}/csdo:AddressKindCode": "2",
        f"{ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{ADDRESS}/csdo:CityName": "Москва",
        f"{ADDRESS}/csdo:StreetName": "Тверская",
        f"{ADDRESS}/csdo:BuildingNumberId": "1",
        COMMUNICATION: [""],
        f"{COMMUNICATION}/csdo:CommunicationChannelCode": "EM",
        f"{COMMUNICATION}/csdo:CommunicationChannelId": "info@example.com",
        TRADEMARK: [None],
        f"{TRADEMARK}/ipsdo:TrademarkPicture": "base64data",
        f"{TRADEMARK}/ipsdo:TrademarkKindName": "Словесный",
        f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "0",
        DESCRIPTION: [""],
        f"{DESCRIPTION}/csdo:DescriptionText": "Описание товарного знака",
        ELEMENT: [""],
        f"{ELEMENT}/ipsdo:TrademarkCFECode": "01.01.01",
        f"{ELEMENT}/csdo:DesignationName": "Элемент",
        f"{ELEMENT}/ipsdo:TMLocalizedName": "Перевод",
        f"{ELEMENT}/ipsdo:TMLocalizedName/@languageCode": "ru",
        f"{ELEMENT}/ipsdo:TMTransliterationName": "Translit",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "09",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 09",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        f"{GOODS}/ipsdo:TrademarkDecisionIndicator": "1",
        f"{GOODS}/ipsdo:TrademarkApplicationId": "2026/RU-000050",
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:EndDateTime": "2026-10-01T14:00:00+03:00",
        SIGNATURE: [None],
        f"{SIGNATURE}/csdo:DocCreationDate": "2026-09-30",
        OFFICER: [None],
        OFFICER_NAME: [None],
        f"{OFFICER_NAME}/csdo:LastName": "Иванов",
        f"{OFFICER_NAME}/csdo:FirstName": "Иван",
        f"{OFFICER}/csdo:PositionName": "Эксперт",
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


def test_e2e_req1_and_req2_cardinality_and_trademark_id():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # 2 records -> fails REQ 2
    extracted_two = dict(extracted, **{R007: ["", ""]})
    val_two = engine.validate_body(MESSAGE, extracted_two, mode=GenerationMode.TEST)
    assert not val_two.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.050.T68.REQ.2" for iss in val_two.issues)

    # Missing TrademarkId -> fails REQ 1
    extracted_missing_tm_id = dict(extracted)
    del extracted_missing_tm_id[f"{R007}/ipsdo:TrademarkId"]
    val_missing = engine.validate_body(MESSAGE, extracted_missing_tm_id, mode=GenerationMode.TEST)
    assert not val_missing.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.050.T68.REQ.1" for iss in val_missing.issues)


def test_e2e_req3_end_datetime_required():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Missing EndDateTime -> FAIL REQ 3
    extracted_no_end = dict(extracted)
    del extracted_no_end[f"{VALIDITY}/csdo:EndDateTime"]
    val_no_end = engine.validate_body(MESSAGE, extracted_no_end, mode=GenerationMode.TEST)
    assert not val_no_end.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.050.T68.REQ.3" for iss in val_no_end.issues)


def test_e2e_req4_and_req5_document_kind():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Code present and Name present -> FAIL REQ 4
    extracted_both = dict(extracted, **{f"{R007}/ipsdo:IPDocKindName": EXACT_DOC_NAME})
    val_both = engine.validate_body(MESSAGE, extracted_both, mode=GenerationMode.TEST)
    assert not val_both.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.050.T68.REQ.4" for iss in val_both.issues)

    # Code absent and exact literal name -> PASS
    extracted_exact_name = dict(extracted)
    del extracted_exact_name[f"{R007}/ipsdo:IPDocKindCode"]
    extracted_exact_name[f"{R007}/ipsdo:IPDocKindName"] = EXACT_DOC_NAME
    val_exact = engine.validate_body(MESSAGE, extracted_exact_name, mode=GenerationMode.TEST)
    assert val_exact.is_valid

    # Code absent and wrong literal name -> FAIL REQ 5
    extracted_wrong_name = dict(extracted)
    del extracted_wrong_name[f"{R007}/ipsdo:IPDocKindCode"]
    extracted_wrong_name[f"{R007}/ipsdo:IPDocKindName"] = "Неверное ходатайство"
    val_wrong = engine.validate_body(MESSAGE, extracted_wrong_name, mode=GenerationMode.TEST)
    assert not val_wrong.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.050.T68.REQ.5" for iss in val_wrong.issues)


def test_e2e_req20_status_code_05():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # StatusCode != 05 -> FAIL
    for bad_code in ["01", "03"]:
        extracted_wrong_code = dict(extracted, **{f"{STATUS}/csdo:StatusCode": [bad_code]})
        val_code = engine.validate_body(MESSAGE, extracted_wrong_code, mode=GenerationMode.TEST)
        assert not val_code.is_valid
        assert any(iss.rule_id == "P.SP.02.MSG.050.T68.REQ.20" for iss in val_code.issues)

    # StatusCode with codeListId -> FAIL
    extracted_with_codelist = dict(extracted, **{f"{STATUS}/csdo:StatusCode/@codeListId": ["test_list"]})
    val_list = engine.validate_body(MESSAGE, extracted_with_codelist, mode=GenerationMode.TEST)
    assert not val_list.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.050.T68.REQ.20" for iss in val_list.issues)


def test_e2e_req21_23_signatures():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Officer present with FullNameDetails sibling -> FAIL REQ 21 & REQ 22
    extracted_both = dict(extracted, **{f"{SIGNATURE}/ccdo:FullNameDetails": [""]})
    val_both = engine.validate_body(MESSAGE, extracted_both, mode=GenerationMode.TEST)
    assert not val_both.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.050.T68.REQ.21.BRANCH" for iss in val_both.issues)
    assert any(iss.rule_id == "P.SP.02.MSG.050.T68.REQ.22" for iss in val_both.issues)

    # Officer missing PositionName -> FAIL REQ 23
    extracted_missing_pos = dict(extracted)
    del extracted_missing_pos[f"{OFFICER}/csdo:PositionName"]
    val_pos = engine.validate_body(MESSAGE, extracted_missing_pos, mode=GenerationMode.TEST)
    assert not val_pos.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.050.T68.REQ.23" for iss in val_pos.issues)

    # Officer with CommunicationDetails -> FAIL REQ 23
    extracted_comm = dict(extracted, **{f"{OFFICER}/ccdo:CommunicationDetails": [""]})
    val_comm = engine.validate_body(MESSAGE, extracted_comm, mode=GenerationMode.TEST)
    assert not val_comm.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.050.T68.REQ.23" for iss in val_comm.issues)


def test_critical_message_isolation():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    msg50_rules = {r["rule_id"] for r in engine.rules[MESSAGE].structured_rules}
    assert all(r.startswith(f"{MESSAGE}.") for r in msg50_rules)

    for other in ["P.SP.02.MSG.048", "P.SP.02.MSG.047", "P.SP.02.MSG.045", "P.SP.02.MSG.043", "P.SP.02.MSG.031"]:
        if other in engine.rules:
            other_rules = {r["rule_id"] for r in engine.rules[other].structured_rules}
            assert msg50_rules.isdisjoint(other_rules)

    # Semantic difference check:
    # In MSG047 and MSG048: StatusCode == "03", EndDateTime is FORBIDDEN
    # In MSG050: StatusCode == "05", EndDateTime is REQUIRED
    for r in engine.rules[MESSAGE].structured_rules:
        if r["rule_id"] == "P.SP.02.MSG.050.T68.REQ.20":
            status_assertion = next(a for a in r["assertions"] if a["target"]["field"] == "csdo:StatusCode")
            assert status_assertion["value"] == "05"
        if r["rule_id"] == "P.SP.02.MSG.050.T68.REQ.3":
            end_assertion = next(a for a in r["assertions"] if "EndDateTime" in a["target"]["field"])
            assert end_assertion["state"] == "REQUIRED"
