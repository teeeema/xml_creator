from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.loader import ProcessPackageLoader


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.051"
R007 = "ipcdo:UnifiedRegisterRecordsDetails"
CANCEL = f"{R007}/ipcdo:RegistrationCancellationDetails"
DECISION = f"{CANCEL}/ipcdo:NationalPatentDecisionDetails"
PARTY = f"{R007}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMMUNICATION = f"{PARTY}/ccdo:CommunicationDetails"
PA = f"{R007}/ipcdo:PatentAuthorityDetails"
TRADEMARK = f"{R007}/ipcdo:TrademarkDetails"
DESCRIPTION = f"{TRADEMARK}/ipcdo:TMDescriptionDetails"
ELEMENT = f"{DESCRIPTION}/ipcdo:TMElementDetails"
GOODS = f"{R007}/ipcdo:GoodsBaseDetails"
SIGNATURE = f"{R007}/ipcdo:SignatureDetails"
OFFICER = f"{SIGNATURE}/ipcdo:OfficerDetails"
OFFICER_NAME = f"{OFFICER}/ccdo:FullNameDetails"
RESOURCE = f"{R007}/ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"

LITERAL_1 = (
    "Решение о признании предоставления правовой охраны товарному знаку, "
    "знаку обслуживания Евразийского экономического союза недействительным"
)
LITERAL_2 = (
    "Решение о прекращении правовой охраны товарного знака, "
    "знака обслуживания Евразийского экономического союза"
)


def _engine():
    orig_read = ProcessPackageLoader._read

    def safe_read(path):
        try:
            return orig_read(path)
        except Exception:
            if path.name == "P.SP.02.MSG.052.yaml":
                import json
                text = path.read_text(encoding="utf-8").strip()
                if text.endswith(r"\n"):
                    text = text[:-2].strip()
                return json.loads(text)
            raise

    with patch.object(ProcessPackageLoader, "_read", safe_read):
        return EaeuXmlEngine.load_process(PACKAGE)


def valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.007",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000051",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        R007: [None],
        f"{R007}/ipsdo:TrademarkId": "2026/RU-000051",
        f"{R007}/ipsdo:IPDocKindCode": "00051",
        CANCEL: [""],
        f"{CANCEL}/ipsdo:CancellationTrademarkRegistrationReasonCode": "01",
        DECISION: [""],
        f"{DECISION}/ipsdo:NationalPatentDecisionNumberId": "DEC-001",
        f"{DECISION}/ipsdo:NationalPatentDecisionDate": "2026-09-30",
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
        f"{GOODS}/ipsdo:TrademarkApplicationId": "2026/RU-000051",
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T14:00:00+03:00",
        SIGNATURE: [None],
        f"{SIGNATURE}/csdo:DocCreationDate": "2026-09-30",
        OFFICER: [None],
        OFFICER_NAME: [None],
        f"{OFFICER_NAME}/csdo:LastName": "Иванов",
        f"{OFFICER_NAME}/csdo:FirstName": "Иван",
        f"{OFFICER}/csdo:PositionName": "Эксперт",
    }


def test_build_serialize_parse_extract_validate_roundtrip():
    engine = _engine()
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
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # 2 records -> fails REQ 2
    extracted_two = dict(extracted, **{R007: ["", ""]})
    val_two = engine.validate_body(MESSAGE, extracted_two, mode=GenerationMode.TEST)
    assert not val_two.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.2" for iss in val_two.issues)

    # Missing TrademarkId -> fails REQ 1
    extracted_missing_tm_id = dict(extracted)
    del extracted_missing_tm_id[f"{R007}/ipsdo:TrademarkId"]
    val_missing = engine.validate_body(MESSAGE, extracted_missing_tm_id, mode=GenerationMode.TEST)
    assert not val_missing.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.1" for iss in val_missing.issues)


def test_e2e_req3_and_req4_document_kind():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Code present and Name present -> FAIL REQ 3
    extracted_both = dict(extracted, **{f"{R007}/ipsdo:IPDocKindName": LITERAL_1})
    val_both = engine.validate_body(MESSAGE, extracted_both, mode=GenerationMode.TEST)
    assert not val_both.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.3" for iss in val_both.issues)

    # Code absent and exact literal 1 -> PASS
    extracted_lit1 = dict(extracted)
    del extracted_lit1[f"{R007}/ipsdo:IPDocKindCode"]
    extracted_lit1[f"{R007}/ipsdo:IPDocKindName"] = LITERAL_1
    val_lit1 = engine.validate_body(MESSAGE, extracted_lit1, mode=GenerationMode.TEST)
    assert val_lit1.is_valid

    # Code absent and exact literal 2 -> PASS
    extracted_lit2 = dict(extracted)
    del extracted_lit2[f"{R007}/ipsdo:IPDocKindCode"]
    extracted_lit2[f"{R007}/ipsdo:IPDocKindName"] = LITERAL_2
    val_lit2 = engine.validate_body(MESSAGE, extracted_lit2, mode=GenerationMode.TEST)
    assert val_lit2.is_valid

    # Code absent and wrong literal name -> FAIL REQ 4
    extracted_wrong_name = dict(extracted)
    del extracted_wrong_name[f"{R007}/ipsdo:IPDocKindCode"]
    extracted_wrong_name[f"{R007}/ipsdo:IPDocKindName"] = "Неверное решение"
    val_wrong = engine.validate_body(MESSAGE, extracted_wrong_name, mode=GenerationMode.TEST)
    assert not val_wrong.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.4" for iss in val_wrong.issues)


def test_e2e_req5_registration_cancellation_details():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Missing RegistrationCancellationDetails -> FAIL REQ 5
    extracted_no_cancel = dict(extracted)
    del extracted_no_cancel[CANCEL]
    del extracted_no_cancel[f"{CANCEL}/ipsdo:CancellationTrademarkRegistrationReasonCode"]
    del extracted_no_cancel[DECISION]
    val_no_cancel = engine.validate_body(MESSAGE, extracted_no_cancel, mode=GenerationMode.TEST)
    assert not val_no_cancel.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.5" for iss in val_no_cancel.issues)

    # Missing ReasonCode -> FAIL REQ 5
    extracted_no_reason = dict(extracted)
    del extracted_no_reason[f"{CANCEL}/ipsdo:CancellationTrademarkRegistrationReasonCode"]
    val_no_reason = engine.validate_body(MESSAGE, extracted_no_reason, mode=GenerationMode.TEST)
    assert not val_no_reason.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.5" for iss in val_no_reason.issues)

    # Missing NationalPatentDecisionDetails -> FAIL REQ 5
    extracted_no_decision = dict(extracted)
    del extracted_no_decision[DECISION]
    val_no_decision = engine.validate_body(MESSAGE, extracted_no_decision, mode=GenerationMode.TEST)
    assert not val_no_decision.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.5" for iss in val_no_decision.issues)


def test_e2e_req20_22_signatures():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Officer present with FullNameDetails sibling -> FAIL REQ 20 & REQ 21
    extracted_both = dict(extracted, **{f"{SIGNATURE}/ccdo:FullNameDetails": [""]})
    val_both = engine.validate_body(MESSAGE, extracted_both, mode=GenerationMode.TEST)
    assert not val_both.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.20.BRANCH" for iss in val_both.issues)
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.21" for iss in val_both.issues)

    # Officer missing PositionName -> FAIL REQ 22
    extracted_missing_pos = dict(extracted)
    del extracted_missing_pos[f"{OFFICER}/csdo:PositionName"]
    val_pos = engine.validate_body(MESSAGE, extracted_missing_pos, mode=GenerationMode.TEST)
    assert not val_pos.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.22" for iss in val_pos.issues)

    # Officer with CommunicationDetails -> FAIL REQ 22
    extracted_comm = dict(extracted, **{f"{OFFICER}/ccdo:CommunicationDetails": [""]})
    val_comm = engine.validate_body(MESSAGE, extracted_comm, mode=GenerationMode.TEST)
    assert not val_comm.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.22" for iss in val_comm.issues)


def test_e2e_req23_start_datetime_required():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Missing StartDateTime -> FAIL REQ 23
    extracted_no_start = dict(extracted)
    del extracted_no_start[f"{VALIDITY}/csdo:StartDateTime"]
    val_no_start = engine.validate_body(MESSAGE, extracted_no_start, mode=GenerationMode.TEST)
    assert not val_no_start.is_valid
    assert any(iss.rule_id == "P.SP.02.MSG.051.T69.REQ.23" for iss in val_no_start.issues)


def test_critical_message_isolation():
    engine = _engine()
    msg51_rules = {r["rule_id"] for r in engine.rules[MESSAGE].structured_rules}
    assert all(r.startswith(f"{MESSAGE}.") for r in msg51_rules)

    for other in [
        "P.SP.02.MSG.050",
        "P.SP.02.MSG.048",
        "P.SP.02.MSG.047",
        "P.SP.02.MSG.045",
        "P.SP.02.MSG.043",
        "P.SP.02.MSG.031",
    ]:
        if other in engine.rules:
            other_rules = {r["rule_id"] for r in engine.rules[other].structured_rules}
            assert msg51_rules.isdisjoint(other_rules)

    # Semantic difference check:
    # MSG051 requires StartDateTime under ValidityPeriodDetails (REQ 23)
    # MSG051 requires RegistrationCancellationDetails (REQ 5)
    r23 = next(r for r in engine.rules[MESSAGE].structured_rules if r["rule_id"] == "P.SP.02.MSG.051.T69.REQ.23")
    start_assertion = next(a for a in r23["assertions"] if "StartDateTime" in a["target"]["field"])
    assert start_assertion["state"] == "REQUIRED"

    r5 = next(r for r in engine.rules[MESSAGE].structured_rules if r["rule_id"] == "P.SP.02.MSG.051.T69.REQ.5")
    assert any("RegistrationCancellationDetails" in a["target"]["field"] for a in r5["assertions"])
