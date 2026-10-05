from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.020"
STRUCTURE = "R.IP.SP.02.007"
TRANSACTION = "P.SP.02.TRN.018"
P = "ipcdo:UnifiedRegisterRecordsDetails"
STATUS = f"{P}/ipcdo:IPEntityStatusDetails"
PARTY = f"{P}/ipcdo:IPPartyDetails"
ADDRESS = f"{PARTY}/ccdo:SubjectAddressDetails"
COMM = f"{PARTY}/ccdo:CommunicationDetails"
TM = f"{P}/ipcdo:TrademarkDetails"
DESC = f"{TM}/ipcdo:TMDescriptionDetails"
ELEMENT = f"{DESC}/ipcdo:TMElementDetails"
GOODS = f"{P}/ipcdo:GoodsBaseDetails"
RESOURCE = f"{P}/ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
REG = f"{P}/ipcdo:RegistrationCancellationDetails"
COMPLAINT = f"{REG}/ipcdo:ComplaintInvalidateProtectionTrademarkDetails"
CANCEL_NAME = "Решение об аннулировании регистрации товарного знака, знака обслуживания Евразийского экономического союза"
NEW_NAME = "Решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении всех заявленных товаров и (или) услуг"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _validation_fail_ids(validation):
    return {
        issue.rule_id
        for issue in validation.issues
        if issue.code == "STRUCTURED_RULE_FAILED" and issue.rule_id
    }


def _valid_one_cancel_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": STRUCTURE,
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000020",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-24T12:00:00+03:00",
        P: [None],
        f"{P}/ipsdo:TrademarkId": "TM-CANCEL",
        f"{P}/ipsdo:IPDocKindCode": "12345",
        STATUS: [None],
        f"{STATUS}/csdo:EventDate": "2026-09-24",
        f"{STATUS}/csdo:StatusCode": "04",
        PARTY: [None],
        f"{PARTY}/ipsdo:IPPartyKindCode": "RH",
        f"{PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{PARTY}/ipsdo:IPSubjectName": "Правообладатель",
        ADDRESS: [""],
        f"{ADDRESS}/csdo:AddressKindCode": "2",
        f"{ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{ADDRESS}/csdo:CityName": "Москва",
        f"{ADDRESS}/csdo:StreetName": "Тестовая",
        f"{ADDRESS}/csdo:BuildingNumberId": "1",
        COMM: [""],
        f"{COMM}/csdo:CommunicationChannelCode": "EM",
        f"{COMM}/csdo:CommunicationChannelId": "test@example.test",
        TM: [None],
        f"{TM}/ipsdo:TrademarkPicture": "IMAGE",
        f"{TM}/ipsdo:TrademarkKindName": "Словесный знак",
        f"{TM}/ipsdo:CollectiveMarkIndicator": "0",
        DESC: [""],
        f"{DESC}/csdo:DescriptionText": "Описание",
        ELEMENT: [""],
        f"{ELEMENT}/ipsdo:TrademarkCFECode": "01.01.01",
        f"{ELEMENT}/csdo:DesignationName": "TEST",
        f"{ELEMENT}/ipsdo:TMLocalizedName": "TEST",
        f"{ELEMENT}/ipsdo:TMLocalizedName/@languageCode": "ru",
        f"{ELEMENT}/ipsdo:TMTransliterationName": "TEST",
        GOODS: [None],
        f"{GOODS}/ipsdo:GoodsClassName": "Класс 01",
        f"{GOODS}/ipsdo:GoodsName": "Товар",
        f"{GOODS}/ipsdo:TrademarkDecisionIndicator": True,
        f"{GOODS}/ipsdo:TrademarkApplicationId": "APP-1",
        RESOURCE: [None],
        VALIDITY: [None],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-24T12:00:00+03:00",
        f"{VALIDITY}/csdo:EndDateTime": "2026-09-24T13:00:00+03:00",
        REG: [None],
        f"{REG}/ipsdo:CancellationTrademarkRegistrationReasonCode": "1",
        COMPLAINT: [None],
        f"{COMPLAINT}/ipsdo:CancellationRegistrationTrademarkCode": "1",
        f"{COMPLAINT}/ipsdo:SolutionCancellationRegistrationTrademarkCode": "1",
        f"{COMPLAINT}/csdo:EventDate": "2026-09-24",
        f"{COMPLAINT}/ipcdo:ApplicantV2Details": [None],
        f"{COMPLAINT}/ipcdo:ApplicantV2Details/ccdo:CommunicationDetails": [None],
        f"{COMPLAINT}/ipcdo:ApplicantV2Details/ccdo:CommunicationDetails/csdo:CommunicationChannelCode": "EM",
        f"{COMPLAINT}/ipcdo:ApplicantV2Details/ccdo:CommunicationDetails/csdo:CommunicationChannelId": "applicant@example.test",
    }


def _build_parse_validate(values):
    engine = _engine()
    pre = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert pre.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in pre.issues]
    body = engine.build_body(MESSAGE, values, mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    extracted, extraction_issues = engine.body_provider._values_from_element(structure, parsed)
    assert not extraction_issues
    post = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    return engine, structure, parsed, extracted, post


def _child(parent, structure, prefix, local, text=None, attrs=None):
    node = ET.SubElement(parent, ET.QName(structure.imported_namespaces[prefix], local))
    if text is not None:
        node.text = text
    for key, value in (attrs or {}).items():
        node.set(key, value)
    return node


def _raw_root(engine):
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    header = _child(root, structure, "ccdo", "EDocHeader")
    _child(header, structure, "csdo", "InfEnvelopeCode", MESSAGE)
    _child(header, structure, "csdo", "EDocCode", STRUCTURE)
    _child(header, structure, "csdo", "EDocId", "00000000-0000-0000-0000-000000000020")
    _child(header, structure, "csdo", "EDocDateTime", "2026-09-24T12:00:00+03:00")
    return structure, root


def _add_party(record, structure, suffix):
    party = _child(record, structure, "ipcdo", "IPPartyDetails")
    _child(party, structure, "ipsdo", "IPPartyKindCode", "RH")
    _child(party, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
    _child(party, structure, "ipsdo", "IPSubjectName", f"Правообладатель {suffix}")
    address = _child(party, structure, "ccdo", "SubjectAddressDetails")
    _child(address, structure, "csdo", "AddressKindCode", "2")
    _child(address, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
    _child(address, structure, "csdo", "CityName", "Москва")
    _child(address, structure, "csdo", "StreetName", "Тестовая")
    _child(address, structure, "csdo", "BuildingNumberId", suffix)
    comm = _child(party, structure, "ccdo", "CommunicationDetails")
    _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
    _child(comm, structure, "csdo", "CommunicationChannelId", f"u{suffix}@example.test")


def _add_trademark(record, structure, suffix):
    tm = _child(record, structure, "ipcdo", "TrademarkDetails")
    _child(tm, structure, "ipsdo", "TrademarkPicture", "IMAGE")
    desc = _child(tm, structure, "ipcdo", "TMDescriptionDetails")
    _child(desc, structure, "csdo", "DescriptionText", "Описание")
    element = _child(desc, structure, "ipcdo", "TMElementDetails")
    _child(element, structure, "ipsdo", "TrademarkCFECode", "01.01.01")
    _child(element, structure, "csdo", "DesignationName", f"TEST-{suffix}")
    localized = _child(element, structure, "ipsdo", "TMLocalizedName", f"TEST-{suffix}")
    localized.set("languageCode", "ru")
    _child(element, structure, "ipsdo", "TMTransliterationName", f"TEST-{suffix}")
    _child(tm, structure, "ipsdo", "TrademarkKindName", "Словесный знак")
    _child(tm, structure, "ipsdo", "CollectiveMarkIndicator", "0")


def _add_goods(record, structure, suffix, *, second_bad=False):
    goods = _child(record, structure, "ipcdo", "GoodsBaseDetails")
    _child(goods, structure, "ipsdo", "GoodsClassName", "Класс 01")
    _child(goods, structure, "ipsdo", "GoodsName", f"Товар-{suffix}")
    _child(goods, structure, "ipsdo", "TrademarkDecisionIndicator", "1")
    _child(goods, structure, "ipsdo", "TrademarkApplicationId", f"APP-{suffix}")
    if second_bad:
        bad = _child(record, structure, "ipcdo", "GoodsBaseDetails")
        _child(bad, structure, "ipsdo", "GoodsClassName", "Класс 02")
        _child(bad, structure, "ipsdo", "TrademarkDecisionIndicator", "1")
        _child(bad, structure, "ipsdo", "TrademarkApplicationId", f"APP-{suffix}-BAD")


def _add_record(
    root,
    structure,
    role,
    *,
    missing_event=False,
    missing_end=False,
    missing_req23=False,
    fallback="code",
    second_bad_goods=False,
    status_code=None,
    missing_resource=False,
):
    suffix = "C" if role == "CANCEL" else "N"
    record = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
    if fallback == "code":
        _child(record, structure, "ipsdo", "IPDocKindCode", "12345")
    elif fallback == "correct":
        _child(record, structure, "ipsdo", "IPDocKindName", CANCEL_NAME if role == "CANCEL" else NEW_NAME)
    elif fallback == "wrong":
        _child(record, structure, "ipsdo", "IPDocKindName", "WRONG DOCUMENT NAME")

    _child(record, structure, "ipsdo", "TrademarkId", f"TM-{suffix}")
    status = _child(record, structure, "ipcdo", "IPEntityStatusDetails")
    _child(status, structure, "csdo", "StatusCode", status_code or ("04" if role == "CANCEL" else "01"))
    if not missing_event:
        _child(status, structure, "csdo", "EventDate", "2026-09-24")

    _add_party(record, structure, suffix)
    _add_trademark(record, structure, suffix)
    _add_goods(record, structure, suffix, second_bad=second_bad_goods)

    if not missing_resource:
        resource = _child(record, structure, "ccdo", "ResourceItemStatusDetails")
        validity = _child(resource, structure, "ccdo", "ValidityPeriodDetails")
        _child(validity, structure, "csdo", "StartDateTime", "2026-09-24T12:00:00+03:00")
        if not missing_end:
            _child(validity, structure, "csdo", "EndDateTime", "2026-09-24T13:00:00+03:00")

    if role == "CANCEL":
        reg = _child(record, structure, "ipcdo", "RegistrationCancellationDetails")
        _child(reg, structure, "ipsdo", "CancellationTrademarkRegistrationReasonCode", "1")
        complaint = _child(reg, structure, "ipcdo", "ComplaintInvalidateProtectionTrademarkDetails")
        _child(complaint, structure, "ipsdo", "CancellationRegistrationTrademarkCode", "1")
        if not missing_req23:
            _child(complaint, structure, "ipsdo", "SolutionCancellationRegistrationTrademarkCode", "1")
        applicant = _child(complaint, structure, "ipcdo", "ApplicantV2Details")
        comm = _child(applicant, structure, "ccdo", "CommunicationDetails")
        _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
        _child(comm, structure, "csdo", "CommunicationChannelId", "applicant@example.test")
        _child(complaint, structure, "csdo", "EventDate", "2026-09-24")
    return record


def _extract_validate_raw(build):
    engine = _engine()
    structure, root = _raw_root(engine)
    build(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, extraction_issues = engine.body_provider._values_from_element(structure, parsed)
    assert not extraction_issues, [(i.code, i.field_path, i.message) for i in extraction_issues]
    validation = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    return engine, structure, parsed, values, validation


def _rebuild_from_extracted(engine, values):
    body = engine.build_body(MESSAGE, values, mode=GenerationMode.TEST)
    rebuilt = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    extracted, issues = engine.body_provider._values_from_element(structure, rebuilt)
    assert not issues
    validation = engine.validate_body(MESSAGE, extracted, mode=GenerationMode.TEST)
    return rebuilt, extracted, validation


def test_valid_one_cancel_build_serialize_parse_extract_validate():
    engine, structure, parsed, extracted, validation = _build_parse_validate(_valid_one_cancel_values())
    assert parsed.tag == f"{{{structure.namespace}}}TrademarkRegisterDetails"
    assert extracted[f"{STATUS}/csdo:StatusCode"] == "04"
    assert validation.is_valid
    assert validation.is_complete
    assert validation.rule_evaluations and all(item.status is RuleStatus.PASS for item in validation.rule_evaluations)
    transaction = engine.get_transaction(TRANSACTION)
    assert transaction.initiating_message == MESSAGE
    assert engine.build_application_action(TRANSACTION, MESSAGE).serialize().endswith(f"/{MESSAGE}")


def test_invalid_cancel_status_fails_exact_cancel_cardinality():
    values = _valid_one_cancel_values()
    values[f"{STATUS}/csdo:StatusCode"] = "03"
    validation = _engine().validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert not validation.is_valid
    assert "P.SP.02.MSG.020.T53.REQ.2" in _validation_fail_ids(validation)


def test_one_cancel_with_cancellation_indicator_keeps_req3_explicitly_unmapped():
    values = _valid_one_cancel_values()
    values[f"{GOODS}/ipsdo:CancellationStatusIndicator"] = True
    engine, _, _, _, validation = _build_parse_validate(values)
    assert validation.is_valid
    assert all(item.rule_id != "P.SP.02.MSG.020.T53.REQ.3" for item in validation.rule_evaluations)
    assert all(rule["rule_id"] != "P.SP.02.MSG.020.T53.REQ.3" for rule in engine.rules[MESSAGE].structured_rules)


@pytest.mark.parametrize("order", [("CANCEL", "NEW"), ("NEW", "CANCEL")])
def test_valid_two_parent_raw_xml_validates_in_both_orders(order):
    def build(root, structure):
        for role in order:
            _add_record(root, structure, role)

    engine, structure, parsed, values, validation = _extract_validate_raw(build)
    assert parsed.tag == f"{{{structure.namespace}}}TrademarkRegisterDetails"
    assert validation.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in validation.issues]
    assert values[f"{STATUS}/csdo:StatusCode"] == ["04", "01"] if order == ("CANCEL", "NEW") else ["01", "04"]

    rebuilt, extracted, rebuilt_validation = _rebuild_from_extracted(engine, values)
    assert rebuilt.tag == parsed.tag
    assert extracted[f"{STATUS}/csdo:StatusCode"] == values[f"{STATUS}/csdo:StatusCode"]
    assert extracted[REG] == (["", None] if order == ("CANCEL", "NEW") else [None, ""])
    for path in (
        f"{STATUS}/csdo:EventDate",
        f"{P}/ipsdo:TrademarkId",
        RESOURCE,
        f"{VALIDITY}/csdo:StartDateTime",
        f"{VALIDITY}/csdo:EndDateTime",
        f"{P}/ipsdo:IPDocKindCode",
        f"{P}/ipsdo:IPDocKindName",
        ADDRESS,
        COMM,
        ELEMENT,
        f"{ADDRESS}/csdo:UnifiedCountryCode/@codeListId",
        f"{COMPLAINT}/ipcdo:ApplicantV2Details/ccdo:CommunicationDetails/csdo:CommunicationChannelCode",
    ):
        assert extracted.get(path) == values.get(path), path
    assert rebuilt_validation.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in rebuilt_validation.issues]


@pytest.mark.parametrize(
    ("present", "expected"),
    [
        ((True, False), ["", None]),
        ((False, True), [None, ""]),
    ],
)
def test_sparse_cancellation_branch_roundtrip_keeps_parent_ownership(present, expected):
    def build(root, structure):
        for index, enabled in enumerate(present):
            role = "CANCEL" if enabled else "NEW"
            _add_record(root, structure, role)

    engine, _, _, values, validation = _extract_validate_raw(build)
    assert validation.is_valid
    assert values.get(REG) == expected
    rebuilt, extracted, rebuilt_validation = _rebuild_from_extracted(engine, values)
    assert extracted.get(REG) == expected
    assert rebuilt_validation.is_valid, [(i.code, i.rule_id, i.field_path, i.message) for i in rebuilt_validation.issues]


@pytest.mark.parametrize(
    ("roles", "expected"),
    [
        (("CANCEL", "CANCEL"), ["", ""]),
        (("NEW", "NEW"), None),
    ],
)
def test_sparse_cancellation_branch_serializer_handles_both_present_and_both_absent(roles, expected):
    def build(root, structure):
        for role in roles:
            _add_record(root, structure, role)

    engine, structure, _, values, _ = _extract_validate_raw(build)
    rebuilt = engine.body_provider._serialize(structure, values)
    reparsed = ET.fromstring(ET.tostring(rebuilt, encoding="utf-8"))
    extracted, issues = engine.body_provider._values_from_element(structure, reparsed)
    assert not issues
    assert extracted.get(REG) == expected
    reg_qname = f"{{{structure.imported_namespaces['ipcdo']}}}RegistrationCancellationDetails"
    assert len(list(rebuilt.iter(reg_qname))) == (2 if expected is not None else 0)


@pytest.mark.parametrize("missing_index", [0, 1])
def test_required_resource_item_status_missing_in_sparse_parent_fails_structure_validation(missing_index):
    def build(root, structure):
        for index, role in enumerate(("CANCEL", "NEW")):
            _add_record(root, structure, role, missing_resource=index == missing_index)

    _, _, _, values, validation = _extract_validate_raw(build)
    assert values[RESOURCE] == ([None, ""] if missing_index == 0 else ["", None])
    assert any(
        issue.code == "MIN_OCCURS" and issue.field_path == RESOURCE
        for issue in validation.issues
    )


@pytest.mark.parametrize("order", [("CANCEL", "NEW"), ("NEW", "CANCEL")])
def test_bad_cancel_good_new_fails_cancel_only(order):
    def build(root, structure):
        for role in order:
            _add_record(root, structure, role, missing_end=role == "CANCEL")

    _, _, _, _, validation = _extract_validate_raw(build)
    assert not validation.is_valid
    failed = _validation_fail_ids(validation)
    assert "P.SP.02.MSG.020.T53.REQ.22" in failed
    assert "P.SP.02.MSG.020.T53.REQ.4" not in failed


@pytest.mark.parametrize("order", [("CANCEL", "NEW"), ("NEW", "CANCEL")])
def test_good_cancel_bad_new_fails_new_only(order):
    def build(root, structure):
        for role in order:
            _add_record(root, structure, role, missing_event=role == "NEW")

    _, _, _, _, validation = _extract_validate_raw(build)
    assert not validation.is_valid
    failed = _validation_fail_ids(validation)
    assert "P.SP.02.MSG.020.T53.REQ.4" in failed
    assert "P.SP.02.MSG.020.T53.REQ.2" not in failed


def test_wrong_cancel_fallback_document_name_fails_req26():
    def build(root, structure):
        _add_record(root, structure, "CANCEL", fallback="wrong")
        _add_record(root, structure, "NEW", fallback="code")

    _, _, _, _, validation = _extract_validate_raw(build)
    assert "P.SP.02.MSG.020.T53.REQ.26" in _validation_fail_ids(validation)


def test_wrong_new_fallback_document_name_fails_req28():
    def build(root, structure):
        _add_record(root, structure, "CANCEL", fallback="code")
        _add_record(root, structure, "NEW", fallback="wrong")

    _, _, _, _, validation = _extract_validate_raw(build)
    assert "P.SP.02.MSG.020.T53.REQ.28" in _validation_fail_ids(validation)


def test_missing_req23_solution_code_fails_req23():
    def build(root, structure):
        _add_record(root, structure, "CANCEL", missing_req23=True)

    _, _, _, _, validation = _extract_validate_raw(build)
    assert "P.SP.02.MSG.020.T53.REQ.23" in _validation_fail_ids(validation)


def test_inherited_nested_repeatable_bad_second_goods_fails_req16():
    def build(root, structure):
        _add_record(root, structure, "CANCEL", second_bad_goods=True)

    _, _, _, _, validation = _extract_validate_raw(build)
    assert not validation.is_valid
    failures = [
        evaluation
        for evaluation in validation.rule_evaluations
        if evaluation.status is RuleStatus.FAIL
        and len(evaluation.source_refs) == 2
        and evaluation.source_refs[1].get("item") == "16"
    ]
    assert failures


def test_message_code_selects_msg020_rules_and_keeps_msg016_019_exact_one_parent():
    def build(root, structure):
        _add_record(root, structure, "CANCEL")
        _add_record(root, structure, "NEW")

    engine, _, _, values, msg020 = _extract_validate_raw(build)
    assert msg020.is_valid
    assert all(
        not (item.rule_id == "P.SP.02.MSG.020.T53.REQ.1" and item.status is RuleStatus.FAIL)
        for item in msg020.rule_evaluations
    )

    for message in ("P.SP.02.MSG.016", "P.SP.02.MSG.017", "P.SP.02.MSG.018", "P.SP.02.MSG.019"):
        validation = engine.validate_body(message, deepcopy(values), mode=GenerationMode.TEST)
        assert any(
            item.rule_id == f"{message}.REQ.2" and item.status is RuleStatus.FAIL
            for item in validation.rule_evaluations
        ), message


def test_status03_and_05_are_not_cancel_for_msg020():
    for status in ("03", "05"):
        def build(root, structure, status=status):
            _add_record(root, structure, "CANCEL", status_code=status)

        _, _, _, _, validation = _extract_validate_raw(build)
        assert any(
            item.rule_id == "P.SP.02.MSG.020.T53.REQ.2" and item.status is RuleStatus.FAIL
            for item in validation.rule_evaluations
        )
