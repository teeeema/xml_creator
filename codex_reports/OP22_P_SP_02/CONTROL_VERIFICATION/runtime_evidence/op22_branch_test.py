"""Normative acceptance tests for independent CASE 3/4 verification.

The current implementation is expected to fail some of these assertions;
these tests deliberately expose missing classifier-present enforcement.
"""
from pathlib import Path

import pytest

import op22_branch_runtime as proof
from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.process_packages.body import GenerationMode


@pytest.fixture(scope='module')
def context():
    return EaeuXmlApplication(proof.ROOT)


@pytest.mark.parametrize('suffix,trn,code', [('027', '022', '07365'), ('004', '003', '07320')])
def test_classifier_snapshot_contains_normatively_current_code(suffix, trn, code):
    import json
    snapshot = json.loads((proof.ROOT / 'P.SP.02_OP_22/normative_classifier_data/P.CLS.027.yaml').read_text())
    assert any(row['code'] == code for row in snapshot['entries'])


@pytest.mark.parametrize('suffix,trn,code', [('027', '022', '07365'), ('004', '003', '07320')])
def test_actual_get_form_projects_classifier_present_branch(context, suffix, trn, code):
    msg = 'P.SP.02.MSG.' + suffix
    form = context.get_form('P.SP.02', 'P.SP.02.TRN.' + trn, msg)
    code_field = proof.field_view(form, proof.CODE_PATH)
    name_field = proof.field_view(form, proof.NAME_PATH)
    policies = context._effective_message_field_policies(context._engine('P.SP.02'), msg) or {}
    assert code_field is not None and name_field is not None
    assert code_field['effective_message_policy'] == 'FIXED'
    assert code_field['fixed_value'] == code
    assert not code_field['editable']
    assert name_field['effective_message_policy'] == 'FORBIDDEN'
    assert not name_field['editable']
    assert policies[proof.CODE_PATH].fixed_value == code
    assert policies[proof.NAME_PATH].policy == 'FORBIDDEN'


@pytest.mark.parametrize('suffix,trn,code', [('027', '022', '07365'), ('004', '003', '07320')])
def test_positive_generated_and_reextracted_xml_is_valid(context, suffix, trn, code):
    msg = 'P.SP.02.MSG.' + suffix
    eng = context._engine('P.SP.02')
    structure = eng.get_structure(msg, mode=GenerationMode.TEST)
    fixture = proof.fixture_module(suffix)
    values = fixture._valid_values() if suffix == '027' else fixture._generation_values()
    values.pop(proof.NAME_PATH, None)
    values[proof.CODE_PATH] = code
    result = proof.run_scenario(eng, structure, msg, values, suffix, 'positive')
    assert result['runtime_valid'] and result['runtime_complete'], result['issues']
    assert not result['extraction_issues']
    assert result['code'] == [code] and result['name'] == []


@pytest.mark.parametrize(
    'suffix,case,expected_rule', [
        ('027', 'wrong_code', 'P.SP.02.MSG.027.T57.REQ.2'),
        ('027', 'code_and_name', 'P.SP.02.MSG.027.T57.REQ.2'),
        ('004', 'wrong_code', 'P.SP.02.MSG.004.REQ.2'),
        ('004', 'code_and_name', 'P.SP.02.MSG.004.REQ.2'),
    ],
)
def test_invalid_raw_xml_rejected_by_normative_rule(context, suffix, case, expected_rule):
    msg = 'P.SP.02.MSG.' + suffix
    eng = context._engine('P.SP.02')
    structure = eng.get_structure(msg, mode=GenerationMode.TEST)
    fixture = proof.fixture_module(suffix)
    values = fixture._valid_values() if suffix == '027' else fixture._generation_values()
    values.pop(proof.NAME_PATH, None)
    values[proof.CODE_PATH] = '07365' if suffix == '027' else '07320'
    result = proof.run_scenario(eng, structure, msg, values, suffix, case)
    assert not result['extraction_issues']
    assert not result['runtime_valid']
    assert any(issue['code'] == 'STRUCTURED_RULE_FAILED' and issue['rule_id'] == expected_rule
               for issue in result['issues']), result['issues']
