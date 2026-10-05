from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.046"
ROOT = "ipcdo:UnifiedRegisterRecordsDetails"
NATIONAL = f"{ROOT}/ipcdo:TrademarkNationalApplicationDetails"
STATUS = f"{ROOT}/ipcdo:IPEntityStatusDetails"
RESOURCE = f"{ROOT}/ccdo:ResourceItemStatusDetails"
SIG = f"{ROOT}/ipcdo:SignatureDetails"
OFFICER = f"{SIG}/ipcdo:OfficerDetails"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _child(parent, structure, prefix, local, text=None, attrs=None, namespace=None):
    ns = namespace if namespace is not None else structure.imported_namespaces[prefix]
    node = ET.SubElement(parent, ET.QName(ns, local))
    if text is not None:
        node.text = text
    for key, value in (attrs or {}).items():
        node.set(key, value)
    return node


def _direct(parent, structure, prefix, local):
    tag = f"{{{structure.imported_namespaces[prefix]}}}{local}"
    return next(node for node in list(parent) if node.tag == tag)


def _record(root, structure, index):
    record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
    _child(record, structure, "ipsdo", "TrademarkId", f"TM-046-{index}")

    national = _child(record, structure, "ipcdo", "TrademarkNationalApplicationDetails")
    _child(national, structure, "csdo", "UnifiedCountryCode", "RU")
    _child(national, structure, "ipsdo", "NationalApplicationId", f"RU-{index}")
    _child(national, structure, "ipsdo", "NationalApplicationReceiptDate", "2026-09-30")

    status = _child(record, structure, "ipcdo", "IPEntityStatusDetails")
    _child(status, structure, "csdo", "StatusCode", "06")
    _child(status, structure, "csdo", "EventDate", "2026-09-30")

    resource = _child(record, structure, "ccdo", "ResourceItemStatusDetails")
    validity = _child(resource, structure, "ccdo", "ValidityPeriodDetails")
    _child(validity, structure, "csdo", "EndDateTime", "2026-10-01T00:00:00+03:00")

    sig = _child(record, structure, "ipcdo", "SignatureDetails")
    officer = _child(sig, structure, "ipcdo", "OfficerDetails")
    full = _child(officer, structure, "ccdo", "FullNameDetails")
    _child(full, structure, "csdo", "FirstName", "Иван")
    _child(full, structure, "csdo", "LastName", "Иванов")
    _child(officer, structure, "csdo", "PositionName", "Эксперт")
    return record


def _two_record_values(mutator=None):
    engine = _engine()
    structure = engine.resolve_structure("R.IP.SP.02.007", mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    records = [_record(root, structure, index) for index in range(2)]
    if mutator is not None:
        mutator(records, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues, [(item.code, item.field_path, item.message) for item in issues]
    return engine, values


def _rules(engine, code):
    prefix = f"{MESSAGE}.T64.REQ.{code}"
    rules = [
        rule
        for rule in engine.rules[MESSAGE].structured_rules
        if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")
    ]
    assert rules
    return rules


def _statuses(engine, code, values):
    return [
        StructuredRuleEvaluator().evaluate(rule, values).status
        for rule in _rules(engine, code)
    ]


def _assert_pass(engine, code, values):
    statuses = _statuses(engine, code, values)
    assert all(status is RuleStatus.PASS for status in statuses), statuses


def _assert_fail(engine, code, values):
    statuses = _statuses(engine, code, values)
    assert RuleStatus.FAIL in statuses, statuses


def test_two_record_valid_production_xml_passes_req3_through_req9():
    engine, values = _two_record_values()
    assert values[f"{ROOT}/ipsdo:TrademarkId"] == ["TM-046-0", "TM-046-1"]
    for code in range(3, 10):
        _assert_pass(engine, code, values)


def test_req3_two_records_cannot_repair_missing_trademark_id():
    def mutate(records, structure):
        second = records[1]
        second.remove(_direct(second, structure, "ipsdo", "TrademarkId"))

    engine, values = _two_record_values(mutate)
    assert values[f"{ROOT}/ipsdo:TrademarkId"] == ["TM-046-0", None]
    _assert_fail(engine, 3, values)


def test_req4_two_records_cannot_repair_missing_national_application_field():
    def mutate(records, structure):
        national = _direct(records[1], structure, "ipcdo", "TrademarkNationalApplicationDetails")
        national.remove(_direct(national, structure, "ipsdo", "NationalApplicationId"))

    engine, values = _two_record_values(mutate)
    assert values[f"{NATIONAL}/ipsdo:NationalApplicationId"] == ["RU-0", None]
    _assert_fail(engine, 4, values)


def test_req5_two_records_cannot_repair_wrong_status_or_forbidden_codelist():
    def mutate(records, structure):
        status = _direct(records[1], structure, "ipcdo", "IPEntityStatusDetails")
        code = _direct(status, structure, "csdo", "StatusCode")
        code.text = "05"
        code.set("codeListId", "SHOULD-BE-ABSENT")

    engine, values = _two_record_values(mutate)
    assert values[f"{STATUS}/csdo:StatusCode"] == ["06", "05"]
    assert values[f"{STATUS}/csdo:StatusCode/@codeListId"] == [None, "SHOULD-BE-ABSENT"]
    _assert_fail(engine, 5, values)


def test_req6_two_records_cannot_repair_missing_end_datetime_and_start_is_not_required():
    def mutate(records, structure):
        resource = _direct(records[1], structure, "ccdo", "ResourceItemStatusDetails")
        validity = _direct(resource, structure, "ccdo", "ValidityPeriodDetails")
        validity.remove(_direct(validity, structure, "csdo", "EndDateTime"))

    engine, values = _two_record_values(mutate)
    end_path = f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:EndDateTime"
    assert values[end_path][0] == "2026-10-01T00:00:00+03:00"
    assert values[end_path][1] is None
    assert f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:StartDateTime" not in values
    _assert_fail(engine, 6, values)


def test_req7_two_records_keep_signature_branch_ownership():
    def separate_branches(records, structure):
        second_sig = _direct(records[1], structure, "ipcdo", "SignatureDetails")
        second_sig.remove(_direct(second_sig, structure, "ipcdo", "OfficerDetails"))
        full = _child(second_sig, structure, "ccdo", "FullNameDetails")
        _child(full, structure, "csdo", "FirstName", "Анна")
        _child(full, structure, "csdo", "LastName", "Петрова")

    engine, values = _two_record_values(separate_branches)
    assert values[f"{SIG}/ipcdo:OfficerDetails"] == ["", None]
    assert values[f"{SIG}/ccdo:FullNameDetails"] == [None, ""]
    _assert_pass(engine, 7, values)
    _assert_pass(engine, 8, values)

    def conflict(records, structure):
        second_sig = _direct(records[1], structure, "ipcdo", "SignatureDetails")
        full = _child(second_sig, structure, "ccdo", "FullNameDetails")
        _child(full, structure, "csdo", "FirstName", "Анна")
        _child(full, structure, "csdo", "LastName", "Петрова")

    engine, values = _two_record_values(conflict)
    _assert_fail(engine, 7, values)


def test_req8_two_records_reject_same_signature_mutual_exclusion_conflict():
    def mutate(records, structure):
        second_sig = _direct(records[1], structure, "ipcdo", "SignatureDetails")
        full = _child(second_sig, structure, "ccdo", "FullNameDetails")
        _child(full, structure, "csdo", "FirstName", "Анна")
        _child(full, structure, "csdo", "LastName", "Петрова")

    engine, values = _two_record_values(mutate)
    _assert_fail(engine, 8, values)


@pytest.mark.parametrize("field", ["FirstName", "LastName", "PositionName"])
def test_req9_two_records_cannot_repair_missing_officer_field(field):
    def mutate(records, structure):
        sig = _direct(records[1], structure, "ipcdo", "SignatureDetails")
        officer = _direct(sig, structure, "ipcdo", "OfficerDetails")
        if field == "PositionName":
            officer.remove(_direct(officer, structure, "csdo", field))
        else:
            full = _direct(officer, structure, "ccdo", "FullNameDetails")
            full.remove(_direct(full, structure, "csdo", field))

    engine, values = _two_record_values(mutate)
    _assert_fail(engine, 9, values)


def test_req9_forbidden_communication_is_scoped_to_officer_under_signature():
    def mutate(records, structure):
        sig = _direct(records[1], structure, "ipcdo", "SignatureDetails")
        officer = _direct(sig, structure, "ipcdo", "OfficerDetails")
        _child(officer, structure, "ccdo", "CommunicationDetails")

    engine, values = _two_record_values(mutate)
    assert values[f"{OFFICER}/ccdo:CommunicationDetails"] == [None, ""]
    _assert_fail(engine, 9, values)


def test_wrong_namespace_trademark_id_does_not_satisfy_exact_qname():
    def mutate(records, structure):
        second = records[1]
        second.remove(_direct(second, structure, "ipsdo", "TrademarkId"))
        _child(
            second,
            structure,
            "ipsdo",
            "TrademarkId",
            "WRONG-NS",
            namespace="urn:test:wrong:ipsdo",
        )

    engine, values = _two_record_values(mutate)
    assert values[f"{ROOT}/ipsdo:TrademarkId"] == ["TM-046-0", None]
    _assert_fail(engine, 3, values)
