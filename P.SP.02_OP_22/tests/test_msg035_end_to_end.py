from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.035"
STRUCTURE = "R.IP.SP.02.002"
TRANSACTION = "P.SP.02.TRN.030"
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
DESC = f"{TM}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
FULL = {1, 4, 5, *range(6, 13), 14, 15, *range(21, 26), 27, 28, 29}
PARTIAL = {2, 3}
MAPPED = FULL | PARTIAL


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": STRUCTURE,
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000035",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T15:00:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:IPDocKindCode": "LOCAL-PRESENT-ONLY",
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-30",
        f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000035",
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
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T15:01:00+03:00",
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
    _child(party, structure, "ipsdo", "IPSubjectName", f"Party {role}")
    if omit != "address":
        _add_address(party, structure)
    if omit != "communication":
        _add_comm(party, structure)
    if role == "PA" and omit != "attorney":
        _child(party, structure, "ipsdo", "PatentAttorneyId", "PA-035")
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
    values, issues = engine.body_provider._values_from_element(structure, reparsed)
    result = engine.validate_body(message, values, mode=GenerationMode.TEST)
    return values, issues, result


def _target_rules(engine, code):
    prefix = f"{MESSAGE}.T53.REQ.{code}"
    return [r for r in engine.rules[MESSAGE].structured_rules if r["rule_id"] == prefix or r["rule_id"].startswith(prefix + ".")]


def _target_fails(engine, code, values):
    statuses = [StructuredRuleEvaluator().evaluate(r, values).status for r in _target_rules(engine, code)]
    assert statuses and RuleStatus.FAIL in statuses, (code, statuses)


def _rule_code(rule_id):
    return int(rule_id.split(".REQ.", 1)[1].split(".", 1)[0])


def test_valid_msg035_build_serialize_parse_extract_validate_roundtrip_and_transaction():
    engine, structure, parsed = _build_valid_parsed()
    values, extraction_issues, validation = _extract_validate(engine, structure, parsed)
    assert parsed.tag == "{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails"
    assert not extraction_issues
    assert values[f"{APP}/ipsdo:IPDocKindCode"] == "LOCAL-PRESENT-ONLY"
    assert values[f"{VALIDITY}/csdo:StartDateTime"] == "2026-09-30T15:01:00+03:00"
    assert f"{VALIDITY}/csdo:EndDateTime" not in values
    assert validation.is_valid, [(x.rule_id, x.message) for x in validation.issues]
    assert validation.is_complete
    assert len(validation.rule_evaluations) == 24
    assert all(x.status is RuleStatus.PASS for x in validation.rule_evaluations)
    assert {_rule_code(x.rule_id) for x in validation.rule_evaluations} == MAPPED

    tx = engine.get_transaction(TRANSACTION)
    assert tx.initiating_message == MESSAGE
    assert tx.response_messages == ("P.SP.02.MSG.002",)
    assert tx.procedure_code == "P.SP.02.PRC.011"
    assert tx.initiating_operation == "P.SP.02.OPR.044"
    assert tx.responding_operation == "P.SP.02.OPR.045"
    assert tx.initiating_participant == "P.SP.02.ACT.002"
    assert tx.responding_participant == "P.SP.02.ACT.001"
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(f"/{MESSAGE}")


def _m1_zero(root, s): root.remove(_required(root, s, "ipcdo", "TrademarkApplicationDetails"))
def _m1_two(root, s): root.append(deepcopy(_required(root, s, "ipcdo", "TrademarkApplicationDetails")))
def _m2(root, s):
    app = _required(root, s, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, s, "ipsdo", "IPDocKindCode"))
def _m3(root, s):
    app = _required(root, s, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, s, "ipsdo", "TrademarkApplicationId"))
def _m4(root, s):
    validity = _required(_required(root, s, "ccdo", "ResourceItemStatusDetails"), s, "ccdo", "ValidityPeriodDetails")
    validity.remove(_required(validity, s, "csdo", "StartDateTime"))
def _m5(root, s):
    validity = _required(_required(root, s, "ccdo", "ResourceItemStatusDetails"), s, "ccdo", "ValidityPeriodDetails")
    _child(validity, s, "csdo", "EndDateTime", "2026-09-30T16:00:00+03:00")
def _m6(root, s):
    app = _required(root, s, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, s, "ipsdo", "ApplicationReceiptDate"))
def _m7(root, s):
    party = _required(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, "ipcdo", "IPPartyDetails")
    _required(party, s, "csdo", "UnifiedCountryCode").set("codeListId", "WRONG")
def _m8(root, s):
    party = _required(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, "ipcdo", "IPPartyDetails")
    address = _required(party, s, "ccdo", "SubjectAddressDetails")
    address.remove(_required(address, s, "csdo", "CityName"))
def _m9(root, s):
    party = _required(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, "ipcdo", "IPPartyDetails")
    comm = _required(party, s, "ccdo", "CommunicationDetails")
    comm.remove(_required(comm, s, "csdo", "CommunicationChannelId"))
def _m10(root, s):
    party = _required(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, "ipcdo", "IPPartyDetails")
    _required(_required(party, s, "ccdo", "CommunicationDetails"), s, "csdo", "CommunicationChannelCode").text = "PH"
def _m11(root, s): _add_direct_authority(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, country=False)
def _m12(root, s): _add_direct_authority(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, address_kind="3")
def _m14(root, s):
    party = _required(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, "ipcdo", "IPPartyDetails")
    _required(party, s, "ipsdo", "IPPartyKindCode").text = "RE"
def _m15(root, s):
    party = _required(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, "ipcdo", "IPPartyDetails")
    party.remove(_required(party, s, "ccdo", "CommunicationDetails"))
def _m21(root, s): _add_party(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, "PA", omit="attorney")
def _m22(root, s): _add_party(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, "RE", omit="address")
def _m23(root, s): _add_correspondence(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, kind="2")
def _m24(root, s): _add_correspondence(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, country="US")
def _m25(root, s):
    app = _required(root, s, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, s, "ipcdo", "TrademarkDetails"))
def _m27(root, s):
    tm = _required(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, "ipcdo", "TrademarkDetails")
    _required(tm, s, "ipsdo", "TrademarkKindCode").text = "140"
def _m28(root, s):
    tm = _required(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, "ipcdo", "TrademarkDetails")
    _required(tm, s, "ipsdo", "CollectiveMarkIndicator").text = "2"
def _m29(root, s):
    goods = _required(_required(root, s, "ipcdo", "TrademarkApplicationDetails"), s, "ipcdo", "GoodsBaseDetails")
    goods.remove(_required(goods, s, "ipsdo", "GoodsClassCode"))


INVALID_CASES = [
    (1, _m1_zero), (1, _m1_two), (2, _m2), (3, _m3), (4, _m4), (5, _m5),
    (6, _m6), (7, _m7), (8, _m8), (9, _m9), (10, _m10), (11, _m11), (12, _m12),
    (14, _m14), (15, _m15), (21, _m21), (22, _m22), (23, _m23), (24, _m24),
    (25, _m25), (27, _m27), (28, _m28), (29, _m29),
]


@pytest.mark.parametrize(("requirement", "mutator"), INVALID_CASES, ids=[f"req{c}_{i}" for i, (c, _) in enumerate(INVALID_CASES)])
def test_each_executable_requirement_has_independent_production_xml_negative_proof(requirement, mutator):
    engine, structure, parsed = _build_valid_parsed()
    mutator(parsed, structure)
    values, _, validation = _extract_validate(engine, structure, parsed)
    assert not validation.is_valid
    _target_fails(engine, requirement, values)


@pytest.mark.parametrize("mode", ["nested", "wrong_namespace"])
def test_req2_wrong_owner_or_wrong_namespace_code_cannot_satisfy_direct_code_requirement(mode):
    engine, structure, parsed = _build_valid_parsed()
    app = _required(parsed, structure, "ipcdo", "TrademarkApplicationDetails")
    app.remove(_required(app, structure, "ipsdo", "IPDocKindCode"))
    if mode == "nested":
        doc = _child(app, structure, "ipcdo", "AccompanyingDocumentsDetails")
        _child(doc, structure, "ipsdo", "IPDocKindCode", "NESTED")
    else:
        _child(app, structure, "ipsdo", "IPDocKindCode", "WRONG-NS", namespace="urn:wrong:ipsdo")
    values, extraction_issues, _ = _extract_validate(engine, structure, parsed)
    assert not extraction_issues
    assert f"{APP}/ipsdo:IPDocKindCode" not in values
    _target_fails(engine, 2, values)


def test_req4_req5_wrong_namespace_validity_fields_do_not_satisfy_or_trigger_rules():
    engine, structure, parsed = _build_valid_parsed()
    validity = _required(_required(parsed, structure, "ccdo", "ResourceItemStatusDetails"), structure, "ccdo", "ValidityPeriodDetails")
    validity.remove(_required(validity, structure, "csdo", "StartDateTime"))
    _child(validity, structure, "csdo", "StartDateTime", "WRONG", namespace="urn:wrong:csdo")
    _child(validity, structure, "csdo", "EndDateTime", "WRONG", namespace="urn:wrong:csdo")
    values, extraction_issues, _ = _extract_validate(engine, structure, parsed)
    assert not extraction_issues
    _target_fails(engine, 4, values)
    assert all(StructuredRuleEvaluator().evaluate(r, values).status is RuleStatus.PASS for r in _target_rules(engine, 5))


def test_message_rule_ids_are_isolated_for_same_r002_messages():
    engine, structure, parsed = _build_valid_parsed()
    values, extraction_issues, result035 = _extract_validate(engine, structure, parsed)
    assert not extraction_issues
    ids035 = {x.rule_id for x in result035.rule_evaluations}
    assert ids035 == {r["rule_id"] for r in engine.rules[MESSAGE].structured_rules}
    assert all(x.startswith(MESSAGE + ".") for x in ids035)
    for code in ("P.SP.02.MSG.033", "P.SP.02.MSG.034", "P.SP.02.MSG.036"):
        defined = {r["rule_id"] for r in engine.rules[code].structured_rules}
        assert defined
        assert ids035.isdisjoint(defined)
