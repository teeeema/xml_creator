import copy
import json
from pathlib import Path

from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.012"
APP = "ipcdo:TrademarkApplicationDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
PATENT = f"{APP}/ipcdo:PatentAuthorityDetails"
CORR = f"{APP}/ipcdo:CorrespondenceAddressDetails"
TM = f"{APP}/ipcdo:TrademarkDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
VALIDITY = "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails"


def raw_rules():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))["structured_rules"]


def base_valid_values():
    # Index 0: Role A (02); Index 1: Role B (01)
    return {
        "ccdo:EDocHeader": "",
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": "R.IP.SP.02.002",
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000012",
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
        "ccdo:ResourceItemStatusDetails": "",
        "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails": "",
        f"{VALIDITY}/csdo:StartDateTime": "2026-09-30T14:01:00+03:00",
    }


def reversed_valid_values():
    # Index 0: Role B (01); Index 1: Role A (02)
    val = base_valid_values()
    for path, v in list(val.items()):
        if isinstance(v, list) and len(v) == 2 and path not in {APP, f"{APP}/ipsdo:ApplicationReceiptDate"}:
            val[path] = [v[1], v[0]]
    return val


def test_cardinality_two_applications_passes():
    evaluator = StructuredRuleEvaluator()
    rules = raw_rules()
    r1 = next(r for r in rules if r["rule_id"] == f"{MESSAGE}.T45.REQ.1")
    values = base_valid_values()
    result = evaluator.evaluate(r1, values)
    assert result.status == RuleStatus.PASS


def test_cardinality_one_application_fails():
    evaluator = StructuredRuleEvaluator()
    rules = raw_rules()
    r1 = next(r for r in rules if r["rule_id"] == f"{MESSAGE}.T45.REQ.1")
    values = base_valid_values()
    values[APP] = [None]
    result = evaluator.evaluate(r1, values)
    assert result.status == RuleStatus.FAIL


def test_cardinality_three_applications_fails():
    evaluator = StructuredRuleEvaluator()
    rules = raw_rules()
    r1 = next(r for r in rules if r["rule_id"] == f"{MESSAGE}.T45.REQ.1")
    values = base_valid_values()
    values[APP] = [None, None, None]
    result = evaluator.evaluate(r1, values)
    assert result.status == RuleStatus.FAIL


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
    r30 = next(r for r in raw_rules() if r["rule_id"] == f"{MESSAGE}.T45.REQ.30")

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
    r26 = next(r for r in raw_rules() if r["rule_id"] == f"{MESSAGE}.T45.REQ.26")

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
    r28 = next(r for r in raw_rules() if r["rule_id"] == f"{MESSAGE}.T45.REQ.28")

    # Invalid value under Role A (02) must NOT fail the rule
    values = base_valid_values()
    values[f"{TM}/ipsdo:CollectiveMarkIndicator"] = ["INVALID_VALUE", "0"]
    assert evaluator.evaluate(r28, values).status == RuleStatus.PASS

    # Invalid value under Role B (01) MUST fail the rule
    values_b_invalid = base_valid_values()
    values_b_invalid[f"{TM}/ipsdo:CollectiveMarkIndicator"] = ["0", "INVALID_VALUE"]
    assert evaluator.evaluate(r28, values_b_invalid).status == RuleStatus.FAIL


def test_semantic_role_uniqueness():
    evaluator = StructuredRuleEvaluator()
    r_role01 = next(r for r in raw_rules() if r["rule_id"] == f"{MESSAGE}.T45.REQ.31.ROLE01")
    r_role02 = next(r for r in raw_rules() if r["rule_id"] == f"{MESSAGE}.T45.REQ.31.ROLE02")

    # Valid: one 01, one 02
    val = base_valid_values()
    assert evaluator.evaluate(r_role01, val).status == RuleStatus.PASS
    assert evaluator.evaluate(r_role02, val).status == RuleStatus.PASS

    # Duplicate 01 (two 01s, zero 02s)
    val_dup01 = copy.deepcopy(val)
    val_dup01[f"{STATUS}/csdo:StatusCode"] = ["01", "01"]
    assert evaluator.evaluate(r_role01, val_dup01).status == RuleStatus.FAIL
    assert evaluator.evaluate(r_role02, val_dup01).status == RuleStatus.FAIL


def test_resource_validity_start_datetime_required():
    evaluator = StructuredRuleEvaluator()
    rules = raw_rules()
    r33 = next(r for r in rules if r["rule_id"] == f"{MESSAGE}.T45.REQ.33")

    values = base_valid_values()
    assert evaluator.evaluate(r33, values).status == RuleStatus.PASS

    del values[f"{VALIDITY}/csdo:StartDateTime"]
    assert evaluator.evaluate(r33, values).status == RuleStatus.FAIL


def test_resource_validity_end_datetime_forbidden():
    evaluator = StructuredRuleEvaluator()
    rules = raw_rules()
    r34 = next(r for r in rules if r["rule_id"] == f"{MESSAGE}.T45.REQ.34")

    values = base_valid_values()
    assert evaluator.evaluate(r34, values).status == RuleStatus.PASS

    values[f"{VALIDITY}/csdo:EndDateTime"] = "2026-10-01T14:00:00+03:00"
    assert evaluator.evaluate(r34, values).status == RuleStatus.FAIL


def test_no_positional_status_rules():
    rules = raw_rules()
    for rule in rules:
        rule_str = json.dumps(rule)
        assert "[0]" not in rule_str
        assert "[1]" not in rule_str
        assert "first" not in rule_str
        assert "second" not in rule_str
