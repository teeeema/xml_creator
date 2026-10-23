from pathlib import Path
import sys,json,hashlib,importlib.util,copy
from dataclasses import asdict
from xml.etree import ElementTree as ET
from pypdf import PdfReader
from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.presentation.controller import GuiController
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
MSG='P.SP.02.MSG.004';TRN='P.SP.02.TRN.003';APP='ipcdo:TrademarkApplicationDetails';CODE=APP+'/ipsdo:IPDocKindCode';NAME=APP+'/ipsdo:IPDocKindName'
def run(phase):
 app=EaeuXmlApplication(ROOT);e=app._engine('P.SP.02');s=e.get_structure(MSG,mode=GenerationMode.TEST)
 spec=importlib.util.spec_from_file_location('fixture004',ROOT/'P.SP.02_OP_22/tests/test_msg004_end_to_end.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 form=app.get_form('P.SP.02',TRN,MSG);fields={f.path:f for f in app._walk_fields(form.fields)};pol=app._effective_message_field_policies(e,MSG) or {}
 gui=GuiController(app);gui.select_process('P.SP.02');gui.select_transaction(TRN);gui.select_message(MSG)
 result={'phase':phase,'transaction':asdict(e.transactions[TRN]),'structure':s.structure_id,'namespace':s.namespace,'fields':{p:{'form':asdict(fields[p]),'resolver':asdict(pol[p]) if p in pol else None,'gui_control':str(gui._control(gui.find_field(p)))} for p in (CODE,NAME)},'scenarios':{}}
 vals=m._generation_values();vals[CODE]='07320';vals.pop(NAME,None)
 root=ET.fromstring(ET.tostring(e.build_body(MSG,vals,mode=GenerationMode.TEST).serialize_xml_element()))
 ns=s.imported_namespaces;ownerq='{'+ns['ipcdo']+'}TrademarkApplicationDetails';cq='{'+ns['ipsdo']+'}IPDocKindCode';nq='{'+ns['ipsdo']+'}IPDocKindName'
 for case in ('positive','missing','forbidden','wrong_code','both','form_tamper','serializer_tamper'):
  x=copy.deepcopy(root);owner=x.find(ownerq)
  if case=='missing':owner.remove(owner.find(cq))
  if case in ('forbidden','both'):ET.SubElement(owner,nq).text='Forbidden Name'
  if case=='wrong_code':owner.find(cq).text='99999'
  if case in ('form_tamper','serializer_tamper'):
   stale=dict(vals);stale[CODE]='99999';stale[NAME]='Forbidden Name'
   if case=='form_tamper':stale=app._sanitize_message_values('P.SP.02',MSG,stale)
   try:
    x=ET.fromstring(ET.tostring(e.build_body(MSG,stale,mode=GenerationMode.TEST).serialize_xml_element()))
   except Exception as exc:
    if case!='serializer_tamper':raise
    result['scenarios'][case]={'expected_valid':False,'actual_valid':False,'matches_expected':True,'serializer_rejected':True,'exception':type(exc).__name__,'issues':[{'rule_id':i.rule_id,'code':i.code} for i in exc.issues]}
    continue
  raw=ET.tostring(x,encoding='utf-8',xml_declaration=True);filename=phase+'_'+case+'.xml';(OUT/filename).write_bytes(raw)
  actual,issues=e.body_provider._values_from_element(s,ET.fromstring(raw));v=e.validate_body(MSG,actual,mode=GenerationMode.TEST);owner=x.find(ownerq)
  expected=case in ('positive','form_tamper')
  # Direct serializer is a low-level builder, not an application sanitization boundary.
  if case=='serializer_tamper':expected=False
  result['scenarios'][case]={'expected_valid':expected,'actual_valid':v.is_valid,'matches_expected':expected==v.is_valid,'code':[n.text for n in owner.findall(cq)],'name':[n.text for n in owner.findall(nq)],'xml':filename,'sha256':hashlib.sha256(raw).hexdigest(),'extraction_issues':[str(i) for i in issues],'rule_results':{r.rule_id:r.status.value for r in v.rule_evaluations if r.rule_id==MSG+'.REQ.2'},'issues':[{'rule_id':i.rule_id,'code':i.code} for i in v.issues]}
 (OUT/(phase+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str))
 print(phase,[(k,v['actual_valid'],v.get('code'),v.get('name')) for k,v in result['scenarios'].items()])
 return result
if __name__=='__main__':run(sys.argv[1])
