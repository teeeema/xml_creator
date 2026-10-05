from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.015"
STRUCTURE_ID = "R.IP.SP.02.007"
ROOT = "ipcdo:UnifiedRegisterRecordsDetails"
NAT_APP = f"{ROOT}/ipcdo:TrademarkNationalApplicationDetails"
STATUS = f"{ROOT}/ipcdo:IPEntityStatusDetails"
RESOURCE = f"{ROOT}/ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _rules(code, suffix=""):
    engine = _engine()
    rule_id = f"{MESSAGE}.T48.REQ.{code}{suffix}"
    return [
        r for r in engine.rules[MESSAGE].structured_rules
        if r["rule_id"] == rule_id or r["rule_id"].startswith(rule_id + ".")
    ]


def _eval(code, values, suffix=""):
    rules = _rules(code, suffix)
    assert rules, f"No rules for REQ.{code}{suffix}"
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(r, values).status for r in rules]


def _assert_pass(code, values, suffix=""):
    statuses = _eval(code, values, suffix)
    assert all(s is RuleStatus.PASS for s in statuses), f"Expected PASS for REQ.{code}{suffix}, got {statuses}"


def _assert_fail(code, values, suffix=""):
    statuses = _eval(code, values, suffix)
    assert RuleStatus.FAIL in statuses, f"Expected FAIL for REQ.{code}{suffix}, got {statuses}"


def _child(parent, structure, prefix, local, text=None, attrs=None):
    ns = structure.imported_namespaces[prefix]
    node = ET.SubElement(parent, ET.QName(ns, local))
    if text is not None:
        node.text = text
    for k, v in (attrs or {}).items():
        node.set(k, v)
    return node


def _values_from_xml(builder):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE_ID, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    return engine, structure, values, issues


def valid_record_values():
    return {
        ROOT: [{}],
        f"{ROOT}/ipsdo:TrademarkId": ["2026/RU-000015"],
        NAT_APP: [{}],
        f"{NAT_APP}/csdo:UnifiedCountryCode": ["RU"],
        f"{NAT_APP}/ipsdo:NationalApplicationId": ["NAT-001"],
        f"{NAT_APP}/ipsdo:NationalApplicationReceiptDate": ["2026-09-30"],
        STATUS: [{}],
        f"{STATUS}/csdo:StatusCode": ["06"],
        f"{STATUS}/csdo:EventDate": ["2026-09-30"],
        RESOURCE: [{}],
        VALIDITY: [{}],
        f"{VALIDITY}/csdo:EndDateTime": ["2026-10-01T14:00:00+03:00"],
    }


def test_valid_record_passes_all_executable_rules():
    v = valid_record_values()
    _assert_pass(3, v)
    _assert_pass(4, v)
    _assert_pass(5, v)
    _assert_pass(6, v)


def test_req3_trademark_id_negative():
    v = valid_record_values()
    del v[f"{ROOT}/ipsdo:TrademarkId"]
    _assert_fail(3, v)


def test_req4_national_application_presence_and_fields_negatives():
    # Missing container -> fails PRESENCE
    v_no_container = valid_record_values()
    del v_no_container[NAT_APP]
    _assert_fail(4, v_no_container, suffix=".PRESENCE")

    # Missing country code -> fails FIELDS
    v_no_country = valid_record_values()
    del v_no_country[f"{NAT_APP}/csdo:UnifiedCountryCode"]
    _assert_fail(4, v_no_country, suffix=".FIELDS")

    # Missing national application ID -> fails FIELDS
    v_no_nat_id = valid_record_values()
    del v_no_nat_id[f"{NAT_APP}/ipsdo:NationalApplicationId"]
    _assert_fail(4, v_no_nat_id, suffix=".FIELDS")

    # Missing national application receipt date -> fails FIELDS
    v_no_date = valid_record_values()
    del v_no_date[f"{NAT_APP}/ipsdo:NationalApplicationReceiptDate"]
    _assert_fail(4, v_no_date, suffix=".FIELDS")


def test_req5_status_details_negatives():
    # Missing container -> fails PRESENCE
    v_no_status = valid_record_values()
    del v_no_status[STATUS]
    _assert_fail(5, v_no_status, suffix=".PRESENCE")

    # Wrong StatusCode != "06" -> fails FIELDS
    v_wrong_status = valid_record_values()
    v_wrong_status[f"{STATUS}/csdo:StatusCode"] = ["05"]
    _assert_fail(5, v_wrong_status, suffix=".FIELDS")

    # Missing EventDate -> fails FIELDS
    v_no_event = valid_record_values()
    del v_no_event[f"{STATUS}/csdo:EventDate"]
    _assert_fail(5, v_no_event, suffix=".FIELDS")

    # codeListId present on StatusCode -> fails FIELDS
    v_with_codelist = valid_record_values()
    v_with_codelist[f"{STATUS}/csdo:StatusCode/@codeListId"] = ["1.0"]
    _assert_fail(5, v_with_codelist, suffix=".FIELDS")


def test_req6_end_date_time_negative():
    v = valid_record_values()
    del v[f"{VALIDITY}/csdo:EndDateTime"]
    _assert_fail(6, v)


def test_repeatable_records_isolation():
    # good + good -> PASS
    good_good = {
        ROOT: [{}, {}],
        f"{ROOT}/ipsdo:TrademarkId": ["TM-001", "TM-002"],
        NAT_APP: [{}, {}],
        f"{NAT_APP}/csdo:UnifiedCountryCode": ["RU", "BY"],
        f"{NAT_APP}/ipsdo:NationalApplicationId": ["NAT-001", "NAT-002"],
        f"{NAT_APP}/ipsdo:NationalApplicationReceiptDate": ["2026-09-30", "2026-09-30"],
        STATUS: [{}, {}],
        f"{STATUS}/csdo:StatusCode": ["06", "06"],
        f"{STATUS}/csdo:EventDate": ["2026-09-30", "2026-09-30"],
        RESOURCE: [{}, {}],
        VALIDITY: [{}, {}],
        f"{VALIDITY}/csdo:EndDateTime": ["2026-10-01T14:00:00+03:00", "2026-10-01T15:00:00+03:00"],
    }
    _assert_pass(3, good_good)
    _assert_pass(4, good_good)
    _assert_pass(5, good_good)
    _assert_pass(6, good_good)

    # good + bad (TrademarkId missing in 2nd) -> fails REQ 3
    good_bad_tm = dict(good_good, **{f"{ROOT}/ipsdo:TrademarkId": ["TM-001", None]})
    _assert_fail(3, good_bad_tm)

    # bad + good (TrademarkId missing in 1st) -> fails REQ 3
    bad_good_tm = dict(good_good, **{f"{ROOT}/ipsdo:TrademarkId": [None, "TM-002"]})
    _assert_fail(3, bad_good_tm)

    # good + bad (StatusCode 05 in 2nd) -> fails REQ 5.FIELDS
    good_bad_status = dict(good_good, **{f"{STATUS}/csdo:StatusCode": ["06", "05"]})
    _assert_fail(5, good_bad_status, suffix=".FIELDS")

    # bad + good (StatusCode 05 in 1st) -> fails REQ 5.FIELDS
    bad_good_status = dict(good_good, **{f"{STATUS}/csdo:StatusCode": ["05", "06"]})
    _assert_fail(5, bad_good_status, suffix=".FIELDS")

    # good + bad (EndDateTime missing in 2nd) -> fails REQ 6
    good_bad_end = dict(good_good, **{f"{VALIDITY}/csdo:EndDateTime": ["2026-10-01T14:00:00+03:00", None]})
    _assert_fail(6, good_bad_end)


def test_xml_extraction_valid_record():
    def build_xml(root, structure):
        rec = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        _child(rec, structure, "ipsdo", "TrademarkId", text="2026/RU-000015")

        nat = _child(rec, structure, "ipcdo", "TrademarkNationalApplicationDetails")
        _child(nat, structure, "csdo", "UnifiedCountryCode", text="RU")
        _child(nat, structure, "ipsdo", "NationalApplicationId", text="NAT-001")
        _child(nat, structure, "ipsdo", "NationalApplicationReceiptDate", text="2026-09-30")

        st = _child(rec, structure, "ipcdo", "IPEntityStatusDetails")
        _child(st, structure, "csdo", "StatusCode", text="06")
        _child(st, structure, "csdo", "EventDate", text="2026-09-30")

        res = _child(rec, structure, "ccdo", "ResourceItemStatusDetails")
        val = _child(res, structure, "ccdo", "ValidityPeriodDetails")
        _child(val, structure, "csdo", "EndDateTime", text="2026-10-01T14:00:00+03:00")

    _, _, values, issues = _values_from_xml(build_xml)
    assert not issues
    _assert_pass(3, values)
    _assert_pass(4, values)
    _assert_pass(5, values)
    _assert_pass(6, values)


def test_xml_extraction_negative_record():
    def build_xml(root, structure):
        rec = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        # Missing TrademarkId (fails REQ 3)
        # NationalApplicationDetails missing NationalApplicationReceiptDate (fails REQ 4.FIELDS)
        nat = _child(rec, structure, "ipcdo", "TrademarkNationalApplicationDetails")
        _child(nat, structure, "csdo", "UnifiedCountryCode", text="RU")
        _child(nat, structure, "ipsdo", "NationalApplicationId", text="NAT-001")

        # StatusCode 05 (fails REQ 5.FIELDS)
        st = _child(rec, structure, "ipcdo", "IPEntityStatusDetails")
        _child(st, structure, "csdo", "StatusCode", text="05")
        _child(st, structure, "csdo", "EventDate", text="2026-09-30")

        # Missing EndDateTime (fails REQ 6)

    _, _, values, issues = _values_from_xml(build_xml)
    assert not issues
    _assert_fail(3, values)
    _assert_fail(4, values, suffix=".FIELDS")
    _assert_fail(5, values, suffix=".FIELDS")
    _assert_fail(6, values)
