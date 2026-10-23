from __future__ import annotations

import csv
import importlib.util
from collections import Counter
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SUPPORT_PATH = Path(__file__).with_name("proof_completion_support.py")
MATRIX_PATH = (
    ROOT
    / "codex_reports/OP22_P_SP_02/FINAL_MAPPED_PROOF/OP22_OLD_OPEN261_PROOF_MATRIX.csv"
)
BLOCKED_PATH = ROOT / "codex_reports/OP22_P_SP_02/FINAL_MAPPED_PROOF/OP22_FINAL_BLOCKED85.csv"

support_spec = importlib.util.spec_from_file_location("op22_old_open261_support", SUPPORT_PATH)
assert support_spec is not None and support_spec.loader is not None
support = importlib.util.module_from_spec(support_spec)
support_spec.loader.exec_module(support)

with MATRIX_PATH.open(encoding="utf-8-sig", newline="") as stream:
    MATRIX_ROWS = list(csv.DictReader(stream))
with BLOCKED_PATH.open(encoding="utf-8-sig", newline="") as stream:
    BLOCKED_ROWS = list(csv.DictReader(stream))

RECONCILIATION = {row["canonical_id"]: row for row in support.load_reconciliation_rows()}

assert len(MATRIX_ROWS) == 261
assert Counter(row["closure_verdict"] for row in MATRIX_ROWS) == Counter(
    {
        "FULL_PROOF_CLOSED": 141,
        "CONDITIONAL_INACTIVE": 1,
        "SEMANTIC_REVIEW_REQUIRED": 98,
        "PROOF_INCOMPLETE": 21,
    }
)
assert len(BLOCKED_ROWS) == 85
assert "P.SP.02.MSG.031:49:19" not in {row["canonical_id"] for row in MATRIX_ROWS}
table49_req19 = [row for row in BLOCKED_ROWS if row["canonical_id"] == "P.SP.02.MSG.031:49:19"]
assert len(table49_req19) == 1
assert table49_req19[0]["remaining_category"] == "CLASSIFIER"


@pytest.mark.parametrize("proof_row", MATRIX_ROWS, ids=lambda row: row["canonical_id"])
def test_old_open_now_mapped_requirement_matches_strict_proof_verdict(proof_row):
    row = RECONCILIATION[proof_row["canonical_id"]]
    assert row["old_open_now_has_mapping"] == "YES"
    assert row["rule_status"] == proof_row["production_rule_status"]
    assert row["current_rule_or_mechanism"] == proof_row["production_rule_or_mechanism"]

    if proof_row["closure_verdict"] == "CONDITIONAL_INACTIVE":
        _prove_current_classifier_disables_fallback(row)
        return

    if proof_row["closure_verdict"] == "FULL_PROOF_CLOSED":
        if row["rule_status"] == "RULE_EXISTS_AGGREGATED":
            ok, results, errors = support.prove_aggregated_requirement(row)
        else:
            ok, results, errors = support.prove_requirement(row)
        assert ok, f"{row['canonical_id']}: {errors}"
        assert results
        assert all(item["positive_status"] == "PASS" for item in results)
        assert all(item["negative_status"] == "FAIL" for item in results)
        return

    assert row["rule_status"] == "RULE_EXISTS_AGGREGATED"
    strict_ok, strict_results, strict_errors = support.prove_aggregated_requirement(row)
    assert not strict_ok
    assert strict_results == []
    assert strict_errors == ["NO_ATOMIC_SOURCE_LINK"]

    range_ok, range_results, range_errors = support.prove_requirement(row)
    assert range_results
    if proof_row["closure_verdict"] == "SEMANTIC_REVIEW_REQUIRED":
        assert range_ok, f"{row['canonical_id']}: {range_errors}"
        assert all(item["positive_status"] == "PASS" for item in range_results)
        assert all(item["negative_status"] == "FAIL" for item in range_results)
    else:
        assert proof_row["closure_verdict"] == "PROOF_INCOMPLETE"
        assert not range_ok
        assert range_errors


def _prove_current_classifier_disables_fallback(row):
    """REQ3 is retained as a conditional requirement, not a skipped test."""
    import json
    from copy import deepcopy
    from xml.etree import ElementTree as ET
    from eaeu_xml.process_packages.body import GenerationMode

    assert row["canonical_id"] == "P.SP.02.MSG.027:57:3"
    entries = json.loads((ROOT / "P.SP.02_OP_22/normative_classifier_data/P.CLS.027.yaml").read_text())["entries"]
    assert any(e["code"] == "07365" and "отозванной" in e["name"] for e in entries)
    engine = support.ENG
    msg = "P.SP.02.MSG.027"
    rules = engine.rules[msg]
    source = next(r for r in rules.business_rules if r["rule_id"] == msg + ".T57.REQ.3")
    assert "при отсутствии в классификаторе" in source["source_text"]
    assert any(str(ref.get("table")) == "57" and str(ref.get("item")) == "3" for ref in source["source_refs"])
    assert not any(r["rule_id"] == msg + ".T57.REQ.3" for r in rules.structured_rules)
    spec = importlib.util.spec_from_file_location("catalog_msg027_fixture", ROOT / "P.SP.02_OP_22/tests/test_msg027_end_to_end.py")
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    structure = engine.get_structure(msg, mode=GenerationMode.TEST)
    ns = structure.imported_namespaces
    root = ET.fromstring(ET.tostring(engine.build_body(msg, fixture._valid_values(), mode=GenerationMode.TEST).serialize_xml_element()))
    owner_qname = "{" + ns["ipcdo"] + "}TrademarkApplicationDetails"
    code_qname = "{" + ns["ipsdo"] + "}IPDocKindCode"
    name_qname = "{" + ns["ipsdo"] + "}IPDocKindName"
    for scenario in ("positive", "wrong", "missing", "both", "fallback"):
        changed = deepcopy(root)
        owner = changed.find(owner_qname)
        code = owner.find(code_qname)
        assert code.text == "07365"
        if scenario == "wrong":
            code.text = "99999"
        if scenario in ("missing", "fallback"):
            owner.remove(code)
        if scenario in ("both", "fallback"):
            ET.SubElement(owner, name_qname).text = fixture.FALLBACK
        values, issues = engine.body_provider._values_from_element(structure, ET.fromstring(ET.tostring(changed)))
        assert not issues
        result = engine.validate_body(msg, values, mode=GenerationMode.TEST)
        active = next(e for e in result.rule_evaluations if e.rule_id == msg + ".T57.REQ.2")
        assert active.status.value == ("PASS" if scenario == "positive" else "FAIL")
        assert result.is_valid == (scenario == "positive")
