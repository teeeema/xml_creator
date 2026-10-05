from pathlib import Path
from dataclasses import replace
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


FIXTURE = Path(__file__).parent / "fixtures/P.TEST.01"
STRUCTURE_ID = "R.TEST.001"


def _extract(item_specs: list[dict[str, object]]):
    engine = EaeuXmlEngine.load_process(FIXTURE)
    structure = engine.resolve_structure(STRUCTURE_ID, mode=GenerationMode.TEST).definition
    item_ns = structure.imported_namespaces["t"]

    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    for spec in item_specs:
        item = ET.SubElement(root, ET.QName(item_ns, "Items"))
        code = spec.get("code")
        if code is not None:
            item.set("code", str(code))
        if spec.get("name_present"):
            namespace = str(spec.get("name_namespace") or item_ns)
            name = ET.SubElement(item, ET.QName(namespace, "Name"))
            name.text = str(spec.get("name", "G"))

    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    return values


REQUIRED_NAME_RULE = {
    "rule_id": "TEST.REPEATABLE.REQUIRED_NAME",
    "kind": "for_each",
    "selector": {"collection": "Items"},
    "assertions": [
        {"kind": "presence", "target": {"field": "Name"}, "state": "REQUIRED"},
    ],
}

REQUIRED_CODE_RULE = {
    "rule_id": "TEST.REPEATABLE.REQUIRED_CODE",
    "kind": "for_each",
    "selector": {"collection": "Items"},
    "assertions": [
        {"kind": "presence", "target": {"field": "@code"}, "state": "REQUIRED"},
    ],
}


@pytest.mark.parametrize(
    ("present", "expected"),
    [
        ((True, True), RuleStatus.PASS),
        ((True, False), RuleStatus.FAIL),
        ((False, True), RuleStatus.FAIL),
        ((False, False), RuleStatus.FAIL),
    ],
)
def test_repeatable_complex_parent_required_child_uses_real_xml_extraction(present, expected) -> None:
    values = _extract([
        {"name_present": present[0], "name": "A"},
        {"name_present": present[1], "name": "B"},
    ])
    evaluation = StructuredRuleEvaluator().evaluate(REQUIRED_NAME_RULE, values)
    assert evaluation.status is expected


@pytest.mark.parametrize(
    ("present", "expected_values"),
    [
        ((True, False), ["A", None]),
        ((False, True), [None, "B"]),
    ],
)
def test_repeatable_simple_content_keeps_parent_index_alignment(present, expected_values) -> None:
    values = _extract([
        {"name_present": present[0], "name": "A"},
        {"name_present": present[1], "name": "B"},
    ])
    assert values["Items/Name"] == expected_values


@pytest.mark.parametrize(
    ("codes", "expected_values"),
    [
        (("A", None), ["A", None]),
        ((None, "B"), [None, "B"]),
    ],
)
def test_repeatable_attribute_keeps_parent_index_alignment(codes, expected_values) -> None:
    values = _extract([
        {"name_present": True, "name": "A", "code": codes[0]},
        {"name_present": True, "name": "B", "code": codes[1]},
    ])
    assert values["Items/@code"] == expected_values
    assert StructuredRuleEvaluator().evaluate(REQUIRED_CODE_RULE, values).status is RuleStatus.FAIL


def test_same_local_name_in_wrong_namespace_does_not_fill_missing_qname() -> None:
    values = _extract([
        {"name_present": True, "name": "A"},
        {"name_present": True, "name": "WRONG", "name_namespace": "urn:test:wrong"},
    ])
    assert values["Items/Name"] == ["A", None]
    assert StructuredRuleEvaluator().evaluate(REQUIRED_NAME_RULE, values).status is RuleStatus.FAIL


def test_qname_selector_ignores_sparse_missing_repeatable_slot() -> None:
    values = {
        "Root": [None, None],
        "Root/Optional/ccdo:CommunicationDetails": [None, ""],
        "Root/Optional/ccdo:CommunicationDetails/csdo:CommunicationChannelCode": [None, "EM"],
        "Root/Optional/ccdo:CommunicationDetails/csdo:CommunicationChannelId": [None, "a@example.test"],
    }
    selected = StructuredRuleEvaluator().select(
        {"qname": "ccdo:CommunicationDetails", "under": "Root"}, values,
    )
    assert len(selected) == 1
    assert selected[0]["csdo:CommunicationChannelCode"] == "EM"
    assert selected[0]["csdo:CommunicationChannelId"] == "a@example.test"


def test_sparse_repeatable_none_is_not_datatype_validated() -> None:
    engine = EaeuXmlEngine.load_process(FIXTURE)
    structure = engine.resolve_structure(STRUCTURE_ID, mode=GenerationMode.TEST).definition
    parent = structure.fields[0]
    date_field = replace(
        structure.fields[1],
        field_id="1.2",
        order=3,
        path="Items/EventDate",
        official_name="EventDate",
        xml_name="EventDate",
        datatype="bdt:DateType",
        datatype_text="date",
        min_occurs=0,
        max_occurs=1,
    )
    sparse_structure = replace(structure, fields=(parent, date_field))
    issues = engine.body_provider._validate_structure_values(
        sparse_structure,
        {"Items": [None, None], "Items/EventDate": [None, "2026-09-24"]},
        mode=GenerationMode.TEST,
    )
    assert not [issue for issue in issues if issue.code == "DATATYPE_INVALID"]


@pytest.mark.parametrize(
    ("min_occurs", "values", "expect_min_occurs"),
    [
        (1, ["2026-09-24", "2026-09-25"], False),
        (1, [None, "2026-09-25"], True),
        (1, ["2026-09-24", None], True),
        (1, [None, None], True),
        (0, ["2026-09-24", "2026-09-25"], False),
        (0, [None, "2026-09-25"], False),
        (0, ["2026-09-24", None], False),
        (0, [None, None], False),
    ],
)
def test_sparse_repeated_child_cardinality_is_checked_per_parent(
    min_occurs, values, expect_min_occurs,
) -> None:
    engine = EaeuXmlEngine.load_process(FIXTURE)
    structure = engine.resolve_structure(STRUCTURE_ID, mode=GenerationMode.TEST).definition
    parent = structure.fields[0]
    date_field = replace(
        structure.fields[1],
        field_id="1.2",
        order=3,
        path="Items/EventDate",
        official_name="EventDate",
        xml_name="EventDate",
        datatype="bdt:DateType",
        datatype_text="date",
        min_occurs=min_occurs,
        max_occurs=1,
    )
    sparse_structure = replace(structure, fields=(parent, date_field))
    issues = engine.body_provider._validate_structure_values(
        sparse_structure,
        {"Items": ["", ""], "Items/EventDate": values},
        mode=GenerationMode.TEST,
    )
    has_min_occurs = any(issue.code == "MIN_OCCURS" for issue in issues)
    assert has_min_occurs is expect_min_occurs
    assert not [issue for issue in issues if issue.code == "DATATYPE_INVALID"]


@pytest.mark.parametrize("values", [["not-a-date", "2026-09-25"], ["2026-09-24", "not-a-date"]])
def test_sparse_repeated_child_still_validates_real_invalid_values(values) -> None:
    engine = EaeuXmlEngine.load_process(FIXTURE)
    structure = engine.resolve_structure(STRUCTURE_ID, mode=GenerationMode.TEST).definition
    parent = structure.fields[0]
    date_field = replace(
        structure.fields[1],
        field_id="1.2",
        order=3,
        path="Items/EventDate",
        official_name="EventDate",
        xml_name="EventDate",
        datatype="bdt:DateType",
        datatype_text="date",
        min_occurs=1,
        max_occurs=1,
    )
    sparse_structure = replace(structure, fields=(parent, date_field))
    issues = engine.body_provider._validate_structure_values(
        sparse_structure,
        {"Items": ["", ""], "Items/EventDate": values},
        mode=GenerationMode.TEST,
    )
    assert any(issue.code == "DATATYPE_INVALID" for issue in issues)
