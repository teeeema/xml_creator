from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.004"
STRUCTURE_ID = "R.IP.SP.02.002"
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
PATENT = f"{APP}/ipcdo:PatentAuthorityDetails"
CORR_ADDR = f"{APP}/ipcdo:CorrespondenceAddressDetails/ccdo:SubjectAddressDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
DOC = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"


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
    serialized = ET.tostring(root, encoding="utf-8")
    parsed = ET.fromstring(serialized)
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    return engine, structure, values


def _rules_for_code(engine: EaeuXmlEngine, code: str):
    direct_id = f"{MESSAGE}.REQ.{code}"
    result = []
    for rule in engine.rules[MESSAGE].structured_rules:
        if rule["rule_id"] == direct_id:
            result.append(rule)
            continue
        refs = rule.get("source_refs", [])
        if len(refs) >= 2 and refs[1].get("item") == code:
            result.append(rule)
    return result


def _status(engine, values, code: str, *, kind: str | None = None, collection: str | None = None):
    rules = _rules_for_code(engine, code)
    if kind is not None:
        rules = [rule for rule in rules if rule.get("kind") == kind]
    if collection is not None:
        rules = [rule for rule in rules if rule.get("selector", {}).get("collection") == collection]
    assert len(rules) == 1, (code, kind, collection, rules)
    return StructuredRuleEvaluator().evaluate(rules[0], values).status


def _address(parent, structure, *, valid=True, country="RU", code_list="ВОИС ST.3"):
    address = _child(parent, structure, "ccdo", "SubjectAddressDetails")
    _child(address, structure, "csdo", "AddressKindCode", "2")
    country_el = _child(address, structure, "csdo", "UnifiedCountryCode", country)
    country_el.set("codeListId", code_list)
    _child(address, structure, "csdo", "CityName", "Москва")
    _child(address, structure, "csdo", "StreetName", "Тестовая")
    if valid:
        _child(address, structure, "csdo", "BuildingNumberId", "1")
    return address


def _communication(parent, structure, *, code="EM", include_id=True):
    comm = _child(parent, structure, "ccdo", "CommunicationDetails")
    _child(comm, structure, "csdo", "CommunicationChannelCode", code)
    if include_id:
        _child(comm, structure, "csdo", "CommunicationChannelId", "test@example.test")
    return comm


@pytest.mark.parametrize(
    ("codes", "expected"),
    [
        (("ВОИС ST.3", "ВОИС ST.3"), RuleStatus.PASS),
        (("ВОИС ST.3", "WRONG"), RuleStatus.FAIL),
        (("WRONG", "ВОИС ST.3"), RuleStatus.FAIL),
    ],
)
def test_req7_repeatable_country_attribute_alignment(codes, expected) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        party = _child(app, structure, "ipcdo", "IPPartyDetails")
        for index, code_list in enumerate(codes):
            address = _child(party, structure, "ccdo", "SubjectAddressDetails")
            country = _child(address, structure, "csdo", "UnifiedCountryCode", "RU")
            country.set("codeListId", code_list)

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "7") is expected


@pytest.mark.parametrize("bad_index", [0, 1])
def test_req8_repeatable_addresses_reject_one_incomplete_in_both_orders(bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        party = _child(app, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            _address(party, structure, valid=index != bad_index)

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "8") is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_req9_repeatable_communications_reject_one_missing_channel_id(bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        party = _child(app, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            _communication(party, structure, include_id=index != bad_index)

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "9") is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_req10_repeatable_communications_reject_one_invalid_code(bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        party = _child(app, structure, "ipcdo", "IPPartyDetails")
        for index in range(2):
            _communication(party, structure, code="XX" if index == bad_index else "EM")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "10") is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_req11_repeatable_patent_authorities_reject_one_missing_country(bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            authority = _child(app, structure, "ipcdo", "PatentAuthorityDetails")
            if index != bad_index:
                country = _child(authority, structure, "csdo", "UnifiedCountryCode", "RU")
                country.set("codeListId", "ВОИС ST.3")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "11") is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_req12_repeatable_patent_authorities_reject_one_wrong_address_kind(bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            authority = _child(app, structure, "ipcdo", "PatentAuthorityDetails")
            _child(authority, structure, "csdo", "AuthorityName", f"Ведомство {index}")
            address = _child(authority, structure, "ccdo", "SubjectAddressDetails")
            _child(address, structure, "csdo", "AddressKindCode", "3" if index == bad_index else "2")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "12") is RuleStatus.FAIL


def _party(parent, structure, kind: str, *, complete=True):
    party = _child(parent, structure, "ipcdo", "IPPartyDetails")
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


@pytest.mark.parametrize(("code", "bad_kind"), [("15", "AP"), ("21", "PA"), ("22", "RE")])
def test_req15_21_22_party_instances_do_not_leak_values(code, bad_kind) -> None:
    def valid_build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for kind in ("AP", "PA", "RE"):
            _party(app, structure, kind, complete=True)

    engine, _, valid = _parsed_values(valid_build)
    assert _status(engine, valid, code) is RuleStatus.PASS

    def invalid_build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for kind in ("AP", "PA", "RE"):
            _party(app, structure, kind, complete=kind != bad_kind)

    engine, _, invalid = _parsed_values(invalid_build)
    assert _status(engine, invalid, code) is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_req23_repeatable_correspondence_addresses_reject_wrong_kind(bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        corr = _child(app, structure, "ipcdo", "CorrespondenceAddressDetails")
        for index in range(2):
            address = _child(corr, structure, "ccdo", "SubjectAddressDetails")
            _child(address, structure, "csdo", "AddressKindCode", "2" if index == bad_index else "3")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "23") is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [0, 1])
def test_req24_repeatable_correspondence_addresses_reject_non_eaeu_country(bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        corr = _child(app, structure, "ipcdo", "CorrespondenceAddressDetails")
        for index in range(2):
            address = _child(corr, structure, "ccdo", "SubjectAddressDetails")
            _child(address, structure, "csdo", "UnifiedCountryCode", "US" if index == bad_index else "RU")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "24") is RuleStatus.FAIL


def _goods(app, structure, *, complete=True, suffix="0"):
    goods = _child(app, structure, "ipcdo", "GoodsBaseDetails")
    if complete:
        _child(goods, structure, "ipsdo", "GoodsClassCode", "01")
    _child(goods, structure, "ipsdo", "GoodsClassName", f"Class {suffix}")
    _child(goods, structure, "ipsdo", "GoodsName", f"Goods {suffix}")
    return goods


def test_req29_repeatable_goods_good_good_passes() -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _goods(app, structure, complete=True, suffix="0")
        _goods(app, structure, complete=True, suffix="1")

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "29", kind="for_each") is RuleStatus.PASS


@pytest.mark.parametrize("bad_index", [0, 1])
def test_req29_repeatable_goods_reject_one_bad_in_both_orders(bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            _goods(app, structure, complete=index != bad_index, suffix=str(index))

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "29", kind="for_each") is RuleStatus.FAIL


def _doc(parent, structure, *, complete=True, suffix="0"):
    doc = _child(parent, structure, "ipcdo", "AccompanyingDocumentsDetails")
    _child(doc, structure, "ipsdo", "IPDocKindName", "Приложение")
    _child(doc, structure, "csdo", "DocId", f"DOC-{suffix}")
    _child(doc, structure, "csdo", "DocCreationDate", "2026-09-18")
    _child(doc, structure, "csdo", "DescriptionText", "Описание")
    if complete:
        _child(doc, structure, "csdo", "PageQuantity", "1")
    return doc


@pytest.mark.parametrize("bad_index", [0, 1])
def test_req30_repeatable_direct_documents_reject_one_bad_in_both_orders(bad_index) -> None:
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for index in range(2):
            _doc(app, structure, complete=index != bad_index, suffix=str(index))

    engine, _, values = _parsed_values(build)
    assert _status(engine, values, "30") is RuleStatus.FAIL


def test_req30_nested_document_does_not_satisfy_or_pollute_direct_scope() -> None:
    def nested_only(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        proof = _child(app, structure, "ipcdo", "NamingAbilityProofDetails")
        proof_text = _child(proof, structure, "ipcdo", "ProofDocTextDetails")
        _doc(proof_text, structure, complete=False, suffix="nested")

    engine, _, nested_values = _parsed_values(nested_only)
    assert _status(engine, nested_values, "30") is RuleStatus.PASS

    def direct_bad_nested_good(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _doc(app, structure, complete=False, suffix="direct")
        proof = _child(app, structure, "ipcdo", "NamingAbilityProofDetails")
        proof_text = _child(proof, structure, "ipcdo", "ProofDocTextDetails")
        _doc(proof_text, structure, complete=True, suffix="nested")

    engine, _, mixed_values = _parsed_values(direct_bad_nested_good)
    assert _status(engine, mixed_values, "30") is RuleStatus.FAIL


def test_req35_real_status_code_attribute_is_forbidden() -> None:
    def build(root, structure, with_attribute: bool):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        status = _child(app, structure, "ipcdo", "IPEntityStatusDetails")
        _child(status, structure, "csdo", "EventDate", "2026-09-18")
        code = _child(status, structure, "csdo", "StatusCode", "02")
        if with_attribute:
            code.set("codeListId", "TEST")

    engine, _, valid = _parsed_values(lambda root, structure: build(root, structure, False))
    assert _status(engine, valid, "35") is RuleStatus.PASS

    engine, _, invalid = _parsed_values(lambda root, structure: build(root, structure, True))
    assert _status(engine, invalid, "35") is RuleStatus.FAIL
