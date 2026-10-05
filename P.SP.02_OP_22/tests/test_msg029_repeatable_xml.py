from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = 'P.SP.02.MSG.029'
STRUCTURE = 'R.IP.SP.02.002'
APP = 'ipcdo:TrademarkApplicationDetails'
PARTY = f'{APP}/ipcdo:IPPartyDetails'
ADDRESS = f'{PARTY}/ccdo:SubjectAddressDetails'
COMM = f'{PARTY}/ccdo:CommunicationDetails'
GOODS = f'{APP}/ipcdo:GoodsBaseDetails'
DOCS = f'{APP}/ipcdo:AccompanyingDocumentsDetails'
TM = f'{APP}/ipcdo:TrademarkDetails'
SIG = f'{APP}/ipcdo:SignatureDetails'
OFFICER = f'{SIG}/ipcdo:OfficerDetails'


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
    rid = f'{MESSAGE}.T45.REQ.{code}'
    return [rule for rule in engine.rules[MESSAGE].structured_rules if rule['rule_id'] == rid]


def _assert_status(rules, values, expected):
    statuses = [StructuredRuleEvaluator().evaluate(rule, values).status for rule in rules]
    assert statuses
    if expected is RuleStatus.PASS:
        assert all(status is RuleStatus.PASS for status in statuses), statuses
    else:
        assert RuleStatus.FAIL in statuses, statuses


def _address(parent, structure, *, complete=True, kind='2', country='RU'):
    node = _child(parent, structure, 'ccdo', 'SubjectAddressDetails')
    _child(node, structure, 'csdo', 'AddressKindCode', kind)
    _child(node, structure, 'csdo', 'UnifiedCountryCode', country, attrs={'codeListId': 'ВОИС ST.3'})
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


def _party(app, structure, role, *, omit=None):
    party = _child(app, structure, 'ipcdo', 'IPPartyDetails')
    _child(party, structure, 'ipsdo', 'IPPartyKindCode', role)
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
    node = _child(app, structure, 'ipcdo', 'GoodsBaseDetails')
    if complete:
        _child(node, structure, 'ipsdo', 'GoodsClassCode', '01')
    _child(node, structure, 'ipsdo', 'GoodsClassName', f'Class {suffix}')
    _child(node, structure, 'ipsdo', 'GoodsName', f'Goods {suffix}')
    return node


def _document(app, structure, *, kind='code', complete=True, suffix='0'):
    node = _child(app, structure, 'ipcdo', 'AccompanyingDocumentsDetails')
    if kind in {'code', 'both'}:
        _child(node, structure, 'ipsdo', 'IPDocKindCode', f'C-{suffix}')
    if kind in {'name', 'both'}:
        _child(node, structure, 'ipsdo', 'IPDocKindName', f'Document kind {suffix}')
    _child(node, structure, 'csdo', 'DocName', f'Document {suffix}')
    if complete:
        _child(node, structure, 'csdo', 'DocId', f'DOC-{suffix}')
    _child(node, structure, 'csdo', 'DocCreationDate', '2026-09-24')
    _child(node, structure, 'csdo', 'DocValidityDate', '2027-09-24')
    _child(node, structure, 'csdo', 'DescriptionText', 'Description')
    _child(node, structure, 'csdo', 'PageQuantity', '1')
    return node


def _signature_direct(app, structure, *, with_officer=False):
    sig = _child(app, structure, 'ipcdo', 'SignatureDetails')
    _child(sig, structure, 'csdo', 'DocCreationDate', '2026-09-24')
    full = _child(sig, structure, 'ccdo', 'FullNameDetails')
    _child(full, structure, 'csdo', 'FirstName', 'Иван')
    _child(full, structure, 'csdo', 'LastName', 'Иванов')
    if with_officer:
        _officer(sig, structure)
    return sig


def _officer(sig, structure, *, missing=None, with_comm=False, namespace=None):
    officer = _child(sig, structure, 'ipcdo', 'OfficerDetails', namespace=namespace)
    full = _child(officer, structure, 'ccdo', 'FullNameDetails')
    if missing != 'LastName':
        _child(full, structure, 'csdo', 'LastName', 'Петров')
    if missing != 'FirstName':
        _child(full, structure, 'csdo', 'FirstName', 'Петр')
    if missing != 'PositionName':
        _child(officer, structure, 'csdo', 'PositionName', 'Специалист')
    if with_comm:
        _communication(officer, structure)
    return officer


def _signature_officer(app, structure, *, missing=None, with_comm=False, namespace=None):
    sig = _child(app, structure, 'ipcdo', 'SignatureDetails')
    _child(sig, structure, 'csdo', 'DocCreationDate', '2026-09-24')
    _officer(sig, structure, missing=missing, with_comm=with_comm, namespace=namespace)
    return sig


@pytest.mark.parametrize('order', [
    ('AP', 'PA', 'RE'),
    ('PA', 'AP', 'RE'),
    ('RE', 'PA', 'AP'),
    ('RE', 'AP', 'PA'),
])
def test_party_role_order_is_semantic_in_production_xml(order):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for role in order:
            _party(app, structure, role)

    engine, _, values, _ = _parsed_values(build)
    for code in (14, 15, 21, 22):
        _assert_status(_rules(engine, code), values, RuleStatus.PASS)


@pytest.mark.parametrize(('bad_role', 'code', 'omit'), [
    ('AP', 15, 'communication'),
    ('PA', 21, 'attorney'),
    ('RE', 22, 'address'),
])
def test_role_specific_missing_child_does_not_leak_across_other_party_parents(bad_role, code, omit):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for role in ('AP', 'PA', 'RE'):
            _party(app, structure, role, omit=omit if role == bad_role else None)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, code), values, RuleStatus.FAIL)
    for other in ({15, 21, 22} - {code}):
        _assert_status(_rules(engine, other), values, RuleStatus.PASS)


def test_optional_pa_re_correspondence_and_documents_do_not_create_synthetic_existence_requirements():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _party(app, structure, 'AP')

    engine, _, values, _ = _parsed_values(build)
    for code in (21, 22, 23, 24, 33):
        _assert_status(_rules(engine, code), values, RuleStatus.PASS)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req29_goods_good_bad_order_preserves_parent_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(2):
            _goods(app, structure, complete=index != bad_index, suffix=str(index))

    engine, _, values, _ = _parsed_values(build)
    if bad_index is not None:
        assert values[f'{GOODS}/ipsdo:GoodsClassCode'][bad_index] is None
    _assert_status(_rules(engine, 29), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize(('kinds', 'expected'), [
    (('code', 'code'), RuleStatus.PASS),
    (('name', 'name'), RuleStatus.PASS),
    (('code', 'name'), RuleStatus.PASS),
    (('name', 'code'), RuleStatus.PASS),
    (('none', 'code'), RuleStatus.FAIL),
    (('code', 'none'), RuleStatus.FAIL),
])
def test_req33_per_document_code_or_name_matrix_uses_same_parent(kinds, expected):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index, kind in enumerate(kinds):
            _document(app, structure, kind=kind, suffix=str(index))

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 33), values, expected)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req33_common_document_child_missing_first_or_last_fails_only_by_ownership(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(2):
            _document(app, structure, kind='code', complete=index != bad_index, suffix=str(index))

    engine, _, values, _ = _parsed_values(build)
    if bad_index is not None:
        assert values[f'{DOCS}/csdo:DocId'][bad_index] is None
    _assert_status(_rules(engine, 33), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


def test_req27_code_or_name_each_independently_triggers_picture_and_colour_in_same_trademark_parent():
    scenarios = (
        ('code', True, True, RuleStatus.PASS),
        ('name', True, True, RuleStatus.PASS),
        ('code', True, False, RuleStatus.FAIL),
        ('name', False, True, RuleStatus.FAIL),
    )

    for trigger, picture, colour, expected in scenarios:
        def build(root, structure, trigger=trigger, picture=picture, colour=colour):
            app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
            tm = _child(app, structure, 'ipcdo', 'TrademarkDetails')
            if trigger == 'code':
                _child(tm, structure, 'ipsdo', 'TrademarkKindCode', '140')
                _child(tm, structure, 'ipsdo', 'TrademarkKindName', 'Unrelated name')
            else:
                _child(tm, structure, 'ipsdo', 'TrademarkKindCode', '110')
                _child(tm, structure, 'ipsdo', 'TrademarkKindName', 'Изобразительный знак')
            if picture:
                _child(tm, structure, 'ipsdo', 'TrademarkPicture', 'IMAGE')
            if colour:
                _child(tm, structure, 'ipsdo', 'TrademarkColourName', 'Красный')

        engine, _, values, _ = _parsed_values(build)
        _assert_status(_rules(engine, 27), values, expected)


def test_req27_wrong_namespace_colour_cannot_satisfy_exact_qname():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        tm = _child(app, structure, 'ipcdo', 'TrademarkDetails')
        _child(tm, structure, 'ipsdo', 'TrademarkKindCode', '140')
        _child(tm, structure, 'ipsdo', 'TrademarkPicture', 'IMAGE')
        _child(tm, structure, 'ipsdo', 'TrademarkColourName', 'Красный', namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 27), values, RuleStatus.FAIL)


@pytest.mark.parametrize('shape', ['officer', 'direct'])
def test_req37_39_single_signature_branch_variants_pass(shape):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        if shape == 'officer':
            _signature_officer(app, structure)
        else:
            _signature_direct(app, structure)

    engine, _, values, _ = _parsed_values(build)
    for code in (37, 38, 39):
        _assert_status(_rules(engine, code), values, RuleStatus.PASS)


@pytest.mark.parametrize('order', [('direct', 'officer'), ('officer', 'direct')])
def test_req37_39_two_signatures_preserve_same_parent_mutual_exclusion(order):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for shape in order:
            if shape == 'direct':
                _signature_direct(app, structure)
            else:
                _signature_officer(app, structure)

    engine, _, values, _ = _parsed_values(build)
    for code in (37, 38, 39):
        _assert_status(_rules(engine, code), values, RuleStatus.PASS)


def test_req37_38_both_branches_in_same_signature_fail_without_cross_parent_escape():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_direct(app, structure, with_officer=True)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 37), values, RuleStatus.FAIL)
    _assert_status(_rules(engine, 38), values, RuleStatus.FAIL)


@pytest.mark.parametrize('missing', ['LastName', 'FirstName', 'PositionName'])
def test_req39_missing_each_officer_required_child_fails(missing):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_officer(app, structure, missing=missing)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 39), values, RuleStatus.FAIL)


def test_req39_officer_communication_is_forbidden_per_officer():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_officer(app, structure)
        _signature_officer(app, structure, with_comm=True)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 39), values, RuleStatus.FAIL)


def test_wrong_namespace_officer_is_not_selected_as_ipcdo_officer():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_officer(app, structure, namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build)
    assert OFFICER not in values or values[OFFICER] is None
    _assert_status(_rules(engine, 39), values, RuleStatus.PASS)


def test_wrong_owner_document_kind_cannot_satisfy_direct_application_document_kind_rule():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        doc = _document(app, structure, kind='code')
        _child(doc, structure, 'ipsdo', 'IPDocKindName', 'Nested only')

    engine, _, values, _ = _parsed_values(build)
    assert values.get(f'{APP}/ipsdo:IPDocKindCode') is None
    assert values.get(f'{APP}/ipsdo:IPDocKindName') is None
    _assert_status(_rules(engine, 5), values, RuleStatus.FAIL)
