import json
from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = 'P.SP.02.MSG.028'
APP = 'ipcdo:TrademarkApplicationDetails'
PARTY = f'{APP}/ipcdo:IPPartyDetails'
TM = f'{APP}/ipcdo:TrademarkDetails'
RESOURCE = 'ccdo:ResourceItemStatusDetails'
FALLBACK = 'Заявка на регистрацию товарного знака, знака обслуживания Евразийского экономического союза'
FULL = {1, 2, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 38, 39, 40, 41}
PARTIAL = {3, 4, 5, 37}
UNMAPPED = {13, 18, 19, 32}


def _raw():
    return json.loads((PACKAGE / 'message_rules' / f'{MESSAGE}.yaml').read_text())


def _rules(code):
    rid = f'{MESSAGE}.T44.REQ.{code}'
    return [rule for rule in _raw()['structured_rules'] if rule['rule_id'] == rid]


def test_msg028_audit_classification_and_direct_table44_provenance():
    data = _raw()
    mapped = {int(rule['rule_id'].rsplit('.', 1)[1]) for rule in data['structured_rules']}
    assert mapped == FULL | PARTIAL
    assert not (mapped & UNMAPPED)
    assert len(data['business_rules']) == 41
    assert all(len(rule['source_refs']) == 1 for rule in data['structured_rules'])
    for rule in data['structured_rules']:
        ref = rule['source_refs'][0]
        assert ref['table'] == '44'
        assert ref['location'].startswith('Таблица 44.')
        assert ref['source_id'].startswith('22OP-RULE-P.SP.02.MSG.028-T44-')
        assert 'INHERITED' != rule.get('mapping_status')

    audit = data['mapping_audit']
    assert {int(code) for code in audit['partial_remainders']} == PARTIAL
    assert {int(item['requirement_code']) for item in audit['unmapped_requirements']} == UNMAPPED
    classes = {int(item['requirement_code']): item['classification'] for item in audit['unmapped_requirements']}
    assert classes[13] == 'AMBIGUOUS'
    assert all(classes[code] == 'ENGINE_UNSUPPORTED' for code in (18, 19))
    assert classes[32] == 'EXTERNAL'


def test_table_number_source_conflict_is_preserved_as_metadata():
    conflict = _raw()['mapping_audit']['source_conflicts'][0]
    assert conflict['classification'] == 'SOURCE_CONFLICT_METADATA'
    assert conflict['intro_reference']['section'] == '55'
    assert conflict['intro_reference']['declared_table'] == '46'
    assert conflict['actual_table_reference']['table'] == '44'
    assert conflict['actual_table_reference']['message_code'] == MESSAGE


def test_req1_application_cardinality_is_exactly_one():
    rule, = _rules(1)
    assert rule['kind'] == 'selection_cardinality'
    assert rule['selector'] == {'collection': APP}
    assert (rule['min_occurs'], rule['max_occurs']) == (1, 1)


def test_req2_status_is_exact_application_owned_status_code():
    rule, = _rules(2)
    assert rule['selector'] == {'collection': APP}
    assert rule['assertions'] == [
        {'kind': 'fixed_value', 'target': {'field': 'ipcdo:IPEntityStatusDetails/csdo:StatusCode'}, 'value': '01'},
        {'kind': 'presence', 'target': {'field': 'ipcdo:IPEntityStatusDetails/csdo:StatusCode/@codeListId'}, 'state': 'FORBIDDEN'},
    ]


def test_req3_5_are_partial_and_use_msg028_fallback():
    req3, = _rules(3)
    req4, = _rules(4)
    req5, = _rules(5)
    assert req3['mapping_status'] == req4['mapping_status'] == req5['mapping_status'] == 'PARTIAL'
    assert req3['assertions'][0]['target']['field'] == 'ipsdo:TrademarkApplicationId'
    assert req4['kind'] == 'conditional_presence'
    assert req4['condition'] == {'field': 'ipsdo:IPDocKindCode', 'operator': 'NE', 'value': None}
    assert req4['target']['field'] == 'ipsdo:IPDocKindName'
    assert req5['kind'] == 'conditional_fixed_value'
    assert req5['condition'] == {'field': 'ipsdo:IPDocKindCode', 'operator': 'EQ', 'value': None}
    assert req5['value'] == FALLBACK


def test_req6_12_use_exact_msg028_owners_and_qname_scopes():
    req6, = _rules(6)
    assert req6['selector'] == {'collection': APP}
    req7, = _rules(7)
    assert req7['selector'] == {'qname': 'csdo:UnifiedCountryCode', 'under': APP}
    req8, = _rules(8)
    assert req8['selector'] == {'qname': 'ccdo:SubjectAddressDetails', 'under': APP}
    assert {a['target']['field'] for a in req8['assertions']} == {
        'csdo:AddressKindCode', 'csdo:UnifiedCountryCode', 'csdo:CityName', 'csdo:StreetName', 'csdo:BuildingNumberId'
    }
    req9, = _rules(9)
    assert req9['selector'] == {'qname': 'ccdo:CommunicationDetails', 'under': APP}
    req10, = _rules(10)
    assert req10['assertions'][0]['right_value'] == ['TE', 'EM', 'FX']
    req11, = _rules(11)
    req12, = _rules(12)
    authority = f'{APP}/ipcdo:PatentAuthorityDetails'
    assert req11['selector'] == req12['selector'] == {'collection': authority}
    assert any(a.get('value') == '2' for a in req12['assertions'])


def test_req14_15_21_22_are_role_filtered_and_order_independent_by_design():
    expected = {14: 'AP', 15: 'AP', 21: 'PA', 22: 'RE'}
    for code, role in expected.items():
        rule, = _rules(code)
        assert rule['selector']['collection'] == PARTY
        assert rule['selector']['where'] == {'field': 'ipsdo:IPPartyKindCode', 'operator': 'EQ', 'value': role}
    assert _rules(14)[0]['kind'] == 'selection_cardinality'
    assert any(a['target']['field'] == 'ipsdo:PatentAttorneyId' for a in _rules(21)[0]['assertions'])


def test_req23_24_are_correspondence_branch_only():
    collection = f'{APP}/ipcdo:CorrespondenceAddressDetails/ccdo:SubjectAddressDetails'
    req23, = _rules(23)
    req24, = _rules(24)
    assert req23['selector'] == req24['selector'] == {'collection': collection}
    assert req23['assertions'][0]['value'] == '3'
    assert req24['assertions'][0]['right_value'] == ['AM', 'BY', 'KZ', 'KG', 'RU']


def test_req25_28_trademark_rules_include_exact_pair_and_image_colour_qnames():
    req25 = _rules(25)
    assert {rule['kind'] for rule in req25} == {'selection_cardinality', 'for_each'}
    body = next(rule for rule in req25 if rule['kind'] == 'for_each')
    assert {a['target']['field'] for a in body['assertions']} == {
        'ipcdo:TMDescriptionDetails', 'ipsdo:TrademarkKindCode', 'ipsdo:TrademarkKindName', 'ipsdo:CollectiveMarkIndicator'
    }
    req26, = _rules(26)
    assert req26['kind'] == 'for_each'
    assert req26['assertions'] == [{'kind': 'condition', 'condition': {'any': [
        {'field': 'ipsdo:TrademarkKindCode', 'operator': 'IN', 'value': ['110', '120', '130', '140', '150', '160', '170', '180']},
        {'field': 'ipsdo:TrademarkKindName', 'operator': 'IN', 'value': ['Словесный знак', 'Буквенный знак', 'Цифровой знак', 'Изобразительный знак', 'Объемный знак', 'Знак, представляющий собой цвет', 'Знак, представляющий собой сочетание цветов', 'Комбинированный знак']},
    ]}}]
    req27, = _rules(27)
    targets = {a['target']['field'] for a in req27['assertions']}
    assert targets == {'ipsdo:TrademarkPicture', 'ipsdo:TrademarkColourName'}
    req28, = _rules(28)
    assert req28['assertions'][0]['right_value'] == ['1', '0']


def test_req29_34_goods_priority_documents_and_consent_are_per_parent():
    req29 = _rules(29)
    assert any(r['kind'] == 'selection_cardinality' and r['selector']['collection'] == f'{APP}/ipcdo:GoodsBaseDetails' for r in req29)
    req30, = _rules(30)
    assert req30['selector']['collection'] == f'{APP}/ipcdo:GoodsBaseDetails'
    assert {a['target']['field'] for a in req30['assertions']} == {
        'ipsdo:TrademarkDecisionIndicator', 'ipsdo:TrademarkApplicationId', 'ipsdo:ApellationOfOriginEAEUId', 'ipsdo:TrademarkRegRefusalReasonText'
    }
    req31, = _rules(31)
    assert req31['selector']['collection'] == f'{APP}/ipcdo:TrademarkPriorityDetails'
    assert {a['target']['field'] for a in req31['assertions'] if a['state'] == 'FORBIDDEN'} == {
        'ipsdo:ExhibitionSiteText', 'ipsdo:FirstTrademarkApplicationId'
    }
    req33, = _rules(33)
    assert req33['selector']['collection'] == f'{APP}/ipcdo:AccompanyingDocumentsDetails'
    assert len(req33['assertions']) == 6
    req34, = _rules(34)
    assert req34['selector'] == {'collection': APP}
    assert req34['assertions'] == [{'kind': 'fixed_value', 'target': {'field': 'ipsdo:ConsentToDataProcessingIndicator'}, 'value': '1'}]


def test_req35_38_exact_forbidden_and_resource_paths():
    req35 = _rules(35)
    assert {r['selector']['collection'] for r in req35} == {
        f'{APP}/ipcdo:TrademarkNationalApplicationDetails',
        f'{APP}/ipcdo:ApplicantChangeDetails',
        f'{APP}/ipcdo:TrademarkClaimDetails',
        f'{APP}/ipcdo:ComplaintDetails',
        f'{APP}/ipcdo:ApplicantComplainResponseDetails',
    }
    req36, = _rules(36)
    assert req36['selector']['collection'] == 'ipcdo:RefusalDetails'
    req37, = _rules(37)
    assert req37['mapping_status'] == 'PARTIAL'
    assert req37['selector'] == {'collection': RESOURCE}
    assert req37['assertions'][0]['target']['field'] == 'ccdo:ValidityPeriodDetails/csdo:StartDateTime'
    assert {r['selector']['collection'] for r in _rules(38)} == {
        f'{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:EndDateTime', f'{RESOURCE}/csdo:UpdateDateTime'
    }


def test_req39_41_signature_rules_use_direct_signature_and_officer_scopes():
    req39 = _rules(39)
    assert any(r['kind'] == 'selection_cardinality' and r['selector']['collection'] == f'{APP}/ipcdo:SignatureDetails' and r['min_occurs'] == 1 for r in req39)
    conditional = next(r for r in req39 if r['kind'] == 'for_each')
    assert conditional['assertions'][0]['condition']['field'] == 'ipcdo:OfficerDetails'
    assert conditional['assertions'][0]['target']['field'] == 'ccdo:FullNameDetails'
    req40, = _rules(40)
    assert req40['assertions'][0]['condition']['field'] == 'ccdo:FullNameDetails'
    assert req40['assertions'][0]['target']['field'] == 'ipcdo:OfficerDetails'
    req41, = _rules(41)
    assert req41['selector']['collection'] == f'{APP}/ipcdo:SignatureDetails/ipcdo:OfficerDetails'
    assert {a['target']['field'] for a in req41['assertions']} == {
        'ccdo:FullNameDetails/csdo:LastName', 'ccdo:FullNameDetails/csdo:FirstName', 'csdo:PositionName', 'ccdo:CommunicationDetails'
    }


def test_message_isolation_keeps_msg028_rules_out_of_msg027_and_msg029():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    ids028 = {r['rule_id'] for r in engine.rules[MESSAGE].structured_rules}
    ids027 = {r['rule_id'] for r in engine.rules['P.SP.02.MSG.027'].structured_rules}
    ids029 = {r['rule_id'] for r in engine.rules['P.SP.02.MSG.029'].structured_rules}
    assert ids028 and all(rule_id.startswith(MESSAGE + '.') for rule_id in ids028)
    assert all(rule_id.startswith('P.SP.02.MSG.027.') for rule_id in ids027)
    assert not (ids028 & ids027)
    assert not (ids028 & ids029)
