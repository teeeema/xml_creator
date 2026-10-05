from pathlib import Path
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator
PACKAGE=Path(__file__).resolve().parents[1]; MESSAGE='P.SP.02.MSG.056'; P='ipcdo:IPPaymentDetails'; D=P+'/ipcdo:AccompanyingDocumentsDetails'
def test_document_requirements_remain_per_document_parent():
 e=EaeuXmlEngine.load_process(PACKAGE); r=next(x for x in e.rules[MESSAGE].structured_rules if x['rule_id'].endswith('REQ.18'))
 good={D:[{},{}],D+'/csdo:DocId':['1','2'],D+'/csdo:DocCreationDate':['2026-01-01','2026-01-01']}; assert StructuredRuleEvaluator().evaluate(r,good).status is RuleStatus.PASS
 good[D+'/csdo:DocId']=['1',None]; assert StructuredRuleEvaluator().evaluate(r,good).status is RuleStatus.FAIL
