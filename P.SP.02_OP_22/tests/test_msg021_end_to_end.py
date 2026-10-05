from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.021"
MESSAGE_NO_RULES = "P.SP.02.MSG.023"
STRUCTURE = "R.IP.SP.02.007"
TRANSACTION = "P.SP.02.TRN.019"
P = "ipcdo:UnifiedRegisterRecordsDetails"
STATUS = f"{P}/ipcdo:IPEntityStatusDetails"
PARTY = f"{P}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{P}/ipcdo:TrademarkDetails"
DESC = f"{TM}/ipcdo:TMDescriptionDetails"
ELEMENT = f"{DESC}/ipcdo:TMElementDetails"
GOODS = f"{P}/ipcdo:GoodsBaseDetails"
RESOURCE = f"{P}/ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
DOC_DATE = f"{P}/csdo:DocValidityDate"
FALLBACK = "Заявление о продлении срока действия исключительного права на товарный знак, знак обслуживания Евразийского экономического союза"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _fail_ids(validation):
    return {
        issue.rule_id
        for issue in validation.issues
        if issue.code == "STRUCTURED_RULE_FAILED" and issue.rule_id
    }


def _valid_values(*, fallback=False):
    values = {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": STRUCTURE,
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000021",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-24T12:00:00+03:00",
        P: [None],
        f"{P}/ipsdo:TrademarkId": "TM-021",
        STATUS: [None],
        f"{STATUS}/csdo:EventDate": "2026-09-24",
        f"{STATUS}/csdo:StatusCode": "03",
        DOC_DATE: "2036-09-24",
        RESOURCE: [None],
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": "RH",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": "Правообладатель",
        ADDRESS: [""],
        f"{ADDRESS}/csdo:AddressKindCode": "2",
        f"{ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{ADDRESS}/csdo:CityName": "Москва",
        f"{ADDRESS}/csdo:StreetName": "Тестовая",
        f"{ADDRESS}/csdo:BuildingNumberId": "1",
        COMM: [""],
        f"{COMM}/csdo:CommunicationChannelCode": "EM",
        f"{COMM}/csdo:CommunicationChannelId": "test@example.test",
        TM: [None],
        f"{TM}/ipsdo:TrademarkPicture": "IMAGE",
        f"{TM}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TM}/ipsdo:CollectiveMarkIndicator": "0",
        DESC: [""],
        f"{DESC}/csdo:DescriptionText": "Описание",
        ELEMENT: [""],
        f"{ELEMENT}/ipsdo:TrademarkCFECode": "01.01.01",
        f"{ELEMENT}/csdo:DesignationName": "TEST",
        f"{ELEMENT}/ipsdo:TMLocalizedName": "TEST",
        f"{ELEMENT}/ipsdo:TMLocalizedName/@languageCode": "ru",
        f"{ELEMENT}/ipsdo:TMTransliterationName": "TEST",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        f"{GOODS}/ipsdo:TrademarkDecisionIndicator": True,
        f"{GOODS}/ipsdo:TrademarkApplicationId": "APP-1",
    }
    if fallback:
        values[f"{P}/ipsdo:IPDocKindName"] = FALLBACK
    else:
        values[f"{P}/ipsdo:IPDocKindCode"] = "12345"
    return values


def _build_parse_validate(values):
    engine = _engine()
    pre = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert pre.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in pre.issues]
    body = engine.build_body(MESSAGE, values, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    post = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    return engine, structure, parsed, extracted, post


def _child(parent, structure, prefix, local, text=None, attrs=None, namespace=None):
    ns = namespace if namespace is not None else structure.imported_namespaces[prefix]
    node = ET.SubElement(parent, ET.QName(ns, local))
    if text is not None:
        node.text = text
    for key, value in (attrs or {}).items():
        node.set(key, value)
    return node


def _raw_root(engine, message=MESSAGE):
    structure = engine.get_structure(message, mode=GenerationMode.TEST)
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    header = _child(root, structure, "ccdo", "EDocHeader")
    _child(header, structure, "csdo", "InfEnvelopeCode", message)
    _child(header, structure, "csdo", "EDocCode", STRUCTURE)
    _child(header, structure, "csdo", "EDocId", "00000000-0000-0000-0000-000000000021")
    _child(header, structure, "csdo", "EDocDateTime", "2026-09-24T12:00:00+03:00")
    return structure, root


def _add_party(record, structure, kind="RH", suffix="1"):
    party = _child(record, structure, "ipcdo", "IPPartyDetails")
    _child(party, structure, "ipsdo", "IPPartyKindCode", kind)
    _child(party, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
    _child(party, structure, "ipsdo", "IPSubjectName", f"Правообладатель {suffix}")
    address = _child(party, structure, "ccdo", "SubjectAddressDetails")
    _child(address, structure, "csdo", "AddressKindCode", "2")
    _child(address, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
    _child(address, structure, "csdo", "CityName", "Москва")
    _child(address, structure, "csdo", "StreetName", "Тестовая")
    _child(address, structure, "csdo", "BuildingNumberId", suffix)
    comm = _child(party, structure, "ccdo", "CommunicationDetails")
    _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
    _child(comm, structure, "csdo", "CommunicationChannelId", f"u{suffix}@example.test")
    return party


def _add_trademark(record, structure):
    tm = _child(record, structure, "ipcdo", "TrademarkDetails")
    _child(tm, structure, "ipsdo", "TrademarkPicture", "IMAGE")
    desc = _child(tm, structure, "ipcdo", "TMDescriptionDetails")
    _child(desc, structure, "csdo", "DescriptionText", "Описание")
    element = _child(desc, structure, "ipcdo", "TMElementDetails")
    _child(element, structure, "ipsdo", "TrademarkCFECode", "01.01.01")
    _child(element, structure, "csdo", "DesignationName", "TEST")
    localized = _child(element, structure, "ipsdo", "TMLocalizedName", "TEST")
    localized.set("languageCode", "ru")
    _child(element, structure, "ipsdo", "TMTransliterationName", "TEST")
    _child(tm, structure, "ipsdo", "TrademarkKindName", "Словесный знак")
    _child(tm, structure, "ipsdo", "CollectiveMarkIndicator", "0")


def _add_goods(record, structure, *, forbidden=False):
    goods = _child(record, structure, "ipcdo", "GoodsBaseDetails")
    _child(goods, structure, "ipsdo", "GoodsClassName", "Класс 01")
    _child(goods, structure, "ipsdo", "GoodsName", "Товар")
    _child(goods, structure, "ipsdo", "TrademarkDecisionIndicator", "1")
    _child(goods, structure, "ipsdo", "TrademarkApplicationId", "APP-1")
    if forbidden:
        _child(goods, structure, "ipsdo", "TrademarkId", "FORBIDDEN")


def _add_valid_record(root, structure, *, status="03", fallback=False, party_kinds=("RH",), direct_date=True, end=False, bad_goods=False):
    record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
    _child(record, structure, "ipsdo", "TrademarkId", "TM-021")
    if fallback:
        _child(record, structure, "ipsdo", "IPDocKindName", FALLBACK)
    else:
        _child(record, structure, "ipsdo", "IPDocKindCode", "12345")
    status_node = _child(record, structure, "ipcdo", "IPEntityStatusDetails")
    _child(status_node, structure, "csdo", "EventDate", "2026-09-24")
    _child(status_node, structure, "csdo", "StatusCode", status)
    if direct_date:
        _child(record, structure, "csdo", "DocValidityDate", "2036-09-24")
    for index, kind in enumerate(party_kinds):
        _add_party(record, structure, kind, str(index + 1))
    _add_trademark(record, structure)
    _add_goods(record, structure, forbidden=bad_goods)
    resource = _child(record, structure, "ccdo", "ResourceItemStatusDetails")
    if end:
        validity = _child(resource, structure, "ccdo", "ValidityPeriodDetails")
        _child(validity, structure, "csdo", "EndDateTime", "2036-09-24T12:00:00+03:00")
    return record


def _extract_validate_raw(build, message=MESSAGE):
    engine = _engine()
    structure, root = _raw_root(engine, message)
    build(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues, [(i.code, i.field_path, i.message) for i in issues]
    validation = engine.validate_body(message, values, mode=GenerationMode.TEST)
    return engine, structure, parsed, values, validation


def test_valid_msg021_build_serialize_parse_extract_validate():
    engine, structure, parsed, extracted, validation = _build_parse_validate(_valid_values())
    assert parsed.tag == f"{{{structure.namespace}}}TrademarkRegisterDetails"
    assert extracted[f"{STATUS}/csdo:StatusCode"] == "03"
    assert extracted[DOC_DATE] == "2036-09-24"
    assert validation.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in validation.issues]
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.initiating_message == MESSAGE
    assert transaction.response_messages == ("P.SP.02.MSG.002",)
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(f"/{MESSAGE}")


def test_missing_trademark_id_fails_req1():
    values = _valid_values()
    values.pop(f"{P}/ipsdo:TrademarkId")
    validation = _engine().validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert "P.SP.02.MSG.021.T54.REQ.1" in _fail_ids(validation)


def test_two_outer_records_fail_req2():
    def build(root, structure):
        _add_valid_record(root, structure)
        _add_valid_record(root, structure)

    *_, validation = _extract_validate_raw(build)
    assert "P.SP.02.MSG.021.T54.REQ.2" in _fail_ids(validation)


def test_end_datetime_present_fails_req3():
    values = _valid_values()
    values[RESOURCE] = [None]
    values[VALIDITY] = [None]
    values[f"{VALIDITY}/csdo:EndDateTime"] = "2036-09-24T12:00:00+03:00"
    validation = _engine().validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert "P.SP.02.MSG.021.T54.REQ.3" in _fail_ids(validation)


def test_wrong_status_fails_req20():
    values = _valid_values()
    values[f"{STATUS}/csdo:StatusCode"] = "01"
    validation = _engine().validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert "P.SP.02.MSG.021.T54.REQ.20" in _fail_ids(validation)


def test_status_codelistid_must_be_absent():
    good = _engine().validate_body(MESSAGE, _valid_values(), mode=GenerationMode.TEST)
    assert "P.SP.02.MSG.021.T54.REQ.20" not in _fail_ids(good)
    bad_values = _valid_values()
    bad_values[f"{STATUS}/csdo:StatusCode/@codeListId"] = "SOME-LIST"
    bad = _engine().validate_body(MESSAGE, bad_values, mode=GenerationMode.TEST)
    assert "P.SP.02.MSG.021.T54.REQ.20" in _fail_ids(bad)


def test_exact_fallback_document_name_is_valid_end_to_end():
    *_, validation = _build_parse_validate(_valid_values(fallback=True))
    assert validation.is_valid


def test_wrong_fallback_document_name_fails_req5():
    values = _valid_values(fallback=True)
    values[f"{P}/ipsdo:IPDocKindName"] = "WRONG"
    validation = _engine().validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert "P.SP.02.MSG.021.T54.REQ.5" in _fail_ids(validation)


@pytest.mark.parametrize("party_kinds", [(), ("XX",), ("RH", "RH")])
def test_rh_cardinality_failures(party_kinds):
    def build(root, structure):
        _add_valid_record(root, structure, party_kinds=party_kinds)

    *_, validation = _extract_validate_raw(build)
    assert "P.SP.02.MSG.021.T54.REQ.6_19" in _fail_ids(validation)


def test_invalid_inherited_repeatable_fails_req17():
    def build(root, structure):
        record = _add_valid_record(root, structure)
        _add_goods(record, structure, forbidden=True)

    *_, validation = _extract_validate_raw(build)
    assert "P.SP.02.MSG.021.T54.REQ.6_19" in _fail_ids(validation)


def test_nested_doc_validity_does_not_replace_direct_req21_target():
    def build(root, structure):
        record = _add_valid_record(root, structure, direct_date=False)
        doc = _child(record, structure, "ipcdo", "AccompanyingDocumentsDetails")
        _child(doc, structure, "csdo", "DocValidityDate", "2036-09-24")

    *_, validation = _extract_validate_raw(build)
    assert "P.SP.02.MSG.021.T54.REQ.21" in _fail_ids(validation)


def test_wrong_namespace_direct_doc_validity_does_not_satisfy_req21():
    def build(root, structure):
        record = _add_valid_record(root, structure, direct_date=False)
        _child(record, structure, "csdo", "DocValidityDate", "2036-09-24", namespace="urn:wrong")

    *_, validation = _extract_validate_raw(build)
    assert "P.SP.02.MSG.021.T54.REQ.21" in _fail_ids(validation)


def test_msg021_rules_do_not_apply_to_msg023_same_structure_dispatch():
    engine = _engine()
    values = _valid_values()
    values["ccdo:EDocHeader/csdo:InfEnvelopeCode"] = MESSAGE_NO_RULES
    values.pop(f"{P}/ipsdo:TrademarkId")
    values.pop(DOC_DATE)
    values[f"{STATUS}/csdo:StatusCode"] = "01"
    values[RESOURCE] = [None]
    values[VALIDITY] = [None]
    values[f"{VALIDITY}/csdo:EndDateTime"] = "2036-09-24T12:00:00+03:00"

    msg021_values = deepcopy(values)
    msg021_values["ccdo:EDocHeader/csdo:InfEnvelopeCode"] = MESSAGE
    msg021 = engine.validate_body(MESSAGE, msg021_values, mode=GenerationMode.TEST)
    assert {
        "P.SP.02.MSG.021.T54.REQ.1",
        "P.SP.02.MSG.021.T54.REQ.3",
        "P.SP.02.MSG.021.T54.REQ.20",
        "P.SP.02.MSG.021.T54.REQ.21",
    }.issubset(_fail_ids(msg021))

    msg023 = engine.validate_body(MESSAGE_NO_RULES, values, mode=GenerationMode.TEST)
    assert msg023.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in msg023.issues]
    assert not msg023.rule_evaluations


def test_msg016_020_dispatch_never_executes_msg021_rule_ids():
    engine = _engine()
    for code in ("P.SP.02.MSG.016", "P.SP.02.MSG.017", "P.SP.02.MSG.018", "P.SP.02.MSG.019", "P.SP.02.MSG.020"):
        values = _valid_values()
        values["ccdo:EDocHeader/csdo:InfEnvelopeCode"] = code
        validation = engine.validate_body(code, values, mode=GenerationMode.TEST)
        assert all(not item.rule_id.startswith("P.SP.02.MSG.021") for item in validation.rule_evaluations)
