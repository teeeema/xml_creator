from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).resolve().parents[1]
APP = "ipcdo:TrademarkApplicationDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
PARTY_ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
PARTY_COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
TMDESC = f"{TM}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
DOC = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
TRANSACTIONS = {
    "P.SP.02.MSG.011": "P.SP.02.TRN.009",
    "P.SP.02.MSG.013": "P.SP.02.TRN.011",
    "P.SP.02.MSG.014": "P.SP.02.TRN.012",
}


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _values(message):
    suffix = message.rsplit(".", 1)[-1]
    status = "30" if message == "P.SP.02.MSG.013" else "02"
    indicator = "1" if message == "P.SP.02.MSG.011" else "0"
    values = {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": message,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": f"00000000-0000-0000-0000-000000000{suffix}",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-24T12:00:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-24",
        f"{APP}/ipsdo:TrademarkApplicationId": f"APP-{suffix}",
        STATUS: [None],
        f"{STATUS}/csdo:StatusCode": status,
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": "AP",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": "Заявитель",
        f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": "OR",
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": "RU",
        PARTY_ADDRESS: [""],
        f"{PARTY_ADDRESS}/csdo:AddressKindCode": "2",
        f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY_ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY_ADDRESS}/csdo:CityName": "Москва",
        f"{PARTY_ADDRESS}/csdo:StreetName": "Тестовая",
        f"{PARTY_ADDRESS}/csdo:BuildingNumberId": "1",
        PARTY_COMM: [""],
        f"{PARTY_COMM}/csdo:CommunicationChannelCode": "EM",
        f"{PARTY_COMM}/csdo:CommunicationChannelId": "test@example.test",
        TM: [None],
        TMDESC: [None],
        f"{TMDESC}/csdo:DescriptionText": "Описание",
        f"{TM}/ipsdo:TrademarkKindCode": "110",
        f"{TM}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TM}/ipsdo:CollectiveMarkIndicator": indicator,
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "01",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        RESOURCE: [None],
        VALIDITY: [None],
    }
    if message == "P.SP.02.MSG.011":
        values[f"{VALIDITY}/csdo:StartDateTime"] = "2026-09-24T12:00:00+03:00"
    elif message == "P.SP.02.MSG.013":
        values[f"{VALIDITY}/csdo:EndDateTime"] = "2026-09-24T13:00:00+03:00"
        values[DOC] = [None]
        values[f"{DOC}/csdo:DocId"] = "D-13"
        values[f"{DOC}/csdo:DocCreationDate"] = "2026-09-24"
        values[f"{DOC}/csdo:DescriptionText"] = "Документ"
        values[f"{DOC}/csdo:PageQuantity"] = "1"
    elif message == "P.SP.02.MSG.014":
        values[f"{STATUS}/csdo:EventDate"] = "2026-09-24"
        values[f"{STATUS}/csdo:DocId"] = "D-14"
        values[f"{STATUS}/ipsdo:IPDocReceiptDate"] = "2026-09-24"
        values[f"{STATUS}/csdo:DescriptionText"] = "Изменение"
    return values


def _build_parse(message):
    engine = _engine()
    values = _values(message)
    prevalidation = engine.validate_body(message, values, mode=GenerationMode.TEST)
    assert prevalidation.is_valid, [
        (issue.code, issue.rule_id, issue.field_path, issue.message)
        for issue in prevalidation.issues
    ]
    body = engine.build_body(message, values, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    structure = engine.get_structure(message, mode=GenerationMode.TEST)
    return engine, structure, parsed


def _validate(engine, structure, message, parsed):
    reparsed = ET.fromstring(ET.tostring(parsed, encoding="utf-8"))
    extracted, extraction_issues = engine.body_provider._values_from_element(structure, reparsed)
    assert not extraction_issues
    return extracted, engine.validate_body(message, extracted, mode=GenerationMode.TEST)


def _find(parsed, namespace, local):
    tag = f"{{{namespace}}}{local}"
    return next(node for node in parsed.iter() if node.tag == tag)


@pytest.mark.parametrize("message", TRANSACTIONS)
def test_valid_build_serialize_parse_structural_and_structured_validation(message):
    engine, structure, parsed = _build_parse(message)
    extracted, validation = _validate(engine, structure, message, parsed)
    assert parsed.tag == f"{{{structure.namespace}}}TrademarkRegistrationDetails"
    assert extracted[f"{APP}/ipsdo:TrademarkApplicationId"] == f"APP-{message.rsplit('.', 1)[-1]}"
    assert validation.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in validation.issues]
    assert validation.is_complete
    assert validation.rule_evaluations and all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    transaction = engine.get_transaction(TRANSACTIONS[message])
    assert transaction.initiating_message == message
    assert engine.build_application_action(TRANSACTIONS[message], message).serialize().endswith(f"/{message}")


@pytest.mark.parametrize(
    "message,invalidator,expected_rule",
    [
        (
            "P.SP.02.MSG.011",
            lambda parsed, s: setattr(_find(parsed, s.imported_namespaces["ipsdo"], "CollectiveMarkIndicator"), "text", "0"),
            "P.SP.02.MSG.011.REQ.30",
        ),
        (
            "P.SP.02.MSG.013",
            lambda parsed, s: setattr(_find(parsed, s.imported_namespaces["csdo"], "StatusCode"), "text", "02"),
            "P.SP.02.MSG.013.REQ.5",
        ),
        (
            "P.SP.02.MSG.014",
            lambda parsed, s: _find(parsed, s.imported_namespaces["ipcdo"], "IPEntityStatusDetails").remove(
                _find(parsed, s.imported_namespaces["csdo"], "DocId")
            ),
            "P.SP.02.MSG.014.REQ.32",
        ),
    ],
)
def test_representative_invalid_fails_end_to_end(message, invalidator, expected_rule):
    engine, structure, parsed = _build_parse(message)
    invalidator(parsed, structure)
    _, validation = _validate(engine, structure, message, parsed)
    assert not validation.is_valid
    assert any(issue.code == "STRUCTURED_RULE_FAILED" and issue.rule_id == expected_rule for issue in validation.issues)
    assert any(item.rule_id == expected_rule and item.status is RuleStatus.FAIL for item in validation.rule_evaluations)
