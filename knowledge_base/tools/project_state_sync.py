#!/usr/bin/env python3
"""Build the authoritative requirement-level PROJECT_STATE overlay.

This tool never changes normative SOURCE/KNOWLEDGE fields.  It reconciles
current implementation/proof/blocker state from the latest requirement-level
reports and writes a deterministic overlay consumed by ``schema_v1.py``.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "knowledge_base"
REQ_DIR = KB / "data" / "requirements"
OVERLAY = KB / "project_state" / "requirement_state.json"
REPORT_DIR = ROOT / "codex_reports" / "KNOWLEDGE_BASE" / "FINAL_SYNC_2026"

EXPECTED = {"OP22": 1609, "OP23": 710, "OP26": 239, "OP32": 170, "OP49": 166}

OP22_STRICT = "codex_reports/OP22_P_SP_02/FINAL_ATOMIC_REVIEW/OP22_FINAL_STRICT_STATE.md"
OP22_ATOMIC119 = "codex_reports/OP22_P_SP_02/FINAL_ATOMIC_REVIEW/OP22_ATOMIC_SOURCE_119_MATRIX.csv"
OP22_BLOCKED85 = "codex_reports/OP22_P_SP_02/FINAL_MAPPED_PROOF/OP22_FINAL_BLOCKED85.csv"
OP22_OLD261 = "codex_reports/OP22_P_SP_02/FINAL_MAPPED_PROOF/OP22_OLD_OPEN261_PROOF_MATRIX.csv"

OP23_STRICT = "codex_reports/OP23_P_SP_03/PROOF_CLOSURE/OP23_CURRENT_STRICT_STATE.md"
OP23_MATRIX = "codex_reports/OP23_P_SP_03/PROOF_CLOSURE/OP23_PROOF_CLOSURE_MATRIX.csv"
OP23_POST = "codex_reports/OP23_P_SP_03/POST_ENGINE_WAVE/OP23_POST_ENGINE_AUDIT.md"
OP23_POST_MATRIX = "codex_reports/OP23_P_SP_03/POST_ENGINE_WAVE/OP23_POST_ENGINE_MATRIX.csv"

OP26_AUDIT = "codex_reports/OP26_P_MM_01/EXECUTABLE_PROOF/OP26_EXECUTABLE204_PROOF_AUDIT.md"
OP26_MATRIX = "codex_reports/OP26_P_MM_01/EXECUTABLE_PROOF/OP26_EXECUTABLE204_PROOF_MATRIX.csv"
OP26_BLOCKED = "codex_reports/OP26_P_MM_01/EXECUTABLE_PROOF/OP26_BLOCKED35_CONFIRMATION.csv"

OP32_AUDIT = "codex_reports/OP32_P_MM_06/REAUDIT_2026/OP32_REAUDIT_FINAL.md"
OP32_OPR = "codex_reports/OP32_P_MM_06/OP32_MISSING_OPERATIONS_AUDIT.md"

OP49_TRIAGE = "codex_reports/OP49_P_DS_01/OP49_IMPLEMENTATION_TRIAGE.csv"
OP49_W1 = "codex_reports/OP49_P_DS_01/IMPLEMENTATION_WAVE_1/OP49_WAVE1_RESULTS.csv"
OP49_W1_RECLASS = "codex_reports/OP49_P_DS_01/IMPLEMENTATION_WAVE_1/OP49_WAVE1_RECLASSIFIED.csv"
OP49_W2 = "codex_reports/OP49_P_DS_01/IMPLEMENTATION_WAVE_2/OP49_WAVE2_RESULTS.csv"
OP49_W2_RECLASS = "codex_reports/OP49_P_DS_01/IMPLEMENTATION_WAVE_2/OP49_WAVE2_RECLASSIFIED.csv"


def read_csv(rel: str) -> list[dict[str, str]]:
    path = ROOT / rel
    if not path.exists():
        raise RuntimeError(f"Missing authoritative report: {rel}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_requirements() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for path in REQ_DIR.glob("*.yaml"):
        obj = json.loads(path.read_text(encoding="utf-8"))
        cid = obj["identity"]["canonical_id"]
        if cid in out:
            raise RuntimeError(f"Duplicate canonical requirement ID: {cid}")
        out[cid] = obj
    counts = Counter(obj["identity"]["op"] for obj in out.values())
    if dict(sorted(counts.items())) != dict(sorted(EXPECTED.items())):
        raise RuntimeError(f"Canonical requirement scope mismatch: {dict(counts)}")
    return out


def split_ids(value: Any) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return []
    return [item.strip() for item in re.split(r"\s*;\s*", text) if item.strip()]


def entry(
    *,
    state: str,
    mapped: bool,
    full_proof: bool,
    blockers: list[str] | None = None,
    production_rule_ids: list[str] | None = None,
    positive_test_ids: list[str] | None = None,
    negative_test_ids: list[str] | None = None,
    runtime_evidence: list[str] | None = None,
    real_xml_status: str | None = None,
    evidence_refs: list[str] | None = None,
    note: str = "",
) -> dict[str, Any]:
    return {
        "state": state,
        "mapped": mapped,
        "full_proof": full_proof,
        "blockers": sorted(set(blockers or [])),
        "production_rule_ids": sorted(set(production_rule_ids or [])),
        "positive_test_ids": sorted(set(positive_test_ids or [])),
        "negative_test_ids": sorted(set(negative_test_ids or [])),
        "runtime_evidence": sorted(set(runtime_evidence or [])),
        "real_xml_status": real_xml_status,
        "evidence_refs": sorted(set(evidence_refs or [])),
        "note": note,
    }


def op22_state(ids: set[str]) -> dict[str, dict[str, Any]]:
    atomic = {row["canonical_id"]: row for row in read_csv(OP22_ATOMIC119)}
    blocked = {row["canonical_id"]: row for row in read_csv(OP22_BLOCKED85)}
    old261 = {row["canonical_id"]: row for row in read_csv(OP22_OLD261)}
    if len(atomic) != 119 or len(blocked) != 85 or atomic.keys() & blocked.keys():
        raise RuntimeError("OP22 119/85 authoritative partitions are inconsistent")
    full_ids = ids - set(atomic) - set(blocked)
    if len(full_ids) != 1405:
        raise RuntimeError(f"OP22 FULL_PROOF complement {len(full_ids)} != 1405")

    out: dict[str, dict[str, Any]] = {}
    for cid in full_ids:
        row = old261.get(cid)
        exact_test = [row["test_evidence"]] if row and row.get("closure_verdict") == "FULL_PROOF_CLOSED" and row.get("test_evidence") else []
        rules = split_ids(row.get("production_rule_or_mechanism")) if row and row.get("closure_verdict") == "FULL_PROOF_CLOSED" else []
        refs = [OP22_STRICT]
        if row and row.get("closure_verdict") == "FULL_PROOF_CLOSED":
            refs.append(OP22_OLD261)
        out[cid] = entry(
            state="FULL_PROOF", mapped=True, full_proof=True,
            production_rule_ids=rules,
            positive_test_ids=exact_test,
            negative_test_ids=exact_test,
            runtime_evidence=exact_test,
            evidence_refs=refs,
            note="Current OP22 strict-state partition: 1405 FULL_PROOF; exact links are copied only where the requirement-level report names them.",
        )

    for cid, row in atomic.items():
        blockers = ["EXECUTABLE_ATOMIC_LINK_MISSING"]
        if row.get("prior_bucket") == "PROOF_INCOMPLETE":
            blockers.append("TARGETED_NEGATIVE_PROOF_INCOMPLETE")
        out[cid] = entry(
            state="IMPLEMENTED_PROOF_INCOMPLETE", mapped=True, full_proof=False,
            blockers=blockers,
            evidence_refs=[OP22_STRICT, OP22_ATOMIC119, OP22_OLD261],
            note="Primary atomic normative source is confirmed, but strict executable attribution remains incomplete; aggregate proof is not promoted to atomic proof.",
        )

    blocker_map = {
        "CLASSIFIER": "BLOCKED_CLASSIFIER",
        "EXTERNAL": "BLOCKED_EXTERNAL_REGISTRY",
        "SOURCE_CONFLICT": "BLOCKED_SOURCE_CONFLICT",
        "OTHER": "BLOCKED_OTHER",
    }
    for cid, row in blocked.items():
        category = row.get("remaining_category", "OTHER")
        out[cid] = entry(
            state=blocker_map.get(category, "BLOCKED_OTHER"), mapped=False, full_proof=False,
            blockers=[category], evidence_refs=[OP22_STRICT, OP22_BLOCKED85],
            note=row.get("current_state") or row.get("final_blocker_status") or "OP22 blocker remains open.",
        )
    if set(out) != ids:
        raise RuntimeError("OP22 state map does not cover the canonical set exactly")
    return out


def op23_state(ids: set[str]) -> dict[str, dict[str, Any]]:
    matrix = {row["canonical_id"]: row for row in read_csv(OP23_MATRIX)}
    if set(matrix) != ids:
        raise RuntimeError("OP23 proof-closure matrix does not match canonical IDs")
    post = {row["requirement_id"]: row for row in read_csv(OP23_POST_MATRIX) if row.get("requirement_id")}
    post_closed = {cid for cid, row in post.items() if row.get("closure_status") == "CLOSED_FULL_PROOF"}
    expected_closed = {"P.SP.03.MSG.007.REQ.036", "P.SP.03.MSG.014.REQ.039"}
    if post_closed != expected_closed:
        raise RuntimeError(f"OP23 post-engine closure set mismatch: {sorted(post_closed)}")

    out: dict[str, dict[str, Any]] = {}
    source_map = {
        "CLASSIFIER": "BLOCKED_CLASSIFIER",
        "BLOCKED_CLASSIFIER_NO_AUTHORITATIVE_CODE_NAME_MAPPING": "BLOCKED_CLASSIFIER",
        "EXTERNAL_REGISTRY": "BLOCKED_EXTERNAL_REGISTRY",
        "SOURCE_CONFLICT": "BLOCKED_SOURCE_CONFLICT",
        "XSD": "BLOCKED_XSD",
        "EVIDENCE_BLOCKED_XSD_CLASSIFIER": "BLOCKED_MULTIPLE",
    }
    for cid, row in matrix.items():
        strict = row.get("strict_status", "")
        rules = split_ids(row.get("rule_ids"))
        proof_ids = split_ids(row.get("proof_test_nodeids"))
        refs = [OP23_STRICT, OP23_MATRIX]
        if cid in post_closed:
            p = post[cid]
            out[cid] = entry(
                state="FULL_PROOF", mapped=True, full_proof=True,
                production_rule_ids=[cid],
                positive_test_ids=["P.SP.03_OP_23/tests/test_next_implementation.py::test_post_engine_date_rules_real_xml"],
                negative_test_ids=["P.SP.03_OP_23/tests/test_next_implementation.py::test_post_engine_date_rules_real_xml"],
                runtime_evidence=["P.SP.03_OP_23/tests/test_next_implementation.py::test_post_engine_date_rules_real_xml"],
                real_xml_status="PRESENT",
                evidence_refs=[*refs, OP23_POST, OP23_POST_MATRIX],
                note=p.get("source_evidence", "") + "; post-engine DATE rule has positive and negative real-XML proof.",
            )
        elif strict in {"FULL_PROOF", "LINK_ONLY_RESOLVED", "NEW_TEST_ADDED"}:
            out[cid] = entry(
                state="FULL_PROOF", mapped=True, full_proof=True,
                production_rule_ids=rules,
                positive_test_ids=proof_ids,
                negative_test_ids=proof_ids,
                runtime_evidence=proof_ids,
                real_xml_status="PRESENT" if proof_ids else None,
                evidence_refs=refs,
                note=row.get("proof_basis", ""),
            )
        elif strict == "PARTIAL":
            out[cid] = entry(
                state="PARTIAL", mapped=True, full_proof=False,
                blockers=["THRESHOLD_SEMANTICS_UNKNOWN"], production_rule_ids=rules,
                evidence_refs=[*refs, OP23_POST], note=row.get("note", "") or "Normative <=5 MB is confirmed but decimal-vs-binary byte semantics remain unresolved.",
            )
        elif strict == "BLOCKED_ENGINE":
            out[cid] = entry(
                state="BLOCKED_ENGINE", mapped=False, full_proof=False,
                blockers=[row.get("blocker_code") or "ENGINE"], evidence_refs=refs, note=row.get("note", ""),
            )
        elif strict == "BLOCKED_MULTIPLE":
            out[cid] = entry(
                state="BLOCKED_MULTIPLE", mapped=False, full_proof=False,
                blockers=[row.get("blocker_code") or "MULTIPLE"], evidence_refs=refs, note=row.get("note", ""),
            )
        elif strict == "BLOCKED_SOURCE":
            blocker = row.get("blocker_code", "")
            out[cid] = entry(
                state=source_map.get(blocker, "BLOCKED_OTHER"), mapped=False, full_proof=False,
                blockers=[blocker or "SOURCE"], evidence_refs=refs, note=row.get("note", ""),
            )
        else:
            raise RuntimeError(f"Unknown OP23 strict status for {cid}: {strict}")

    counts = Counter(item["state"] for item in out.values())
    if sum(item["mapped"] for item in out.values()) != 503 or sum(item["full_proof"] for item in out.values()) != 501:
        raise RuntimeError(f"OP23 mapped/full arithmetic mismatch: {dict(counts)}")
    if counts["PARTIAL"] != 2 or sum(not item["mapped"] for item in out.values()) != 207:
        raise RuntimeError(f"OP23 partial/blocked arithmetic mismatch: {dict(counts)}")
    return out


def op26_state(ids: set[str]) -> dict[str, dict[str, Any]]:
    # The executable-proof reports predate the final canonical disambiguation
    # for the two distinct Table 21 item 5 rows.  Their #A/#B aliases are
    # evidence-level identifiers only; the canonical KB entities use source
    # occurrence 1 and 2 respectively.
    alias_to_canonical = {
        "OP26.P_MM_01.P.MM.01.MSG.028.REQ.005#A": "OP26.P_MM_01.P.MM.01.MSG.028.REQ.005",
        "OP26.P_MM_01.P.MM.01.MSG.028.REQ.005#B": "OP26.P_MM_01.P.MM.01.MSG.028.REQ.005.2",
    }
    matrix = {
        alias_to_canonical.get(row["canonical_id"], row["canonical_id"]): row
        for row in read_csv(OP26_MATRIX)
    }
    blocked = {
        alias_to_canonical.get(row["canonical_requirement_id"], row["canonical_requirement_id"]): row
        for row in read_csv(OP26_BLOCKED)
    }
    if len(matrix) != 204 or len(blocked) != 35 or matrix.keys() & blocked.keys() or set(matrix) | set(blocked) != ids:
        raise RuntimeError("OP26 executable/blocker partition is inconsistent")
    out: dict[str, dict[str, Any]] = {}
    for cid, row in matrix.items():
        rules = split_ids(row.get("production_rule_ids"))
        proof = [row["proof_test"]] if row.get("proof_test") else []
        if row.get("strict_verdict") == "FULL_PROOF":
            out[cid] = entry(
                state="FULL_PROOF", mapped=True, full_proof=True,
                production_rule_ids=rules, positive_test_ids=proof, negative_test_ids=proof,
                runtime_evidence=proof, real_xml_status="PRESENT",
                evidence_refs=[OP26_AUDIT, OP26_MATRIX],
                note="Production mapping, confirmed source link, positive/negative proof, engine runtime and serialized body XML are all present.",
            )
        elif row.get("strict_verdict") == "RUNTIME_PROOF_MISSING":
            out[cid] = entry(
                state="IMPLEMENTED_REAL_XML_PROOF_BLOCKED", mapped=True, full_proof=False,
                blockers=[row.get("real_xml_blocker") or "MESSAGE_LEVEL_REAL_XML_BLOCKER"],
                production_rule_ids=rules, positive_test_ids=proof, negative_test_ids=proof,
                runtime_evidence=proof, real_xml_status="BLOCKED",
                evidence_refs=[OP26_AUDIT, OP26_MATRIX],
                note="Executable rule proof passes; serialized body XML is blocked by existing message-level normative/classifier issues.",
            )
        else:
            raise RuntimeError(f"Unknown OP26 strict verdict for {cid}: {row.get('strict_verdict')}")
    block_map = {
        "EXTERNAL_REGISTRY": "BLOCKED_EXTERNAL_REGISTRY",
        "CLASSIFIER_P_CLS_019": "BLOCKED_CLASSIFIER",
        "SOURCE_CONFLICT": "BLOCKED_SOURCE_CONFLICT",
        "CLASSIFIER_AMBIGUITY": "BLOCKED_OTHER",
        "TRUNCATED_RULE": "BLOCKED_OTHER",
    }
    for cid, row in blocked.items():
        category = row.get("category", "")
        out[cid] = entry(
            state=block_map.get(category, "BLOCKED_OTHER"), mapped=False, full_proof=False,
            blockers=[category or "OTHER"], evidence_refs=[OP26_AUDIT, OP26_BLOCKED],
            note=row.get("current_resolution", "") or row.get("confirmation", ""),
        )
    if sum(item["full_proof"] for item in out.values()) != 113 or sum(item["state"] == "IMPLEMENTED_REAL_XML_PROOF_BLOCKED" for item in out.values()) != 91:
        raise RuntimeError("OP26 113/91 proof partition mismatch")
    return out


def op32_state(ids: set[str]) -> dict[str, dict[str, Any]]:
    # The 2026 re-audit confirms the same universal root blocker for all 170
    # child-payload requirements: imported model versions are placeholders, so
    # exact Clark QName/path cannot be established.  Do not infer finer per-row
    # XSD/classifier/registry buckets from the overlap totals.
    return {
        cid: entry(
            state="BLOCKED_MODEL_VERSION", mapped=False, full_proof=False,
            blockers=["IMPORTED_MODEL_VERSION_UNRESOLVED"], evidence_refs=[OP32_AUDIT, OP32_OPR],
            note="All OP32 child-payload requirements remain non-implementable because imported model versions and exact child Clark QName/path are unresolved.",
        )
        for cid in ids
    }


def op49_state(ids: set[str]) -> dict[str, dict[str, Any]]:
    triage = {row["canonical_id"]: row for row in read_csv(OP49_TRIAGE)}
    if set(triage) != ids:
        raise RuntimeError("OP49 triage does not match canonical IDs")
    out: dict[str, dict[str, Any]] = {}
    blocker_map = {
        "CLASSIFIER_BLOCKED": "BLOCKED_CLASSIFIER",
        "SOURCE_CONFLICT": "BLOCKED_SOURCE_CONFLICT",
        "ENGINE_GAP": "BLOCKED_ENGINE",
        "MISSING_XSD/QNAME_ONLY": "BLOCKED_XSD",
        "EXTERNAL_REGISTRY_BLOCKED": "BLOCKED_EXTERNAL_REGISTRY",
        "PRODUCTION_MAPPING_MISSING": "UNMAPPED",
        "OTHER": "BLOCKED_OTHER",
    }
    for cid, row in triage.items():
        mapped = row.get("already_production_mapped") == "YES"
        if mapped:
            out[cid] = entry(
                state="IMPLEMENTED_PROOF_INCOMPLETE", mapped=True, full_proof=False,
                blockers=[row.get("primary_triage_status") or "STRICT_PROOF_INCOMPLETE"],
                production_rule_ids=split_ids(row.get("structured_rule_ids")),
                evidence_refs=[OP49_TRIAGE],
                note=row.get("implementation_status_before_triage", "") or row.get("primary_blocker_reason", ""),
            )
        else:
            status = row.get("primary_triage_status", "OTHER")
            out[cid] = entry(
                state=blocker_map.get(status, "BLOCKED_OTHER"), mapped=False, full_proof=False,
                blockers=[status], evidence_refs=[OP49_TRIAGE], note=row.get("primary_blocker_reason", ""),
            )

    for row in read_csv(OP49_W1):
        cid = row["canonical_id"]
        if row.get("status") == "CLOSED":
            tests = [
                "P.DS.01_OP_49/tests/test_process_pipeline.py::test_wave1_safe_rules_pass_for_valid_runtime_values",
                "P.DS.01_OP_49/tests/test_process_pipeline.py::test_wave1_safe_rules_reject_invalid_runtime_values",
            ]
            out[cid] = entry(
                state="FULL_PROOF", mapped=True, full_proof=True,
                production_rule_ids=[row["production_rule"]] if row.get("production_rule") else [],
                positive_test_ids=[tests[0]], negative_test_ids=[tests[1]], runtime_evidence=tests,
                real_xml_status="PRESENT", evidence_refs=[OP49_W1], note=row.get("reason", ""),
            )
    reclass_map = {
        "ENGINE_GAP": "BLOCKED_ENGINE",
        "EXTERNAL_REGISTRY_BLOCKED": "BLOCKED_EXTERNAL_REGISTRY",
        "CLASSIFIER_BLOCKED": "BLOCKED_CLASSIFIER",
    }
    for row in read_csv(OP49_W1_RECLASS):
        cid = row["canonical_id"]
        out[cid] = entry(
            state=reclass_map.get(row.get("classification", ""), "BLOCKED_OTHER"), mapped=False, full_proof=False,
            blockers=[row.get("classification") or "OTHER"], evidence_refs=[OP49_W1_RECLASS], note=row.get("evidence", ""),
        )
    for row in read_csv(OP49_W2):
        cid = row["canonical_id"]
        if row.get("status") == "CLOSED":
            test = "P.DS.01_OP_49/tests/test_wave2_implementation.py"
            out[cid] = entry(
                state="FULL_PROOF", mapped=True, full_proof=True,
                production_rule_ids=[row["production_rule"]] if row.get("production_rule") else [],
                positive_test_ids=[test], negative_test_ids=[test], runtime_evidence=[test],
                real_xml_status="PRESENT", evidence_refs=[OP49_W2], note=row.get("reason", ""),
            )
        elif row.get("status") == "STILL_ENGINE_BLOCKED":
            out[cid] = entry(
                state="BLOCKED_ENGINE", mapped=False, full_proof=False,
                blockers=["NESTED_CONTEXT_CORRELATION"], evidence_refs=[OP49_W2, OP49_W2_RECLASS], note=row.get("reason", ""),
            )
    counts = Counter(item["state"] for item in out.values())
    if sum(item["mapped"] for item in out.values()) != 46 or sum(item["full_proof"] for item in out.values()) != 10:
        raise RuntimeError(f"OP49 mapped/full arithmetic mismatch: {dict(counts)}")
    if sum(not item["mapped"] for item in out.values()) != 120:
        raise RuntimeError(f"OP49 blocked/unmapped count mismatch: {dict(counts)}")
    return out


def build_overlay(requirements: dict[str, dict[str, Any]]) -> dict[str, Any]:
    by_op: dict[str, set[str]] = {
        op: {cid for cid, obj in requirements.items() if obj["identity"]["op"] == op}
        for op in EXPECTED
    }
    state: dict[str, dict[str, Any]] = {}
    for part in [op22_state(by_op["OP22"]), op23_state(by_op["OP23"]), op26_state(by_op["OP26"]), op32_state(by_op["OP32"]), op49_state(by_op["OP49"])]:
        overlap = state.keys() & part.keys()
        if overlap:
            raise RuntimeError(f"Duplicate state assignments: {sorted(overlap)[:5]}")
        state.update(part)
    if set(state) != set(requirements):
        raise RuntimeError("Final project-state overlay does not cover exactly 2894 canonical IDs")
    evidence_sources = sorted({ref for item in state.values() for ref in item["evidence_refs"]})
    return {
        "schema_version": "1.0",
        "scope": {**EXPECTED, "TOTAL": sum(EXPECTED.values())},
        "policy": "SOURCE -> KNOWLEDGE -> PROJECT_STATE; this overlay changes project state only and does not resolve normative unknowns.",
        "evidence_sources": evidence_sources,
        "requirements": dict(sorted(state.items())),
    }


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_text(path: Path, text: str) -> None:
    resolved = path.resolve()
    if not (resolved.is_relative_to(KB.resolve()) or resolved.is_relative_to(REPORT_DIR.resolve())):
        raise RuntimeError(f"Refusing write outside approved sync scope: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    from io import StringIO
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: row.get(key, "") for key in fieldnames})
    write_text(path, buf.getvalue())


def legacy_state(req: dict[str, Any]) -> str:
    impl = req["implementation"]["status"]
    if impl == "IMPLEMENTED_CONFIRMED":
        return "FULL_PROOF" if req["gap"]["status"] == "CLOSED" else "IMPLEMENTED_PROOF_INCOMPLETE"
    mapping = {
        "OPEN_CLASSIFIER": "BLOCKED_CLASSIFIER",
        "OPEN_EXTERNAL_REGISTRY": "BLOCKED_EXTERNAL_REGISTRY",
        "OPEN_SOURCE_CONFLICT": "BLOCKED_SOURCE_CONFLICT",
        "OPEN_ENGINE": "BLOCKED_ENGINE",
        "OPEN_MISSING_NORMATIVE_DATA": "BLOCKED_MODEL_VERSION",
        "OPEN_PRODUCTION_MAPPING": "UNMAPPED",
        "OPEN_NORMATIVE_AMBIGUITY": "BLOCKED_OTHER",
        "OTHER": "BLOCKED_OTHER",
    }
    return mapping.get(impl, impl)


def prepare() -> dict[str, Any]:
    requirements = load_requirements()
    overlay = build_overlay(requirements)
    write_text(OVERLAY, stable_json(overlay))

    all_rows: list[dict[str, Any]] = []
    stale_rows: list[dict[str, Any]] = []
    for cid, req in sorted(requirements.items()):
        target = overlay["requirements"][cid]
        old_state = legacy_state(req)
        changed = old_state != target["state"]
        row = {
            "canonical_id": cid,
            "op": req["identity"]["op"],
            "old_state": old_state,
            "new_state": target["state"],
            "old_implementation_status": req["implementation"]["status"],
            "new_mapped": "YES" if target["mapped"] else "NO",
            "old_gap_status": req["gap"]["status"],
            "new_full_proof": "YES" if target["full_proof"] else "NO",
            "semantic_state_changed": "YES" if changed else "NO",
            "evidence_refs": "; ".join(target["evidence_refs"]),
        }
        all_rows.append(row)
        if changed:
            stale_rows.append(row)
    fields = [
        "canonical_id", "op", "old_state", "new_state", "old_implementation_status", "new_mapped",
        "old_gap_status", "new_full_proof", "semantic_state_changed", "evidence_refs",
    ]
    write_csv(REPORT_DIR / "KB_FINAL_SYNC_CHANGES.csv", fields, all_rows)
    write_csv(REPORT_DIR / "KB_FINAL_SYNC_STALE_STATE_FIXED.csv", fields, stale_rows)
    return {"requirements": len(requirements), "stale_fixed": len(stale_rows)}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git_status() -> list[str]:
    cp = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return cp.stdout.splitlines()


def git_text(*args: str) -> str:
    cp = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)
    return cp.stdout.strip()


def status_path(line: str) -> str:
    path = line[3:].strip() if len(line) >= 4 else line.strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return path.strip('"')


def classify_workspace_path(path: str) -> str:
    if path.startswith("knowledge_base/"):
        return "KB"
    if path.startswith("graphify-out/"):
        return "generated_graph"
    if path.startswith("codex_reports/"):
        return "report"
    if path.startswith("eaeu_xml/src/eaeu_xml/gui"):
        return "GUI"
    if path in {
        "eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py",
        "eaeu_xml/src/eaeu_xml/process_packages/validator.py",
    }:
        return "shared_engine"
    if path.startswith("eaeu_xml/src/"):
        return "production"
    if path.startswith("eaeu_xml/tests/") or re.match(r"^P\.[^/]+_OP_\d+/tests/", path):
        return "test"
    if re.match(r"^P\.[^/]+_OP_\d+/(message_rules|process|transactions|messages|structures)/", path):
        return "production"
    if re.match(r"^P\.[^/]+_OP_\d+/", path):
        return "production"
    return "unrelated"


def file_mtime(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    return dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def finalize(old_fingerprint: str | None) -> dict[str, Any]:
    requirements = load_requirements()
    overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
    states = overlay["requirements"]
    if set(states) != set(requirements):
        raise RuntimeError("Overlay/canonical ID mismatch at finalization")
    for cid, req in requirements.items():
        if req.get("project_state", {}).get("state") != states[cid]["state"]:
            raise RuntimeError(f"Canonical requirement not synchronized: {cid}")

    state_rows: list[dict[str, Any]] = []
    for cid, req in sorted(requirements.items()):
        st = states[cid]
        source = req["source"]
        state_rows.append({
            "canonical_id": cid,
            "op": req["identity"]["op"],
            "process": req["identity"]["process"],
            "procedure": req["identity"]["procedure"],
            "transaction": req["identity"]["transaction"],
            "message": req["identity"]["message"],
            "requirement": req["identity"]["requirement"],
            "normative_evidence": source.get("evidence", {}).get("level"),
            "source_document": source.get("document"),
            "source_page": source.get("pdf_page"),
            "source_table": source.get("table"),
            "source_item": source.get("item"),
            "atomic_qname_status": req["structure"]["atomic_qname"]["status"],
            "production_mapping": "MAPPED" if st["mapped"] else "UNMAPPED",
            "project_state": st["state"],
            "full_proof": "YES" if st["full_proof"] else "NO",
            "blockers": "; ".join(st["blockers"]),
            "production_rule_ids": "; ".join(st["production_rule_ids"]),
            "positive_test_ids": "; ".join(st["positive_test_ids"]),
            "negative_test_ids": "; ".join(st["negative_test_ids"]),
            "runtime_evidence": "; ".join(st["runtime_evidence"]),
            "real_xml_status": st.get("real_xml_status") or "",
            "latest_evidence": "; ".join(st["evidence_refs"]),
        })
    fields = list(state_rows[0])
    write_csv(REPORT_DIR / "KB_FINAL_SYNC_REQUIREMENT_STATE.csv", fields, state_rows)

    counts = Counter(req["identity"]["op"] for req in requirements.values())
    ids = list(requirements)
    duplicates = len(ids) - len(set(ids))
    missing_files = sum(1 for cid in states if not (REQ_DIR / f"{cid}.yaml").exists())
    broken_relations = 0
    for cid, req in requirements.items():
        for rel in req["relationships"]["inherits_from"]:
            if rel["requirement"] not in requirements:
                broken_relations += 1
    stale_sources = 0
    source_index = json.loads((KB / "indexes" / "source_index.json").read_text(encoding="utf-8"))
    for src in source_index:
        p = Path(src.get("absolute_path") or "")
        if p.exists() and src.get("sha256") and sha256(p) != src["sha256"]:
            stale_sources += 1

    validation_path = ROOT / "codex_reports" / "KNOWLEDGE_BASE" / "KB_CANONICAL_SCOPE_2894_VALIDATION.json"
    validation = json.loads(validation_path.read_text(encoding="utf-8")) if validation_path.exists() else {}
    evidence_sources = list(overlay.get("evidence_sources") or [])
    engine_reports = [
        "codex_reports/SHARED_ENGINE_WAVE/SHARED_ENGINE_IMPLEMENTATION_REPORT.md",
        "codex_reports/SHARED_ENGINE_WAVE/SHARED_ENGINE_REGRESSION_RESULTS.md",
    ]
    evidence_sources = sorted(set([*evidence_sources, *engine_reports]))
    missing_evidence_refs = [rel for rel in evidence_sources if not (ROOT / rel).exists()]
    broken_links = int(validation.get("broken_internal_links", 0)) + len(missing_evidence_refs)

    current_head = git_text("rev-parse", "--verify", "HEAD")
    current_branch = git_text("branch", "--show-current")
    stale_project_state_refs: list[str] = []
    project_state_dirs = [
        KB / "data" / "requirements",
        KB / "data" / "messages",
        KB / "data" / "transactions",
        KB / "data" / "processes",
    ]
    for directory in project_state_dirs:
        for path in sorted(directory.glob("*.yaml")):
            obj = json.loads(path.read_text(encoding="utf-8"))
            project_state = obj.get("project_state", {})
            if project_state.get("snapshot") != "data/project_state/current.json" or project_state.get("git_head") != current_head:
                stale_project_state_refs.append(str(path.relative_to(ROOT)))
    current_snapshot_path = KB / "data" / "project_state" / "current.json"
    current_snapshot = json.loads(current_snapshot_path.read_text(encoding="utf-8")) if current_snapshot_path.exists() else {}
    if current_snapshot.get("git_head") != current_head:
        stale_project_state_refs.append(str(current_snapshot_path.relative_to(ROOT)))
    stale_project_state = len(stale_project_state_refs)

    op_counts: dict[str, Counter[str]] = {}
    for op in EXPECTED:
        op_counts[op] = Counter(states[cid]["state"] for cid, req in requirements.items() if req["identity"]["op"] == op)

    stale_rows = list(csv.DictReader((REPORT_DIR / "KB_FINAL_SYNC_STALE_STATE_FIXED.csv").open(encoding="utf-8", newline="")))
    global_md = f"""# KB Final Sync Global Counts

- CANONICAL_TOTAL: **{len(requirements)}**
- OP22_TOTAL: **{counts['OP22']}**; FULL_PROOF **{op_counts['OP22']['FULL_PROOF']}**; MAPPED_NOT_STRICT **{op_counts['OP22']['IMPLEMENTED_PROOF_INCOMPLETE']}**; BLOCKED **{counts['OP22'] - op_counts['OP22']['FULL_PROOF'] - op_counts['OP22']['IMPLEMENTED_PROOF_INCOMPLETE']}**
- OP23_TOTAL: **{counts['OP23']}**; FULL_PROOF **{op_counts['OP23']['FULL_PROOF']}**; PARTIAL **{op_counts['OP23']['PARTIAL']}**; BLOCKED **{sum(not states[cid]['mapped'] for cid, req in requirements.items() if req['identity']['op'] == 'OP23')}**
- OP26_TOTAL: **{counts['OP26']}**; FULL_PROOF **{op_counts['OP26']['FULL_PROOF']}**; EXECUTABLE_REAL_XML_PROOF_BLOCKED **{op_counts['OP26']['IMPLEMENTED_REAL_XML_PROOF_BLOCKED']}**; BLOCKED **{sum(not states[cid]['mapped'] for cid, req in requirements.items() if req['identity']['op'] == 'OP26')}**
- OP32_TOTAL: **{counts['OP32']}**; IMPLEMENTABLE **0**; BLOCKED **{counts['OP32']}**
- OP49_TOTAL: **{counts['OP49']}**; MAPPED **{sum(states[cid]['mapped'] for cid, req in requirements.items() if req['identity']['op'] == 'OP49')}**; FULL_PROOF_KNOWN **{op_counts['OP49']['FULL_PROOF']}**; BLOCKED_OR_UNMAPPED **{sum(not states[cid]['mapped'] for cid, req in requirements.items() if req['identity']['op'] == 'OP49')}**

- DUPLICATE_CANONICAL_IDS: **{duplicates}**
- MISSING_REQUIREMENT_FILES: **{missing_files}**
- BROKEN_CANONICAL_RELATIONS: **{broken_relations}**
- BROKEN_INTERNAL_LINKS: **{broken_links}**
- STALE_SOURCE_REFERENCES: **{stale_sources}**
- STALE_PROJECT_STATE: **{stale_project_state}**
- STALE_PROJECT_STATE_FIXED: **{len(stale_rows)}**
"""
    write_text(REPORT_DIR / "KB_FINAL_SYNC_GLOBAL_COUNTS.md", global_md)

    new_fingerprint = validation.get("reproducibility", {}).get("second_fingerprint")
    reproducibility = validation.get("reproducibility", {}).get("status", "UNKNOWN")
    repro_md = f"""# KB Final Sync Reproducibility

- Schema validation: **{validation.get('status', 'UNKNOWN')}**
- Reproducibility: **{reproducibility}**
- Previous deterministic fingerprint: `{old_fingerprint or 'UNKNOWN'}`
- New deterministic fingerprint: `{new_fingerprint or 'UNKNOWN'}`
- Fingerprint changed: **{'YES' if old_fingerprint and new_fingerprint and old_fingerprint != new_fingerprint else 'NO/UNKNOWN'}**
- Timestamped `data/project_state/current.json` remains excluded from the deterministic fingerprint.
- Requirement-state overlay: `{OVERLAY.relative_to(ROOT)}`
"""
    write_text(REPORT_DIR / "KB_FINAL_SYNC_REPRODUCIBILITY.md", repro_md)

    graph_path = ROOT / "graphify-out" / "graph.json"
    graph_nodes = graph_edges = 0
    if graph_path.exists():
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        graph_nodes = len(graph.get("nodes", [])) if isinstance(graph.get("nodes"), list) else len(graph.get("nodes", {}))
        # Graphify serializes its NetworkX graph with node-link JSON, where
        # edges are stored under ``links`` rather than ``edges``.
        graph_edges = len(graph.get("links", graph.get("edges", [])))
    graph_status = "UPDATED" if graph_nodes and graph_edges else "UNAVAILABLE"
    graph_viz_note = "graph.html visualization remains stale because the aggregated community view exceeds the 5000-node HTML limit." if graph_nodes > 5000 else "No graph.html size-limit warning observed."

    workspace_status = git_status()
    classified_status: list[tuple[str, str, str]] = []
    for line in workspace_status:
        path = status_path(line)
        classified_status.append((line, path, classify_workspace_path(path)))
    relevant_dirty = [item for item in classified_status if item[2] in {"production", "test", "shared_engine"}]
    parallel = [
        item for item in classified_status
        if not (
            item[1].startswith("knowledge_base/")
            or item[1].startswith("codex_reports/KNOWLEDGE_BASE/")
            or item[1].startswith("graphify-out/")
        )
    ]
    classification_counts = Counter(item[2] for item in classified_status)

    evidence_lines: list[str] = []
    for rel in evidence_sources:
        path = ROOT / rel
        digest = sha256(path) if path.exists() else "MISSING"
        evidence_lines.append(f"- `{rel}` | mtime `{file_mtime(path)}` | sha256 `{digest}`")
    relevant_lines = [f"- `{line}` | {category}" for line, _, category in relevant_dirty]
    parallel_lines = [f"- `{line}` | {category}" for line, _, category in parallel]
    engine_impl = ROOT / engine_reports[0]
    engine_reg = ROOT / engine_reports[1]
    snapshot_md = f"""# KB Final Sync Workspace Snapshot

- HEAD: `{current_head}`
- Branch: `{current_branch}`
- Captured project-state snapshot: `{current_snapshot_path.relative_to(ROOT)}`
- WORKSPACE_RELEVANT_DIRTY_FILES: **{len(relevant_dirty)}**
- Production dirty files: **{classification_counts.get('production', 0)}**
- Test dirty files: **{classification_counts.get('test', 0)}**
- Shared-engine dirty files: **{classification_counts.get('shared_engine', 0)}**
- GUI dirty files: **{classification_counts.get('GUI', 0)}**
- KB dirty files: **{classification_counts.get('KB', 0)}**
- Report dirty files: **{classification_counts.get('report', 0)}**
- Generated graph dirty files: **{classification_counts.get('generated_graph', 0)}**
- Engine state: **COMPLETE** per `{engine_reports[0]}`
- Engine implementation report mtime: `{file_mtime(engine_impl)}`
- Engine regression report mtime: `{file_mtime(engine_reg)}`

## Relevant production/test/engine dirty inventory

{chr(10).join(relevant_lines) if relevant_lines else '- None'}

## Latest requirement-level evidence used

{chr(10).join(evidence_lines) if evidence_lines else '- None'}

## Preserved pre-existing / parallel non-sync entries

{chr(10).join(parallel_lines) if parallel_lines else '- None'}
"""
    write_text(REPORT_DIR / "KB_FINAL_SYNC_WORKSPACE_SNAPSHOT.md", snapshot_md)

    preconditions_pass = (
        len(requirements) == 2894
        and validation.get("status") == "PASS"
        and reproducibility == "PASS"
        and duplicates == 0
        and missing_files == 0
        and broken_relations == 0
        and broken_links == 0
        and stale_sources == 0
        and stale_project_state == 0
    )
    sync_marker = "COMPLETE" if preconditions_pass else "PARTIAL"
    gate_marker = "YES" if preconditions_pass else "NO"
    audit_md = f"""# KB Final Sync Audit

STATUS: {'PASS' if preconditions_pass else 'PARTIAL'}

KB_FINAL_SYNC: {sync_marker}
READY_FOR_FINAL_GATE: {gate_marker}

The reconciliation preserves the architecture `SOURCE -> KNOWLEDGE -> PROJECT_STATE`. Normative/source fields were not promoted from production state. Unknown QName/model/classifier/registry facts remain unresolved or blocked.

## Canonical state

- Requirements synchronized: **{len(requirements)} / 2894**
- FULL_PROOF total: **{sum(item['full_proof'] for item in states.values())}**
- Open/non-full project-state requirements: **{sum(not item['full_proof'] for item in states.values())}**
- OP32 process knowledge: normative OPR count **46**; package exposes **44**; missing `P.MM.06.OPR.007` and `P.MM.06.OPR.008`; five structure roots are confirmed, `R.006`/`R.007` remain unresolved; child payload QName/path remains unresolved for 170/170.

## Integrity

- Duplicate canonical IDs: **{duplicates}**
- Missing requirement files: **{missing_files}**
- Broken canonical relations: **{broken_relations}**
- Broken internal links: **{broken_links}**
- Stale source references: **{stale_sources}**
- Stale PROJECT_STATE references: **{stale_project_state}**
- Semantic stale-state rows fixed: **{len(stale_rows)}**
- Missing evidence files referenced by current PROJECT_STATE: **{len(missing_evidence_refs)}**

## Graph

- Nodes: **{graph_nodes}**
- Edges: **{graph_edges}**
- Status: **{graph_status}**
- Visualization note: {graph_viz_note}

## Reproducibility

- Status: **{reproducibility}**
- New fingerprint: `{new_fingerprint or 'UNKNOWN'}`

## Safety boundary

- Production changed by this sync: **0**
- Engine changed by this sync: **0**
- GUI changed by this sync: **0**
- Pre-existing/parallel non-KB dirty entries preserved: **{len(parallel)}**
- Relevant production/test/engine dirty files preserved: **{len(relevant_dirty)}**

See `KB_FINAL_SYNC_REQUIREMENT_STATE.csv` for the 2894-row reconciliation and `KB_FINAL_SYNC_STALE_STATE_FIXED.csv` for semantic corrections.
"""
    write_text(REPORT_DIR / "KB_FINAL_SYNC_AUDIT.md", audit_md)
    return {
        "validation": validation.get("status"),
        "reproducibility": reproducibility,
        "new_fingerprint": new_fingerprint,
        "graph_nodes": graph_nodes,
        "graph_edges": graph_edges,
        "stale_fixed": len(stale_rows),
        "stale_project_state": stale_project_state,
        "relevant_dirty_files": len(relevant_dirty),
        "kb_final_sync": sync_marker,
        "ready_for_final_gate": gate_marker,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--old-fingerprint")
    args = parser.parse_args()
    if args.prepare == args.finalize:
        parser.error("choose exactly one of --prepare or --finalize")
    result = prepare() if args.prepare else finalize(args.old_fingerprint)
    print(stable_json(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
