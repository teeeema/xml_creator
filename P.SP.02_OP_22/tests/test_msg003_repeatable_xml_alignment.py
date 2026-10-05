from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.003"
STRUCTURE_002 = "R.IP.SP.02.002"
STRUCTURE_007 = "R.IP.SP.02.007"


def _engine() -> EaeuXmlEngine:
    return EaeuXmlEngine.load_process(PACKAGE)


def _child(parent, structure, prefix: str, name: str, text: str | None = None):
    element = ET.SubElement(parent, ET.QName(structure.imported_namespaces[prefix], name))
    element.text = text
    return element


def _parsed_values(structure_id: str, build_xml):
    engine = _engine()
    structure = engine.resolve_structure(structure_id, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    build_xml(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    return engine, values


def _rule(engine: EaeuXmlEngine, rule_id: str, *, collection: str | None = None, kind: str | None = None):
    matches = [rule for rule in engine.rules[MESSAGE].structured_rules if rule["rule_id"] == rule_id]
    if collection is not None:
        matches = [rule for rule in matches if rule.get("selector", {}).get("collection") == collection]
    if kind is not None:
        matches = [rule for rule in matches if rule.get("kind") == kind]
    assert len(matches) == 1
    return matches[0]


def _status(engine, values, rule_id: str, *, collection: str | None = None, kind: str | None = None) -> RuleStatus:
    return StructuredRuleEvaluator().evaluate(
        _rule(engine, rule_id, collection=collection, kind=kind), values
    ).status


@pytest.mark.parametrize("bad_index", [0, 1])
def test_t36_repeatable_trademark_application_details_rejects_one_missing_application_id(bad_index) -> None:
    def build(root, structure):
        for index in range(2):
            app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
            if index != bad_index:
                _child(app, structure, "ipsdo", "TrademarkApplicationId", f"APP-{index}")

    engine, values = _parsed_values(STRUCTURE_002, build)
    assert _status(engine, values, "P.SP.02.MSG.003.T36.REQ.1") is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_t36_repeatable_goods_rejects_one_missing_required_field(bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            goods = _child(app, structure, "ipcdo", "GoodsBaseDetails")
            _child(goods, structure, "ipsdo", "TrademarkApplicationId", f"APP-{index}")
            if index != bad_index:
                _child(goods, structure, "ipsdo", "TrademarkRegRefusalReasonText", f"R-{index}")

    engine, values = _parsed_values(STRUCTURE_002, build)
    assert _status(engine, values, "P.SP.02.MSG.003.T36.REQ.30") is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_t36_repeatable_statuses_reject_one_missing_event_date(bad_index) -> None:
    def build(root, structure):
        for index in range(2):
            app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
            status = _child(app, structure, "ipcdo", "IPEntityStatusDetails")
            if index != bad_index:
                _child(status, structure, "csdo", "EventDate", "2026-09-18")
            _child(status, structure, "csdo", "StatusCode", "20")

    engine, values = _parsed_values(STRUCTURE_002, build)
    assert _status(engine, values, "P.SP.02.MSG.003.T36.REQ.5") is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_t37_repeatable_register_records_rejects_one_missing_application_id(bad_index) -> None:
    def build(root, structure):
        for index in range(2):
            record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
            if index != bad_index:
                _child(record, structure, "ipsdo", "TrademarkApplicationId", f"APP-{index}")

    engine, values = _parsed_values(STRUCTURE_007, build)
    assert _status(engine, values, "P.SP.02.MSG.003.T37.REQ.2") is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_t37_repeatable_parties_reject_one_missing_subject_name(bad_index) -> None:
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        for index in range(2):
            party = _child(record, structure, "ipcdo", "IPPartyDetails")
            _child(party, structure, "csdo", "UnifiedCountryCode", "RU")
            if index != bad_index:
                _child(party, structure, "ipsdo", "IPSubjectName", f"Owner-{index}")
            _child(party, structure, "ccdo", "SubjectAddressDetails")
            _child(party, structure, "ccdo", "CommunicationDetails")

    engine, values = _parsed_values(STRUCTURE_007, build)
    assert _status(engine, values, "P.SP.02.MSG.003.T37.REQ.12") is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_t37_repeatable_goods_rejects_one_missing_goods_name(bad_index) -> None:
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        for index in range(2):
            goods = _child(record, structure, "ipcdo", "GoodsBaseDetails")
            _child(goods, structure, "ipsdo", "GoodsClassName", f"Class-{index}")
            if index != bad_index:
                _child(goods, structure, "ipsdo", "GoodsName", f"Goods-{index}")
            _child(goods, structure, "ipsdo", "TrademarkDecisionIndicator", "1")
            _child(goods, structure, "ipsdo", "TrademarkApplicationId", f"APP-{index}")

    engine, values = _parsed_values(STRUCTURE_007, build)
    assert _status(
        engine,
        values,
        "P.SP.02.MSG.003.T37.REQ.16",
        collection="ipcdo:UnifiedRegisterRecordsDetails/ipcdo:GoodsBaseDetails",
        kind="for_each",
    ) is RuleStatus.FAIL


def _build_tm_elements(root, structure, missing_cfe_index: int | None):
    record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
    trademark = _child(record, structure, "ipcdo", "TrademarkDetails")
    description = _child(trademark, structure, "ipcdo", "TMDescriptionDetails")
    _child(description, structure, "csdo", "DescriptionText", "Description")
    for index in range(2):
        element = _child(description, structure, "ipcdo", "TMElementDetails")
        if index != missing_cfe_index:
            _child(element, structure, "ipsdo", "TrademarkCFECode", f"CFE-{index}")
        _child(element, structure, "csdo", "DesignationName", f"D-{index}")
        _child(element, structure, "ipsdo", "TMLocalizedName", f"L-{index}")
        _child(element, structure, "ipsdo", "TMTransliterationName", f"T-{index}")


def test_t37_req15_nested_repeatable_two_valid_instances_pass() -> None:
    engine, values = _parsed_values(STRUCTURE_007, lambda root, structure: _build_tm_elements(root, structure, None))
    collection = "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:TrademarkDetails/ipcdo:TMDescriptionDetails/ipcdo:TMElementDetails"
    assert _status(engine, values, "P.SP.02.MSG.003.T37.REQ.15", collection=collection) is RuleStatus.PASS


@pytest.mark.parametrize("bad_index", [0, 1])
def test_t37_req15_nested_repeatable_rejects_one_missing_cfe_code(bad_index) -> None:
    engine, values = _parsed_values(STRUCTURE_007, lambda root, structure: _build_tm_elements(root, structure, bad_index))
    collection = "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:TrademarkDetails/ipcdo:TMDescriptionDetails/ipcdo:TMElementDetails"
    assert _status(engine, values, "P.SP.02.MSG.003.T37.REQ.15", collection=collection) is RuleStatus.FAIL
