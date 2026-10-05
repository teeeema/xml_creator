from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGES = ("P.SP.02.MSG.011", "P.SP.02.MSG.013", "P.SP.02.MSG.014")
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _child(parent, structure, prefix, local, text=None):
    node = ET.SubElement(parent, ET.QName(structure.imported_namespaces[prefix], local))
    if text is not None:
        node.text = text
    return node


def _parsed_values(builder):
    engine = _engine()
    structure = engine.resolve_structure("R.IP.SP.02.002", mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    return engine, structure, values


def _rules_for_code(engine, message, code):
    result = []
    direct_id = f"{message}.REQ.{code}"
    for rule in engine.rules[message].structured_rules:
        if rule["rule_id"] == direct_id:
            result.append(rule)
        elif len(rule.get("source_refs", [])) == 2 and rule["source_refs"][1].get("item") == code:
            result.append(rule)
    return result


def _statuses(engine, values, message, code):
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(rule, values).status for rule in _rules_for_code(engine, message, code)]


def _address(parent, structure, complete=True):
    address = _child(parent, structure, "ccdo", "SubjectAddressDetails")
    _child(address, structure, "csdo", "AddressKindCode", "2")
    country = _child(address, structure, "csdo", "UnifiedCountryCode", "RU")
    country.set("codeListId", "ВОИС ST.3")
    _child(address, structure, "csdo", "CityName", "Москва")
    _child(address, structure, "csdo", "StreetName", "Тестовая")
    if complete:
        _child(address, structure, "csdo", "BuildingNumberId", "1")
    return address


def _communication(parent, structure, complete=True):
    comm = _child(parent, structure, "ccdo", "CommunicationDetails")
    _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
    if complete:
        _child(comm, structure, "csdo", "CommunicationChannelId", "a@test")
    return comm


def _party(app, structure, kind, complete=True):
    party = _child(app, structure, "ipcdo", "IPPartyDetails")
    _child(party, structure, "ipsdo", "IPPartyKindCode", kind)
    if complete:
        country = _child(party, structure, "csdo", "UnifiedCountryCode", "RU")
        country.set("codeListId", "ВОИС ST.3")
        _child(party, structure, "ipsdo", "IPSubjectName", kind)
        _address(party, structure)
        _communication(party, structure)
        if kind == "PA":
            _child(party, structure, "ipsdo", "PatentAttorneyId", "PA-1")
    return party


def _goods(app, structure, complete=True, suffix="0"):
    goods = _child(app, structure, "ipcdo", "GoodsBaseDetails")
    if complete:
        _child(goods, structure, "ipsdo", "GoodsClassCode", "01")
    _child(goods, structure, "ipsdo", "GoodsClassName", f"Class {suffix}")
    _child(goods, structure, "ipsdo", "GoodsName", f"Goods {suffix}")
    return goods


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_repeatable_goods_bad_first_or_second_fails(message, bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            _goods(app, structure, complete=index != bad_index, suffix=str(index))
    engine, _, values = _parsed_values(build)
    assert RuleStatus.FAIL in _statuses(engine, values, message, "29")


@pytest.mark.parametrize("message", MESSAGES)
def test_repeatable_goods_good_good_pass(message):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _goods(app, structure, suffix="0")
        _goods(app, structure, suffix="1")
    engine, _, values = _parsed_values(build)
    assert all(status is RuleStatus.PASS for status in _statuses(engine, values, message, "29"))


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_repeatable_communications_bad_first_or_second_fails(message, bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        party = _child(app, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            _communication(party, structure, complete=index != bad_index)
    engine, _, values = _parsed_values(build)
    assert RuleStatus.FAIL in _statuses(engine, values, message, "9")


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("kind,code", [("AP", "15"), ("PA", "21"), ("RE", "22")])
@pytest.mark.parametrize("bad_index", [0, 1])
def test_filtered_party_instances_preserve_context(message, kind, code, bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            _party(app, structure, kind, complete=index != bad_index)
    engine, _, values = _parsed_values(build)
    assert RuleStatus.FAIL in _statuses(engine, values, message, code)


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_unified_country_code_attribute_bad_first_or_second_fails(message, bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        party = _child(app, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            address = _child(party, structure, "ccdo", "SubjectAddressDetails")
            country = _child(address, structure, "csdo", "UnifiedCountryCode", "RU")
            country.set("codeListId", "WRONG" if index == bad_index else "ВОИС ST.3")
    engine, _, values = _parsed_values(build)
    assert RuleStatus.FAIL in _statuses(engine, values, message, "7")


@pytest.mark.parametrize("message", MESSAGES)
def test_wrong_namespace_does_not_satisfy_goods_code(message):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _goods(app, structure, suffix="0")
        goods = _child(app, structure, "ipcdo", "GoodsBaseDetails")
        ET.SubElement(goods, ET.QName("urn:wrong:namespace", "GoodsClassCode")).text = "01"
        _child(goods, structure, "ipsdo", "GoodsClassName", "Class 1")
        _child(goods, structure, "ipsdo", "GoodsName", "Goods 1")
    engine, _, values = _parsed_values(build)
    assert values[f"{GOODS}/ipsdo:GoodsClassCode"] == ["01", None]
    assert RuleStatus.FAIL in _statuses(engine, values, message, "29")


@pytest.mark.parametrize("code,name,wrong", [
    ("110", "Словесный знак", "Буквенный знак"),
    ("170", "Знак, представляющий собой сочетание цветов", "Изобразительный знак"),
])
def test_req26_pairing_on_production_xml(code, name, wrong):
    def build(root, structure, kind_name):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        tm = _child(app, structure, "ipcdo", "TrademarkDetails")
        _child(tm, structure, "ipsdo", "TrademarkKindCode", code)
        _child(tm, structure, "ipsdo", "TrademarkKindName", kind_name)
    engine, _, good = _parsed_values(lambda r, s: build(r, s, name))
    assert all(x is RuleStatus.PASS for x in _statuses(engine, good, "P.SP.02.MSG.011", "26"))
    engine, _, bad = _parsed_values(lambda r, s: build(r, s, wrong))
    assert RuleStatus.FAIL in _statuses(engine, bad, "P.SP.02.MSG.011", "26")


def _document(parent, structure, complete=True):
    doc = _child(parent, structure, "ipcdo", "AccompanyingDocumentsDetails")
    if complete:
        _child(doc, structure, "csdo", "DocId", "D-1")
        _child(doc, structure, "csdo", "DocCreationDate", "2026-09-24")
        _child(doc, structure, "csdo", "DescriptionText", "Описание")
        _child(doc, structure, "csdo", "PageQuantity", "1")
    return doc


@pytest.mark.parametrize("bad_nested", [False, True])
def test_msg013_req30_direct_and_nested_bad_first_or_second(bad_nested):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _document(app, structure, complete=bad_nested)
        naming = _child(app, structure, "ipcdo", "NamingAbilityProofDetails")
        proof = _child(naming, structure, "ipcdo", "ProofDocTextDetails")
        _document(proof, structure, complete=not bad_nested)
    engine, _, values = _parsed_values(build)
    assert _statuses(engine, values, "P.SP.02.MSG.013", "30") == [RuleStatus.FAIL]


def test_msg013_req30_direct_and_nested_good_good_pass():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _document(app, structure)
        naming = _child(app, structure, "ipcdo", "NamingAbilityProofDetails")
        proof = _child(naming, structure, "ipcdo", "ProofDocTextDetails")
        _document(proof, structure)
    engine, _, values = _parsed_values(build)
    assert _statuses(engine, values, "P.SP.02.MSG.013", "30") == [RuleStatus.PASS]
