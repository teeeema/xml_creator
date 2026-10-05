from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.012"
APP = "ipcdo:TrademarkApplicationDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
PATENT = f"{APP}/ipcdo:PatentAuthorityDetails"
CORR = f"{APP}/ipcdo:CorrespondenceAddressDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
VALIDITY = "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails"


def valid_values():
    # Physical order: Index 0 = Role A (02, initial app); Index 1 = Role B (01, divided app)
    return {
        "ccdo:EDocHeader": "",
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000012",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        APP: ["", ""],
        f"{APP}/ipsdo:ApplicationReceiptDate": ["2026-09-30", "2026-09-30"],
        f"{APP}/ipsdo:TrademarkApplicationId": ["2026/RU-000001", "2026/RU-000002"],
        f"{APP}/ipsdo:SourceTrademarkApplicationId": [None, "2026/RU-000001"],
        STATUS: ["", ""],
        f"{STATUS}/csdo:StatusCode": ["02", "01"],
        PATENT: [None, ""],
        f"{PATENT}/csdo:AuthorityName": [None, "Роспатент"],
        f"{PATENT}/ipsdo:OriginOfficeIndicator": [None, "1"],
        f"{PATENT}/csdo:UnifiedCountryCode": [None, "RU"],
        f"{PATENT}/csdo:UnifiedCountryCode/@codeListId": [None, "ВОИС ST.3"],
        f"{PATENT}/ccdo:SubjectAddressDetails": [None, ""],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": [None, "2"],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode": [None, "RU"],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode/@codeListId": [None, "ВОИС ST.3"],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:CityName": [None, "Москва"],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:StreetName": [None, "Бережковская наб."],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:BuildingNumberId": [None, "30"],
        CORR: [None, ""],
        f"{CORR}/ccdo:SubjectAddressDetails": [None, ""],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": [None, "3"],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode": [None, "RU"],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode/@codeListId": [None, "ВОИС ST.3"],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:CityName": [None, "Москва"],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:StreetName": [None, "Ленина"],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:BuildingNumberId": [None, "10"],
        f"{CORR}/ccdo:CommunicationDetails": [None, ""],
        f"{CORR}/ccdo:CommunicationDetails/csdo:CommunicationChannelCode": [None, "EM"],
        f"{CORR}/ccdo:CommunicationDetails/csdo:CommunicationChannelId": [None, "corr@example.com"],
        PARTY: [None, ""],
        f"{PARTY}/ipsdo:IPPartyKindCode": [None, "AP"],
        f"{PARTY}/csdo:UnifiedCountryCode": [None, "RU"],
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": [None, "ВОИС ST.3"],
        f"{PARTY}/ipsdo:IPSubjectName": [None, "Заявитель"],
        f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": [None, "OR"],
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": [None, "RU"],
        f"{PARTY}/ccdo:SubjectAddressDetails": [None, ""],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": [None, "2"],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode": [None, "RU"],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode/@codeListId": [None, "ВОИС ST.3"],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:CityName": [None, "Москва"],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:StreetName": [None, "Тверская"],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:BuildingNumberId": [None, "1"],
        f"{PARTY}/ccdo:CommunicationDetails": [None, ""],
        f"{PARTY}/ccdo:CommunicationDetails/csdo:CommunicationChannelCode": [None, "EM"],
        f"{PARTY}/ccdo:CommunicationDetails/csdo:CommunicationChannelId": [None, "applicant@example.com"],
        TM: [None, ""],
        f"{TM}/ipsdo:TrademarkKindCode": [None, "110"],
        f"{TM}/ipsdo:TrademarkKindName": [None, "Словесный знак"],
        f"{TM}/ipsdo:CollectiveMarkIndicator": [None, "0"],
        f"{TM}/ipcdo:TMDescriptionDetails": [None, ""],
        f"{TM}/ipcdo:TMDescriptionDetails/csdo:DescriptionText": [None, "Описание знака"],
        GOODS: [None, ""],
        f"{GOODS}/ipsdo:GoodsClassCode": [None, "01"],
        f"{GOODS}/ipsdo:GoodsClassName": [None, "Класс 01"],
        f"{GOODS}/ipsdo:GoodsName": [None, "Химические продукты"],
        "ccdo:ResourceItemStatusDetails": "",
        "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails": "",
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T14:01:00+03:00",
    }


def reversed_valid_values():
    # Physical order: Index 0 = Role B (01, divided app); Index 1 = Role A (02, initial app)
    val = valid_values()
    for path, v in list(val.items()):
        if isinstance(v, list) and len(v) == 2 and path not in {APP, f"{APP}/ipsdo:ApplicationReceiptDate"}:
            val[path] = [v[1], v[0]]
    return val


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


def test_e2e_reversed_roles_passes():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = reversed_valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    parsed = ET.fromstring(serialized)
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues, f"Extraction issues: {issues}"
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert validation.is_valid, [(x.rule_id, x.message) for x in validation.issues]


def test_e2e_req1_one_application_fails():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    extracted = valid_values()
    extracted[APP] = [""]
    extracted[f"{APP}/ipsdo:TrademarkApplicationId"] = ["2026/RU-000001"]
    extracted[STATUS] = [""]
    extracted[f"{STATUS}/csdo:StatusCode"] = ["02"]
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert not validation.is_valid
    failed_rule_ids = [iss.rule_id for iss in validation.issues if iss.rule_id]
    assert f"{MESSAGE}.T45.REQ.1" in failed_rule_ids


def test_e2e_req1_three_applications_fails():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    extracted = valid_values()
    extracted[APP] = ["", "", ""]
    extracted[f"{APP}/ipsdo:TrademarkApplicationId"] = ["2026/RU-000001", "2026/RU-000002", "2026/RU-000003"]
    extracted[STATUS] = ["", "", ""]
    extracted[f"{STATUS}/csdo:StatusCode"] = ["02", "01", "01"]
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert not validation.is_valid
    failed_rule_ids = [iss.rule_id for iss in validation.issues if iss.rule_id]
    assert f"{MESSAGE}.T45.REQ.1" in failed_rule_ids


def test_e2e_req30_cross_instance_mismatch_fails():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    extracted = valid_values()
    extracted[f"{APP}/ipsdo:SourceTrademarkApplicationId"] = [None, "2026/RU-DIFFERENT"]
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert not validation.is_valid
    failed_rule_ids = [iss.rule_id for iss in validation.issues if iss.rule_id]
    assert f"{MESSAGE}.T45.REQ.30" in failed_rule_ids


def test_e2e_req31_role_uniqueness_fails():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    extracted = valid_values()
    extracted[f"{STATUS}/csdo:StatusCode"] = ["01", "01"]
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert not validation.is_valid
    failed_rule_ids = [iss.rule_id for iss in validation.issues if iss.rule_id]
    assert f"{MESSAGE}.T45.REQ.31.ROLE02" in failed_rule_ids


def test_e2e_req33_missing_start_datetime_fails():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    extracted = valid_values()
    del extracted[f"{VALIDITY}/csdo:StartDateTime"]
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert not validation.is_valid
    failed_rule_ids = [iss.rule_id for iss in validation.issues]
    assert f"{MESSAGE}.T45.REQ.33" in failed_rule_ids


def test_e2e_req34_end_datetime_forbidden():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    extracted = valid_values()
    extracted[f"{VALIDITY}/csdo:EndDateTime"] = "2026-10-01T14:01:00+03:00"
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert not validation.is_valid
    failed_rule_ids = [iss.rule_id for iss in validation.issues]
    assert f"{MESSAGE}.T45.REQ.34" in failed_rule_ids


def test_message_isolation():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    extracted = valid_values()
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert validation.is_valid
    rules = engine.rules[MESSAGE].structured_rules
    assert all(r["rule_id"].startswith(MESSAGE) for r in rules)
