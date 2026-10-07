import pytest
from pathlib import Path
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator, RuleStatus

BASE_DIR = Path(__file__).resolve().parents[2]
engine = EaeuXmlEngine.load_process(BASE_DIR / "P.MM.01_OP_26")
evaluator = StructuredRuleEvaluator()

print("Engine and evaluator initialized.")
