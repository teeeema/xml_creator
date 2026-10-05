from pathlib import Path
import xml.etree.ElementTree as ET
import pytest
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

@pytest.fixture(scope='module')
def engine():
    return EaeuXmlEngine.load_process(Path(__file__).resolve().parents[1])


def extracted(engine,records):
    s=engine.resolve_structure('R.IP.SP.02.007',mode=GenerationMode.TEST).definition
    root=ET.Element(ET.QName(s.namespace,s.root_element))
    def child(parent,path,value=None):
        for qn in path.split('/'):
            pre,name=qn.split(':')
            parent=ET.SubElement(parent,ET.QName(s.imported_namespaces[pre],name))
        parent.text=value
        return parent
    for indicator,kind,status,flags in records:
        record=child(root,'ipcdo:UnifiedRegisterRecordsDetails')
        child(record,'ipcdo:TrademarkDetails/ipsdo:CollectiveMarkIndicator',indicator)
        child(record,'ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode',kind)
        child(record,'ipcdo:IPEntityStatusDetails/csdo:StatusCode',status)
        for flag in flags:child(record,'ipcdo:GoodsBaseDetails/ipsdo:CancellationStatusIndicator',flag)
    return engine.body_provider._values_from_element(s,ET.fromstring(ET.tostring(root)))[0]


@pytest.mark.parametrize('message,table',[('003','37'),('031','49'),('047','65'),('048','66'),('049','67'),('050','68'),('051','69'),('052','70'),('053','71')])
@pytest.mark.parametrize('case',['valid','inactive','wrong_owner','missing_role'])
@pytest.mark.parametrize('reverse',[False,True])
def test_collective_ue_party_is_required_in_same_record(engine,message,table,case,reverse):
    records=[('0' if case=='inactive' else '1',None if case=='missing_role' else ('RH' if case=='wrong_owner' else 'UE'),'01',[]),('0','UE','01',[])]
    if reverse:records.reverse()
    values=extracted(engine,records)
    rule=next(r for r in engine.rules[f'P.SP.02.MSG.{message}'].structured_rules if r['rule_id']==f'P.SP.02.MSG.{message}.T{table}.REQ.18')
    assert (StructuredRuleEvaluator().evaluate(rule,values).status is RuleStatus.FAIL)==(case in ('wrong_owner','missing_role'))


@pytest.mark.parametrize('message,table',[('020','53'),('052','70')])
@pytest.mark.parametrize('records,passes',[
    ([('0','RH','04',['0'])],True),
    ([('0','RH','04',['0','1'])],False),
    ([('0','RH','04',['0','1']),('0','RH','01',[])],True),
    ([('0','RH','01',[]),('0','RH','04',['1','0'])],True),
    ([('0','RH','04',['0']),('0','RH','03',['1'])],True),
    ([('0','RH','04',[None])],True),
    ([('0','RH','04',['true'])],False),
    ([('0','RH','04',['true']),('0','RH','01',[])],True),
])
def test_msg052_new_record_required_after_cancel_goods_filter(engine,records,passes,message,table):
    values=extracted(engine,records)
    rule=next(r for r in engine.rules[f'P.SP.02.MSG.{message}'].structured_rules if r['rule_id']==f'P.SP.02.MSG.{message}.T{table}.REQ.3')
    assert (StructuredRuleEvaluator().evaluate(rule,values).status is RuleStatus.PASS)==passes


@pytest.mark.parametrize('requirement',[30,31])
@pytest.mark.parametrize('bad',[False,True],ids=['positive','negative'])
@pytest.mark.parametrize('reverse',[False,True])
def test_msg029_goods_filtered_cardinality_stays_with_application(engine,requirement,bad,reverse):
    s=engine.resolve_structure('R.IP.SP.02.002',mode=GenerationMode.TEST).definition
    def q(pre,name):return str(ET.QName(s.imported_namespaces[pre],name))
    root=ET.Element(ET.QName(s.namespace,s.root_element))
    cases=[('01' if requirement==30 else '02', ['0'] if (bad and requirement==30) or (not bad and requirement==31) else ['1']), ('01' if requirement==31 else '02',['1'] if requirement==31 else ['0'])]
    if reverse:cases.reverse()
    for registration, flags in cases:
        app=ET.SubElement(root,q('ipcdo','TrademarkApplicationDetails'))
        ET.SubElement(app,q('ipsdo','TrademarkRegistrationCode')).text=registration
        for flag in flags:ET.SubElement(ET.SubElement(app,q('ipcdo','GoodsBaseDetails')),q('ipsdo','TrademarkDecisionIndicator')).text=flag
    values=engine.body_provider._values_from_element(s,ET.fromstring(ET.tostring(root)))[0]
    rule=next(r for r in engine.rules['P.SP.02.MSG.029'].structured_rules if r['rule_id']==f'P.SP.02.MSG.029.T45.REQ.{requirement}')
    assert (StructuredRuleEvaluator().evaluate(rule,values).status is RuleStatus.FAIL)==bad


@pytest.mark.parametrize('bank,payment_system',[(False,False),(True,False),(False,True),(True,True)])
@pytest.mark.parametrize('wrong_owner',[False,True])
def test_msg055_inclusive_account_or_per_payment_owner(engine,bank,payment_system,wrong_owner):
    s=engine.resolve_structure('R.IP.SP.03.003',mode=GenerationMode.TEST).definition
    def q(pre,name):return str(ET.QName(s.imported_namespaces[pre],name))
    root=ET.Element(ET.QName(s.namespace,s.root_element))
    payment=ET.SubElement(root,q('ipcdo','IPPaymentDetails'))
    other=ET.SubElement(root,q('ipcdo','IPPaymentDetails')) if wrong_owner else payment
    if bank:ET.SubElement(other,q('ccdo','BankAccountDetails'))
    if payment_system:ET.SubElement(other,q('ccdo','PaymentSystemAccountDetails'))
    values=engine.body_provider._values_from_element(s,ET.fromstring(ET.tostring(root)))[0]
    rules=[r for r in engine.rules['P.SP.02.MSG.055'].structured_rules if r['rule_id'].startswith('P.SP.02.MSG.055.T73.REQ.7.')]
    assert len(rules)==2
    statuses=[StructuredRuleEvaluator().evaluate(r,values).status for r in rules]
    assert (RuleStatus.FAIL not in statuses)==((bank or payment_system) and not wrong_owner)


def test_msg055_payment_presence_is_not_created_by_rule(engine):
    s=engine.resolve_structure('R.IP.SP.03.003',mode=GenerationMode.TEST).definition
    root=ET.Element(ET.QName(s.namespace,s.root_element))
    before=ET.tostring(root)
    values=engine.body_provider._values_from_element(s,root)[0]
    rule=next(r for r in engine.rules['P.SP.02.MSG.055'].structured_rules if r['rule_id'].endswith('REQ.7.PRESENCE'))
    assert StructuredRuleEvaluator().evaluate(rule,values).status is RuleStatus.FAIL
    assert ET.tostring(root)==before
