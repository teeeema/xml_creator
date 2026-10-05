from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.052"
R = "ipcdo:UnifiedRegisterRecordsDetails"
STATUS = f"{R}/ipcdo:IPEntityStatusDetails"
CANCEL = f"{R}/ipcdo:RegistrationCancellationDetails"
COMPLAINT = f"{CANCEL}/ipcdo:ComplaintInvalidateProtectionTrademarkDetails"
APPLICANT = f"{COMPLAINT}/ipcdo:ApplicantV2Details"
PARTY = f"{R}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMM = f"{PARTY}/ccdo:CommunicationDetails"
PA = f"{R}/ipcdo:PatentAuthorityDetails"
TM = f"{R}/ipcdo:TrademarkDetails"
DESC = f"{TM}/ipcdo:TMDescriptionDetails"
ELEMENT = f"{DESC}/ipcdo:TMElementDetails"
GOODS = f"{R}/ipcdo:GoodsBaseDetails"
SIG = f"{R}/ipcdo:SignatureDetails"
OFFICER = f"{SIG}/ipcdo:OfficerDetails"
OFFICER_NAME = f"{OFFICER}/ccdo:FullNameDetails"
RESOURCE = f"{R}/ccdo:ResourceItemStatusDetails"

def valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.007",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000052",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        R: [None],
        f"{R}/ipsdo:TrademarkId": "2026/RU-000052",
        f"{R}/ipsdo:IPDocKindCode": "00052",
        STATUS: [None],
        f"{STATUS}/csdo:StatusCode": "04",
        f"{STATUS}/csdo:EventDate": "2026-09-30",
        CANCEL: [""],
        f"{CANCEL}/ipsdo:CancellationTrademarkRegistrationReasonCode": "01",
        COMPLAINT: [""],
        f"{COMPLAINT}/ipsdo:CancellationRegistrationTrademarkCode": "01",
        f"{COMPLAINT}/ipsdo:SolutionCancellationRegistrationTrademarkCode": "01",
        APPLICANT: [""],
        f"{COMPLAINT}/csdo:EventDate": "2026-09-30",
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
        COMM: [""],
        f"{COMM}/csdo:CommunicationChannelCode": "EM",
        f"{COMM}/csdo:CommunicationChannelId": "info@example.com",
        TM: [None],
        f"{TM}/ipsdo:TrademarkPicture": "base64data",
        f"{TM}/ipsdo:TrademarkKindName": "Словесный",
        f"{TM}/ipsdo:CollectiveMarkIndicator": "0",
        DESC: [""],
        f"{DESC}/csdo:DescriptionText": "Описание",
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
        f"{GOODS}/ipsdo:TrademarkApplicationId": "APP-052",
        RESOURCE: [""],
        SIG: [""],
        f"{SIG}/csdo:DocCreationDate": "2026-09-30",
        OFFICER: [None],
        OFFICER_NAME: [None],
        f"{OFFICER_NAME}/csdo:LastName": "Иванов",
        f"{OFFICER_NAME}/csdo:FirstName": "Иван",
        f"{OFFICER}/csdo:PositionName": "Эксперт",
    }

def extracted_valid():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    body = engine.build_body(MESSAGE, valid_values(), mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    return engine, values

def test_build_serialize_parse_extract_validate_roundtrip():
    engine, values = extracted_valid()
    validation = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert validation.is_valid, [(x.rule_id, x.message) for x in validation.issues]

def test_e2e_req2_and_req23_cancellation_owner():
    engine, values = extracted_valid()
    no_date = dict(values)
    del no_date[f"{STATUS}/csdo:EventDate"]
    result = engine.validate_body(MESSAGE, no_date, mode=GenerationMode.TEST)
    assert any(i.rule_id == f"{MESSAGE}.T70.REQ.2.DETAILS" for i in result.issues)
    no_cancel_code = dict(values)
    del no_cancel_code[f"{COMPLAINT}/ipsdo:CancellationRegistrationTrademarkCode"]
    result = engine.validate_body(MESSAGE, no_cancel_code, mode=GenerationMode.TEST)
    assert any(i.rule_id == f"{MESSAGE}.T70.REQ.23" for i in result.issues)

def test_e2e_req25_document_kind_branch():
    engine, values = extracted_valid()
    both = dict(values)
    both[f"{R}/ipsdo:IPDocKindName"] = ["Решение об аннулировании регистрации товарного знака, знака обслуживания Евразийского экономического союза"]
    result = engine.validate_body(MESSAGE, both, mode=GenerationMode.TEST)
    assert any(i.rule_id == f"{MESSAGE}.T70.REQ.25" for i in result.issues)

def test_e2e_signature_same_parent_rules():
    engine, values = extracted_valid()
    both = dict(values)
    both[f"{SIG}/ccdo:FullNameDetails"] = [""]
    result = engine.validate_body(MESSAGE, both, mode=GenerationMode.TEST)
    assert any(i.rule_id == f"{MESSAGE}.T70.REQ.29.BRANCH" for i in result.issues)
    assert any(i.rule_id == f"{MESSAGE}.T70.REQ.30" for i in result.issues)
    missing_pos = dict(values)
    del missing_pos[f"{OFFICER}/csdo:PositionName"]
    result = engine.validate_body(MESSAGE, missing_pos, mode=GenerationMode.TEST)
    assert any(i.rule_id == f"{MESSAGE}.T70.REQ.31" for i in result.issues)

def test_critical_message_isolation():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    ours = {r["rule_id"] for r in engine.rules[MESSAGE].structured_rules}
    assert ours and all(x.startswith(f"{MESSAGE}.") for x in ours)
    for other in ("P.SP.02.MSG.050", "P.SP.02.MSG.051"):
        theirs = {r["rule_id"] for r in engine.rules[other].structured_rules}
        assert ours.isdisjoint(theirs)
