from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.031"
APP = "ipcdo:TrademarkApplicationDetails"
R002_GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
R002_SIG = f"{APP}/ipcdo:SignatureDetails"
R007_ROOT = "ipcdo:UnifiedRegisterRecordsDetails"
R007_GOODS = f"{R007_ROOT}/ipcdo:GoodsBaseDetails"
R007_DESC = f"{R007_ROOT}/ipcdo:TrademarkDetails/ipcdo:TMDescriptionDetails"
R007_ELEMENT = f"{R007_DESC}/ipcdo:TMElementDetails"


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


def _values_from_xml(structure_id, builder):
    engine = _engine()
    structure = engine.resolve_structure(structure_id, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    return engine, structure, values, issues


def _rules(engine, table, code):
    rid = f"{MESSAGE}.T{table}.REQ.{code}"
    return [r for r in engine.rules[MESSAGE].structured_rules if r["rule_id"] == rid]


def _statuses(engine, table, code, values):
    rules = _rules(engine, table, code)
    assert rules, (table, code)
    return [StructuredRuleEvaluator().evaluate(rule, values).status for rule in rules]


def _assert_pass(engine, table, code, values):
    statuses = _statuses(engine, table, code, values)
    assert all(status is RuleStatus.PASS for status in statuses), statuses


def _assert_fail(engine, table, code, values):
    statuses = _statuses(engine, table, code, values)
    assert RuleStatus.FAIL in statuses, statuses


def _r002_goods(parent, structure, suffix, *, omit=None, wrong_namespace=False):
    goods = _child(parent, structure, "ipcdo", "GoodsBaseDetails")
    if omit != "GoodsClassCode":
        ns = "urn:test:wrong:namespace" if wrong_namespace else None
        _child(goods, structure, "ipsdo", "GoodsClassCode", f"0{suffix + 1}", namespace=ns)
    _child(goods, structure, "ipsdo", "GoodsClassName", f"Class {suffix}")
    _child(goods, structure, "ipsdo", "GoodsName", f"Goods {suffix}")
    return goods


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_r002_repeatable_goods_preserve_parent_alignment_from_production_xml(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            _r002_goods(app, structure, index, omit="GoodsClassCode" if index == bad_index else None)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.002", build)
    codes = values[f"{R002_GOODS}/ipsdo:GoodsClassCode"]
    assert len(codes) == 2
    if bad_index is None:
        assert codes == ["01", "02"]
        _assert_pass(engine, 48, 29, values)
    else:
        assert codes[bad_index] is None
        _assert_fail(engine, 48, 29, values)


def test_r002_wrong_namespace_goods_class_code_does_not_satisfy_exact_qname():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _r002_goods(app, structure, 0, omit="GoodsClassCode")
        goods = list(app)[0]
        _child(goods, structure, "ipsdo", "GoodsClassCode", "01", namespace="urn:test:wrong:ipsdo")

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.002", build)
    assert f"{R002_GOODS}/ipsdo:GoodsClassCode" not in values
    _assert_fail(engine, 48, 29, values)


def _officer(signature, structure):
    officer = _child(signature, structure, "ipcdo", "OfficerDetails")
    full = _child(officer, structure, "ccdo", "FullNameDetails")
    _child(full, structure, "csdo", "FirstName", "Петр")
    _child(full, structure, "csdo", "LastName", "Петров")
    _child(officer, structure, "csdo", "PositionName", "Специалист")
    return officer


def _direct_name(signature, structure):
    full = _child(signature, structure, "ccdo", "FullNameDetails")
    _child(full, structure, "csdo", "FirstName", "Иван")
    _child(full, structure, "csdo", "LastName", "Иванов")
    return full


def test_r002_signature_rules_do_not_leak_between_repeatable_signature_parents():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        first = _child(app, structure, "ipcdo", "SignatureDetails")
        _child(first, structure, "csdo", "DocCreationDate", "2026-09-30")
        _officer(first, structure)
        second = _child(app, structure, "ipcdo", "SignatureDetails")
        _child(second, structure, "csdo", "DocCreationDate", "2026-09-30")
        _direct_name(second, structure)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.002", build)
    _assert_pass(engine, 48, 34, values)
    _assert_pass(engine, 48, 35, values)
    _assert_pass(engine, 48, 36, values)


def test_r002_signature_same_parent_mutual_exclusion_rejects_both_forms():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        sig = _child(app, structure, "ipcdo", "SignatureDetails")
        _child(sig, structure, "csdo", "DocCreationDate", "2026-09-30")
        _officer(sig, structure)
        _direct_name(sig, structure)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.002", build)
    _assert_fail(engine, 48, 34, values)
    _assert_fail(engine, 48, 35, values)


def _r007_element(desc, structure, suffix, *, omit=None):
    element = _child(desc, structure, "ipcdo", "TMElementDetails")
    fields = (
        ("ipsdo", "TrademarkCFECode", f"01.01.0{suffix + 1}"),
        ("csdo", "DesignationName", f"Mark {suffix}"),
        ("ipsdo", "TMLocalizedName", f"Localized {suffix}"),
        ("ipsdo", "TMTransliterationName", f"Translit {suffix}"),
    )
    for prefix, local, value in fields:
        if local != omit:
            _child(element, structure, prefix, local, value)
    return element


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_r007_nested_repeatable_tm_elements_preserve_parent_alignment(bad_index):
    def build(root, structure):
        records = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        tm = _child(records, structure, "ipcdo", "TrademarkDetails")
        desc = _child(tm, structure, "ipcdo", "TMDescriptionDetails")
        _child(desc, structure, "csdo", "DescriptionText", "Description")
        for index in range(2):
            _r007_element(desc, structure, index, omit="TrademarkCFECode" if index == bad_index else None)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.007", build)
    codes = values[f"{R007_ELEMENT}/ipsdo:TrademarkCFECode"]
    assert len(codes) == 2
    if bad_index is None:
        _assert_pass(engine, 49, 15, values)
    else:
        assert codes[bad_index] is None
        _assert_fail(engine, 49, 15, values)


def _r007_goods(parent, structure, suffix, *, omit=None):
    goods = _child(parent, structure, "ipcdo", "GoodsBaseDetails")
    fields = (
        ("ipsdo", "GoodsClassCode", f"0{suffix + 1}"),
        ("ipsdo", "GoodsClassName", f"Class {suffix}"),
        ("ipsdo", "GoodsName", f"Goods {suffix}"),
        ("ipsdo", "TrademarkDecisionIndicator", "1"),
        ("ipsdo", "TrademarkApplicationId", f"APP-{suffix}"),
    )
    for prefix, local, value in fields:
        if local != omit:
            _child(goods, structure, prefix, local, value)
    return goods


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_r007_repeatable_goods_req16_checks_each_parent_without_cross_parent_leakage(bad_index):
    def build(root, structure):
        records = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        for index in range(2):
            _r007_goods(records, structure, index, omit="GoodsClassCode" if index == bad_index else None)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.007", build)
    codes = values[f"{R007_GOODS}/ipsdo:GoodsClassCode"]
    assert len(codes) == 2
    if bad_index is None:
        _assert_pass(engine, 49, 16, values)
    else:
        assert codes[bad_index] is None
        _assert_fail(engine, 49, 16, values)


def test_r007_req17_forbidden_goods_fields_are_checked_on_each_existing_parent():
    def build(root, structure):
        records = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        _r007_goods(records, structure, 0)
        bad = _r007_goods(records, structure, 1)
        _child(bad, structure, "ipsdo", "TrademarkId", "TM-1")

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.007", build)
    assert values[f"{R007_GOODS}/ipsdo:TrademarkId"] == [None, "TM-1"]
    _assert_fail(engine, 49, 17, values)


def test_optional_for_each_branches_remain_vacuous_when_parent_is_absent():
    engine = _engine()
    empty_r002 = {APP: [None]}
    for code in (11, 12, 21, 22, 23, 24):
        _assert_pass(engine, 48, code, empty_r002)

    empty_r007 = {R007_ROOT: [None]}
    for code in (6, 7, 8, 9, 10, 12, 13, 14, 15, 17, 20, 24):
        _assert_pass(engine, 49, code, empty_r007)
