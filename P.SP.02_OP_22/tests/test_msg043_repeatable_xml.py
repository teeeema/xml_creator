import copy
import json
from pathlib import Path

from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.043"
APP = "ipcdo:TrademarkApplicationDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
PATENT = f"{APP}/ipcdo:PatentAuthorityDetails"
CORR = f"{APP}/ipcdo:CorrespondenceAddressDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
SIGNATURE = f"{APP}/ipcdo:SignatureDetails"
OFFICER = f"{SIGNATURE}/ipcdo:OfficerDetails"
OFFICER_NAME = f"{OFFICER}/ccdo:FullNameDetails"
VALIDITY = "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails"


def raw_rules():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))["structured_rules"]


def rule(code, suffix=""):
    rule_id = f"{MESSAGE}.T61.REQ.{code}{suffix}"
    return next(item for item in raw_rules() if item["rule_id"] == rule_id)


def base_valid_values():
    # Index 0: Role A (StatusCode 02); Index 1: Role B (StatusCode 01)
    return {
        "ccdo:EDocHeader": "",
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000043",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T14:00:00+03:00",
        APP: ["", ""],
        f"{APP}/ipsdo:ApplicationReceiptDate": ["2026-09-30", "2026-09-30"],
        f"{APP}/ipsdo:TrademarkApplicationId": ["2026/RU-000001", "2026/RU-000002"],
        f"{APP}/ipsdo:SourceTrademarkApplicationId": [None, "2026/RU-000001"],
        STATUS: ["", ""],
        f"{STATUS}/csdo:StatusCode": ["02", "01"],
        PATENT: [None, ""],
        f"{PATENT}/csdo:AuthorityName": [None, "Роспатент"],
        f"{PATENT}/ipsdo:OriginOfficeIndicator": [None, "1"],
        f"{PATENT}/csdo:UnifiedCountryCode": [None, "RU"],
        f"{PATENT}/csdo:UnifiedCountryCode/@codeListId": [None, "ВОИС ST.3"],
        f"{PATENT}/ccdo:SubjectAddressDetails": [None, ""],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": [None, "2"],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode": [None, "RU"],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode/@codeListId": [None, "ВОИС ST.3"],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:CityName": [None, "Москва"],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:StreetName": [None, "Бережковская наб."],
        f"{PATENT}/ccdo:SubjectAddressDetails/csdo:BuildingNumberId": [None, "30"],
        CORR: [None, ""],
        f"{CORR}/ccdo:SubjectAddressDetails": [None, ""],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": [None, "3"],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode": [None, "RU"],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode/@codeListId": [None, "ВОИС ST.3"],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:CityName": [None, "Москва"],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:StreetName": [None, "Ленина"],
        f"{CORR}/ccdo:SubjectAddressDetails/csdo:BuildingNumberId": [None, "10"],
        f"{CORR}/ccdo:CommunicationDetails": [None, ""],
        f"{CORR}/ccdo:CommunicationDetails/csdo:CommunicationChannelCode": [None, "EM"],
        f"{CORR}/ccdo:CommunicationDetails/csdo:CommunicationChannelId": [None, "corr@example.com"],
        PARTY: [None, ""],
        f"{PARTY}/ipsdo:IPPartyKindCode": [None, "AP"],
        f"{PARTY}/csdo:UnifiedCountryCode": [None, "RU"],
        f"{PARTY}/csdo:UnifiedCountryCode/@codeListId": [None, "ВОИС ST.3"],
        f"{PARTY}/ipsdo:IPSubjectName": [None, "Заявитель"],
        f"{PARTY}/ipsdo:IPSubjectName/@nameRepresentationKindCode": [None, "OR"],
        f"{PARTY}/ipsdo:IPSubjectName/@languageCode": [None, "RU"],
        f"{PARTY}/ccdo:SubjectAddressDetails": [None, ""],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": [None, "2"],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode": [None, "RU"],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode/@codeListId": [None, "ВОИС ST.3"],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:CityName": [None, "Москва"],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:StreetName": [None, "Тверская"],
        f"{PARTY}/ccdo:SubjectAddressDetails/csdo:BuildingNumberId": [None, "1"],
        f"{PARTY}/ccdo:CommunicationDetails": [None, ""],
        f"{PARTY}/ccdo:CommunicationDetails/csdo:CommunicationChannelCode": [None, "EM"],
        f"{PARTY}/ccdo:CommunicationDetails/csdo:CommunicationChannelId": [None, "applicant@example.com"],
        TM: [None, ""],
        f"{TM}/ipsdo:TrademarkKindCode": [None, "110"],
        f"{TM}/ipsdo:TrademarkKindName": [None, "Словесный знак"],
        f"{TM}/ipsdo:CollectiveMarkIndicator": [None, "0"],
        f"{TM}/ipcdo:TMDescriptionDetails": [None, ""],
        f"{TM}/ipcdo:TMDescriptionDetails/csdo:DescriptionText": [None, "Описание знака"],
        GOODS: [None, ""],
        f"{GOODS}/ipsdo:GoodsClassCode": [None, "01"],
        f"{GOODS}/ipsdo:GoodsClassName": [None, "Класс 01"],
        f"{GOODS}/ipsdo:GoodsName": [None, "Химические продукты"],
        SIGNATURE: ["", ""],
        f"{SIGNATURE}/csdo:DocCreationDate": ["2026-09-30", "2026-09-30"],
        OFFICER: ["", None],
        OFFICER_NAME: ["", None],
        f"{OFFICER_NAME}/csdo:LastName": ["Петров", None],
        f"{OFFICER_NAME}/csdo:FirstName": ["Петр", None],
        f"{OFFICER}/csdo:PositionName": ["Эксперт", None],
        f"{SIGNATURE}/ccdo:FullNameDetails": [None, ""],
        f"{SIGNATURE}/ccdo:FullNameDetails/csdo:LastName": [None, "Иванов"],
        f"{SIGNATURE}/ccdo:FullNameDetails/csdo:FirstName": [None, "Иван"],
        "ccdo:ResourceItemStatusDetails": "",
        "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails": "",
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T14:01:00+03:00",
    }


def reversed_valid_values():
    # Index 0: Role B (StatusCode 01); Index 1: Role A (StatusCode 02)
    val = base_valid_values()
    for path, v in list(val.items()):
        if isinstance(v, list) and len(v) == 2 and path not in {APP, f"{APP}/ipsdo:ApplicationReceiptDate", SIGNATURE, f"{SIGNATURE}/csdo:DocCreationDate"}:
            val[path] = [v[1], v[0]]
    return val


def test_req1_exactly_two_applications():
    evaluator = StructuredRuleEvaluator()
    r = rule(1)
    # 0 applications -> FAIL
    assert evaluator.evaluate(r, {APP: []}).status is RuleStatus.FAIL
    # 1 application -> FAIL
    assert evaluator.evaluate(r, {APP: [{}]}).status is RuleStatus.FAIL
    # 2 applications -> PASS
    assert evaluator.evaluate(r, {APP: [{}, {}]}).status is RuleStatus.PASS
    # 3 applications -> FAIL
    assert evaluator.evaluate(r, {APP: [{}, {}, {}]}).status is RuleStatus.FAIL


def test_reversed_xml_order_identical_semantic_result():
    evaluator = StructuredRuleEvaluator()
    rules = raw_rules()

    values_a = base_valid_values()
    results_a = [evaluator.evaluate(r, values_a).status for r in rules]

    values_b = reversed_valid_values()
    results_b = [evaluator.evaluate(r, values_b).status for r in rules]

    assert results_a == [RuleStatus.PASS] * len(rules)
    assert results_b == [RuleStatus.PASS] * len(rules)
    assert results_a == results_b


def test_req30_cross_instance_comparison_evaluation():
    evaluator = StructuredRuleEvaluator()
    r30 = rule(30)

    # Matching values -> PASS
    values = base_valid_values()
    assert evaluator.evaluate(r30, values).status == RuleStatus.PASS

    # Mismatching values -> FAIL
    mismatch_values = copy.deepcopy(values)
    mismatch_values[f"{APP}/ipsdo:SourceTrademarkApplicationId"] = [None, "2026/RU-DIFFERENT"]
    assert evaluator.evaluate(r30, mismatch_values).status == RuleStatus.FAIL

    # Reversed order matching -> PASS
    rev_values = reversed_valid_values()
    assert evaluator.evaluate(r30, rev_values).status == RuleStatus.PASS


def test_req26_inclusive_or_truth_table():
    evaluator = StructuredRuleEvaluator()
    r26 = rule(26)

    # True, True -> PASS
    val_tt = base_valid_values()
    assert evaluator.evaluate(r26, val_tt).status == RuleStatus.PASS

    # True, False (Valid Code, Unknown Name) -> PASS
    val_tf = base_valid_values()
    val_tf[f"{TM}/ipsdo:TrademarkKindName"] = [None, "Неизвестный вид знака"]
    assert evaluator.evaluate(r26, val_tf).status == RuleStatus.PASS

    # False, True (Unknown Code, Valid Name) -> PASS
    val_ft = base_valid_values()
    val_ft[f"{TM}/ipsdo:TrademarkKindCode"] = [None, "999"]
    assert evaluator.evaluate(r26, val_ft).status == RuleStatus.PASS

    # False, False (Unknown Code, Unknown Name) -> FAIL
    val_ff = base_valid_values()
    val_ff[f"{TM}/ipsdo:TrademarkKindCode"] = [None, "999"]
    val_ff[f"{TM}/ipsdo:TrademarkKindName"] = [None, "Неизвестный вид знака"]
    assert evaluator.evaluate(r26, val_ff).status == RuleStatus.FAIL

    # Both missing -> FAIL
    val_none = base_valid_values()
    val_none[f"{TM}/ipsdo:TrademarkKindCode"] = [None, None]
    val_none[f"{TM}/ipsdo:TrademarkKindName"] = [None, None]
    assert evaluator.evaluate(r26, val_none).status == RuleStatus.FAIL


def test_parent_context_child_isolation():
    evaluator = StructuredRuleEvaluator()
    r28 = rule(28)

    # Invalid value under Role A (StatusCode 02) must NOT fail the rule
    values = base_valid_values()
    values[f"{TM}/ipsdo:CollectiveMarkIndicator"] = ["INVALID_VALUE", "0"]
    assert evaluator.evaluate(r28, values).status == RuleStatus.PASS

    # Invalid value under Role B (StatusCode 01) MUST fail the rule
    values_b_invalid = base_valid_values()
    values_b_invalid[f"{TM}/ipsdo:CollectiveMarkIndicator"] = ["0", "INVALID_VALUE"]
    assert evaluator.evaluate(r28, values_b_invalid).status == RuleStatus.FAIL


def test_semantic_role_uniqueness_and_attribute():
    evaluator = StructuredRuleEvaluator()
    r_role01 = rule(32, ".ROLE01")
    r_role02 = rule(32, ".ROLE02")
    r_attr = rule(32, ".ATTR")

    # Valid: one 01, one 02, no codeListId on 02
    val = base_valid_values()
    assert evaluator.evaluate(r_role01, val).status == RuleStatus.PASS
    assert evaluator.evaluate(r_role02, val).status == RuleStatus.PASS
    assert evaluator.evaluate(r_attr, val).status == RuleStatus.PASS

    # Duplicate 01 (two 01s, zero 02s) -> both fail
    val_dup01 = copy.deepcopy(val)
    val_dup01[f"{STATUS}/csdo:StatusCode"] = ["01", "01"]
    assert evaluator.evaluate(r_role01, val_dup01).status == RuleStatus.FAIL
    assert evaluator.evaluate(r_role02, val_dup01).status == RuleStatus.FAIL

    # Role A has forbidden codeListId -> ATTR fails
    val_with_attr = copy.deepcopy(val)
    val_with_attr[f"{STATUS}/csdo:StatusCode/@codeListId"] = ["SOME_LIST", None]
    assert evaluator.evaluate(r_attr, val_with_attr).status == RuleStatus.FAIL


def test_validity_dates_req33_and_req34():
    evaluator = StructuredRuleEvaluator()
    r33 = rule(33)
    r34 = rule(34)

    # StartDateTime present, EndDateTime absent -> both PASS
    valid = {
        "ccdo:ResourceItemStatusDetails": [{}],
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T14:00:00+03:00",
    }
    assert evaluator.evaluate(r33, valid).status is RuleStatus.PASS
    assert evaluator.evaluate(r34, valid).status is RuleStatus.PASS

    # Missing StartDateTime -> REQ33 FAIL
    missing_start = {"ccdo:ResourceItemStatusDetails": [{}]}
    assert evaluator.evaluate(r33, missing_start).status is RuleStatus.FAIL

    # Wrong owner StartDateTime -> REQ33 FAIL
    wrong_owner_start = {
        "ccdo:ResourceItemStatusDetails": [{}],
        "other:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime": "2026-09-30T14:00:00+03:00",
    }
    assert evaluator.evaluate(r33, wrong_owner_start).status is RuleStatus.FAIL

    # EndDateTime present in governed owner -> REQ34 FAIL
    with_end = dict(valid, **{f"{VALIDITY}/csdo:EndDateTime": "2026-10-01T14:00:00+03:00"})
    assert evaluator.evaluate(r34, with_end).status is RuleStatus.FAIL


def test_req35_37_signature_branches_and_officers_same_parent():
    evaluator = StructuredRuleEvaluator()
    r35_pres = rule(35, ".PRESENCE")
    r35_branch = rule(35, ".BRANCH")
    r36 = rule(36)
    r37 = rule(37)

    # 0 signatures -> FAIL
    assert evaluator.evaluate(r35_pres, {SIGNATURE: []}).status is RuleStatus.FAIL

    # Distinct signatures: one with OfficerDetails, one with FullNameDetails -> PASS
    separate = {
        SIGNATURE: [{}, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, None],
        f"{SIGNATURE}/ccdo:FullNameDetails": [None, {}],
    }
    assert evaluator.evaluate(r35_pres, separate).status is RuleStatus.PASS
    assert evaluator.evaluate(r35_branch, separate).status is RuleStatus.PASS
    assert evaluator.evaluate(r36, separate).status is RuleStatus.PASS

    # Mutual exclusion violation within same signature -> FAIL
    same_parent_conflict = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ccdo:FullNameDetails": [{}],
    }
    assert evaluator.evaluate(r35_branch, same_parent_conflict).status is RuleStatus.FAIL
    assert evaluator.evaluate(r36, same_parent_conflict).status is RuleStatus.FAIL

    # OfficerDetails valid required fields (REQ 37)
    valid_officer = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Петров"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Петр"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
    }
    assert evaluator.evaluate(r37, valid_officer).status is RuleStatus.PASS

    # Missing LastName -> FAIL
    missing_last = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": [None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Петр"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
    }
    assert evaluator.evaluate(r37, missing_last).status is RuleStatus.FAIL

    # Missing FirstName -> FAIL
    missing_first = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Петров"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": [None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
    }
    assert evaluator.evaluate(r37, missing_first).status is RuleStatus.FAIL

    # Missing PositionName -> FAIL
    missing_pos = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Петров"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Петр"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": [None],
    }
    assert evaluator.evaluate(r37, missing_pos).status is RuleStatus.FAIL

    # CommunicationDetails forbidden in OfficerDetails -> FAIL
    with_comm = dict(valid_officer, **{f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:CommunicationDetails": [{}]})
    assert evaluator.evaluate(r37, with_comm).status is RuleStatus.FAIL

    # Repeatable officers: one good, one bad -> FAIL
    mixed_officers = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["А", None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Б", "В"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["П", "П"],
    }
    assert evaluator.evaluate(r37, mixed_officers).status is RuleStatus.FAIL


def test_signature_rules_across_two_applications():
    evaluator = StructuredRuleEvaluator()
    r35_pres = rule(35, ".PRESENCE")
    r35_branch = rule(35, ".BRANCH")
    r36 = rule(36)
    r37 = rule(37)

    # Both applications have valid signatures (one officer, one full name)
    values = {
        APP: [{}, {}],
        SIGNATURE: [{}, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов", None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван", None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Инспектор", None],
        f"{SIGNATURE}/ccdo:FullNameDetails": [None, {}],
    }
    assert evaluator.evaluate(r35_pres, values).status is RuleStatus.PASS
    assert evaluator.evaluate(r35_branch, values).status is RuleStatus.PASS
    assert evaluator.evaluate(r36, values).status is RuleStatus.PASS
    assert evaluator.evaluate(r37, values).status is RuleStatus.PASS

    # Second application has conflicting Officer + FullNameDetails in its signature -> FAIL
    conflict_values = {
        APP: [{}, {}],
        SIGNATURE: [{}, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов", "Петров"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван", "Петр"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Инспектор", "Эксперт"],
        f"{SIGNATURE}/ccdo:FullNameDetails": [None, {}],
    }
    assert evaluator.evaluate(r35_branch, conflict_values).status is RuleStatus.FAIL
    assert evaluator.evaluate(r36, conflict_values).status is RuleStatus.FAIL
