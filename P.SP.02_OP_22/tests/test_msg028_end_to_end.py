from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = 'P.SP.02.MSG.028'
STRUCTURE = 'R.IP.SP.02.002'
TRANSACTION = 'P.SP.02.TRN.023'
APP = 'ipcdo:TrademarkApplicationDetails'
STATUS = f'{APP}/ipcdo:IPEntityStatusDetails'
PARTY = f'{APP}/ipcdo:IPPartyDetails'
ADDRESS = f'{PARTY}/ccdo:SubjectAddressDetails'
COMM = f'{PARTY}/ccdo:CommunicationDetails'
TM = f'{APP}/ipcdo:TrademarkDetails'
DESC = f'{TM}/ipcdo:TMDescriptionDetails'
GOODS = f'{APP}/ipcdo:GoodsBaseDetails'
SIG = f'{APP}/ipcdo:SignatureDetails'
FULL_NAME = f'{SIG}/ccdo:FullNameDetails'
RESOURCE = 'ccdo:ResourceItemStatusDetails'
VALIDITY = f'{RESOURCE}/ccdo:ValidityPeriodDetails'
FALLBACK = 'Заявка на регистрацию товарного знака, знака обслуживания Евразийского экономического союза'


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _valid_values():
    return {
        'ccdo:EDocHeader': [None],
        'ccdo:EDocHeader/csdo:InfEnvelopeCode': MESSAGE,
        'ccdo:EDocHeader/csdo:EDocCode': STRUCTURE,
        'ccdo:EDocHeader/csdo:EDocId': '00000000-0000-0000-0000-000000000028',
        'ccdo:EDocHeader/csdo:EDocDateTime': '2026-09-24T12:00:00+03:00',
        APP: [None],
        f'{APP}/ipsdo:IPDocKindName': FALLBACK,
        f'{APP}/ipsdo:ApplicationReceiptDate': '2026-09-24',
        f'{APP}/ipsdo:TrademarkApplicationId': 'APP-028',
        STATUS: [None],
        f'{STATUS}/csdo:StatusCode': '01',
        PARTY: [None],
        f'{PARTY}/ipsdo:IPPartyKindCode': 'AP',
        f'{PARTY}/csdo:UnifiedCountryCode': 'RU',
        f'{PARTY}/csdo:UnifiedCountryCode/@codeListId': 'ВОИС ST.3',
        f'{PARTY}/ipsdo:IPSubjectName': ['Заявитель'],
        f'{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode': ['OR'],
        f'{PARTY}/ipsdo:IPSubjectName/@languageCode': ['RU'],
        ADDRESS: [''],
        f'{ADDRESS}/csdo:AddressKindCode': '2',
        f'{ADDRESS}/csdo:UnifiedCountryCode': 'RU',
        f'{ADDRESS}/csdo:UnifiedCountryCode/@codeListId': 'ВОИС ST.3',
        f'{ADDRESS}/csdo:CityName': 'Москва',
        f'{ADDRESS}/csdo:StreetName': 'Тестовая',
        f'{ADDRESS}/csdo:BuildingNumberId': '1',
        COMM: [''],
        f'{COMM}/csdo:CommunicationChannelCode': 'EM',
        f'{COMM}/csdo:CommunicationChannelId': 'applicant@example.test',
        TM: [None],
        DESC: [''],
        f'{DESC}/csdo:DescriptionText': 'Описание',
        f'{TM}/ipsdo:TrademarkKindCode': '110',
        f'{TM}/ipsdo:TrademarkKindName': 'Словесный знак',
        f'{TM}/ipsdo:CollectiveMarkIndicator': '0',
        GOODS: [None],
        f'{GOODS}/ipsdo:GoodsClassCode': '01',
        f'{GOODS}/ipsdo:GoodsClassName': 'Класс 01',
        f'{GOODS}/ipsdo:GoodsName': 'Товар',
        f'{APP}/ipsdo:ConsentToDataProcessingIndicator': '1',
        SIG: [None],
        f'{SIG}/csdo:DocCreationDate': '2026-09-24',
        FULL_NAME: [''],
        f'{FULL_NAME}/csdo:FirstName': 'Иван',
        f'{FULL_NAME}/csdo:LastName': 'Иванов',
        RESOURCE: [None],
        VALIDITY: [None],
        f'{VALIDITY}/csdo:StartDateTime': '2026-09-24T12:01:00+03:00',
    }


def _q(structure, prefix, local):
    return f"{{{structure.imported_namespaces[prefix]}}}{local}"


def _first(parent, structure, prefix, local):
    return parent.find(_q(structure, prefix, local))


def _required(parent, structure, prefix, local):
    node = _first(parent, structure, prefix, local)
    assert node is not None, (prefix, local)
    return node


def _child(parent, structure, prefix, local, text=None, attrs=None, namespace=None):
    ns = namespace if namespace is not None else structure.imported_namespaces[prefix]
    node = ET.SubElement(parent, ET.QName(ns, local))
    if text is not None:
        node.text = text
    for key, value in (attrs or {}).items():
        node.set(key, value)
    return node


def _add_address(parent, structure, *, kind='2', country='RU'):
    address = _child(parent, structure, 'ccdo', 'SubjectAddressDetails')
    _child(address, structure, 'csdo', 'AddressKindCode', kind)
    _child(address, structure, 'csdo', 'UnifiedCountryCode', country, attrs={'codeListId': 'ВОИС ST.3'})
    _child(address, structure, 'csdo', 'CityName', 'Москва')
    _child(address, structure, 'csdo', 'StreetName', 'Тестовая')
    _child(address, structure, 'csdo', 'BuildingNumberId', '1')
    return address


def _add_comm(parent, structure):
    comm = _child(parent, structure, 'ccdo', 'CommunicationDetails')
    _child(comm, structure, 'csdo', 'CommunicationChannelCode', 'EM')
    _child(comm, structure, 'csdo', 'CommunicationChannelId', 'role@example.test')
    return comm


def _add_party(app, structure, role, *, omit=None):
    party = _child(app, structure, 'ipcdo', 'IPPartyDetails')
    _child(party, structure, 'ipsdo', 'IPPartyKindCode', role)
    _child(party, structure, 'csdo', 'UnifiedCountryCode', 'RU', attrs={'codeListId': 'ВОИС ST.3'})
    name = _child(party, structure, 'ipsdo', 'IPSubjectName', f'Party {role}')
    if role == 'AP':
        name.set('nameRepresentationKindCode', 'OR')
        name.set('languageCode', 'RU')
    if omit != 'address':
        _add_address(party, structure)
    if omit != 'communication':
        _add_comm(party, structure)
    if role == 'PA' and omit != 'attorney':
        _child(party, structure, 'ipsdo', 'PatentAttorneyId', 'PA-1')
    return party


def _build_valid_parsed():
    engine = _engine()
    body = engine.build_body(MESSAGE, _valid_values(), mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding='utf-8'))
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    return engine, structure, parsed


def _extract_validate(engine, structure, parsed, message=MESSAGE):
    reparsed = ET.fromstring(ET.tostring(parsed, encoding='utf-8'))
    values, extraction_issues = engine.body_provider._values_from_element(structure, reparsed)
    validation = engine.validate_body(message, values, mode=GenerationMode.TEST)
    return values, extraction_issues, validation


def _target_rules(engine, code):
    rid = f'{MESSAGE}.T44.REQ.{code}'
    return [rule for rule in engine.rules[MESSAGE].structured_rules if rule['rule_id'] == rid]


def _target_fails(engine, code, values):
    rules = _target_rules(engine, code)
    assert rules, code
    statuses = [StructuredRuleEvaluator().evaluate(rule, values).status for rule in rules]
    assert RuleStatus.FAIL in statuses, (code, statuses)


def test_valid_msg028_build_serialize_parse_extract_validate_pipeline():
    engine, structure, parsed = _build_valid_parsed()
    values, extraction_issues, validation = _extract_validate(engine, structure, parsed)
    assert not extraction_issues, [(i.code, i.field_path, i.message) for i in extraction_issues]
    assert parsed.tag == '{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails'
    assert values[f'{STATUS}/csdo:StatusCode'] == '01'
    assert values[f'{APP}/ipsdo:IPDocKindName'] == FALLBACK
    assert validation.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in validation.issues]
    assert validation.is_complete
    assert len(validation.rule_evaluations) == 48
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.initiating_message == MESSAGE
    assert transaction.response_messages == ('P.SP.02.MSG.002',)
    assert transaction.initiating_participant == 'P.SP.02.ACT.001'
    assert transaction.responding_participant == 'P.SP.02.ACT.002'
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(f'/{MESSAGE}')


def _mutate_req1_zero(root, structure):
    root.remove(_required(root, structure, 'ipcdo', 'TrademarkApplicationDetails'))


def _mutate_req1_two(root, structure):
    root.append(deepcopy(_required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')))


def _mutate_req2_status(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    status = _required(app, structure, 'ipcdo', 'IPEntityStatusDetails')
    _required(status, structure, 'csdo', 'StatusCode').text = '02'


def _mutate_req2_attribute(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    status = _required(app, structure, 'ipcdo', 'IPEntityStatusDetails')
    _required(status, structure, 'csdo', 'StatusCode').set('codeListId', 'STATUS')


def _mutate_req3(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    app.remove(_required(app, structure, 'ipsdo', 'TrademarkApplicationId'))


def _mutate_req4(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    _child(app, structure, 'ipsdo', 'IPDocKindCode', '12345')


def _mutate_req5(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    _required(app, structure, 'ipsdo', 'IPDocKindName').text = 'WRONG'


def _mutate_req6(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    app.remove(_required(app, structure, 'ipsdo', 'ApplicationReceiptDate'))


def _mutate_req7(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    party = _required(app, structure, 'ipcdo', 'IPPartyDetails')
    _required(party, structure, 'csdo', 'UnifiedCountryCode').set('codeListId', 'WRONG')


def _mutate_req8(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    party = _required(app, structure, 'ipcdo', 'IPPartyDetails')
    address = _required(party, structure, 'ccdo', 'SubjectAddressDetails')
    address.remove(_required(address, structure, 'csdo', 'CityName'))


def _mutate_req9(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    party = _required(app, structure, 'ipcdo', 'IPPartyDetails')
    comm = _required(party, structure, 'ccdo', 'CommunicationDetails')
    comm.remove(_required(comm, structure, 'csdo', 'CommunicationChannelId'))


def _mutate_req10(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    party = _required(app, structure, 'ipcdo', 'IPPartyDetails')
    comm = _required(party, structure, 'ccdo', 'CommunicationDetails')
    _required(comm, structure, 'csdo', 'CommunicationChannelCode').text = 'PH'


def _mutate_req11(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    authority = _child(app, structure, 'ipcdo', 'PatentAuthorityDetails')
    _child(authority, structure, 'csdo', 'AuthorityName', 'Office')
    _add_address(authority, structure, kind='2')
    _child(authority, structure, 'ipsdo', 'OriginOfficeIndicator', '1')


def _mutate_req12(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    authority = _child(app, structure, 'ipcdo', 'PatentAuthorityDetails')
    _child(authority, structure, 'csdo', 'UnifiedCountryCode', 'RU', attrs={'codeListId': 'ВОИС ST.3'})
    _child(authority, structure, 'csdo', 'AuthorityName', 'Office')
    _add_address(authority, structure, kind='3')
    _child(authority, structure, 'ipsdo', 'OriginOfficeIndicator', '1')


def _mutate_req14(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    party = _required(app, structure, 'ipcdo', 'IPPartyDetails')
    _required(party, structure, 'ipsdo', 'IPPartyKindCode').text = 'RE'


def _mutate_req15(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    party = _required(app, structure, 'ipcdo', 'IPPartyDetails')
    party.remove(_required(party, structure, 'ccdo', 'CommunicationDetails'))


def _mutate_req21(root, structure):
    _add_party(_required(root, structure, 'ipcdo', 'TrademarkApplicationDetails'), structure, 'PA', omit='attorney')


def _mutate_req22(root, structure):
    _add_party(_required(root, structure, 'ipcdo', 'TrademarkApplicationDetails'), structure, 'RE', omit='address')


def _add_correspondence(app, structure, *, kind='3', country='RU'):
    corr = _child(app, structure, 'ipcdo', 'CorrespondenceAddressDetails')
    _add_address(corr, structure, kind=kind, country=country)


def _mutate_req23(root, structure):
    _add_correspondence(_required(root, structure, 'ipcdo', 'TrademarkApplicationDetails'), structure, kind='2')


def _mutate_req24(root, structure):
    _add_correspondence(_required(root, structure, 'ipcdo', 'TrademarkApplicationDetails'), structure, country='US')


def _mutate_req25(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    app.remove(_required(app, structure, 'ipcdo', 'TrademarkDetails'))


def _mutate_req26(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    tm = _required(app, structure, 'ipcdo', 'TrademarkDetails')
    _required(tm, structure, 'ipsdo', 'TrademarkKindCode').text = '999'
    _required(tm, structure, 'ipsdo', 'TrademarkKindName').text = 'Неизвестный знак'


def _mutate_req27(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    tm = _required(app, structure, 'ipcdo', 'TrademarkDetails')
    _required(tm, structure, 'ipsdo', 'TrademarkKindCode').text = '140'
    _required(tm, structure, 'ipsdo', 'TrademarkKindName').text = 'Изобразительный знак'


@pytest.mark.parametrize(('code', 'name', 'expected'), [
    ('110', 'Словесный знак', RuleStatus.PASS),
    ('110', 'Неизвестный знак', RuleStatus.PASS),
    ('999', 'Словесный знак', RuleStatus.PASS),
    ('999', 'Неизвестный знак', RuleStatus.FAIL),
    (None, None, RuleStatus.FAIL),
])
def test_req26_inclusive_or_truth_table_uses_production_extraction(code, name, expected):
    engine, structure, parsed = _build_valid_parsed()
    app = _required(parsed, structure, 'ipcdo', 'TrademarkApplicationDetails')
    trademark = _required(app, structure, 'ipcdo', 'TrademarkDetails')
    for prefix, local, value in (
        ('ipsdo', 'TrademarkKindCode', code),
        ('ipsdo', 'TrademarkKindName', name),
    ):
        node = _required(trademark, structure, prefix, local)
        if value is None:
            trademark.remove(node)
        else:
            node.text = value
    values, extraction_issues, _ = _extract_validate(engine, structure, parsed)
    assert not extraction_issues
    statuses = [StructuredRuleEvaluator().evaluate(rule, values).status for rule in _target_rules(engine, 26)]
    assert statuses == [expected]


def _mutate_req28(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    tm = _required(app, structure, 'ipcdo', 'TrademarkDetails')
    _required(tm, structure, 'ipsdo', 'CollectiveMarkIndicator').text = '2'


def _mutate_req29(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    goods = _required(app, structure, 'ipcdo', 'GoodsBaseDetails')
    goods.remove(_required(goods, structure, 'ipsdo', 'GoodsClassCode'))


def _mutate_req30(root, structure, field):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    goods = _required(app, structure, 'ipcdo', 'GoodsBaseDetails')
    _child(goods, structure, 'ipsdo', field, 'X')


def _add_priority(app, structure):
    priority = _child(app, structure, 'ipcdo', 'TrademarkPriorityDetails')
    _child(priority, structure, 'ipsdo', 'PriorityKindCode', '010')
    _child(priority, structure, 'ipsdo', 'PriorityKindName', 'Приоритет')
    _child(priority, structure, 'ipsdo', 'PriorityDate', '2026-09-24')
    _child(priority, structure, 'csdo', 'UnifiedCountryCode', 'RU', attrs={'codeListId': 'ВОИС ST.3'})
    return priority


def _mutate_req31(root, structure, field, forbidden):
    priority = _add_priority(_required(root, structure, 'ipcdo', 'TrademarkApplicationDetails'), structure)
    if forbidden:
        _child(priority, structure, 'ipsdo', field, 'X')
    else:
        priority.remove(_required(priority, structure, 'csdo' if field == 'UnifiedCountryCode' else 'ipsdo', field))


def _add_document(app, structure):
    doc = _child(app, structure, 'ipcdo', 'AccompanyingDocumentsDetails')
    _child(doc, structure, 'ipsdo', 'IPDocKindCode', '12345')
    _child(doc, structure, 'ipsdo', 'IPDocKindName', 'Документ')
    _child(doc, structure, 'csdo', 'DocId', 'D-1')
    _child(doc, structure, 'csdo', 'DocCreationDate', '2026-09-24')
    _child(doc, structure, 'csdo', 'DescriptionText', 'Описание')
    _child(doc, structure, 'csdo', 'PageQuantity', '1')
    return doc


def _mutate_req33(root, structure, prefix, field):
    doc = _add_document(_required(root, structure, 'ipcdo', 'TrademarkApplicationDetails'), structure)
    doc.remove(_required(doc, structure, prefix, field))


def _mutate_req34(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    _required(app, structure, 'ipsdo', 'ConsentToDataProcessingIndicator').text = '0'


def _mutate_req35(root, structure, child):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    _child(app, structure, 'ipcdo', child)


def _mutate_req36(root, structure):
    _child(root, structure, 'ipcdo', 'RefusalDetails')


def _mutate_req37(root, structure):
    resource = _required(root, structure, 'ccdo', 'ResourceItemStatusDetails')
    validity = _required(resource, structure, 'ccdo', 'ValidityPeriodDetails')
    validity.remove(_required(validity, structure, 'csdo', 'StartDateTime'))


def _mutate_req38(root, structure, field):
    resource = _required(root, structure, 'ccdo', 'ResourceItemStatusDetails')
    if field == 'EndDateTime':
        validity = _required(resource, structure, 'ccdo', 'ValidityPeriodDetails')
        _child(validity, structure, 'csdo', field, '2026-09-24T13:00:00+03:00')
    else:
        _child(resource, structure, 'csdo', field, '2026-09-24T13:00:00+03:00')


def _mutate_req39(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    app.remove(_required(app, structure, 'ipcdo', 'SignatureDetails'))


def _add_officer(signature, structure, *, position=True):
    officer = _child(signature, structure, 'ipcdo', 'OfficerDetails')
    name = _child(officer, structure, 'ccdo', 'FullNameDetails')
    _child(name, structure, 'csdo', 'LastName', 'Петров')
    _child(name, structure, 'csdo', 'FirstName', 'Петр')
    if position:
        _child(officer, structure, 'csdo', 'PositionName', 'Специалист')
    return officer


def _mutate_req40(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    signature = _required(app, structure, 'ipcdo', 'SignatureDetails')
    _add_officer(signature, structure)


def _mutate_req41(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    signature = _required(app, structure, 'ipcdo', 'SignatureDetails')
    signature.remove(_required(signature, structure, 'ccdo', 'FullNameDetails'))
    _add_officer(signature, structure, position=False)


BASIC_INVALID_CASES = [
    (1, _mutate_req1_zero), (1, _mutate_req1_two),
    (2, _mutate_req2_status), (2, _mutate_req2_attribute),
    (3, _mutate_req3), (4, _mutate_req4), (5, _mutate_req5),
    (6, _mutate_req6), (7, _mutate_req7), (8, _mutate_req8), (9, _mutate_req9), (10, _mutate_req10),
    (11, _mutate_req11), (12, _mutate_req12), (14, _mutate_req14), (15, _mutate_req15),
    (21, _mutate_req21), (22, _mutate_req22), (23, _mutate_req23), (24, _mutate_req24),
    (25, _mutate_req25), (26, _mutate_req26), (27, _mutate_req27), (28, _mutate_req28), (29, _mutate_req29),
    (34, _mutate_req34), (36, _mutate_req36), (37, _mutate_req37), (39, _mutate_req39),
    (40, _mutate_req40), (41, _mutate_req41),
]


@pytest.mark.parametrize(('requirement', 'mutator'), BASIC_INVALID_CASES, ids=[f'req{req}_{i}' for i, (req, _) in enumerate(BASIC_INVALID_CASES)])
def test_each_basic_executable_requirement_has_independent_invalid_proof(requirement, mutator):
    engine, structure, parsed = _build_valid_parsed()
    mutator(parsed, structure)
    values, _, validation = _extract_validate(engine, structure, parsed)
    assert not validation.is_valid
    _target_fails(engine, requirement, values)


@pytest.mark.parametrize('field', ['TrademarkDecisionIndicator', 'TrademarkApplicationId', 'ApellationOfOriginEAEUId', 'TrademarkRegRefusalReasonText'])
def test_req30_each_forbidden_goods_child_has_independent_invalid_proof(field):
    engine, structure, parsed = _build_valid_parsed()
    _mutate_req30(parsed, structure, field)
    values, _, _ = _extract_validate(engine, structure, parsed)
    _target_fails(engine, 30, values)


@pytest.mark.parametrize(('field', 'forbidden'), [
    ('PriorityKindCode', False), ('PriorityKindName', False), ('PriorityDate', False), ('UnifiedCountryCode', False),
    ('ExhibitionSiteText', True), ('FirstTrademarkApplicationId', True),
])
def test_req31_each_required_and_forbidden_priority_field_has_invalid_proof(field, forbidden):
    engine, structure, parsed = _build_valid_parsed()
    _mutate_req31(parsed, structure, field, forbidden)
    values, _, _ = _extract_validate(engine, structure, parsed)
    _target_fails(engine, 31, values)


@pytest.mark.parametrize(('prefix', 'field'), [
    ('ipsdo', 'IPDocKindCode'), ('ipsdo', 'IPDocKindName'), ('csdo', 'DocId'),
    ('csdo', 'DocCreationDate'), ('csdo', 'DescriptionText'), ('csdo', 'PageQuantity'),
])
def test_req33_each_required_document_field_has_invalid_proof(prefix, field):
    engine, structure, parsed = _build_valid_parsed()
    _mutate_req33(parsed, structure, prefix, field)
    values, _, _ = _extract_validate(engine, structure, parsed)
    _target_fails(engine, 33, values)


@pytest.mark.parametrize('child', [
    'TrademarkNationalApplicationDetails', 'ApplicantChangeDetails', 'TrademarkClaimDetails', 'ComplaintDetails', 'ApplicantComplainResponseDetails'
])
def test_req35_each_forbidden_application_subtree_has_independent_invalid_proof(child):
    engine, structure, parsed = _build_valid_parsed()
    _mutate_req35(parsed, structure, child)
    values, _, _ = _extract_validate(engine, structure, parsed)
    _target_fails(engine, 35, values)


@pytest.mark.parametrize('field', ['EndDateTime', 'UpdateDateTime'])
def test_req38_end_and_update_have_separate_invalid_proofs(field):
    engine, structure, parsed = _build_valid_parsed()
    _mutate_req38(parsed, structure, field)
    values, _, _ = _extract_validate(engine, structure, parsed)
    _target_fails(engine, 38, values)


def test_same_r002_values_execute_only_rules_for_requested_message_code():
    engine, structure, parsed = _build_valid_parsed()
    values, _, result028 = _extract_validate(engine, structure, parsed, MESSAGE)
    result027 = engine.validate_body('P.SP.02.MSG.027', values, mode=GenerationMode.TEST)
    result029 = engine.validate_body('P.SP.02.MSG.029', values, mode=GenerationMode.TEST)
    assert result028.rule_evaluations and all(item.rule_id.startswith('P.SP.02.MSG.028.') for item in result028.rule_evaluations)
    assert result027.rule_evaluations and all(item.rule_id.startswith('P.SP.02.MSG.027.') for item in result027.rule_evaluations)
    assert result029.rule_evaluations and all(item.rule_id.startswith('P.SP.02.MSG.029.') for item in result029.rule_evaluations)

    msg028_rule_ids = {item.rule_id for item in result028.rule_evaluations}
    msg029_rule_ids = {item.rule_id for item in result029.rule_evaluations}
    assert not any(rule_id.startswith('P.SP.02.MSG.029.') for rule_id in msg028_rule_ids)
    assert not any(rule_id.startswith('P.SP.02.MSG.028.') for rule_id in msg029_rule_ids)
    assert msg028_rule_ids.isdisjoint(msg029_rule_ids)
