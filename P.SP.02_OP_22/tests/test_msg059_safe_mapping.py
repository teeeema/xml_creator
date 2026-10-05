import json
from pathlib import Path
import pytest

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.059"

ALLOWED_EXTENSIONS = [
    "tif", "tiff", "bmp", "jpg", "jpeg", "png", "gif", "doc", "docx", "rtf", "pdf"
]

T78_FULL = {1, 2, 3}
T78_PARTIAL = {4}
T78_AMBIGUOUS = {5}

T79_FULL = {1, 2, 3}
T79_PARTIAL = {4}
T79_AMBIGUOUS = {5}


def _raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def _rules(table, code):
    rid = f"{MESSAGE}.T{table}.REQ.{code}"
    return [rule for rule in _raw()["structured_rules"] if rule["rule_id"] == rid]


def _inventory(table, code):
    return next(
        item
        for item in _raw()["mapping_audit"]["inventory"]
        if item["table"] == str(table) and item["requirement_code"] == str(code)
    )


def test_expanded_normative_inventory_has_exactly_11_distinct_requirements():
    inventory = _raw()["mapping_audit"]["inventory"]
    identities = {(item["table"], item["branch"], item["requirement_code"]) for item in inventory}
    assert len(inventory) == len(identities) == 11
    assert _raw()["mapping_audit"]["expanded_requirement_count"] == 11
    assert _raw()["mapping_audit"]["captured_row_count"] == 11
    assert {(item["table"], item["branch"]) for item in inventory} == {
        ("77", "R.010"),
        ("78", "R.IP.SP.02.002"),
        ("79", "R.IP.SP.02.007"),
    }


def test_mapping_classification_counts_and_arithmetic():
    audit = _raw()["mapping_audit"]
    counts = audit["counts"]
    assert counts == {
        "FULLY_MAPPABLE": 7,
        "SAFE_PARTIAL": 2,
        "EXTERNAL": 0,
        "AMBIGUOUS": 2,
        "ENGINE_UNSUPPORTED": 0,
        "SOURCE_CONFLICT": 0,
    }
    assert sum(counts.values()) == audit["expanded_requirement_count"] == 11
    assert audit["classification_counts"] == counts

    assert audit["summary"] == {
        "table77": {"FULLY_MAPPABLE": [1]},
        "table78": {
            "FULLY_MAPPABLE": sorted(T78_FULL),
            "SAFE_PARTIAL": sorted(T78_PARTIAL),
            "AMBIGUOUS": sorted(T78_AMBIGUOUS),
        },
        "table79": {
            "FULLY_MAPPABLE": sorted(T79_FULL),
            "SAFE_PARTIAL": sorted(T79_PARTIAL),
            "AMBIGUOUS": sorted(T79_AMBIGUOUS),
        },
    }


def test_table77_uses_existing_one_of_infrastructure():
    messages = json.loads((PACKAGE / "messages.yaml").read_text(encoding="utf-8"))["messages"]
    definition = next(item for item in messages if item["message_code"] == MESSAGE)
    assert definition["structure_id"] == "R.010"
    assert definition["embedded_structures"] == {
        "selection": "ONE_OF",
        "structures": ["R.IP.SP.02.002", "R.IP.SP.02.007"],
    }
    item = _inventory(77, 1)
    assert item["classification"] == "FULLY_MAPPABLE"
    assert item["mapping_status"] == "INFRASTRUCTURE_EXECUTABLE"
    assert not any(".T77." in rule["rule_id"] for rule in _raw()["structured_rules"])


def test_structured_rules_count_and_scope():
    rules = _raw()["structured_rules"]
    assert len(rules) == 8
    assert all(rule["rule_id"].startswith(MESSAGE + ".") for rule in rules)
    assert {rule["applies_to_structure"] for rule in rules} == {
        "R.IP.SP.02.002",
        "R.IP.SP.02.007",
    }
    assert sum(1 for r in rules if r["applies_to_structure"] == "R.IP.SP.02.002") == 4
    assert sum(1 for r in rules if r["applies_to_structure"] == "R.IP.SP.02.007") == 4
    assert all(
        (".T78." in rule["rule_id"]) == (rule["applies_to_structure"] == "R.IP.SP.02.002")
        for rule in rules
    )
    assert all(
        (".T79." in rule["rule_id"]) == (rule["applies_to_structure"] == "R.IP.SP.02.007")
        for rule in rules
    )


def test_r002_t78_req1_and_req2_presence():
    evaluator = StructuredRuleEvaluator()
    rule_req1 = _rules(78, 1)[0]
    rule_req2 = _rules(78, 2)[0]

    # Valid context
    valid_values = {
        "ipcdo:TrademarkApplicationDetails": [""],
        "ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId": ["APP-001"],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails": [""],
    }
    assert evaluator.evaluate(rule_req1, valid_values).status == RuleStatus.PASS
    assert evaluator.evaluate(rule_req2, valid_values).status == RuleStatus.PASS

    # Missing TrademarkApplicationId
    bad_id = {
        "ipcdo:TrademarkApplicationDetails": [""],
        "ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId": [None],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails": [""],
    }
    assert evaluator.evaluate(rule_req1, bad_id).status == RuleStatus.FAIL

    # Missing AccompanyingDocumentsDetails
    bad_doc = {
        "ipcdo:TrademarkApplicationDetails": [""],
        "ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId": ["APP-001"],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails": [None],
    }
    assert evaluator.evaluate(rule_req2, bad_doc).status == RuleStatus.FAIL


@pytest.mark.parametrize(
    ("kind_code", "kind_name", "expected_pass"),
    [
        ("07015", "Документ", True),   # TT
        ("07015", None, True),         # TF
        (None, "Документ", True),       # FT
        (None, None, False),           # FF
    ],
)
def test_r002_t78_req3_inclusive_or_truth_table(kind_code, kind_name, expected_pass):
    evaluator = StructuredRuleEvaluator()
    rule_req3 = _rules(78, 3)[0]

    values = {
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails": [""],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindCode": [kind_code],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindName": [kind_name],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocName": ["DocName"],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId": ["DOC-123"],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocCreationDate": ["2026-09-30"],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText": ["dGVzdA=="],
    }
    status = evaluator.evaluate(rule_req3, values).status
    if expected_pass:
        assert status == RuleStatus.PASS
    else:
        assert status == RuleStatus.FAIL


@pytest.mark.parametrize(
    "missing_field",
    [
        "csdo:DocName",
        "csdo:DocId",
        "csdo:DocCreationDate",
        "csdo:DocBinaryText",
    ],
)
def test_r002_t78_req3_mandatory_fields_fail_when_missing(missing_field):
    evaluator = StructuredRuleEvaluator()
    rule_req3 = _rules(78, 3)[0]

    values = {
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails": [""],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindCode": ["07015"],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindName": [None],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocName": ["DocName"],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId": ["DOC-123"],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocCreationDate": ["2026-09-30"],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText": ["dGVzdA=="],
    }
    values[f"ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/{missing_field}"] = [None]
    assert evaluator.evaluate(rule_req3, values).status == RuleStatus.FAIL


@pytest.mark.parametrize("ext", ALLOWED_EXTENSIONS)
def test_r002_t78_req4_allowed_extensions_pass(ext):
    evaluator = StructuredRuleEvaluator()
    rule_req4 = _rules(78, 4)[0]

    values = {
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails": [""],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText": ["dGVzdA=="],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText/@mediaTypeCode": [ext],
    }
    assert evaluator.evaluate(rule_req4, values).status == RuleStatus.PASS


@pytest.mark.parametrize("bad_ext", ["exe", "zip", "txt", "mp3", "sh", "bat", ""])
def test_r002_t78_req4_disallowed_extensions_fail(bad_ext):
    evaluator = StructuredRuleEvaluator()
    rule_req4 = _rules(78, 4)[0]

    values = {
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails": [""],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText": ["dGVzdA=="],
        "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText/@mediaTypeCode": [bad_ext],
    }
    assert evaluator.evaluate(rule_req4, values).status == RuleStatus.FAIL


def test_r007_t79_req1_and_req2_presence():
    evaluator = StructuredRuleEvaluator()
    rule_req1 = _rules(79, 1)[0]
    rule_req2 = _rules(79, 2)[0]

    valid_values = {
        "ipcdo:UnifiedRegisterRecordsDetails": [""],
        "ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId": ["TM-001"],
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails": [""],
    }
    assert evaluator.evaluate(rule_req1, valid_values).status == RuleStatus.PASS
    assert evaluator.evaluate(rule_req2, valid_values).status == RuleStatus.PASS

    bad_id = {
        "ipcdo:UnifiedRegisterRecordsDetails": [""],
        "ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId": [None],
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails": [""],
    }
    assert evaluator.evaluate(rule_req1, bad_id).status == RuleStatus.FAIL

    bad_doc = {
        "ipcdo:UnifiedRegisterRecordsDetails": [""],
        "ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId": ["TM-001"],
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails": [None],
    }
    assert evaluator.evaluate(rule_req2, bad_doc).status == RuleStatus.FAIL


@pytest.mark.parametrize(
    ("kind_code", "kind_name", "expected_pass"),
    [
        ("07015", "Документ", True),   # TT
        ("07015", None, True),         # TF
        (None, "Документ", True),       # FT
        (None, None, False),           # FF
    ],
)
def test_r007_t79_req3_inclusive_or_truth_table(kind_code, kind_name, expected_pass):
    evaluator = StructuredRuleEvaluator()
    rule_req3 = _rules(79, 3)[0]

    values = {
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails": [""],
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindCode": [kind_code],
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindName": [kind_name],
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocName": ["DocName"],
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId": ["DOC-123"],
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocCreationDate": ["2026-09-30"],
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText": ["dGVzdA=="],
    }
    status = evaluator.evaluate(rule_req3, values).status
    if expected_pass:
        assert status == RuleStatus.PASS
    else:
        assert status == RuleStatus.FAIL


@pytest.mark.parametrize("ext", ALLOWED_EXTENSIONS)
def test_r007_t79_req4_allowed_extensions_pass(ext):
    evaluator = StructuredRuleEvaluator()
    rule_req4 = _rules(79, 4)[0]

    values = {
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails": [""],
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText": ["dGVzdA=="],
        "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText/@mediaTypeCode": [ext],
    }
    assert evaluator.evaluate(rule_req4, values).status == RuleStatus.PASS


def test_ambiguous_requirements_are_unmapped_with_documented_rationale():
    inv78_5 = _inventory(78, 5)
    assert inv78_5["classification"] == "AMBIGUOUS"
    assert inv78_5["mapping_status"] == "UNMAPPED"
    assert inv78_5["engine_gap"] == "CLOSED_WORLD_NEGATIVE_CONSTRAINTS_NOT_SUPPORTED"

    inv79_5 = _inventory(79, 5)
    assert inv79_5["classification"] == "AMBIGUOUS"
    assert inv79_5["mapping_status"] == "UNMAPPED"
    assert inv79_5["engine_gap"] == "CLOSED_WORLD_NEGATIVE_CONSTRAINTS_NOT_SUPPORTED"

    assert not any(".REQ.5" in rule["rule_id"] for rule in _raw()["structured_rules"])
