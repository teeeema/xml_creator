from pathlib import Path
from xml.etree import ElementTree as ET
import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.059"
TRANSACTION = "P.SP.02.TRN.051"
R002 = "R.IP.SP.02.002"
R007 = "R.IP.SP.02.007"
APP = "ipcdo:TrademarkApplicationDetails"
R007_ROOT = "ipcdo:UnifiedRegisterRecordsDetails"


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
    _header(values, "", R002, "00000000-0000-0000-0000-000000000259")

    doc = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
    values.update(
        {
            APP: [None],
            f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
            doc: [None],
            f"{doc}/ipsdo:IPDocKindCode": "07015",
            f"{doc}/csdo:DocName": "Прилагаемый документ",
            f"{doc}/csdo:DocId": "DOC-059-001",
            f"{doc}/csdo:DocCreationDate": "2026-09-30",
            f"{doc}/csdo:DocBinaryText": "dGVzdA==",
            f"{doc}/csdo:DocBinaryText/@mediaTypeCode": "pdf",
            "ccdo:ResourceItemStatusDetails": [None],
            "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails": [None],
            "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime": "2026-09-30T12:00:00+03:00",
        }
    )
    return values


def _r007_values(structure):
    values = _minimal_values(structure)
    _header(values, "", R007, "00000000-0000-0000-0000-000000000759")

    root = R007_ROOT
    doc = f"{root}/ipcdo:AccompanyingDocumentsDetails"
    values.update(
        {
            root: [None],
            f"{root}/ipsdo:TrademarkId": "TM-059",
            doc: [None],
            f"{doc}/ipsdo:IPDocKindCode": "07015",
            f"{doc}/csdo:DocName": "Прилагаемый документ",
            f"{doc}/csdo:DocId": "DOC-059-002",
            f"{doc}/csdo:DocCreationDate": "2026-09-30",
            f"{doc}/csdo:DocBinaryText": "dGVzdA==",
            f"{doc}/csdo:DocBinaryText/@mediaTypeCode": "pdf",
            f"{root}/ccdo:ResourceItemStatusDetails": [None],
            f"{root}/ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails": [None],
            f"{root}/ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime": "2026-09-30T12:00:00+03:00",
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
            "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000059",
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
        (R002, 78, "{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails", 4),
        (R007, 79, "{urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}TrademarkRegisterDetails", 4),
    ],
)
def test_msg059_build_serialize_parse_extract_validate_for_each_embedded_branch(
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
    opposite = 79 if table == 78 else 78
    assert not any(f".T{opposite}." in item.rule_id for item in result.rule_evaluations)


def test_table77_one_of_rejects_neither_payload():
    engine = _engine()
    result = engine.validate_body(MESSAGE, _container_values(engine), mode=GenerationMode.TEST)
    assert not result.is_valid
    assert "EMBEDDED_STRUCTURE_CARDINALITY" in {issue.code for issue in result.issues}


def test_table77_one_of_rejects_both_allowed_payloads():
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
def test_table77_one_of_does_not_recognize_right_local_name_in_wrong_namespace(local_name, wrong_namespace):
    engine = _engine()
    fake = ET.Element(ET.QName(wrong_namespace, local_name))
    values = _container_values(engine)
    values["*"] = fake
    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert not result.is_valid
    assert "UNKNOWN_EMBEDDED_STRUCTURE" in {issue.code for issue in result.issues}


def test_transaction_context_for_msg059_is_trn051_opr186_to_opr187():
    engine = _engine()
    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.transaction_code == TRANSACTION
    assert transaction.procedure_code == "P.SP.02.PRC.036"
    assert transaction.initiating_message == "P.SP.02.MSG.058"
    assert MESSAGE in transaction.response_messages
    assert transaction.initiating_operation == "P.SP.02.OPR.186"
    assert transaction.responding_operation == "P.SP.02.OPR.187"


# ==============================================================================
# Production XML Negative Cases (Condition & Presence Rules)
# ==============================================================================


def test_r002_production_xml_missing_trademark_application_id_fails_rule():
    engine = _engine()
    _, _, payload = _build_payload(engine, R002)
    # Remove ipsdo:TrademarkApplicationId from payload
    app = payload.find(f"{{{engine.resolve_structure(R002, mode=GenerationMode.TEST).definition.imported_namespaces['ipcdo']}}}TrademarkApplicationDetails")
    target = app.find(f"{{{engine.resolve_structure(R002, mode=GenerationMode.TEST).definition.imported_namespaces['ipsdo']}}}TrademarkApplicationId")
    app.remove(target)

    values = _container_values(engine)
    values["*"] = payload
    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert not result.is_valid
    failed_rule_ids = {issue.rule_id for issue in result.issues if issue.rule_id}
    assert f"{MESSAGE}.T78.REQ.1" in failed_rule_ids


def test_r002_production_xml_missing_accompanying_docs_fails_rule():
    engine = _engine()
    _, _, payload = _build_payload(engine, R002)
    app = payload.find(f"{{{engine.resolve_structure(R002, mode=GenerationMode.TEST).definition.imported_namespaces['ipcdo']}}}TrademarkApplicationDetails")
    doc = app.find(f"{{{engine.resolve_structure(R002, mode=GenerationMode.TEST).definition.imported_namespaces['ipcdo']}}}AccompanyingDocumentsDetails")
    app.remove(doc)

    values = _container_values(engine)
    values["*"] = payload
    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert not result.is_valid
    failed_rule_ids = {issue.rule_id for issue in result.issues if issue.rule_id}
    assert f"{MESSAGE}.T78.REQ.2" in failed_rule_ids


def test_r002_production_xml_bad_media_type_code_fails_rule():
    engine = _engine()
    _, _, payload = _build_payload(engine, R002)
    app = payload.find(f"{{{engine.resolve_structure(R002, mode=GenerationMode.TEST).definition.imported_namespaces['ipcdo']}}}TrademarkApplicationDetails")
    doc = app.find(f"{{{engine.resolve_structure(R002, mode=GenerationMode.TEST).definition.imported_namespaces['ipcdo']}}}AccompanyingDocumentsDetails")
    bin_text = doc.find(f"{{{engine.resolve_structure(R002, mode=GenerationMode.TEST).definition.imported_namespaces['csdo']}}}DocBinaryText")
    bin_text.set("mediaTypeCode", "exe")

    values = _container_values(engine)
    values["*"] = payload
    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert not result.is_valid
    failed_rule_ids = {issue.rule_id for issue in result.issues if issue.rule_id}
    assert f"{MESSAGE}.T78.REQ.4" in failed_rule_ids


def test_r007_production_xml_missing_trademark_id_fails_rule():
    engine = _engine()
    _, _, payload = _build_payload(engine, R007)
    reg = payload.find(f"{{{engine.resolve_structure(R007, mode=GenerationMode.TEST).definition.imported_namespaces['ipcdo']}}}UnifiedRegisterRecordsDetails")
    tm_id = reg.find(f"{{{engine.resolve_structure(R007, mode=GenerationMode.TEST).definition.imported_namespaces['ipsdo']}}}TrademarkId")
    reg.remove(tm_id)

    values = _container_values(engine)
    values["*"] = payload
    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert not result.is_valid
    failed_rule_ids = {issue.rule_id for issue in result.issues if issue.rule_id}
    assert f"{MESSAGE}.T79.REQ.1" in failed_rule_ids


def test_r007_production_xml_bad_media_type_code_fails_rule():
    engine = _engine()
    _, _, payload = _build_payload(engine, R007)
    reg = payload.find(f"{{{engine.resolve_structure(R007, mode=GenerationMode.TEST).definition.imported_namespaces['ipcdo']}}}UnifiedRegisterRecordsDetails")
    doc = reg.find(f"{{{engine.resolve_structure(R007, mode=GenerationMode.TEST).definition.imported_namespaces['ipcdo']}}}AccompanyingDocumentsDetails")
    bin_text = doc.find(f"{{{engine.resolve_structure(R007, mode=GenerationMode.TEST).definition.imported_namespaces['csdo']}}}DocBinaryText")
    bin_text.set("mediaTypeCode", "zip")

    values = _container_values(engine)
    values["*"] = payload
    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert not result.is_valid
    failed_rule_ids = {issue.rule_id for issue in result.issues if issue.rule_id}
    assert f"{MESSAGE}.T79.REQ.4" in failed_rule_ids
