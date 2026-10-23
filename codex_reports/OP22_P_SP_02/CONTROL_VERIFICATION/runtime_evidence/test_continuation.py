"""Acceptance gates for selected controls; CV01/02 intentionally not re-executed."""
import json
import pytest
from continuation_audit import OUT, extra_cases, load, source_audit


@pytest.fixture(scope='module')
def evidence():
    source_audit()
    for module in ('probe_op22_cases_05_06_11_12_13_15', 'op26_op23_B_runtime_proof',
                   'op49_case09_case10_probe', 'continuation_case03'):
        load(module).main()
    extra_cases()
    return {p.stem: json.loads(p.read_text()) for p in OUT.glob('*.json')}


@pytest.mark.parametrize('case', ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15'])
def test_selected_control(evidence, case):
    if case == '03':
        assert evidence['continuation_case03']['result'] == 'PASS'
    elif case == '04':
        result = evidence['continuation_case04_case15']['04']
        assert result['result'] == 'SOURCE_BLOCKED' and result['dependency_status'] == 'STILL_EXTERNAL'
        assert result['scenarios']['name_branch']['valid']
        assert all(not result['scenarios'][k]['valid'] for k in ('bad_name', 'missing_name', 'both'))
        assert all(not s['extraction_issues'] for s in result['scenarios'].values())
        assert all(v['resolver'] is None for v in result['fields'].values())
    elif case in ('05', '06', '11', '12', '13'):
        result = evidence['op22_cases_05_06_11_12_13_15'][case]
        assert not result['negative']['valid'] and not result['negative']['extraction_issues']
        if case in ('05', '06'):
            assert result['roundtrip_is_valid'] and not result['extraction_issues']
        elif case == '11':
            path = 'ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId'
            assert result['positive']['valid'] and not result['positive']['extraction_issues']
            assert result['positive']['extracted_DocId'][path] == ['DOCUMENT-1', 'DOCUMENT-2']
            assert result['negative']['extracted_DocId'][path] == ['DOCUMENT-1', None]
            assert result['field']['effective_policy'] == 'REQUIRED'
        else:
            assert result['positive']['roundtrip_is_valid']
            assert result['field']['structure_min_occurs'] == 0
            assert result['field']['effective_policy'] == ('REQUIRED' if case == '12' else 'FORBIDDEN')
    elif case in ('07', '08', '14'):
        result = evidence['op26_op23_B_case07_case08_case14_evidence']['case' + str(int(case))]
        assert result['status'] == 'PASS' and result['positive']['is_valid']
        negatives = ['negative_raw_xml'] if case == '07' else (['tampered_xml'] if case == '14' else ['missing_docid', 'missing_authorityname', 'forbidden_consent'])
        assert all(not result[k]['is_valid'] and not result[k]['extraction_issues'] for k in negatives)
    elif case in ('09', '10'):
        result = evidence['op49_case09_case10_evidence']
        assert result['get_form']['executed'] and result['effective_resolver']['executed']
        assert result['effective_resolver']['indicator_static_policy'] is None
        assert all(v['status'] == 'PASS' for v in result['xml_proof']['generated_positive']['validation']['rule_results'].values())
        for name, rule in [('duplicate_true', 'R002'), ('add_forbidden_false', 'R003')]:
            scenario = result['xml_proof'][name]
            assert not scenario['extract_issue_codes']
            assert scenario['validation']['rule_results']['P.DS.01.MSG.001.' + rule]['status'] == 'FAIL'
        if case == '10':
            path = 'ChargedDistributedReport/ds01cdo:ChargedDistributedDutyReportDetails/ds01cdo:ChargedDistributedDutyDetails'
            assert path not in result['effective_resolver']['all_resolved_paths']
    else:
        result = evidence['continuation_case04_case15']['15']
        rule = 'P.SP.03.MSG.001.REQ.021.or_language'
        assert result['positive']['valid'] and result['positive']['rule_results'][rule] == 'PASS'
        assert not result['negative']['valid'] and result['negative']['rule_results'][rule] == 'FAIL'
        assert all(rule not in f['get_form']['message_policy_req_ids'] for f in result['field'].values())
