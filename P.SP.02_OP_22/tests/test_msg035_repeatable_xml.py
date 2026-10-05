from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.035"
STRUCTURE = "R.IP.SP.02.002"
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _child(parent, structure, prefix, local, text=None, attrs=None):
    node = ET.SubElement(parent, ET.QName(structure.imported_namespaces[prefix], local))
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
    return engine, values


def _rules(engine, code):
    prefix = f"{MESSAGE}.T53.REQ.{code}"
    rules = [
        rule
        for rule in engine.rules[MESSAGE].structured_rules
        if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")
    ]
    assert rules, code
    return rules


def _assert_status(engine, code, values, expected):
    statuses = [StructuredRuleEvaluator().evaluate(rule, values).status for rule in _rules(engine, code)]
    if expected is RuleStatus.PASS:
        assert all(status is RuleStatus.PASS for status in statuses), statuses
    else:
        assert RuleStatus.FAIL in statuses, statuses


def _address(parent, structure, index, *, omit=None):
    address = _child(parent, structure, "ccdo", "SubjectAddressDetails")
    for prefix, local, text in (
        ("csdo", "AddressKindCode", "2"),
        ("csdo", "UnifiedCountryCode", "RU"),
        ("csdo", "CityName", f"City {index}"),
        ("csdo", "StreetName", f"Street {index}"),
        ("csdo", "BuildingNumberId", str(index + 1)),
    ):
        if local == omit:
            continue
        attrs = {"codeListId": "ВОИС ST.3"} if local == "UnifiedCountryCode" else None
        _child(address, structure, prefix, local, text, attrs=attrs)
    return address


def _communication(parent, structure, index, *, omit=None):
    comm = _child(parent, structure, "ccdo", "CommunicationDetails")
    _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
    if omit != "CommunicationChannelId":
        _child(comm, structure, "csdo", "CommunicationChannelId", f"user{index}@example.test")
    return comm


@pytest.mark.parametrize("bad_index", [None, 0, 1], ids=["good_good", "bad_good", "good_bad"])
def test_req8_repeatable_addresses_preserve_parent_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            party = _child(app, structure, "ipcdo", "IPPartyDetails")
            _child(party, structure, "ipsdo", "IPPartyKindCode", "RE")
            _address(party, structure, index, omit="CityName" if index == bad_index else None)

    engine, values = _parsed_values(build)
    cities = values[f"{PARTY}/ccdo:SubjectAddressDetails/csdo:CityName"]
    assert len(cities) == 2
    if bad_index is None:
        assert cities == ["City 0", "City 1"]
        _assert_status(engine, 8, values, RuleStatus.PASS)
    else:
        assert cities[bad_index] is None
        _assert_status(engine, 8, values, RuleStatus.FAIL)


@pytest.mark.parametrize("bad_index", [None, 0, 1], ids=["good_good", "bad_good", "good_bad"])
def test_req9_repeatable_communications_preserve_parent_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            party = _child(app, structure, "ipcdo", "IPPartyDetails")
            _child(party, structure, "ipsdo", "IPPartyKindCode", "RE")
            _communication(party, structure, index, omit="CommunicationChannelId" if index == bad_index else None)

    engine, values = _parsed_values(build)
    ids = values[f"{PARTY}/ccdo:CommunicationDetails/csdo:CommunicationChannelId"]
    assert len(ids) == 2
    if bad_index is None:
        _assert_status(engine, 9, values, RuleStatus.PASS)
    else:
        assert ids[bad_index] is None
        _assert_status(engine, 9, values, RuleStatus.FAIL)


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


@pytest.mark.parametrize("bad_index", [None, 0, 1], ids=["good_good", "bad_good", "good_bad"])
def test_req27_repeatable_trademarks_keep_trigger_and_required_fields_in_same_parent(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            _trademark(app, structure, index, missing="TrademarkColourName" if index == bad_index else None)

    engine, values = _parsed_values(build)
    colours = values[f"{TM}/ipsdo:TrademarkColourName"]
    assert len(colours) == 2
    if bad_index is None:
        _assert_status(engine, 27, values, RuleStatus.PASS)
    else:
        assert colours[bad_index] is None
        _assert_status(engine, 27, values, RuleStatus.FAIL)


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


@pytest.mark.parametrize("bad_index", [None, 0, 1], ids=["good_good", "bad_good", "good_bad"])
def test_req29_repeatable_goods_preserve_parent_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            _goods(app, structure, index, missing="GoodsClassCode" if index == bad_index else None)

    engine, values = _parsed_values(build)
    codes = values[f"{GOODS}/ipsdo:GoodsClassCode"]
    assert len(codes) == 2
    if bad_index is None:
        _assert_status(engine, 29, values, RuleStatus.PASS)
    else:
        assert codes[bad_index] is None
        _assert_status(engine, 29, values, RuleStatus.FAIL)
