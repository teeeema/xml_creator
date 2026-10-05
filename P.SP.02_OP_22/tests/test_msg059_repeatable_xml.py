from pathlib import Path
from xml.etree import ElementTree as ET
import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.059"
APP = "ipcdo:TrademarkApplicationDetails"
APP_DOCS = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
REG = "ipcdo:UnifiedRegisterRecordsDetails"
REG_DOCS = f"{REG}/ipcdo:AccompanyingDocumentsDetails"


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


def _values_from_xml(structure_id, builder):
    engine = _engine()
    structure = engine.resolve_structure(structure_id, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    return engine, structure, values, issues


def _rules(engine, table, code):
    rid = f"{MESSAGE}.T{table}.REQ.{code}"
    return [r for r in engine.rules[MESSAGE].structured_rules if r["rule_id"] == rid]


def _statuses(engine, table, code, values):
    rules = _rules(engine, table, code)
    assert rules, (table, code)
    return [StructuredRuleEvaluator().evaluate(rule, values).status for rule in rules]


def _assert_pass(engine, table, code, values):
    statuses = _statuses(engine, table, code, values)
    assert all(status is RuleStatus.PASS for status in statuses), statuses


def _assert_fail(engine, table, code, values):
    statuses = _statuses(engine, table, code, values)
    assert RuleStatus.FAIL in statuses, statuses


def _build_r002_doc(
    app,
    structure,
    *,
    kind_code="07015",
    kind_name=None,
    doc_name="Doc Name",
    doc_id="DOC-123",
    doc_date="2026-09-30",
    doc_bin="dGVzdA==",
    media_type="pdf",
    wrong_ns_field=None,
):
    doc = _child(app, structure, "ipcdo", "AccompanyingDocumentsDetails")
    if kind_code is not None:
        _child(doc, structure, "ipsdo", "IPDocKindCode", kind_code)
    if kind_name is not None:
        _child(doc, structure, "ipsdo", "IPDocKindName", kind_name)
    if doc_name is not None:
        _child(doc, structure, "csdo", "DocName", doc_name)
    if doc_id is not None:
        ns = "urn:test:wrong:ns" if wrong_ns_field == "DocId" else None
        _child(doc, structure, "csdo", "DocId", doc_id, namespace=ns)
    if doc_date is not None:
        _child(doc, structure, "csdo", "DocCreationDate", doc_date)
    if doc_bin is not None:
        attrs = {"mediaTypeCode": media_type} if media_type is not None else {}
        _child(doc, structure, "csdo", "DocBinaryText", doc_bin, attrs=attrs)
    return doc


def _build_r007_doc(
    reg,
    structure,
    *,
    kind_code="07015",
    kind_name=None,
    doc_name="Doc Name",
    doc_id="DOC-123",
    doc_date="2026-09-30",
    doc_bin="dGVzdA==",
    media_type="pdf",
):
    doc = _child(reg, structure, "ipcdo", "AccompanyingDocumentsDetails")
    if kind_code is not None:
        _child(doc, structure, "ipsdo", "IPDocKindCode", kind_code)
    if kind_name is not None:
        _child(doc, structure, "ipsdo", "IPDocKindName", kind_name)
    if doc_name is not None:
        _child(doc, structure, "csdo", "DocName", doc_name)
    if doc_id is not None:
        _child(doc, structure, "csdo", "DocId", doc_id)
    if doc_date is not None:
        _child(doc, structure, "csdo", "DocCreationDate", doc_date)
    if doc_bin is not None:
        attrs = {"mediaTypeCode": media_type} if media_type is not None else {}
        _child(doc, structure, "csdo", "DocBinaryText", doc_bin, attrs=attrs)
    return doc


# ==============================================================================
# R.IP.SP.02.002 Repeatable XML & Alignment Tests
# ==============================================================================


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_r002_multiple_applications_trademark_application_id_isolation(bad_index):
    def build(root, structure):
        for index in range(2):
            app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
            if index != bad_index:
                _child(app, structure, "ipsdo", "TrademarkApplicationId", f"APP-{index + 1}")
            _build_r002_doc(app, structure)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.002", build)
    if bad_index is None:
        _assert_pass(engine, 78, 1, values)
    else:
        _assert_fail(engine, 78, 1, values)


@pytest.mark.parametrize("missing_doc_index", [0, 1])
def test_r002_multiple_applications_missing_accompanying_docs_fails(missing_doc_index):
    def build(root, structure):
        for index in range(2):
            app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
            _child(app, structure, "ipsdo", "TrademarkApplicationId", f"APP-{index + 1}")
            if index != missing_doc_index:
                _build_r002_doc(app, structure)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.002", build)
    _assert_fail(engine, 78, 2, values)


def test_r002_multiple_accompanying_documents_all_valid():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _child(app, structure, "ipsdo", "TrademarkApplicationId", "APP-001")
        _build_r002_doc(app, structure, kind_code="07015", kind_name=None, media_type="pdf")
        _build_r002_doc(app, structure, kind_code=None, kind_name="Копия устава", media_type="docx")

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.002", build)
    _assert_pass(engine, 78, 1, values)
    _assert_pass(engine, 78, 2, values)
    _assert_pass(engine, 78, 3, values)
    _assert_pass(engine, 78, 4, values)


@pytest.mark.parametrize("bad_doc_index", [0, 1])
def test_r002_second_document_invalid_fails_governed_parent(bad_doc_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _child(app, structure, "ipsdo", "TrademarkApplicationId", "APP-001")
        for index in range(2):
            if index == bad_doc_index:
                # Missing both IPDocKindCode and IPDocKindName
                _build_r002_doc(app, structure, kind_code=None, kind_name=None)
            else:
                _build_r002_doc(app, structure, kind_code="07015")

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.002", build)
    _assert_fail(engine, 78, 3, values)


@pytest.mark.parametrize("bad_doc_index", [0, 1])
def test_r002_bad_media_type_fails_for_each(bad_doc_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _child(app, structure, "ipsdo", "TrademarkApplicationId", "APP-001")
        for index in range(2):
            media = "exe" if index == bad_doc_index else "jpg"
            _build_r002_doc(app, structure, media_type=media)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.002", build)
    _assert_fail(engine, 78, 4, values)


def test_r002_reverse_physical_order_preserves_evaluation():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        # Reverse element order: doc first, then trademark app id
        _build_r002_doc(app, structure, kind_code="07015", media_type="png")
        _child(app, structure, "ipsdo", "TrademarkApplicationId", "APP-REV-01")

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.002", build)
    _assert_pass(engine, 78, 1, values)
    _assert_pass(engine, 78, 2, values)
    _assert_pass(engine, 78, 3, values)
    _assert_pass(engine, 78, 4, values)


def test_r002_wrong_namespace_element_does_not_satisfy_exact_qname():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _child(app, structure, "ipsdo", "TrademarkApplicationId", "APP-001")
        # DocId with wrong namespace
        _build_r002_doc(app, structure, wrong_ns_field="DocId")

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.002", build)
    _assert_fail(engine, 78, 3, values)


# ==============================================================================
# R.IP.SP.02.007 Repeatable XML & Alignment Tests
# ==============================================================================


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_r007_multiple_records_trademark_id_isolation(bad_index):
    def build(root, structure):
        for index in range(2):
            reg = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
            if index != bad_index:
                _child(reg, structure, "ipsdo", "TrademarkId", f"TM-{index + 1}")
            _build_r007_doc(reg, structure)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.007", build)
    if bad_index is None:
        _assert_pass(engine, 79, 1, values)
    else:
        _assert_fail(engine, 79, 1, values)


@pytest.mark.parametrize("missing_doc_index", [0, 1])
def test_r007_multiple_records_missing_accompanying_docs_fails(missing_doc_index):
    def build(root, structure):
        for index in range(2):
            reg = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
            _child(reg, structure, "ipsdo", "TrademarkId", f"TM-{index + 1}")
            if index != missing_doc_index:
                _build_r007_doc(reg, structure)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.007", build)
    _assert_fail(engine, 79, 2, values)


def test_r007_multiple_accompanying_documents_all_valid():
    def build(root, structure):
        reg = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        _child(reg, structure, "ipsdo", "TrademarkId", "TM-001")
        _build_r007_doc(reg, structure, kind_code="07015", kind_name=None, media_type="tiff")
        _build_r007_doc(reg, structure, kind_code=None, kind_name="Доверенность", media_type="pdf")

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.007", build)
    _assert_pass(engine, 79, 1, values)
    _assert_pass(engine, 79, 2, values)
    _assert_pass(engine, 79, 3, values)
    _assert_pass(engine, 79, 4, values)


@pytest.mark.parametrize("bad_doc_index", [0, 1])
def test_r007_second_document_invalid_fails_governed_parent(bad_doc_index):
    def build(root, structure):
        reg = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        _child(reg, structure, "ipsdo", "TrademarkId", "TM-001")
        for index in range(2):
            if index == bad_doc_index:
                _build_r007_doc(reg, structure, doc_name=None)
            else:
                _build_r007_doc(reg, structure)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.007", build)
    _assert_fail(engine, 79, 3, values)


@pytest.mark.parametrize("bad_doc_index", [0, 1])
def test_r007_bad_media_type_fails_for_each(bad_doc_index):
    def build(root, structure):
        reg = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        _child(reg, structure, "ipsdo", "TrademarkId", "TM-001")
        for index in range(2):
            media = "zip" if index == bad_doc_index else "pdf"
            _build_r007_doc(reg, structure, media_type=media)

    engine, _, values, _ = _values_from_xml("R.IP.SP.02.007", build)
    _assert_fail(engine, 79, 4, values)
