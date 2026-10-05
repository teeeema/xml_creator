from pathlib import Path
from xml.etree import ElementTree as ET
import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.062"
STRUCTURE_ID = "R.IP.SP.02.002"
APP = "ipcdo:TrademarkApplicationDetails"


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


def _values_from_xml(builder):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE_ID, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    return engine, structure, values, issues


def _rules(engine, code):
    p = f"{MESSAGE}.T81.REQ.{code}"
    return [r for r in engine.rules[MESSAGE].structured_rules if r["rule_id"] == p or r["rule_id"].startswith(p + ".") or r["rule_id"].startswith(p + "_")]


def _assert_pass(engine, code, values):
    rules = _rules(engine, code)
    assert rules, f"No rules for REQ {code}"
    statuses = [StructuredRuleEvaluator().evaluate(r, values).status for r in rules]
    assert all(s is RuleStatus.PASS for s in statuses), f"Expected all PASS for REQ {code}, got: {statuses}"


def _assert_fail(engine, code, values):
    rules = _rules(engine, code)
    assert rules, f"No rules for REQ {code}"
    statuses = [StructuredRuleEvaluator().evaluate(r, values).status for r in rules]
    assert RuleStatus.FAIL in statuses, f"Expected FAIL for REQ {code}, got: {statuses}"


def _build_minimal_app(root, structure):
    app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
    _child(app, structure, "ipsdo", "TrademarkApplicationId", "2026/RU-000001")
    _child(app, structure, "ipsdo", "ApplicationReceiptDate", "2026-09-30")

    arg = _child(app, structure, "ipcdo", "ArgumentDetails")
    _child(arg, structure, "csdo", "DescriptionText", "Доводы заявителя")
    _child(arg, structure, "csdo", "EventDate", "2026-09-30")

    res = _child(root, structure, "ccdo", "ResourceItemStatusDetails")
    val = _child(res, structure, "ccdo", "ValidityPeriodDetails")
    _child(val, structure, "csdo", "StartDateTime", "2026-09-30T10:00:00+03:00")

    sig = _child(app, structure, "ipcdo", "SignatureDetails")
    fn = _child(sig, structure, "ccdo", "FullNameDetails")
    _child(fn, structure, "csdo", "LastName", "Иванов")

    return app


def test_req1_single_app_instance_pass():
    def builder(root, structure):
        _build_minimal_app(root, structure)

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_pass(engine, 1, values)


def test_req1_zero_app_instances_fail():
    def builder(root, structure):
        pass

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_fail(engine, 1, values)


def test_req1_two_app_instances_fail():
    def builder(root, structure):
        _build_minimal_app(root, structure)
        _build_minimal_app(root, structure)

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_fail(engine, 1, values)


def test_req5_and_32_argument_details_xml():
    def builder(root, structure):
        app = _build_minimal_app(root, structure)

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_pass(engine, 5, values)
    _assert_pass(engine, 32, values)


def test_req32_argument_details_missing_date_fails():
    def builder(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _child(app, structure, "ipsdo", "TrademarkApplicationId", "2026/RU-000001")
        arg = _child(app, structure, "ipcdo", "ArgumentDetails")
        _child(arg, structure, "csdo", "DescriptionText", "Только описание")
        # Missing EventDate

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_pass(engine, 5, values)
    _assert_fail(engine, 32, values)


def test_req29_multiple_goods_base_details():
    def builder(root, structure):
        app = _build_minimal_app(root, structure)
        for i in range(2):
            g = _child(app, structure, "ipcdo", "GoodsBaseDetails")
            _child(g, structure, "ipsdo", "GoodsClassCode", f"0{i+1}")
            _child(g, structure, "ipsdo", "GoodsClassName", f"Класс {i+1}")
            _child(g, structure, "ipsdo", "GoodsName", f"Товар {i+1}")

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_pass(engine, 29, values)


def test_req29_goods_one_invalid_fails():
    def builder(root, structure):
        app = _build_minimal_app(root, structure)
        g0 = _child(app, structure, "ipcdo", "GoodsBaseDetails")
        _child(g0, structure, "ipsdo", "GoodsClassCode", "01")
        _child(g0, structure, "ipsdo", "GoodsClassName", "Класс 01")
        _child(g0, structure, "ipsdo", "GoodsName", "Товар 01")

        g1 = _child(app, structure, "ipcdo", "GoodsBaseDetails")
        _child(g1, structure, "ipsdo", "GoodsClassCode", "02")
        _child(g1, structure, "ipsdo", "GoodsClassName", "Класс 02")
        # Missing GoodsName

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_fail(engine, 29, values)


def test_req30_and_31_claim_and_stakeholder_details_xml():
    def builder(root, structure):
        app = _build_minimal_app(root, structure)
        claim = _child(app, structure, "ipcdo", "TrademarkClaimDetails")
        _child(claim, structure, "ipsdo", "RequestId", "REQ-062-001")
        _child(claim, structure, "ipsdo", "RequestDate", "2026-09-30")

        stake = _child(claim, structure, "ipcdo", "StakeholderDetails")
        _child(stake, structure, "csdo", "UnifiedCountryCode", "RU")
        _child(stake, structure, "csdo", "SubjectName", "ООО Заинтересованное лицо")
        _child(stake, structure, "csdo", "SubjectBriefName", "ООО ЗЛ")
        addr = _child(stake, structure, "ccdo", "SubjectAddressDetails")
        _child(addr, structure, "csdo", "AddressKindCode", "1")
        _child(addr, structure, "csdo", "UnifiedCountryCode", "RU")
        _child(addr, structure, "csdo", "CityName", "Москва")
        _child(addr, structure, "csdo", "StreetName", "Тверская")
        _child(addr, structure, "csdo", "BuildingNumberId", "1")

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_pass(engine, 30, values)
    _assert_pass(engine, 31, values)


def test_req33_forbidden_elements_fail_when_present_in_xml():
    def builder(root, structure):
        app = _build_minimal_app(root, structure)
        _child(app, structure, "ipcdo", "ComplaintDetails")

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_fail(engine, 33, values)


def test_req34_forbidden_refusal_details_fails_when_present():
    def builder(root, structure):
        _build_minimal_app(root, structure)
        _child(root, structure, "ipcdo", "RefusalDetails")

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_fail(engine, 34, values)


def test_req35_and_36_resource_item_status_dates():
    def builder(root, structure):
        _build_minimal_app(root, structure)

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_pass(engine, 35, values)
    _assert_pass(engine, 36, values)


def test_req37_38_signature_mutual_exclusion_in_xml():
    def builder(root, structure):
        app = _build_minimal_app(root, structure)
        # Add both OfficerDetails and FullNameDetails to the signature
        sig = _child(app, structure, "ipcdo", "SignatureDetails")
        off = _child(sig, structure, "ipcdo", "OfficerDetails")
        fn1 = _child(off, structure, "ccdo", "FullNameDetails")
        _child(fn1, structure, "csdo", "LastName", "Иванов")
        _child(fn1, structure, "csdo", "FirstName", "Иван")
        _child(off, structure, "csdo", "PositionName", "Эксперт")

        fn2 = _child(sig, structure, "ccdo", "FullNameDetails")
        _child(fn2, structure, "csdo", "LastName", "Петров")

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_fail(engine, 37, values)
    _assert_fail(engine, 38, values)


def test_req16_17_20_are_scoped_to_ap_parent():
    def builder(root, structure):
        app = _build_minimal_app(root, structure)
        party = _child(app, structure, "ipcdo", "IPPartyDetails")
        _child(party, structure, "ipsdo", "IPPartyKindCode", "AP")
        _child(party, structure, "ipsdo", "IPSubjectName", "Заявитель", attrs={
            "nameRepresentationKindCode": "OR",
            "languageCode": "RU"
        })
        addr = _child(party, structure, "ccdo", "SubjectAddressDetails")
        _child(addr, structure, "csdo", "AddressKindCode", "2")
        _child(addr, structure, "csdo", "UnifiedCountryCode", "RU")
        _child(addr, structure, "csdo", "CityName", "Москва")
        _child(addr, structure, "csdo", "StreetName", "Тверская")
        _child(addr, structure, "csdo", "BuildingNumberId", "1")

    engine, structure, values, issues = _values_from_xml(builder)
    _assert_pass(engine, 16, values)
    _assert_pass(engine, 17, values)
    _assert_pass(engine, 20, values)
