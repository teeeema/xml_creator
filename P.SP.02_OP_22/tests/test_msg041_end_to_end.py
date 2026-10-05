from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.041"
STRUCTURE = "R.IP.SP.02.002"
TRANSACTION = "P.SP.02.TRN.036"
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
DESC = f"{TM}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
SIGNATURE = f"{APP}/ipcdo:SignatureDetails"
OFFICER = f"{SIGNATURE}/ipcdo:OfficerDetails"
OFFICER_NAME = f"{OFFICER}/ccdo:FullNameDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
MAPPED = {1,4,5,6,7,8,9,10,11,12,14,15,21,22,23,24,25,27,28,29,30,31,32,33,34,35}

def engine():
    return EaeuXmlEngine.load_process(PACKAGE)

def values():
    return {
        "ccdo:EDocHeader":[None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode":MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode":STRUCTURE,
        "ccdo:EDocHeader/csdo:EDocId":"00000000-0000-0000-0000-000000000041",
        "ccdo:EDocHeader/csdo:EDocDateTime":"2026-09-30T15:00:00+03:00",
        APP:[None],
        f"{APP}/ipsdo:IPDocKindName":"Ходатайство о преобразовании заявки на коллективный знак Союза в заявку на ТЗ Союза",
        f"{APP}/ipsdo:ApplicationReceiptDate":"2026-09-30",
        f"{APP}/ipsdo:TrademarkApplicationId":"2026/RU-000041",
        STATUS:[None], f"{STATUS}/csdo:StatusCode":"02",
        PARTY:[None],
        f"{PARTY}/ipsdo:IPPartyKindCode":"AP",
        f"{PARTY}/csdo:UnifiedCountryCode":"RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId":"ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName":"Заявитель",
        ADDRESS:[""],
        f"{ADDRESS}/csdo:AddressKindCode":"2",
        f"{ADDRESS}/csdo:UnifiedCountryCode":"RU",
        f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId":"ВОИС ST.3",
        f"{ADDRESS}/csdo:CityName":"Москва",
        f"{ADDRESS}/csdo:StreetName":"Тестовая",
        f"{ADDRESS}/csdo:BuildingNumberId":"1",
        COMM:[""],
        f"{COMM}/csdo:CommunicationChannelCode":"EM",
        f"{COMM}/csdo:CommunicationChannelId":"applicant@example.test",
        TM:[None], DESC:[""],
        f"{DESC}/csdo:DescriptionText":"Описание товарного знака",
        f"{TM}/ipsdo:TrademarkKindCode":"110",
        f"{TM}/ipsdo:TrademarkKindName":"Словесный знак",
        f"{TM}/ipsdo:CollectiveMarkIndicator":"0",
        GOODS:[None],
        f"{GOODS}/ipsdo:GoodsClassCode":"01",
        f"{GOODS}/ipsdo:GoodsClassName":"Класс 01",
        f"{GOODS}/ipsdo:GoodsName":"Товар",
        SIGNATURE:[None],
        f"{SIGNATURE}/csdo:DocCreationDate":"2026-09-30",
        OFFICER:[None], OFFICER_NAME:[None],
        f"{OFFICER_NAME}/csdo:FirstName":"Петр",
        f"{OFFICER_NAME}/csdo:LastName":"Петров",
        f"{OFFICER}/csdo:PositionName":"Эксперт",
        RESOURCE:[None], VALIDITY:[None],
        f"{VALIDITY}/csdo:StartDateTime":"2026-09-30T15:01:00+03:00",
    }

def q(structure,prefix,local):
    return f"{{{structure.imported_namespaces[prefix]}}}{local}"

def required(parent,structure,prefix,local):
    node = parent.find(q(structure,prefix,local))
    assert node is not None, (prefix,local)
    return node

def child(parent,structure,prefix,local,text=None,attrs=None):
    node=ET.SubElement(parent,ET.QName(structure.imported_namespaces[prefix],local))
    if text is not None:
        node.text=text
    for key,value in (attrs or {}).items():
        node.set(key,value)
    return node

def add_address(parent,structure,kind="2",country="RU"):
    address=child(parent,structure,"ccdo","SubjectAddressDetails")
    child(address,structure,"csdo","AddressKindCode",kind)
    child(address,structure,"csdo","UnifiedCountryCode",country,{"codeListId":"ВОИС ST.3"})
    child(address,structure,"csdo","CityName","Москва")
    child(address,structure,"csdo","StreetName","Тестовая")
    child(address,structure,"csdo","BuildingNumberId","1")
    return address

def add_comm(parent,structure):
    comm=child(parent,structure,"ccdo","CommunicationDetails")
    child(comm,structure,"csdo","CommunicationChannelCode","EM")
    child(comm,structure,"csdo","CommunicationChannelId","role@example.test")
    return comm

def add_party(app,structure,role,omit=None):
    party=child(app,structure,"ipcdo","IPPartyDetails")
    child(party,structure,"ipsdo","IPPartyKindCode",role)
    child(party,structure,"csdo","UnifiedCountryCode","RU",{"codeListId":"ВОИС ST.3"})
    child(party,structure,"ipsdo","IPSubjectName",f"Party {role}")
    if omit!="address":
        add_address(party,structure)
    if omit!="communication":
        add_comm(party,structure)
    if role=="PA" and omit!="attorney":
        child(party,structure,"ipsdo","PatentAttorneyId","PA-1")
    return party

def build_parsed():
    e=engine()
    body=e.build_body(MESSAGE,values(),mode=GenerationMode.TEST)
    parsed=ET.fromstring(ET.tostring(body.serialize_xml_element(),encoding="utf-8"))
    structure=e.get_structure(MESSAGE,mode=GenerationMode.TEST)
    return e,structure,parsed

def extract_validate(e,structure,parsed):
    reparsed=ET.fromstring(ET.tostring(parsed,encoding="utf-8"))
    extracted,issues=e.body_provider._values_from_element(structure,reparsed)
    validation=e.validate_body(MESSAGE,extracted,mode=GenerationMode.TEST)
    return extracted,issues,validation

def target_rules(e,code):
    prefix=f"{MESSAGE}.T59.REQ.{code}"
    return [r for r in e.rules[MESSAGE].structured_rules if r["rule_id"]==prefix or r["rule_id"].startswith(prefix+".")]

def assert_req_fails(e,code,extracted):
    statuses=[StructuredRuleEvaluator().evaluate(r,extracted).status for r in target_rules(e,code)]
    assert statuses and RuleStatus.FAIL in statuses, (code,statuses)

def test_build_serialize_parse_extract_validate_pipeline_and_transaction():
    e,structure,parsed=build_parsed()
    extracted,issues,validation=extract_validate(e,structure,parsed)
    assert not issues
    assert parsed.tag=="{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails"
    assert extracted[f"{STATUS}/csdo:StatusCode"]=="02"
    assert extracted[f"{TM}/ipsdo:CollectiveMarkIndicator"]=="0"
    assert extracted[f"{VALIDITY}/csdo:StartDateTime"]=="2026-09-30T15:01:00+03:00"
    assert f"{VALIDITY}/csdo:EndDateTime" not in extracted or extracted[f"{VALIDITY}/csdo:EndDateTime"] is None
    assert validation.is_valid, [(x.rule_id,x.message) for x in validation.issues]
    codes={int(x.rule_id.split(".REQ.",1)[1].split(".",1)[0]) for x in validation.rule_evaluations}
    assert codes==MAPPED
    t=e.get_transaction(TRANSACTION)
    assert t.initiating_message==MESSAGE
    assert t.response_messages==("P.SP.02.MSG.002",)
    assert t.initiating_operation=="P.SP.02.OPR.072"
    assert t.responding_operation=="P.SP.02.OPR.073"
    assert t.initiating_participant=="P.SP.02.ACT.001"
    assert t.responding_participant=="P.SP.02.ACT.002"

@pytest.mark.parametrize("code,mutator", [
    (4, "app_id"),
    (5, "status_missing"),
    (5, "status_wrong"),
    (5, "status_attr"),
    (30, "indicator_one"),
    (30, "indicator_missing"),
    (31, "start_missing"),
    (32, "end_present"),
    (33, "signature_missing"),
    (33, "signature_conflict"),
    (34, "signature_conflict_reverse"),
    (35, "officer_last"),
    (35, "officer_first"),
    (35, "officer_position"),
    (35, "officer_comm"),
])
def test_msg041_specific_negative_proofs_use_production_xml(code,mutator):
    e,structure,parsed=build_parsed()
    app=required(parsed,structure,"ipcdo","TrademarkApplicationDetails")
    tm=required(app,structure,"ipcdo","TrademarkDetails")
    signature=required(app,structure,"ipcdo","SignatureDetails")
    officer=required(signature,structure,"ipcdo","OfficerDetails")
    officer_name=required(officer,structure,"ccdo","FullNameDetails")
    resource=required(parsed,structure,"ccdo","ResourceItemStatusDetails")
    validity=required(resource,structure,"ccdo","ValidityPeriodDetails")
    if mutator=="app_id":
        app.remove(required(app,structure,"ipsdo","TrademarkApplicationId"))
    elif mutator=="status_missing":
        app.remove(required(app,structure,"ipcdo","IPEntityStatusDetails"))
    elif mutator=="status_wrong":
        status=required(app,structure,"ipcdo","IPEntityStatusDetails")
        required(status,structure,"csdo","StatusCode").text="01"
    elif mutator=="status_attr":
        status=required(app,structure,"ipcdo","IPEntityStatusDetails")
        required(status,structure,"csdo","StatusCode").set("codeListId","STATUS")
    elif mutator=="indicator_one":
        required(tm,structure,"ipsdo","CollectiveMarkIndicator").text="1"
    elif mutator=="indicator_missing":
        tm.remove(required(tm,structure,"ipsdo","CollectiveMarkIndicator"))
    elif mutator=="start_missing":
        validity.remove(required(validity,structure,"csdo","StartDateTime"))
    elif mutator=="end_present":
        ET.SubElement(validity,ET.QName(structure.imported_namespaces["csdo"],"EndDateTime")).text="2026-10-01T15:00:00+03:00"
    elif mutator=="signature_missing":
        app.remove(signature)
    elif mutator in {"signature_conflict","signature_conflict_reverse"}:
        full=ET.SubElement(signature,ET.QName(structure.imported_namespaces["ccdo"],"FullNameDetails"))
        ET.SubElement(full,ET.QName(structure.imported_namespaces["csdo"],"LastName")).text="Сидоров"
        ET.SubElement(full,ET.QName(structure.imported_namespaces["csdo"],"FirstName")).text="Сидор"
    elif mutator=="officer_last":
        officer_name.remove(required(officer_name,structure,"csdo","LastName"))
    elif mutator=="officer_first":
        officer_name.remove(required(officer_name,structure,"csdo","FirstName"))
    elif mutator=="officer_position":
        officer.remove(required(officer,structure,"csdo","PositionName"))
    elif mutator=="officer_comm":
        ET.SubElement(officer,ET.QName(structure.imported_namespaces["ccdo"],"CommunicationDetails"))
    extracted,_,validation=extract_validate(e,structure,parsed)
    assert not validation.is_valid
    assert_req_fails(e,code,extracted)

def test_wrong_owner_start_and_indicator_do_not_satisfy_after_production_extract():
    e,structure,parsed=build_parsed()
    app=required(parsed,structure,"ipcdo","TrademarkApplicationDetails")
    tm=required(app,structure,"ipcdo","TrademarkDetails")
    tm.remove(required(tm,structure,"ipsdo","CollectiveMarkIndicator"))
    ET.SubElement(app,ET.QName(structure.imported_namespaces["ipsdo"],"CollectiveMarkIndicator")).text="0"
    resource=required(parsed,structure,"ccdo","ResourceItemStatusDetails")
    validity=required(resource,structure,"ccdo","ValidityPeriodDetails")
    validity.remove(required(validity,structure,"csdo","StartDateTime"))
    ET.SubElement(resource,ET.QName(structure.imported_namespaces["csdo"],"StartDateTime")).text="2026-09-30T15:01:00+03:00"
    extracted,_,_=extract_validate(e,structure,parsed)
    assert_req_fails(e,30,extracted)
    assert_req_fails(e,31,extracted)

def test_msg041_rules_are_isolated_from_msg042():
    e,structure,parsed=build_parsed()
    extracted,_,validation41=extract_validate(e,structure,parsed)
    assert validation41.rule_evaluations
    assert all(x.rule_id.startswith(MESSAGE+".") for x in validation41.rule_evaluations)
    if "P.SP.02.MSG.042" in e.rules:
        validation42=e.validate_body("P.SP.02.MSG.042",extracted,mode=GenerationMode.TEST)
        assert all(x.rule_id.startswith("P.SP.02.MSG.042.") for x in validation42.rule_evaluations)
        assert {x.rule_id for x in validation41.rule_evaluations}.isdisjoint({x.rule_id for x in validation42.rule_evaluations})

def mutate_inherited(parsed,structure,code):
    app=required(parsed,structure,"ipcdo","TrademarkApplicationDetails")
    party=required(app,structure,"ipcdo","IPPartyDetails")
    address=required(party,structure,"ccdo","SubjectAddressDetails")
    comm=required(party,structure,"ccdo","CommunicationDetails")
    tm=required(app,structure,"ipcdo","TrademarkDetails")
    goods=required(app,structure,"ipcdo","GoodsBaseDetails")
    if code==6:
        app.remove(required(app,structure,"ipsdo","ApplicationReceiptDate"))
    elif code==7:
        required(party,structure,"csdo","UnifiedCountryCode").set("codeListId","WRONG")
    elif code==8:
        address.remove(required(address,structure,"csdo","CityName"))
    elif code==9:
        comm.remove(required(comm,structure,"csdo","CommunicationChannelId"))
    elif code==10:
        required(comm,structure,"csdo","CommunicationChannelCode").text="PH"
    elif code==11:
        authority=child(app,structure,"ipcdo","PatentAuthorityDetails")
        child(authority,structure,"csdo","AuthorityName","Office")
        add_address(authority,structure,kind="2")
    elif code==12:
        authority=child(app,structure,"ipcdo","PatentAuthorityDetails")
        child(authority,structure,"csdo","UnifiedCountryCode","RU",{"codeListId":"ВОИС ST.3"})
        child(authority,structure,"csdo","AuthorityName","Office")
        add_address(authority,structure,kind="3")
    elif code==14:
        required(party,structure,"ipsdo","IPPartyKindCode").text="RE"
    elif code==15:
        party.remove(comm)
    elif code==21:
        add_party(app,structure,"PA",omit="attorney")
    elif code==22:
        add_party(app,structure,"RE",omit="address")
    elif code==23:
        corr=child(app,structure,"ipcdo","CorrespondenceAddressDetails")
        add_address(corr,structure,kind="2")
    elif code==24:
        corr=child(app,structure,"ipcdo","CorrespondenceAddressDetails")
        add_address(corr,structure,country="US")
    elif code==25:
        app.remove(tm)
    elif code==27:
        required(tm,structure,"ipsdo","TrademarkKindCode").text="140"
    elif code==28:
        required(tm,structure,"ipsdo","CollectiveMarkIndicator").text="2"
    elif code==29:
        goods.remove(required(goods,structure,"ipsdo","GoodsClassCode"))
    else:
        raise AssertionError(code)

@pytest.mark.parametrize("code",[6,7,8,9,10,11,12,14,15,21,22,23,24,25,27,28,29])
def test_each_inherited_executable_requirement_has_negative_proof(code):
    e,structure,parsed=build_parsed()
    mutate_inherited(parsed,structure,code)
    extracted,_,validation=extract_validate(e,structure,parsed)
    assert not validation.is_valid
    assert_req_fails(e,code,extracted)
