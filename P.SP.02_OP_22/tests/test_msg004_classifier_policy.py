from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET
import pytest
from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.process_packages.body import GenerationMode
import importlib.util
spec=importlib.util.spec_from_file_location('msg004_fixture',Path(__file__).with_name('test_msg004_end_to_end.py'))
fixture=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
_engine, _generation_values, MESSAGE, APP, TRANSACTION = (getattr(fixture,n) for n in ('_engine','_generation_values','MESSAGE','APP','TRANSACTION'))

@pytest.mark.parametrize('case', ['positive','missing','wrong','both','name_only','wrong_namespace'])
def test_classifier_branch_raw_xml(case):
    e=_engine();s=e.get_structure(MESSAGE,mode=GenerationMode.TEST)
    root=ET.fromstring(ET.tostring(e.build_body(MESSAGE,_generation_values(),mode=GenerationMode.TEST).serialize_xml_element()))
    ns=s.imported_namespaces;owner=root.find('{'+ns['ipcdo']+'}TrademarkApplicationDetails');cq='{'+ns['ipsdo']+'}IPDocKindCode';nq='{'+ns['ipsdo']+'}IPDocKindName'
    if case in ('missing','name_only','wrong_namespace'):owner.remove(owner.find(cq))
    if case=='wrong':owner.find(cq).text='99999'
    if case in ('both','name_only'):ET.SubElement(owner,nq).text='Обращение'
    if case=='wrong_namespace':ET.SubElement(owner,'{urn:wrong}IPDocKindCode').text='07320'
    values,issues=e.body_provider._values_from_element(s,ET.fromstring(ET.tostring(root)))
    checked=e.validate_body(MESSAGE,values,mode=GenerationMode.TEST)
    target=next(r for r in checked.rule_evaluations if r.rule_id==MESSAGE+'.REQ.2')
    assert target.status.value==('PASS' if case=='positive' else 'FAIL')
    if case=='positive':
        assert checked.is_valid
        nested=APP+'/ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindName'
        assert values[nested]=='Приложение'


def test_form_resolver_and_application_sanitization(tmp_path):
    app=EaeuXmlApplication(Path(__file__).resolve().parents[2],drafts_root=tmp_path)
    form=app.get_form('P.SP.02',TRANSACTION,MESSAGE);f={x.path:x for x in app._walk_fields(form.fields)}
    c,n=APP+'/ipsdo:IPDocKindCode',APP+'/ipsdo:IPDocKindName'
    policies=app._effective_message_field_policies(app._engine('P.SP.02'),MESSAGE)
    assert f[c].effective_message_policy==policies[c].policy=='FIXED'
    assert f[c].fixed_value=='07320' and not f[c].editable
    assert f[n].effective_message_policy=='FORBIDDEN' and not f[n].editable
    assert app._sanitize_message_values('P.SP.02',MESSAGE,{c:'99999',n:'Bad'})=={c:'07320'}
