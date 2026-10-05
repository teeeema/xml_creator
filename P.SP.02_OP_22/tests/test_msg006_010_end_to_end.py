from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).resolve().parents[1]
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
PARTY_ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
PARTY_COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
TMDESC = f"{TM}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
NAMING = f"{APP}/ipcdo:NamingAbilityProofDetails"
PROOF = f"{NAMING}/ipcdo:ProofDocTextDetails"
PRIORITY = f"{APP}/ipcdo:TrademarkPriorityDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
NATIONAL = f"{APP}/ipcdo:TrademarkNationalApplicationDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"

TRANSACTIONS = {
    "P.SP.02.MSG.006": "P.SP.02.TRN.005",
    "P.SP.02.MSG.007": "P.SP.02.TRN.006",
    "P.SP.02.MSG.009": "P.SP.02.TRN.007",
    "P.SP.02.MSG.010": "P.SP.02.TRN.008",
}


def _engine() -> EaeuXmlEngine:
    return EaeuXmlEngine.load_process(PACKAGE)


def _common_values(message: str) -> dict[str, object]:
    suffix = message.rsplit(".", 1)[-1]
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": message,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": f"00000000-0000-0000-0000-000000000{suffix}",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-22T12:00:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-22",
        f"{APP}/ipsdo:TrademarkApplicationId": f"APP-{suffix}",
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
        f"{TM}/ipsdo:CollectiveMarkIndicator": "0",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "01",
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-22T12:00:00+03:00",
    }


def _generation_values(message: str) -> dict[str, object]:
    values = _common_values(message)
    if message == "P.SP.02.MSG.006":
        values[NAMING] = [None]
        values[f"{NAMING}/ipsdo:ProofKindCode"] = "01"
        values[PROOF] = [None]
    elif message == "P.SP.02.MSG.007":
        values[PRIORITY] = [None]
        values[f"{PRIORITY}/ipsdo:PriorityKindCode"] = "01"
        values[f"{PRIORITY}/ipsdo:PriorityDate"] = "2026-09-01"
        values[f"{PRIORITY}/csdo:UnifiedCountryCode"] = "RU"
        values[f"{PRIORITY}/csdo:UnifiedCountryCode/@codeListId"] = "ВОИС ST.3"
    elif message == "P.SP.02.MSG.009":
        values[STATUS] = [None]
        values[f"{STATUS}/csdo:StatusCode"] = "21"
        values[NATIONAL] = [None]
        values[f"{VALIDITY}/csdo:EndDateTime"] = "2026-09-23T12:00:00+03:00"
    elif message == "P.SP.02.MSG.010":
        values[STATUS] = [None]
        values[f"{STATUS}/csdo:StatusCode"] = "02"
    else:
        raise AssertionError(message)
    return values


def _build_parse(message: str):
    engine = _engine()
    body = engine.build_body(message, _generation_values(message), mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    structure = engine.get_structure(message, mode=GenerationMode.TEST)
    return engine, structure, parsed


def _extract_validate(engine, structure, message: str, parsed):
    reparsed = ET.fromstring(ET.tostring(parsed, encoding="utf-8"))
    extracted, extraction_issues = engine.body_provider._values_from_element(structure, reparsed)
    assert not extraction_issues
    validation = engine.validate_body(message, extracted, mode=GenerationMode.TEST)
    return extracted, validation


@pytest.mark.parametrize("message", TRANSACTIONS)
def test_valid_message_build_serialize_parse_validate_end_to_end(message: str) -> None:
    engine, structure, parsed = _build_parse(message)
    extracted, validation = _extract_validate(engine, structure, message, parsed)

    transaction = engine.get_transaction(TRANSACTIONS[message])
    assert transaction.initiating_message == message
    assert parsed.tag == f"{{{structure.namespace}}}TrademarkRegistrationDetails"
    assert extracted[f"{APP}/ipsdo:TrademarkApplicationId"] == f"APP-{message.rsplit('.', 1)[-1]}"
    assert validation.is_valid, [(issue.code, issue.rule_id, issue.field_path, issue.message) for issue in validation.issues]
    assert validation.is_complete
    assert validation.rule_evaluations
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    assert engine.build_application_action(TRANSACTIONS[message], message).serialize().endswith(f"/{message}")


def _find(parsed, namespace: str, local_name: str):
    tag = f"{{{namespace}}}{local_name}"
    return next(element for element in parsed.iter() if element.tag == tag)


@pytest.mark.parametrize(
    ("message", "invalidator", "expected_rule"),
    [
        (
            "P.SP.02.MSG.006",
            lambda parsed, structure: _find(
                parsed, structure.imported_namespaces["ipcdo"], "TrademarkApplicationDetails"
            ).remove(
                _find(parsed, structure.imported_namespaces["ipcdo"], "TrademarkApplicationDetails").find(
                    f"{{{structure.imported_namespaces['ipcdo']}}}NamingAbilityProofDetails"
                )
            ),
            "P.SP.02.MSG.006.REQ.31",
        ),
        (
            "P.SP.02.MSG.007",
            lambda parsed, structure: _find(parsed, structure.imported_namespaces["ipcdo"], "TrademarkPriorityDetails").remove(
                _find(parsed, structure.imported_namespaces["ipsdo"], "PriorityKindCode")
            ),
            "P.SP.02.MSG.007.REQ.31",
        ),
        (
            "P.SP.02.MSG.009",
            lambda parsed, structure: setattr(
                _find(parsed, structure.imported_namespaces["csdo"], "StatusCode"), "text", "02"
            ),
            "P.SP.02.MSG.009.REQ.5",
        ),
        (
            "P.SP.02.MSG.010",
            lambda parsed, structure: setattr(
                _find(parsed, structure.imported_namespaces["ipsdo"], "CollectiveMarkIndicator"), "text", "1"
            ),
            "P.SP.02.MSG.010.REQ.30",
        ),
    ],
)
def test_representative_invalid_message_fails_end_to_end(message, invalidator, expected_rule) -> None:
    engine, structure, parsed = _build_parse(message)
    invalidator(parsed, structure)
    _, validation = _extract_validate(engine, structure, message, parsed)

    assert not validation.is_valid
    assert any(
        issue.code == "STRUCTURED_RULE_FAILED" and issue.rule_id == expected_rule
        for issue in validation.issues
    )
    assert any(
        item.rule_id == expected_rule and item.status is RuleStatus.FAIL
        for item in validation.rule_evaluations
    )
