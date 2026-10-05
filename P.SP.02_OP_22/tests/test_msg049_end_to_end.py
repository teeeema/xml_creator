from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.049"
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


def valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.007",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000049",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        R007: [None],
        f"{R007}/ipsdo:TrademarkId": "2026/RU-000049",
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
        f"{GOODS}/ipsdo:TrademarkApplicationId": "2026/RU-000049",
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



EXACT_DOC_NAME = "Заявление о внесении изменений в сведения Единого реестра товарных знаков, знаков обслуживания Евразийского экономического союза"

def _roundtrip():
    engine=EaeuXmlEngine.load_process(PACKAGE)
    structure=engine.get_structure(MESSAGE,mode=GenerationMode.TEST)
    body=engine.build_body(MESSAGE,valid_values(),mode=GenerationMode.TEST)
    parsed=ET.fromstring(ET.tostring(body.serialize_xml_element(),encoding="utf-8"))
    extracted,issues=engine.body_provider._values_from_element(structure,parsed)
    assert not issues
    return engine,extracted

def _validate(engine,values):
    return engine.validate_body(MESSAGE,values,mode=GenerationMode.TEST)

def test_build_serialize_parse_extract_validate_roundtrip():
    engine,extracted=_roundtrip()
    result=_validate(engine,extracted)
    assert result.is_valid,[(x.rule_id,x.message) for x in result.issues]

def test_e2e_cardinality_trademark_and_resource_dates():
    engine,extracted=_roundtrip()
    two=dict(extracted,**{R007:["",""]})
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.2" for x in _validate(engine,two).issues)
    missing=dict(extracted); missing.pop(f"{R007}/ipsdo:TrademarkId",None)
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.1" for x in _validate(engine,missing).issues)
    no_start=dict(extracted); no_start.pop(f"{VALIDITY}/csdo:StartDateTime",None)
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.3" for x in _validate(engine,no_start).issues)
    with_end=dict(extracted,**{f"{VALIDITY}/csdo:EndDateTime":["2026-10-01T14:00:00+03:00"]})
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.4" for x in _validate(engine,with_end).issues)

def test_e2e_status_03_event_date_and_no_codelist():
    engine,extracted=_roundtrip()
    wrong=dict(extracted,**{f"{STATUS}/csdo:StatusCode":["01"]})
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.5" for x in _validate(engine,wrong).issues)
    missing=dict(extracted); missing.pop(f"{STATUS}/csdo:EventDate",None)
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.5" for x in _validate(engine,missing).issues)
    listed=dict(extracted,**{f"{STATUS}/csdo:StatusCode/@codeListId":["X"]})
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.5" for x in _validate(engine,listed).issues)

def test_e2e_document_kind_branches_and_exact_literal():
    engine,extracted=_roundtrip()
    both=dict(extracted,**{f"{R007}/ipsdo:IPDocKindName":EXACT_DOC_NAME})
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.21" for x in _validate(engine,both).issues)
    exact=dict(extracted); exact.pop(f"{R007}/ipsdo:IPDocKindCode",None); exact[f"{R007}/ipsdo:IPDocKindName"]=EXACT_DOC_NAME
    assert _validate(engine,exact).is_valid
    wrong=dict(exact,**{f"{R007}/ipsdo:IPDocKindName":"Неверное наименование"})
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.22" for x in _validate(engine,wrong).issues)

def test_e2e_inherited_subset_and_signatures():
    engine,extracted=_roundtrip()
    bad_goods=dict(extracted); bad_goods.pop(f"{GOODS}/ipsdo:GoodsClassCode",None)
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.16" for x in _validate(engine,bad_goods).issues)
    sibling=dict(extracted,**{f"{SIGNATURE}/ccdo:FullNameDetails":[""]})
    issues=_validate(engine,sibling).issues
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.23.BRANCH" for x in issues)
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.24" for x in issues)
    missing_pos=dict(extracted); missing_pos.pop(f"{OFFICER}/csdo:PositionName",None)
    assert any(x.rule_id==f"{MESSAGE}.T67.REQ.25" for x in _validate(engine,missing_pos).issues)

def test_message_rule_isolation_and_req20_absence():
    engine=EaeuXmlEngine.load_process(PACKAGE)
    ids={r["rule_id"] for r in engine.rules[MESSAGE].structured_rules}
    assert ids and all(x.startswith(f"{MESSAGE}.") for x in ids)
    assert not any(".REQ.20" in x for x in ids)
    for other in ("P.SP.02.MSG.047","P.SP.02.MSG.048","P.SP.02.MSG.050"):
        if other in engine.rules:
            assert ids.isdisjoint({r["rule_id"] for r in engine.rules[other].structured_rules})
