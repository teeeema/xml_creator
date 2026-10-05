from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.048"
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
TRANSFORMATION = f"{R007}/ipcdo:TransformationDetails"
SIGNATURE = f"{R007}/ipcdo:SignatureDetails"
OFFICER = f"{SIGNATURE}/ipcdo:OfficerDetails"
OFFICER_NAME = f"{OFFICER}/ccdo:FullNameDetails"
RESOURCE = f"{R007}/ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
EXACT_DOC_NAME = (
    "Ходатайство о преобразовании коллективного знака Евразийского экономического союза "
    "в товарный знак, знак обслуживания Евразийского экономического союза"
)
REVERSED_DOC_NAME = (
    "Ходатайство о преобразовании товарного знака Евразийского экономического союза "
    "в коллективный знак Евразийского экономического союза"
)


def valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.007",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000048",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        R007: [None],
        f"{R007}/ipsdo:TrademarkId": "2026/RU-000048",
        f"{R007}/ipsdo:IPDocKindCode": "00042",
        STATUS: [{}],
        f"{STATUS}/csdo:StatusCode": "03",
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
        f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "1",
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
        f"{GOODS}/ipsdo:TrademarkApplicationId": "2026/RU-000048",
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T14:01:00+03:00",
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
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.2" for iss in val_two.issues)

    # Missing TrademarkId -> fails REQ 1
    extracted_missing_tm_id = dict(extracted)
    del extracted_missing_tm_id[f"{R007}/ipsdo:TrademarkId"]
    val_missing = engine.validate_body(MESSAGE, extracted_missing_tm_id, mode=GenerationMode.TEST)
    assert not val_missing.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.1" for iss in val_missing.issues)


def test_e2e_req3_status_code_03_and_no_codelist():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # StatusCode != 03 -> FAIL
    extracted_wrong_code = dict(extracted, **{f"{STATUS}/csdo:StatusCode": ["01"]})
    val_code = engine.validate_body(MESSAGE, extracted_wrong_code, mode=GenerationMode.TEST)
    assert not val_code.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.3" for iss in val_code.issues)

    # StatusCode with codeListId -> FAIL
    extracted_with_codelist = dict(extracted, **{f"{STATUS}/csdo:StatusCode/@codeListId": ["test_list"]})
    val_list = engine.validate_body(MESSAGE, extracted_with_codelist, mode=GenerationMode.TEST)
    assert not val_list.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.3" for iss in val_list.issues)


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
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.4" for iss in val_both.issues)

    # Code absent and exact literal name -> PASS
    extracted_exact_name = dict(extracted)
    del extracted_exact_name[f"{R007}/ipsdo:IPDocKindCode"]
    extracted_exact_name[f"{R007}/ipsdo:IPDocKindName"] = EXACT_DOC_NAME
    val_exact = engine.validate_body(MESSAGE, extracted_exact_name, mode=GenerationMode.TEST)
    assert val_exact.is_valid

    # Code absent and wrong / reversed literal name -> FAIL REQ 5
    extracted_wrong_name = dict(extracted)
    del extracted_wrong_name[f"{R007}/ipsdo:IPDocKindCode"]
    extracted_wrong_name[f"{R007}/ipsdo:IPDocKindName"] = REVERSED_DOC_NAME
    val_wrong = engine.validate_body(MESSAGE, extracted_wrong_name, mode=GenerationMode.TEST)
    assert not val_wrong.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.5" for iss in val_wrong.issues)


def test_e2e_req20_transformation_details_per_instance():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Without TransformationDetails -> PASS (container is optional)
    val_no_trans = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert val_no_trans.is_valid

    # With valid TransformationDetails -> PASS
    extracted_trans = dict(extracted)
    extracted_trans[TRANSFORMATION] = [""]
    extracted_trans[f"{TRANSFORMATION}/ipsdo:TransformationKindName"] = ["Преобразование"]
    extracted_trans[f"{TRANSFORMATION}/ipsdo:IPObjectId"] = ["2026/RU-000048"]
    extracted_trans[f"{TRANSFORMATION}/csdo:EventDate"] = ["2026-09-30"]
    val_trans = engine.validate_body(MESSAGE, extracted_trans, mode=GenerationMode.TEST)
    assert val_trans.is_valid

    # With incomplete TransformationDetails (missing EventDate) -> FAIL REQ 20
    extracted_inc = dict(extracted_trans)
    del extracted_inc[f"{TRANSFORMATION}/csdo:EventDate"]
    val_inc = engine.validate_body(MESSAGE, extracted_inc, mode=GenerationMode.TEST)
    assert not val_inc.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.20" for iss in val_inc.issues)


def test_e2e_req21_collective_mark_indicator_one():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # CollectiveMarkIndicator == "1" -> PASS
    val_one = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert val_one.is_valid

    # CollectiveMarkIndicator == "0" -> FAIL REQ 21
    extracted_zero = dict(extracted, **{f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": ["0"]})
    val_zero = engine.validate_body(MESSAGE, extracted_zero, mode=GenerationMode.TEST)
    assert not val_zero.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.21" for iss in val_zero.issues)


def test_e2e_req22_resource_end_datetime_forbidden():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Present EndDateTime -> FAIL REQ 22
    extracted_end = dict(extracted, **{f"{VALIDITY}/csdo:EndDateTime": ["2026-10-01T14:00:00+03:00"]})
    val_end = engine.validate_body(MESSAGE, extracted_end, mode=GenerationMode.TEST)
    assert not val_end.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.22" for iss in val_end.issues)


def test_e2e_req23_25_signatures():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Officer present with FullNameDetails sibling -> FAIL REQ 23 & REQ 24
    extracted_both = dict(extracted, **{f"{SIGNATURE}/ccdo:FullNameDetails": [""]})
    val_both = engine.validate_body(MESSAGE, extracted_both, mode=GenerationMode.TEST)
    assert not val_both.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.23.BRANCH" for iss in val_both.issues)
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.24" for iss in val_both.issues)

    # Officer missing PositionName -> FAIL REQ 25
    extracted_missing_pos = dict(extracted)
    del extracted_missing_pos[f"{OFFICER}/csdo:PositionName"]
    val_pos = engine.validate_body(MESSAGE, extracted_missing_pos, mode=GenerationMode.TEST)
    assert not val_pos.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.25" for iss in val_pos.issues)

    # Officer with CommunicationDetails -> FAIL REQ 25
    extracted_comm = dict(extracted, **{f"{OFFICER}/ccdo:CommunicationDetails": [""]})
    val_comm = engine.validate_body(MESSAGE, extracted_comm, mode=GenerationMode.TEST)
    assert not val_comm.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.048.T66.REQ.25" for iss in val_comm.issues)


def test_message_rule_isolation():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    msg48_rules = {r["rule_id"] for r in engine.rules[MESSAGE].structured_rules}
    assert all(r.startswith(f"{MESSAGE}.") for r in msg48_rules)

    for other in ["P.SP.02.MSG.047", "P.SP.02.MSG.045", "P.SP.02.MSG.043", "P.SP.02.MSG.031"]:
        if other in engine.rules:
            other_rules = {r["rule_id"] for r in engine.rules[other].structured_rules}
            assert msg48_rules.isdisjoint(other_rules)
