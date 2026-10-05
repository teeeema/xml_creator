import json
from pathlib import Path

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
RULE_FILE = PACKAGE / 'message_rules' / 'P.SP.02.MSG.027.yaml'
MESSAGE = 'P.SP.02.MSG.027'
STRUCTURE = 'R.IP.SP.02.002'
APP = 'ipcdo:TrademarkApplicationDetails'
TM = f'{APP}/ipcdo:TrademarkDetails'
FALLBACK = 'Уведомление о признании заявки на регистрацию товарного знака, знака обслуживания Евразийского экономического союза отозванной'
FULL_INHERITED = {16,17,18,19,20,6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 26, 28, 29}
UNMAPPED = ({13, 16, 17, 18, 19, 20, 27}) - {16, 17, 18, 19, 20}
ORIGINAL_PAGES = {
    16: 516, 17: 516, 18: 516, 19: 517, 20: 517,
    6: 514, 7: 514, 8: 514, 9: 514, 10: 514, 11: 514,
    12: 515, 14: 515, 15: 515, 21: 518, 22: 518, 23: 518,
    24: 519, 25: 519, 26: 519, 28: 520, 29: 520,
}
UNMAPPED_PAGES = {13: 515, 16: 516, 17: 516, 18: 516, 19: 517, 20: 517, 27: 520}


def _data():
    return json.loads(RULE_FILE.read_text(encoding='utf-8'))


def _direct(code):
    rid = f'{MESSAGE}.T57.REQ.{code}'
    return [r for r in _data()['structured_rules'] if r['rule_id'] == rid]


def _inherited(item):
    return [
        r for r in _data()['structured_rules']
        if len(r.get('source_refs', [])) == 2
        and r['source_refs'][1].get('table') == '34'
        and r['source_refs'][1].get('item') == str(item)
    ]


def test_exact_structure_root_and_critical_paths():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    assert structure.structure_id == STRUCTURE
    assert f'{{{structure.namespace}}}{structure.root_element}' == '{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails'
    fields = {f.path: f for f in structure.fields}
    for path in (
        APP,
        f'{APP}/ipsdo:IPDocKindCode',
        f'{APP}/ipsdo:IPDocKindName',
        f'{APP}/ipsdo:ApplicationReceiptDate',
        f'{APP}/ipsdo:TrademarkApplicationId',
        f'{APP}/ipcdo:IPEntityStatusDetails/csdo:StatusCode',
        f'{APP}/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode',
        f'{TM}/ipcdo:TMDescriptionDetails',
        f'{TM}/ipsdo:TrademarkKindCode',
        f'{TM}/ipsdo:TrademarkKindName',
        f'{TM}/ipsdo:CollectiveMarkIndicator',
        f'{APP}/ipcdo:GoodsBaseDetails/ipsdo:GoodsClassCode',
        'ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime',
    ):
        assert path in fields
    assert fields[APP].min_occurs == 1 and fields[APP].max_occurs is None


def test_classification_sets_are_exact_and_unmapped_have_no_rules():
    assert _direct(1)
    assert _direct(5)
    assert _direct(30)
    for code in (2, 3, 4):
        rules = _direct(code)
        assert rules and all(r.get('mapping_status') == 'PARTIAL' for r in rules)
    inherited_items = {
        int(r['source_refs'][1]['item'])
        for r in _data()['structured_rules']
        if len(r.get('source_refs', [])) == 2 and r['source_refs'][1].get('table') == '34'
    }
    assert inherited_items == FULL_INHERITED
    assert inherited_items.isdisjoint(UNMAPPED)


def test_req1_exactly_one_application():
    rule, = _direct(1)
    assert rule['kind'] == 'selection_cardinality'
    assert rule['selector'] == {'collection': APP}
    assert (rule['min_occurs'], rule['max_occurs']) == (1, 1)


def test_req2_and_req3_are_exact_safe_partial_document_kind_branches():
    req2, = _direct(2)
    assert req2['kind'] == 'conditional_presence'
    assert req2['scope'] == {'collection': APP}
    assert req2['condition'] == {'field': 'ipsdo:IPDocKindCode', 'operator': 'NE', 'value': None}
    assert req2['target'] == {'field': 'ipsdo:IPDocKindName'}
    assert req2['state'] == 'FORBIDDEN'

    req3, = _direct(3)
    assert req3['kind'] == 'conditional_fixed_value'
    assert req3['scope'] == {'collection': APP}
    assert req3['condition'] == {'field': 'ipsdo:IPDocKindCode', 'operator': 'EQ', 'value': None}
    assert req3['target'] == {'field': 'ipsdo:IPDocKindName'}
    assert req3['value'] == FALLBACK


def test_req4_contains_only_local_identifier_presence_fragment():
    req4, = _direct(4)
    assert req4['kind'] == 'for_each'
    assert req4['selector'] == {'collection': APP}
    assert req4['assertions'] == [
        {'kind': 'presence', 'target': {'field': 'ipsdo:TrademarkApplicationId'}, 'state': 'REQUIRED'}
    ]
    encoded = json.dumps(req4, ensure_ascii=False)
    assert 'StatusCode' not in encoded and 'EndDateTime' not in encoded


def test_req5_requires_status_instance_allowed_value_and_forbids_code_list_id():
    cardinality, body = _direct(5)
    assert cardinality['kind'] == 'selection_cardinality'
    assert cardinality['selector']['collection'] == f'{APP}/ipcdo:IPEntityStatusDetails'
    assert (cardinality['min_occurs'], cardinality['max_occurs']) == (1, 1)
    assert body['kind'] == 'for_each'
    assert body['assertions'] == [
        {'kind': 'comparison', 'left': {'field': 'csdo:StatusCode'}, 'operator': 'IN', 'right_value': ['32', '33']},
        {'kind': 'presence', 'target': {'field': 'csdo:StatusCode/@codeListId'}, 'state': 'FORBIDDEN'},
    ]


def test_inherited_rules_have_dual_table57_table34_provenance():
    current = _data()['business_rules'][5]['source_refs'][0]
    for item in sorted(FULL_INHERITED):
        rules = _inherited(item)
        assert rules, item
        for rule in rules:
            assert rule['mapping_status'] == 'INHERITED'
            assert rule['source_refs'][0] == current
            original = rule['source_refs'][1]
            assert original['source_id'] == f'22OP-RULE-P.SP.02.MSG.001-{item}'
            assert original['table'] == '34'
            assert original['item'] == str(item)
            assert original['page'] == ORIGINAL_PAGES[item]


def test_req7_to_req10_qname_selectors_are_scoped_under_application():
    expected_qname = {
        7: 'csdo:UnifiedCountryCode',
        8: 'ccdo:SubjectAddressDetails',
        9: 'ccdo:CommunicationDetails',
        10: 'ccdo:CommunicationDetails',
    }
    for item, qname in expected_qname.items():
        rule, = _inherited(item)
        assert rule['selector'] == {'qname': qname, 'under': APP}


def test_req14_15_21_22_use_semantic_party_roles_not_positions():
    expected = {14: 'AP', 15: 'AP', 21: 'PA', 22: 'RE'}
    for item, role in expected.items():
        rule, = _inherited(item)
        assert rule['selector']['collection'] == f'{APP}/ipcdo:IPPartyDetails'
        assert rule['selector']['where'] == {'field': 'ipsdo:IPPartyKindCode', 'operator': 'EQ', 'value': role}
    assert _inherited(14)[0]['kind'] == 'selection_cardinality'
    assert (_inherited(14)[0]['min_occurs'], _inherited(14)[0]['max_occurs']) == (1, 1)
    assert _inherited(21)[0]['kind'] == 'for_each'
    assert _inherited(22)[0]['kind'] == 'for_each'


def test_req25_26_28_29_are_exact_structure_owned_rules():
    assert {r['kind'] for r in _inherited(25)} == {'selection_cardinality', 'for_each'}
    assert any(r.get('selector', {}).get('collection') == f'{TM}/ipcdo:TMDescriptionDetails' for r in _inherited(25))
    required = next(r for r in _inherited(25) if r['kind'] == 'for_each')
    assert {a['target']['field'] for a in required['assertions']} == {
        'ipsdo:TrademarkKindCode', 'ipsdo:TrademarkKindName', 'ipsdo:CollectiveMarkIndicator'
    }

    req26 = _inherited(26)
    assert len(req26) == 1
    assert req26[0]['selector'] == {'collection': TM}
    condition = req26[0]['assertions'][0]['condition']
    assert [item['field'] for item in condition['any']] == ['ipsdo:TrademarkKindCode', 'ipsdo:TrademarkKindName']
    assert condition['any'][0]['value'] == ['110', '120', '130', '140', '150', '160', '170', '180']
    assert len(condition['any'][1]['value']) == 8

    req28, = _inherited(28)
    assert req28['selector'] == {'collection': TM}
    assert req28['assertions'][0]['right_value'] == ['1', '0']

    req29 = _inherited(29)
    assert any(r['kind'] == 'selection_cardinality' and r['selector']['collection'] == f'{APP}/ipcdo:GoodsBaseDetails' for r in req29)
    goods = next(r for r in req29 if r['kind'] == 'for_each')
    assert {a['target']['field'] for a in goods['assertions']} == {'ipsdo:GoodsClassCode', 'ipsdo:GoodsClassName', 'ipsdo:GoodsName'}


def test_req30_uses_only_root_resource_validity_end_datetime():
    req30, = _direct(30)
    assert req30['kind'] == 'selection_cardinality'
    assert req30['selector'] == {'collection': 'ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime'}
    assert (req30['min_occurs'], req30['max_occurs']) == (1, 1)


def test_req13_16_20_and_27_have_no_synthetic_evaluations():
    encoded = json.dumps(_data()['structured_rules'], ensure_ascii=False)
    for item in UNMAPPED:
        assert not _inherited(item)
    assert 'nameRepresentationKindCode' in encoded
    assert 'languageCode' in encoded
    assert 'TrademarkPicture' not in encoded
    assert 'TrademarkColourName' not in encoded


def test_unmapped_and_partial_audit_provenance_is_explicit():
    audit = _data()['mapping_audit']
    assert set(audit['partial_remainders']) == {'2', '3', '4'}
    assert all(item['classification'] == 'SAFE_PARTIAL' for item in audit['partial_remainders'].values())
    unmapped = {int(item['requirement_code']): item for item in audit['unmapped_requirements']}
    assert set(unmapped) == UNMAPPED
    assert unmapped[13]['classification'] == 'AMBIGUOUS'
    assert {int(i['requirement_code']) for i in audit['inventory']} >= {16, 17, 18, 19, 20}
    assert unmapped[27]['classification'] == 'SOURCE_CONFLICT'
    for item, entry in unmapped.items():
        current, original = entry['source_refs']
        assert current['source_id'] == '22OP-RULE-P.SP.02.MSG.027-T57-6-29'
        assert current['table'] == '57' and current['item'] == '6-29'
        assert original['source_id'] == f'22OP-RULE-P.SP.02.MSG.001-{item}'
        assert original['table'] == '34' and original['item'] == str(item)
        assert original['page'] == UNMAPPED_PAGES[item]


def test_message_isolation_keeps_msg027_and_msg028_rule_sets_separate():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    rules27 = engine.rules[MESSAGE].structured_rules
    rules28 = engine.rules['P.SP.02.MSG.028'].structured_rules
    assert rules27
    assert rules28
    assert all(r['rule_id'].startswith(MESSAGE + '.') for r in rules27)
    assert all(r['rule_id'].startswith('P.SP.02.MSG.028.') for r in rules28)
    assert {r['rule_id'] for r in rules27}.isdisjoint({r['rule_id'] for r in rules28})
