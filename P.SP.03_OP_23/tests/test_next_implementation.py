from copy import deepcopy
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine

from test_b1_production import (
    PACKAGE,
    _append_msg013_national_registration,
    _append_register_attachment,
    _apply_rh_register_mutation,
    _assert_rule_fails,
    _assert_rule_passes,
    _ensure_child,
    _normalise_register_item,
    _raw_register_document,
    _register_items,
    _remove_direct_children,
    _set_identifier_pair,
    _status_of,
    _validate_document,
)


def _namespaces(message: str):
    return EaeuXmlEngine.load_process(PACKAGE).get_structure(
        message,
        mode=GenerationMode.TEST,
    ).imported_namespaces


def _set_status(item: ET.Element, namespaces, code: str):
    status = _ensure_child(item, namespaces["ipcdo"], "IPEntityStatusDetails")
    _ensure_child(status, namespaces["csdo"], "EventDate", "2026-10-08")
    code_element = _ensure_child(status, namespaces["csdo"], "StatusCode", code)
    code_element.attrib.pop("codeListId", None)


def _ensure_geographic_country(item: ET.Element, namespaces):
    geographic = next(
        element
        for element in item.iter()
        if element.tag.endswith("}GeographicRegionDescriptionTextDetails")
    )
    country = _ensure_child(geographic, namespaces["csdo"], "UnifiedCountryCode", "RU")
    country.set("codeListId", "ВОИС ST.3")


def _submission_document(message: str, *, two_items: bool):
    document = _raw_register_document(message)
    namespaces = _namespaces(message)
    items = _register_items(document)
    first = items[0]
    for extra in items[1:]:
        document.remove(extra)

    if two_items:
        _normalise_register_item(first, namespaces, "AO")
        _set_status(first, namespaces, "01")
        period = next(element for element in first.iter() if element.tag.endswith("}ValidityPeriodDetails"))
        _remove_direct_children(period, "EndDateTime")
        second = deepcopy(first)
        _normalise_register_item(second, namespaces, "RH")
        _ensure_geographic_country(second, namespaces)
        _set_status(second, namespaces, "10")
        period = next(element for element in second.iter() if element.tag.endswith("}ValidityPeriodDetails"))
        _remove_direct_children(period, "EndDateTime")
        document.append(second)
    else:
        _normalise_register_item(first, namespaces, "RH")
        _ensure_geographic_country(first, namespaces)
        _set_status(first, namespaces, "10")
        period = next(element for element in first.iter() if element.tag.endswith("}ValidityPeriodDetails"))
        _remove_direct_children(period, "EndDateTime")
    return document


def _two_rh_document(message: str, *, identifier_pair: str = "application", second_status: str):
    document = _raw_register_document(message)
    namespaces = _namespaces(message)
    items = _register_items(document)
    first = items[0]
    for extra in items[1:]:
        document.remove(extra)
    _normalise_register_item(first, namespaces, "RH")
    _ensure_geographic_country(first, namespaces)
    _set_identifier_pair(first, namespaces, identifier_pair)
    _set_status(first, namespaces, "11")
    first_period = next(element for element in first.iter() if element.tag.endswith("}ValidityPeriodDetails"))
    next(element for element in first_period if element.tag.endswith("}StartDateTime")).text = "2026-10-06T10:00:00+03:00"
    next(element for element in first_period if element.tag.endswith("}EndDateTime")).text = "2026-10-07T10:00:00+03:00"

    second = deepcopy(first)
    document.append(second)
    _set_identifier_pair(second, namespaces, identifier_pair)
    _set_status(second, namespaces, second_status)
    second_period = next(element for element in second.iter() if element.tag.endswith("}ValidityPeriodDetails"))
    next(element for element in second_period if element.tag.endswith("}StartDateTime")).text = "2026-10-08T10:00:00+03:00"
    _remove_direct_children(second_period, "EndDateTime")
    return document


def _msg014_document(*, identifier_pair: str = "application"):
    message = "P.SP.03.MSG.014"
    document = _two_rh_document(message, identifier_pair=identifier_pair, second_status="12")
    second = _register_items(document)[1]
    right = next(element for element in second if element.tag.endswith("}ApellationOfOriginEAEURightDetails"))
    next(element for element in right if element.tag.endswith("}DocValidityDate")).text = "2031-01-01"
    _append_register_attachment(message, _register_items(document)[0])
    return document


def _msg015_document():
    return _two_rh_document("P.SP.03.MSG.015", second_status="19")


@pytest.mark.parametrize("message", ["P.SP.03.MSG.004", "P.SP.03.MSG.011"])
def test_submission_req001_cardinality_real_xml(message):
    rule = f"{message}.REQ.001"
    document = _submission_document(message, two_items=False)
    _assert_rule_passes(message, document, rule)
    document.append(deepcopy(_register_items(document)[0]))
    document.append(deepcopy(_register_items(document)[0]))
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", ["P.SP.03.MSG.004", "P.SP.03.MSG.011"])
@pytest.mark.parametrize("suffix,position", [("first_ao", 0), ("second_rh", 1)])
def test_submission_req002_ordered_kinds_real_xml(message, suffix, position):
    rule = f"{message}.REQ.002.{suffix}"
    document = _submission_document(message, two_items=True)
    _assert_rule_passes(message, document, rule)
    kind = next(
        element
        for element in _register_items(document)[position]
        if element.tag.endswith("}ResourceItemKindCode")
    )
    kind.text = "XX"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", ["P.SP.03.MSG.004", "P.SP.03.MSG.011"])
def test_submission_req003_single_item_kind_real_xml(message):
    rule = f"{message}.REQ.003"
    document = _submission_document(message, two_items=False)
    _assert_rule_passes(message, document, rule)
    item = _register_items(document)[0]
    next(element for element in item if element.tag.endswith("}ResourceItemKindCode")).text = "XX"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", ["P.SP.03.MSG.004", "P.SP.03.MSG.011"])
def test_submission_req036_ao_status_real_xml(message):
    rule = f"{message}.REQ.036"
    document = _submission_document(message, two_items=True)
    _assert_rule_passes(message, document, rule)
    status = _status_of(_register_items(document)[0])
    next(element for element in status if element.tag.endswith("}StatusCode")).text = "XX"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", ["P.SP.03.MSG.004", "P.SP.03.MSG.011"])
def test_submission_req037_rh_status_real_xml(message):
    rule = f"{message}.REQ.037"
    document = _submission_document(message, two_items=False)
    _assert_rule_passes(message, document, rule)
    status = _status_of(_register_items(document)[0])
    next(element for element in status if element.tag.endswith("}StatusCode")).text = "XX"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", [
    "P.SP.03.MSG.006",
    "P.SP.03.MSG.007",
    "P.SP.03.MSG.008",
])
def test_req023_national_registration_shape_real_xml(message):
    rule = f"{message}.REQ.023.shape"
    from test_b1_production import _two_register_document

    document = _two_register_document(message)
    item = _register_items(document)[0]
    registration = _append_msg013_national_registration(
        item,
        _namespaces(message),
        "RU",
        "NAT-001",
        include_right=True,
    )
    _assert_rule_passes(message, document, rule)
    registration.remove(next(element for element in registration if element.tag.endswith("}IPRightDetails")))
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", [
    "P.SP.03.MSG.006",
    "P.SP.03.MSG.007",
    "P.SP.03.MSG.008",
])
def test_req023_national_registration_country_unique_real_xml(message):
    rule = f"{message}.REQ.023.unique_country"
    from test_b1_production import _two_register_document

    document = _two_register_document(message)
    item = _register_items(document)[0]
    namespaces = _namespaces(message)
    _append_msg013_national_registration(item, namespaces, "RU", "NAT-001", include_right=True)
    _assert_rule_passes(message, document, rule)
    _append_msg013_national_registration(item, namespaces, "RU", "NAT-002", include_right=True)
    _assert_rule_fails(message, document, rule)


def test_msg006_req042_national_registration_shape_real_xml():
    message = "P.SP.03.MSG.006"
    rule = f"{message}.REQ.042.shape"
    from test_b1_production import _two_register_document

    document = _two_register_document(message, kind="AO")
    item = _register_items(document)[0]
    registration = _append_msg013_national_registration(item, _namespaces(message), "RU", "NAT-001")
    _assert_rule_passes(message, document, rule)
    ET.SubElement(registration, f"{{{_namespaces(message)['ipsdo']}}}RegistrationDate").text = "2026-10-01"
    _assert_rule_fails(message, document, rule)


def test_msg006_req042_national_registration_country_unique_real_xml():
    message = "P.SP.03.MSG.006"
    rule = f"{message}.REQ.042.unique_country"
    from test_b1_production import _two_register_document

    document = _two_register_document(message, kind="AO")
    item = _register_items(document)[0]
    namespaces = _namespaces(message)
    _append_msg013_national_registration(item, namespaces, "RU", "NAT-001")
    _assert_rule_passes(message, document, rule)
    _append_msg013_national_registration(item, namespaces, "RU", "NAT-002")
    _assert_rule_fails(message, document, rule)


MSG014_CASES = [
    ("P.SP.03.MSG.014.REQ.001.cardinality", "remove_second", "application"),
    ("P.SP.03.MSG.014.REQ.003.presence", "remove_start", "application"),
    ("P.SP.03.MSG.014.REQ.003.order", "reverse_start", "application"),
    ("P.SP.03.MSG.014.REQ.004.presence", "remove_old_end", "application"),
    ("P.SP.03.MSG.014.REQ.004.after_old_start", "old_end_before_start", "application"),
    ("P.SP.03.MSG.014.REQ.004.before_new_start", "old_end_after_new_start", "application"),
    ("P.SP.03.MSG.014.REQ.006.presence", "remove_origin_id", "application"),
    ("P.SP.03.MSG.014.REQ.006.equality", "change_origin_id", "application"),
    ("P.SP.03.MSG.014.REQ.007.combination", "break_identifier_pair", "application"),
    ("P.SP.03.MSG.014.REQ.007.application_id", "application_id", "application"),
    ("P.SP.03.MSG.014.REQ.007.application_date", "application_date", "application"),
    ("P.SP.03.MSG.014.REQ.007.doc_id", "doc_id", "document"),
    ("P.SP.03.MSG.014.REQ.007.receipt_date", "receipt_date", "document"),
    ("P.SP.03.MSG.014.REQ.015", "change_certificate", "application"),
    ("P.SP.03.MSG.014.REQ.036", "status", "application"),
]


@pytest.mark.parametrize("rule_id,mutation,identifier_pair", MSG014_CASES)
def test_msg014_next_rules_real_xml(rule_id, mutation, identifier_pair):
    message = "P.SP.03.MSG.014"
    document = _msg014_document(identifier_pair=identifier_pair)
    _assert_rule_passes(message, document, rule_id)
    _apply_rh_register_mutation(message, document, mutation)
    _assert_rule_fails(message, document, rule_id)


def test_msg014_req023_national_registration_shape_real_xml():
    message = "P.SP.03.MSG.014"
    rule = f"{message}.REQ.023.shape"
    document = _msg014_document()
    item = _register_items(document)[0]
    registration = _append_msg013_national_registration(
        item,
        _namespaces(message),
        "RU",
        "NAT-001",
        include_right=True,
    )
    _assert_rule_passes(message, document, rule)
    registration.remove(next(element for element in registration if element.tag.endswith("}IPRightDetails")))
    _assert_rule_fails(message, document, rule)


def test_msg014_req023_national_registration_country_unique_real_xml():
    message = "P.SP.03.MSG.014"
    rule = f"{message}.REQ.023.unique_country"
    document = _msg014_document()
    item = _register_items(document)[0]
    namespaces = _namespaces(message)
    _append_msg013_national_registration(item, namespaces, "RU", "NAT-001", include_right=True)
    _assert_rule_passes(message, document, rule)
    _append_msg013_national_registration(item, namespaces, "RU", "NAT-002", include_right=True)
    _assert_rule_fails(message, document, rule)


def test_msg015_req001_cardinality_real_xml():
    message = "P.SP.03.MSG.015"
    rule = f"{message}.REQ.001"
    document = _msg015_document()
    _assert_rule_passes(message, document, rule)
    document.remove(_register_items(document)[1])
    _assert_rule_fails(message, document, rule)


def test_msg015_req003_single_item_kind_runtime_real_xml():
    message = "P.SP.03.MSG.015"
    rule = f"{message}.REQ.003"
    document = _msg015_document()
    document.remove(_register_items(document)[1])
    result = _validate_document(message, document)
    assert any(
        evaluation.rule_id == rule and evaluation.status.value == "PASS"
        for evaluation in result.rule_evaluations
    )
    item = _register_items(document)[0]
    next(element for element in item if element.tag.endswith("}ResourceItemKindCode")).text = "XX"
    result = _validate_document(message, document)
    assert any(
        evaluation.rule_id == rule and evaluation.status.value == "FAIL"
        for evaluation in result.rule_evaluations
    )


def test_msg015_req007_origin_id_equal_real_xml():
    message = "P.SP.03.MSG.015"
    rule = f"{message}.REQ.007"
    document = _msg015_document()
    _assert_rule_passes(message, document, rule)
    second = _register_items(document)[1]
    origin = next(element for element in second if element.tag.endswith("}ApellationOfOriginDetails"))
    next(element for element in origin if element.tag.endswith("}ApellationOfOriginEAEUId")).text = "AO-OTHER"
    _assert_rule_fails(message, document, rule)


def test_msg015_req035_second_status_real_xml():
    message = "P.SP.03.MSG.015"
    rule = f"{message}.REQ.035"
    document = _msg015_document()
    _assert_rule_passes(message, document, rule)
    status = _status_of(_register_items(document)[1])
    next(element for element in status if element.tag.endswith("}StatusCode")).text = "XX"
    _assert_rule_fails(message, document, rule)


def test_msg015_req036_doc_validity_equal_real_xml():
    message = "P.SP.03.MSG.015"
    rule = f"{message}.REQ.036"
    document = _msg015_document()
    _assert_rule_passes(message, document, rule)
    second = _register_items(document)[1]
    right = next(element for element in second if element.tag.endswith("}ApellationOfOriginEAEURightDetails"))
    next(element for element in right if element.tag.endswith("}DocValidityDate")).text = "2031-01-01"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize(
    "message,rule,document_factory",
    [
        ("P.SP.03.MSG.007", "P.SP.03.MSG.007.REQ.036", lambda: __import__("test_b1_production")._two_register_document("P.SP.03.MSG.007")),
        ("P.SP.03.MSG.014", "P.SP.03.MSG.014.REQ.039", _msg014_document),
    ],
)
def test_post_engine_date_rules_real_xml(message, rule, document_factory):
    document = document_factory()
    _assert_rule_passes(message, document, rule)
    first, second = _register_items(document)
    first_right = next(element for element in first if element.tag.endswith("}ApellationOfOriginEAEURightDetails"))
    second_right = next(element for element in second if element.tag.endswith("}ApellationOfOriginEAEURightDetails"))
    old_date = next(element for element in first_right if element.tag.endswith("}DocValidityDate")).text
    next(element for element in second_right if element.tag.endswith("}DocValidityDate")).text = old_date
    _assert_rule_fails(message, document, rule)
