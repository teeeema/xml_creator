from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.046"
TRANSACTION = "P.SP.02.TRN.041"
ROOT = "ipcdo:UnifiedRegisterRecordsDetails"
NATIONAL = f"{ROOT}/ipcdo:TrademarkNationalApplicationDetails"
STATUS = f"{ROOT}/ipcdo:IPEntityStatusDetails"
RESOURCE = f"{ROOT}/ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
SIG = f"{ROOT}/ipcdo:SignatureDetails"
OFFICER = f"{SIG}/ipcdo:OfficerDetails"
OFFICER_NAME = f"{OFFICER}/ccdo:FullNameDetails"
FALLBACK = (
    "Ходатайство о преобразовании аннулированной регистрации товарного знака, "
    "знака обслуживания Евразийского экономического союза в национальную заявку "
    "на регистрацию товарного знака, знака обслуживания"
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


def valid_values(engine=None):
    engine = engine or _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    values = _minimal_values(structure)
    values.update(
        {
            "ccdo:EDocHeader": [None],
            "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
            "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.007",
            "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000046",
            "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T15:00:00+03:00",
            ROOT: [None],
            f"{ROOT}/ipsdo:IPDocKindName": FALLBACK,
            f"{ROOT}/ipsdo:TrademarkId": "TM-046",
            NATIONAL: [""],
            f"{NATIONAL}/csdo:UnifiedCountryCode": "RU",
            f"{NATIONAL}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            f"{NATIONAL}/ipsdo:NationalApplicationId": "RU-046",
            f"{NATIONAL}/ipsdo:NationalApplicationReceiptDate": "2026-09-30",
            STATUS: [""],
            f"{STATUS}/csdo:StatusCode": "06",
            f"{STATUS}/csdo:EventDate": "2026-09-30",
            RESOURCE: [""],
            VALIDITY: [""],
            f"{VALIDITY}/csdo:EndDateTime": "2026-10-01T00:00:00+03:00",
            SIG: [""],
            f"{SIG}/csdo:DocCreationDate": "2026-09-30",
            OFFICER: [""],
            OFFICER_NAME: [""],
            f"{OFFICER_NAME}/csdo:FirstName": "Иван",
            f"{OFFICER_NAME}/csdo:LastName": "Иванов",
            f"{OFFICER}/csdo:PositionName": "Эксперт",
        }
    )
    values.pop(f"{ROOT}/ipsdo:IPDocKindCode", None)
    values.pop(f"{STATUS}/csdo:StatusCode/@codeListId", None)
    values.pop(f"{SIG}/ccdo:FullNameDetails", None)
    values.pop(f"{OFFICER}/ccdo:CommunicationDetails", None)
    return values


def _roundtrip():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    values = valid_values(engine)
    prevalidation = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert prevalidation.is_valid, [
        (item.code, item.rule_id, item.field_path, item.message)
        for item in prevalidation.issues
    ]
    body = engine.build_body(MESSAGE, values, mode=GenerationMode.TEST)
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    parsed = ET.fromstring(serialized)
    extracted, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues, [(item.code, item.field_path, item.message) for item in issues]
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    return engine, structure, parsed, extracted, validation


def test_msg046_build_serialize_parse_production_extract_validate_roundtrip():
    engine, structure, parsed, extracted, validation = _roundtrip()
    assert parsed.tag == (
        "{urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}"
        "TrademarkRegisterDetails"
    )
    assert structure.structure_id == "R.IP.SP.02.007"
    assert extracted[f"{ROOT}/ipsdo:TrademarkId"] == "TM-046"
    assert extracted[f"{STATUS}/csdo:StatusCode"] == "06"
    assert extracted[f"{VALIDITY}/csdo:EndDateTime"] == "2026-10-01T00:00:00+03:00"
    assert validation.is_valid, [
        (item.code, item.rule_id, item.field_path, item.message)
        for item in validation.issues
    ]
    assert validation.is_complete
    assert len(validation.rule_evaluations) == 12
    assert all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    assert all(item.rule_id.startswith(MESSAGE + ".T64.REQ.") for item in validation.rule_evaluations)


def test_e2e_req2_exact_fallback_name_is_enforced_when_code_absent():
    engine, _, _, extracted, _ = _roundtrip()
    invalid = dict(extracted)
    invalid[f"{ROOT}/ipsdo:IPDocKindName"] = ["WRONG"]
    validation = engine.validate_body(MESSAGE, invalid, mode=GenerationMode.TEST)
    assert not validation.is_valid
    assert any(item.rule_id == f"{MESSAGE}.T64.REQ.2" for item in validation.issues)


def test_e2e_req4_req5_req6_required_same_record_fields_have_negative_proof():
    engine, _, _, extracted, _ = _roundtrip()
    cases = [
        (4, f"{NATIONAL}/ipsdo:NationalApplicationId"),
        (5, f"{STATUS}/csdo:EventDate"),
        (6, f"{VALIDITY}/csdo:EndDateTime"),
    ]
    for code, path in cases:
        invalid = dict(extracted)
        invalid[path] = None
        validation = engine.validate_body(MESSAGE, invalid, mode=GenerationMode.TEST)
        assert not validation.is_valid, (code, path)
        assert any(
            item.rule_id
            and (
                item.rule_id == f"{MESSAGE}.T64.REQ.{code}"
                or item.rule_id.startswith(f"{MESSAGE}.T64.REQ.{code}.")
            )
            for item in validation.issues
        )


def test_e2e_req7_req8_mutual_exclusion_and_req9_officer_fields():
    engine, _, _, extracted, _ = _roundtrip()
    conflict = dict(extracted)
    conflict[f"{SIG}/ccdo:FullNameDetails"] = [{}]
    conflict[f"{SIG}/ccdo:FullNameDetails/csdo:FirstName"] = ["Анна"]
    conflict[f"{SIG}/ccdo:FullNameDetails/csdo:LastName"] = ["Петрова"]
    validation = engine.validate_body(MESSAGE, conflict, mode=GenerationMode.TEST)
    failed = {item.rule_id for item in validation.issues if item.rule_id}
    assert f"{MESSAGE}.T64.REQ.7.BRANCH" in failed
    assert f"{MESSAGE}.T64.REQ.8" in failed

    missing_position = dict(extracted)
    missing_position[f"{OFFICER}/csdo:PositionName"] = None
    validation = engine.validate_body(
        MESSAGE, missing_position, mode=GenerationMode.TEST
    )
    assert not validation.is_valid
    assert any(item.rule_id == f"{MESSAGE}.T64.REQ.9" for item in validation.issues)


def test_transaction_context_for_msg046_is_exact_trn041():
    engine = _engine()
    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.procedure_code == "P.SP.02.PRC.023"
    assert transaction.initiating_message == MESSAGE
    assert transaction.response_messages == ("P.SP.02.MSG.002",)
    assert transaction.initiating_operation == "P.SP.02.OPR.112"
    assert transaction.responding_operation == "P.SP.02.OPR.113"
    assert transaction.initiating_participant == "P.SP.02.ACT.001"
    assert transaction.responding_participant == "P.SP.02.ACT.002"
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(
        f"/{MESSAGE}"
    )


def test_same_r007_values_execute_only_requested_message_rules():
    engine, _, _, extracted, result046 = _roundtrip()
    ids046 = {item.rule_id for item in result046.rule_evaluations}
    assert ids046
    assert all(rule_id.startswith(MESSAGE + ".") for rule_id in ids046)

    result047 = engine.validate_body(
        "P.SP.02.MSG.047", extracted, mode=GenerationMode.TEST
    )
    ids047 = {item.rule_id for item in result047.rule_evaluations}
    assert ids047
    assert all(rule_id.startswith("P.SP.02.MSG.047.") for rule_id in ids047)
    assert ids046.isdisjoint(ids047)
