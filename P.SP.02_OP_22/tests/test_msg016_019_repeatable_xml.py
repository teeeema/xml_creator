from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
STRUCTURE = "R.IP.SP.02.007"
MESSAGES = ("P.SP.02.MSG.016", "P.SP.02.MSG.017", "P.SP.02.MSG.018", "P.SP.02.MSG.019")


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _child(parent, structure, prefix, local, text=None):
    node = ET.SubElement(parent, ET.QName(structure.imported_namespaces[prefix], local))
    if text is not None:
        node.text = text
    return node


def _parsed_values(builder):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    return engine, values


def _rules_for_item(engine, message, item):
    return [
        rule
        for rule in engine.rules[message].structured_rules
        if len(rule.get("source_refs", [])) == 2 and rule["source_refs"][1].get("item") == item
    ]


def _statuses(engine, message, item, values):
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(rule, values).status for rule in _rules_for_item(engine, message, item)]


def _record(root, structure):
    return _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")


def _goods(record, structure, complete=True, suffix="0"):
    goods = _child(record, structure, "ipcdo", "GoodsBaseDetails")
    _child(goods, structure, "ipsdo", "GoodsClassName", f"Class {suffix}")
    if complete:
        _child(goods, structure, "ipsdo", "GoodsName", f"Goods {suffix}")
    _child(goods, structure, "ipsdo", "TrademarkDecisionIndicator", "1")
    _child(goods, structure, "ipsdo", "TrademarkApplicationId", f"APP-{suffix}")
    return goods


def _communication(party, structure, complete=True, suffix="0"):
    comm = _child(party, structure, "ccdo", "CommunicationDetails")
    _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
    if complete:
        _child(comm, structure, "csdo", "CommunicationChannelId", f"u{suffix}@example.test")
    return comm


def _address(party, structure, kind="2", country_list="ВОИС ST.3", suffix="0"):
    address = _child(party, structure, "ccdo", "SubjectAddressDetails")
    _child(address, structure, "csdo", "AddressKindCode", kind)
    country = _child(address, structure, "csdo", "UnifiedCountryCode", "RU")
    country.set("codeListId", country_list)
    _child(address, structure, "csdo", "CityName", "Москва")
    _child(address, structure, "csdo", "StreetName", "Тестовая")
    _child(address, structure, "csdo", "BuildingNumberId", suffix)
    return address


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_repeatable_goods_bad_first_or_second_fails_inherited_req16(message, bad_index):
    def build(root, structure):
        record = _record(root, structure)
        for index in range(2):
            _goods(record, structure, complete=index != bad_index, suffix=str(index))

    engine, values = _parsed_values(build)
    assert RuleStatus.FAIL in _statuses(engine, message, "16", values)


@pytest.mark.parametrize("message", MESSAGES)
def test_repeatable_goods_good_good_pass_inherited_req16(message):
    def build(root, structure):
        record = _record(root, structure)
        _goods(record, structure, suffix="0")
        _goods(record, structure, suffix="1")

    engine, values = _parsed_values(build)
    assert all(status is RuleStatus.PASS for status in _statuses(engine, message, "16", values))


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_repeatable_communications_bad_first_or_second_fails_req8(message, bad_index):
    def build(root, structure):
        record = _record(root, structure)
        party = _child(record, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            _communication(party, structure, complete=index != bad_index, suffix=str(index))

    engine, values = _parsed_values(build)
    assert RuleStatus.FAIL in _statuses(engine, message, "8", values)


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_repeatable_addresses_bad_kind_first_or_second_fails_req13(message, bad_index):
    def build(root, structure):
        record = _record(root, structure)
        party = _child(record, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            _address(party, structure, kind="3" if index == bad_index else "2", suffix=str(index))

    engine, values = _parsed_values(build)
    assert RuleStatus.FAIL in _statuses(engine, message, "13", values)


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_repeatable_country_codelist_attribute_first_or_second_fails_req6(message, bad_index):
    def build(root, structure):
        record = _record(root, structure)
        party = _child(record, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            _address(
                party,
                structure,
                country_list="WRONG" if index == bad_index else "ВОИС ST.3",
                suffix=str(index),
            )

    engine, values = _parsed_values(build)
    assert RuleStatus.FAIL in _statuses(engine, message, "6", values)


def test_msg017_inherited_req18_finds_ue_in_second_party_after_xml_parse():
    def build(root, structure):
        record = _record(root, structure)
        first = _child(record, structure, "ipcdo", "IPPartyDetails")
        _child(first, structure, "ipsdo", "IPPartyKindCode", "RH")
        second = _child(record, structure, "ipcdo", "IPPartyDetails")
        _child(second, structure, "ipsdo", "IPPartyKindCode", "UE")

    engine, values = _parsed_values(build)
    assert _statuses(engine, "P.SP.02.MSG.017", "18", values) == [RuleStatus.PASS]


def test_msg017_inherited_req18_fails_without_ue_after_xml_parse():
    def build(root, structure):
        record = _record(root, structure)
        for _ in range(2):
            party = _child(record, structure, "ipcdo", "IPPartyDetails")
            _child(party, structure, "ipsdo", "IPPartyKindCode", "RH")

    engine, values = _parsed_values(build)
    assert _statuses(engine, "P.SP.02.MSG.017", "18", values) == [RuleStatus.FAIL]
