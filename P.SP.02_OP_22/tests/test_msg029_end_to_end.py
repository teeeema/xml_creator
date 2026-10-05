from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = 'P.SP.02.MSG.029'
STRUCTURE = 'R.IP.SP.02.002'
TRANSACTION = 'P.SP.02.TRN.024'
APP = 'ipcdo:TrademarkApplicationDetails'
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
DOC_KIND_NAME = (
    'Заключение национального патентного ведомства по результатам экспертизы заявленного обозначения '
    'о возможности (невозможности) регистрации товарного знака, знака обслуживания Евразийского '
    'экономического союза'
)
MAPPED = {30,31} | ({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 33, 34, 35, 36, 37, 38, 39}) | {16, 17, 18, 19, 20, 26}


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _valid_values():
    return {
        'ccdo:EDocHeader': [None],
        'ccdo:EDocHeader/csdo:InfEnvelopeCode': MESSAGE,
        'ccdo:EDocHeader/csdo:EDocCode': STRUCTURE,
        'ccdo:EDocHeader/csdo:EDocId': '00000000-0000-0000-0000-000000000029',
        'ccdo:EDocHeader/csdo:EDocDateTime': '2026-09-30T10:00:00+03:00',
        APP: [None],
        f'{APP}/ipsdo:IPDocKindName': DOC_KIND_NAME,
        f'{APP}/ipsdo:ApplicationReceiptDate': '2026-09-24',
        f'{APP}/ipsdo:TrademarkApplicationId': 'APP-029',
        f'{APP}/ipsdo:TrademarkRegistrationCode': '01',
        PARTY: [None],
        f'{PARTY}/ipsdo:IPPartyKindCode': 'AP',
        f'{PARTY}/csdo:UnifiedCountryCode': 'RU',
        f'{PARTY}/csdo:UnifiedCountryCode/@codeListId': 'ВОИС ST.3',
        f'{PARTY}/ipsdo:IPSubjectName': 'Заявитель', f'{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode': 'OR', f'{PARTY}/ipsdo:IPSubjectName/@languageCode': 'RU',
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
        SIG: [None],
        f'{SIG}/csdo:DocCreationDate': '2026-09-24',
        FULL_NAME: [''],
        f'{FULL_NAME}/csdo:FirstName': 'Иван',
        f'{FULL_NAME}/csdo:LastName': 'Иванов',
        RESOURCE: [None],
        VALIDITY: [None],
        f'{VALIDITY}/csdo:StartDateTime': '2026-09-30T10:01:00+03:00',
    }


def _q(structure, prefix, local):
    return f'{{{structure.imported_namespaces[prefix]}}}{local}'


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


def _add_document(app, structure, *, kind='code'):
    doc = _child(app, structure, 'ipcdo', 'AccompanyingDocumentsDetails')
    if kind == 'code':
        _child(doc, structure, 'ipsdo', 'IPDocKindCode', 'DOC-CODE')
    elif kind == 'name':
        _child(doc, structure, 'ipsdo', 'IPDocKindName', 'Документ')
    _child(doc, structure, 'csdo', 'DocName', 'Приложение')
    _child(doc, structure, 'csdo', 'DocId', 'D-1')
    _child(doc, structure, 'csdo', 'DocCreationDate', '2026-09-24')
    _child(doc, structure, 'csdo', 'DocValidityDate', '2027-09-24')
    _child(doc, structure, 'csdo', 'DescriptionText', 'Описание')
    _child(doc, structure, 'csdo', 'PageQuantity', '1')
    return doc


def _add_officer(signature, structure, *, position=True):
    officer = _child(signature, structure, 'ipcdo', 'OfficerDetails')
    full = _child(officer, structure, 'ccdo', 'FullNameDetails')
    _child(full, structure, 'csdo', 'LastName', 'Петров')
    _child(full, structure, 'csdo', 'FirstName', 'Петр')
    if position:
        _child(officer, structure, 'csdo', 'PositionName', 'Специалист')
    return officer


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
    rid = f'{MESSAGE}.T45.REQ.{code}'
    return [rule for rule in engine.rules[MESSAGE].structured_rules if rule['rule_id'] == rid]


def _target_fails(engine, code, values):
    rules = _target_rules(engine, code)
    assert rules, code
    statuses = [StructuredRuleEvaluator().evaluate(rule, values).status for rule in rules]
    assert RuleStatus.FAIL in statuses, (code, statuses)


def test_valid_msg029_build_serialize_parse_extract_validate_pipeline():
    engine, structure, parsed = _build_valid_parsed()
    values, extraction_issues, validation = _extract_validate(engine, structure, parsed)
    assert not extraction_issues, [(item.code, item.field_path, item.message) for item in extraction_issues]
    assert parsed.tag == '{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails'
    assert values[f'{APP}/ipsdo:TrademarkApplicationId'] == 'APP-029'
    assert values[f'{APP}/ipsdo:TrademarkRegistrationCode'] == '01'
    assert values[f'{APP}/ipsdo:IPDocKindName'] == DOC_KIND_NAME
    assert validation.is_valid, [(item.code, item.rule_id, item.field_path, item.message) for item in validation.issues]
    assert validation.is_complete
    assert len(validation.rule_evaluations) == 41
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    assert {int(item.rule_id.split('.REQ.')[1].split('.')[0]) for item in validation.rule_evaluations} == MAPPED

    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.initiating_message == MESSAGE
    assert transaction.response_messages == ('P.SP.02.MSG.002',)
    assert transaction.initiating_operation == 'P.SP.02.OPR.008'
    assert transaction.responding_operation == 'P.SP.02.OPR.009'
    assert transaction.initiating_participant == 'P.SP.02.ACT.002'
    assert transaction.responding_participant == 'P.SP.02.ACT.001'
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(f'/{MESSAGE}')


def _mutate_req1_zero(root, structure):
    root.remove(_required(root, structure, 'ipcdo', 'TrademarkApplicationDetails'))


def _mutate_req1_two(root, structure):
    root.append(deepcopy(_required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')))


def _mutate_req2(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    app.remove(_required(app, structure, 'ipsdo', 'TrademarkApplicationId'))


def _mutate_req3(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    app.remove(_required(app, structure, 'ipsdo', 'TrademarkRegistrationCode'))


def _mutate_req4(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    _child(app, structure, 'ipsdo', 'IPDocKindCode', 'DOC-CODE')


def _mutate_req5(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    app.remove(_required(app, structure, 'ipsdo', 'IPDocKindName'))


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


def _mutate_req27(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    tm = _required(app, structure, 'ipcdo', 'TrademarkDetails')
    _required(tm, structure, 'ipsdo', 'TrademarkKindCode').text = '140'


def _mutate_req28(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    tm = _required(app, structure, 'ipcdo', 'TrademarkDetails')
    _required(tm, structure, 'ipsdo', 'CollectiveMarkIndicator').text = '2'


def _mutate_req29(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    goods = _required(app, structure, 'ipcdo', 'GoodsBaseDetails')
    goods.remove(_required(goods, structure, 'ipsdo', 'GoodsClassCode'))


def _mutate_req33(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    doc = _add_document(app, structure, kind='code')
    doc.remove(_required(doc, structure, 'csdo', 'DocId'))


def _mutate_req34(root, structure):
    refusal = _child(root, structure, 'ipcdo', 'RefusalDetails')
    _child(refusal, structure, 'csdo', 'EventDate', '2026-09-30')
    _child(refusal, structure, 'csdo', 'DescriptionText', 'Refusal')


def _mutate_req35(root, structure):
    resource = _required(root, structure, 'ccdo', 'ResourceItemStatusDetails')
    validity = _required(resource, structure, 'ccdo', 'ValidityPeriodDetails')
    validity.remove(_required(validity, structure, 'csdo', 'StartDateTime'))


def _mutate_req36(root, structure):
    resource = _required(root, structure, 'ccdo', 'ResourceItemStatusDetails')
    validity = _required(resource, structure, 'ccdo', 'ValidityPeriodDetails')
    _child(validity, structure, 'csdo', 'EndDateTime', '2026-09-30T11:00:00+03:00')


def _mutate_req37(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    app.remove(_required(app, structure, 'ipcdo', 'SignatureDetails'))


def _mutate_req38(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    signature = _required(app, structure, 'ipcdo', 'SignatureDetails')
    _add_officer(signature, structure)


def _mutate_req39(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    signature = _required(app, structure, 'ipcdo', 'SignatureDetails')
    signature.remove(_required(signature, structure, 'ccdo', 'FullNameDetails'))
    _add_officer(signature, structure, position=False)


INVALID_CASES = [
    (1, _mutate_req1_zero),
    (1, _mutate_req1_two),
    (2, _mutate_req2),
    (3, _mutate_req3),
    (4, _mutate_req4),
    (5, _mutate_req5),
    (6, _mutate_req6),
    (7, _mutate_req7),
    (8, _mutate_req8),
    (9, _mutate_req9),
    (10, _mutate_req10),
    (11, _mutate_req11),
    (12, _mutate_req12),
    (14, _mutate_req14),
    (15, _mutate_req15),
    (21, _mutate_req21),
    (22, _mutate_req22),
    (23, _mutate_req23),
    (24, _mutate_req24),
    (25, _mutate_req25),
    (27, _mutate_req27),
    (28, _mutate_req28),
    (29, _mutate_req29),
    (33, _mutate_req33),
    (34, _mutate_req34),
    (35, _mutate_req35),
    (36, _mutate_req36),
    (37, _mutate_req37),
    (38, _mutate_req38),
    (39, _mutate_req39),
]


@pytest.mark.parametrize(
    ('requirement', 'mutator'),
    INVALID_CASES,
    ids=[f'req{requirement}_{index}' for index, (requirement, _) in enumerate(INVALID_CASES)],
)
def test_each_executable_requirement_has_independent_production_xml_invalid_proof(requirement, mutator):
    engine, structure, parsed = _build_valid_parsed()
    mutator(parsed, structure)
    values, _, validation = _extract_validate(engine, structure, parsed)
    assert not validation.is_valid
    _target_fails(engine, requirement, values)


def test_same_r002_values_keep_rule_identity_isolated_by_requested_message_code():
    engine, structure, parsed = _build_valid_parsed()
    values, extraction_issues, _ = _extract_validate(engine, structure, parsed)
    assert not extraction_issues
    for code in ('P.SP.02.MSG.027', 'P.SP.02.MSG.028', 'P.SP.02.MSG.029', 'P.SP.02.MSG.030'):
        result = engine.validate_body(code, values, mode=GenerationMode.TEST)
        assert all(item.rule_id.startswith(code + '.') for item in result.rule_evaluations)
