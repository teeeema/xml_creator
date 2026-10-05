from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.loader import ProcessPackageLoader


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.057"
AUTHORITY = "ipcdo:PatentAuthorityDetails"
PAYMENT = "ipcdo:IPPaymentDetails"
PARTY = f"{PAYMENT}/ipcdo:IPPartyDetails"
DOC = f"{PAYMENT}/ipcdo:AccompanyingDocumentsDetails"


def _engine():
    orig_read = ProcessPackageLoader._read

    def safe_read(path):
        try:
            return orig_read(path)
        except Exception:
            if path.name == "P.SP.02.MSG.052.yaml":
                import json
                text = path.read_text(encoding="utf-8").strip()
                if text.endswith(r"\n"):
                    text = text[:-2].strip()
                return json.loads(text)
            raise

    with patch.object(ProcessPackageLoader, "_read", safe_read):
        return EaeuXmlEngine.load_process(PACKAGE)


def valid_values_true_indicator():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.03.003",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000057",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-10-01T12:00:00+03:00",
        AUTHORITY: [None],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": "RU",
        f"{AUTHORITY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{AUTHORITY}/csdo:AuthorityName": "Роспатент",
        f"{AUTHORITY}/ipsdo:OriginOfficeIndicator": "1",
        f"{AUTHORITY}/ccdo:SubjectAddressDetails": [""],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": "2",
        "ipsdo:TrademarkApplicationId": "2026/RU-000057",
        PAYMENT: [""],
        f"{PAYMENT}/csdo:EventDateTime": "2026-10-01T12:00:00+03:00",
        PARTY: [""],
        f"{PARTY}/ipsdo:IPPartyKindCode": "AP",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": "ООО Заявитель",
        f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": "OR",
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": "RU",
        DOC: [""],
        f"{DOC}/ipsdo:IPDocKindCode": "07015",
        f"{DOC}/csdo:DocId": "DOC-57",
        f"{DOC}/csdo:DocCreationDate": "2026-10-01",
        f"{DOC}/csdo:DocBinaryText": "AQID",
        f"{DOC}/csdo:DocBinaryText/@mediaTypeCode": "pdf",
        "ipsdo:DutyPaymentIndicator": "true",
        "csdo:PaymentAmount": "0",
        "csdo:PaymentAmount/@currencyCode": "RUB",
    }


def valid_values_false_indicator():
    values = valid_values_true_indicator()
    values["ipsdo:DutyPaymentIndicator"] = "false"
    values["csdo:PaymentAmount"] = "15000.00"
    values[f"{PARTY}/ipsdo:IPPartyKindCode"] = "PA"
    values[f"{PARTY}/ipsdo:PatentAttorneyId"] = "PA-777"
    del values[f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode"]
    return values


def test_build_serialize_parse_extract_validate_roundtrip_true_indicator():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values_true_indicator()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    parsed = ET.fromstring(serialized)
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues, f"Extraction issues: {issues}"
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert validation.is_valid, [(x.rule_id, x.message) for x in validation.issues]


def test_build_serialize_parse_extract_validate_roundtrip_false_indicator():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values_false_indicator()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    parsed = ET.fromstring(serialized)
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues, f"Extraction issues: {issues}"
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert validation.is_valid, [(x.rule_id, x.message) for x in validation.issues]


def test_e2e_req1_req2_req3_patent_authority():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values_true_indicator()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Missing UnifiedCountryCode -> fails REQ 1
    extracted_no_cc = dict(extracted)
    del extracted_no_cc[f"{AUTHORITY}/csdo:UnifiedCountryCode"]
    val1 = engine.validate_body(MESSAGE, extracted_no_cc, mode=GenerationMode.TEST)
    assert not val1.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.1" for iss in val1.issues)

    # Missing AuthorityName -> fails REQ 2
    extracted_no_name = dict(extracted)
    del extracted_no_name[f"{AUTHORITY}/csdo:AuthorityName"]
    val2 = engine.validate_body(MESSAGE, extracted_no_name, mode=GenerationMode.TEST)
    assert not val2.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.2" for iss in val2.issues)

    # AddressKindCode != "2" -> fails REQ 3
    extracted_wrong_addr = dict(
        extracted,
        **{f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": "1"},
    )
    val3 = engine.validate_body(MESSAGE, extracted_wrong_addr, mode=GenerationMode.TEST)
    assert not val3.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.3" for iss in val3.issues)


def test_e2e_req6_trademark_application_id():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values_true_indicator()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    extracted_no_app = dict(extracted)
    del extracted_no_app["ipsdo:TrademarkApplicationId"]
    val = engine.validate_body(MESSAGE, extracted_no_app, mode=GenerationMode.TEST)
    assert not val.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.6" for iss in val.issues)


def test_e2e_req7_req8_payment_details():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values_true_indicator()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Injected BankAccountDetails -> fails REQ 7
    extracted_with_bank = dict(
        extracted,
        **{f"{PAYMENT}/ccdo:BankAccountDetails": ""},
    )
    val7 = engine.validate_body(MESSAGE, extracted_with_bank, mode=GenerationMode.TEST)
    assert not val7.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.7" for iss in val7.issues)

    # Missing EventDateTime -> fails REQ 8
    extracted_no_dt = dict(extracted)
    del extracted_no_dt[f"{PAYMENT}/csdo:EventDateTime"]
    val8 = engine.validate_body(MESSAGE, extracted_no_dt, mode=GenerationMode.TEST)
    assert not val8.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.8" for iss in val8.issues)


def test_e2e_req9_to_req14_party_details():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values_true_indicator()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # AP with wrong nameRepresentationKindCode -> fails REQ 11
    extracted_bad_rep = dict(
        extracted,
        **{f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": "TR"},
    )
    val11 = engine.validate_body(MESSAGE, extracted_bad_rep, mode=GenerationMode.TEST)
    assert not val11.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.11" for iss in val11.issues)

    # PA without PatentAttorneyId -> fails REQ 12
    extracted_pa_no_id = dict(
        extracted,
        **{
            f"{PARTY}/ipsdo:IPPartyKindCode": "PA",
            f"{PARTY}/ipsdo:IPSubjectName/@languageCode": "RU",
        },
    )
    if f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode" in extracted_pa_no_id:
        del extracted_pa_no_id[f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode"]
    val12 = engine.validate_body(MESSAGE, extracted_pa_no_id, mode=GenerationMode.TEST)
    assert not val12.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.12" for iss in val12.issues)

    # PA with forbidden nameRepresentationKindCode -> fails REQ 14
    extracted_pa_with_rep = dict(
        extracted,
        **{
            f"{PARTY}/ipsdo:IPPartyKindCode": "PA",
            f"{PARTY}/ipsdo:PatentAttorneyId": "PA-1",
            f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": "OR",
            f"{PARTY}/ipsdo:IPSubjectName/@languageCode": "RU",
        },
    )
    val14 = engine.validate_body(MESSAGE, extracted_pa_with_rep, mode=GenerationMode.TEST)
    assert not val14.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.14" for iss in val14.issues)


def test_e2e_req15_to_req19_accompanying_docs():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values_true_indicator()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Injected IPDocKindName -> fails REQ 16
    extracted_with_name = dict(
        extracted,
        **{f"{DOC}/ipsdo:IPDocKindName": "Квитанция"},
    )
    val16 = engine.validate_body(MESSAGE, extracted_with_name, mode=GenerationMode.TEST)
    assert not val16.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.16" for iss in val16.issues)

    # Wrong IPDocKindCode -> fails REQ 17
    extracted_wrong_code = dict(
        extracted,
        **{f"{DOC}/ipsdo:IPDocKindCode": "99999"},
    )
    val17 = engine.validate_body(MESSAGE, extracted_wrong_code, mode=GenerationMode.TEST)
    assert not val17.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.17" for iss in val17.issues)

    # Disallowed mediaTypeCode -> fails REQ 19
    extracted_bad_media = dict(
        extracted,
        **{f"{DOC}/csdo:DocBinaryText/@mediaTypeCode": "exe"},
    )
    val19 = engine.validate_body(MESSAGE, extracted_bad_media, mode=GenerationMode.TEST)
    assert not val19.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.19" for iss in val19.issues)


def test_e2e_req20_req21_req22_duty_payment_indicator_and_amount():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values_true_indicator()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Missing DutyPaymentIndicator -> fails REQ 20
    extracted_no_ind = dict(extracted)
    del extracted_no_ind["ipsdo:DutyPaymentIndicator"]
    val20 = engine.validate_body(MESSAGE, extracted_no_ind, mode=GenerationMode.TEST)
    assert not val20.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.20" for iss in val20.issues)

    # Indicator true, PaymentAmount != 0 -> fails REQ 21
    extracted_true_nonzero = dict(
        extracted,
        **{"csdo:PaymentAmount": "5000.00"},
    )
    val21 = engine.validate_body(MESSAGE, extracted_true_nonzero, mode=GenerationMode.TEST)
    assert not val21.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.21" for iss in val21.issues)

    # Indicator false, missing PaymentAmount -> fails REQ 22
    extracted_false_no_amount = dict(
        extracted,
        **{"ipsdo:DutyPaymentIndicator": "false"},
    )
    del extracted_false_no_amount["csdo:PaymentAmount"]
    val22 = engine.validate_body(MESSAGE, extracted_false_no_amount, mode=GenerationMode.TEST)
    assert not val22.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T75.REQ.22" for iss in val22.issues)


def test_msg057_isolation():
    engine = _engine()
    rules57 = engine.rules[MESSAGE].structured_rules
    assert all(r["rule_id"].startswith(f"{MESSAGE}.") for r in rules57)
    assert len(rules57) == 20

    # Ensure other messages in OP22 preserve their own rules
    assert "P.SP.02.MSG.054" in engine.rules
    assert "P.SP.02.MSG.055" in engine.rules
    assert len(engine.rules["P.SP.02.MSG.055"].structured_rules) == 8
