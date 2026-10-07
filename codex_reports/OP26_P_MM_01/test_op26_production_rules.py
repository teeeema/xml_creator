from pathlib import Path
import pytest
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator, RuleStatus

BASE_DIR = Path(__file__).resolve().parents[2]
PACKAGE = BASE_DIR / "P.MM.01_OP_26"

def get_engine():
    return EaeuXmlEngine.load_process(PACKAGE)

def get_evaluator():
    return StructuredRuleEvaluator()

def test_all_16_messages_have_structured_rules():
    engine = get_engine()
    assert len(engine.rules) == 16
    total_rules = sum(len(r.structured_rules) for r in engine.rules.values())
    assert total_rules == 159, f"Expected 159 structured rules, got {total_rules}"

def test_rules_counts_per_message():
    engine = get_engine()
    expected_counts = {
        "P.MM.01.MSG.001": 39,
        "P.MM.01.MSG.002": 44,
        "P.MM.01.MSG.003": 6,
        "P.MM.01.MSG.007": 2,
        "P.MM.01.MSG.010": 1,
        "P.MM.01.MSG.012": 5,
        "P.MM.01.MSG.014": 1,
        "P.MM.01.MSG.016": 3,
        "P.MM.01.MSG.019": 11,
        "P.MM.01.MSG.020": 7,
        "P.MM.01.MSG.021": 14,
        "P.MM.01.MSG.023": 6,
        "P.MM.01.MSG.024": 5,
        "P.MM.01.MSG.025": 2,
        "P.MM.01.MSG.027": 7,
        "P.MM.01.MSG.028": 6,
    }
    for msg, count in expected_counts.items():
        assert len(engine.rules[msg].structured_rules) == count, f"Mismatch in {msg}"
