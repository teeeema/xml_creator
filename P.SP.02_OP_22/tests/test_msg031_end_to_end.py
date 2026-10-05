from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.031"
TRANSACTION = "P.SP.02.TRN.026"
R002 = "R.IP.SP.02.002"
R007 = "R.IP.SP.02.007"
APP = "ipcdo:TrademarkApplicationDetails"
R007_ROOT = "ipcdo:UnifiedRegisterRecordsDetails"
REFUSAL_NAME = (
    "Решение об отказе в регистрации товарного знака, знака обслуживания "
    "Евразийского экономического союза"
)
REGISTRATION_NAME = (
    "Решение о регистрации товарного знака, знака обслуживания Евразийского "
    "экономического союза в отношении всех заявленных товаров и (или) услуг"
)


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _sample_value(field):
    datatype = (field.datatype or "").lower()
    if "indicatortype" in datatype:
        return True
    if "datetimetype" in datatype:
        return "2026-09-30T12:00:00+03:00"
    if datatype.endswith("datetype"):
        return "2026-09-30"
    if "quantity" in datatype or "integer" in datatype:
        return 1
    return "TEST"


def _minimal_values(structure):
    fields_by_id = {field.field_id: field for field in structure.fields}
    included = set()
    children = {field.parent for field in structure.fields if field.parent}
    values = {}
    for field in sorted(structure.fields, key=lambda item: item.order):
        if not field.min_occurs:
            continue
        if field.parent and field.parent not in included:
            continue
        included.add(field.field_id)
        if field.kind == "ATTRIBUTE" or field.field_id not in children:
            values[field.path] = _sample_value(field)
        else:
            values[field.path] = None
    return values


def _header(values, root_path, structure_id, edoc_id):
    values.update(
        {
            f"{root_path}ccdo:EDocHeader": [None],
            f"{root_path}ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
            f"{root_path}ccdo:EDocHeader/csdo:EDocCode": structure_id,
            f"{root_path}ccdo:EDocHeader/csdo:EDocId": edoc_id,
            f"{root_path}ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T12:00:00+03:00",
        }
    )


def _r002_values(structure):
    values = _minimal_values(structure)
    _header(values, "", R002, "00000000-0000-0000-0000-000000000231")

    party = f"{APP}/ipcdo:IPPartyDetails"
    address = f"{party}/ccdo:SubjectAddressDetails"
    comm = f"{party}/ccdo:CommunicationDetails"
    tm = f"{APP}/ipcdo:TrademarkDetails"
    desc = f"{tm}/ipcdo:TMDescriptionDetails"
    goods = f"{APP}/ipcdo:GoodsBaseDetails"
    status = f"{APP}/ipcdo:IPEntityStatusDetails"
    sig = f"{APP}/ipcdo:SignatureDetails"
    full = f"{sig}/ccdo:FullNameDetails"
    refusal = "ipcdo:RefusalDetails"
    resource = "ccdo:ResourceItemStatusDetails"
    validity = f"{resource}/ccdo:ValidityPeriodDetails"

    values.update(
        {
            APP: [None],
            f"{APP}/ipsdo:IPDocKindName": REFUSAL_NAME,
            f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-24",
            f"{APP}/ipsdo:TrademarkApplicationId": "APP-031-R002",
            status: [None],
            f"{status}/csdo:StatusCode": "20",
            f"{status}/csdo:EventDate": "2026-09-30",
            party: [None],
            f"{party}/ipsdo:IPPartyKindCode": "AP",
            f"{party}/csdo:UnifiedCountryCode": "RU",
            f"{party}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            f"{party}/ipsdo:IPSubjectName": "Заявитель",
            f"{party}/ipsdo:IPSubjectName/@nameRepresentationKindCode": "OR",
            f"{party}/ipsdo:IPSubjectName/@languageCode": "RU",
            address: [None],
            f"{address}/csdo:AddressKindCode": "2",
            f"{address}/csdo:UnifiedCountryCode": "RU",
            f"{address}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            f"{address}/csdo:CityName": "Москва",
            f"{address}/csdo:StreetName": "Тестовая",
            f"{address}/csdo:BuildingNumberId": "1",
            comm: [None],
            f"{comm}/csdo:CommunicationChannelCode": "EM",
            f"{comm}/csdo:CommunicationChannelId": "applicant@example.test",
            tm: [None],
            desc: [None],
            f"{desc}/csdo:DescriptionText": "Описание",
            f"{tm}/ipsdo:TrademarkKindCode": "110",
            f"{tm}/ipsdo:TrademarkKindName": "Словесный знак",
            f"{tm}/ipsdo:CollectiveMarkIndicator": "0",
            goods: [None],
            f"{goods}/ipsdo:GoodsClassCode": "01",
            f"{goods}/ipsdo:GoodsClassName": "Класс 01",
            f"{goods}/ipsdo:GoodsName": "Товар",
            sig: [None],
            f"{sig}/csdo:DocCreationDate": "2026-09-30",
            full: [None],
            f"{full}/csdo:FirstName": "Иван",
            f"{full}/csdo:LastName": "Иванов",
            refusal: [None],
            f"{refusal}/csdo:EventDate": "2026-09-30",
            f"{refusal}/csdo:DescriptionText": "Отказ в регистрации",
            resource: [None],
            validity: [None],
            f"{validity}/csdo:StartDateTime": "2026-09-30T12:00:00+03:00",
            f"{validity}/csdo:EndDateTime": "2026-09-30T12:01:00+03:00",
        }
    )
    return values


def _r007_values(structure):
    values = _minimal_values(structure)
    _header(values, "", R007, "00000000-0000-0000-0000-000000000731")

    root = R007_ROOT
    party = f"{root}/ipcdo:IPPartyDetails"
    address = f"{party}/ccdo:SubjectAddressDetails"
    comm = f"{party}/ccdo:CommunicationDetails"
    tm = f"{root}/ipcdo:TrademarkDetails"
    desc = f"{tm}/ipcdo:TMDescriptionDetails"
    element = f"{desc}/ipcdo:TMElementDetails"
    goods = f"{root}/ipcdo:GoodsBaseDetails"
    status = f"{root}/ipcdo:IPEntityStatusDetails"
    sig = f"{root}/ipcdo:SignatureDetails"
    full = f"{sig}/ccdo:FullNameDetails"
    resource = f"{root}/ccdo:ResourceItemStatusDetails"
    validity = f"{resource}/ccdo:ValidityPeriodDetails"

    values.update(
        {
            root: [None],
            f"{root}/ipsdo:IPDocKindName": REGISTRATION_NAME,
            f"{root}/ipsdo:TrademarkApplicationId": "APP-031-R007",
            f"{root}/ipsdo:TrademarkId": "TM-031",
            f"{root}/ipsdo:RegistrationDate": "2026-09-30",
            f"{root}/csdo:DocValidityDate": "2036-09-30",
            status: [None],
            f"{status}/csdo:StatusCode": "01",
            f"{status}/csdo:EventDate": "2026-09-30",
            party: [None],
            f"{party}/ipsdo:IPPartyKindCode": "RH",
            f"{party}/csdo:UnifiedCountryCode": "RU",
            f"{party}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            f"{party}/ipsdo:IPSubjectName": "Правообладатель",
            address: [None],
            f"{address}/csdo:AddressKindCode": "2",
            f"{address}/csdo:UnifiedCountryCode": "RU",
            f"{address}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            f"{address}/csdo:CityName": "Москва",
            f"{address}/csdo:StreetName": "Тестовая",
            f"{address}/csdo:BuildingNumberId": "1",
            comm: [None],
            f"{comm}/csdo:CommunicationChannelCode": "EM",
            f"{comm}/csdo:CommunicationChannelId": "holder@example.test",
            tm: [None],
            f"{tm}/ipsdo:TrademarkPicture": "QUJD",
            desc: [None],
            f"{desc}/csdo:DescriptionText": "Описание",
            element: [None],
            f"{element}/ipsdo:TrademarkCFECode": "01.01.01",
            f"{element}/csdo:DesignationName": "TEST",
            f"{element}/ipsdo:TMLocalizedName": "Тест",
            f"{element}/ipsdo:TMLocalizedName/@languageCode": "RU",
            f"{element}/ipsdo:TMTransliterationName": "Test",
            f"{tm}/ipsdo:TrademarkKindName": "Словесный знак",
            f"{tm}/ipsdo:CollectiveMarkIndicator": "0",
            goods: [None],
            f"{goods}/ipsdo:GoodsClassCode": "01",
            f"{goods}/ipsdo:GoodsClassName": "Класс 01",
            f"{goods}/ipsdo:GoodsName": "Товар",
            f"{goods}/ipsdo:TrademarkDecisionIndicator": "1",
            f"{goods}/ipsdo:TrademarkApplicationId": "APP-031-R007",
            sig: [None],
            f"{sig}/csdo:DocCreationDate": "2026-09-30",
            full: [None],
            f"{full}/csdo:FirstName": "Иван",
            f"{full}/csdo:LastName": "Иванов",
            resource: [None],
            validity: [None],
            f"{validity}/csdo:StartDateTime": "2026-09-30T12:00:00+03:00",
        }
    )
    return values


def _container_values(engine):
    container = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    values = _minimal_values(container)
    values.update(
        {
            "ccdo:EDocHeader": [None],
            "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
            "ccdo:EDocHeader/csdo:EDocCode": "R.010",
            "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000031",
            "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T12:00:00+03:00",
        }
    )
    return values


def _embedded_values(engine, structure_id):
    structure = engine.resolve_structure(structure_id, mode=GenerationMode.TEST).definition
    if structure_id == R002:
        return _r002_values(structure)
    if structure_id == R007:
        return _r007_values(structure)
    raise AssertionError(structure_id)


def _build_payload(engine, structure_id):
    body = engine.build_body(
        MESSAGE,
        _container_values(engine),
        mode=GenerationMode.TEST,
        embedded_structure_id=structure_id,
        embedded_values=_embedded_values(engine, structure_id),
    )
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    outer = ET.fromstring(serialized)
    payload = list(outer)[-1]
    return body, outer, payload


@pytest.mark.parametrize(
    ("structure_id", "table", "expected_qname", "expected_rule_count"),
    [
        (R002, 48, "{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails", 36),
        (R007, 49, "{urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}TrademarkRegisterDetails", 26),
    ],
)
def test_msg031_build_serialize_parse_extract_validate_for_each_embedded_branch(
    structure_id, table, expected_qname, expected_rule_count
):
    engine = _engine()
    _, outer, payload = _build_payload(engine, structure_id)

    assert outer.tag == "{urn:EEC:R:GenericEDocDetails:vY.Y.Y}GenericEDocDetails"
    assert payload.tag == expected_qname

    embedded = engine.resolve_structure(structure_id, mode=GenerationMode.TEST).definition
    extracted, extraction_issues = engine.body_provider._values_from_element(embedded, payload)
    assert not extraction_issues, [
        (item.code, item.field_path, item.message) for item in extraction_issues
    ]
    assert extracted

    values = _container_values(engine)
    values["*"] = payload
    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert result.is_valid, [
        (item.code, item.rule_id, item.field_path, item.message) for item in result.issues
    ]
    assert result.is_complete
    assert len(result.rule_evaluations) == expected_rule_count
    assert all(item.status is RuleStatus.PASS for item in result.rule_evaluations)
    assert all(item.rule_id.startswith(f"{MESSAGE}.T{table}.REQ.") for item in result.rule_evaluations)
    opposite = 49 if table == 48 else 48
    assert not any(f".T{opposite}." in item.rule_id for item in result.rule_evaluations)


def test_table47_one_of_rejects_neither_payload():
    engine = _engine()
    result = engine.validate_body(MESSAGE, _container_values(engine), mode=GenerationMode.TEST)
    assert not result.is_valid
    assert "EMBEDDED_STRUCTURE_CARDINALITY" in {issue.code for issue in result.issues}


def test_table47_one_of_rejects_both_allowed_payloads():
    engine = _engine()
    _, _, r002 = _build_payload(engine, R002)
    _, _, r007 = _build_payload(engine, R007)
    values = _container_values(engine)
    values["*"] = [r002, r007]
    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert not result.is_valid
    assert "EMBEDDED_STRUCTURE_CARDINALITY" in {issue.code for issue in result.issues}


@pytest.mark.parametrize(
    ("local_name", "wrong_namespace"),
    [
        ("TrademarkRegistrationDetails", "urn:test:wrong:r002"),
        ("TrademarkRegisterDetails", "urn:test:wrong:r007"),
    ],
)
def test_table47_one_of_does_not_recognize_right_local_name_in_wrong_namespace(local_name, wrong_namespace):
    engine = _engine()
    fake = ET.Element(ET.QName(wrong_namespace, local_name))
    values = _container_values(engine)
    values["*"] = fake
    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert not result.is_valid
    assert "UNKNOWN_EMBEDDED_STRUCTURE" in {issue.code for issue in result.issues}


def test_transaction_context_for_msg031_is_trn026_opr015_to_opr016():
    engine = _engine()
    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.initiating_message == MESSAGE
    assert transaction.response_messages == ("P.SP.02.MSG.002",)
    assert transaction.initiating_operation == "P.SP.02.OPR.015"
    assert transaction.responding_operation == "P.SP.02.OPR.016"
    assert transaction.initiating_participant == "P.SP.02.ACT.001"
    assert transaction.responding_participant == "P.SP.02.ACT.002"
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(f"/{MESSAGE}")


def test_same_r010_r002_payload_executes_only_rules_of_requested_message():
    engine = _engine()
    _, _, payload = _build_payload(engine, R002)

    values031 = _container_values(engine)
    values031["*"] = payload
    result031 = engine.validate_body(MESSAGE, values031, mode=GenerationMode.TEST)
    ids031 = {item.rule_id for item in result031.rule_evaluations}
    assert ids031
    assert all(rule_id.startswith("P.SP.02.MSG.031.") for rule_id in ids031)

    values003 = dict(values031)
    values003["ccdo:EDocHeader/csdo:InfEnvelopeCode"] = "P.SP.02.MSG.003"
    result003 = engine.validate_body("P.SP.02.MSG.003", values003, mode=GenerationMode.TEST)
    ids003 = {item.rule_id for item in result003.rule_evaluations}
    assert ids003
    assert all(rule_id.startswith("P.SP.02.MSG.003.") for rule_id in ids003)

    assert ids031.isdisjoint(ids003)
    assert not any(rule_id.startswith("P.SP.02.MSG.003.") for rule_id in ids031)
    assert not any(rule_id.startswith("P.SP.02.MSG.031.") for rule_id in ids003)
