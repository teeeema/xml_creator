from pathlib import Path
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

P = Path(__file__).resolve().parents[1]; M = "P.SP.02.MSG.058"; D = "ipcdo:AccompanyingDocumentsDetails"


def test_document_requirements_are_per_document_parent():
    e = EaeuXmlEngine.load_process(P)
    r = next(x for x in e.rules[M].structured_rules if x["rule_id"].endswith("REQ.7"))
    values = {D: [{}, {}], f"{D}/csdo:DocName": ["a", "b"], f"{D}/csdo:DocId": ["1", None], f"{D}/csdo:DocCreationDate": ["2026-01-01", "2026-01-01"]}
    assert StructuredRuleEvaluator().evaluate(r, values).status is RuleStatus.FAIL
