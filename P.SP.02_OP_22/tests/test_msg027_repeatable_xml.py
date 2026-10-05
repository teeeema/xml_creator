from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = 'P.SP.02.MSG.027'
STRUCTURE = 'R.IP.SP.02.002'
APP = 'ipcdo:TrademarkApplicationDetails'
PARTY = f'{APP}/ipcdo:IPPartyDetails'
ADDRESS = f'{PARTY}/ccdo:SubjectAddressDetails'
COMM = f'{PARTY}/ccdo:CommunicationDetails'
TM = f'{APP}/ipcdo:TrademarkDetails'
GOODS = f'{APP}/ipcdo:GoodsBaseDetails'
STATUS = f'{APP}/ipcdo:IPEntityStatusDetails'
RESOURCE = 'ccdo:ResourceItemStatusDetails'
END = f'{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:EndDateTime'
FALLBACK = 'Уведомление о признании заявки на регистрацию товарного знака, знака обслуживания Евразийского экономического союза отозванной'


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _child(parent, structure, prefix, local, text=None, attrs=None, namespace=None):
    ns = namespace if namespace is not None else structure.imported_namespaces[prefix]
    node = ET.SubElement(parent, ET.QName(ns, local))
    if text is not None:
        node.text = text
    for key, value in (attrs or {}).items():
        node.set(key, value)
    return node


def _parsed_values(builder, *, allow_issues=False):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding='utf-8'))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    if not allow_issues:
        assert not issues, [(i.code, i.field_path, i.message) for i in issues]
    return engine, structure, values, issues


def _direct(engine, code):
    rid = f'{MESSAGE}.T57.REQ.{code}'
    return [r for r in engine.rules[MESSAGE].structured_rules if r['rule_id'] == rid]


def _inherited(engine, item):
    return [
        r for r in engine.rules[MESSAGE].structured_rules
        if len(r.get('source_refs', [])) == 2
        and r['source_refs'][1].get('table') == '34'
        and r['source_refs'][1].get('item') == str(item)
    ]


def _statuses(rules, values):
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(r, values).status for r in rules]


def _assert_status(rules, values, expected):
    statuses = _statuses(rules, values)
    assert statuses
    if expected is RuleStatus.PASS:
        assert all(s is RuleStatus.PASS for s in statuses), statuses
    else:
        assert RuleStatus.FAIL in statuses, statuses


def _address(parent, structure, *, complete=True, kind='2', country='RU', list_id='ВОИС ST.3'):
    node = _child(parent, structure, 'ccdo', 'SubjectAddressDetails')
    _child(node, structure, 'csdo', 'AddressKindCode', kind)
    _child(node, structure, 'csdo', 'UnifiedCountryCode', country, attrs={'codeListId': list_id})
    if complete:
        _child(node, structure, 'csdo', 'CityName', 'Москва')
    _child(node, structure, 'csdo', 'StreetName', 'Тестовая')
    _child(node, structure, 'csdo', 'BuildingNumberId', '1')
    return node


def _communication(parent, structure, *, include_id=True, code='EM'):
    node = _child(parent, structure, 'ccdo', 'CommunicationDetails')
    _child(node, structure, 'csdo', 'CommunicationChannelCode', code)
    if include_id:
        _child(node, structure, 'csdo', 'CommunicationChannelId', 'user@example.test')
    return node


def _party(app, structure, role, *, complete=True, omit=None):
    party = _child(app, structure, 'ipcdo', 'IPPartyDetails')
    _child(party, structure, 'ipsdo', 'IPPartyKindCode', role)
    if complete:
        if omit != 'country':
            _child(party, structure, 'csdo', 'UnifiedCountryCode', 'RU', attrs={'codeListId': 'ВОИС ST.3'})
        if omit != 'name':
            _child(party, structure, 'ipsdo', 'IPSubjectName', f'Party {role}')
        if omit != 'address':
            _address(party, structure)
        if omit != 'communication':
            _communication(party, structure)
        if role == 'PA' and omit != 'attorney':
            _child(party, structure, 'ipsdo', 'PatentAttorneyId', 'PA-1')
    return party


def _goods(app, structure, *, complete=True, suffix='0'):
    goods = _child(app, structure, 'ipcdo', 'GoodsBaseDetails')
    if complete:
        _child(goods, structure, 'ipsdo', 'GoodsClassCode', '01')
    _child(goods, structure, 'ipsdo', 'GoodsClassName', f'Class {suffix}')
    _child(goods, structure, 'ipsdo', 'GoodsName', f'Goods {suffix}')
    return goods


def _trademark(app, structure, *, code='110', name='Словесный знак', indicator='0', complete=True):
    tm = _child(app, structure, 'ipcdo', 'TrademarkDetails')
    if complete:
        desc = _child(tm, structure, 'ipcdo', 'TMDescriptionDetails')
        _child(desc, structure, 'csdo', 'DescriptionText', 'Описание')
        _child(tm, structure, 'ipsdo', 'TrademarkKindCode', code)
        _child(tm, structure, 'ipsdo', 'TrademarkKindName', name)
        _child(tm, structure, 'ipsdo', 'CollectiveMarkIndicator', indicator)
    return tm


@pytest.mark.parametrize(('count', 'expected'), [(0, RuleStatus.FAIL), (1, RuleStatus.PASS), (2, RuleStatus.FAIL)])
def test_req1_exact_application_cardinality_raw_xml(count, expected):
    engine, _, values, _ = _parsed_values(
        lambda root, structure: [_child(root, structure, 'ipcdo', 'TrademarkApplicationDetails') for _ in range(count)],
        allow_issues=True,
    )
    _assert_status(_direct(engine, 1), values, expected)


def test_req2_req3_ignore_nested_document_kind_collisions():
    def direct_code_nested_name(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _child(app, structure, 'ipsdo', 'IPDocKindCode', '12345')
        status = _child(app, structure, 'ipcdo', 'IPEntityStatusDetails')
        _child(status, structure, 'ipsdo', 'IPDocKindName', FALLBACK)

    def fallback_nested_code(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _child(app, structure, 'ipsdo', 'IPDocKindName', FALLBACK)
        status = _child(app, structure, 'ipcdo', 'IPEntityStatusDetails')
        _child(status, structure, 'ipsdo', 'IPDocKindCode', '99999')

    for builder in (direct_code_nested_name, fallback_nested_code):
        engine, _, values, _ = _parsed_values(builder, allow_issues=True)
        _assert_status(_direct(engine, 2), values, RuleStatus.PASS)
        _assert_status(_direct(engine, 3), values, RuleStatus.PASS)


def test_req3_nested_fallback_cannot_satisfy_missing_direct_name():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        status = _child(app, structure, 'ipcdo', 'IPEntityStatusDetails')
        _child(status, structure, 'ipsdo', 'IPDocKindName', FALLBACK)

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_direct(engine, 3), values, RuleStatus.FAIL)


@pytest.mark.parametrize(('code', 'code_list', 'expected'), [('32', None, RuleStatus.PASS), ('33', None, RuleStatus.PASS), ('31', None, RuleStatus.FAIL), ('32', 'STATUS-LIST', RuleStatus.FAIL)])
def test_req5_status_domain_and_forbidden_classifier_attribute(code, code_list, expected):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        status = _child(app, structure, 'ipcdo', 'IPEntityStatusDetails')
        attrs = {'codeListId': code_list} if code_list else None
        _child(status, structure, 'csdo', 'StatusCode', code, attrs=attrs)

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_direct(engine, 5), values, expected)


def test_req6_direct_application_date_cannot_be_satisfied_by_wrong_namespace_lookalike():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _child(app, structure, 'ipsdo', 'ApplicationReceiptDate', '2026-09-24', namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, 6), values, RuleStatus.FAIL)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req7_repeatable_country_classifier_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        party = _child(app, structure, 'ipcdo', 'IPPartyDetails')
        for index in range(2):
            _child(party, structure, 'csdo', 'UnifiedCountryCode', 'RU', attrs={'codeListId': 'WRONG' if index == bad_index else 'ВОИС ST.3'})

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, 7), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req8_repeatable_addresses_preserve_bad_position(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        party = _child(app, structure, 'ipcdo', 'IPPartyDetails')
        for index in range(2):
            _address(party, structure, complete=index != bad_index)

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    if bad_index is not None:
        assert values[f'{ADDRESS}/csdo:CityName'][bad_index] is None
    _assert_status(_inherited(engine, 8), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req9_repeatable_communications_preserve_bad_position(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        party = _child(app, structure, 'ipcdo', 'IPPartyDetails')
        for index in range(2):
            _communication(party, structure, include_id=index != bad_index)

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    if bad_index is not None:
        assert values[f'{COMM}/csdo:CommunicationChannelId'][bad_index] is None
    _assert_status(_inherited(engine, 9), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize(('code', 'expected'), [('TE', RuleStatus.PASS), ('EM', RuleStatus.PASS), ('FX', RuleStatus.PASS), ('PH', RuleStatus.FAIL)])
def test_req10_channel_domain(code, expected):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        party = _child(app, structure, 'ipcdo', 'IPPartyDetails')
        _communication(party, structure, code=code)

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, 10), values, expected)


def test_req11_12_patent_authority_optional_when_absent_and_strict_when_present():
    engine, _, values, _ = _parsed_values(lambda root, structure: _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails'), allow_issues=True)
    _assert_status(_inherited(engine, 11), values, RuleStatus.PASS)
    _assert_status(_inherited(engine, 12), values, RuleStatus.PASS)

    def bad(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        authority = _child(app, structure, 'ipcdo', 'PatentAuthorityDetails')
        _child(authority, structure, 'csdo', 'UnifiedCountryCode', 'RU', attrs={'codeListId': 'ВОИС ST.3'})
        _child(authority, structure, 'csdo', 'AuthorityName', 'Office')
        address = _child(authority, structure, 'ccdo', 'SubjectAddressDetails')
        _child(address, structure, 'csdo', 'AddressKindCode', '3')

    engine, _, values, _ = _parsed_values(bad, allow_issues=True)
    _assert_status(_inherited(engine, 11), values, RuleStatus.PASS)
    _assert_status(_inherited(engine, 12), values, RuleStatus.FAIL)


@pytest.mark.parametrize('order', [('AP', 'PA', 'RE'), ('PA', 'AP', 'RE'), ('RE', 'PA', 'AP'), ('RE', 'AP', 'PA')])
def test_req14_15_21_22_party_roles_are_order_independent(order):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for role in order:
            _party(app, structure, role)

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    for item in (14, 15, 21, 22):
        _assert_status(_inherited(engine, item), values, RuleStatus.PASS)


@pytest.mark.parametrize(('roles', 'expected'), [(('PA', 'RE'), RuleStatus.FAIL), (('AP',), RuleStatus.PASS), (('AP', 'AP'), RuleStatus.FAIL)])
def test_req14_exactly_one_ap(roles, expected):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for role in roles:
            _party(app, structure, role)

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, 14), values, expected)


@pytest.mark.parametrize(('bad_role', 'item', 'omit'), [('AP', 15, 'communication'), ('PA', 21, 'attorney'), ('RE', 22, 'address')])
def test_role_specific_missing_child_fails_only_corresponding_rule(bad_role, item, omit):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for role in ('AP', 'PA', 'RE'):
            _party(app, structure, role, omit=omit if role == bad_role else None)

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, item), values, RuleStatus.FAIL)
    for other in ({15, 21, 22} - {item}):
        _assert_status(_inherited(engine, other), values, RuleStatus.PASS)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req15_repeated_ap_instances_preserve_role_parent_ownership(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(2):
            _party(app, structure, 'AP', omit='communication' if index == bad_index else None)

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, 15), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


def test_pa_re_and_correspondence_are_not_synthetically_required():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _party(app, structure, 'AP')

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    for item in (21, 22, 23, 24):
        _assert_status(_inherited(engine, item), values, RuleStatus.PASS)


@pytest.mark.parametrize(('kind', 'country', 'req23', 'req24'), [('3', 'RU', RuleStatus.PASS, RuleStatus.PASS), ('2', 'RU', RuleStatus.FAIL, RuleStatus.PASS), ('3', 'US', RuleStatus.PASS, RuleStatus.FAIL)])
def test_req23_24_correspondence_scope(kind, country, req23, req24):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        corr = _child(app, structure, 'ipcdo', 'CorrespondenceAddressDetails')
        _address(corr, structure, kind=kind, country=country)

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, 23), values, req23)
    _assert_status(_inherited(engine, 24), values, req24)


@pytest.mark.parametrize(('code', 'name', 'indicator', 'item', 'expected'), [
    ('110', 'Словесный знак', '0', 26, RuleStatus.PASS),
    ('110', 'Цифровой знак', '0', 26, RuleStatus.PASS),
    ('999', 'Недопустимый вид', '0', 26, RuleStatus.FAIL),
    ('130', 'Цифровой знак', '0', 26, RuleStatus.PASS),
    ('110', 'Словесный знак', '2', 28, RuleStatus.FAIL),
])
def test_req26_inclusive_or_and_req28_indicator(code, name, indicator, item, expected):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _trademark(app, structure, code=code, name=name, indicator=indicator)

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, item), values, expected)


def test_req25_requires_trademark_description_code_name_and_indicator():
    engine, _, values, _ = _parsed_values(lambda root, structure: _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails'), allow_issues=True)
    _assert_status(_inherited(engine, 25), values, RuleStatus.FAIL)

    def good(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _trademark(app, structure)

    engine, _, values, _ = _parsed_values(good, allow_issues=True)
    _assert_status(_inherited(engine, 25), values, RuleStatus.PASS)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req29_goods_good_good_and_bad_in_both_orders(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(2):
            _goods(app, structure, complete=index != bad_index, suffix=str(index))

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, 29), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize('bad_index', [0, 2])
def test_req29_goods_three_instances_reject_bad_at_front_or_back(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(3):
            _goods(app, structure, complete=index != bad_index, suffix=str(index))

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, 29), values, RuleStatus.FAIL)


def test_req29_goods_wrong_namespace_lookalike_cannot_fill_missing_child():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        goods = _child(app, structure, 'ipcdo', 'GoodsBaseDetails')
        _child(goods, structure, 'ipsdo', 'GoodsClassCode', '01', namespace='urn:wrong')
        _child(goods, structure, 'ipsdo', 'GoodsClassName', 'Class')
        _child(goods, structure, 'ipsdo', 'GoodsName', 'Goods')

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, 29), values, RuleStatus.FAIL)


def test_req30_requires_exact_root_resource_end_datetime_and_ignores_lookalike():
    def good(root, structure):
        validity = _child(_child(root, structure, 'ccdo', 'ResourceItemStatusDetails'), structure, 'ccdo', 'ValidityPeriodDetails')
        _child(validity, structure, 'csdo', 'EndDateTime', '2026-09-24T14:00:00+03:00')

    def wrong_namespace(root, structure):
        validity = _child(_child(root, structure, 'ccdo', 'ResourceItemStatusDetails'), structure, 'ccdo', 'ValidityPeriodDetails')
        _child(validity, structure, 'csdo', 'EndDateTime', '2026-09-24T14:00:00+03:00', namespace='urn:wrong')

    for builder, expected in ((good, RuleStatus.PASS), (wrong_namespace, RuleStatus.FAIL)):
        engine, _, values, _ = _parsed_values(builder, allow_issues=True)
        _assert_status(_direct(engine, 30), values, expected)


def test_status_code_wrong_namespace_lookalike_does_not_satisfy_req5():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        status = _child(app, structure, 'ipcdo', 'IPEntityStatusDetails')
        _child(status, structure, 'csdo', 'StatusCode', '32', namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_direct(engine, 5), values, RuleStatus.FAIL)


def test_unified_country_code_wrong_namespace_lookalike_does_not_satisfy_req11():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        authority = _child(app, structure, 'ipcdo', 'PatentAuthorityDetails')
        _child(authority, structure, 'csdo', 'UnifiedCountryCode', 'RU', namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, 11), values, RuleStatus.FAIL)


def test_address_kind_code_wrong_namespace_lookalike_does_not_satisfy_req23():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        corr = _child(app, structure, 'ipcdo', 'CorrespondenceAddressDetails')
        address = _child(corr, structure, 'ccdo', 'SubjectAddressDetails')
        _child(address, structure, 'csdo', 'AddressKindCode', '3', namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build, allow_issues=True)
    _assert_status(_inherited(engine, 23), values, RuleStatus.FAIL)
