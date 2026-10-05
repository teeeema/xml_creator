from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = 'P.SP.02.MSG.028'
STRUCTURE = 'R.IP.SP.02.002'
APP = 'ipcdo:TrademarkApplicationDetails'
PARTY = f'{APP}/ipcdo:IPPartyDetails'
ADDRESS = f'{PARTY}/ccdo:SubjectAddressDetails'
COMM = f'{PARTY}/ccdo:CommunicationDetails'
GOODS = f'{APP}/ipcdo:GoodsBaseDetails'
PRIORITY = f'{APP}/ipcdo:TrademarkPriorityDetails'
DOCS = f'{APP}/ipcdo:AccompanyingDocumentsDetails'
SIG = f'{APP}/ipcdo:SignatureDetails'
RESOURCE = 'ccdo:ResourceItemStatusDetails'
FALLBACK = 'Заявка на регистрацию товарного знака, знака обслуживания Евразийского экономического союза'


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


def _parsed_values(builder):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding='utf-8'))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    return engine, structure, values, issues


def _rules(engine, code):
    rid = f'{MESSAGE}.T44.REQ.{code}'
    return [rule for rule in engine.rules[MESSAGE].structured_rules if rule['rule_id'] == rid or rule['rule_id'].startswith(rid + '.')]


def _assert_status(rules, values, expected):
    evaluator = StructuredRuleEvaluator()
    statuses = [evaluator.evaluate(rule, values).status for rule in rules]
    assert statuses
    if expected is RuleStatus.PASS:
        assert all(status is RuleStatus.PASS for status in statuses), statuses
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


def _communication(parent, structure, *, complete=True, code='EM'):
    node = _child(parent, structure, 'ccdo', 'CommunicationDetails')
    _child(node, structure, 'csdo', 'CommunicationChannelCode', code)
    if complete:
        _child(node, structure, 'csdo', 'CommunicationChannelId', 'user@example.test')
    return node


def _party(app, structure, role, *, omit=None, country_list='ВОИС ST.3'):
    party = _child(app, structure, 'ipcdo', 'IPPartyDetails')
    _child(party, structure, 'ipsdo', 'IPPartyKindCode', role)
    if omit != 'country':
        _child(party, structure, 'csdo', 'UnifiedCountryCode', 'RU', attrs={'codeListId': country_list})
    if omit != 'name':
        _child(party, structure, 'ipsdo', 'IPSubjectName', f'Party {role}')
    if omit != 'address':
        _address(party, structure)
    if omit != 'communication':
        _communication(party, structure)
    if role == 'PA' and omit != 'attorney':
        _child(party, structure, 'ipsdo', 'PatentAttorneyId', 'PA-1')
    return party


def _goods(app, structure, *, complete=True, forbidden=None, suffix='0'):
    node = _child(app, structure, 'ipcdo', 'GoodsBaseDetails')
    if complete:
        _child(node, structure, 'ipsdo', 'GoodsClassCode', '01')
    _child(node, structure, 'ipsdo', 'GoodsClassName', f'Class {suffix}')
    _child(node, structure, 'ipsdo', 'GoodsName', f'Goods {suffix}')
    if forbidden:
        _child(node, structure, 'ipsdo', forbidden, 'X')
    return node


def _priority(app, structure, *, complete=True, forbidden=None, suffix='0'):
    node = _child(app, structure, 'ipcdo', 'TrademarkPriorityDetails')
    if complete:
        _child(node, structure, 'ipsdo', 'PriorityKindCode', '010')
    _child(node, structure, 'ipsdo', 'PriorityKindName', f'Priority {suffix}')
    _child(node, structure, 'ipsdo', 'PriorityDate', '2026-09-24')
    _child(node, structure, 'csdo', 'UnifiedCountryCode', 'RU', attrs={'codeListId': 'ВОИС ST.3'})
    if forbidden:
        _child(node, structure, 'ipsdo', forbidden, 'X')
    return node


def _document(app, structure, *, complete=True, suffix='0'):
    node = _child(app, structure, 'ipcdo', 'AccompanyingDocumentsDetails')
    _child(node, structure, 'ipsdo', 'IPDocKindCode', '12345')
    _child(node, structure, 'ipsdo', 'IPDocKindName', f'Doc kind {suffix}')
    if complete:
        _child(node, structure, 'csdo', 'DocId', f'DOC-{suffix}')
    _child(node, structure, 'csdo', 'DocCreationDate', '2026-09-24')
    _child(node, structure, 'csdo', 'DescriptionText', 'Description')
    _child(node, structure, 'csdo', 'PageQuantity', '1')
    return node


def _signature_direct(app, structure, *, with_officer=False):
    sig = _child(app, structure, 'ipcdo', 'SignatureDetails')
    _child(sig, structure, 'csdo', 'DocCreationDate', '2026-09-24')
    name = _child(sig, structure, 'ccdo', 'FullNameDetails')
    _child(name, structure, 'csdo', 'FirstName', 'Иван')
    _child(name, structure, 'csdo', 'LastName', 'Иванов')
    if with_officer:
        _officer(sig, structure)
    return sig


def _officer(sig, structure, *, complete=True, with_comm=False):
    officer = _child(sig, structure, 'ipcdo', 'OfficerDetails')
    name = _child(officer, structure, 'ccdo', 'FullNameDetails')
    _child(name, structure, 'csdo', 'LastName', 'Петров')
    _child(name, structure, 'csdo', 'FirstName', 'Петр')
    if complete:
        _child(officer, structure, 'csdo', 'PositionName', 'Специалист')
    if with_comm:
        _communication(officer, structure)
    return officer


def _signature_officer(app, structure, *, complete=True, with_comm=False):
    sig = _child(app, structure, 'ipcdo', 'SignatureDetails')
    _child(sig, structure, 'csdo', 'DocCreationDate', '2026-09-24')
    _officer(sig, structure, complete=complete, with_comm=with_comm)
    return sig


@pytest.mark.parametrize(('count', 'expected'), [(0, RuleStatus.FAIL), (1, RuleStatus.PASS), (2, RuleStatus.FAIL)])
def test_req1_application_cardinality_raw_xml(count, expected):
    engine, _, values, _ = _parsed_values(
        lambda root, structure: [_child(root, structure, 'ipcdo', 'TrademarkApplicationDetails') for _ in range(count)]
    )
    _assert_status(_rules(engine, 1), values, expected)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req7_country_classifier_alignment_across_repeated_parties(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index, role in enumerate(('AP', 'RE')):
            _party(app, structure, role, country_list='WRONG' if index == bad_index else 'ВОИС ST.3')

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 7), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req8_repeatable_address_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        party = _child(app, structure, 'ipcdo', 'IPPartyDetails')
        for index in range(2):
            _address(party, structure, complete=index != bad_index)

    engine, _, values, _ = _parsed_values(build)
    if bad_index is not None:
        assert values[f'{ADDRESS}/csdo:CityName'][bad_index] is None
    _assert_status(_rules(engine, 8), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req9_repeatable_communication_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        party = _child(app, structure, 'ipcdo', 'IPPartyDetails')
        for index in range(2):
            _communication(party, structure, complete=index != bad_index)

    engine, _, values, _ = _parsed_values(build)
    if bad_index is not None:
        assert values[f'{COMM}/csdo:CommunicationChannelId'][bad_index] is None
    _assert_status(_rules(engine, 9), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize('order', [('AP', 'PA', 'RE'), ('PA', 'AP', 'RE'), ('RE', 'PA', 'AP'), ('RE', 'AP', 'PA')])
def test_req14_15_21_22_party_role_order_is_semantic(order):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for role in order:
            _party(app, structure, role)

    engine, _, values, _ = _parsed_values(build)
    for code in (14, 15, 21, 22):
        _assert_status(_rules(engine, code), values, RuleStatus.PASS)


@pytest.mark.parametrize(('bad_role', 'code', 'omit'), [('AP', 15, 'communication'), ('PA', 21, 'attorney'), ('RE', 22, 'address')])
def test_role_specific_bad_child_only_breaks_its_role_rule(bad_role, code, omit):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for role in ('AP', 'PA', 'RE'):
            _party(app, structure, role, omit=omit if role == bad_role else None)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, code), values, RuleStatus.FAIL)
    for other in ({15, 21, 22} - {code}):
        _assert_status(_rules(engine, other), values, RuleStatus.PASS)


def test_pa_re_correspondence_priority_documents_are_optional_when_absent():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _party(app, structure, 'AP')

    engine, _, values, _ = _parsed_values(build)
    for code in (21, 22, 23, 24, 31, 33):
        _assert_status(_rules(engine, code), values, RuleStatus.PASS)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req23_24_repeatable_correspondence_addresses_keep_ownership(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        corr = _child(app, structure, 'ipcdo', 'CorrespondenceAddressDetails')
        for index in range(2):
            _address(corr, structure, kind='2' if index == bad_index else '3', country='RU')

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 23), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)
    _assert_status(_rules(engine, 24), values, RuleStatus.PASS)


@pytest.mark.parametrize('bad_index', [None, 0, 1, 2])
def test_req29_goods_three_parent_matrix(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(3):
            _goods(app, structure, complete=index != bad_index, suffix=str(index))

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 29), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize(('field', 'bad_index'), [
    ('TrademarkDecisionIndicator', 0), ('TrademarkApplicationId', 1),
    ('ApellationOfOriginEAEUId', 0), ('TrademarkRegRefusalReasonText', 1),
])
def test_req30_goods_forbidden_children_are_per_goods(field, bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(2):
            _goods(app, structure, forbidden=field if index == bad_index else None, suffix=str(index))

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 30), values, RuleStatus.FAIL)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req31_priority_good_bad_order_matrix(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(2):
            _priority(app, structure, complete=index != bad_index, suffix=str(index))

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 31), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req33_documents_good_bad_order_matrix(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(2):
            _document(app, structure, complete=index != bad_index, suffix=str(index))

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 33), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


def test_req27_picture_and_colour_are_distinct_exact_qnames():
    def build(root, structure, *, picture=True, colour=True, wrong_colour=False):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        tm = _child(app, structure, 'ipcdo', 'TrademarkDetails')
        _child(tm, structure, 'ipsdo', 'TrademarkKindCode', '140')
        _child(tm, structure, 'ipsdo', 'TrademarkKindName', 'Изобразительный знак')
        if picture:
            _child(tm, structure, 'ipsdo', 'TrademarkPicture', 'IMAGE')
        if colour:
            _child(tm, structure, 'ipsdo', 'TrademarkColourName', 'Красный', namespace='urn:wrong' if wrong_colour else None)

        return root

    for picture, colour, wrong_colour, expected in (
        (True, True, False, RuleStatus.PASS),
        (True, False, False, RuleStatus.FAIL),
        (False, True, False, RuleStatus.FAIL),
        (True, True, True, RuleStatus.FAIL),
    ):
        engine, _, values, _ = _parsed_values(lambda root, structure: build(root, structure, picture=picture, colour=colour, wrong_colour=wrong_colour))
        _assert_status(_rules(engine, 27), values, expected)


def test_req16_17_20_are_scoped_to_the_same_ap_parent():
    def build(root, structure, *, representation='OR', language='RU', address_kind='2'):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        party = _child(app, structure, 'ipcdo', 'IPPartyDetails')
        _child(party, structure, 'ipsdo', 'IPPartyKindCode', 'AP')
        _child(party, structure, 'ipsdo', 'IPSubjectName', 'Заявитель', attrs={
            'nameRepresentationKindCode': representation,
            **({'languageCode': language} if language is not None else {}),
        })
        _address(party, structure, kind=address_kind)

    for representation, language, address_kind, expected in (
        ('OR', 'RU', '2', RuleStatus.PASS),
        ('ZZ', 'RU', '2', RuleStatus.FAIL),
        ('OR', None, '2', RuleStatus.FAIL),
        ('OR', 'RU', '3', RuleStatus.FAIL),
    ):
        engine, _, values, _ = _parsed_values(lambda root, structure: build(
            root, structure, representation=representation, language=language, address_kind=address_kind
        ))
        statuses = [StructuredRuleEvaluator().evaluate(rule, values).status for code in (16, 17, 20) for rule in _rules(engine, code)]
        if expected is RuleStatus.PASS:
            assert all(status is RuleStatus.PASS for status in statuses)
        else:
            assert RuleStatus.FAIL in statuses


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req39_41_repeated_officer_signatures_matrix(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(2):
            _signature_officer(app, structure, complete=index != bad_index)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 39), values, RuleStatus.PASS)
    _assert_status(_rules(engine, 40), values, RuleStatus.PASS)
    _assert_status(_rules(engine, 41), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


def test_req39_40_signature_direct_name_and_officer_are_mutually_exclusive():
    def direct_only(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_direct(app, structure)

    def officer_only(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_officer(app, structure)

    def both(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_direct(app, structure, with_officer=True)

    for builder, req39, req40 in (
        (direct_only, RuleStatus.PASS, RuleStatus.PASS),
        (officer_only, RuleStatus.PASS, RuleStatus.PASS),
        (both, RuleStatus.FAIL, RuleStatus.FAIL),
    ):
        engine, _, values, _ = _parsed_values(builder)
        _assert_status(_rules(engine, 39), values, req39)
        _assert_status(_rules(engine, 40), values, req40)


def test_req41_officer_communication_is_forbidden_per_officer():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_officer(app, structure)
        _signature_officer(app, structure, with_comm=True)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 41), values, RuleStatus.FAIL)


def test_qname_and_owner_collisions_do_not_satisfy_or_trigger_msg028_targets():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        # Correct status owner exists, while a wrong-namespace lookalike cannot substitute for it.
        status = _child(app, structure, 'ipcdo', 'IPEntityStatusDetails')
        _child(status, structure, 'csdo', 'StatusCode', '01', namespace='urn:wrong')
        # Nested document fields cannot satisfy direct application-level document-kind/id rules.
        docs = _child(app, structure, 'ipcdo', 'AccompanyingDocumentsDetails')
        _child(docs, structure, 'ipsdo', 'IPDocKindCode', '12345')
        _child(docs, structure, 'ipsdo', 'IPDocKindName', FALLBACK)
        _child(docs, structure, 'ipsdo', 'TrademarkApplicationId', 'NESTED')
        # Wrong-namespace country/address-kind cannot satisfy exact QNames.
        authority = _child(app, structure, 'ipcdo', 'PatentAuthorityDetails')
        _child(authority, structure, 'csdo', 'UnifiedCountryCode', 'RU', namespace='urn:wrong')
        corr = _child(app, structure, 'ipcdo', 'CorrespondenceAddressDetails')
        addr = _child(corr, structure, 'ccdo', 'SubjectAddressDetails')
        _child(addr, structure, 'csdo', 'AddressKindCode', '3', namespace='urn:wrong')
        # Wrong-owner/wrong-namespace forbidden lookalikes must not trigger goods/resource rules.
        _child(app, structure, 'ipsdo', 'TrademarkDecisionIndicator', '1', namespace='urn:wrong')
        _child(app, structure, 'csdo', 'EndDateTime', '2026-09-24T12:00:00+03:00', namespace='urn:wrong')
        _child(app, structure, 'csdo', 'UpdateDateTime', '2026-09-24T12:00:00+03:00', namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build)
    for code in (2, 3, 11, 23):
        _assert_status(_rules(engine, code), values, RuleStatus.FAIL)
    # Nested doc kind fields mean the direct code is still absent; exact MSG028 fallback is also absent at APP.
    _assert_status(_rules(engine, 5), values, RuleStatus.FAIL)
    _assert_status(_rules(engine, 30), values, RuleStatus.PASS)
    _assert_status(_rules(engine, 38), values, RuleStatus.PASS)
