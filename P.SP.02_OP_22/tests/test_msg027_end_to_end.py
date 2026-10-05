from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = 'P.SP.02.MSG.027'
STRUCTURE = 'R.IP.SP.02.002'
TRANSACTION = 'P.SP.02.TRN.022'
APP = 'ipcdo:TrademarkApplicationDetails'
STATUS = f'{APP}/ipcdo:IPEntityStatusDetails'
PARTY = f'{APP}/ipcdo:IPPartyDetails'
ADDRESS = f'{PARTY}/ccdo:SubjectAddressDetails'
COMM = f'{PARTY}/ccdo:CommunicationDetails'
TM = f'{APP}/ipcdo:TrademarkDetails'
DESC = f'{TM}/ipcdo:TMDescriptionDetails'
GOODS = f'{APP}/ipcdo:GoodsBaseDetails'
RESOURCE = 'ccdo:ResourceItemStatusDetails'
VALIDITY = f'{RESOURCE}/ccdo:ValidityPeriodDetails'
FALLBACK = 'Уведомление о признании заявки на регистрацию товарного знака, знака обслуживания Евразийского экономического союза отозванной'


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _valid_values():
    return {
        'ccdo:EDocHeader': [None],
        'ccdo:EDocHeader/csdo:InfEnvelopeCode': MESSAGE,
        'ccdo:EDocHeader/csdo:EDocCode': STRUCTURE,
        'ccdo:EDocHeader/csdo:EDocId': '00000000-0000-0000-0000-000000000027',
        'ccdo:EDocHeader/csdo:EDocDateTime': '2026-09-24T12:00:00+03:00',
        APP: [None],
        f'{APP}/ipsdo:IPDocKindName': FALLBACK,
        f'{APP}/ipsdo:ApplicationReceiptDate': '2026-09-24',
        f'{APP}/ipsdo:TrademarkApplicationId': 'APP-027',
        STATUS: [None],
        f'{STATUS}/csdo:StatusCode': '32',
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
        DESC: [None],
        f'{DESC}/csdo:DescriptionText': 'Описание',
        f'{TM}/ipsdo:TrademarkKindCode': '110',
        f'{TM}/ipsdo:TrademarkKindName': 'Словесный знак',
        f'{TM}/ipsdo:CollectiveMarkIndicator': '0',
        GOODS: [None],
        f'{GOODS}/ipsdo:GoodsClassCode': '01',
        f'{GOODS}/ipsdo:GoodsClassName': 'Класс 01',
        f'{GOODS}/ipsdo:GoodsName': 'Товар',
        RESOURCE: [None],
        VALIDITY: [None],
        f'{VALIDITY}/csdo:EndDateTime': '2026-09-24T13:00:00+03:00',
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


def _add_authority(app, structure, *, country=True, name=True):
    authority = _child(app, structure, 'ipcdo', 'PatentAuthorityDetails')
    if country:
        _child(authority, structure, 'csdo', 'UnifiedCountryCode', 'RU', attrs={'codeListId': 'ВОИС ST.3'})
    if name:
        _child(authority, structure, 'csdo', 'AuthorityName', 'Patent office')
    _add_address(authority, structure, kind='2')
    _child(authority, structure, 'ipsdo', 'OriginOfficeIndicator', '1')
    return authority


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
    if code in {1, 2, 3, 4, 5, 30}:
        rid = f'{MESSAGE}.T57.REQ.{code}'
        return [r for r in engine.rules[MESSAGE].structured_rules if r['rule_id'] == rid]
    return [
        r for r in engine.rules[MESSAGE].structured_rules
        if len(r.get('source_refs', [])) == 2
        and r['source_refs'][1].get('table') == '34'
        and r['source_refs'][1].get('item') == str(code)
    ]


def _target_fails(engine, code, values):
    rules = _target_rules(engine, code)
    assert rules, code
    statuses = [StructuredRuleEvaluator().evaluate(rule, values).status for rule in rules]
    assert RuleStatus.FAIL in statuses, (code, statuses)


def test_valid_msg027_full_build_serialize_parse_extract_validate_pipeline():
    engine, structure, parsed = _build_valid_parsed()
    values, extraction_issues, validation = _extract_validate(engine, structure, parsed)
    assert not extraction_issues, [(i.code, i.field_path, i.message) for i in extraction_issues]
    assert parsed.tag == '{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails'
    assert values[f'{STATUS}/csdo:StatusCode'] == '32'
    assert values[f'{APP}/ipsdo:IPDocKindName'] == FALLBACK
    assert validation.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in validation.issues]
    assert validation.is_complete
    assert validation.rule_evaluations
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.initiating_message == MESSAGE
    assert transaction.response_messages == ('P.SP.02.MSG.002',)
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(f'/{MESSAGE}')


def _mutate_req1_two_apps(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    root.append(deepcopy(app))


def _mutate_req2(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    code = ET.Element(ET.QName(structure.imported_namespaces['ipsdo'], 'IPDocKindCode'))
    code.text = '12345'
    app.insert(0, code)


def _mutate_req3(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    _required(app, structure, 'ipsdo', 'IPDocKindName').text = 'WRONG'


def _mutate_req4(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    app.remove(_required(app, structure, 'ipsdo', 'TrademarkApplicationId'))


def _mutate_req5(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    status = _required(app, structure, 'ipcdo', 'IPEntityStatusDetails')
    _required(status, structure, 'csdo', 'StatusCode').text = '31'


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
    _add_authority(app, structure, country=False)


def _mutate_req12(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    _add_authority(app, structure, name=False)


def _mutate_req14(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    party = _required(app, structure, 'ipcdo', 'IPPartyDetails')
    _required(party, structure, 'ipsdo', 'IPPartyKindCode').text = 'XX'


def _mutate_req15(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    party = _required(app, structure, 'ipcdo', 'IPPartyDetails')
    party.remove(_required(party, structure, 'ccdo', 'CommunicationDetails'))


def _mutate_req21(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    _add_party(app, structure, 'PA', omit='attorney')


def _mutate_req22(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    _add_party(app, structure, 'RE', omit='address')


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
    _required(tm, structure, 'ipsdo', 'TrademarkKindName').text = 'Недопустимый вид'


def _mutate_req28(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    tm = _required(app, structure, 'ipcdo', 'TrademarkDetails')
    _required(tm, structure, 'ipsdo', 'CollectiveMarkIndicator').text = '2'


def _mutate_req29(root, structure):
    app = _required(root, structure, 'ipcdo', 'TrademarkApplicationDetails')
    goods = _required(app, structure, 'ipcdo', 'GoodsBaseDetails')
    goods.remove(_required(goods, structure, 'ipsdo', 'GoodsClassCode'))


def _mutate_req30(root, structure):
    resource = _required(root, structure, 'ccdo', 'ResourceItemStatusDetails')
    validity = _required(resource, structure, 'ccdo', 'ValidityPeriodDetails')
    validity.remove(_required(validity, structure, 'csdo', 'EndDateTime'))


INVALID_CASES = [
    (1, _mutate_req1_two_apps),
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
    (26, _mutate_req26),
    (28, _mutate_req28),
    (29, _mutate_req29),
    (30, _mutate_req30),
]


@pytest.mark.parametrize(('requirement', 'mutator'), INVALID_CASES, ids=[f'req{item}' for item, _ in INVALID_CASES])
def test_each_executable_requirement_has_independent_invalid_proof(requirement, mutator):
    engine, structure, parsed = _build_valid_parsed()
    mutator(parsed, structure)
    values, _, validation = _extract_validate(engine, structure, parsed)
    assert not validation.is_valid
    _target_fails(engine, requirement, values)


def test_same_r002_xml_gets_message_specific_evaluations_and_no_msg027_leakage():
    engine, structure, parsed = _build_valid_parsed()
    values, extraction_issues, validation27 = _extract_validate(engine, structure, parsed, MESSAGE)
    assert not extraction_issues
    validation28 = engine.validate_body('P.SP.02.MSG.028', values, mode=GenerationMode.TEST)
    validation10 = engine.validate_body('P.SP.02.MSG.010', values, mode=GenerationMode.TEST)
    assert validation27.rule_evaluations
    assert validation28.rule_evaluations
    assert all(item.rule_id.startswith(MESSAGE + '.') for item in validation27.rule_evaluations)
    assert all(item.rule_id.startswith('P.SP.02.MSG.028.') for item in validation28.rule_evaluations)
    assert {item.rule_id for item in validation27.rule_evaluations}.isdisjoint(
        {item.rule_id for item in validation28.rule_evaluations}
    )
    assert all(item.rule_id.startswith('P.SP.02.MSG.010') for item in validation10.rule_evaluations)
    assert all(not item.rule_id.startswith(MESSAGE) for item in validation10.rule_evaluations)


def test_unmapped_requirements_never_produce_synthetic_evaluations():
    engine, structure, parsed = _build_valid_parsed()
    _, _, validation = _extract_validate(engine, structure, parsed)
    rules = engine.rules[MESSAGE].structured_rules
    for item in (13, 27):
        assert not any(
            len(rule.get('source_refs', [])) == 2 and rule['source_refs'][1].get('item') == str(item)
            for rule in rules
        )
    assert all(item.rule_id != f'{MESSAGE}.T57.REQ.13' for item in validation.rule_evaluations)
