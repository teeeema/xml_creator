"""OP49 Table 10 R002/R003: evaluate indicators after real XML serialization."""

from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator
from test_msg001_full_message import msg001_values


PACKAGE = Path(__file__).parents[1]
MESSAGE = "P.DS.01.MSG.001"


@pytest.mark.parametrize(
    ("first_value", "second_value", "expected_r002", "expected_r003"),
    [
        ("true", None, RuleStatus.PASS, RuleStatus.PASS),
        ("1", None, RuleStatus.PASS, RuleStatus.PASS),
        ("false", None, RuleStatus.FAIL, RuleStatus.FAIL),
        ("0", None, RuleStatus.FAIL, RuleStatus.FAIL),
        ("true", "true", RuleStatus.FAIL, RuleStatus.PASS),
        ("true", "false", RuleStatus.PASS, RuleStatus.FAIL),
        ("true", "0", RuleStatus.PASS, RuleStatus.FAIL),
    ],
)
def test_msg001_selection_cardinality_on_serialized_xml(
    first_value, second_value, expected_r002, expected_r003
):
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    initial = engine.build_body(MESSAGE, msg001_values(engine), mode=GenerationMode.TEST)
    xml_root = initial.serialize_xml_element()

    entry_qname = f"{{{structure.imported_namespaces['ds01cdo']}}}ChargedDistributedDutyDetails"
    indicator_qname = f"{{{structure.imported_namespaces['ds01sdo']}}}DailyInfoIndicator"
    entry = next(xml_root.iter(entry_qname))
    indicator = next(entry.iter(indicator_qname))
    indicator.text = first_value
    if second_value is not None:
        parent = next(parent for parent in xml_root.iter() if entry in parent)
        other_entry = deepcopy(entry)
        next(other_entry.iter(indicator_qname)).text = second_value
        parent.append(other_entry)

    # Serialize and parse XML; the extractor intentionally preserves lexical text.
    parsed_xml = ET.fromstring(ET.tostring(xml_root, encoding="utf-8"))
    assert [node.text for node in parsed_xml.iter(indicator_qname)] == (
        [first_value] if second_value is None else [first_value, second_value]
    )
    extracted, extraction_issues = engine.body_provider._values_from_element(
        structure, parsed_xml
    )
    assert not extraction_issues
    indicator_path = next(field.path for field in structure.fields if field.xml_name == "DailyInfoIndicator")
    assert extracted[indicator_path] == (
        first_value if second_value is None else [first_value, second_value]
    )

    checked = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    outcomes = {item.rule_id: item.status for item in checked.rule_evaluations}
    assert outcomes[f"{MESSAGE}.R002"] is expected_r002
    assert outcomes[f"{MESSAGE}.R003"] is expected_r003


@pytest.mark.parametrize(
    ("lexical", "logical"),
    [("true", True), ("false", False), ("1", True), ("0", False), (" true ", True)],
)
def test_shared_condition_comparison_uses_xml_boolean_lexicals(lexical, logical):
    evaluator = StructuredRuleEvaluator()
    assert evaluator._compare(lexical, "EQ", logical)
    assert evaluator._compare(logical, "EQ", lexical)
    assert not evaluator._compare(lexical, "NE", logical)
    assert not evaluator._compare(lexical, "EQ", not logical)


def test_shared_condition_rejects_non_boolean_xml_lexicals():
    evaluator = StructuredRuleEvaluator()
    for lexical in ("yes", "TRUE", "", "unknown"):
        assert not evaluator._compare(lexical, "EQ", True)
        assert not evaluator._compare(lexical, "EQ", False)
    assert not evaluator._compare("1", "EQ", "true")
