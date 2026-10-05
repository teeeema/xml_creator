from pathlib import Path
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.038"
APP = "ipcdo:TrademarkApplicationDetails"
PRIORITY = f"{APP}/ipcdo:TrademarkPriorityDetails"

def rule(code):
    engine = EaeuXmlEngine.load_process(PACKAGE)
    prefix = f"{MESSAGE}.T56.REQ.{code}"
    return engine, [r for r in engine.rules[MESSAGE].structured_rules if r["rule_id"] == prefix]

def test_priority_fields_are_checked_per_priority_parent():
    _, rules = rule(30)
    values = {PRIORITY: [{}, {}], f"{PRIORITY}/ipsdo:PriorityKindCode": ["P", None], f"{PRIORITY}/ipsdo:PriorityDate": ["2026-01-01", "2026-01-02"], f"{PRIORITY}/csdo:UnifiedCountryCode": ["RU", "BY"]}
    assert StructuredRuleEvaluator().evaluate(rules[0], values).status is RuleStatus.FAIL
def test_all_qname_documents_require_exactly_five_children_per_instance():
    _, rules = rule(32)
    values = {"ipcdo:AccompanyingDocumentsDetails": [{}, {}], "ipcdo:AccompanyingDocumentsDetails/csdo:DocName": ["a", "b"], "ipcdo:AccompanyingDocumentsDetails/csdo:DocId": ["1", "2"], "ipcdo:AccompanyingDocumentsDetails/csdo:DocCreationDate": ["2026-01-01", "2026-01-01"], "ipcdo:AccompanyingDocumentsDetails/csdo:DescriptionText": ["d", None], "ipcdo:AccompanyingDocumentsDetails/csdo:PageQuantity": ["1", "1"]}
    assert StructuredRuleEvaluator().evaluate(rules[0], values).status is RuleStatus.FAIL
