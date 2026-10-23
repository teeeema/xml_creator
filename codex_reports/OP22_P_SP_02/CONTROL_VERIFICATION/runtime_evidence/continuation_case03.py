"""Post-audit CV03: actual form/resolver and raw XML trust-boundary proof."""
from copy import deepcopy
from dataclasses import asdict
import json
from xml.etree import ElementTree as ET

from continuation_audit import ROOT, OUT, field, load, xml_check
from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.process_packages.body import GenerationMode


def main():
    app = EaeuXmlApplication(ROOT)
    engine = app._engine('P.SP.02')
    msg = 'P.SP.02.MSG.027'
    parent = 'ipcdo:TrademarkApplicationDetails'
    paths = [parent + '/ipsdo:IPDocKindCode', parent + '/ipsdo:IPDocKindName']
    states = field(app, 'P.SP.02', 'P.SP.02.TRN.022', msg, paths)
    assert states[paths[0]]['get_form']['fixed_value'] == '07365'
    assert states[paths[0]]['resolver']['policy'] == 'FIXED'
    assert not states[paths[0]]['get_form']['editable']
    assert states[paths[1]]['resolver']['policy'] == 'FORBIDDEN'
    assert not states[paths[1]]['get_form']['editable']
    proof = load('op22_branch_runtime')
    fixture = proof.fixture_module('027')
    values = fixture._valid_values()
    stale = dict(values)
    stale[paths[0]], stale[paths[1]] = '99999', fixture.FALLBACK
    sanitized = app._sanitize_message_values('P.SP.02', msg, stale)
    assert sanitized[paths[0]] == '07365' and paths[1] not in sanitized
    body = engine.build_body(msg, sanitized, mode=GenerationMode.TEST)
    root = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    structure = engine.get_structure(msg, mode=GenerationMode.TEST)
    ns = structure.imported_namespaces
    parentq = '{' + ns['ipcdo'] + '}TrademarkApplicationDetails'
    codeq = '{' + ns['ipsdo'] + '}IPDocKindCode'
    nameq = '{' + ns['ipsdo'] + '}IPDocKindName'
    owner = root.find(parentq)
    assert owner.find(codeq).text == '07365' and owner.find(nameq) is None
    rule = msg + '.T57.REQ.2'
    outcomes = {'positive': xml_check(engine, msg, root, 'cv03_positive.xml', [rule])}
    for label in ('wrong_code', 'both', 'missing_code', 'legacy_name_only'):
        changed = deepcopy(root)
        owner = changed.find(parentq)
        code = owner.find(codeq)
        if label == 'wrong_code':
            code.text = '99999'
        if label in ('missing_code', 'legacy_name_only'):
            owner.remove(code)
        if label in ('both', 'legacy_name_only'):
            ET.SubElement(owner, nameq).text = fixture.FALLBACK
        outcomes[label] = xml_check(engine, msg, changed, 'cv03_' + label + '.xml', [rule])
    assert outcomes['positive']['valid'] and outcomes['positive']['rule_results'][rule] == 'PASS'
    for label, evidence in outcomes.items():
        assert not evidence['extraction_issues'], (label, evidence)
        if label != 'positive':
            assert not evidence['valid'] and evidence['rule_results'][rule] == 'FAIL', (label, evidence)
    result = {'process': 'P.SP.02', 'transaction': 'P.SP.02.TRN.022', 'message': msg,
              'requirements': [rule], 'fields': states, 'sanitization_checked': True,
              'scenarios': outcomes, 'result': 'PASS'}
    (OUT / 'continuation_case03.json').write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    print('CV03 PASS: form FIXED07365/FORBIDDEN, sanitization, positive XML, 4 rejected raw XML mutations')


if __name__ == '__main__':
    main()
