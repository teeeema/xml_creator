from pathlib import Path
import json
import pytest
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator, RuleStatus

BASE_DIR = Path(__file__).resolve().parents[2]
PACKAGE = BASE_DIR / "P.MM.01_OP_26"

def get_engine():
    return EaeuXmlEngine.load_process(PACKAGE)

def get_evaluator():
    return StructuredRuleEvaluator()

def test_all_16_messages_have_source_traced_structured_rules():
    engine = get_engine()
    assert len(engine.rules) == 16
    assert all(rules.structured_rules for rules in engine.rules.values())
    for rules in engine.rules.values():
        for rule in rules.structured_rules:
            assert rule.get("rule_id")
            source_refs = rule.get("source_refs") or []
            assert source_refs
            assert all(ref.get("status") == "CONFIRMED" for ref in source_refs)

def test_structured_rule_inventory_has_expected_messages_and_no_exact_duplicates():
    engine = get_engine()
    expected_messages = {
        "P.MM.01.MSG.001", "P.MM.01.MSG.002", "P.MM.01.MSG.003", "P.MM.01.MSG.007",
        "P.MM.01.MSG.010", "P.MM.01.MSG.012", "P.MM.01.MSG.014", "P.MM.01.MSG.016",
        "P.MM.01.MSG.019", "P.MM.01.MSG.020", "P.MM.01.MSG.021", "P.MM.01.MSG.023",
        "P.MM.01.MSG.024", "P.MM.01.MSG.025", "P.MM.01.MSG.027", "P.MM.01.MSG.028",
    }
    assert set(engine.rules) == expected_messages
    for message_code, rules in engine.rules.items():
        serialized = [json.dumps(rule, ensure_ascii=False, sort_keys=True) for rule in rules.structured_rules]
        assert len(serialized) == len(set(serialized)), f"Exact duplicate structured rule in {message_code}"
