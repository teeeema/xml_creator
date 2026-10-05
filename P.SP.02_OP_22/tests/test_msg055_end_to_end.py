from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.loader import ProcessPackageLoader


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.055"
AUTHORITY = "ipcdo:PatentAuthorityDetails"
PAYMENT = "ipcdo:IPPaymentDetails"


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


def valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.03.003",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000055",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        PAYMENT: [None],
        f"{PAYMENT}/csdo:PaymentKindName": "Пошлина",
        f"{PAYMENT}/ccdo:BankAccountDetails": [""],
        f"{PAYMENT}/ccdo:BankAccountDetails/csdo:BankAccountId": "00000000000000000000",
        f"{PAYMENT}/ccdo:BankAccountDetails/ccdo:BankDetails": [""],
        f"{PAYMENT}/ccdo:BankAccountDetails/ccdo:BankDetails/csdo:BusinessEntityName": "Тестовый банк",
        f"{PAYMENT}/ccdo:BankAccountDetails/ccdo:BankDetails/csdo:UnifiedBankId": "044525225",
        f"{PAYMENT}/ccdo:BankAccountDetails/ccdo:BankDetails/csdo:UnifiedBankId/@schemeId": "BIC",
        AUTHORITY: [None],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": "RU",
        f"{AUTHORITY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{AUTHORITY}/csdo:AuthorityName": "Роспатент",
        f"{AUTHORITY}/ipsdo:OriginOfficeIndicator": "1",
        f"{AUTHORITY}/ccdo:SubjectAddressDetails": [""],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": "2",
        "ipsdo:IPLegalActionKindCode": "00055",
        "ipsdo:IPLegalActionKindCode/@codeListId": "1.0",
        "ipsdo:TrademarkApplicationId": "2026/RU-000055",
    }


def test_build_serialize_parse_extract_validate_roundtrip_with_required_account():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    parsed = ET.fromstring(serialized)
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues, f"Extraction issues: {issues}"
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert validation.is_valid, [(x.rule_id, x.message) for x in validation.issues]


def test_build_serialize_parse_extract_validate_roundtrip_with_clean_payment():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = dict(
        valid_values(),
        **{
            PAYMENT: [None],
            f"{PAYMENT}/csdo:PaymentKindName": "Пошлина за действия",
        },
    )
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
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Missing UnifiedCountryCode -> fails REQ 1
    extracted_no_cc = dict(extracted)
    del extracted_no_cc[f"{AUTHORITY}/csdo:UnifiedCountryCode"]
    val1 = engine.validate_body(MESSAGE, extracted_no_cc, mode=GenerationMode.TEST)
    assert not val1.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T73.REQ.1" for iss in val1.issues)

    # Missing AuthorityName -> fails REQ 2
    extracted_no_name = dict(extracted)
    del extracted_no_name[f"{AUTHORITY}/csdo:AuthorityName"]
    val2 = engine.validate_body(MESSAGE, extracted_no_name, mode=GenerationMode.TEST)
    assert not val2.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T73.REQ.2" for iss in val2.issues)

    # AddressKindCode != "2" -> fails REQ 3
    extracted_wrong_addr = dict(
        extracted,
        **{f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["1"]},
    )
    val3 = engine.validate_body(MESSAGE, extracted_wrong_addr, mode=GenerationMode.TEST)
    assert not val3.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T73.REQ.3" for iss in val3.issues)


def test_e2e_req4_req5_legal_action_kind():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Code present and Name present -> FAIL REQ 4
    extracted_both = dict(extracted, **{"ipsdo:IPLegalActionKindName": "Продление"})
    val_both = engine.validate_body(MESSAGE, extracted_both, mode=GenerationMode.TEST)
    assert not val_both.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T73.REQ.4" for iss in val_both.issues)

    # Code absent and Name present -> PASS
    extracted_name_only = dict(extracted)
    del extracted_name_only["ipsdo:IPLegalActionKindCode"]
    if "ipsdo:IPLegalActionKindCode/@codeListId" in extracted_name_only:
        del extracted_name_only["ipsdo:IPLegalActionKindCode/@codeListId"]
    extracted_name_only["ipsdo:IPLegalActionKindName"] = "Продление"
    val_name = engine.validate_body(MESSAGE, extracted_name_only, mode=GenerationMode.TEST)
    assert val_name.is_valid

    # Both absent -> FAIL REQ 5
    extracted_neither = dict(extracted)
    del extracted_neither["ipsdo:IPLegalActionKindCode"]
    if "ipsdo:IPLegalActionKindCode/@codeListId" in extracted_neither:
        del extracted_neither["ipsdo:IPLegalActionKindCode/@codeListId"]
    val_neither = engine.validate_body(MESSAGE, extracted_neither, mode=GenerationMode.TEST)
    assert not val_neither.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T73.REQ.5" for iss in val_neither.issues)


def test_e2e_req6_trademark_application_id_required():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Missing TrademarkApplicationId -> FAIL REQ 6
    extracted_no_tm = dict(extracted)
    del extracted_no_tm["ipsdo:TrademarkApplicationId"]
    val_no_tm = engine.validate_body(MESSAGE, extracted_no_tm, mode=GenerationMode.TEST)
    assert not val_no_tm.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T73.REQ.6" for iss in val_no_tm.issues)


def test_e2e_req8_forbidden_payment_event_datetime():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Add EventDateTime to payment in extracted values -> FAIL REQ 8
    extracted_dirty = dict(
        extracted,
        **{
            PAYMENT: [{}],
            f"{PAYMENT}/csdo:EventDateTime": ["2026-09-30T14:30:00+03:00"],
        },
    )
    val = engine.validate_body(MESSAGE, extracted_dirty, mode=GenerationMode.TEST)
    assert not val.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T73.REQ.8" for iss in val.issues)


def test_e2e_req9_forbidden_payment_amount():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Add PaymentAmount to payment in extracted values -> FAIL REQ 9
    extracted_dirty = dict(
        extracted,
        **{
            PAYMENT: [{}],
            f"{PAYMENT}/csdo:PaymentAmount": ["25000.00"],
        },
    )
    val = engine.validate_body(MESSAGE, extracted_dirty, mode=GenerationMode.TEST)
    assert not val.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T73.REQ.9" for iss in val.issues)


def test_e2e_msg054_isolation_payment_permitted_in_msg055():
    engine = _engine()
    # MSG055 with payment details is completely valid under MSG055
    original = dict(
        valid_values(),
        **{
            PAYMENT: [None],
            f"{PAYMENT}/csdo:PaymentKindName": "Пошлина",
        },
    )
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    val055 = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert val055.is_valid
    # And verify no rule from MSG054 was executed for MSG055
    rule_ids = {iss.rule_id for iss in val055.issues}
    assert not any("MSG.054" in r for r in rule_ids)
