from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).resolve().parents[1]
ROOT = "ipcdo:UnifiedRegisterRecordsDetails"
STATUS = f"{ROOT}/ipcdo:IPEntityStatusDetails"
PARTY = f"{ROOT}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{ROOT}/ipcdo:TrademarkDetails"
DESC = f"{TM}/ipcdo:TMDescriptionDetails"
ELEMENT = f"{DESC}/ipcdo:TMElementDetails"
GOODS = f"{ROOT}/ipcdo:GoodsBaseDetails"
DOC = f"{ROOT}/ipcdo:AccompanyingDocumentsDetails"
TRANSFORM = f"{ROOT}/ipcdo:TransformationDetails"
RESOURCE = f"{ROOT}/ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"

TRANSACTIONS = {
    "P.SP.02.MSG.016": "P.SP.02.TRN.014",
    "P.SP.02.MSG.017": "P.SP.02.TRN.015",
    "P.SP.02.MSG.018": "P.SP.02.TRN.016",
    "P.SP.02.MSG.019": "P.SP.02.TRN.017",
}


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _values(message):
    suffix = message.rsplit(".", 1)[-1]
    kinds = ["RH"]
    if message == "P.SP.02.MSG.017":
        kinds.append("UE")
    count = len(kinds)
    values = {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": message,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.007",
        "ccdo:EDocHeader/csdo:EDocId": f"00000000-0000-0000-0000-000000000{suffix}",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-24T12:00:00+03:00",
        ROOT: [None],
        f"{ROOT}/ipsdo:TrademarkId": f"TM-{suffix}",
        f"{ROOT}/ipsdo:IPDocKindCode": "12345",
        STATUS: [None],
        f"{STATUS}/csdo:EventDate": "2026-09-24",
        f"{STATUS}/csdo:StatusCode": "05" if message == "P.SP.02.MSG.019" else "03",
        PARTY: [None] * count,
        f"{PARTY}/ipsdo:IPPartyKindCode": kinds,
        f"{PARTY}/csdo:UnifiedCountryCode": ["RU"] * count,
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": ["ВОИС ST.3"] * count,
        f"{PARTY}/ipsdo:IPSubjectName": ["Правообладатель"] * count,
        ADDRESS: [""] * count,
        f"{ADDRESS}/csdo:AddressKindCode": ["2"] * count,
        f"{ADDRESS}/csdo:UnifiedCountryCode": ["RU"] * count,
        f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId": ["ВОИС ST.3"] * count,
        f"{ADDRESS}/csdo:CityName": ["Москва"] * count,
        f"{ADDRESS}/csdo:StreetName": ["Тестовая"] * count,
        f"{ADDRESS}/csdo:BuildingNumberId": [str(i + 1) for i in range(count)],
        COMM: [""] * count,
        f"{COMM}/csdo:CommunicationChannelCode": ["EM"] * count,
        f"{COMM}/csdo:CommunicationChannelId": [f"u{i}@example.test" for i in range(count)],
        TM: [None],
        f"{TM}/ipsdo:TrademarkPicture": "IMAGE",
        f"{TM}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TM}/ipsdo:CollectiveMarkIndicator": "1" if message == "P.SP.02.MSG.017" else "0",
        DESC: "",
        f"{DESC}/csdo:DescriptionText": "Описание",
        ELEMENT: "",
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
        RESOURCE: [None],
    }
    if message in {"P.SP.02.MSG.016", "P.SP.02.MSG.017"}:
        values[TRANSFORM] = [None]
        values[f"{TRANSFORM}/ipsdo:TransformationKindName"] = "Преобразование"
        values[f"{TRANSFORM}/ipsdo:IPObjectId"] = f"TM-{suffix}"
        values[f"{TRANSFORM}/csdo:EventDate"] = "2026-09-24"
    if message == "P.SP.02.MSG.017":
        values[DOC] = [None]
    if message == "P.SP.02.MSG.018":
        values[VALIDITY] = [None]
        values[f"{VALIDITY}/csdo:StartDateTime"] = "2026-09-24T12:00:00+03:00"
    if message == "P.SP.02.MSG.019":
        values[VALIDITY] = [None]
        values[f"{VALIDITY}/csdo:EndDateTime"] = "2026-09-24T13:00:00+03:00"
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
    extracted, extraction_issues = engine.body_provider._values_from_element(structure, parsed)
    assert not extraction_issues
    return extracted, engine.validate_body(message, extracted, mode=GenerationMode.TEST)


def _find(parsed, namespace, local):
    tag = f"{{{namespace}}}{local}"
    return next(node for node in parsed.iter() if node.tag == tag)


@pytest.mark.parametrize("message", TRANSACTIONS)
def test_valid_build_serialize_parse_and_structured_validation(message):
    engine, structure, parsed = _build_parse(message)
    extracted, validation = _validate(engine, structure, message, parsed)
    assert parsed.tag == f"{{{structure.namespace}}}TrademarkRegisterDetails"
    assert extracted[f"{ROOT}/ipsdo:TrademarkId"] == f"TM-{message.rsplit('.', 1)[-1]}"
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
            "P.SP.02.MSG.016",
            lambda parsed, s: setattr(_find(parsed, s.imported_namespaces["ipsdo"], "CollectiveMarkIndicator"), "text", "1"),
            "P.SP.02.MSG.016.REQ.21",
        ),
        (
            "P.SP.02.MSG.017",
            lambda parsed, s: setattr(_find(parsed, s.imported_namespaces["ipsdo"], "CollectiveMarkIndicator"), "text", "0"),
            "P.SP.02.MSG.017.REQ.21",
        ),
        (
            "P.SP.02.MSG.018",
            lambda parsed, s: setattr(_find(parsed, s.imported_namespaces["csdo"], "StatusCode"), "text", "01"),
            "P.SP.02.MSG.018.REQ.5",
        ),
        (
            "P.SP.02.MSG.019",
            lambda parsed, s: setattr(_find(parsed, s.imported_namespaces["csdo"], "StatusCode"), "text", "03"),
            "P.SP.02.MSG.019.REQ.20",
        ),
    ],
)
def test_representative_invalid_xml_fails_expected_rule(message, invalidator, expected_rule):
    engine, structure, parsed = _build_parse(message)
    invalidator(parsed, structure)
    _, validation = _validate(engine, structure, message, parsed)
    assert not validation.is_valid
    assert any(issue.code == "STRUCTURED_RULE_FAILED" and issue.rule_id == expected_rule for issue in validation.issues)
    assert any(item.rule_id == expected_rule and item.status is RuleStatus.FAIL for item in validation.rule_evaluations)
