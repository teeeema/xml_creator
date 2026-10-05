from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.033"
STRUCTURE = "R.IP.SP.02.002"
TRANSACTION = "P.SP.02.TRN.028"
APP = "ipcdo:TrademarkApplicationDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
DESC = f"{TM}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
SIG = f"{APP}/ipcdo:SignatureDetails"
FULLNAME = f"{SIG}/ccdo:FullNameDetails"
RESPONSE = f"{APP}/ipcdo:ApplicantComplainResponseDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
FALLBACK = (
    "Заключение национального патентного ведомства по результатам экспертизы "
    "заявленного обозначения о возможности (невозможности) регистрации товарного знака, "
    "знака обслуживания Евразийского экономического союза"
)
MAPPED = ({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37}) | {16, 17, 18, 19, 20, 26}
FULL = {1, 2, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37}


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": STRUCTURE,
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000033",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T13:00:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:IPDocKindName": FALLBACK,
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-30",
        f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000033",
        STATUS: [None],
        f"{STATUS}/csdo:StatusCode": "10",
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": "AP",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": "Заявитель", f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": "OR", f"{PARTY}/ipsdo:IPSubjectName/@languageCode": "RU",
        ADDRESS: [""],
        f"{ADDRESS}/csdo:AddressKindCode": "2",
        f"{ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{ADDRESS}/csdo:CityName": "Москва",
        f"{ADDRESS}/csdo:StreetName": "Тестовая",
        f"{ADDRESS}/csdo:BuildingNumberId": "1",
        COMM: [""],
        f"{COMM}/csdo:CommunicationChannelCode": "EM",
        f"{COMM}/csdo:CommunicationChannelId": "applicant@example.test",
        TM: [None],
        DESC: [""],
        f"{DESC}/csdo:DescriptionText": "Описание товарного знака",
        f"{TM}/ipsdo:TrademarkKindCode": "110",
        f"{TM}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TM}/ipsdo:CollectiveMarkIndicator": "0",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "01",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        f"{APP}/ipsdo:TrademarkRegistrationCode": "01",
        SIG: [None],
        f"{SIG}/csdo:DocCreationDate": "2026-09-30",
        FULLNAME: [None],
        f"{FULLNAME}/csdo:FirstName": "Иван",
        f"{FULLNAME}/csdo:LastName": "Иванов",
        RESPONSE: [""],
        f"{RESPONSE}/ipsdo:ApplicantComplainResponseName": "Жалоба удовлетворена",
        f"{RESPONSE}/ipsdo:ApplicantComplainResponseDate": "2026-09-30",
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T13:01:00+03:00",
    }


def _q(structure, prefix, local):
    return f"{{{structure.imported_namespaces[prefix]}}}{local}"


def _first(parent, structure, prefix, local):
    return parent.find(_q(structure, prefix, local))


def _required(parent, structure, prefix, local):
    node = _first(parent, structure, prefix, local)
    assert node is not None, (prefix, local)
    return node


def _child(parent, structure, prefix, local, text=None, attrs=None, namespace=None):
    ns = namespace if namespace is not None else structure.imported_namespaces[prefix]
    node = ET.SubElement(parent, ET.QName(ns, local))
    if text is not None:
        node.text = text
    for key, value in (attrs or {}).items():
        node.set(key, value)
    return node


def _add_address(parent, structure, *, kind="2", country="RU"):
    address = _child(parent, structure, "ccdo", "SubjectAddressDetails")
    _child(address, structure, "csdo", "AddressKindCode", kind)
    _child(address, structure, "csdo", "UnifiedCountryCode", country, attrs={"codeListId": "ВОИС ST.3"})
    _child(address, structure, "csdo", "CityName", "Москва")
    _child(address, structure, "csdo", "StreetName", "Тестовая")
    _child(address, structure, "csdo", "BuildingNumberId", "1")
    return address


def _add_comm(parent, structure):
    comm = _child(parent, structure, "ccdo", "CommunicationDetails")
    _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
    _child(comm, structure, "csdo", "CommunicationChannelId", "role@example.test")
    return comm


def _add_party(app, structure, role, *, omit=None):
    party = _child(app, structure, "ipcdo", "IPPartyDetails")
    _child(party, structure, "ipsdo", "IPPartyKindCode", role)
    _child(party, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
    name = _child(party, structure, "ipsdo", "IPSubjectName", f"Party {role}")
    if role == "AP":
        name.set("nameRepresentationKindCode", "OR")
        name.set("languageCode", "RU")
    if omit != "address":
        _add_address(party, structure)
    if omit != "communication":
        _add_comm(party, structure)
    if role == "PA" and omit != "attorney":
        _child(party, structure, "ipsdo", "PatentAttorneyId", "PA-033")
    return party


def _add_direct_authority(app, structure, *, country=True, address_kind="2"):
    authority = _child(app, structure, "ipcdo", "PatentAuthorityDetails")
    if country:
        _child(authority, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
    _child(authority, structure, "csdo", "AuthorityName", "Patent office")
    _add_address(authority, structure, kind=address_kind)
    _child(authority, structure, "ipsdo", "OriginOfficeIndicator", "1")
    return authority


def _add_correspondence(app, structure, *, kind="3", country="RU"):
    corr = _child(app, structure, "ipcdo", "CorrespondenceAddressDetails")
    _add_address(corr, structure, kind=kind, country=country)
    return corr


def _build_valid_parsed():
    engine = _engine()
    body = engine.build_body(MESSAGE, _valid_values(), mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    return engine, structure, parsed


def _extract_validate(engine, structure, parsed, message=MESSAGE):
    reparsed = ET.fromstring(ET.tostring(parsed, encoding="utf-8"))
    values, extraction_issues = engine.body_provider._values_from_element(structure, reparsed)
    validation = engine.validate_body(message, values, mode=GenerationMode.TEST)
    return values, extraction_issues, validation


def _target_rules(engine, code):
    rid = f"{MESSAGE}.T51.REQ.{code}"
    return [rule for rule in engine.rules[MESSAGE].structured_rules if rule["rule_id"] == rid]


def _target_fails(engine, code, values):
    rules = _target_rules(engine, code)
    assert rules, code
    statuses = [StructuredRuleEvaluator().evaluate(rule, values).status for rule in rules]
    assert RuleStatus.FAIL in statuses, (code, statuses)


def test_valid_msg033_build_serialize_parse_extract_validate_pipeline():
    engine, structure, parsed = _build_valid_parsed()
    values, extraction_issues, validation = _extract_validate(engine, structure, parsed)

    assert parsed.tag == "{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails"
    assert not extraction_issues, [(item.code, item.field_path, item.message) for item in extraction_issues]
    assert values[f"{APP}/ipsdo:IPDocKindName"] == FALLBACK
    assert values[f"{STATUS}/csdo:StatusCode"] == "10"
    assert values[f"{APP}/ipsdo:TrademarkRegistrationCode"] == "01"
    assert RESPONSE in values
    assert SIG in values
    assert "ipcdo:RefusalDetails" not in values
    assert validation.is_valid, [(item.code, item.rule_id, item.field_path, item.message) for item in validation.issues]
    assert validation.is_complete
    assert len(validation.rule_evaluations) == 40
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    assert {int(item.rule_id.split(".REQ.")[1].split(".")[0]) for item in validation.rule_evaluations} == MAPPED
    assert all(item.rule_id.startswith(MESSAGE + ".") for item in validation.rule_evaluations)

    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.initiating_message == MESSAGE
    assert transaction.response_messages == ("P.SP.02.MSG.002",)
    assert transaction.procedure_code == "P.SP.02.PRC.007"
    assert transaction.initiating_operation == "P.SP.02.OPR.025"
    assert transaction.responding_operation == "P.SP.02.OPR.026"
    assert transaction.initiating_participant == "P.SP.02.ACT.002"
    assert transaction.responding_participant == "P.SP.02.ACT.001"
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(f"/{MESSAGE}")


def _mutate_req1_zero(root, structure):
    root.remove(_required(root, structure, "ipcdo", "TrademarkApplicationDetails"))


def _mutate_req1_two(root, structure):
    root.append(deepcopy(_required(root, structure, "ipcdo", "TrademarkApplicationDetails")))


def _mutate_req2(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    status = _required(app, structure, "ipcdo", "IPEntityStatusDetails")
    _required(status, structure, "csdo", "StatusCode").text = "99"


def _mutate_req6(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, structure, "ipsdo", "ApplicationReceiptDate"))


def _mutate_req7(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    _required(party, structure, "csdo", "UnifiedCountryCode").set("codeListId", "WRONG")


def _mutate_req8(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    address = _required(party, structure, "ccdo", "SubjectAddressDetails")
    address.remove(_required(address, structure, "csdo", "CityName"))


def _mutate_req9(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    comm = _required(party, structure, "ccdo", "CommunicationDetails")
    comm.remove(_required(comm, structure, "csdo", "CommunicationChannelId"))


def _mutate_req10(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    comm = _required(party, structure, "ccdo", "CommunicationDetails")
    _required(comm, structure, "csdo", "CommunicationChannelCode").text = "PH"


def _mutate_req11(root, structure):
    _add_direct_authority(_required(root, structure, "ipcdo", "TrademarkApplicationDetails"), structure, country=False)


def _mutate_req12(root, structure):
    _add_direct_authority(_required(root, structure, "ipcdo", "TrademarkApplicationDetails"), structure, address_kind="3")


def _mutate_req14(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    _required(party, structure, "ipsdo", "IPPartyKindCode").text = "RE"


def _mutate_req15(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    party.remove(_required(party, structure, "ccdo", "CommunicationDetails"))


def _mutate_req21(root, structure):
    _add_party(_required(root, structure, "ipcdo", "TrademarkApplicationDetails"), structure, "PA", omit="attorney")


def _mutate_req22(root, structure):
    _add_party(_required(root, structure, "ipcdo", "TrademarkApplicationDetails"), structure, "RE", omit="address")


def _mutate_req23(root, structure):
    _add_correspondence(_required(root, structure, "ipcdo", "TrademarkApplicationDetails"), structure, kind="2")


def _mutate_req24(root, structure):
    _add_correspondence(_required(root, structure, "ipcdo", "TrademarkApplicationDetails"), structure, country="US")


def _mutate_req25(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, structure, "ipcdo", "TrademarkDetails"))


def _mutate_req27(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    tm = _required(app, structure, "ipcdo", "TrademarkDetails")
    _required(tm, structure, "ipsdo", "TrademarkKindCode").text = "140"


def _mutate_req28(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    tm = _required(app, structure, "ipcdo", "TrademarkDetails")
    _required(tm, structure, "ipsdo", "CollectiveMarkIndicator").text = "2"


def _mutate_req29(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    goods = _required(app, structure, "ipcdo", "GoodsBaseDetails")
    goods.remove(_required(goods, structure, "ipsdo", "GoodsClassCode"))


def _mutate_req30(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, structure, "ipsdo", "TrademarkRegistrationCode"))


def _mutate_req31(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, structure, "ipcdo", "SignatureDetails"))


def _add_valid_officer(sig, structure, *, position=True, communication=False):
    officer = _child(sig, structure, "ipcdo", "OfficerDetails")
    full = _child(officer, structure, "ccdo", "FullNameDetails")
    _child(full, structure, "csdo", "FirstName", "Петр")
    _child(full, structure, "csdo", "LastName", "Петров")
    if position:
        _child(officer, structure, "csdo", "PositionName", "Эксперт")
    if communication:
        _add_comm(officer, structure)
    return officer


def _mutate_req32(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    sig = _required(app, structure, "ipcdo", "SignatureDetails")
    _add_valid_officer(sig, structure)


def _mutate_req33(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    sig = _required(app, structure, "ipcdo", "SignatureDetails")
    sig.remove(_required(sig, structure, "ccdo", "FullNameDetails"))
    _add_valid_officer(sig, structure, position=False)


def _mutate_req34(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, structure, "ipcdo", "ApplicantComplainResponseDetails"))


def _mutate_req35(root, structure):
    refusal = _child(root, structure, "ipcdo", "RefusalDetails")
    _child(refusal, structure, "csdo", "EventDate", "2026-09-30")


def _mutate_req36(root, structure):
    resource = _required(root, structure, "ccdo", "ResourceItemStatusDetails")
    validity = _required(resource, structure, "ccdo", "ValidityPeriodDetails")
    validity.remove(_required(validity, structure, "csdo", "StartDateTime"))


def _mutate_req37(root, structure):
    resource = _required(root, structure, "ccdo", "ResourceItemStatusDetails")
    validity = _required(resource, structure, "ccdo", "ValidityPeriodDetails")
    _child(validity, structure, "csdo", "EndDateTime", "2026-09-30T14:00:00+03:00")


INVALID_FULL_CASES = [
    (1, _mutate_req1_zero), (1, _mutate_req1_two), (2, _mutate_req2),
    (6, _mutate_req6), (7, _mutate_req7), (8, _mutate_req8), (9, _mutate_req9),
    (10, _mutate_req10), (11, _mutate_req11), (12, _mutate_req12),
    (14, _mutate_req14), (15, _mutate_req15), (21, _mutate_req21), (22, _mutate_req22),
    (23, _mutate_req23), (24, _mutate_req24), (25, _mutate_req25), (27, _mutate_req27),
    (28, _mutate_req28), (29, _mutate_req29), (30, _mutate_req30), (31, _mutate_req31),
    (32, _mutate_req32), (33, _mutate_req33), (34, _mutate_req34), (35, _mutate_req35),
    (36, _mutate_req36), (37, _mutate_req37),
]


@pytest.mark.parametrize(("requirement", "mutator"), INVALID_FULL_CASES, ids=[f"req{code}_{index}" for index, (code, _) in enumerate(INVALID_FULL_CASES)])
def test_each_full_executable_requirement_has_independent_production_xml_invalid_proof(requirement, mutator):
    assert requirement in FULL
    engine, structure, parsed = _build_valid_parsed()
    mutator(parsed, structure)
    values, _, validation = _extract_validate(engine, structure, parsed)
    assert not validation.is_valid
    _target_fails(engine, requirement, values)


@pytest.mark.parametrize("code", [3, 4, 5])
def test_each_safe_partial_local_fragment_has_independent_negative_proof(code):
    engine, structure, parsed = _build_valid_parsed()
    app = _required(parsed, structure, "ipcdo", "TrademarkApplicationDetails")
    if code == 3:
        _child(app, structure, "ipsdo", "IPDocKindCode", "00033")
    elif code == 4:
        _required(app, structure, "ipsdo", "IPDocKindName").text = "WRONG"
    else:
        app.remove(_required(app, structure, "ipsdo", "TrademarkApplicationId"))
    values, _, _ = _extract_validate(engine, structure, parsed)
    _target_fails(engine, code, values)


def test_nested_complaint_patent_authority_does_not_satisfy_or_trigger_direct_authority_rules():
    engine, structure, parsed = _build_valid_parsed()
    app = _required(parsed, structure, "ipcdo", "TrademarkApplicationDetails")
    complaint = _child(app, structure, "ipcdo", "ComplaintDetails")
    nested = _child(complaint, structure, "ipcdo", "PatentAuthorityDetails")
    _child(nested, structure, "ipsdo", "OriginOfficeIndicator", "1")

    values, extraction_issues, _ = _extract_validate(engine, structure, parsed)
    assert not extraction_issues
    assert f"{APP}/ipcdo:ComplaintDetails/ipcdo:PatentAuthorityDetails" in values
    assert f"{APP}/ipcdo:PatentAuthorityDetails" not in values
    for code in (11, 12):
        statuses = [StructuredRuleEvaluator().evaluate(rule, values).status for rule in _target_rules(engine, code)]
        assert statuses
        assert all(status is RuleStatus.PASS for status in statuses)


def test_same_r002_values_execute_only_rules_for_requested_message_code():
    engine, structure, parsed = _build_valid_parsed()
    _, extraction_issues, result033 = _extract_validate(engine, structure, parsed)
    assert not extraction_issues

    ids031 = {
        rule["rule_id"]
        for rule in engine.rules["P.SP.02.MSG.031"].structured_rules
        if rule.get("applies_to_structure") == STRUCTURE and ".T48." in rule["rule_id"]
    }
    ids032 = {rule["rule_id"] for rule in engine.rules["P.SP.02.MSG.032"].structured_rules}
    ids033_defined = {rule["rule_id"] for rule in engine.rules[MESSAGE].structured_rules}
    ids033_executed = {item.rule_id for item in result033.rule_evaluations}

    assert ids031 and ids032 and ids033_defined and ids033_executed
    assert all(rule_id.startswith("P.SP.02.MSG.031.") for rule_id in ids031)
    assert all(rule_id.startswith("P.SP.02.MSG.032.") for rule_id in ids032)
    assert all(rule_id.startswith("P.SP.02.MSG.033.") for rule_id in ids033_executed)
    assert ids033_executed == ids033_defined
    assert ids031.isdisjoint(ids032)
    assert ids031.isdisjoint(ids033_executed)
    assert ids032.isdisjoint(ids033_executed)
