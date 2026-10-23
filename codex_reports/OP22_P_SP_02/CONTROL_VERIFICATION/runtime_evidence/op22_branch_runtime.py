"""Focused, independent OP22 Code/Name runtime evidence for CV-03 and CV-04."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'eaeu_xml' / 'src'))

from eaeu_xml.application import EaeuXmlApplication  # noqa: E402
from eaeu_xml.process_packages.body import GenerationMode  # noqa: E402

APPLICATION_PATH = 'ipcdo:TrademarkApplicationDetails'
CODE_PATH = APPLICATION_PATH + '/ipsdo:IPDocKindCode'
NAME_PATH = APPLICATION_PATH + '/ipsdo:IPDocKindName'
NORM = Path('/Users/tema/Documents/Work/Документы_xml')


def fixture_module(suffix: str):
    path = ROOT / 'P.SP.02_OP_22' / 'tests' / f'test_msg{suffix}_end_to_end.py'
    spec = importlib.util.spec_from_file_location(f'op22_branch_{suffix}_fixture', path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def field_view(form, path):
    queue = list(form.fields)
    while queue:
        field = queue.pop(0)
        if field.path == path:
            return {
                k: getattr(field, k) for k in (
                    'path', 'required', 'fixed_value', 'editable', 'visibility',
                    'effective_message_policy', 'manual_edit_allowed', 'message_policy_req_ids',
                )
            }
        queue.extend(field.children)
    return None


def run_scenario(engine, structure, msg, values, suffix, name):
    raw_validation = engine.validate_body(msg, values, mode=GenerationMode.TEST)
    serialized = ET.tostring(
        engine.build_body(msg, values, mode=GenerationMode.TEST).serialize_xml_element(),
        encoding='utf-8', xml_declaration=True,
    )
    root = ET.fromstring(serialized)
    ipcdo = structure.imported_namespaces['ipcdo']
    ipsdo = structure.imported_namespaces['ipsdo']
    app = root.find(f'.//{{{ipcdo}}}TrademarkApplicationDetails')
    assert app is not None

    if name == 'wrong_code':
        code = app.find(f'{{{ipsdo}}}IPDocKindCode')
        assert code is not None
        code.text = '99999'
    elif name == 'code_and_name':
        assert app.find(f'{{{ipsdo}}}IPDocKindName') is None
        wrong = ET.Element(ET.QName(ipsdo, 'IPDocKindName'))
        wrong.text = 'НЕДОПУСТИМОЕ НАИМЕНОВАНИЕ'
        index = next(i for i, node in enumerate(app) if node.tag == f'{{{ipsdo}}}IPDocKindCode')
        app.insert(index + 1, wrong)
    elif name == 'missing_code':
        code = app.find(f'{{{ipsdo}}}IPDocKindCode')
        assert code is not None
        app.remove(code)

    actual_xml = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    path = OUT / f'op22_branch_CASE{3 if suffix=="027" else 4}_{name}.xml'
    path.write_bytes(actual_xml)
    extracted, extraction_issues = engine.body_provider._values_from_element(
        structure, ET.fromstring(actual_xml)
    )
    validation = engine.validate_body(msg, extracted, mode=GenerationMode.TEST)
    targeted = tuple(
        item for item in validation.rule_evaluations
        if item.rule_id.endswith(('.REQ.2', '.REQ.3'))
    )
    return {
        'xml_path': str(path),
        'xml_sha256': sha256(actual_xml).hexdigest(),
        'root_qname': root.tag,
        'code': [node.text for node in app.findall(f'{{{ipsdo}}}IPDocKindCode')],
        'name': [node.text for node in app.findall(f'{{{ipsdo}}}IPDocKindName')],
        'direct_values_valid': raw_validation.is_valid,
        'extraction_issues': [str(issue) for issue in extraction_issues],
        'runtime_valid': validation.is_valid,
        'runtime_complete': validation.is_complete,
        'issues': [
            {'code': issue.code, 'rule_id': issue.rule_id, 'path': issue.field_path,
             'message': issue.message}
            for issue in validation.issues
        ],
        'targeted_rules': [
            {'rule_id': item.rule_id, 'status': item.status.value} for item in targeted
        ],
    }


def main():
    app = EaeuXmlApplication(ROOT)
    classifier = json.loads((ROOT / 'P.SP.02_OP_22/normative_classifier_data/P.CLS.027.yaml').read_text())
    proof = {
        'source_sha256': {
            p.name: sha256(p.read_bytes()).hexdigest()
            for p in (NORM / '92 решение.pdf', NORM / '148 решение.pdf', NORM / 'ОП_22.pdf')
        },
        'classifier_entry_count': len(classifier['entries']),
        'cases': {},
    }
    for suffix, trn, code in (('027', '022', '07365'), ('004', '003', '07320')):
        msg = 'P.SP.02.MSG.' + suffix
        form = app.get_form('P.SP.02', 'P.SP.02.TRN.' + trn, msg)
        eng = app._engine('P.SP.02')
        structure = eng.get_structure(msg, mode=GenerationMode.TEST)
        policies = app._effective_message_field_policies(eng, msg) or {}
        fixture = fixture_module(suffix)
        original_values = (fixture._valid_values() if suffix == '027' else fixture._generation_values())
        base = deepcopy(original_values)
        base.pop(NAME_PATH, None)
        base[CODE_PATH] = code
        policy_info = {}
        for p in (CODE_PATH, NAME_PATH):
            policy = policies.get(p)
            policy_info[p] = dict(vars(policy)) if policy else None
        info = {
            'message': msg,
            'transaction': 'P.SP.02.TRN.' + trn,
            'normative_table': 57 if suffix == '027' else 38,
            'normative_requirements': [2, 3],
            'actual_classifier_code': code,
            'classifier_snapshot_entry': next((e for e in classifier['entries'] if e['code'] == code), None),
            'get_form': {p: field_view(form, p) for p in (CODE_PATH, NAME_PATH)},
            'effective_resolver': policy_info,
            'structured_rules': [
                {'rule_id': rule['rule_id'], 'kind': rule['kind'],
                 'mapping_status': rule.get('mapping_status')}
                for rule in eng.rules[msg].structured_rules
                if rule['rule_id'].endswith(('.REQ.2', '.REQ.3'))
            ],
            'scenarios': {},
        }
        for scenario in ('positive', 'wrong_code', 'code_and_name', 'missing_code'):
            info['scenarios'][scenario] = run_scenario(eng, structure, msg, base, suffix, scenario)
        info['scenarios']['legacy_fallback'] = run_scenario(
            eng, structure, msg, original_values, suffix, 'legacy_fallback'
        )
        proof['cases'][f'CV-0{3 if suffix=="027" else 4}'] = info
    target = OUT / 'op22_branch_CASE3_CASE4_baseline.json'
    target.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n')
    for key, value in proof['cases'].items():
        print(key, value['message'], 'code', value['actual_classifier_code'],
              'snapshot', bool(value['classifier_snapshot_entry']))
        for name, scenario in value['scenarios'].items():
            print('  ', name, 'valid', scenario['runtime_valid'],
                  'issues', [(issue['code'], issue['rule_id']) for issue in scenario['issues']])
    print('EVIDENCE', target)


if __name__ == '__main__':
    main()
