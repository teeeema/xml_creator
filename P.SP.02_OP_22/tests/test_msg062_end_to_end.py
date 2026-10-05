from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET
import pytest

from eaeu_xml.core.errors import BodyValidationError
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.062"
TRANSACTION = "P.SP.02.TRN.053"
STRUCTURE_ID = "R.IP.SP.02.002"

APP = "ipcdo:TrademarkApplicationDetails"
PA = f"{APP}/ipcdo:PatentAuthorityDetails"
CORR = f"{APP}/ipcdo:CorrespondenceAddressDetails"
CORR_ADDR = f"{CORR}/ccdo:SubjectAddressDetails"
CORR_COMM = f"{CORR}/ccdo:CommunicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
PARTY_ADDR = f"{PARTY}/ccdo:SubjectAddressDetails"
PARTY_COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
TMDESC = f"{TM}/ipcdo:TMDescriptionDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
ARG = f"{APP}/ipcdo:ArgumentDetails"
CLAIM = f"{APP}/ipcdo:TrademarkClaimDetails"
STAKE = f"{CLAIM}/ipcdo:StakeholderDetails"
STAKE_ADDR = f"{STAKE}/ccdo:SubjectAddressDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
SIG = f"{APP}/ipcdo:SignatureDetails"
OFFICER = f"{SIG}/ipcdo:OfficerDetails"
OFFICER_FN = f"{OFFICER}/ccdo:FullNameDetails"


def _engine() -> EaeuXmlEngine:
    return EaeuXmlEngine.load_process(PACKAGE)


def _generation_values() -> dict[str, object]:
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": STRUCTURE_ID,
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000062",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T12:00:00+03:00",

        APP: [None],
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-30",
        f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000001",

        # PatentAuthorityDetails
        PA: [None],
        f"{PA}/csdo:UnifiedCountryCode": "RU",
        f"{PA}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PA}/csdo:AuthorityName": "Роспатент",
        f"{PA}/ipsdo:OriginOfficeIndicator": True,
        f"{PA}/ccdo:SubjectAddressDetails": [""],
        f"{PA}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": "2",
        f"{PA}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode": "RU",
        f"{PA}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PA}/ccdo:SubjectAddressDetails/csdo:CityName": "Москва",
        f"{PA}/ccdo:SubjectAddressDetails/csdo:StreetName": "Бережковская наб.",
        f"{PA}/ccdo:SubjectAddressDetails/csdo:BuildingNumberId": "30",

        # CorrespondenceAddressDetails
        CORR_ADDR: [""],
        f"{CORR_ADDR}/csdo:AddressKindCode": "3",
        f"{CORR_ADDR}/csdo:UnifiedCountryCode": "RU",
        f"{CORR_ADDR}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{CORR_ADDR}/csdo:CityName": "Москва",
        f"{CORR_ADDR}/csdo:StreetName": "Бережковская наб.",
        f"{CORR_ADDR}/csdo:BuildingNumberId": "30",

        CORR_COMM: [""],
        f"{CORR_COMM}/csdo:CommunicationChannelCode": "EM",
        f"{CORR_COMM}/csdo:CommunicationChannelId": "info@rupto.ru",

        # IPPartyDetails
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": "AP",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": ["Заявитель"],
        f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": ["OR"],
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": ["RU"],

        PARTY_ADDR: [""],
        f"{PARTY_ADDR}/csdo:AddressKindCode": "2",
        f"{PARTY_ADDR}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY_ADDR}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY_ADDR}/csdo:CityName": "Москва",
        f"{PARTY_ADDR}/csdo:StreetName": "Тверская ул.",
        f"{PARTY_ADDR}/csdo:BuildingNumberId": "1",

        PARTY_COMM: [""],
        f"{PARTY_COMM}/csdo:CommunicationChannelCode": "EM",
        f"{PARTY_COMM}/csdo:CommunicationChannelId": "applicant@example.ru",

        # TrademarkDetails
        TM: [None],
        TMDESC: [""],
        f"{TMDESC}/csdo:DescriptionText": "Словесный товарный знак",
        f"{TM}/ipsdo:TrademarkKindCode": "110",
        f"{TM}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TM}/ipsdo:CollectiveMarkIndicator": "0",

        # GoodsBaseDetails
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassCode": "09",
        f"{GOODS}/ipsdo:GoodsClassName": "Приборы и инструменты",
        f"{GOODS}/ipsdo:GoodsName": "Программное обеспечение",

        # ArgumentDetails
        ARG: [""],
        f"{ARG}/csdo:DescriptionText": "Доводы заявителя по обращению",
        f"{ARG}/csdo:EventDate": "2026-09-30",

        # TrademarkClaimDetails
        CLAIM: [None],
        f"{CLAIM}/ipsdo:RequestId": "REQ-062-001",
        f"{CLAIM}/ipsdo:RequestDate": "2026-09-30",

        STAKE: [""],
        f"{STAKE}/csdo:UnifiedCountryCode": "RU",
        f"{STAKE}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{STAKE}/csdo:SubjectName": "Заинтересованное лицо",
        f"{STAKE}/csdo:SubjectBriefName": "ЗЛ",

        STAKE_ADDR: [""],
        f"{STAKE_ADDR}/csdo:AddressKindCode": "1",
        f"{STAKE_ADDR}/csdo:UnifiedCountryCode": "RU",
        f"{STAKE_ADDR}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{STAKE_ADDR}/csdo:CityName": "Москва",
        f"{STAKE_ADDR}/csdo:StreetName": "Ленина ул.",
        f"{STAKE_ADDR}/csdo:BuildingNumberId": "10",

        # ResourceItemStatusDetails
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T10:00:00+03:00",

        # SignatureDetails
        SIG: [None],
        f"{SIG}/csdo:DocCreationDate": "2026-09-30",
        OFFICER: [""],
        OFFICER_FN: [None],
        f"{OFFICER_FN}/csdo:LastName": "Сидоров",
        f"{OFFICER_FN}/csdo:FirstName": "Сидор",
        f"{OFFICER}/csdo:PositionName": "Патентный поверенный",
    }


def _round_trip_and_validate(values):
    engine = _engine()
    body = engine.build_body(MESSAGE, values, mode=GenerationMode.TEST)
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    parsed = ET.fromstring(serialized)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    extracted, extraction_issues = engine.body_provider._values_from_element(structure, parsed)
    assert not extraction_issues, [(i.code, i.field_path, i.message) for i in extraction_issues]
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    return engine, parsed, extracted, validation


def test_transaction_binding_and_metadata():
    engine = _engine()
    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.transaction_code == TRANSACTION
    assert transaction.procedure_code == "P.SP.02.PRC.009"
    assert transaction.initiating_message == MESSAGE
    assert transaction.response_messages == ("P.SP.02.MSG.002",)
    assert transaction.initiating_operation == "P.SP.02.OPR.194"
    assert transaction.responding_operation == "P.SP.02.OPR.195"

    message_def = engine.get_message(MESSAGE)
    assert message_def.structure_id == STRUCTURE_ID
    assert message_def.structure_version == "1.0.0"
    assert message_def.direction == "REQUEST"
    assert TRANSACTION in message_def.context


def test_msg062_full_build_serialize_parse_and_validate_passes():
    engine, parsed, extracted, validation = _round_trip_and_validate(_generation_values())

    expected_qname = f"{{{engine.get_structure(MESSAGE, mode=GenerationMode.TEST).namespace}}}TrademarkRegistrationDetails"
    assert parsed.tag == expected_qname
    assert extracted[f"{APP}/ipsdo:TrademarkApplicationId"] == "2026/RU-000001"
    assert validation.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in validation.issues]
    assert validation.is_complete
    assert validation.rule_evaluations
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(f"/{MESSAGE}")


def test_msg062_missing_trademark_application_id_fails():
    engine = _engine()
    vals = _generation_values()
    vals.pop(f"{APP}/ipsdo:TrademarkApplicationId")
    with pytest.raises(BodyValidationError) as excinfo:
        engine.build_body(MESSAGE, vals, mode=GenerationMode.TEST)
    failed_rule_ids = {issue.rule_id for issue in excinfo.value.issues if issue.rule_id}
    assert f"{MESSAGE}.T81.REQ.4" in failed_rule_ids


def test_msg062_missing_argument_details_fails():
    engine = _engine()
    vals = _generation_values()
    vals.pop(ARG)
    vals.pop(f"{ARG}/csdo:DescriptionText")
    vals.pop(f"{ARG}/csdo:EventDate")
    with pytest.raises(BodyValidationError) as excinfo:
        engine.build_body(MESSAGE, vals, mode=GenerationMode.TEST)
    failed_rule_ids = {issue.rule_id for issue in excinfo.value.issues if issue.rule_id}
    assert f"{MESSAGE}.T81.REQ.5" in failed_rule_ids


def test_msg062_missing_start_date_time_fails():
    engine = _engine()
    vals = _generation_values()
    vals.pop(f"{VALIDITY}/csdo:StartDateTime")
    with pytest.raises(BodyValidationError) as excinfo:
        engine.build_body(MESSAGE, vals, mode=GenerationMode.TEST)
    failed_rule_ids = {issue.rule_id for issue in excinfo.value.issues if issue.rule_id}
    assert f"{MESSAGE}.T81.REQ.35" in failed_rule_ids


def test_msg062_end_date_time_present_fails():
    engine = _engine()
    vals = _generation_values()
    vals[f"{VALIDITY}/csdo:EndDateTime"] = "2026-10-01T12:00:00+03:00"
    with pytest.raises(BodyValidationError) as excinfo:
        engine.build_body(MESSAGE, vals, mode=GenerationMode.TEST)
    failed_rule_ids = {issue.rule_id for issue in excinfo.value.issues if issue.rule_id}
    assert f"{MESSAGE}.T81.REQ.36" in failed_rule_ids


def test_msg062_forbidden_complaint_details_fails():
    engine = _engine()
    vals = _generation_values()
    vals[f"{APP}/ipcdo:ComplaintDetails"] = [None]
    with pytest.raises(BodyValidationError) as excinfo:
        engine.build_body(MESSAGE, vals, mode=GenerationMode.TEST)
    failed_rule_ids = {issue.rule_id for issue in excinfo.value.issues if issue.rule_id}
    assert f"{MESSAGE}.T81.REQ.33" in failed_rule_ids


def test_msg062_forbidden_refusal_details_fails():
    engine = _engine()
    vals = _generation_values()
    vals["ipcdo:RefusalDetails"] = [None]
    with pytest.raises(BodyValidationError) as excinfo:
        engine.build_body(MESSAGE, vals, mode=GenerationMode.TEST)
    failed_rule_ids = {issue.rule_id for issue in excinfo.value.issues if issue.rule_id}
    assert f"{MESSAGE}.T81.REQ.34" in failed_rule_ids
