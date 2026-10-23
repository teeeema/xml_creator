import importlib.util
from pathlib import Path

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.process_packages.body import GenerationMode

import pytest


_SUPPORT_PATH = Path(__file__).with_name("proof_completion_support.py")
_SUPPORT_SPEC = importlib.util.spec_from_file_location("op22_proof_completion_support", _SUPPORT_PATH)
assert _SUPPORT_SPEC is not None and _SUPPORT_SPEC.loader is not None
_SUPPORT = importlib.util.module_from_spec(_SUPPORT_SPEC)
_SUPPORT_SPEC.loader.exec_module(_SUPPORT)

existing_requirement_test_links = _SUPPORT.existing_requirement_test_links
load_reconciliation_rows = _SUPPORT.load_reconciliation_rows
prove_aggregated_requirement = _SUPPORT.prove_aggregated_requirement
prove_requirement = _SUPPORT.prove_requirement


ROWS = load_reconciliation_rows()
GROUP_B = [
    row
    for row in ROWS
    if row["reconciliation_group"] == "B_REAL_IMPLEMENTATION_BUT_PROOF_NOT_LINKED"
]
GROUP_B_NEEDS_NEW_PROOF = [row for row in GROUP_B if not existing_requirement_test_links(row)]
GROUP_C = [
    row
    for row in ROWS
    if row["reconciliation_group"] == "C_REAL_IMPLEMENTATION_BUT_NEGATIVE_PROOF_MISSING"
]
GROUP_D_AGGREGATED = [
    row
    for row in ROWS
    if row["reconciliation_group"] == "D_ONLY_GENERIC_OR_AGGREGATED_COVERAGE_NEEDS_REVIEW"
    and row["rule_status"] == "RULE_EXISTS_AGGREGATED"
]


@pytest.mark.parametrize("row", GROUP_B_NEEDS_NEW_PROOF, ids=lambda row: row["canonical_id"])
def test_group_b_without_existing_exact_link_gets_requirement_specific_proof(row):
    ok, results, errors = prove_requirement(row)
    assert ok, f"{row['canonical_id']}: {errors}"
    assert results
    assert all(item["positive_status"] == "PASS" for item in results)
    assert all(item["negative_status"] == "FAIL" for item in results)


@pytest.mark.parametrize("row", GROUP_C, ids=lambda row: row["canonical_id"])
def test_group_c_requirement_has_positive_negative_runtime_and_source_proof(row):
    ok, results, errors = prove_requirement(row)
    assert ok, f"{row['canonical_id']}: {errors}"
    assert results
    assert all(item["positive_status"] == "PASS" for item in results)
    assert all(item["negative_status"] == "FAIL" for item in results)


@pytest.mark.parametrize("row", GROUP_D_AGGREGATED, ids=lambda row: row["canonical_id"])
def test_group_d_aggregated_requirement_resolves_to_atomic_inherited_proof(row):
    ok, results, errors = prove_aggregated_requirement(row)
    assert ok, f"{row['canonical_id']}: {errors}"
    assert results
    assert all(item["positive_status"] == "PASS" for item in results)
    assert all(item["negative_status"] == "FAIL" for item in results)


def test_msg003_table35_r010_one_of_rejects_missing_payload():
    """Table 35 REQ 1 negative proof missing from the pre-wave OP22 tests."""
    repository = Path(__file__).resolve().parents[2]
    app = EaeuXmlApplication(repository)
    values = app.generate_required_data("P.SP.02", "P.SP.02.TRN.002", "P.SP.02.MSG.003")
    values.pop("*", None)

    result = app.validate(
        "P.SP.02",
        "P.SP.02.TRN.002",
        "P.SP.02.MSG.003",
        values,
        mode=GenerationMode.TEST,
    )

    assert not result.is_valid
    assert "EMBEDDED_STRUCTURE_CARDINALITY" in {item.code for item in result.errors}
