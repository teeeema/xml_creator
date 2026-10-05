from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.loader import ProcessPackageLoader
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.057"
STRUCTURE_ID = "R.IP.SP.03.003"
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


def _rules(code):
    engine = _engine()
    rule_id = f"{MESSAGE}.T75.REQ.{code}"
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
    ns = structure.imported_namespaces.get(prefix, structure.namespace)
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
        AUTHORITY: [None],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": ["RU"],
        f"{AUTHORITY}/csdo:AuthorityName": ["Роспатент"],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails": [""],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["2"],
    }
    _assert_pass(1, values)
    _assert_pass(2, values)
    _assert_pass(3, values)


def test_req1_req2_req3_patent_authority_failures():
    values_no_cc = {
        AUTHORITY: [None],
        f"{AUTHORITY}/csdo:AuthorityName": ["Роспатент"],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["2"],
    }
    _assert_fail(1, values_no_cc)

    values_no_name = {
        AUTHORITY: [None],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": ["RU"],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["2"],
    }
    _assert_fail(2, values_no_name)

    values_wrong_addr = {
        AUTHORITY: [None],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": ["RU"],
        f"{AUTHORITY}/csdo:AuthorityName": ["Роспатент"],
        f"{AUTHORITY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["1"],
    }
    _assert_fail(3, values_wrong_addr)


# --- REQ 6: TrademarkApplicationId ---

def test_req6_trademark_application_id():
    _assert_pass(6, {"ipsdo:TrademarkApplicationId": "2026/RU-000057"})
    _assert_fail(6, {})


# --- REQ 7, 8: IPPaymentDetails forbidden and required fields ---

def test_req7_req8_payment_details_clean():
    values = {
        PAYMENT: [""],
        f"{PAYMENT}/csdo:EventDateTime": ["2026-10-01T12:00:00Z"],
        PARTY: [""],
        DOC: [""],
    }
    _assert_pass(7, values)
    _assert_pass(8, values)


def test_req7_payment_forbidden_accounts():
    values_with_bank = {
        PAYMENT: [""],
        f"{PAYMENT}/ccdo:BankAccountDetails": [""],
        f"{PAYMENT}/csdo:EventDateTime": ["2026-10-01T12:00:00Z"],
        PARTY: [""],
        DOC: [""],
    }
    _assert_fail(7, values_with_bank)

    values_with_system = {
        PAYMENT: [""],
        f"{PAYMENT}/ccdo:PaymentSystemAccountDetails": [""],
        f"{PAYMENT}/csdo:EventDateTime": ["2026-10-01T12:00:00Z"],
        PARTY: [""],
        DOC: [""],
    }
    _assert_fail(7, values_with_system)


def test_req8_payment_missing_required_children():
    values_no_dt = {
        PAYMENT: [""],
        PARTY: [""],
        DOC: [""],
    }
    _assert_fail(8, values_no_dt)

    values_no_party = {
        PAYMENT: [""],
        f"{PAYMENT}/csdo:EventDateTime": ["2026-10-01T12:00:00Z"],
        DOC: [""],
    }
    _assert_fail(8, values_no_party)

    values_no_doc = {
        PAYMENT: [""],
        f"{PAYMENT}/csdo:EventDateTime": ["2026-10-01T12:00:00Z"],
        PARTY: [""],
    }
    _assert_fail(8, values_no_doc)


# --- REQ 9 to 14: IPPartyDetails tests ---

def test_req9_party_cardinality_and_kind():
    v_ap = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["AP"],
    }
    _assert_pass(9, v_ap)

    v_pa = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["PA"],
    }
    _assert_pass(9, v_pa)

    v_re = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["RE"],
    }
    _assert_pass(9, v_re)

    # 0 instances -> FAIL
    _assert_fail(9, {PARTY: []})

    # 2 instances -> FAIL
    v_two = {
        PARTY: [None, None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["AP", "PA"],
    }
    _assert_fail(9, v_two)

    # Invalid kind -> FAIL
    v_bad = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["XX"],
    }
    _assert_fail(9, v_bad)


def test_req10_party_required_fields():
    v_clean = {
        PARTY: [None],
        f"{PARTY}/csdo:UnifiedCountryCode": ["RU"],
        f"{PARTY}/ipsdo:IPSubjectName": ["ООО Ромашка"],
    }
    _assert_pass(10, v_clean)

    v_no_cc = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPSubjectName": ["ООО Ромашка"],
    }
    _assert_fail(10, v_no_cc)

    v_no_name = {
        PARTY: [None],
        f"{PARTY}/csdo:UnifiedCountryCode": ["RU"],
    }
    _assert_fail(10, v_no_name)


def test_req11_ap_subject_name_attributes():
    v_ap_valid = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["AP"],
        f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": ["OR"],
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": ["RU"],
    }
    _assert_pass(11, v_ap_valid)

    v_ap_bad_rep = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["AP"],
        f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": ["TR"],
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": ["RU"],
    }
    _assert_fail(11, v_ap_bad_rep)

    v_ap_bad_lang = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["AP"],
        f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": ["OR"],
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": ["EN"],
    }
    _assert_fail(11, v_ap_bad_lang)


def test_req12_pa_attorney_id():
    v_pa_valid = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["PA"],
        f"{PARTY}/ipsdo:PatentAttorneyId": ["12345"],
    }
    _assert_pass(12, v_pa_valid)

    v_pa_no_id = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["PA"],
    }
    _assert_fail(12, v_pa_no_id)

    # AP does not require attorney id
    v_ap = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["AP"],
    }
    _assert_pass(12, v_ap)


def test_req13_pa_re_country_code():
    for cc in ["AM", "BY", "KZ", "KG", "RU"]:
        v = {
            PARTY: [None],
            f"{PARTY}/ipsdo:IPPartyKindCode": ["PA"],
            f"{PARTY}/csdo:UnifiedCountryCode": [cc],
        }
        _assert_pass(13, v)

    v_foreign = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["PA"],
        f"{PARTY}/csdo:UnifiedCountryCode": ["US"],
    }
    _assert_fail(13, v_foreign)


def test_req14_pa_re_subject_name_attributes():
    v_valid = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["PA"],
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": ["RU"],
    }
    _assert_pass(14, v_valid)

    # nameRepresentationKindCode forbidden for PA/RE
    v_with_rep = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["PA"],
        f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": ["OR"],
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": ["RU"],
    }
    _assert_fail(14, v_with_rep)

    v_bad_lang = {
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["RE"],
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": ["EN"],
    }
    _assert_fail(14, v_bad_lang)


# --- REQ 15 to 19: AccompanyingDocumentsDetails tests ---

def test_req15_accompanying_docs_cardinality():
    _assert_pass(15, {DOC: [None]})
    _assert_fail(15, {DOC: []})
    _assert_fail(15, {DOC: [None, None]})


def test_req16_req17_req18_req19_accompanying_docs_valid():
    values = {
        DOC: [None],
        f"{DOC}/ipsdo:IPDocKindCode": ["07015"],
        f"{DOC}/csdo:DocId": ["DOC-001"],
        f"{DOC}/csdo:DocCreationDate": ["2026-10-01"],
        f"{DOC}/csdo:DocBinaryText": ["YmluYXJ5"],
        f"{DOC}/csdo:DocBinaryText/@mediaTypeCode": ["pdf"],
    }
    _assert_pass(16, values)
    _assert_pass(17, values)
    _assert_pass(18, values)
    _assert_pass(19, values)


def test_req16_doc_kind_name_forbidden():
    values = {
        DOC: [None],
        f"{DOC}/ipsdo:IPDocKindName": ["Платежка"],
    }
    _assert_fail(16, values)


def test_req17_doc_kind_code_value():
    _assert_pass(17, {DOC: [None], f"{DOC}/ipsdo:IPDocKindCode": ["07015"]})
    _assert_fail(17, {DOC: [None], f"{DOC}/ipsdo:IPDocKindCode": ["99999"]})


def test_req18_doc_id_and_date_required():
    _assert_fail(18, {DOC: [None], f"{DOC}/csdo:DocId": ["D1"]})
    _assert_fail(18, {DOC: [None], f"{DOC}/csdo:DocCreationDate": ["2026-10-01"]})


def test_req19_doc_binary_and_media_type():
    _assert_fail(19, {DOC: [None]})
    _assert_fail(19, {
        DOC: [None],
        f"{DOC}/csdo:DocBinaryText": ["bin"],
        f"{DOC}/csdo:DocBinaryText/@mediaTypeCode": ["exe"],
    })


# --- REQ 20, 21, 22: DutyPaymentIndicator & PaymentAmount tests ---

def test_req20_duty_payment_indicator_required():
    _assert_pass(20, {"ipsdo:DutyPaymentIndicator": "true"})
    _assert_pass(20, {"ipsdo:DutyPaymentIndicator": "false"})
    _assert_fail(20, {})


def test_req21_true_indicator_requires_zero_amount():
    # Indicator true, PaymentAmount "0" -> PASS
    v_clean = {
        "ccdo:EDocHeader": [None],
        "ipsdo:DutyPaymentIndicator": "true",
        "csdo:PaymentAmount": "0",
    }
    _assert_pass(21, v_clean)

    # Indicator true, PaymentAmount "100" -> FAIL
    v_nonzero = {
        "ccdo:EDocHeader": [None],
        "ipsdo:DutyPaymentIndicator": "true",
        "csdo:PaymentAmount": "100",
    }
    _assert_fail(21, v_nonzero)

    # Indicator true, PaymentAmount missing -> FAIL
    v_missing = {
        "ccdo:EDocHeader": [None],
        "ipsdo:DutyPaymentIndicator": "true",
    }
    _assert_fail(21, v_missing)

    # Indicator false -> REQ 21 does not fail even if PaymentAmount is "100"
    v_false = {
        "ccdo:EDocHeader": [None],
        "ipsdo:DutyPaymentIndicator": "false",
        "csdo:PaymentAmount": "100",
    }
    _assert_pass(21, v_false)


def test_req22_false_indicator_requires_amount_presence():
    # Indicator false, PaymentAmount present -> PASS
    v_clean = {
        "ccdo:EDocHeader": [None],
        "ipsdo:DutyPaymentIndicator": "false",
        "csdo:PaymentAmount": "100",
    }
    _assert_pass(22, v_clean)

    # Indicator false, PaymentAmount missing -> FAIL
    v_missing = {
        "ccdo:EDocHeader": [None],
        "ipsdo:DutyPaymentIndicator": "false",
    }
    _assert_fail(22, v_missing)

    # Indicator true, PaymentAmount missing -> REQ 22 does not fail
    v_true_no_amount = {
        "ccdo:EDocHeader": [None],
        "ipsdo:DutyPaymentIndicator": "true",
    }
    _assert_pass(22, v_true_no_amount)


# --- Full XML extraction roundtrip tests ---

def test_xml_builder_full_valid_case_true_indicator():
    def build(root, structure):
        hdr = _child(root, structure, "ccdo", "EDocHeader")
        _child(hdr, structure, "csdo", "InfEnvelopeCode", text=MESSAGE)
        _child(hdr, structure, "csdo", "EDocCode", text="R.IP.SP.03.003")
        _child(hdr, structure, "csdo", "EDocId", text="00000000-0000-0000-0000-000000000057")
        _child(hdr, structure, "csdo", "EDocDateTime", text="2026-10-01T12:00:00Z")

        auth = _child(root, structure, "ipcdo", "PatentAuthorityDetails")
        _child(auth, structure, "csdo", "UnifiedCountryCode", text="RU", attrs={"codeListId": "ВОИС ST.3"})
        _child(auth, structure, "csdo", "AuthorityName", text="Роспатент")
        _child(auth, structure, "ipsdo", "OriginOfficeIndicator", text="1")
        addr = _child(auth, structure, "ccdo", "SubjectAddressDetails")
        _child(addr, structure, "csdo", "AddressKindCode", text="2")

        _child(root, structure, "ipsdo", "TrademarkApplicationId", text="2026/RU-000057")

        pmt = _child(root, structure, "ipcdo", "IPPaymentDetails")
        _child(pmt, structure, "csdo", "EventDateTime", text="2026-10-01T12:00:00Z")

        party = _child(pmt, structure, "ipcdo", "IPPartyDetails")
        _child(party, structure, "ipsdo", "IPPartyKindCode", text="AP")
        _child(party, structure, "csdo", "UnifiedCountryCode", text="RU", attrs={"codeListId": "ВОИС ST.3"})
        _child(party, structure, "ipsdo", "IPSubjectName", text="Заявитель", attrs={
            "nameRepresentationKindCode": "OR",
            "languageCode": "RU",
        })

        doc = _child(pmt, structure, "ipcdo", "AccompanyingDocumentsDetails")
        _child(doc, structure, "ipsdo", "IPDocKindCode", text="07015")
        _child(doc, structure, "csdo", "DocId", text="DOC-57")
        _child(doc, structure, "csdo", "DocCreationDate", text="2026-10-01")
        _child(doc, structure, "csdo", "DocBinaryText", text="AQID", attrs={"mediaTypeCode": "pdf"})

        _child(root, structure, "ipsdo", "DutyPaymentIndicator", text="true")
        _child(root, structure, "csdo", "PaymentAmount", text="0", attrs={"currencyCode": "RUB"})

    engine, structure, values, issues = _values_from_xml(build)
    assert not issues, f"Extraction issues: {issues}"
    res = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert res.is_valid, [(i.rule_id, i.message) for i in res.issues]


def test_xml_builder_full_valid_case_false_indicator():
    def build(root, structure):
        hdr = _child(root, structure, "ccdo", "EDocHeader")
        _child(hdr, structure, "csdo", "InfEnvelopeCode", text=MESSAGE)
        _child(hdr, structure, "csdo", "EDocCode", text="R.IP.SP.03.003")
        _child(hdr, structure, "csdo", "EDocId", text="00000000-0000-0000-0000-000000000057")
        _child(hdr, structure, "csdo", "EDocDateTime", text="2026-10-01T12:00:00Z")

        auth = _child(root, structure, "ipcdo", "PatentAuthorityDetails")
        _child(auth, structure, "csdo", "UnifiedCountryCode", text="RU", attrs={"codeListId": "ВОИС ST.3"})
        _child(auth, structure, "csdo", "AuthorityName", text="Роспатент")
        _child(auth, structure, "ipsdo", "OriginOfficeIndicator", text="1")
        addr = _child(auth, structure, "ccdo", "SubjectAddressDetails")
        _child(addr, structure, "csdo", "AddressKindCode", text="2")

        _child(root, structure, "ipsdo", "TrademarkApplicationId", text="2026/RU-000057")

        pmt = _child(root, structure, "ipcdo", "IPPaymentDetails")
        _child(pmt, structure, "csdo", "EventDateTime", text="2026-10-01T12:00:00Z")

        party = _child(pmt, structure, "ipcdo", "IPPartyDetails")
        _child(party, structure, "ipsdo", "IPPartyKindCode", text="PA")
        _child(party, structure, "ipsdo", "PatentAttorneyId", text="PA-999")
        _child(party, structure, "csdo", "UnifiedCountryCode", text="RU", attrs={"codeListId": "ВОИС ST.3"})
        _child(party, structure, "ipsdo", "IPSubjectName", text="Патентный поверенный", attrs={
            "languageCode": "RU",
        })

        doc = _child(pmt, structure, "ipcdo", "AccompanyingDocumentsDetails")
        _child(doc, structure, "ipsdo", "IPDocKindCode", text="07015")
        _child(doc, structure, "csdo", "DocId", text="DOC-57-PA")
        _child(doc, structure, "csdo", "DocCreationDate", text="2026-10-01")
        _child(doc, structure, "csdo", "DocBinaryText", text="AQID", attrs={"mediaTypeCode": "pdf"})

        _child(root, structure, "ipsdo", "DutyPaymentIndicator", text="false")
        _child(root, structure, "csdo", "PaymentAmount", text="15000.00", attrs={"currencyCode": "RUB"})

    engine, structure, values, issues = _values_from_xml(build)
    assert not issues, f"Extraction issues: {issues}"
    res = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert res.is_valid, [(i.rule_id, i.message) for i in res.issues]
