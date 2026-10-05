from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.020"
STRUCTURE = "R.IP.SP.02.007"
P = "ipcdo:UnifiedRegisterRecordsDetails"
STATUS_CODE = "ipcdo:IPEntityStatusDetails/csdo:StatusCode"
CANCEL_NAME = "Решение об аннулировании регистрации товарного знака, знака обслуживания Евразийского экономического союза"
NEW_NAME = "Решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении всех заявленных товаров и (или) услуг"


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


def _parsed_values(builder, *, allow_issues=False):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    if not allow_issues:
        assert not issues
    return engine, values, issues


def _direct_rules(engine, requirement):
    rule_id = f"P.SP.02.MSG.020.T53.REQ.{requirement}"
    return [rule for rule in engine.rules[MESSAGE].structured_rules if rule["rule_id"] == rule_id]


def _direct_statuses(engine, requirement, values):
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(rule, values).status for rule in _direct_rules(engine, requirement)]


def _inherited_rules(engine, item):
    return [
        rule
        for rule in engine.rules[MESSAGE].structured_rules
        if len(rule.get("source_refs", [])) == 2
        and rule["source_refs"][0].get("source_id") == "22OP-RULE-P.SP.02.MSG.020-T53-6-19"
        and rule["source_refs"][1].get("item") == str(item)
    ]


def _inherited_statuses(engine, item, values):
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(rule, values).status for rule in _inherited_rules(engine, item)]


def _assert_all_pass(statuses):
    assert statuses
    assert all(status is RuleStatus.PASS for status in statuses)


def _role_record(
    root,
    structure,
    role,
    *,
    event=True,
    trademark_id=True,
    start=True,
    end=True,
    req23_complete=True,
    doc_mode="code",
    nested_collision=False,
    cancellation_indicator=False,
    event_date="2026-09-24",
    start_time="2026-09-24T12:00:00+03:00",
    end_time="2026-09-24T13:00:00+03:00",
    doc_code="12345",
):
    record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
    if trademark_id:
        _child(record, structure, "ipsdo", "TrademarkId", f"TM-{role}")

    if doc_mode == "code":
        _child(record, structure, "ipsdo", "IPDocKindCode", doc_code)
    elif doc_mode in {"fallback", "wrong-fallback"}:
        expected = CANCEL_NAME if role == "CANCEL" else NEW_NAME
        _child(record, structure, "ipsdo", "IPDocKindName", expected if doc_mode == "fallback" else "WRONG")

    status = _child(record, structure, "ipcdo", "IPEntityStatusDetails")
    if event:
        _child(status, structure, "csdo", "EventDate", event_date)
    _child(status, structure, "csdo", "StatusCode", "04" if role == "CANCEL" else "01")
    if nested_collision:
        _child(status, structure, "ipsdo", "IPDocKindCode", "99999")
        _child(status, structure, "ipsdo", "IPDocKindName", "NESTED STATUS NAME")
        nested_doc = _child(record, structure, "ipcdo", "AccompanyingDocumentsDetails")
        _child(nested_doc, structure, "ipsdo", "IPDocKindCode", "88888")
        _child(nested_doc, structure, "ipsdo", "IPDocKindName", "NESTED DOCUMENT NAME")

    validity = _child(_child(record, structure, "ccdo", "ResourceItemStatusDetails"), structure, "ccdo", "ValidityPeriodDetails")
    if start:
        _child(validity, structure, "csdo", "StartDateTime", start_time)
    if end:
        _child(validity, structure, "csdo", "EndDateTime", end_time)

    if cancellation_indicator:
        goods = _child(record, structure, "ipcdo", "GoodsBaseDetails")
        _child(goods, structure, "ipsdo", "CancellationStatusIndicator", "1")

    if role == "CANCEL":
        reg = _child(record, structure, "ipcdo", "RegistrationCancellationDetails")
        complaint = _child(reg, structure, "ipcdo", "ComplaintInvalidateProtectionTrademarkDetails")
        _child(complaint, structure, "ipsdo", "CancellationRegistrationTrademarkCode", "1")
        if req23_complete:
            _child(complaint, structure, "ipsdo", "SolutionCancellationRegistrationTrademarkCode", "1")
    return record


@pytest.mark.parametrize("order", [("CANCEL", "NEW"), ("NEW", "CANCEL")])
def test_role_selectors_are_position_independent_in_production_xml(order):
    def build(root, structure):
        for role in order:
            _role_record(root, structure, role)

    engine, values, _ = _parsed_values(build)
    for requirement in ("1", "2", "4", "5", "20", "21", "22", "23", "25", "26", "27", "28"):
        _assert_all_pass(_direct_statuses(engine, requirement, values))

    evaluator = StructuredRuleEvaluator()
    for code, expected_id in (("04", "TM-CANCEL"), ("01", "TM-NEW")):
        selected = evaluator.select(
            {"collection": P, "where": {"field": STATUS_CODE, "operator": "EQ", "value": code}},
            values,
        )
        assert len(selected) == 1
        assert selected[0]["ipsdo:TrademarkId"] == expected_id


@pytest.mark.parametrize("order", [("CANCEL", "NEW"), ("NEW", "CANCEL")])
def test_role_relative_fields_do_not_leak_between_parent_indexes(order):
    expected = {
        "CANCEL": {
            "code": "04",
            "event": "2026-09-20",
            "start": "2026-09-20T10:00:00+03:00",
            "end": "2026-09-20T11:00:00+03:00",
            "doc": "C-DOC",
            "trademark": "TM-CANCEL",
        },
        "NEW": {
            "code": "01",
            "event": "2026-09-21",
            "start": "2026-09-21T10:00:00+03:00",
            "end": "2026-09-21T11:00:00+03:00",
            "doc": "N-DOC",
            "trademark": "TM-NEW",
        },
    }

    def build(root, structure):
        for role in order:
            item = expected[role]
            _role_record(
                root,
                structure,
                role,
                event_date=item["event"],
                start_time=item["start"],
                end_time=item["end"],
                doc_code=item["doc"],
            )

    _, values, _ = _parsed_values(build)
    evaluator = StructuredRuleEvaluator()
    for role in ("CANCEL", "NEW"):
        item = expected[role]
        selected = evaluator.select(
            {"collection": P, "where": {"field": STATUS_CODE, "operator": "EQ", "value": item["code"]}},
            values,
        )
        assert len(selected) == 1
        context = selected[0]
        assert context["ipcdo:IPEntityStatusDetails/csdo:EventDate"] == item["event"]
        assert context["ipsdo:TrademarkId"] == item["trademark"]
        assert context["ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime"] == item["start"]
        assert context["ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime"] == item["end"]
        assert context["ipsdo:IPDocKindCode"] == item["doc"]
        if role == "CANCEL":
            assert context["ipcdo:RegistrationCancellationDetails"] is not None
        else:
            assert context.get("ipcdo:RegistrationCancellationDetails") is None


def test_one_cancel_only_does_not_force_new_record_rules_and_req3_stays_unmapped():
    def build(root, structure):
        _role_record(root, structure, "CANCEL", cancellation_indicator=True)

    engine, values, _ = _parsed_values(build)
    for requirement in ("1", "2", "4", "5", "20", "21", "22", "23", "25", "26", "27", "28"):
        _assert_all_pass(_direct_statuses(engine, requirement, values))
    assert _direct_rules(engine, "3")


@pytest.mark.parametrize("order", [("CANCEL", "NEW"), ("NEW", "CANCEL")])
def test_bad_new_does_not_leak_into_cancel_and_fails_new_rule(order):
    def build(root, structure):
        for role in order:
            _role_record(root, structure, role, event=role != "NEW")

    engine, values, _ = _parsed_values(build)
    _assert_all_pass(_direct_statuses(engine, "2", values))
    assert RuleStatus.FAIL in _direct_statuses(engine, "4", values)


@pytest.mark.parametrize("order", [("CANCEL", "NEW"), ("NEW", "CANCEL")])
def test_bad_cancel_does_not_leak_into_new_and_fails_cancel_rule(order):
    def build(root, structure):
        for role in order:
            _role_record(root, structure, role, end=role != "CANCEL")

    engine, values, _ = _parsed_values(build)
    _assert_all_pass(_direct_statuses(engine, "4", values))
    assert RuleStatus.FAIL in _direct_statuses(engine, "22", values)


def test_req23_fails_when_nested_solution_code_is_missing():
    def build(root, structure):
        _role_record(root, structure, "CANCEL", req23_complete=False)

    engine, values, _ = _parsed_values(build)
    assert RuleStatus.FAIL in _direct_statuses(engine, "23", values)


@pytest.mark.parametrize(
    "role,requirement,other_role",
    [("CANCEL", "26", "NEW"), ("NEW", "28", "CANCEL")],
)
def test_wrong_role_fallback_name_fails_only_its_role(role, requirement, other_role):
    def build(root, structure):
        _role_record(root, structure, role, doc_mode="wrong-fallback")
        _role_record(root, structure, other_role, doc_mode="fallback")

    engine, values, _ = _parsed_values(build)
    assert RuleStatus.FAIL in _direct_statuses(engine, requirement, values)
    other_requirement = "28" if requirement == "26" else "26"
    _assert_all_pass(_direct_statuses(engine, other_requirement, values))


def test_top_level_document_rules_ignore_nested_qname_collisions():
    def build(root, structure):
        _role_record(root, structure, "CANCEL", doc_mode="fallback", nested_collision=True)
        _role_record(root, structure, "NEW", doc_mode="fallback", nested_collision=True)

    engine, values, _ = _parsed_values(build)
    _assert_all_pass(_direct_statuses(engine, "26", values))
    _assert_all_pass(_direct_statuses(engine, "28", values))


def test_nested_document_name_cannot_satisfy_missing_top_level_fallback():
    def build(root, structure):
        cancel = _role_record(root, structure, "CANCEL", doc_mode="none", nested_collision=True)
        status = next(node for node in cancel if node.tag == f"{{{structure.imported_namespaces['ipcdo']}}}IPEntityStatusDetails")
        for node in status:
            if node.tag == f"{{{structure.imported_namespaces['ipsdo']}}}IPDocKindName":
                node.text = CANCEL_NAME

    engine, values, _ = _parsed_values(build)
    assert RuleStatus.FAIL in _direct_statuses(engine, "26", values)


def _goods_case(root, structure, bad_index):
    record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
    for index in range(2):
        goods = _child(record, structure, "ipcdo", "GoodsBaseDetails")
        _child(goods, structure, "ipsdo", "GoodsClassName", f"Class {index}")
        if bad_index != index:
            _child(goods, structure, "ipsdo", "GoodsName", f"Goods {index}")
        _child(goods, structure, "ipsdo", "TrademarkDecisionIndicator", "1")
        _child(goods, structure, "ipsdo", "TrademarkApplicationId", f"APP-{index}")


def _party_case(root, structure, bad_index):
    record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
    for index in range(2):
        party = _child(record, structure, "ipcdo", "IPPartyDetails")
        country = _child(party, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
        assert country is not None
        if bad_index != index:
            _child(party, structure, "ipsdo", "IPSubjectName", f"Party {index}")
        address = _child(party, structure, "ccdo", "SubjectAddressDetails")
        _child(address, structure, "csdo", "AddressKindCode", "2")
        _child(address, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
        _child(address, structure, "csdo", "CityName", "Москва")
        _child(address, structure, "csdo", "StreetName", "Тестовая")
        _child(address, structure, "csdo", "BuildingNumberId", str(index))
        comm = _child(party, structure, "ccdo", "CommunicationDetails")
        _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
        _child(comm, structure, "csdo", "CommunicationChannelId", f"u{index}@example.test")


def _address_case(root, structure, bad_index):
    record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
    party = _child(record, structure, "ipcdo", "IPPartyDetails")
    for index in range(2):
        address = _child(party, structure, "ccdo", "SubjectAddressDetails")
        _child(address, structure, "csdo", "AddressKindCode", "2")
        _child(address, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
        if bad_index != index:
            _child(address, structure, "csdo", "CityName", "Москва")
        _child(address, structure, "csdo", "StreetName", "Тестовая")
        _child(address, structure, "csdo", "BuildingNumberId", str(index))


def _comm_case(root, structure, bad_index):
    record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
    party = _child(record, structure, "ipcdo", "IPPartyDetails")
    for index in range(2):
        comm = _child(party, structure, "ccdo", "CommunicationDetails")
        _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
        if bad_index != index:
            _child(comm, structure, "csdo", "CommunicationChannelId", f"u{index}@example.test")


def _element_case(root, structure, bad_index):
    record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
    tm = _child(record, structure, "ipcdo", "TrademarkDetails")
    desc = _child(tm, structure, "ipcdo", "TMDescriptionDetails")
    _child(desc, structure, "csdo", "DescriptionText", "Описание")
    for index in range(2):
        element = _child(desc, structure, "ipcdo", "TMElementDetails")
        if bad_index != index:
            _child(element, structure, "ipsdo", "TrademarkCFECode", "01.01.01")
        _child(element, structure, "csdo", "DesignationName", f"D{index}")
        _child(element, structure, "ipsdo", "TMLocalizedName", f"L{index}")
        _child(element, structure, "ipsdo", "TMTransliterationName", f"T{index}")


def _country_case(root, structure, bad_index):
    record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
    party = _child(record, structure, "ipcdo", "IPPartyDetails")
    for index in range(2):
        address = _child(party, structure, "ccdo", "SubjectAddressDetails")
        _child(
            address,
            structure,
            "csdo",
            "UnifiedCountryCode",
            "RU",
            attrs={"codeListId": "WRONG" if bad_index == index else "ВОИС ST.3"},
        )


@pytest.mark.parametrize(
    "builder,item",
    [
        (_goods_case, 16),
        (_party_case, 12),
        (_address_case, 7),
        (_comm_case, 8),
        (_element_case, 15),
        (_country_case, 6),
    ],
)
@pytest.mark.parametrize("bad_index", [None, 0, 1])
def test_nested_repeatables_preserve_good_bad_position(builder, item, bad_index):
    engine, values, _ = _parsed_values(lambda root, structure: builder(root, structure, bad_index))
    statuses = _inherited_statuses(engine, item, values)
    if bad_index is None:
        _assert_all_pass(statuses)
    else:
        assert RuleStatus.FAIL in statuses


def test_wrong_namespace_required_child_does_not_match_by_local_name():
    def build(root, structure):
        record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        party = _child(record, structure, "ipcdo", "IPPartyDetails")
        comm = _child(party, structure, "ccdo", "CommunicationDetails")
        _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
        _child(comm, structure, "csdo", "CommunicationChannelId", "wrong@example.test", namespace="urn:wrong")

    engine, values, _ = _parsed_values(build, allow_issues=True)
    assert values.get(f"{P}/ipcdo:IPPartyDetails/ccdo:CommunicationDetails/csdo:CommunicationChannelId") is None
    assert RuleStatus.FAIL in _inherited_statuses(engine, 8, values)
