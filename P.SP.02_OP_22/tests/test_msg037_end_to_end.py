from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.037"
STRUCTURE = "R.IP.SP.02.002"
TRANSACTION = "P.SP.02.TRN.032"
APP = "ipcdo:TrademarkApplicationDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
DESC = f"{TM}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
MAPPED = {1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31}


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": STRUCTURE,
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000037",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T12:00:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-30",
        f"{APP}/ipsdo:TrademarkApplicationId": "APP-037",
        STATUS: [None],
        f"{STATUS}/csdo:StatusCode": "31",
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
        COMM: [""],
        f"{COMM}/csdo:CommunicationChannelCode": "EM",
        f"{COMM}/csdo:CommunicationChannelId": "applicant@example.test",
        TM: [None],
        DESC: [""],
        f"{DESC}/csdo:DescriptionText": "Описание",
        f"{TM}/ipsdo:TrademarkKindCode": "110",
        f"{TM}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TM}/ipsdo:CollectiveMarkIndicator": "0",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "01",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T12:01:00+03:00",
        f"{VALIDITY}/csdo:EndDateTime": "2026-09-30T13:00:00+03:00",
    }


def _q(structure, prefix, local):
    return f"{{{structure.imported_namespaces[prefix]}}}{local}"


def _first(parent, structure, prefix, local):
    return parent.find(_q(structure, prefix, local))


def _required(parent, structure, prefix, local):
    node = _first(parent, structure, prefix, local)
    assert node is not None, (prefix, local)
    return node


def _child(parent, structure, prefix, local, text=None, attrs=None):
    node = ET.SubElement(parent, ET.QName(structure.imported_namespaces[prefix], local))
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
    _child(party, structure, "ipsdo", "IPSubjectName", f"Party {role}")
    if omit != "address":
        _add_address(party, structure)
    if omit != "communication":
        _add_comm(party, structure)
    if role == "PA" and omit != "attorney":
        _child(party, structure, "ipsdo", "PatentAttorneyId", "PA-1")
    return party


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
    base = f"{MESSAGE}.T55.REQ.{code}"
    return [
        r for r in engine.rules[MESSAGE].structured_rules
        if r["rule_id"] == base or r["rule_id"].startswith(base + ".")
    ]


def _target_fails(engine, code, values):
    rules = _target_rules(engine, code)
    assert rules, code
    statuses = [StructuredRuleEvaluator().evaluate(rule, values).status for rule in rules]
    assert RuleStatus.FAIL in statuses, (code, statuses)


def test_valid_msg037_build_serialize_parse_extract_validate_pipeline():
    engine, structure, parsed = _build_valid_parsed()
    values, extraction_issues, validation = _extract_validate(engine, structure, parsed)
    assert not extraction_issues, [(i.code, i.field_path, i.message) for i in extraction_issues]
    assert parsed.tag == "{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails"
    assert values[f"{STATUS}/csdo:StatusCode"] == "31"
    assert values[f"{VALIDITY}/csdo:StartDateTime"] == "2026-09-30T12:01:00+03:00"
    assert values[f"{VALIDITY}/csdo:EndDateTime"] == "2026-09-30T13:00:00+03:00"
    assert validation.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in validation.issues]
    assert validation.is_complete
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    codes = {int(item.rule_id.split(".REQ.", 1)[1].split(".", 1)[0]) for item in validation.rule_evaluations}
    assert codes == MAPPED

    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.initiating_message == MESSAGE
    assert transaction.response_messages == ("P.SP.02.MSG.002",)
    assert transaction.initiating_operation == "P.SP.02.OPR.050"
    assert transaction.responding_operation == "P.SP.02.OPR.051"
    assert transaction.initiating_participant == "P.SP.02.ACT.001"
    assert transaction.responding_participant == "P.SP.02.ACT.002"
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(f"/{MESSAGE}")


def _req1_zero(root, structure):
    root.remove(_required(root, structure, "ipcdo", "TrademarkApplicationDetails"))


def _req1_two(root, structure):
    root.append(deepcopy(_required(root, structure, "ipcdo", "TrademarkApplicationDetails")))


def _req4(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, structure, "ipsdo", "TrademarkApplicationId"))


def _req5_missing(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, structure, "ipcdo", "IPEntityStatusDetails"))


def _req5_wrong(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    status = _required(app, structure, "ipcdo", "IPEntityStatusDetails")
    _required(status, structure, "csdo", "StatusCode").text = "30"


def _req5_attr(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    status = _required(app, structure, "ipcdo", "IPEntityStatusDetails")
    _required(status, structure, "csdo", "StatusCode").set("codeListId", "STATUS")


def _req6(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, structure, "ipsdo", "ApplicationReceiptDate"))


def _req7(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    _required(party, structure, "csdo", "UnifiedCountryCode").set("codeListId", "WRONG")


def _req8(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    address = _required(party, structure, "ccdo", "SubjectAddressDetails")
    address.remove(_required(address, structure, "csdo", "CityName"))


def _req9(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    comm = _required(party, structure, "ccdo", "CommunicationDetails")
    comm.remove(_required(comm, structure, "csdo", "CommunicationChannelId"))


def _req10(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    comm = _required(party, structure, "ccdo", "CommunicationDetails")
    _required(comm, structure, "csdo", "CommunicationChannelCode").text = "PH"


def _req11(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    authority = _child(app, structure, "ipcdo", "PatentAuthorityDetails")
    _child(authority, structure, "csdo", "AuthorityName", "Office")
    _add_address(authority, structure, kind="2")


def _req12(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    authority = _child(app, structure, "ipcdo", "PatentAuthorityDetails")
    _child(authority, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
    _child(authority, structure, "csdo", "AuthorityName", "Office")
    _add_address(authority, structure, kind="3")


def _req14(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    _required(party, structure, "ipsdo", "IPPartyKindCode").text = "RE"


def _req15(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    party = _required(app, structure, "ipcdo", "IPPartyDetails")
    party.remove(_required(party, structure, "ccdo", "CommunicationDetails"))


def _req21(root, structure):
    _add_party(_required(root, structure, "ipcdo", "TrademarkApplicationDetails"), structure, "PA", omit="attorney")


def _req22(root, structure):
    _add_party(_required(root, structure, "ipcdo", "TrademarkApplicationDetails"), structure, "RE", omit="address")


def _correspondence(root, structure, *, kind="3", country="RU"):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    corr = _child(app, structure, "ipcdo", "CorrespondenceAddressDetails")
    _add_address(corr, structure, kind=kind, country=country)


def _req23(root, structure):
    _correspondence(root, structure, kind="2")


def _req24(root, structure):
    _correspondence(root, structure, country="US")


def _req25(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, structure, "ipcdo", "TrademarkDetails"))


def _req27(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    tm = _required(app, structure, "ipcdo", "TrademarkDetails")
    _required(tm, structure, "ipsdo", "TrademarkKindCode").text = "140"


def _req28(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    tm = _required(app, structure, "ipcdo", "TrademarkDetails")
    _required(tm, structure, "ipsdo", "CollectiveMarkIndicator").text = "2"


def _req29(root, structure):
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    goods = _required(app, structure, "ipcdo", "GoodsBaseDetails")
    goods.remove(_required(goods, structure, "ipsdo", "GoodsClassCode"))


def _req30(root, structure):
    resource = _required(root, structure, "ccdo", "ResourceItemStatusDetails")
    validity = _required(resource, structure, "ccdo", "ValidityPeriodDetails")
    validity.remove(_required(validity, structure, "csdo", "StartDateTime"))


def _req31(root, structure):
    resource = _required(root, structure, "ccdo", "ResourceItemStatusDetails")
    validity = _required(resource, structure, "ccdo", "ValidityPeriodDetails")
    validity.remove(_required(validity, structure, "csdo", "EndDateTime"))


INVALID_CASES = [
    (1, _req1_zero), (1, _req1_two), (4, _req4),
    (5, _req5_missing), (5, _req5_wrong), (5, _req5_attr),
    (6, _req6), (7, _req7), (8, _req8), (9, _req9), (10, _req10),
    (11, _req11), (12, _req12), (14, _req14), (15, _req15),
    (21, _req21), (22, _req22), (23, _req23), (24, _req24),
    (25, _req25), (27, _req27), (28, _req28), (29, _req29),
    (30, _req30), (31, _req31),
]


@pytest.mark.parametrize(("requirement", "mutator"), INVALID_CASES, ids=[f"req{r}_{i}" for i, (r, _) in enumerate(INVALID_CASES)])
def test_each_executable_requirement_has_production_xml_negative_proof(requirement, mutator):
    engine, structure, parsed = _build_valid_parsed()
    mutator(parsed, structure)
    values, _, validation = _extract_validate(engine, structure, parsed)
    assert not validation.is_valid
    _target_fails(engine, requirement, values)


def test_message_isolation_keeps_msg037_rules_out_of_other_message_validation():
    engine, structure, parsed = _build_valid_parsed()
    values, extraction_issues, validation37 = _extract_validate(engine, structure, parsed)
    assert not extraction_issues
    validation34 = engine.validate_body("P.SP.02.MSG.034", values, mode=GenerationMode.TEST)
    assert validation37.rule_evaluations
    assert validation34.rule_evaluations
    assert all(x.rule_id.startswith(MESSAGE + ".") for x in validation37.rule_evaluations)
    assert all(x.rule_id.startswith("P.SP.02.MSG.034.") for x in validation34.rule_evaluations)
    assert {x.rule_id for x in validation37.rule_evaluations}.isdisjoint({x.rule_id for x in validation34.rule_evaluations})


def test_unmapped_requirements_never_produce_synthetic_evaluations():
    engine, structure, parsed = _build_valid_parsed()
    _, _, validation = _extract_validate(engine, structure, parsed)
    codes = {int(x.rule_id.split(".REQ.", 1)[1].split(".", 1)[0]) for x in validation.rule_evaluations}
    assert codes.isdisjoint({2, 3, 13, 16, 17, 18, 19, 20, 26})
