from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.021"
STRUCTURE = "R.IP.SP.02.007"
P = "ipcdo:UnifiedRegisterRecordsDetails"
FALLBACK = "Заявление о продлении срока действия исключительного права на товарный знак, знак обслуживания Евразийского экономического союза"


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


def _parsed_values(builder):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues, [(i.code, i.field_path, i.message) for i in issues]
    return engine, values


def _inherited_rules(engine, item):
    return [
        rule
        for rule in engine.rules[MESSAGE].structured_rules
        if rule["rule_id"] == "P.SP.02.MSG.021.T54.REQ.6_19"
        and len(rule.get("source_refs", [])) == 2
        and rule["source_refs"][1].get("item") == str(item)
    ]


def _direct_rules(engine, item):
    return [r for r in engine.rules[MESSAGE].structured_rules if r["rule_id"] == f"P.SP.02.MSG.021.T54.REQ.{item}"]


def _statuses(rules, values):
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(rule, values).status for rule in rules]


def _assert_expected(rules, values, expected):
    statuses = _statuses(rules, values)
    assert statuses
    if expected is RuleStatus.PASS:
        assert all(status is RuleStatus.PASS for status in statuses)
    else:
        assert RuleStatus.FAIL in statuses


@pytest.mark.parametrize("bad_index,expected", [(None, RuleStatus.PASS), (0, RuleStatus.FAIL), (1, RuleStatus.FAIL)])
def test_unified_country_code_repeatable_good_bad_positions(bad_index, expected):
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        for index in range(2):
            authority = _child(record, structure, "ipcdo", "PatentAuthorityDetails")
            attrs = {"codeListId": "ВОИС ST.3"} if index != bad_index else {"codeListId": "WRONG"}
            _child(authority, structure, "csdo", "UnifiedCountryCode", "RU", attrs=attrs)

    engine, values = _parsed_values(build)
    _assert_expected(_inherited_rules(engine, 6), values, expected)


@pytest.mark.parametrize("bad_index,expected", [(None, RuleStatus.PASS), (0, RuleStatus.FAIL), (1, RuleStatus.FAIL)])
def test_subject_address_repeatable_good_bad_positions(bad_index, expected):
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        party = _child(record, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            address = _child(party, structure, "ccdo", "SubjectAddressDetails")
            _child(address, structure, "csdo", "AddressKindCode", "2")
            _child(address, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
            if index != bad_index:
                _child(address, structure, "csdo", "CityName", "Москва")
            _child(address, structure, "csdo", "StreetName", "Тестовая")
            _child(address, structure, "csdo", "BuildingNumberId", str(index + 1))

    engine, values = _parsed_values(build)
    _assert_expected(_inherited_rules(engine, 7), values, expected)


@pytest.mark.parametrize("bad_index,expected", [(None, RuleStatus.PASS), (0, RuleStatus.FAIL), (1, RuleStatus.FAIL)])
def test_communication_repeatable_good_bad_positions(bad_index, expected):
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        party = _child(record, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            comm = _child(party, structure, "ccdo", "CommunicationDetails")
            _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
            if index != bad_index:
                _child(comm, structure, "csdo", "CommunicationChannelId", f"u{index}@example.test")

    engine, values = _parsed_values(build)
    _assert_expected(_inherited_rules(engine, 8), values, expected)
    if expected is RuleStatus.PASS:
        _assert_expected(_inherited_rules(engine, 9), values, RuleStatus.PASS)


@pytest.mark.parametrize("bad_index,expected", [(None, RuleStatus.PASS), (0, RuleStatus.FAIL), (1, RuleStatus.FAIL)])
def test_ip_party_repeatable_good_bad_positions(bad_index, expected):
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        for index in range(2):
            party = _child(record, structure, "ipcdo", "IPPartyDetails")
            _child(party, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
            if index != bad_index:
                _child(party, structure, "ipsdo", "IPSubjectName", f"Party {index}")
            address = _child(party, structure, "ccdo", "SubjectAddressDetails")
            _child(address, structure, "csdo", "AddressKindCode", "2")
            _child(address, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
            _child(address, structure, "csdo", "CityName", "Москва")
            _child(address, structure, "csdo", "StreetName", "Тестовая")
            _child(address, structure, "csdo", "BuildingNumberId", str(index + 1))
            comm = _child(party, structure, "ccdo", "CommunicationDetails")
            _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
            _child(comm, structure, "csdo", "CommunicationChannelId", f"u{index}@example.test")

    engine, values = _parsed_values(build)
    _assert_expected(_inherited_rules(engine, 12), values, expected)


@pytest.mark.parametrize("bad_index,expected", [(None, RuleStatus.PASS), (0, RuleStatus.FAIL), (1, RuleStatus.FAIL)])
def test_tm_element_repeatable_good_bad_positions(bad_index, expected):
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        trademark = _child(record, structure, "ipcdo", "TrademarkDetails")
        desc = _child(trademark, structure, "ipcdo", "TMDescriptionDetails")
        _child(desc, structure, "csdo", "DescriptionText", "Описание")
        for index in range(2):
            element = _child(desc, structure, "ipcdo", "TMElementDetails")
            _child(element, structure, "ipsdo", "TrademarkCFECode", "01.01.01")
            if index != bad_index:
                _child(element, structure, "csdo", "DesignationName", f"TEST-{index}")
            localized = _child(element, structure, "ipsdo", "TMLocalizedName", f"TEST-{index}")
            localized.set("languageCode", "ru")
            _child(element, structure, "ipsdo", "TMTransliterationName", f"TEST-{index}")

    engine, values = _parsed_values(build)
    _assert_expected(_inherited_rules(engine, 15), values, expected)


@pytest.mark.parametrize("bad_index,expected", [(None, RuleStatus.PASS), (0, RuleStatus.FAIL), (1, RuleStatus.FAIL)])
def test_goods_repeatable_good_bad_positions(bad_index, expected):
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        for index in range(2):
            goods = _child(record, structure, "ipcdo", "GoodsBaseDetails")
            if index == bad_index:
                _child(goods, structure, "ipsdo", "TrademarkId", f"FORBIDDEN-{index}")

    engine, values = _parsed_values(build)
    _assert_expected(_inherited_rules(engine, 17), values, expected)


@pytest.mark.parametrize(
    "kinds,expected",
    [(["RH", "XX"], RuleStatus.PASS), (["XX", "RH"], RuleStatus.PASS), (["XX", "YY"], RuleStatus.FAIL), (["RH", "RH"], RuleStatus.FAIL)],
)
def test_req11_rh_exactly_one_is_order_independent(kinds, expected):
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        for kind in kinds:
            party = _child(record, structure, "ipcdo", "IPPartyDetails")
            _child(party, structure, "ipsdo", "IPPartyKindCode", kind)

    engine, values = _parsed_values(build)
    _assert_expected(_inherited_rules(engine, 11), values, expected)


def test_req21_counts_only_direct_doc_validity_date():
    def direct_only(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        _child(record, structure, "csdo", "DocValidityDate", "2036-09-24")

    def nested_only(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        doc = _child(record, structure, "ipcdo", "AccompanyingDocumentsDetails")
        _child(doc, structure, "csdo", "DocValidityDate", "2036-09-24")

    def direct_and_nested(root, structure):
        direct_only(root, structure)
        record = next(iter(root))
        doc = _child(record, structure, "ipcdo", "AccompanyingDocumentsDetails")
        _child(doc, structure, "csdo", "DocValidityDate", "2037-09-24")

    for builder, expected in ((direct_only, RuleStatus.PASS), (nested_only, RuleStatus.FAIL), (direct_and_nested, RuleStatus.PASS)):
        engine, values = _parsed_values(builder)
        rules = _direct_rules(engine, 21)
        _assert_expected(rules, values, expected)
        selected = StructuredRuleEvaluator().select(rules[0]["selector"], values)
        assert len(selected) == (1 if expected is RuleStatus.PASS else 0)


def test_req21_wrong_namespace_direct_looking_date_does_not_satisfy():
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        _child(record, structure, "csdo", "DocValidityDate", "2036-09-24", namespace="urn:wrong")

    engine, values = _parsed_values(build)
    _assert_expected(_direct_rules(engine, 21), values, RuleStatus.FAIL)


def test_direct_document_kind_rules_ignore_nested_qname_collisions():
    def direct_code_nested_name(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        _child(record, structure, "ipsdo", "IPDocKindCode", "12345")
        status = _child(record, structure, "ipcdo", "IPEntityStatusDetails")
        _child(status, structure, "ipsdo", "IPDocKindName", "NESTED")

    def nested_code_direct_fallback(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        _child(record, structure, "ipsdo", "IPDocKindName", FALLBACK)
        doc = _child(record, structure, "ipcdo", "AccompanyingDocumentsDetails")
        _child(doc, structure, "ipsdo", "IPDocKindCode", "99999")

    for builder in (direct_code_nested_name, nested_code_direct_fallback):
        engine, values = _parsed_values(builder)
        _assert_expected(_direct_rules(engine, 4), values, RuleStatus.PASS)
        _assert_expected(_direct_rules(engine, 5), values, RuleStatus.PASS)


def test_nested_document_name_cannot_satisfy_direct_fallback():
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        doc = _child(record, structure, "ipcdo", "AccompanyingDocumentsDetails")
        _child(doc, structure, "ipsdo", "IPDocKindName", FALLBACK)

    engine, values = _parsed_values(build)
    _assert_expected(_direct_rules(engine, 5), values, RuleStatus.FAIL)


def test_optional_qname_branches_are_not_implicitly_required():
    def build(root, structure):
        _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")

    engine, values = _parsed_values(build)
    for item in (6, 7, 8, 9, 10, 12, 13, 14, 15, 17):
        _assert_expected(_inherited_rules(engine, item), values, RuleStatus.PASS)
