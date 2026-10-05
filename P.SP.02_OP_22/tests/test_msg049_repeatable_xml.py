from pathlib import Path
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE=Path(__file__).resolve().parents[1]
MESSAGE="P.SP.02.MSG.049"
R007="ipcdo:UnifiedRegisterRecordsDetails"
RESOURCE=f"{R007}/ccdo:ResourceItemStatusDetails"
STATUS=f"{R007}/ipcdo:IPEntityStatusDetails"
SIG=f"{R007}/ipcdo:SignatureDetails"
OFF=f"{SIG}/ipcdo:OfficerDetails"
EXACT="Заявление о внесении изменений в сведения Единого реестра товарных знаков, знаков обслуживания Евразийского экономического союза"

def _rules(code):
    eng=EaeuXmlEngine.load_process(PACKAGE)
    p=f"{MESSAGE}.T67.REQ.{code}"
    return [r for r in eng.rules[MESSAGE].structured_rules if r["rule_id"]==p or r["rule_id"].startswith(p+".")]

def _statuses(code,values):
    ev=StructuredRuleEvaluator()
    return [ev.evaluate(r,values).status for r in _rules(code)]

def _pass(code,v): assert all(s is RuleStatus.PASS for s in _statuses(code,v))
def _fail(code,v): assert RuleStatus.FAIL in _statuses(code,v)

def test_req1_and_req2_record_scope():
    _pass(1,{R007:[{}],f"{R007}/ipsdo:TrademarkId":["TM1"]})
    _fail(1,{R007:[{}]})
    _fail(2,{R007:[]}); _pass(2,{R007:[{}]}); _fail(2,{R007:[{},{}]})

def test_req3_req4_resource_validity_owner_and_repeatable_alignment():
    valid={RESOURCE:[{},{}],f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:StartDateTime":["2026-01-01T00:00:00","2026-01-02T00:00:00"]}
    _pass(3,valid); _pass(4,valid)
    _fail(3,{RESOURCE:[{},{}],f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:StartDateTime":["2026-01-01T00:00:00",None]})
    _fail(4,{**valid,f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:EndDateTime":[None,"2026-02-01T00:00:00"]})
    _fail(3,{RESOURCE:[{}],f"{STATUS}/ccdo:ValidityPeriodDetails/csdo:StartDateTime":["2026-01-01T00:00:00"]})

def test_req5_status_owner_isolation():
    good={STATUS:[{},{}],f"{STATUS}/csdo:StatusCode":["03","03"],f"{STATUS}/csdo:EventDate":["2026-09-30","2026-09-30"]}
    _pass(5,good)
    _fail(5,{**good,f"{STATUS}/csdo:StatusCode":["03","01"]})
    _fail(5,{**good,f"{STATUS}/csdo:EventDate":["2026-09-30",None]})
    _fail(5,{**good,f"{STATUS}/csdo:StatusCode/@codeListId":[None,"X"]})

def test_req6_17_meaningful_negative_repeatable_proofs():
    goods=f"{R007}/ipcdo:GoodsBaseDetails"
    good={goods:[{},{}],f"{goods}/ipsdo:GoodsClassCode":["09","42"],f"{goods}/ipsdo:GoodsClassName":["A","B"],f"{goods}/ipsdo:GoodsName":["A","B"],f"{goods}/ipsdo:TrademarkDecisionIndicator":["1","1"],f"{goods}/ipsdo:TrademarkApplicationId":["A","B"]}
    _pass(16,good); _pass(17,good)
    _fail(16,{**good,f"{goods}/ipsdo:GoodsClassCode":["09",None]})
    _fail(17,{**good,f"{goods}/ipsdo:TrademarkId":[None,"TM"]})

def test_req21_req22_same_record_document_kind():
    _pass(21,{R007:[{},{}],f"{R007}/ipsdo:IPDocKindCode":["A","B"],f"{R007}/ipsdo:IPDocKindName":[None,None]})
    _fail(21,{R007:[{},{}],f"{R007}/ipsdo:IPDocKindCode":["A","B"],f"{R007}/ipsdo:IPDocKindName":[None,"bad"]})
    _pass(22,{R007:[{}],f"{R007}/ipsdo:IPDocKindName":[EXACT]})
    _fail(22,{R007:[{}],f"{R007}/ipsdo:IPDocKindName":["wrong"]})

def test_req23_25_signature_same_parent_and_cross_parent_isolation():
    _pass(23,{SIG:[{},{}],f"{SIG}/ipcdo:OfficerDetails":[{},None],f"{SIG}/ccdo:FullNameDetails":[None,{}]})
    _fail(23,{SIG:[{},{}],f"{SIG}/ipcdo:OfficerDetails":[{},None],f"{SIG}/ccdo:FullNameDetails":[{},None]})
    _fail(24,{SIG:[{},{}],f"{SIG}/ccdo:FullNameDetails":[None,{}],f"{SIG}/ipcdo:OfficerDetails":[None,{}]})
    good={OFF:[{},{}],f"{OFF}/ccdo:FullNameDetails/csdo:LastName":["A","B"],f"{OFF}/ccdo:FullNameDetails/csdo:FirstName":["C","D"],f"{OFF}/csdo:PositionName":["P","P"]}
    _pass(25,good)
    _fail(25,{**good,f"{OFF}/ccdo:FullNameDetails/csdo:LastName":["A",None]})
    _fail(25,{**good,f"{OFF}/ccdo:CommunicationDetails":[None,{}]})
