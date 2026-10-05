from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
STRUCTURE_ID = "R.IP.SP.02.002"
MESSAGES = ("P.SP.02.MSG.006", "P.SP.02.MSG.007", "P.SP.02.MSG.009", "P.SP.02.MSG.010")
APP = "ipcdo:TrademarkApplicationDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
PRIORITY = f"{APP}/ipcdo:TrademarkPriorityDetails"
DOC = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
NAMING = f"{APP}/ipcdo:NamingAbilityProofDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
NATIONAL = f"{APP}/ipcdo:TrademarkNationalApplicationDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"


def _engine() -> EaeuXmlEngine:
    return EaeuXmlEngine.load_process(PACKAGE)


def _child(parent, structure, prefix: str, name: str, text: str | None = None, **attrs):
    element = ET.SubElement(parent, ET.QName(structure.imported_namespaces[prefix], name), attrs)
    element.text = text
    return element


def _parsed_values(build_xml):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE_ID, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    build_xml(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    return engine, structure, values


def _rules_for_code(engine: EaeuXmlEngine, message: str, code: str):
    direct_id = f"{message}.REQ.{code}"
    result = []
    for rule in engine.rules[message].structured_rules:
        if rule["rule_id"] == direct_id:
            result.append(rule)
            continue
        refs = rule.get("source_refs", [])
        if len(refs) >= 2 and refs[1].get("item") == code:
            result.append(rule)
    return result


def _status(engine, values, message: str, code: str, *, kind: str | None = None):
    rules = _rules_for_code(engine, message, code)
    if kind is not None:
        rules = [rule for rule in rules if rule.get("kind") == kind]
    assert len(rules) == 1, (message, code, kind, rules)
    return StructuredRuleEvaluator().evaluate(rules[0], values).status


def _address(parent, structure, *, valid=True, kind="2", country="RU", code_list="ВОИС ST.3"):
    address = _child(parent, structure, "ccdo", "SubjectAddressDetails")
    _child(address, structure, "csdo", "AddressKindCode", kind)
    country_el = _child(address, structure, "csdo", "UnifiedCountryCode", country)
    country_el.set("codeListId", code_list)
    _child(address, structure, "csdo", "CityName", "Москва")
    _child(address, structure, "csdo", "StreetName", "Тестовая")
    if valid:
        _child(address, structure, "csdo", "BuildingNumberId", "1")
    return address


def _communication(parent, structure, *, code="EM", include_id=True):
    communication = _child(parent, structure, "ccdo", "CommunicationDetails")
    _child(communication, structure, "csdo", "CommunicationChannelCode", code)
    if include_id:
        _child(communication, structure, "csdo", "CommunicationChannelId", "test@example.test")
    return communication


def _party(app, structure, kind: str, *, complete=True):
    party = _child(app, structure, "ipcdo", "IPPartyDetails")
    _child(party, structure, "ipsdo", "IPPartyKindCode", kind)
    if complete:
        country = _child(party, structure, "csdo", "UnifiedCountryCode", "RU")
        country.set("codeListId", "ВОИС ST.3")
        _child(party, structure, "ipsdo", "IPSubjectName", f"Party {kind}")
        _address(party, structure)
        _communication(party, structure)
        if kind == "PA":
            _child(party, structure, "ipsdo", "PatentAttorneyId", "PA-1")
    return party


def _goods(app, structure, *, complete=True, suffix="0"):
    goods = _child(app, structure, "ipcdo", "GoodsBaseDetails")
    if complete:
        _child(goods, structure, "ipsdo", "GoodsClassCode", "01")
    _child(goods, structure, "ipsdo", "GoodsClassName", f"Class {suffix}")
    _child(goods, structure, "ipsdo", "GoodsName", f"Goods {suffix}")
    return goods


def _document(parent, structure, *, binary=True, doc_name=False, complete=True):
    doc = _child(parent, structure, "ipcdo", "AccompanyingDocumentsDetails")
    if not complete:
        return doc
    _child(doc, structure, "ipsdo", "IPDocKindCode", "DOC")
    if doc_name:
        _child(doc, structure, "csdo", "DocName", "Документ")
    _child(doc, structure, "csdo", "DocId", "DOC-1")
    _child(doc, structure, "csdo", "DocCreationDate", "2026-09-22")
    _child(doc, structure, "csdo", "DescriptionText", "Описание")
    _child(doc, structure, "csdo", "PageQuantity", "1")
    if binary:
        _child(doc, structure, "csdo", "DocBinaryText", "QQ==")
    return doc


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_inherited_country_attribute_alignment_real_xml(message, bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        party = _child(app, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            address = _child(party, structure, "ccdo", "SubjectAddressDetails")
            country = _child(address, structure, "csdo", "UnifiedCountryCode", "RU")
            country.set("codeListId", "WRONG" if index == bad_index else "ВОИС ST.3")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, message, "7") is RuleStatus.FAIL


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_inherited_repeatable_subject_addresses_real_xml(message, bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        party = _child(app, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            _address(party, structure, valid=index != bad_index)

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, message, "8") is RuleStatus.FAIL


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_inherited_repeatable_communications_real_xml(message, bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        party = _child(app, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            _communication(party, structure, include_id=index != bad_index)

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, message, "9") is RuleStatus.FAIL


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_inherited_repeatable_patent_authorities_real_xml(message, bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            authority = _child(app, structure, "ipcdo", "PatentAuthorityDetails")
            if index != bad_index:
                country = _child(authority, structure, "csdo", "UnifiedCountryCode", "RU")
                country.set("codeListId", "ВОИС ST.3")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, message, "11") is RuleStatus.FAIL


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize(("code", "bad_kind"), [("15", "AP"), ("21", "PA"), ("22", "RE")])
def test_inherited_filtered_parties_do_not_leak_real_xml(message, code, bad_kind) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for kind in ("AP", "PA", "RE"):
            _party(app, structure, kind, complete=kind != bad_kind)

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, message, code) is RuleStatus.FAIL


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_inherited_repeatable_correspondence_addresses_real_xml(message, bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        corr = _child(app, structure, "ipcdo", "CorrespondenceAddressDetails")
        for index in range(2):
            address = _child(corr, structure, "ccdo", "SubjectAddressDetails")
            _child(address, structure, "csdo", "AddressKindCode", "2" if index == bad_index else "3")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, message, "23") is RuleStatus.FAIL


@pytest.mark.parametrize("message", MESSAGES)
def test_inherited_repeatable_goods_good_good_real_xml(message) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _goods(app, structure, suffix="0")
        _goods(app, structure, suffix="1")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, message, "29", kind="for_each") is RuleStatus.PASS


@pytest.mark.parametrize("message", MESSAGES)
@pytest.mark.parametrize("bad_index", [0, 1])
def test_inherited_repeatable_goods_bad_in_either_order_real_xml(message, bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            _goods(app, structure, complete=index != bad_index, suffix=str(index))

    engine, _, values = _parsed_values(build)
    assert values[f"{GOODS}/ipsdo:GoodsClassCode"][bad_index] is None
    assert _status(engine, values, message, "29", kind="for_each") is RuleStatus.FAIL


@pytest.mark.parametrize("message", MESSAGES)
def test_wrong_namespace_does_not_satisfy_inherited_goods_field(message) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _goods(app, structure, suffix="0")
        second = _child(app, structure, "ipcdo", "GoodsBaseDetails")
        wrong = ET.SubElement(second, ET.QName("urn:wrong:namespace", "GoodsClassCode"))
        wrong.text = "01"
        _child(second, structure, "ipsdo", "GoodsClassName", "Class 1")
        _child(second, structure, "ipsdo", "GoodsName", "Goods 1")

    engine, _, values = _parsed_values(build)
    assert values[f"{GOODS}/ipsdo:GoodsClassCode"] == ["01", None]
    assert _status(engine, values, message, "29", kind="for_each") is RuleStatus.FAIL


@pytest.mark.parametrize("bad_nested", [False, True])
def test_msg006_req30_direct_and_nested_documents_keep_context(bad_nested) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _document(app, structure, complete=bad_nested)
        naming = _child(app, structure, "ipcdo", "NamingAbilityProofDetails")
        proof = _child(naming, structure, "ipcdo", "ProofDocTextDetails")
        _document(proof, structure, complete=not bad_nested)

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "P.SP.02.MSG.006", "30") is RuleStatus.FAIL


def test_msg006_req30_direct_and_nested_documents_both_good_pass() -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _document(app, structure)
        naming = _child(app, structure, "ipcdo", "NamingAbilityProofDetails")
        proof = _child(naming, structure, "ipcdo", "ProofDocTextDetails")
        _document(proof, structure)

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "P.SP.02.MSG.006", "30") is RuleStatus.PASS


@pytest.mark.parametrize(("count", "expected"), [(0, RuleStatus.FAIL), (1, RuleStatus.PASS), (2, RuleStatus.PASS)])
def test_msg006_req31_naming_ability_cardinality_real_xml(count, expected) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for _ in range(count):
            _child(app, structure, "ipcdo", "NamingAbilityProofDetails")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "P.SP.02.MSG.006", "31") is expected


@pytest.mark.parametrize(("count", "expected"), [(0, RuleStatus.FAIL), (1, RuleStatus.PASS), (2, RuleStatus.PASS)])
def test_msg007_req5_priority_cardinality_real_xml(count, expected) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for _ in range(count):
            _child(app, structure, "ipcdo", "TrademarkPriorityDetails")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "P.SP.02.MSG.007", "5") is expected


@pytest.mark.parametrize("code", ["30", "31"])
@pytest.mark.parametrize("bad_index", [0, 1])
def test_msg007_priority_partial_rules_reject_one_bad_instance(code, bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            priority = _child(app, structure, "ipcdo", "TrademarkPriorityDetails")
            if code != "31" or index != bad_index:
                _child(priority, structure, "ipsdo", "PriorityKindCode", "01")
            if code != "30" or index != bad_index:
                _child(priority, structure, "ipsdo", "PriorityDate", "2026-09-01")
                country = _child(priority, structure, "csdo", "UnifiedCountryCode", "RU")
                country.set("codeListId", "ВОИС ST.3")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "P.SP.02.MSG.007", code) is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_msg007_req32_repeatable_direct_documents_reject_one_bad(bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            _document(app, structure, binary=False, doc_name=True, complete=index != bad_index)

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "P.SP.02.MSG.007", "32") is RuleStatus.FAIL


@pytest.mark.parametrize(("message", "valid_code", "wrong_code"), [("P.SP.02.MSG.009", "21", "02"), ("P.SP.02.MSG.010", "02", "21")])
def test_status_rules_real_xml(message, valid_code, wrong_code) -> None:
    def build(root, structure, code, code_list=None):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        status = _child(app, structure, "ipcdo", "IPEntityStatusDetails")
        status_code = _child(status, structure, "csdo", "StatusCode", code)
        if code_list is not None:
            status_code.set("codeListId", code_list)

    engine, _, valid = _parsed_values(lambda r, s: build(r, s, valid_code))
    assert all(StructuredRuleEvaluator().evaluate(rule, valid).status is RuleStatus.PASS for rule in _rules_for_code(engine, message, "5"))
    engine, _, wrong = _parsed_values(lambda r, s: build(r, s, wrong_code))
    assert RuleStatus.FAIL in [StructuredRuleEvaluator().evaluate(rule, wrong).status for rule in _rules_for_code(engine, message, "5")]
    engine, _, attr = _parsed_values(lambda r, s: build(r, s, valid_code, "STATUS-LIST"))
    assert RuleStatus.FAIL in [StructuredRuleEvaluator().evaluate(rule, attr).status for rule in _rules_for_code(engine, message, "5")]


@pytest.mark.parametrize(("count", "expected"), [(0, RuleStatus.FAIL), (1, RuleStatus.PASS), (2, RuleStatus.PASS)])
def test_msg009_req30_national_application_cardinality_real_xml(count, expected) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for _ in range(count):
            _child(app, structure, "ipcdo", "TrademarkNationalApplicationDetails")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "P.SP.02.MSG.009", "30") is expected


def test_msg009_req32_requires_end_datetime_real_xml() -> None:
    def build(root, structure, include_end):
        resource = _child(root, structure, "ccdo", "ResourceItemStatusDetails")
        validity = _child(resource, structure, "ccdo", "ValidityPeriodDetails")
        if include_end:
            _child(validity, structure, "csdo", "EndDateTime", "2026-09-23T12:00:00+03:00")

    engine, _, valid = _parsed_values(lambda r, s: build(r, s, True))
    assert _status(engine, valid, "P.SP.02.MSG.009", "32") is RuleStatus.PASS
    engine, _, invalid = _parsed_values(lambda r, s: build(r, s, False))
    assert _status(engine, invalid, "P.SP.02.MSG.009", "32") is RuleStatus.FAIL


def test_msg010_req30_indicator_and_req32_end_datetime_real_xml() -> None:
    def indicator(root, structure, value):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        trademark = _child(app, structure, "ipcdo", "TrademarkDetails")
        _child(trademark, structure, "ipsdo", "CollectiveMarkIndicator", value)

    engine, _, zero = _parsed_values(lambda r, s: indicator(r, s, "0"))
    assert _status(engine, zero, "P.SP.02.MSG.010", "30") is RuleStatus.PASS
    engine, _, one = _parsed_values(lambda r, s: indicator(r, s, "1"))
    assert _status(engine, one, "P.SP.02.MSG.010", "30") is RuleStatus.FAIL

    def end_date(root, structure):
        resource = _child(root, structure, "ccdo", "ResourceItemStatusDetails")
        validity = _child(resource, structure, "ccdo", "ValidityPeriodDetails")
        _child(validity, structure, "csdo", "EndDateTime", "2026-09-23T12:00:00+03:00")

    engine, _, values = _parsed_values(end_date)
    assert _status(engine, values, "P.SP.02.MSG.010", "32") is RuleStatus.FAIL
