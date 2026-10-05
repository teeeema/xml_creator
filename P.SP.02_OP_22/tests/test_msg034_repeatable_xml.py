from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.034"
APP = "ipcdo:TrademarkApplicationDetails"
DOCS = f"{APP}/ipcdo:AccompanyingDocumentsDetails"
SIG = f"{APP}/ipcdo:SignatureDetails"
OFFICER = f"{SIG}/ipcdo:OfficerDetails"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _q(structure, prefix, local):
    return f"{{{structure.imported_namespaces[prefix]}}}{local}"


def _child(parent, structure, prefix, local, text=None, namespace=None):
    ns = namespace if namespace is not None else structure.imported_namespaces[prefix]
    node = ET.SubElement(parent, ET.QName(ns, local))
    if text is not None:
        node.text = text
    return node


def _first(parent, structure, prefix, local):
    return parent.find(_q(structure, prefix, local))


def _required(parent, structure, prefix, local):
    node = _first(parent, structure, prefix, local)
    assert node is not None, (prefix, local)
    return node


def _values():
    party = f"{APP}/ipcdo:IPPartyDetails"
    address = f"{party}/ccdo:SubjectAddressDetails"
    comm = f"{party}/ccdo:CommunicationDetails"
    tm = f"{APP}/ipcdo:TrademarkDetails"
    desc = f"{tm}/ipcdo:TMDescriptionDetails"
    goods = f"{APP}/ipcdo:GoodsBaseDetails"
    naming = f"{APP}/ipcdo:NamingAbilityProofDetails"
    proof = f"{naming}/ipcdo:ProofDocTextDetails"
    nested_doc = f"{proof}/ipcdo:AccompanyingDocumentsDetails"
    resource = "ccdo:ResourceItemStatusDetails"
    validity = f"{resource}/ccdo:ValidityPeriodDetails"
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000434",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:30:00+03:00",
        APP: [None],
        f"{APP}/ipsdo:IPDocKindName": "Документ, содержащий доказательства в подтверждение приобретения заявленным обозначением различительной способности",
        f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-30",
        f"{APP}/ipsdo:TrademarkApplicationId": "2026/RU-000434",
        party: [None],
        f"{party}/ipsdo:IPPartyKindCode": "AP",
        f"{party}/csdo:UnifiedCountryCode": "RU",
        f"{party}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{party}/ipsdo:IPSubjectName": "Заявитель",
        f"{party}/ipsdo:IPSubjectName/@nameRepresentationKindCode": "OR",
        f"{party}/ipsdo:IPSubjectName/@languageCode": "RU",
        address: [""],
        f"{address}/csdo:AddressKindCode": "2",
        f"{address}/csdo:UnifiedCountryCode": "RU",
        f"{address}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{address}/csdo:CityName": "Москва",
        f"{address}/csdo:StreetName": "Тестовая",
        f"{address}/csdo:BuildingNumberId": "1",
        comm: [""],
        f"{comm}/csdo:CommunicationChannelCode": "EM",
        f"{comm}/csdo:CommunicationChannelId": "applicant@example.test",
        tm: [None],
        desc: [""],
        f"{desc}/csdo:DescriptionText": "Описание",
        f"{tm}/ipsdo:TrademarkKindCode": "110",
        f"{tm}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{tm}/ipsdo:CollectiveMarkIndicator": "0",
        goods: [None],
        f"{goods}/ipsdo:GoodsClassCode": "01",
        f"{goods}/ipsdo:GoodsClassName": "Класс 01",
        f"{goods}/ipsdo:GoodsName": "Товар",
        DOCS: [None],
        f"{DOCS}/ipsdo:IPDocKindCode": "00034",
        f"{DOCS}/csdo:DocId": "DOC-1",
        f"{DOCS}/csdo:DocCreationDate": "2026-09-30",
        f"{DOCS}/csdo:DescriptionText": "Документ 1",
        f"{DOCS}/csdo:PageQuantity": "1",
        f"{DOCS}/csdo:DocBinaryText": "QUJD",
        naming: [None],
        f"{naming}/ipsdo:ProofKindCode": "01",
        proof: [None],
        nested_doc: [None],
        f"{nested_doc}/ipsdo:IPDocKindCode": "00035",
        f"{nested_doc}/csdo:DocId": "NESTED-1",
        f"{nested_doc}/csdo:DocCreationDate": "2026-09-30",
        f"{nested_doc}/csdo:DescriptionText": "Nested",
        f"{nested_doc}/csdo:PageQuantity": "1",
        f"{nested_doc}/csdo:DocBinaryText": "QUJD",
        SIG: [None],
        f"{SIG}/csdo:DocCreationDate": "2026-09-30",
        OFFICER: [None],
        f"{OFFICER}/ccdo:FullNameDetails": [None],
        f"{OFFICER}/ccdo:FullNameDetails/csdo:FirstName": "Иван",
        f"{OFFICER}/ccdo:FullNameDetails/csdo:LastName": "Иванов",
        f"{OFFICER}/csdo:PositionName": "Эксперт",
        resource: [None],
        validity: [None],
        f"{validity}/csdo:StartDateTime": "2026-09-30T14:31:00+03:00",
    }


def _parsed():
    engine = _engine()
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    body = engine.build_body(MESSAGE, _values(), mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    return engine, structure, parsed


def _extract(engine, structure, root):
    reparsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, reparsed)
    assert not issues, [(i.code, i.field_path, i.message) for i in issues]
    return values


def _rules(engine, code):
    prefix = f"{MESSAGE}.T52.REQ.{code}"
    return [
        rule for rule in engine.rules[MESSAGE].structured_rules
        if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")
    ]


def _statuses(engine, code, values):
    rules = _rules(engine, code)
    assert rules
    return [StructuredRuleEvaluator().evaluate(rule, values).status for rule in rules]


def _add_doc(app, structure, *, missing=None):
    doc = _child(app, structure, "ipcdo", "AccompanyingDocumentsDetails")
    for prefix, local, value in (
        ("ipsdo", "IPDocKindCode", "00034"),
        ("csdo", "DocId", "DOC-X"),
        ("csdo", "DocCreationDate", "2026-09-30"),
        ("csdo", "DescriptionText", "Документ"),
        ("csdo", "PageQuantity", "1"),
        ("csdo", "DocBinaryText", "QUJD"),
    ):
        if local != missing:
            _child(doc, structure, prefix, local, value)
    return doc


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_req5_repeated_direct_documents_preserve_per_parent_semantics(bad_index):
    engine, structure, root = _parsed()
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    first = _required(app, structure, "ipcdo", "AccompanyingDocumentsDetails")
    second = _add_doc(app, structure)
    if bad_index == 0:
        first.remove(_required(first, structure, "csdo", "DocBinaryText"))
    elif bad_index == 1:
        second.remove(_required(second, structure, "csdo", "DocBinaryText"))

    values = _extract(engine, structure, root)
    binaries = values[f"{DOCS}/csdo:DocBinaryText"]
    if bad_index is None:
        assert binaries == ["QUJD", "QUJD"]
        assert _statuses(engine, 5, values) == [RuleStatus.PASS]
    elif bad_index == 0:
        assert binaries == [None, "QUJD"]
        assert RuleStatus.FAIL in _statuses(engine, 5, values)
    else:
        assert binaries == ["QUJD", None]
        assert RuleStatus.FAIL in _statuses(engine, 5, values)


def _add_officer(sig, structure, *, missing=None, communication=False):
    officer = _child(sig, structure, "ipcdo", "OfficerDetails")
    full = _child(officer, structure, "ccdo", "FullNameDetails")
    if missing != "FirstName":
        _child(full, structure, "csdo", "FirstName", "Петр")
    if missing != "LastName":
        _child(full, structure, "csdo", "LastName", "Петров")
    if missing != "PositionName":
        _child(officer, structure, "csdo", "PositionName", "Эксперт")
    if communication:
        comm = _child(officer, structure, "ccdo", "CommunicationDetails")
        _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
        _child(comm, structure, "csdo", "CommunicationChannelId", "x@example.test")
    return officer


@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_req37_repeated_officers_preserve_per_parent_semantics(bad_index):
    engine, structure, root = _parsed()
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    sig = _required(app, structure, "ipcdo", "SignatureDetails")
    first = _required(sig, structure, "ipcdo", "OfficerDetails")
    second = _add_officer(sig, structure)
    if bad_index == 0:
        first.remove(_required(first, structure, "csdo", "PositionName"))
    elif bad_index == 1:
        second.remove(_required(second, structure, "csdo", "PositionName"))

    values = _extract(engine, structure, root)
    positions = values[f"{OFFICER}/csdo:PositionName"]
    if bad_index is None:
        assert positions == ["Эксперт", "Эксперт"]
        assert _statuses(engine, 37, values) == [RuleStatus.PASS]
    elif bad_index == 0:
        assert positions == [None, "Эксперт"]
        assert RuleStatus.FAIL in _statuses(engine, 37, values)
    else:
        assert positions == ["Эксперт", None]
        assert RuleStatus.FAIL in _statuses(engine, 37, values)


def _direct_full_name(sig, structure):
    full = _child(sig, structure, "ccdo", "FullNameDetails")
    _child(full, structure, "csdo", "FirstName", "Анна")
    _child(full, structure, "csdo", "LastName", "Сидорова")
    return full


def test_req35_36_two_signatures_do_not_leak_branches_between_parents():
    engine, structure, root = _parsed()
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    sig1 = _required(app, structure, "ipcdo", "SignatureDetails")
    sig2 = _child(app, structure, "ipcdo", "SignatureDetails")
    _child(sig2, structure, "csdo", "DocCreationDate", "2026-09-30")
    _direct_full_name(sig2, structure)

    values = _extract(engine, structure, root)
    assert _statuses(engine, 35, values) == [RuleStatus.PASS, RuleStatus.PASS]
    assert _statuses(engine, 36, values) == [RuleStatus.PASS]

    _direct_full_name(sig1, structure)
    values = _extract(engine, structure, root)
    assert RuleStatus.FAIL in _statuses(engine, 35, values)
    assert RuleStatus.FAIL in _statuses(engine, 36, values)


def test_req37_wrong_owner_officer_under_trademark_claim_does_not_leak_into_signature_scope():
    engine, structure, root = _parsed()
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    claim = _child(app, structure, "ipcdo", "TrademarkClaimDetails")
    stakeholder = _child(claim, structure, "ipcdo", "StakeholderDetails")
    wrong_owner = _child(stakeholder, structure, "ipcdo", "OfficerDetails")
    _child(wrong_owner, structure, "ccdo", "FullNameDetails")

    values = _extract(engine, structure, root)
    assert f"{APP}/ipcdo:TrademarkClaimDetails/ipcdo:StakeholderDetails/ipcdo:OfficerDetails" in values
    assert _statuses(engine, 37, values) == [RuleStatus.PASS]


def test_req5_nested_and_direct_accompanying_documents_are_both_selected_by_exact_qname():
    engine, structure, root = _parsed()
    values = _extract(engine, structure, root)
    selector = _rules(engine, 5)[0]["selector"]
    selected = StructuredRuleEvaluator().select(selector, values)
    assert len(selected) == 2
    assert all(item["csdo:DocBinaryText"] == "QUJD" for item in selected)


def test_wrong_namespace_same_local_name_is_ignored_by_qname_selector():
    engine, structure, root = _parsed()
    app = _required(root, structure, "ipcdo", "TrademarkApplicationDetails")
    bogus = _child(app, structure, "ipcdo", "AccompanyingDocumentsDetails", namespace="urn:wrong")
    _child(bogus, structure, "csdo", "DocId", "WRONG")
    values = _extract(engine, structure, root)
    selected = StructuredRuleEvaluator().select(_rules(engine, 5)[0]["selector"], values)
    assert len(selected) == 2
    assert _statuses(engine, 5, values) == [RuleStatus.PASS]
