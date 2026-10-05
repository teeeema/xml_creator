from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = 'P.SP.02.MSG.030'
STRUCTURE = 'R.IP.SP.02.002'
APP = 'ipcdo:TrademarkApplicationDetails'
PARTY = f'{APP}/ipcdo:IPPartyDetails'
GOODS = f'{APP}/ipcdo:GoodsBaseDetails'
DOCS = f'{APP}/ipcdo:AccompanyingDocumentsDetails'
TM = f'{APP}/ipcdo:TrademarkDetails'
SIG = f'{APP}/ipcdo:SignatureDetails'
OFFICER = f'{SIG}/ipcdo:OfficerDetails'
ARGUMENT = f'{APP}/ipcdo:ArgumentDetails'


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
    rid = f'{MESSAGE}.T46.REQ.{code}'
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


def _goods(
    app,
    structure,
    *,
    complete=True,
    suffix='0',
    decision='0',
    with_application_id=True,
    with_reason=True,
    decision_namespace=None,
):
    node = _child(app, structure, 'ipcdo', 'GoodsBaseDetails')
    if complete:
        _child(node, structure, 'ipsdo', 'GoodsClassCode', '01')
    _child(node, structure, 'ipsdo', 'GoodsClassName', f'Class {suffix}')
    _child(node, structure, 'ipsdo', 'GoodsName', f'Goods {suffix}')
    _child(
        node,
        structure,
        'ipsdo',
        'TrademarkDecisionIndicator',
        decision,
        namespace=decision_namespace,
    )
    if with_application_id:
        _child(node, structure, 'ipsdo', 'TrademarkApplicationId', f'APP-{suffix}')
    if with_reason:
        _child(node, structure, 'ipsdo', 'TrademarkRegRefusalReasonText', f'Reason {suffix}')
    return node


DOCUMENT_REQUIRED = (
    ('ipsdo', 'IPDocKindName'),
    ('csdo', 'DocId'),
    ('csdo', 'DocCreationDate'),
    ('csdo', 'DescriptionText'),
    ('csdo', 'PageQuantity'),
    ('csdo', 'DocBinaryText'),
)


def _document(app, structure, *, missing=None, suffix='0', binary_namespace=None):
    node = _child(app, structure, 'ipcdo', 'AccompanyingDocumentsDetails')
    values = {
        'IPDocKindName': f'Document kind {suffix}',
        'DocId': f'DOC-{suffix}',
        'DocCreationDate': '2026-09-24',
        'DescriptionText': f'Description {suffix}',
        'PageQuantity': '1',
        'DocBinaryText': 'QUJD',
    }
    for prefix, local in DOCUMENT_REQUIRED:
        if local == missing:
            continue
        namespace = binary_namespace if local == 'DocBinaryText' else None
        _child(node, structure, prefix, local, values[local], namespace=namespace)
    return node


def _signature_direct(app, structure, *, with_officer=False):
    sig = _child(app, structure, 'ipcdo', 'SignatureDetails')
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
    for code in (21, 22, 23, 24, 32):
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


@pytest.mark.parametrize('bad_index', [0, 1, 2])
def test_req29_three_goods_sparse_missing_child_stays_at_exact_parent_index(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(3):
            _goods(app, structure, complete=index != bad_index, suffix=str(index))

    engine, _, values, _ = _parsed_values(build)
    assert values[f'{GOODS}/ipsdo:GoodsClassCode'][bad_index] is None
    _assert_status(_rules(engine, 29), values, RuleStatus.FAIL)


@pytest.mark.parametrize(('decisions', 'expected'), [
    (('0',), RuleStatus.PASS),
    (('1', '0'), RuleStatus.PASS),
    (('0', '1'), RuleStatus.PASS),
    (('1', '1'), RuleStatus.FAIL),
])
def test_req30_filtered_cardinality_counts_only_decision_zero_goods(decisions, expected):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index, decision in enumerate(decisions):
            _goods(app, structure, suffix=str(index), decision=decision)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 30), values, expected)


def test_req30_wrong_namespace_decision_zero_does_not_satisfy_filtered_cardinality():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _goods(app, structure, suffix='0', decision='0', decision_namespace='urn:wrong')
        _goods(app, structure, suffix='1', decision='1')

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 30), values, RuleStatus.FAIL)


@pytest.mark.parametrize(('missing', 'expected'), [
    (None, RuleStatus.PASS),
    ('application', RuleStatus.FAIL),
    ('reason', RuleStatus.FAIL),
])
def test_req31_decision_zero_requires_both_fields_on_same_goods_parent(missing, expected):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _goods(
            app,
            structure,
            suffix='0',
            decision='0',
            with_application_id=missing != 'application',
            with_reason=missing != 'reason',
        )
        _goods(app, structure, suffix='1', decision='1')

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 31), values, expected)


def test_req31_decision_one_fields_cannot_fill_missing_decision_zero_fields_cross_parent():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _goods(app, structure, suffix='0', decision='0', with_application_id=False, with_reason=False)
        _goods(app, structure, suffix='1', decision='1', with_application_id=True, with_reason=True)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 31), values, RuleStatus.FAIL)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req31_two_decision_zero_goods_preserve_good_bad_parent_order(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(2):
            _goods(
                app,
                structure,
                suffix=str(index),
                decision='0',
                with_reason=index != bad_index,
            )

    engine, _, values, _ = _parsed_values(build)
    if bad_index is not None:
        assert values[f'{GOODS}/ipsdo:TrademarkRegRefusalReasonText'][bad_index] is None
    _assert_status(_rules(engine, 31), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize('missing', [name for _, name in DOCUMENT_REQUIRED])
def test_req32_each_required_document_child_is_owned_by_each_existing_document(missing):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _document(app, structure, suffix='0')
        _document(app, structure, missing=missing, suffix='1')

    engine, _, values, _ = _parsed_values(build)
    assert values[f'{DOCS}/{next(prefix for prefix, local in DOCUMENT_REQUIRED if local == missing)}:{missing}'][1] is None
    _assert_status(_rules(engine, 32), values, RuleStatus.FAIL)


@pytest.mark.parametrize('bad_index', [None, 0, 1])
def test_req32_document_good_bad_order_preserves_parent_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for index in range(2):
            _document(app, structure, missing='DocId' if index == bad_index else None, suffix=str(index))

    engine, _, values, _ = _parsed_values(build)
    if bad_index is not None:
        assert values[f'{DOCS}/csdo:DocId'][bad_index] is None
    _assert_status(_rules(engine, 32), values, RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


def test_req32_two_complete_documents_pass_independently():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _document(app, structure, suffix='0')
        _document(app, structure, suffix='1')

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 32), values, RuleStatus.PASS)


def test_req32_wrong_namespace_binary_text_cannot_satisfy_exact_qname():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _document(app, structure, suffix='0', binary_namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 32), values, RuleStatus.FAIL)


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
def test_req34_36_single_signature_branch_variants_pass(shape):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        if shape == 'officer':
            _signature_officer(app, structure)
        else:
            _signature_direct(app, structure)

    engine, _, values, _ = _parsed_values(build)
    for code in (34, 35, 36):
        _assert_status(_rules(engine, code), values, RuleStatus.PASS)


@pytest.mark.parametrize('order', [('direct', 'officer'), ('officer', 'direct')])
def test_req34_36_two_signatures_preserve_same_parent_mutual_exclusion(order):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        for shape in order:
            if shape == 'direct':
                _signature_direct(app, structure)
            else:
                _signature_officer(app, structure)

    engine, _, values, _ = _parsed_values(build)
    for code in (34, 35, 36):
        _assert_status(_rules(engine, code), values, RuleStatus.PASS)


def test_req34_35_both_branches_in_same_signature_fail_without_cross_parent_escape():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_direct(app, structure, with_officer=True)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 34), values, RuleStatus.FAIL)
    _assert_status(_rules(engine, 35), values, RuleStatus.FAIL)


@pytest.mark.parametrize('missing', ['LastName', 'FirstName', 'PositionName'])
def test_req36_missing_each_officer_required_child_fails(missing):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_officer(app, structure, missing=missing)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 36), values, RuleStatus.FAIL)


def test_req36_officer_communication_is_forbidden_per_officer():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_officer(app, structure)
        _signature_officer(app, structure, with_comm=True)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 36), values, RuleStatus.FAIL)


def test_wrong_namespace_officer_is_not_selected_as_ipcdo_officer():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _signature_officer(app, structure, namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build)
    assert OFFICER not in values or values[OFFICER] is None
    _assert_status(_rules(engine, 36), values, RuleStatus.PASS)


def test_nested_document_kind_name_cannot_satisfy_direct_application_req3():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _document(app, structure, suffix='0')

    engine, _, values, _ = _parsed_values(build)
    assert values.get(f'{APP}/ipsdo:IPDocKindName') is None
    _assert_status(_rules(engine, 3), values, RuleStatus.FAIL)


def test_nested_consent_value_cannot_satisfy_direct_application_req33():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        doc = _document(app, structure, suffix='0')
        _child(doc, structure, 'ipsdo', 'ConsentToDataProcessingIndicator', '1')

    engine, _, values, _ = _parsed_values(build)
    assert values.get(f'{APP}/ipsdo:ConsentToDataProcessingIndicator') is None
    _assert_status(_rules(engine, 33), values, RuleStatus.FAIL)


@pytest.mark.parametrize(('local', 'code'), [
    ('TrademarkApplicationId', 4),
    ('TrademarkRegistrationCode', 5),
    ('ConsentToDataProcessingIndicator', 33),
])
def test_wrong_namespace_direct_application_fields_do_not_satisfy_exact_qname(local, code):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _child(app, structure, 'ipsdo', local, '02' if local == 'TrademarkRegistrationCode' else '1', namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, code), values, RuleStatus.FAIL)


def test_wrong_namespace_direct_document_code_does_not_switch_req2_req3_branch():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _child(app, structure, 'ipsdo', 'IPDocKindCode', 'DOC-CODE', namespace='urn:wrong')
        _child(
            app,
            structure,
            'ipsdo',
            'IPDocKindName',
            (
                'Доводы и замечания заявителя в связи с уведомлением о результатах экспертизы заявки на товарный '
                'знак, знак обслуживания Евразийского экономического союза в отношении всех или части заявленных товаров'
            ),
        )

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 2), values, RuleStatus.PASS)
    _assert_status(_rules(engine, 3), values, RuleStatus.PASS)


@pytest.mark.parametrize('local', ['GoodsClassCode', 'GoodsClassName', 'GoodsName'])
def test_wrong_namespace_goods_required_child_does_not_satisfy_req29(local):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        goods = _goods(app, structure, suffix='0')
        correct = _child(goods, structure, 'ipsdo', local, 'WRONG-NS', namespace='urn:wrong')
        existing = [
            node for node in list(goods)
            if node is not correct and node.tag == f'{{{structure.imported_namespaces["ipsdo"]}}}{local}'
        ]
        for node in existing:
            goods.remove(node)

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 29), values, RuleStatus.FAIL)


@pytest.mark.parametrize('local', ['TrademarkApplicationId', 'TrademarkRegRefusalReasonText'])
def test_wrong_namespace_decision_zero_goods_field_does_not_satisfy_req31(local):
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        goods = _goods(app, structure, suffix='0', decision='0')
        qname = f'{{{structure.imported_namespaces["ipsdo"]}}}{local}'
        for node in list(goods):
            if node.tag == qname:
                goods.remove(node)
        _child(goods, structure, 'ipsdo', local, 'WRONG-NS', namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 31), values, RuleStatus.FAIL)


def test_wrong_namespace_signature_and_argument_do_not_satisfy_required_qnames():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _child(app, structure, 'ipcdo', 'SignatureDetails', namespace='urn:wrong')
        _child(app, structure, 'ipcdo', 'ArgumentDetails', namespace='urn:wrong')

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 34), values, RuleStatus.FAIL)
    _assert_status(_rules(engine, 37), values, RuleStatus.FAIL)


def test_nested_refusal_does_not_trigger_root_level_req38():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _child(app, structure, 'ipcdo', 'RefusalDetails')

    engine, _, values, _ = _parsed_values(build)
    _assert_status(_rules(engine, 38), values, RuleStatus.PASS)


def test_req37_argument_cardinality_counts_only_direct_application_argument():
    def build(root, structure):
        app = _child(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
        _child(app, structure, 'ipcdo', 'ArgumentDetails')

    engine, _, values, _ = _parsed_values(build)
    assert ARGUMENT in values
    _assert_status(_rules(engine, 37), values, RuleStatus.PASS)
