from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.033"
STRUCTURE = "R.IP.SP.02.002"
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
SIG = f"{APP}/ipcdo:SignatureDetails"
OFFICER = f"{SIG}/ipcdo:OfficerDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _child(parent, structure, prefix, local, text=None, attrs=None, namespace=None):
    ns = namespace if namespace is not None else structure.imported_namespaces[prefix]
    node = ET.SubElement(parent, ET.QName(ns, local))
    if text is not None:
        node.text = text
    for key, value in (attrs or {}).items():
        node.set(key, value)
    return node


def _parsed_values(builder):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues, [(item.code, item.field_path, item.message) for item in issues]
    return engine, structure, values


def _rules(engine, code):
    rid = f"{MESSAGE}.T51.REQ.{code}"
    rules = [rule for rule in engine.rules[MESSAGE].structured_rules if rule["rule_id"] == rid]
    assert rules, code
    return rules


def _statuses(engine, code, values):
    return [StructuredRuleEvaluator().evaluate(rule, values).status for rule in _rules(engine, code)]


def _assert_pass(engine, code, values):
    statuses = _statuses(engine, code, values)
    assert all(status is RuleStatus.PASS for status in statuses), statuses


def _assert_fail(engine, code, values):
    statuses = _statuses(engine, code, values)
    assert RuleStatus.FAIL in statuses, statuses


def _address(parent, structure, suffix, *, omit=None):
    address = _child(parent, structure, "ccdo", "SubjectAddressDetails")
    fields = (
        ("csdo", "AddressKindCode", "2"),
        ("csdo", "UnifiedCountryCode", "RU"),
        ("csdo", "CityName", f"City {suffix}"),
        ("csdo", "StreetName", f"Street {suffix}"),
        ("csdo", "BuildingNumberId", str(suffix + 1)),
    )
    for prefix, local, text in fields:
        if local == omit:
            continue
        attrs = {"codeListId": "ВОИС ST.3"} if local == "UnifiedCountryCode" else None
        _child(address, structure, prefix, local, text, attrs=attrs)
    return address


def _communication(parent, structure, suffix, *, omit=None):
    comm = _child(parent, structure, "ccdo", "CommunicationDetails")
    if omit != "CommunicationChannelCode":
        _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
    if omit != "CommunicationChannelId":
        _child(comm, structure, "csdo", "CommunicationChannelId", f"user{suffix}@example.test")
    return comm


def _party(app, structure, role, suffix, *, omit=None):
    party = _child(app, structure, "ipcdo", "IPPartyDetails")
    _child(party, structure, "ipsdo", "IPPartyKindCode", role)
    if omit != "country":
        _child(party, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
    if omit != "name":
        _child(party, structure, "ipsdo", "IPSubjectName", f"Party {suffix}")
    if omit != "address":
        _address(party, structure, suffix)
    if omit != "communication":
        _communication(party, structure, suffix)
    if role == "PA" and omit != "attorney":
        _child(party, structure, "ipsdo", "PatentAttorneyId", f"PA-{suffix}")
    return party


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_req8_repeatable_subject_addresses_preserve_parent_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            party = _child(app, structure, "ipcdo", "IPPartyDetails")
            _child(party, structure, "ipsdo", "IPPartyKindCode", "RE")
            _address(party, structure, index, omit="CityName" if index == bad_index else None)

    engine, _, values = _parsed_values(build)
    cities = values[f"{PARTY}/ccdo:SubjectAddressDetails/csdo:CityName"]
    assert len(cities) == 2
    if bad_index is None:
        assert cities == ["City 0", "City 1"]
        _assert_pass(engine, 8, values)
    else:
        assert cities[bad_index] is None
        _assert_fail(engine, 8, values)


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_req9_repeatable_communications_preserve_parent_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            party = _child(app, structure, "ipcdo", "IPPartyDetails")
            _child(party, structure, "ipsdo", "IPPartyKindCode", "RE")
            _communication(party, structure, index, omit="CommunicationChannelId" if index == bad_index else None)

    engine, _, values = _parsed_values(build)
    ids = values[f"{PARTY}/ccdo:CommunicationDetails/csdo:CommunicationChannelId"]
    assert len(ids) == 2
    if bad_index is None:
        _assert_pass(engine, 9, values)
    else:
        assert ids[bad_index] is None
        _assert_fail(engine, 9, values)


@pytest.mark.parametrize("roles", [("AP", "RE"), ("RE", "AP")])
def test_req15_ap_party_children_are_checked_in_same_filtered_parent_in_both_orders(roles):
    def good(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index, role in enumerate(roles):
            _party(app, structure, role, index)

    engine, _, values = _parsed_values(good)
    _assert_pass(engine, 15, values)

    def bad(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index, role in enumerate(roles):
            _party(app, structure, role, index, omit="communication" if role == "AP" else None)

    engine, _, values = _parsed_values(bad)
    _assert_fail(engine, 15, values)


def _trademark(app, structure, index, *, missing=None):
    tm = _child(app, structure, "ipcdo", "TrademarkDetails")
    if index == 0:
        _child(tm, structure, "ipsdo", "TrademarkKindCode", "140")
        _child(tm, structure, "ipsdo", "TrademarkKindName", "Unrelated name")
    else:
        _child(tm, structure, "ipsdo", "TrademarkKindCode", "110")
        _child(tm, structure, "ipsdo", "TrademarkKindName", "Изобразительный знак")
    if missing != "TrademarkPicture":
        _child(tm, structure, "ipsdo", "TrademarkPicture", f"IMAGE-{index}")
    if missing != "TrademarkColourName":
        _child(tm, structure, "ipsdo", "TrademarkColourName", f"Colour {index}")
    return tm


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_req27_repeatable_trademarks_do_not_cross_satisfy_picture_and_colour(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        # Structure says TrademarkDetails max=1, but evaluator contexts must still preserve same-parent
        # behavior for a repeated extracted shape; this mirrors production extraction alignment coverage.
        for index in range(2):
            _trademark(app, structure, index, missing="TrademarkColourName" if index == bad_index else None)

    engine, _, values = _parsed_values(build)
    colours = values[f"{TM}/ipsdo:TrademarkColourName"]
    assert len(colours) == 2
    if bad_index is None:
        _assert_pass(engine, 27, values)
    else:
        assert colours[bad_index] is None
        _assert_fail(engine, 27, values)


def _goods(app, structure, index, *, missing=None):
    goods = _child(app, structure, "ipcdo", "GoodsBaseDetails")
    for prefix, local, text in (
        ("ipsdo", "GoodsClassCode", f"{index + 1:02d}"),
        ("ipsdo", "GoodsClassName", f"Class {index}"),
        ("ipsdo", "GoodsName", f"Goods {index}"),
    ):
        if local != missing:
            _child(goods, structure, prefix, local, text)
    return goods


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_req29_repeatable_goods_preserve_parent_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            _goods(app, structure, index, missing="GoodsClassCode" if index == bad_index else None)

    engine, _, values = _parsed_values(build)
    codes = values[f"{GOODS}/ipsdo:GoodsClassCode"]
    assert len(codes) == 2
    if bad_index is None:
        _assert_pass(engine, 29, values)
    else:
        assert codes[bad_index] is None
        _assert_fail(engine, 29, values)


def _direct_name(sig, structure, suffix="D"):
    full = _child(sig, structure, "ccdo", "FullNameDetails")
    _child(full, structure, "csdo", "FirstName", f"Direct{suffix}")
    _child(full, structure, "csdo", "LastName", f"Name{suffix}")
    return full


def _officer(sig, structure, suffix="O", *, omit=None, with_communication=False):
    officer = _child(sig, structure, "ipcdo", "OfficerDetails")
    full = _child(officer, structure, "ccdo", "FullNameDetails")
    if omit != "FirstName":
        _child(full, structure, "csdo", "FirstName", f"Officer{suffix}")
    if omit != "LastName":
        _child(full, structure, "csdo", "LastName", f"Name{suffix}")
    if omit != "PositionName":
        _child(officer, structure, "csdo", "PositionName", "Expert")
    if with_communication:
        _communication(officer, structure, 90)
    return officer


def _signature(app, structure, branch, suffix="0", **kwargs):
    sig = _child(app, structure, "ipcdo", "SignatureDetails")
    if branch == "direct":
        _direct_name(sig, structure, suffix)
    elif branch == "officer":
        _officer(sig, structure, suffix, **kwargs)
    elif branch == "both":
        _direct_name(sig, structure, suffix)
        _officer(sig, structure, suffix, **kwargs)
    return sig


def test_signature_officer_only_passes_same_parent_rules():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _signature(app, structure, "officer")

    engine, _, values = _parsed_values(build)
    for code in (31, 32, 33):
        _assert_pass(engine, code, values)


def test_signature_direct_fullname_only_passes_and_nested_officer_qname_is_not_required():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _signature(app, structure, "direct")

    engine, _, values = _parsed_values(build)
    assert f"{SIG}/ccdo:FullNameDetails" in values
    assert OFFICER not in values
    for code in (31, 32, 33):
        _assert_pass(engine, code, values)


def test_two_signature_parents_may_use_different_branches_without_cross_parent_leakage():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _signature(app, structure, "officer", "A")
        _signature(app, structure, "direct", "B")

    engine, _, values = _parsed_values(build)
    assert len(values[SIG]) == 2
    for code in (31, 32, 33):
        _assert_pass(engine, code, values)


def test_both_signature_branches_in_same_parent_fail_mutual_exclusion():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _signature(app, structure, "both")

    engine, _, values = _parsed_values(build)
    _assert_fail(engine, 31, values)
    _assert_fail(engine, 32, values)


def test_officer_missing_position_name_fails_req33():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _signature(app, structure, "officer", omit="PositionName")

    engine, _, values = _parsed_values(build)
    _assert_fail(engine, 33, values)


def test_officer_communication_details_fails_req33():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _signature(app, structure, "officer", with_communication=True)

    engine, _, values = _parsed_values(build)
    _assert_fail(engine, 33, values)


def test_req2_wrong_namespace_statuscode_does_not_satisfy_exact_qname():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        status = _child(app, structure, "ipcdo", "IPEntityStatusDetails")
        _child(status, structure, "csdo", "StatusCode", "10", namespace="urn:test:wrong:simple")

    engine, _, values = _parsed_values(build)
    assert f"{STATUS}/csdo:StatusCode" not in values
    _assert_fail(engine, 2, values)


def test_req34_wrong_namespace_response_does_not_satisfy_exact_application_owner_qname():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _child(app, structure, "ipcdo", "ApplicantComplainResponseDetails", namespace="urn:test:wrong:ip-complex")

    engine, _, values = _parsed_values(build)
    assert f"{APP}/ipcdo:ApplicantComplainResponseDetails" not in values
    _assert_fail(engine, 34, values)
