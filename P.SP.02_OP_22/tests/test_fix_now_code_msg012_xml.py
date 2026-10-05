"""Table45 inherited Table34 rules on the production structure and extractor."""
from pathlib import Path
import xml.etree.ElementTree as ET
import pytest
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = 'P.SP.02.MSG.012'

@pytest.fixture(scope='module')
def engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def values_for(engine, requirement, invalid, active_first, message=MESSAGE):
    structure = engine.resolve_structure('R.IP.SP.02.002', mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    def child(parent, prefix, local, text=None, **attrs):
        elem = ET.SubElement(parent, ET.QName(structure.imported_namespaces[prefix],local),attrs)
        elem.text = text
        return elem
    for status in (['01','02'] if active_first else ['02','01']):
        app = child(root,'ipcdo','TrademarkApplicationDetails')
        child(child(app,'ipcdo','IPEntityStatusDetails'),'csdo','StatusCode',status)
        for index, role in enumerate(('AP','PA','RE','AP')):
            party = child(app,'ipcdo','IPPartyDetails')
            child(party,'ipsdo','IPPartyKindCode',role)
            is_bad = invalid and status=='01' and index==3
            lang = 'EN' if requirement==19 else 'RU'
            attrs = {'nameRepresentationKindCode':'OR','languageCode':lang}
            if (status=='02' and message in (MESSAGE,'P.SP.02.MSG.043')) or role!='AP': attrs={'nameRepresentationKindCode':'ZZ'}
            elif is_bad and requirement==16: attrs['nameRepresentationKindCode']='ZZ'
            elif is_bad and requirement==17 and invalid is True: attrs.pop('languageCode')
            elif is_bad and requirement==17 and invalid=='missing_original': attrs['nameRepresentationKindCode']='LA'
            child(party,'ipsdo','IPSubjectName','Original',**attrs)
            if is_bad and requirement==17 and invalid=='duplicate_original':
                child(party,'ipsdo','IPSubjectName','Duplicate',nameRepresentationKindCode='OR',languageCode='RU')
            if requirement==19 and not is_bad:
                child(party,'ipsdo','IPSubjectName','Latin',nameRepresentationKindCode='LA')
            if requirement==18 and is_bad:
                child(party,'ipsdo','IPSubjectName','Forbidden',nameRepresentationKindCode='LA')
            addr=child(party,'ccdo','SubjectAddressDetails')
            child(addr,'csdo','AddressKindCode','3' if is_bad and requirement==20 else '2')
    parsed=ET.fromstring(ET.tostring(root))
    return engine.body_provider._values_from_element(structure,parsed)[0]


@pytest.mark.parametrize('message,table', [('P.SP.02.MSG.001','34'), ('P.SP.02.MSG.031','48'), ('P.SP.02.MSG.012', '45'), ('P.SP.02.MSG.061', '80'), ('P.SP.02.MSG.062', '81'), ('P.SP.02.MSG.032', '50'), ('P.SP.02.MSG.033', '51'), ('P.SP.02.MSG.034', '52'), ('P.SP.02.MSG.035', '53'), ('P.SP.02.MSG.036', '54'), ('P.SP.02.MSG.037', '55'), ('P.SP.02.MSG.038', '56'), ('P.SP.02.MSG.039', '57'), ('P.SP.02.MSG.040', '58'), ('P.SP.02.MSG.041', '59'), ('P.SP.02.MSG.042', '60'), ('P.SP.02.MSG.043', '61'), ('P.SP.02.MSG.045', '63'), ('P.SP.02.MSG.027','57'), ('P.SP.02.MSG.028','44'), ('P.SP.02.MSG.029','45'), ('P.SP.02.MSG.030','46')])
@pytest.mark.parametrize('requirement',[16,17,18,19,20])
@pytest.mark.parametrize('invalid',[False,True],ids=['positive','negative'])
@pytest.mark.parametrize('active_first',[False,True],ids=['OLD_NEW','NEW_OLD'])
def test_production_requirement_per_owner(engine, requirement, invalid, active_first, message, table):
    values=values_for(engine,requirement,invalid,active_first,message)
    prefix=f'{message}.T{table}.REQ.{requirement}'
    rules=[r for r in engine.rules[message].structured_rules if r['rule_id']==prefix or r['rule_id'].startswith(prefix+'.') or (message=='P.SP.02.MSG.001' and (r['rule_id']==f'{message}.REQ.{requirement:03}' or r['rule_id'].startswith(f'{message}.REQ.{requirement:03}.')))]
    assert rules
    results=[StructuredRuleEvaluator().evaluate(r,values).status for r in rules]
    assert (RuleStatus.FAIL in results)==invalid
    assert all(s in (RuleStatus.PASS,RuleStatus.FAIL) for s in results)


@pytest.mark.parametrize('message,table',[('P.SP.02.MSG.001','34'), ('P.SP.02.MSG.031','48'), ('P.SP.02.MSG.012', '45'), ('P.SP.02.MSG.061', '80'), ('P.SP.02.MSG.062', '81'), ('P.SP.02.MSG.032', '50'), ('P.SP.02.MSG.033', '51'), ('P.SP.02.MSG.034', '52'), ('P.SP.02.MSG.035', '53'), ('P.SP.02.MSG.036', '54'), ('P.SP.02.MSG.037', '55'), ('P.SP.02.MSG.038', '56'), ('P.SP.02.MSG.039', '57'), ('P.SP.02.MSG.040', '58'), ('P.SP.02.MSG.041', '59'), ('P.SP.02.MSG.042', '60'), ('P.SP.02.MSG.043', '61'), ('P.SP.02.MSG.045', '63'), ('P.SP.02.MSG.027','57'), ('P.SP.02.MSG.028','44'), ('P.SP.02.MSG.029','45'), ('P.SP.02.MSG.030','46')])
@pytest.mark.parametrize('code_ok,name_ok',[(False,False),(True,False),(False,True),(True,True)])
def test_existing_production_inclusive_or_truth_table(engine,code_ok,name_ok,message,table):
    structure=engine.resolve_structure('R.IP.SP.02.002',mode=GenerationMode.TEST).definition
    def q(prefix,name):return str(ET.QName(structure.imported_namespaces[prefix],name))
    root=ET.Element(ET.QName(structure.namespace,structure.root_element))
    app=ET.SubElement(root,q('ipcdo','TrademarkApplicationDetails'))
    ET.SubElement(ET.SubElement(app,q('ipcdo','IPEntityStatusDetails')),q('csdo','StatusCode')).text='01'
    tm=ET.SubElement(app,q('ipcdo','TrademarkDetails'))
    if code_ok:ET.SubElement(tm,q('ipsdo','TrademarkKindCode')).text='110'
    if name_ok:ET.SubElement(tm,q('ipsdo','TrademarkKindName')).text='Словесный знак'
    values=engine.body_provider._values_from_element(structure,ET.fromstring(ET.tostring(root)))[0]
    rule=next(r for r in engine.rules[message].structured_rules if r['rule_id'] in (f'{message}.T{table}.REQ.26', f'{message}.REQ.026'))
    assert (StructuredRuleEvaluator().evaluate(rule,values).status is RuleStatus.PASS)==(code_ok or name_ok)


@pytest.mark.parametrize('requirement,role',[(15,'AP'),(21,'PA'),(22,'RE')])
@pytest.mark.parametrize('bad',[False,True],ids=['positive','negative'])
def test_msg001_filtered_fields_cannot_be_borrowed(engine,requirement,role,bad):
    structure=engine.resolve_structure('R.IP.SP.02.002',mode=GenerationMode.TEST).definition
    root=ET.Element(ET.QName(structure.namespace,structure.root_element))
    def child(parent,path,text=None):
        for token in path.split('/'):
            prefix,local=token.split(':')
            parent=ET.SubElement(parent,ET.QName(structure.imported_namespaces[prefix],local))
        parent.text=text
        return parent
    app=child(root,'ipcdo:TrademarkApplicationDetails')
    for index,r in enumerate((role,'PA' if role!='PA' else 'RE',role)):
        party=child(app,'ipcdo:IPPartyDetails')
        child(party,'ipsdo:IPPartyKindCode',r)
        if not (bad and index==2): child(party,'csdo:UnifiedCountryCode','RU')
        child(party,'ipsdo:IPSubjectName','Name')
        child(party,'ccdo:SubjectAddressDetails/csdo:AddressKindCode','2')
        child(party,'ccdo:CommunicationDetails/csdo:CommunicationChannelId','email')
        child(party,'ipsdo:PatentAttorneyId','ATTORNEY')
    values=engine.body_provider._values_from_element(structure,ET.fromstring(ET.tostring(root)))[0]
    rule=next(r for r in engine.rules['P.SP.02.MSG.001'].structured_rules if r['rule_id']==f'P.SP.02.MSG.001.REQ.{requirement:03}')
    assert (StructuredRuleEvaluator().evaluate(rule,values).status is RuleStatus.FAIL)==bad


@pytest.mark.parametrize('count',[0,1,2])
def test_msg001_cardinality_counts_ap_after_filter(engine,count):
    structure=engine.resolve_structure('R.IP.SP.02.002',mode=GenerationMode.TEST).definition
    def q(prefix,local):return str(ET.QName(structure.imported_namespaces[prefix],local))
    root=ET.Element(ET.QName(structure.namespace,structure.root_element))
    app=ET.SubElement(root,q('ipcdo','TrademarkApplicationDetails'))
    for role in ['PA','RE']+['AP']*count:
        ET.SubElement(ET.SubElement(app,q('ipcdo','IPPartyDetails')),q('ipsdo','IPPartyKindCode')).text=role
    values=engine.body_provider._values_from_element(structure,ET.fromstring(ET.tostring(root)))[0]
    rule=next(r for r in engine.rules['P.SP.02.MSG.001'].structured_rules if r['rule_id']=='P.SP.02.MSG.001.REQ.014')
    assert (StructuredRuleEvaluator().evaluate(rule,values).status is RuleStatus.PASS)==(count==1)


@pytest.mark.parametrize('bad',[False,True],ids=['positive','negative'])
def test_msg001_document_fields_stay_with_each_document(engine,bad):
    structure=engine.resolve_structure('R.IP.SP.02.002',mode=GenerationMode.TEST).definition
    def q(prefix,local):return str(ET.QName(structure.imported_namespaces[prefix],local))
    root=ET.Element(ET.QName(structure.namespace,structure.root_element))
    app=ET.SubElement(root,q('ipcdo','TrademarkApplicationDetails'))
    for i in range(2):
        doc=ET.SubElement(app,q('ipcdo','AccompanyingDocumentsDetails'))
        for prefix,local,text in [('ipsdo','IPDocKindCode','001'),('ipsdo','IPDocKindName','Name'),('csdo','DocId','ID'),('csdo','DocCreationDate','2026-01-01'),('csdo','DescriptionText','Description'),('csdo','PageQuantity','1')]:
            if not (bad and i==1 and local=='DocId'):ET.SubElement(doc,q(prefix,local)).text=text
    values=engine.body_provider._values_from_element(structure,ET.fromstring(ET.tostring(root)))[0]
    rule=next(r for r in engine.rules['P.SP.02.MSG.001'].structured_rules if r['rule_id']=='P.SP.02.MSG.001.REQ.033')
    assert (StructuredRuleEvaluator().evaluate(rule,values).status is RuleStatus.FAIL)==bad


@pytest.mark.parametrize('message,table',[('P.SP.02.MSG.001', '34'), ('P.SP.02.MSG.031', '48'), ('P.SP.02.MSG.012', '45'), ('P.SP.02.MSG.061', '80'), ('P.SP.02.MSG.062', '81'), ('P.SP.02.MSG.032', '50'), ('P.SP.02.MSG.033', '51'), ('P.SP.02.MSG.034', '52'), ('P.SP.02.MSG.035', '53'), ('P.SP.02.MSG.036', '54'), ('P.SP.02.MSG.037', '55'), ('P.SP.02.MSG.038', '56'), ('P.SP.02.MSG.039', '57'), ('P.SP.02.MSG.040', '58'), ('P.SP.02.MSG.041', '59'), ('P.SP.02.MSG.042', '60'), ('P.SP.02.MSG.043', '61'), ('P.SP.02.MSG.045', '63'), ('P.SP.02.MSG.027', '57'), ('P.SP.02.MSG.028', '44'), ('P.SP.02.MSG.029', '45'), ('P.SP.02.MSG.030', '46')])
@pytest.mark.parametrize('case',['missing_original','duplicate_original'])
@pytest.mark.parametrize('active_first',[False,True],ids=['OLD_NEW','NEW_OLD'])
def test_original_name_count_is_exactly_one_per_ap(engine,message,table,case,active_first):
    values=values_for(engine,17,case,active_first,message)
    rule_id=f'{message}.REQ.017' if message=='P.SP.02.MSG.001' else f'{message}.T{table}.REQ.17'
    rule=next(r for r in engine.rules[message].structured_rules if r['rule_id']==rule_id)
    assert StructuredRuleEvaluator().evaluate(rule,values).status is RuleStatus.FAIL
