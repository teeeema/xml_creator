import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.core.errors import BodyValidationError
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


FIXTURE = Path(__file__).parent / "fixtures/P.TEST.01"
MESSAGE = "P.TS.01.MSG.001"
ROOT = "R.TEST.CONTAINER"
EMBEDDED_A = "R.TEST.EMBEDDED.A"
EMBEDDED_B = "R.TEST.EMBEDDED.B"


def _source(item: str):
    return [{
        "source_id": f"TEST-{item}",
        "document": "TEST_FIXTURE_ONLY",
        "location": item,
        "status": "TEST_ONLY",
    }]


def _structure(structure_id: str, namespace: str, root_element: str, fields: list[dict]):
    return {
        "structure_id": structure_id,
        "version": "1.0.0",
        "namespace": namespace,
        "root_element": root_element,
        "xsd_file": None,
        "imported_namespaces": {},
        "expected_normative_rows": len(fields),
        "imported_normative_rows": len(fields),
        "fields": fields,
        "status": "TEST_FIXTURE_ONLY",
        "source_refs": _source(structure_id),
    }


def _field(field_id: str, order: int, path: str, xml_name: str, *, kind="ELEMENT", datatype="test:StringType",
           min_occurs=1, max_occurs=1):
    return {
        "field_id": field_id,
        "order": order,
        "depth": 0,
        "parent": None,
        "path": path,
        "official_name": path,
        "xml_name": xml_name,
        "namespace_prefix": None,
        "kind": kind,
        "datatype": datatype,
        "datatype_text": datatype,
        "min_occurs": min_occurs,
        "max_occurs": max_occurs,
        "source_refs": _source(f"field-{field_id}"),
    }


@pytest.fixture
def one_of_engine():
    with TemporaryDirectory() as temporary:
        target = Path(temporary) / "P.TEST.ONEOF"
        shutil.copytree(FIXTURE, target)

        messages_path = target / "messages.yaml"
        messages = json.loads(messages_path.read_text(encoding="utf-8"))
        messages["messages"][0].update({
            "structure_id": ROOT,
            "embedded_structures": {"selection": "ONE_OF", "structures": [EMBEDDED_A, EMBEDDED_B]},
        })
        messages_path.write_text(json.dumps(messages), encoding="utf-8")

        profile_path = target / "version_profiles/current.yaml"
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        profile["structures"].update({
            ROOT: {"active_version": "1.0.0"},
            EMBEDDED_A: {"active_version": "1.0.0"},
            EMBEDDED_B: {"active_version": "1.0.0"},
        })
        profile_path.write_text(json.dumps(profile), encoding="utf-8")

        root = _structure(ROOT, "urn:test:container", "Container", [
            _field("1", 1, "Header", "Header"),
            _field("2", 2, "*", "*", kind="ANY", datatype="xs:any"),
        ])
        embedded_a = _structure(EMBEDDED_A, "urn:test:embedded:a", "PayloadA", [
            _field("1", 1, "Value", "Value"),
        ])
        embedded_b = _structure(EMBEDDED_B, "urn:test:embedded:b", "PayloadB", [
            _field("1", 1, "Value", "Value"),
        ])
        for definition in (root, embedded_a, embedded_b):
            path = target / "structures" / definition["structure_id"] / "1.0.0.yaml"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(definition), encoding="utf-8")

        rules_path = target / f"message_rules/{MESSAGE}.yaml"
        rules = json.loads(rules_path.read_text(encoding="utf-8"))
        rules.update({
            "structure_id": ROOT,
            "fixed_values": {},
            "field_usage": {},
            "structured_rules": [
                {"rule_id": "A_ONLY", "kind": "fixed_value", "target": "Value", "value": "A",
                 "applies_to_structure": EMBEDDED_A},
                {"rule_id": "B_ONLY", "kind": "fixed_value", "target": "Value", "value": "B",
                 "applies_to_structure": EMBEDDED_B},
                {"rule_id": "UNSCOPED", "kind": "presence", "target": "Header", "state": "REQUIRED"},
            ],
        })
        rules_path.write_text(json.dumps(rules), encoding="utf-8")
        yield EaeuXmlEngine.load_process(target)


def _payload(namespace: str, root: str, value: str | None = None):
    element = ET.Element(f"{{{namespace}}}{root}")
    if value is not None:
        ET.SubElement(element, f"{{{namespace}}}Value").text = value
    return element


@pytest.mark.parametrize(
    ("structure_id", "expected_root", "value"),
    [(EMBEDDED_A, "{urn:test:embedded:a}PayloadA", "A"), (EMBEDDED_B, "{urn:test:embedded:b}PayloadB", "B")],
)
def test_one_of_build_serialize_and_validate(one_of_engine, structure_id, expected_root, value):
    body = one_of_engine.build_body(
        MESSAGE, {"Header": "H"}, mode=GenerationMode.TEST,
        embedded_structure_id=structure_id, embedded_values={"Value": value},
    )
    root = body.serialize_xml_element()
    embedded = list(root)[-1]
    assert embedded.tag == expected_root
    result = one_of_engine.validate_body(MESSAGE, {"Header": "H", "*": embedded}, mode=GenerationMode.TEST)
    assert result.is_valid


def test_one_of_requires_explicit_build_selection(one_of_engine):
    with pytest.raises(BodyValidationError) as error:
        one_of_engine.build_body(MESSAGE, {"Header": "H"}, mode=GenerationMode.TEST)
    assert error.value.code == "EMBEDDED_STRUCTURE_SELECTION_REQUIRED"


def test_one_of_validation_rejects_no_payload(one_of_engine):
    result = one_of_engine.validate_body(MESSAGE, {"Header": "H"}, mode=GenerationMode.TEST)
    assert not result.is_valid
    assert "EMBEDDED_STRUCTURE_CARDINALITY" in {issue.code for issue in result.issues}


def test_one_of_validation_rejects_two_allowed_payloads(one_of_engine):
    result = one_of_engine.validate_body(MESSAGE, {
        "Header": "H",
        "*": [_payload("urn:test:embedded:a", "PayloadA", "A"), _payload("urn:test:embedded:b", "PayloadB", "B")],
    }, mode=GenerationMode.TEST)
    assert not result.is_valid
    assert "EMBEDDED_STRUCTURE_CARDINALITY" in {issue.code for issue in result.issues}


def test_one_of_validation_rejects_unknown_root(one_of_engine):
    result = one_of_engine.validate_body(MESSAGE, {
        "Header": "H", "*": _payload("urn:test:unknown", "Unknown", "X"),
    }, mode=GenerationMode.TEST)
    assert not result.is_valid
    assert "UNKNOWN_EMBEDDED_STRUCTURE" in {issue.code for issue in result.issues}


def test_selected_embedded_payload_is_structurally_validated(one_of_engine):
    result = one_of_engine.validate_body(MESSAGE, {
        "Header": "H", "*": _payload("urn:test:embedded:a", "PayloadA"),
    }, mode=GenerationMode.TEST)
    assert not result.is_valid
    assert any(issue.code == "MIN_OCCURS" and issue.field_path == "Value" for issue in result.issues)


@pytest.mark.parametrize(
    ("payload", "expected_rule_ids"),
    [
        (_payload("urn:test:embedded:a", "PayloadA", "A"), {"A_ONLY", "UNSCOPED"}),
        (_payload("urn:test:embedded:b", "PayloadB", "B"), {"B_ONLY", "UNSCOPED"}),
    ],
)
def test_structured_rule_applies_only_to_selected_structure(one_of_engine, payload, expected_rule_ids):
    result = one_of_engine.validate_body(MESSAGE, {"Header": "H", "*": payload}, mode=GenerationMode.TEST)
    assert result.is_valid
    assert {item.rule_id for item in result.rule_evaluations} == expected_rule_ids
    assert all(item.status is RuleStatus.PASS for item in result.rule_evaluations)


def test_non_one_of_message_keeps_existing_api_and_behavior():
    engine = EaeuXmlEngine.load_process(FIXTURE)
    body = engine.build_body(MESSAGE, {"Items": {"Name": "A"}}, mode=GenerationMode.TEST)
    assert body.serialize_xml_element().tag == "{urn:test:structure:v2.0.0}TestPayload"
