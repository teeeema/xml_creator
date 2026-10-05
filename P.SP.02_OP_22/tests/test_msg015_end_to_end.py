from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.015"
ROOT = "ipcdo:UnifiedRegisterRecordsDetails"
NAT = f"{ROOT}/ipcdo:TrademarkNationalApplicationDetails"
STATUS = f"{ROOT}/ipcdo:IPEntityStatusDetails"
RESOURCE = f"{ROOT}/ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.007",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000015",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        ROOT: [None],
        f"{ROOT}/ipsdo:TrademarkId": "2026/RU-000015",
        NAT: [""],
        f"{NAT}/csdo:UnifiedCountryCode": "RU",
        f"{NAT}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{NAT}/ipsdo:NationalApplicationId": "NAT-001",
        f"{NAT}/ipsdo:NationalApplicationReceiptDate": "2026-09-30",
        STATUS: [""],
        f"{STATUS}/csdo:StatusCode": "06",
        f"{STATUS}/csdo:EventDate": "2026-09-30",
        RESOURCE: [""],
        VALIDITY: [""],
        f"{VALIDITY}/csdo:EndDateTime": "2026-10-01T14:00:00+03:00",
    }


def test_build_serialize_parse_extract_validate_roundtrip():
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


def test_e2e_req3_trademark_id_negative():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    extracted_no_tm = dict(extracted)
    del extracted_no_tm[f"{ROOT}/ipsdo:TrademarkId"]
    val = engine.validate_body(MESSAGE, extracted_no_tm, mode=GenerationMode.TEST)
    assert not val.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T48.REQ.3" for iss in val.issues)


def test_e2e_req4_national_application_negatives():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Missing container
    extracted_no_nat = dict(extracted)
    del extracted_no_nat[NAT]
    del extracted_no_nat[f"{NAT}/csdo:UnifiedCountryCode"]
    del extracted_no_nat[f"{NAT}/ipsdo:NationalApplicationId"]
    del extracted_no_nat[f"{NAT}/ipsdo:NationalApplicationReceiptDate"]
    val_pres = engine.validate_body(MESSAGE, extracted_no_nat, mode=GenerationMode.TEST)
    assert not val_pres.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T48.REQ.4.PRESENCE" for iss in val_pres.issues)

    # Missing NationalApplicationId
    extracted_no_id = dict(extracted)
    del extracted_no_id[f"{NAT}/ipsdo:NationalApplicationId"]
    val_id = engine.validate_body(MESSAGE, extracted_no_id, mode=GenerationMode.TEST)
    assert not val_id.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T48.REQ.4.FIELDS" for iss in val_id.issues)

    # Missing UnifiedCountryCode
    extracted_no_cc = dict(extracted)
    del extracted_no_cc[f"{NAT}/csdo:UnifiedCountryCode"]
    val_cc = engine.validate_body(MESSAGE, extracted_no_cc, mode=GenerationMode.TEST)
    assert not val_cc.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T48.REQ.4.FIELDS" for iss in val_cc.issues)

    # Missing NationalApplicationReceiptDate
    extracted_no_date = dict(extracted)
    del extracted_no_date[f"{NAT}/ipsdo:NationalApplicationReceiptDate"]
    val_date = engine.validate_body(MESSAGE, extracted_no_date, mode=GenerationMode.TEST)
    assert not val_date.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T48.REQ.4.FIELDS" for iss in val_date.issues)


def test_e2e_req5_status_details_negatives():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Missing container
    extracted_no_status = dict(extracted)
    del extracted_no_status[STATUS]
    del extracted_no_status[f"{STATUS}/csdo:StatusCode"]
    del extracted_no_status[f"{STATUS}/csdo:EventDate"]
    val_pres = engine.validate_body(MESSAGE, extracted_no_status, mode=GenerationMode.TEST)
    assert not val_pres.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T48.REQ.5.PRESENCE" for iss in val_pres.issues)

    # StatusCode != "06"
    extracted_wrong_status = dict(extracted, **{f"{STATUS}/csdo:StatusCode": ["05"]})
    val_status = engine.validate_body(MESSAGE, extracted_wrong_status, mode=GenerationMode.TEST)
    assert not val_status.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T48.REQ.5.FIELDS" for iss in val_status.issues)

    # Missing EventDate
    extracted_no_event = dict(extracted)
    del extracted_no_event[f"{STATUS}/csdo:EventDate"]
    val_event = engine.validate_body(MESSAGE, extracted_no_event, mode=GenerationMode.TEST)
    assert not val_event.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T48.REQ.5.FIELDS" for iss in val_event.issues)

    # codeListId present on StatusCode
    extracted_with_codelist = dict(
        extracted,
        **{f"{STATUS}/csdo:StatusCode/@codeListId": ["1.0"]},
    )
    val_cl = engine.validate_body(MESSAGE, extracted_with_codelist, mode=GenerationMode.TEST)
    assert not val_cl.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T48.REQ.5.FIELDS" for iss in val_cl.issues)


def test_e2e_req6_end_date_time_negative():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    # Missing EndDateTime
    extracted_no_end = dict(extracted)
    del extracted_no_end[f"{VALIDITY}/csdo:EndDateTime"]
    val = engine.validate_body(MESSAGE, extracted_no_end, mode=GenerationMode.TEST)
    assert not val.is_valid
    assert any(iss.rule_id == f"{MESSAGE}.T48.REQ.6" for iss in val.issues)


def test_e2e_message_isolation():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    original = valid_values()
    body = engine.build_body(MESSAGE, original, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    extracted, _ = engine.body_provider._values_from_element(structure, parsed)

    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    assert validation.is_valid

    rule_ids = {iss.rule_id for iss in validation.issues}
    assert not any("MSG.046" in r for r in rule_ids)
    assert not any("MSG.016" in r for r in rule_ids)
