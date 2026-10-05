from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.044"
STRUCTURE = "R.IP.SP.02.002"
TRANSACTION = "P.SP.02.TRN.039"
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
SIGNATURE = f"{APP}/ipcdo:SignatureDetails"
OFFICER = f"{SIGNATURE}/ipcdo:OfficerDetails"
OFFICER_NAME = f"{OFFICER}/ccdo:FullNameDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
MAPPED = {1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34}


def engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def values():
    address = f"{PARTY}/ccdo:SubjectAddressDetails"
    communication = f"{PARTY}/ccdo:CommunicationDetails"
    description = f"{TM}/ipcdo:TMDescriptionDetails"
    document = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
    naming = f"{APP}/ipcdo:NamingAbilityProofDetails"
    proof = f"{naming}/ipcdo:ProofDocTextDetails"
    nested_document = f"{proof}/ipcdo:AccompanyingDocumentsDetails"
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": STRUCTURE,
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000044",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:IPDocKindName": "Ходатайство об отзыве заявки на регистрацию товарного знака Союза по инициативе заявителя",
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-30",
        f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000044",
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": "AP",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": "Заявитель",
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
        TM: [None],
        description: [""],
        f"{description}/csdo:DescriptionText": "Описание товарного знака",
        f"{TM}/ipsdo:TrademarkKindCode": "110",
        f"{TM}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TM}/ipsdo:CollectiveMarkIndicator": "0",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "01",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        document: [None],
        f"{document}/ipsdo:IPDocKindCode": "00040",
        f"{document}/csdo:DocName": "Документ",
        f"{document}/csdo:DocId": "DOC-044",
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
        f"{nested_document}/csdo:DocId": "PROOF-044",
        f"{nested_document}/csdo:DocCreationDate": "2026-09-30",
        f"{nested_document}/csdo:DescriptionText": "Документ доказательства",
        f"{nested_document}/csdo:PageQuantity": "1",
        f"{nested_document}/csdo:DocBinaryText": "QUJD",
        STATUS: [{}],
        f"{STATUS}/csdo:StatusCode": "30",
        f"{STATUS}/csdo:EventDate": "2026-09-30",
        SIGNATURE: [None],
        f"{SIGNATURE}/csdo:DocCreationDate": "2026-09-30",
        OFFICER: [None],
        OFFICER_NAME: [None],
        f"{OFFICER_NAME}/csdo:FirstName": "Петр",
        f"{OFFICER_NAME}/csdo:LastName": "Петров",
        f"{OFFICER}/csdo:PositionName": "Эксперт",
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T14:01:00+03:00",
        f"{VALIDITY}/csdo:EndDateTime": "2026-10-01T14:01:00+03:00",
    }


def q(structure, prefix, local):
    return f"{{{structure.imported_namespaces[prefix]}}}{local}"


def required(parent, structure, prefix, local):
    node = parent.find(q(structure, prefix, local))
    assert node is not None, (prefix, local)
    return node


def child(parent, structure, prefix, local, text=None, attrs=None):
    node = ET.SubElement(parent, ET.QName(structure.imported_namespaces[prefix], local))
    if text is not None:
        node.text = text
    for key, value in (attrs or {}).items():
        node.set(key, value)
    return node


def add_address(parent, structure, kind="2", country="RU"):
    address = child(parent, structure, "ccdo", "SubjectAddressDetails")
    child(address, structure, "csdo", "AddressKindCode", kind)
    child(address, structure, "csdo", "UnifiedCountryCode", country, {"codeListId": "ВОИС ST.3"})
    child(address, structure, "csdo", "CityName", "Москва")
    child(address, structure, "csdo", "StreetName", "Тестовая")
    child(address, structure, "csdo", "BuildingNumberId", "1")
    return address


def add_comm(parent, structure):
    communication = child(parent, structure, "ccdo", "CommunicationDetails")
    child(communication, structure, "csdo", "CommunicationChannelCode", "EM")
    child(communication, structure, "csdo", "CommunicationChannelId", "role@example.test")
    return communication


def add_party(app, structure, role, omit=None):
    party = child(app, structure, "ipcdo", "IPPartyDetails")
    child(party, structure, "ipsdo", "IPPartyKindCode", role)
    child(party, structure, "csdo", "UnifiedCountryCode", "RU", {"codeListId": "ВОИС ST.3"})
    child(party, structure, "ipsdo", "IPSubjectName", f"Party {role}")
    if omit != "address":
        add_address(party, structure)
    if omit != "communication":
        add_comm(party, structure)
    if role == "PA" and omit != "attorney":
        child(party, structure, "ipsdo", "PatentAttorneyId", "PA-1")
    return party


def build_parsed():
    e = engine()
    body = e.build_body(MESSAGE, values(), mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    structure = e.get_structure(MESSAGE, mode=GenerationMode.TEST)
    return e, structure, parsed


def extract_validate(e, structure, parsed):
    reparsed = ET.fromstring(ET.tostring(parsed, encoding="utf-8"))
    extracted, issues = e.body_provider._values_from_element(structure, reparsed)
    validation = e.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    return extracted, issues, validation


def target_rules(e, code):
    prefix = f"{MESSAGE}.T62.REQ.{code}"
    return [rule for rule in e.rules[MESSAGE].structured_rules if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")]


def assert_req_fails(e, code, extracted):
    statuses = [StructuredRuleEvaluator().evaluate(rule, extracted).status for rule in target_rules(e, code)]
    assert statuses and RuleStatus.FAIL in statuses, (code, statuses)


def test_build_serialize_parse_extract_validate_roundtrip():
    e, structure, parsed = build_parsed()
    extracted, issues, validation = extract_validate(e, structure, parsed)
    assert not issues
    assert parsed.tag == "{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails"
    assert extracted[f"{STATUS}/csdo:StatusCode"] == "30"
    assert extracted[f"{STATUS}/csdo:EventDate"] == "2026-09-30"
    assert extracted[f"{VALIDITY}/csdo:StartDateTime"] == "2026-09-30T14:01:00+03:00"
    assert extracted[f"{VALIDITY}/csdo:EndDateTime"] == "2026-10-01T14:01:00+03:00"
    assert validation.is_valid, [(item.rule_id, item.message) for item in validation.issues]
    codes = {int(item.rule_id.split(".REQ.", 1)[1].split(".", 1)[0]) for item in validation.rule_evaluations}
    assert codes == MAPPED
    transaction = e.get_transaction(TRANSACTION)
    assert transaction.initiating_message == MESSAGE
    assert transaction.response_messages == ("P.SP.02.MSG.002",)
    assert transaction.initiating_operation == "P.SP.02.OPR.096"
    assert transaction.responding_operation == "P.SP.02.OPR.097"
    assert transaction.initiating_participant == "P.SP.02.ACT.001"
    assert transaction.responding_participant == "P.SP.02.ACT.002"


@pytest.mark.parametrize("mutator", ["status_missing", "status_wrong", "status_attr", "event_missing", "start_missing", "end_missing"])
def test_msg044_status_event_and_validity_negative_proofs(mutator):
    e, structure, parsed = build_parsed()
    app = required(parsed, structure, "ipcdo", "TrademarkApplicationDetails")
    status = required(app, structure, "ipcdo", "IPEntityStatusDetails")
    resource = required(parsed, structure, "ccdo", "ResourceItemStatusDetails")
    validity = required(resource, structure, "ccdo", "ValidityPeriodDetails")
    code = 5
    if mutator == "status_missing":
        app.remove(status)
    elif mutator == "status_wrong":
        required(status, structure, "csdo", "StatusCode").text = "02"
    elif mutator == "status_attr":
        required(status, structure, "csdo", "StatusCode").set("codeListId", "STATUS")
    elif mutator == "event_missing":
        status.remove(required(status, structure, "csdo", "EventDate"))
    elif mutator == "start_missing":
        validity.remove(required(validity, structure, "csdo", "StartDateTime")); code = 33
    else:
        validity.remove(required(validity, structure, "csdo", "EndDateTime")); code = 34
    extracted, _, validation = extract_validate(e, structure, parsed)
    assert not validation.is_valid
    assert_req_fails(e, code, extracted)


def test_wrong_owner_event_and_validity_dates_do_not_satisfy():
    e, structure, parsed = build_parsed()
    app = required(parsed, structure, "ipcdo", "TrademarkApplicationDetails")
    status = required(app, structure, "ipcdo", "IPEntityStatusDetails")
    status.remove(required(status, structure, "csdo", "EventDate"))
    child(app, structure, "csdo", "EventDate", "2026-09-30")
    resource = required(parsed, structure, "ccdo", "ResourceItemStatusDetails")
    validity = required(resource, structure, "ccdo", "ValidityPeriodDetails")
    validity.remove(required(validity, structure, "csdo", "StartDateTime"))
    validity.remove(required(validity, structure, "csdo", "EndDateTime"))
    child(resource, structure, "csdo", "StartDateTime", "2026-09-30T14:01:00+03:00")
    child(resource, structure, "csdo", "EndDateTime", "2026-10-01T14:01:00+03:00")
    extracted, _, _ = extract_validate(e, structure, parsed)
    assert_req_fails(e, 5, extracted)
    assert_req_fails(e, 33, extracted)
    assert_req_fails(e, 34, extracted)


def test_req1_two_applications_fail_after_production_extract():
    e, structure, parsed = build_parsed()
    app = required(parsed, structure, "ipcdo", "TrademarkApplicationDetails")
    parsed.insert(list(parsed).index(app) + 1, deepcopy(app))
    extracted, _, validation = extract_validate(e, structure, parsed)
    assert not validation.is_valid
    assert_req_fails(e, 1, extracted)


def test_req27_same_trademark_parent_after_production_extract():
    e, structure, parsed = build_parsed()
    app = required(parsed, structure, "ipcdo", "TrademarkApplicationDetails")
    first = required(app, structure, "ipcdo", "TrademarkDetails")
    required(first, structure, "ipsdo", "TrademarkKindCode").text = "140"
    second = deepcopy(first)
    required(second, structure, "ipsdo", "TrademarkKindCode").text = "110"
    child(second, structure, "ipsdo", "TrademarkPicture", "picture")
    child(second, structure, "ipsdo", "TrademarkColourName", "red")
    app.append(second)
    extracted, _, _ = extract_validate(e, structure, parsed)
    assert_req_fails(e, 27, extracted)


@pytest.mark.parametrize("mutator", ["signature_missing", "signature_conflict", "officer_last", "officer_first", "officer_position", "officer_comm"])
def test_signature_rules_use_production_same_parent_semantics(mutator):
    e, structure, parsed = build_parsed()
    app = required(parsed, structure, "ipcdo", "TrademarkApplicationDetails")
    signature = required(app, structure, "ipcdo", "SignatureDetails")
    officer = required(signature, structure, "ipcdo", "OfficerDetails")
    officer_name = required(officer, structure, "ccdo", "FullNameDetails")
    code = 32
    if mutator == "signature_missing":
        app.remove(signature); code = 30
    elif mutator == "signature_conflict":
        full_name = child(signature, structure, "ccdo", "FullNameDetails")
        child(full_name, structure, "csdo", "LastName", "Сидоров")
        child(full_name, structure, "csdo", "FirstName", "Сидор")
        code = 30
    elif mutator == "officer_last":
        officer_name.remove(required(officer_name, structure, "csdo", "LastName"))
    elif mutator == "officer_first":
        officer_name.remove(required(officer_name, structure, "csdo", "FirstName"))
    elif mutator == "officer_position":
        officer.remove(required(officer, structure, "csdo", "PositionName"))
    else:
        child(officer, structure, "ccdo", "CommunicationDetails")
    extracted, _, validation = extract_validate(e, structure, parsed)
    assert not validation.is_valid
    assert_req_fails(e, code, extracted)


def mutate_inherited(parsed, structure, code):
    app = required(parsed, structure, "ipcdo", "TrademarkApplicationDetails")
    party = required(app, structure, "ipcdo", "IPPartyDetails")
    address = required(party, structure, "ccdo", "SubjectAddressDetails")
    communication = required(party, structure, "ccdo", "CommunicationDetails")
    trademark = required(app, structure, "ipcdo", "TrademarkDetails")
    goods = required(app, structure, "ipcdo", "GoodsBaseDetails")
    if code == 6:
        app.remove(required(app, structure, "ipsdo", "ApplicationReceiptDate"))
    elif code == 7:
        required(party, structure, "csdo", "UnifiedCountryCode").set("codeListId", "WRONG")
    elif code == 8:
        address.remove(required(address, structure, "csdo", "CityName"))
    elif code == 9:
        communication.remove(required(communication, structure, "csdo", "CommunicationChannelId"))
    elif code == 10:
        required(communication, structure, "csdo", "CommunicationChannelCode").text = "PH"
    elif code == 11:
        authority = child(app, structure, "ipcdo", "PatentAuthorityDetails")
        child(authority, structure, "csdo", "AuthorityName", "Office")
        add_address(authority, structure)
    elif code == 12:
        authority = child(app, structure, "ipcdo", "PatentAuthorityDetails")
        child(authority, structure, "csdo", "UnifiedCountryCode", "RU", {"codeListId": "ВОИС ST.3"})
        child(authority, structure, "csdo", "AuthorityName", "Office")
        add_address(authority, structure, kind="3")
    elif code == 14:
        required(party, structure, "ipsdo", "IPPartyKindCode").text = "RE"
    elif code == 15:
        party.remove(communication)
    elif code == 21:
        add_party(app, structure, "PA", omit="attorney")
    elif code == 22:
        add_party(app, structure, "RE", omit="address")
    elif code == 23:
        correspondence = child(app, structure, "ipcdo", "CorrespondenceAddressDetails")
        add_address(correspondence, structure, kind="2")
    elif code == 24:
        correspondence = child(app, structure, "ipcdo", "CorrespondenceAddressDetails")
        add_address(correspondence, structure, country="US")
    elif code == 25:
        app.remove(trademark)
    elif code == 27:
        required(trademark, structure, "ipsdo", "TrademarkKindCode").text = "140"
    elif code == 28:
        required(trademark, structure, "ipsdo", "CollectiveMarkIndicator").text = "2"
    elif code == 29:
        goods.remove(required(goods, structure, "ipsdo", "GoodsClassCode"))
    else:
        raise AssertionError(code)


@pytest.mark.parametrize("code", [6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29])
def test_each_inherited_executable_requirement_has_negative_proof(code):
    e, structure, parsed = build_parsed()
    mutate_inherited(parsed, structure, code)
    extracted, _, validation = extract_validate(e, structure, parsed)
    assert not validation.is_valid
    assert_req_fails(e, code, extracted)


def test_msg044_rules_are_message_isolated():
    e, structure, parsed = build_parsed()
    extracted, _, validation = extract_validate(e, structure, parsed)
    assert validation.rule_evaluations
    assert all(item.rule_id.startswith(MESSAGE + ".") for item in validation.rule_evaluations)
    if "P.SP.02.MSG.040" in e.rules:
        other = e.validate_body("P.SP.02.MSG.040", extracted, mode=GenerationMode.TEST)
        assert all(item.rule_id.startswith("P.SP.02.MSG.040.") for item in other.rule_evaluations)
        assert {item.rule_id for item in validation.rule_evaluations}.isdisjoint({item.rule_id for item in other.rule_evaluations})
