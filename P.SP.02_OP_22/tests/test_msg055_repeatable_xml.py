from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.loader import ProcessPackageLoader
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.055"
STRUCTURE_ID = "R.IP.SP.03.003"
PAYMENT = "ipcdo:IPPaymentDetails"
AUTHORITY = "ipcdo:PatentAuthorityDetails"


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


def _rules(code):
    engine = _engine()
    rule_id = f"{MESSAGE}.T73.REQ.{code}"
    return [
        r for r in engine.rules[MESSAGE].structured_rules
        if r["rule_id"] == rule_id or r["rule_id"].startswith(rule_id + ".")
    ]


def _eval(code, values):
    rules = _rules(code)
    assert rules, f"No rules for REQ.{code}"
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(r, values).status for r in rules]


def _assert_pass(code, values):
    statuses = _eval(code, values)
    assert all(s is RuleStatus.PASS for s in statuses), f"Expected PASS for REQ.{code}, got {statuses}"


def _assert_fail(code, values):
    statuses = _eval(code, values)
    assert RuleStatus.FAIL in statuses, f"Expected FAIL for REQ.{code}, got {statuses}"


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


# --- REQ 1, 2, 3: PatentAuthorityDetails tests ---

def test_req1_req2_req3_patent_authority_valid():
    values = {
        AUTHORITY: [{}],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": ["RU"],
        f"{AUTHORITY}/csdo:AuthorityName": ["Роспатент"],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails": [{}],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["2"],
    }
    _assert_pass(1, values)
    _assert_pass(2, values)
    _assert_pass(3, values)


def test_req1_req2_req3_patent_authority_failures():
    # Missing country code -> fails REQ 1
    val_no_country = {
        AUTHORITY: [{}],
        f"{AUTHORITY}/csdo:AuthorityName": ["Роспатент"],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails": [{}],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["2"],
    }
    _assert_fail(1, val_no_country)
    _assert_pass(2, val_no_country)
    _assert_pass(3, val_no_country)

    # Missing authority name -> fails REQ 2
    val_no_name = {
        AUTHORITY: [{}],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": ["RU"],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails": [{}],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["2"],
    }
    _assert_pass(1, val_no_name)
    _assert_fail(2, val_no_name)
    _assert_pass(3, val_no_name)

    # Missing address kind code -> fails REQ 3
    val_no_addr = {
        AUTHORITY: [{}],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": ["RU"],
        f"{AUTHORITY}/csdo:AuthorityName": ["Роспатент"],
    }
    _assert_pass(1, val_no_addr)
    _assert_pass(2, val_no_addr)
    _assert_fail(3, val_no_addr)

    # Wrong address kind code -> fails REQ 3
    val_wrong_addr = {
        AUTHORITY: [{}],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": ["RU"],
        f"{AUTHORITY}/csdo:AuthorityName": ["Роспатент"],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails": [{}],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["1"],
    }
    _assert_pass(1, val_wrong_addr)
    _assert_pass(2, val_wrong_addr)
    _assert_fail(3, val_wrong_addr)


# --- REQ 4, 5: Legal Action Kind tests ---

def test_req4_req5_legal_action_kind_code_present_name_absent():
    values = {
        "ccdo:EDocHeader": [{}],
        "ipsdo:IPLegalActionKindCode": "01",
    }
    _assert_pass(4, values)
    _assert_pass(5, values)


def test_req4_req5_legal_action_kind_code_absent_name_present():
    values = {
        "ccdo:EDocHeader": [{}],
        "ipsdo:IPLegalActionKindName": "Продление срока действия",
    }
    _assert_pass(4, values)
    _assert_pass(5, values)


def test_req4_req5_legal_action_kind_both_present_fails_req4():
    values = {
        "ccdo:EDocHeader": [{}],
        "ipsdo:IPLegalActionKindCode": "01",
        "ipsdo:IPLegalActionKindName": "Продление срока действия",
    }
    _assert_fail(4, values)
    _assert_pass(5, values)


def test_req4_req5_legal_action_kind_neither_present_fails_req5():
    values = {
        "ccdo:EDocHeader": [{}],
    }
    _assert_pass(4, values)
    _assert_fail(5, values)


# --- REQ 6: Trademark Application Id tests ---

def test_req6_trademark_application_id_presence():
    values_with_tm = {
        "ipsdo:TrademarkApplicationId": "2026/RU-000055",
    }
    _assert_pass(6, values_with_tm)

    values_without_tm = {}
    _assert_fail(6, values_without_tm)


# --- REQ 8, 9: IPPaymentDetails forbidden fields & repeatables ---

def test_req8_req9_zero_payment_passes():
    # If no payment details are present, for_each on IPPaymentDetails has 0 iterations
    values = {}
    _assert_pass(8, values)
    _assert_pass(9, values)


def test_req8_req9_clean_payment_passes():
    values = {
        PAYMENT: [{"csdo:PaymentKindName": "Пошлина за продление"}],
        f"{PAYMENT}/csdo:PaymentKindName": ["Пошлина за продление"],
    }
    _assert_pass(8, values)
    _assert_pass(9, values)


def test_req8_negative_forbidden_fields():
    # EventDateTime present under payment -> fails REQ 8, passes REQ 9
    v_event = {
        PAYMENT: [{"csdo:EventDateTime": "2026-09-30T12:00:00+03:00"}],
        f"{PAYMENT}/csdo:EventDateTime": ["2026-09-30T12:00:00+03:00"],
    }
    _assert_fail(8, v_event)
    _assert_pass(9, v_event)

    # IPPartyDetails present under payment -> fails REQ 8, passes REQ 9
    v_party = {
        PAYMENT: [{"ipcdo:IPPartyDetails": None}],
        f"{PAYMENT}/ipcdo:IPPartyDetails": [{}],
    }
    _assert_fail(8, v_party)
    _assert_pass(9, v_party)

    # AccompanyingDocumentsDetails present under payment -> fails REQ 8, passes REQ 9
    v_docs = {
        PAYMENT: [{"ipcdo:AccompanyingDocumentsDetails": None}],
        f"{PAYMENT}/ipcdo:AccompanyingDocumentsDetails": [{}],
    }
    _assert_fail(8, v_docs)
    _assert_pass(9, v_docs)


def test_req9_negative_forbidden_fields():
    # TrademarkApplicationId present under payment -> fails REQ 9, passes REQ 8
    v_tm = {
        PAYMENT: [{"ipsdo:TrademarkApplicationId": "2026/RU-000055"}],
        f"{PAYMENT}/ipsdo:TrademarkApplicationId": ["2026/RU-000055"],
    }
    _assert_pass(8, v_tm)
    _assert_fail(9, v_tm)

    # DocId present under payment -> fails REQ 9, passes REQ 8
    v_doc = {
        PAYMENT: [{"csdo:DocId": "DOC-123"}],
        f"{PAYMENT}/csdo:DocId": ["DOC-123"],
    }
    _assert_pass(8, v_doc)
    _assert_fail(9, v_doc)

    # PaymentAmount present under payment -> fails REQ 9, passes REQ 8
    v_amt = {
        PAYMENT: [{"csdo:PaymentAmount": "10000.00"}],
        f"{PAYMENT}/csdo:PaymentAmount": ["10000.00"],
    }
    _assert_pass(8, v_amt)
    _assert_fail(9, v_amt)

    # DutyPaymentIndicator present under payment -> fails REQ 9, passes REQ 8
    v_ind = {
        PAYMENT: [{"ipsdo:DutyPaymentIndicator": "true"}],
        f"{PAYMENT}/ipsdo:DutyPaymentIndicator": ["true"],
    }
    _assert_pass(8, v_ind)
    _assert_fail(9, v_ind)


def test_req8_req9_root_fields_do_not_leak_into_payment():
    # Root has DocId, PaymentAmount, DutyPaymentIndicator, TrademarkApplicationId
    # Payment is clean.
    # REQ 8 and REQ 9 must PASS! Root fields must NOT trigger REQ 9 failures!
    values = {
        "csdo:DocId": "ROOT-DOC-001",
        "csdo:PaymentAmount": "50000.00",
        "ipsdo:DutyPaymentIndicator": "true",
        "ipsdo:TrademarkApplicationId": "2026/RU-000055",
        PAYMENT: [{"csdo:PaymentKindName": "Госпошлина"}],
        f"{PAYMENT}/csdo:PaymentKindName": ["Госпошлина"],
    }
    _assert_pass(8, values)
    _assert_pass(9, values)


def test_req8_req9_repeatable_payments():
    # Two clean payments -> PASS
    clean_clean = {
        PAYMENT: [
            {"csdo:PaymentKindName": "Пошлина 1"},
            {"csdo:PaymentKindName": "Пошлина 2"},
        ],
        f"{PAYMENT}/csdo:PaymentKindName": ["Пошлина 1", "Пошлина 2"],
    }
    _assert_pass(8, clean_clean)
    _assert_pass(9, clean_clean)

    # Clean + Dirty (DocId in second) -> fails REQ 9
    clean_dirty = {
        PAYMENT: [
            {"csdo:PaymentKindName": "Пошлина 1"},
            {"csdo:DocId": "DIRTY-DOC"},
        ],
        f"{PAYMENT}/csdo:PaymentKindName": ["Пошлина 1", None],
        f"{PAYMENT}/csdo:DocId": [None, "DIRTY-DOC"],
    }
    _assert_pass(8, clean_dirty)
    _assert_fail(9, clean_dirty)

    # Dirty (EventDateTime in first) + Clean -> fails REQ 8
    dirty_clean = {
        PAYMENT: [
            {"csdo:EventDateTime": "2026-09-30T12:00:00+03:00"},
            {"csdo:PaymentKindName": "Пошлина 2"},
        ],
        f"{PAYMENT}/csdo:EventDateTime": ["2026-09-30T12:00:00+03:00", None],
        f"{PAYMENT}/csdo:PaymentKindName": [None, "Пошлина 2"],
    }
    _assert_fail(8, dirty_clean)
    _assert_pass(9, dirty_clean)


# --- Extraction from real XML elements ---

def test_xml_extraction_clean_payment():
    def build_xml(root, structure):
        pmt = _child(root, structure, "ipcdo", "IPPaymentDetails")
        _child(pmt, structure, "csdo", "PaymentKindName", text="Пошлина за продление")

    _, _, values, issues = _values_from_xml(build_xml)
    assert not issues
    _assert_pass(8, values)
    _assert_pass(9, values)


def test_xml_extraction_forbidden_payment_fields():
    # Under IPPaymentDetails, add csdo:PaymentAmount (forbidden in REQ 9) and csdo:EventDateTime (forbidden in REQ 8)
    def build_xml(root, structure):
        pmt = _child(root, structure, "ipcdo", "IPPaymentDetails")
        _child(pmt, structure, "csdo", "PaymentAmount", text="5000.00")
        _child(pmt, structure, "csdo", "EventDateTime", text="2026-09-30T15:30:00+03:00")

    _, _, values, issues = _values_from_xml(build_xml)
    assert not issues
    _assert_fail(8, values)
    _assert_fail(9, values)


def test_xml_extraction_root_and_payment_isolation():
    def build_xml(root, structure):
        _child(root, structure, "ipsdo", "TrademarkApplicationId", text="2026/RU-000055")
        _child(root, structure, "csdo", "DocId", text="ROOT-DOC-999")
        _child(root, structure, "csdo", "PaymentAmount", text="12345.00")
        _child(root, structure, "ipsdo", "DutyPaymentIndicator", text="true")

        pmt = _child(root, structure, "ipcdo", "IPPaymentDetails")
        _child(pmt, structure, "csdo", "PaymentKindName", text="Чистый платеж")

    _, _, values, issues = _values_from_xml(build_xml)
    assert not issues
    _assert_pass(6, values)
    _assert_pass(8, values)
    _assert_pass(9, values)
