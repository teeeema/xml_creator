"""Focused, reproducible CASE 7, 8 and 14 runtime XML evidence.

Run from repo root: PYTHONPATH=eaeu_xml/src python3.13 \
 codex_reports/OP22_P_SP_02/CONTROL_VERIFICATION/runtime_evidence/op26_op23_B_runtime_proof.py
No project source files are modified; outputs stay beside this script.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
from xml.etree import ElementTree as ET

from pypdf import PdfReader

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.process_packages.body import GenerationMode


ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
APP = EaeuXmlApplication(ROOT)


def fixture(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def check_pdf(name: str, expected_hash: str, snippets: dict[int, tuple[str, ...]]):
    path = Path('/Users/tema/Documents/Work/Документы_xml') / name
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == expected_hash, f'Original normative PDF changed: {path}'
    reader = PdfReader(str(path))
    pages = {}
    for page_number, terms in snippets.items():
        text = reader.pages[page_number - 1].extract_text() or ''
        assert all(term in text for term in terms), (name, page_number, terms)
        pages[str(page_number)] = list(terms)
    return {'document': str(path), 'sha256': digest, 'verified_pdf_pages': pages}


def field_state(op: str, trn: str, msg: str, paths: dict[str, str]):
    form = APP.get_form(op, trn, msg)
    resolved = APP._effective_message_field_policies(APP._engine(op), msg) or {}
    by_path = {field.path: field for field in APP._walk_fields(form.fields)}
    result = {}
    for label, path in paths.items():
        field = by_path[path]
        policy = resolved[path]
        assert field.effective_message_policy == policy.policy
        result[label] = {
            'path': path,
            'structure_min_occurs': field.min_occurs,
            'get_form_effective_policy': field.effective_message_policy,
            'get_form_fixed_value': field.fixed_value,
            'get_form_editable': field.editable,
            'get_form_visibility': field.visibility,
            'get_form_rule_ids': list(field.message_policy_req_ids),
            'resolver': asdict(policy),
        }
    return {'op': op, 'transaction': trn, 'message': msg,
            'structure': form.structure_id, 'generation_status': form.generation_status,
            'fields': result}


def actual_xml(engine, message: str, name: str, document: ET.Element, rules: tuple[str, ...]):
    # Serialize and reparse to prove that validation sees the actual XML bytes.
    path = OUT / f'op26_op23_B_{name}.xml'
    raw = ET.tostring(document, encoding='utf-8', xml_declaration=True)
    path.write_bytes(raw)
    root = ET.parse(path).getroot()
    structure = engine.get_structure(message, mode=GenerationMode.TEST)
    values, extraction_issues = engine.body_provider._values_from_element(structure, root)
    checked = engine.validate_body(message, values, mode=GenerationMode.TEST)
    evaluations = {}
    for rule_id in rules:
        evaluations[rule_id] = [
            {'status': item.status.value, 'message': getattr(item, 'message', None)}
            for item in checked.rule_evaluations if item.rule_id == rule_id
        ]
    return {'xml': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
            'root_qname': root.tag, 'xml_readback': True,
            'extraction_issues': [{'code': e.code, 'path': e.field_path} for e in extraction_issues],
            'extracted_values': len(values), 'is_valid': checked.is_valid,
            'issues': [{'code': e.code, 'severity': e.severity.value,
                        'rule_id': e.rule_id, 'path': e.field_path} for e in checked.issues],
            'evaluations': evaluations}


def has_issue(scenario: dict, rule_id: str):
    return any(issue['severity'] == 'ERROR' and issue['rule_id'] == rule_id
               for issue in scenario['issues'])


def check_positive(scenario: dict, rule_ids: tuple[str, ...]):
    assert scenario['is_valid'] and not scenario['extraction_issues'], scenario
    for rule_id in rule_ids:
        assert scenario['evaluations'][rule_id], rule_id
        assert all(e['status'] == 'PASS' for e in scenario['evaluations'][rule_id]), scenario


def check_negative(scenario: dict, rule_id: str):
    assert not scenario['extraction_issues'], scenario
    assert scenario['is_valid'] is False and has_issue(scenario, rule_id), scenario
    assert any(e['status'] == 'FAIL' for e in scenario['evaluations'][rule_id]), scenario


def main():
    source26 = check_pdf(
        '26_ОП.pdf',
        'a15cc6c946b35145e58304b7e3621ea76241f510e2202bbaf8912b4f8b0715e6',
        {39: ('P.CLS.019', 'классификатор стран'),
         213: ('34', 'codeListId', 'csdo:UnifiedCountryCode')})
    source23 = check_pdf(
        'ОП_23.pdf',
        '438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d',
        {342: ('10', 'csdo:DocId', '14', 'csdo:AuthorityName'),
         350: ('43', 'ipsdo:ConsentToDataProcessingIndicator')})

    op26 = 'P.MM.01'
    trn26 = 'P.MM.01.TRN.001'
    msg26 = 'P.MM.01.MSG.001'
    req26 = 'OP26.P_MM_01.P.MM.01.MSG.001.REQ.034'
    attr_path = 'DrugRegistrationDetails/DrugCountryRegistrationDetails/UnifiedCountryCode/@codeListId'
    form26 = field_state(op26, trn26, msg26, {'classifier_id': attr_path})
    f26 = form26['fields']['classifier_id']
    assert f26['get_form_effective_policy'] == 'FIXED'
    assert f26['get_form_fixed_value'] == 'P.CLS.019'
    assert not f26['get_form_editable'] and req26 in f26['get_form_rule_ids']
    test_module = fixture('op26_case_B_fixture', 'P.MM.01_OP_26/tests/all_transactions_matrix.py')
    engine26 = APP._engine(op26)
    values26 = test_module.test_values(engine26, msg26)
    body26 = engine26.build_body(msg26, values26, mode=GenerationMode.TEST)
    document26 = ET.fromstring(ET.tostring(body26.serialize_xml_element()))
    countries = [el for el in document26.iter() if el.tag.endswith('}UnifiedCountryCode')]
    assert countries and countries[0].get('codeListId') == 'P.CLS.019'
    positive26 = actual_xml(engine26, msg26, 'case07_positive', document26, (req26,))
    check_positive(positive26, (req26,))
    tampered26 = deepcopy(document26)
    next(el for el in tampered26.iter() if el.tag.endswith('}UnifiedCountryCode')).set('codeListId', 'P.CLS.999')
    negative26 = actual_xml(engine26, msg26, 'case14_negative_raw_xml_tamper', tampered26, (req26,))
    check_negative(negative26, req26)

    op23 = 'P.SP.03'
    trn23 = 'P.SP.03.TRN.001'
    msg23 = 'P.SP.03.MSG.001'
    req10, req14, req43 = (f'P.SP.03.MSG.001.REQ.{i:03}' for i in (10, 14, 43))
    form23 = field_state(op23, trn23, msg23, {
        'required_docid': 'ipcdo:ApellationOfOriginApplicationDetails/csdo:DocId',
        'required_authority': 'ipcdo:ApellationOfOriginApplicationDetails/ipcdo:PatentAuthorityDetails/csdo:AuthorityName',
        'forbidden_consent': 'ipcdo:ApellationOfOriginApplicationDetails/ipsdo:ConsentToDataProcessingIndicator',
    })
    assert (form23['fields']['required_docid']['get_form_effective_policy'],
            form23['fields']['required_authority']['get_form_effective_policy'],
            form23['fields']['forbidden_consent']['get_form_effective_policy']) == (
                'REQUIRED', 'REQUIRED', 'FORBIDDEN')
    assert not form23['fields']['forbidden_consent']['get_form_editable']
    fixture23 = fixture('op23_case_B_fixture', 'P.SP.03_OP_23/tests/test_b1_production.py')
    engine23 = APP._engine(op23)
    # The existing fixture starts with GuiController-generated XML and normalizes
    # required branch values. Rebuild it through the real body engine for proof.
    normalized = fixture23._positive_document(msg23)
    structure23 = engine23.get_structure(msg23, mode=GenerationMode.TEST)
    initial_values, extract_issues = engine23.body_provider._values_from_element(structure23, normalized)
    assert not extract_issues
    body23 = engine23.build_body(msg23, initial_values, mode=GenerationMode.TEST)
    document23 = ET.fromstring(ET.tostring(body23.serialize_xml_element()))
    positive23 = actual_xml(engine23, msg23, 'case08_positive', document23, (req10, req14, req43))
    check_positive(positive23, (req10, req14, req43))

    missing_docid = deepcopy(document23)
    application = next(el for el in missing_docid.iter() if el.tag.endswith('}ApellationOfOriginApplicationDetails'))
    docid = next(el for el in application if el.tag.endswith('}DocId'))
    application.remove(docid)
    negative_docid = actual_xml(engine23, msg23, 'case08_negative_missing_docid', missing_docid, (req10,))
    check_negative(negative_docid, req10)

    missing_authority = deepcopy(document23)
    authority = next(el for el in missing_authority.iter() if el.tag.endswith('}PatentAuthorityDetails'))
    name = next(el for el in authority if el.tag.endswith('}AuthorityName'))
    authority.remove(name)
    negative_authority = actual_xml(engine23, msg23, 'case08_negative_missing_authority', missing_authority, (req14,))
    check_negative(negative_authority, req14)

    forbidden_consent = deepcopy(document23)
    app_root = next(el for el in forbidden_consent.iter() if el.tag.endswith('}ApellationOfOriginApplicationDetails'))
    ET.SubElement(app_root, f'{{{structure23.imported_namespaces["ipsdo"]}}}ConsentToDataProcessingIndicator').text = '1'
    negative_consent = actual_xml(engine23, msg23, 'case08_negative_forbidden_consent', forbidden_consent, (req43,))
    check_negative(negative_consent, req43)

    results = {
        'source26': source26, 'source23': source23,
        'case7': {'status': 'PASS', 'form': form26, 'rule_id': req26,
                  'positive': positive26, 'negative_raw_xml': negative26,
                  'observation': 'P.CLS.019 FIXED readonly, negative XML fails REQ034'},
        'case8': {'status': 'PASS', 'form': form23, 'rule_ids': [req10, req14, req43],
                  'positive': positive23, 'missing_docid': negative_docid,
                  'missing_authorityname': negative_authority,
                  'forbidden_consent': negative_consent},
        'case14': {'status': 'PASS', 'form': form26, 'rule_id': req26,
                   'positive': positive26, 'tampered_xml': negative26,
                   'observation': 'Generated XML mutated after serialization; extracted XML fails REQ034'},
        'status': 'PASS',
    }
    file = OUT / 'op26_op23_B_case07_case08_case14_evidence.json'
    file.write_text(json.dumps(results, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')
    print('CASES 7,8,14 PASS; 6 XML files; evidence', file)
    for k in ('case7', 'case8', 'case14'):
        print(k, results[k]['rule_id'] if 'rule_id' in results[k] else results[k]['rule_ids'], results[k]['status'])


if __name__ == '__main__':
    main()
