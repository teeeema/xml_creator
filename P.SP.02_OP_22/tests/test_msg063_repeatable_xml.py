from pathlib import Path
from xml.etree import ElementTree as ET
import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.063"
STRUCTURE_ID = "R.IP.SP.02.002"
APP = "ipcdo:TrademarkApplicationDetails"


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


def _values_from_xml(builder):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE_ID, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    return engine, structure, values, issues


def _rules(engine, code):
    p = f"{MESSAGE}.T82.REQ.{code}"
    return [r for r in engine.rules[MESSAGE].structured_rules if r["rule_id"] == p or r["rule_id"].startswith(p + ".") or r["rule_id"].startswith(p + "_")]


def _assert_pass(engine, code, values):
    rules = _rules(engine, code)
    assert rules, f"No rules for REQ {code}"
    statuses = [StructuredRuleEvaluator().evaluate(r, values).status for r in rules]
    assert all(s is RuleStatus.PASS for s in statuses), f"Expected all PASS for REQ {code}, got: {statuses}"


def _assert_fail(engine, code, values):
    rules = _rules(engine, code)
    assert rules, f"No rules for REQ {code}"
    statuses = [StructuredRuleEvaluator().evaluate(r, values).status for r in rules]
    assert RuleStatus.FAIL in statuses, f"Expected FAIL for REQ {code}, got: {statuses}"


def _build_valid_app(root, structure):
    app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
    _child(app, structure, "ipsdo", "TrademarkApplicationId", "2026/RU-000001")
    return app


def test_xml_extraction_valid_single_application_passes_all_rules():
    def builder(root, structure):
        _build_valid_app(root, structure)

    engine, _, values, issues = _values_from_xml(builder)
    assert not issues
    assert values.get(f"{APP}/ipsdo:TrademarkApplicationId") == ["2026/RU-000001"] or values.get(f"{APP}/ipsdo:TrademarkApplicationId") == "2026/RU-000001"

    _assert_pass(engine, 1, values)
    _assert_pass(engine, 4, values)


def test_xml_extraction_zero_applications_fails_req1():
    def builder(root, structure):
        pass  # No application

    engine, _, values, issues = _values_from_xml(builder)
    _assert_fail(engine, 1, values)


def test_xml_extraction_multiple_applications_fails_req1():
    def builder(root, structure):
        app1 = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _child(app1, structure, "ipsdo", "TrademarkApplicationId", "2026/RU-000001")
        app2 = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _child(app2, structure, "ipsdo", "TrademarkApplicationId", "2026/RU-000002")

    engine, _, values, issues = _values_from_xml(builder)
    _assert_fail(engine, 1, values)
    # Both have ID, so REQ 4 passes individually
    _assert_pass(engine, 4, values)


def test_xml_extraction_missing_application_id_fails_req4():
    def builder(root, structure):
        _child(root, structure, "ipcdo", "TrademarkApplicationDetails")

    engine, _, values, issues = _values_from_xml(builder)
    _assert_pass(engine, 1, values)
    _assert_fail(engine, 4, values)


def test_xml_extraction_sibling_cannot_repair_missing_id():
    def builder(root, structure):
        app1 = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _child(app1, structure, "ipsdo", "TrademarkApplicationId", "2026/RU-000001")
        app2 = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        # app2 has NO ID

    engine, _, values, issues = _values_from_xml(builder)
    # REQ 4 must FAIL because one of the applications is missing ID
    _assert_fail(engine, 4, values)
