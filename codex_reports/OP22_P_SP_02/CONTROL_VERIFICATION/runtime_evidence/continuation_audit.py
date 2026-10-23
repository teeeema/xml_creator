"""Read-only product audit; writes evidence only. No external classifier is fabricated."""
from pathlib import Path
from copy import deepcopy
from dataclasses import asdict
import hashlib
import importlib.util
import json
from xml.etree import ElementTree as ET

from pypdf import PdfReader
from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.process_packages.body import GenerationMode

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
NORM = Path('/Users/tema/Documents/Work/Документы_xml')


def load(name):
    spec = importlib.util.spec_from_file_location(name, OUT / (name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def source_audit():
    selections = {
        'ОП_22.pdf': {578: ['IPDocKindCode', 'IPDocKindName'],
                      801: ['P.SP.02.MSG.054', 'справочника'],
                      802: ['IPLegalActionKindCode', 'IPLegalActionKindName'],
                      803: ['csdo:DocId', 'не заполняются'],
                      807: ['18', 'csdo:DocId', 'AccompanyingDocumentsDetails'],
                      722: ['33', 'csdo:DocId'],
                      879: ['2.16.4', 'csdo:DocId']},
        'ОП_23.pdf': {342: ['csdo:DocId', 'csdo:AuthorityName'],
                      350: ['ConsentToDataProcessingIndicator'],
                      344: ['21', 'AP', 'OR', 'languageCode'],
                      542: ['csdo:DocId'], 565: ['8.10.4', 'csdo:DocId']},
        '26_ОП.pdf': {39: ['P.CLS.019'], 213: ['34', 'codeListId']},
        '49_ОП.pdf': {79: ['DailyInfoIndicator', '2', '3']},
        '92 решение.pdf': {15: ['07365']},
        '148 решение.pdf': {4: ['07365']},
    }
    result = {}
    for name, pages in selections.items():
        path = NORM / name
        reader = PdfReader(path)
        checked = {}
        for number, terms in pages.items():
            text = reader.pages[number - 1].extract_text() or ''
            assert all(t in text for t in terms), (name, number, terms)
            checked[number] = {'expected_terms': terms, 'text': text}
        result[name] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'path': str(path), 'pages': checked}
    (OUT / 'continuation_sources.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def field(app, process, trn, message, paths):
    form = app.get_form(process, trn, message)
    views = {f.path: f for f in app._walk_fields(form.fields)}
    policies = app._effective_message_field_policies(app._engine(process), message) or {}
    return {p: {'get_form': asdict(views[p]),
                'resolver': asdict(policies[p]) if p in policies else None} for p in paths}


def xml_check(engine, msg, root, filename, rules):
    raw = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    (OUT / filename).write_bytes(raw)
    structure = engine.get_structure(msg, mode=GenerationMode.TEST)
    values, issues = engine.body_provider._values_from_element(structure, ET.fromstring(raw))
    validation = engine.validate_body(msg, values, mode=GenerationMode.TEST)
    return {'xml': filename, 'sha256': hashlib.sha256(raw).hexdigest(),
            'root_qname': root.tag, 'extraction_issues': [str(i) for i in issues],
            'valid': validation.is_valid, 'complete': validation.is_complete,
            'rule_results': {r.rule_id: r.status.value for r in validation.rule_evaluations
                             if r.rule_id in rules},
            'issues': [{'rule_id': i.rule_id, 'code': i.code} for i in validation.issues]}


def extra_cases():
    app = EaeuXmlApplication(ROOT)
    # CV04: execute available conditional branches, without asserting the
    # unavailable authoritative publication state or assigning an invented code.
    e22 = app._engine('P.SP.02')
    msg = 'P.SP.02.MSG.054'
    root = ET.parse(OUT / 'cv05_msg054_positive.xml').getroot()
    rules = tuple(r['rule_id'] for r in e22.rules[msg].structured_rules
                  if r['rule_id'] == msg + '.T72.REQ.4' or '.REQ.5.' in r['rule_id'])
    ns = e22.get_structure(msg, mode=GenerationMode.TEST).imported_namespaces
    nameq = '{' + ns['ipsdo'] + '}IPLegalActionKindName'
    codeq = '{' + ns['ipsdo'] + '}IPLegalActionKindCode'
    outcomes = {'name_branch': xml_check(e22, msg, root, 'cv04_name_branch.xml', rules)}
    for label in ('bad_name', 'missing_name', 'both', 'unverified_code_only'):
        changed = deepcopy(root)
        name = changed.find(nameq)
        assert name is not None
        if label == 'bad_name':
            name.text = 'INVALID-LEGAL-ACTION'
        if label in ('missing_name', 'unverified_code_only'):
            changed.remove(name)
        if label in ('both', 'unverified_code_only'):
            ET.SubElement(changed, codeq).text = 'UNVERIFIED-TEST-CODE'
        outcomes[label] = xml_check(e22, msg, changed, 'cv04_' + label + '.xml', rules)
    assert outcomes['name_branch']['valid']
    assert all(not outcomes[k]['valid'] for k in ('bad_name', 'missing_name', 'both'))
    case4 = {'process': 'P.SP.02', 'transaction': 'P.SP.02.TRN.049', 'message': msg,
             'requirements': list(rules), 'fields': field(app, 'P.SP.02', 'P.SP.02.TRN.049', msg,
                    ['ipsdo:IPLegalActionKindCode', 'ipsdo:IPLegalActionKindName']),
             'result': 'SOURCE_BLOCKED', 'dependency_status': 'STILL_EXTERNAL',
             'reason': 'T72 REQ4/5 depend on publication and payload of the named legal-action reference. '
                       'No authoritative payload/publication-state artifact is identified in the local source registry '
                       'or normative_classifier_data. Code absence is not proof of reference absence. '
                       'Name-branch tests are implementation evidence only; code membership cannot be certified.',
             'local_source_inventory': sorted(str(p.relative_to(NORM)) for p in NORM.rglob('*') if p.is_file()),
             'classifier_inventory': sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'P.SP.02_OP_22/normative_classifier_data').rglob('*') if p.is_file()),
             'scenarios': outcomes}

    # CV15: fully source-defined contextual AP/OR rule in OP23, no external data.
    e23 = app._engine('P.SP.03')
    msg = 'P.SP.03.MSG.001'
    root = ET.parse(OUT / 'op26_op23_B_case08_positive.xml').getroot()
    ns = e23.get_structure(msg, mode=GenerationMode.TEST).imported_namespaces
    path = 'ipcdo:ApellationOfOriginApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPSubjectName/@languageCode'
    rule = msg + '.REQ.021.or_language'
    positive = xml_check(e23, msg, root, 'cv15_op23_positive.xml', [rule])
    changed = deepcopy(root)
    parties = list(changed.iter('{' + ns['ipcdo'] + '}IPPartyDetails'))
    ap = next(p for p in parties if p.find('{' + ns['ipsdo'] + '}IPPartyKindCode').text == 'AP')
    name = next(n for n in ap.findall('{' + ns['ipsdo'] + '}IPSubjectName')
                if n.get('nameRepresentationKindCode') == 'OR')
    assert 'languageCode' in name.attrib
    del name.attrib['languageCode']
    negative = xml_check(e23, msg, changed, 'cv15_op23_missing_language.xml', [rule])
    assert positive['valid'] and positive['rule_results'][rule] == 'PASS'
    assert not negative['valid'] and negative['rule_results'][rule] == 'FAIL'
    state = field(app, 'P.SP.03', 'P.SP.03.TRN.001', msg, [path])
    assert rule not in state[path]['get_form']['message_policy_req_ids']
    case15 = {'process': 'P.SP.03', 'transaction': 'P.SP.03.TRN.001', 'message': msg,
              'requirements': [rule], 'result': 'PASS', 'field': state,
              'positive': positive, 'negative': negative}
    (OUT / 'continuation_case04_case15.json').write_text(json.dumps({'04': case4, '15': case15}, ensure_ascii=False, indent=2, default=str))
    print('CV04 SOURCE_BLOCKED: 5 actual XML scenarios; CV15 PASS: real OP23 AP/OR positive/negative XML')


if __name__ == '__main__':
    source_audit()
    extra_cases()
