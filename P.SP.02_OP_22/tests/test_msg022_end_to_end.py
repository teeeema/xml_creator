from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.022"
STRUCTURE = "R.IP.SP.02.008"
REQ1 = "P.SP.02.MSG.022.T55.REQ.1"


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


def _header(root, structure, *, message=MESSAGE):
    header = _child(root, structure, "ccdo", "EDocHeader")
    _child(header, structure, "csdo", "InfEnvelopeCode", message)
    _child(header, structure, "csdo", "EDocCode", STRUCTURE)
    _child(header, structure, "csdo", "EDocId", "00000000-0000-0000-0000-000000000022")
    _child(header, structure, "csdo", "EDocDateTime", "2026-09-24T12:00:00+03:00")
    return header


def _raw(builder):
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    validation = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    return structure, values, validation


def _req1_statuses(validation):
    return [item.status for item in validation.rule_evaluations if item.rule_id == REQ1]


def test_msg022_valid_production_xml_has_only_one_header():
    structure, values, validation = _raw(lambda root, s: _header(root, s))
    assert (
        f"{{{structure.namespace}}}{structure.root_element}"
        == "{urn:EEC:R:IP:SP:02:TrademarkRegisterRequestDetails:v1.0.0}TrademarkRegisterRequestDetails"
    )
    assert set(values) == {
        "ccdo:EDocHeader",
        "ccdo:EDocHeader/csdo:InfEnvelopeCode",
        "ccdo:EDocHeader/csdo:EDocCode",
        "ccdo:EDocHeader/csdo:EDocId",
        "ccdo:EDocHeader/csdo:EDocDateTime",
    }
    assert validation.is_valid
    assert _req1_statuses(validation) == [RuleStatus.PASS] * 6


def test_msg022_missing_header_fails():
    _, _, validation = _raw(lambda root, structure: None)
    assert not validation.is_valid
    assert RuleStatus.FAIL in _req1_statuses(validation)


def test_msg022_duplicate_header_fails():
    def build(root, structure):
        _header(root, structure)
        _header(root, structure)

    _, _, validation = _raw(build)
    assert not validation.is_valid
    assert RuleStatus.FAIL in _req1_statuses(validation)


@pytest.mark.parametrize(
    "prefix,local,repeat",
    [
        ("csdo", "UpdateDateTime", 1),
        ("csdo", "UnifiedCountryCode", 1),
        ("csdo", "UnifiedCountryCode", 2),
        ("ipsdo", "TrademarkId", 1),
        ("ipsdo", "TrademarkApplicationId", 1),
        ("ipcdo", "AccompanyingDocumentsDetails", 1),
    ],
)
def test_msg022_each_forbidden_top_level_field_fails(prefix, local, repeat):
    def build(root, structure):
        _header(root, structure)
        for index in range(repeat):
            attrs = {"codeListId": "ВОИС ST.3"} if local == "UnifiedCountryCode" else None
            _child(root, structure, prefix, local, f"VALUE-{index}", attrs=attrs)

    _, _, validation = _raw(build)
    assert not validation.is_valid
    assert RuleStatus.FAIL in _req1_statuses(validation)


def test_msg022_nested_local_name_collision_does_not_count_as_top_level_target():
    def build(root, structure):
        header = _header(root, structure)
        _child(header, structure, "csdo", "UpdateDateTime", "2026-09-24T12:01:00+03:00")

    _, values, validation = _raw(build)
    assert "csdo:UpdateDateTime" not in values
    assert validation.is_valid


def test_msg022_wrong_namespace_does_not_count_as_top_level_target():
    def build(root, structure):
        _header(root, structure)
        _child(root, structure, "csdo", "UpdateDateTime", "2026-09-24T12:01:00+03:00", namespace="urn:wrong")

    _, values, validation = _raw(build)
    assert "csdo:UpdateDateTime" not in values
    assert validation.is_valid
