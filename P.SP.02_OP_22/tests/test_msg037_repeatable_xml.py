from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.037"
STRUCTURE = "R.IP.SP.02.002"
APP = "ipcdo:TrademarkApplicationDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"


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


def _values(builder):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, _ = engine.body_provider._values_from_element(structure, parsed)
    return engine, values


def _rules(engine, code):
    base = f"{MESSAGE}.T55.REQ.{code}"
    return [
        r for r in engine.rules[MESSAGE].structured_rules
        if r["rule_id"] == base or r["rule_id"].startswith(base + ".")
    ]


def _status(engine, code, values):
    statuses = [StructuredRuleEvaluator().evaluate(r, values).status for r in _rules(engine, code)]
    assert statuses
    return RuleStatus.FAIL if RuleStatus.FAIL in statuses else RuleStatus.PASS


def _address(parent, structure, *, complete=True):
    node = _child(parent, structure, "ccdo", "SubjectAddressDetails")
    _child(node, structure, "csdo", "AddressKindCode", "2")
    _child(node, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
    if complete:
        _child(node, structure, "csdo", "CityName", "Москва")
    _child(node, structure, "csdo", "StreetName", "Тестовая")
    _child(node, structure, "csdo", "BuildingNumberId", "1")
    return node


def _comm(parent, structure, *, complete=True):
    node = _child(parent, structure, "ccdo", "CommunicationDetails")
    _child(node, structure, "csdo", "CommunicationChannelCode", "EM")
    if complete:
        _child(node, structure, "csdo", "CommunicationChannelId", "x@example.test")
    return node


def _party(app, structure, role, *, omit=None):
    node = _child(app, structure, "ipcdo", "IPPartyDetails")
    _child(node, structure, "ipsdo", "IPPartyKindCode", role)
    _child(node, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
    _child(node, structure, "ipsdo", "IPSubjectName", role)
    if omit != "address":
        _address(node, structure)
    if omit != "communication":
        _comm(node, structure)
    if role == "PA" and omit != "attorney":
        _child(node, structure, "ipsdo", "PatentAttorneyId", "PA-1")
    return node


def _tm(app, structure, *, trigger=False, picture=True, complete=True):
    node = _child(app, structure, "ipcdo", "TrademarkDetails")
    desc = _child(node, structure, "ipcdo", "TMDescriptionDetails")
    _child(desc, structure, "csdo", "DescriptionText", "Описание")
    if complete:
        _child(node, structure, "ipsdo", "TrademarkKindCode", "140" if trigger else "110")
        _child(node, structure, "ipsdo", "TrademarkKindName", "Изобразительный знак" if trigger else "Словесный знак")
        _child(node, structure, "ipsdo", "CollectiveMarkIndicator", "0")
    if trigger and picture:
        _child(node, structure, "ipsdo", "TrademarkPicture", "PIC")
        _child(node, structure, "ipsdo", "TrademarkColourName", "red")
    return node


def _goods(app, structure, *, complete=True):
    node = _child(app, structure, "ipcdo", "GoodsBaseDetails")
    if complete:
        _child(node, structure, "ipsdo", "GoodsClassCode", "01")
    _child(node, structure, "ipsdo", "GoodsClassName", "Class 01")
    _child(node, structure, "ipsdo", "GoodsName", "Goods")
    return node


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_req15_repeated_ap_sparse_parent_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for i in range(2):
            _party(app, structure, "AP", omit="communication" if i == bad_index else None)

    engine, values = _values(build)
    assert _status(engine, 15, values) is (RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize(("code", "role", "omit"), [(21, "PA", "attorney"), (22, "RE", "address")])
@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_req21_req22_repeated_role_parent_alignment(code, role, omit, bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for i in range(2):
            _party(app, structure, role, omit=omit if i == bad_index else None)

    engine, values = _values(build)
    assert _status(engine, code, values) is (RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_req25_repeated_trademark_parent_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for i in range(2):
            _tm(app, structure, complete=i != bad_index)

    engine, values = _values(build)
    assert _status(engine, 25, values) is (RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_req29_repeated_goods_parent_alignment(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for i in range(2):
            _goods(app, structure, complete=i != bad_index)

    engine, values = _values(build)
    assert _status(engine, 29, values) is (RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


def test_req27_same_parent_trigger_and_required_fields_pass():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _tm(app, structure, trigger=True, picture=True)

    engine, values = _values(build)
    assert _status(engine, 27, values) is RuleStatus.PASS


def test_req27_cross_parent_satisfaction_is_rejected():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _tm(app, structure, trigger=True, picture=False)
        other = _tm(app, structure, trigger=False)
        _child(other, structure, "ipsdo", "TrademarkPicture", "PIC")
        _child(other, structure, "ipsdo", "TrademarkColourName", "red")

    engine, values = _values(build)
    assert _status(engine, 27, values) is RuleStatus.FAIL


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_req27_good_good_bad_good_good_bad_matrix(bad_index):
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        for i in range(2):
            _tm(app, structure, trigger=True, picture=i != bad_index)

    engine, values = _values(build)
    assert _status(engine, 27, values) is (RuleStatus.PASS if bad_index is None else RuleStatus.FAIL)


def test_req5_wrong_owner_status_code_cannot_satisfy_required_status_owner():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        _child(app, structure, "csdo", "StatusCode", "31")

    engine, values = _values(build)
    assert _status(engine, 5, values) is RuleStatus.FAIL


def test_req5_wrong_namespace_same_local_status_code_cannot_satisfy_owner():
    def build(root, structure):
        app = _child(root, structure, "ipcdo", "TrademarkApplicationDetails")
        status = _child(app, structure, "ipcdo", "IPEntityStatusDetails")
        _child(status, structure, "csdo", "StatusCode", "31", namespace="urn:wrong")

    engine, values = _values(build)
    assert _status(engine, 5, values) is RuleStatus.FAIL
