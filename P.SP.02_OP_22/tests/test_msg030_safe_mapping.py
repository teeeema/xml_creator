import json
from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = 'P.SP.02.MSG.030'
APP = 'ipcdo:TrademarkApplicationDetails'
PARTY = f'{APP}/ipcdo:IPPartyDetails'
TM = f'{APP}/ipcdo:TrademarkDetails'
GOODS = f'{APP}/ipcdo:GoodsBaseDetails'
DOCS = f'{APP}/ipcdo:AccompanyingDocumentsDetails'
SIG = f'{APP}/ipcdo:SignatureDetails'
RESOURCE = 'ccdo:ResourceItemStatusDetails'

FULL = {16,17,18,19,20,26,
    1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25,
    27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
}
PARTIAL = {2, 3, 4}
UNMAPPED = ({13, 16, 17, 18, 19, 20, 26}) - {16, 17, 18, 19, 20, 26}
INHERITED = ({6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29}) | {16, 17, 18, 19, 20, 26}
FALLBACK_NAME = (
    'Доводы и замечания заявителя в связи с уведомлением о результатах экспертизы заявки на товарный '
    'знак, знак обслуживания Евразийского экономического союза в отношении всех или части заявленных товаров'
)


def _raw():
    return json.loads((PACKAGE / 'message_rules' / f'{MESSAGE}.yaml').read_text(encoding='utf-8'))


def _rules(code):
    rid = f'{MESSAGE}.T46.REQ.{code}'
    return [rule for rule in _raw()['structured_rules'] if rule['rule_id'] == rid]


def test_msg030_mapping_classification_is_complete_and_non_approximating():
    data = _raw()
    mapped = {int(rule['rule_id'].split('.REQ.')[1].split('.')[0]) for rule in data['structured_rules']}
    assert mapped == FULL | PARTIAL
    assert not mapped.intersection(UNMAPPED)

    audit = data['mapping_audit']
    assert set(map(int, audit['requirements'])) == FULL | PARTIAL | UNMAPPED
    assert {int(code) for code in audit['partial_remainders']} == PARTIAL
    unmapped = {int(item['requirement_code']): item['classification'] for item in audit['unmapped_requirements']}
    assert set(unmapped) == UNMAPPED
    assert all(unmapped[code] == 'UNMAPPED' for code in UNMAPPED)
    assert audit['source_conflicts'] == []


def test_inherited_req6_29_executable_rules_have_dual_table46_and_table44_provenance():
    data = _raw()
    for rule in data['structured_rules']:
        code = int(rule['rule_id'].split('.REQ.')[1].split('.')[0])
        refs = rule['source_refs']
        if code in INHERITED:
            assert len(refs) == 2
            current, original = refs
            assert current['table'] == '46'
            assert current['page'] == 729
            assert current['item'] == '6-29'
            assert current['source_id'] == '22OP-RULE-P.SP.02.MSG.030-T46-6-29'
            assert original['table'] == '44'
            assert original['item'] == str(code)
            assert original['source_id'].endswith(f'-T44-{code}')
        else:
            assert len(refs) == 1
            assert refs[0]['table'] == '46'


def test_req1_application_cardinality_is_exactly_one():
    rule, = _rules(1)
    assert rule['kind'] == 'selection_cardinality'
    assert rule['selector'] == {'collection': APP}
    assert (rule['min_occurs'], rule['max_occurs']) == (1, 1)


def test_req2_classifier_present_branch_is_safe_partial_without_inventing_classifier_membership():
    rule, = _rules(2)
    assert rule['mapping_status'] == 'PARTIAL'
    assert rule['kind'] == 'conditional_presence'
    assert rule['scope'] == {'collection': APP}
    assert rule['condition'] == {'field': 'ipsdo:IPDocKindCode', 'operator': 'NE', 'value': None}
    assert rule['target'] == {'field': 'ipsdo:IPDocKindName'}
    assert rule['state'] == 'FORBIDDEN'
    remainder = _raw()['mapping_audit']['partial_remainders']['2']
    assert remainder['external_dependency'] == 'classifier of document/material kinds'
    assert 'authoritative classifier-presence predicate' in remainder['unmapped_remainder']


def test_req3_classifier_absent_branch_uses_exact_single_table46_fallback_name():
    rule, = _rules(3)
    assert rule['mapping_status'] == 'PARTIAL'
    assert rule['kind'] == 'conditional_fixed_value'
    assert rule['scope'] == {'collection': APP}
    assert rule['condition'] == {'field': 'ipsdo:IPDocKindCode', 'operator': 'EQ', 'value': None}
    assert rule['target'] == {'field': 'ipsdo:IPDocKindName'}
    assert rule['value'] == FALLBACK_NAME
    remainder = _raw()['mapping_audit']['partial_remainders']['3']
    assert remainder['unmapped_remainder'] == ['authoritative classifier-absence predicate']


def test_req4_is_safe_partial_local_application_id_presence_only():
    rule, = _rules(4)
    assert rule['mapping_status'] == 'PARTIAL'
    assert rule['selector'] == {'collection': APP}
    assert rule['assertions'] == [
        {'kind': 'presence', 'target': {'field': 'ipsdo:TrademarkApplicationId'}, 'state': 'REQUIRED'}
    ]
    remainder = _raw()['mapping_audit']['partial_remainders']['4']
    assert remainder['external_dependency'] == 'national patent office information resource'
    assert 'external StatusCode=02' in remainder['unmapped_remainder']


def test_req5_registration_code_is_required_and_limited_to_02_or_03():
    rule, = _rules(5)
    assert rule['selector'] == {'collection': APP}
    assert rule['assertions'] == [
        {'kind': 'presence', 'target': {'field': 'ipsdo:TrademarkRegistrationCode'}, 'state': 'REQUIRED'},
        {
            'kind': 'comparison',
            'left': {'field': 'ipsdo:TrademarkRegistrationCode'},
            'operator': 'IN',
            'right_value': ['02', '03'],
        },
    ]


def test_req6_12_core_rules_use_exact_application_scopes():
    assert _rules(6)[0]['selector'] == {'collection': APP}
    assert _rules(7)[0]['selector'] == {'qname': 'csdo:UnifiedCountryCode', 'under': APP}
    assert _rules(8)[0]['selector'] == {'qname': 'ccdo:SubjectAddressDetails', 'under': APP}
    assert _rules(9)[0]['selector'] == {'qname': 'ccdo:CommunicationDetails', 'under': APP}
    assert _rules(10)[0]['assertions'][0]['right_value'] == ['TE', 'EM', 'FX']
    authority = f'{APP}/ipcdo:PatentAuthorityDetails'
    assert _rules(11)[0]['selector'] == _rules(12)[0]['selector'] == {'collection': authority}


def test_req14_15_21_22_are_role_filtered_and_order_independent_by_selector():
    expected = {14: 'AP', 15: 'AP', 21: 'PA', 22: 'RE'}
    for code, role in expected.items():
        rule, = _rules(code)
        assert rule['selector']['collection'] == PARTY
        assert rule['selector']['where'] == {'field': 'ipsdo:IPPartyKindCode', 'operator': 'EQ', 'value': role}
    assert _rules(14)[0]['kind'] == 'selection_cardinality'
    assert any(item['target']['field'] == 'ipsdo:PatentAttorneyId' for item in _rules(21)[0]['assertions'])


def test_req23_24_correspondence_rules_are_scoped_only_to_optional_correspondence_address():
    collection = f'{APP}/ipcdo:CorrespondenceAddressDetails/ccdo:SubjectAddressDetails'
    assert _rules(23)[0]['selector'] == _rules(24)[0]['selector'] == {'collection': collection}
    assert _rules(23)[0]['assertions'][0]['value'] == '3'
    assert _rules(24)[0]['assertions'][0]['right_value'] == ['AM', 'BY', 'KZ', 'KG', 'RU']


def test_req25_trademark_presence_and_required_children_match_original_table44():
    rules = _rules(25)
    cardinality = next(rule for rule in rules if rule['kind'] == 'selection_cardinality')
    body = next(rule for rule in rules if rule['kind'] == 'for_each')
    assert cardinality['selector'] == {'collection': TM}
    assert (cardinality['min_occurs'], cardinality['max_occurs']) == (1, None)
    assert {item['target']['field'] for item in body['assertions']} == {
        'ipcdo:TMDescriptionDetails', 'ipsdo:TrademarkKindCode', 'ipsdo:TrademarkKindName', 'ipsdo:CollectiveMarkIndicator'
    }


def test_req26_executes_inclusive_or_with_original_provenance():
    rule, = _rules(26)
    assert 'any' in rule['assertions'][0]['condition']
    assert [ref['table'] for ref in rule['source_refs']] == ['46', '44']


def test_req27_exact_same_trademark_owner_uses_code_or_name_condition_and_requires_both_outputs():
    rule, = _rules(27)
    assert rule['selector'] == {'collection': TM}
    assert len(rule['assertions']) == 2
    assert {item['target']['field'] for item in rule['assertions']} == {
        'ipsdo:TrademarkPicture', 'ipsdo:TrademarkColourName'
    }
    for assertion in rule['assertions']:
        condition = assertion['condition']
        assert len(condition['any']) == 2
        assert {item['field'] for item in condition['any']} == {'ipsdo:TrademarkKindCode', 'ipsdo:TrademarkKindName'}


def test_req28_29_collective_and_goods_rules_have_exact_owner_paths():
    req28, = _rules(28)
    assert req28['selector'] == {'collection': TM}
    assert req28['assertions'][0]['right_value'] == ['1', '0']
    req29 = _rules(29)
    assert any(rule['kind'] == 'selection_cardinality' and rule['selector'] == {'collection': GOODS} for rule in req29)
    body = next(rule for rule in req29 if rule['kind'] == 'for_each')
    assert {item['target']['field'] for item in body['assertions']} == {
        'ipsdo:GoodsClassCode', 'ipsdo:GoodsClassName', 'ipsdo:GoodsName'
    }


def test_req30_31_use_exact_filtered_same_goods_semantics():
    req30, = _rules(30)
    assert req30['kind'] == 'selection_cardinality'
    assert req30['selector'] == {
        'collection': GOODS,
        'where': {'field': 'ipsdo:TrademarkDecisionIndicator', 'operator': 'EQ', 'value': '0'},
    }
    assert (req30['min_occurs'], req30['max_occurs']) == (1, None)

    req31, = _rules(31)
    assert req31['kind'] == 'for_each'
    assert req31['selector'] == req30['selector']
    assert {item['target']['field'] for item in req31['assertions']} == {
        'ipsdo:TrademarkApplicationId', 'ipsdo:TrademarkRegRefusalReasonText'
    }


def test_req32_documents_are_optional_but_every_existing_document_requires_exact_six_children():
    rule, = _rules(32)
    assert rule['selector'] == {'collection': DOCS}
    assert {item['target']['field'] for item in rule['assertions']} == {
        'ipsdo:IPDocKindName', 'csdo:DocId', 'csdo:DocCreationDate',
        'csdo:DescriptionText', 'csdo:PageQuantity', 'csdo:DocBinaryText',
    }


def test_req33_consent_is_direct_application_child_and_binary_01():
    rule, = _rules(33)
    assert rule['selector'] == {'collection': APP}
    assert rule['assertions'] == [
        {'kind': 'presence', 'target': {'field': 'ipsdo:ConsentToDataProcessingIndicator'}, 'state': 'REQUIRED'},
        {
            'kind': 'comparison',
            'left': {'field': 'ipsdo:ConsentToDataProcessingIndicator'},
            'operator': 'IN',
            'right_value': ['1', '0'],
        },
    ]


def test_req34_36_signature_rules_anchor_same_signature_and_exact_officer_owner():
    req34 = _rules(34)
    assert any(rule['kind'] == 'selection_cardinality' and rule['selector'] == {'collection': SIG} for rule in req34)
    mutual = next(rule for rule in req34 if rule['kind'] == 'for_each')
    assert mutual['assertions'][0]['condition']['field'] == 'ipcdo:OfficerDetails'
    assert mutual['assertions'][0]['target']['field'] == 'ccdo:FullNameDetails'

    req35, = _rules(35)
    assert req35['selector'] == {'collection': SIG}
    assert req35['assertions'][0]['condition']['field'] == 'ccdo:FullNameDetails'
    assert req35['assertions'][0]['target']['field'] == 'ipcdo:OfficerDetails'

    req36, = _rules(36)
    assert req36['selector'] == {'qname': 'ipcdo:OfficerDetails', 'under': SIG}
    assert {item['target']['field'] for item in req36['assertions']} == {
        'ccdo:FullNameDetails/csdo:LastName', 'ccdo:FullNameDetails/csdo:FirstName',
        'csdo:PositionName', 'ccdo:CommunicationDetails',
    }


def test_req37_40_argument_refusal_and_validity_paths_are_exact():
    req37, = _rules(37)
    assert req37['selector'] == {'collection': f'{APP}/ipcdo:ArgumentDetails'}
    assert (req37['min_occurs'], req37['max_occurs']) == (1, None)

    req38, = _rules(38)
    assert req38['selector'] == {'collection': 'ipcdo:RefusalDetails'}
    assert (req38['min_occurs'], req38['max_occurs']) == (0, 0)

    req39, = _rules(39)
    assert req39['selector'] == {'collection': RESOURCE}
    assert req39['assertions'][0]['target']['field'] == 'ccdo:ValidityPeriodDetails/csdo:StartDateTime'

    req40, = _rules(40)
    assert req40['selector'] == {'collection': RESOURCE}
    assert req40['assertions'][0] == {
        'kind': 'presence',
        'target': {'field': 'ccdo:ValidityPeriodDetails/csdo:EndDateTime'},
        'state': 'FORBIDDEN',
    }


def test_message_rule_identity_is_isolated_across_msg027_028_029_030():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    codes = ('P.SP.02.MSG.027', 'P.SP.02.MSG.028', 'P.SP.02.MSG.029', 'P.SP.02.MSG.030')
    by_message = {
        code: {rule['rule_id'] for rule in engine.rules[code].structured_rules}
        for code in codes
    }
    assert by_message[MESSAGE]
    for code, rule_ids in by_message.items():
        assert all(rule_id.startswith(code + '.') for rule_id in rule_ids)
    for i, left in enumerate(codes):
        for right in codes[i + 1:]:
            assert by_message[left].isdisjoint(by_message[right])
