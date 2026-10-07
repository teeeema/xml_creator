from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.024"
STRUCTURE = "R.IP.SP.02.008"
REQ1 = "P.SP.02.MSG.024.T56.REQ.1"
REQ3 = "P.SP.02.MSG.024.T56.REQ.3"


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
    _child(header, structure, "csdo", "EDocId", "00000000-0000-0000-0000-000000000024")
    _child(header, structure, "csdo", "EDocDateTime", "2026-09-24T12:00:00+03:00")
    return header


def _raw(builder, *, message=MESSAGE):
    engine = _engine()
    structure = engine.get_structure(message, mode=GenerationMode.TEST)
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    validation = engine.validate_body(message, values, mode=GenerationMode.TEST)
    return engine, values, validation


def _status(validation, rule_id):
    matches = [item.status for item in validation.rule_evaluations if item.rule_id == rule_id]
    assert len(matches) == 1
    return matches[0]


def _base(root, structure):
    _header(root, structure)
    _child(root, structure, "csdo", "UpdateDateTime", "2026-09-24T12:01:00+03:00")


def test_msg024_update_datetime_present_passes_and_absent_fails():
    _, _, valid = _raw(_base)
    assert valid.is_valid
    assert _status(valid, REQ1) is RuleStatus.PASS

    _, _, invalid = _raw(lambda root, structure: _header(root, structure))
    assert not invalid.is_valid
    assert _status(invalid, REQ1) is RuleStatus.FAIL


@pytest.mark.parametrize(
    "code_lists,expected",
    [
        (["ВОИС ST.3"], RuleStatus.PASS),
        (["ВОИС ST.3", "ВОИС ST.3"], RuleStatus.PASS),
        (["ВОИС ST.3", "WRONG"], RuleStatus.FAIL),
        (["WRONG", "ВОИС ST.3"], RuleStatus.FAIL),
        ([None], RuleStatus.FAIL),
        (["WRONG"], RuleStatus.FAIL),
    ],
)
def test_msg024_repeatable_country_code_list_id_matrix(code_lists, expected):
    def build(root, structure):
        _base(root, structure)
        for index, code_list in enumerate(code_lists):
            attrs = {"codeListId": code_list} if code_list is not None else None
            _child(root, structure, "csdo", "UnifiedCountryCode", "RU", attrs=attrs)

    _, values, validation = _raw(build)
    assert len(values["csdo:UnifiedCountryCode"]) == len(code_lists) if len(code_lists) > 1 else True
    assert _status(validation, REQ3) is expected
    if expected is RuleStatus.PASS:
        assert validation.is_valid
    else:
        assert not validation.is_valid


def test_msg024_wrong_namespace_country_is_not_a_normative_target():
    def build(root, structure):
        _base(root, structure)
        _child(
            root,
            structure,
            "csdo",
            "UnifiedCountryCode",
            "RU",
            attrs={"codeListId": "WRONG"},
            namespace="urn:wrong",
        )

    _, values, validation = _raw(build)
    assert "csdo:UnifiedCountryCode" not in values
    assert _status(validation, REQ3) is RuleStatus.PASS
    assert validation.is_valid


def test_msg024_req2_remains_unmapped_accompanying_document_is_not_rejected():
    def build(root, structure):
        _base(root, structure)
        _child(root, structure, "ipcdo", "AccompanyingDocumentsDetails")

    _, values, validation = _raw(build)
    assert "ipcdo:AccompanyingDocumentsDetails" in values
    assert validation.is_valid
    assert all(item.rule_id != "P.SP.02.MSG.024.T56.REQ.2" for item in validation.rule_evaluations)


def test_same_r008_xml_has_message_specific_business_evaluation():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    _base(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues

    msg024 = engine.validate_body("P.SP.02.MSG.024", values, mode=GenerationMode.TEST)
    msg022 = engine.validate_body("P.SP.02.MSG.022", values, mode=GenerationMode.TEST)
    assert msg024.is_valid
    assert not msg022.is_valid
    assert any(item.rule_id == "P.SP.02.MSG.022.T55.REQ.1" and item.status is RuleStatus.FAIL for item in msg022.rule_evaluations)


def test_msg024_rules_do_not_leak_to_msg026():
    engine = _engine()
    assert "P.SP.02.MSG.026" not in engine.rules


def test_msg024_required_update_datetime_rejects_empty_element():
    def build(root, structure):
        _header(root, structure)
        _child(root, structure, "csdo", "UpdateDateTime")

    _, values, validation = _raw(build)
    assert values["csdo:UpdateDateTime"] is None
    assert not validation.is_valid
    assert _status(validation, REQ1) is RuleStatus.FAIL
