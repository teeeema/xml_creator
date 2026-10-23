# OP22 OLD_OPEN_NOW_MAPPED — FINAL MAPPED-PROOF AUDIT

Date: 2026-10-13  
Process: OP22 / P.SP.02  
Target queue: `OLD_OPEN_NOW_MAPPED` from `codex_reports/OP22_P_SP_02/PROOF_COMPLETION/OP22_OPEN346_CURRENT_STATE.csv`  
Write scope used: `P.SP.02_OP_22/tests/**` and `codex_reports/OP22_P_SP_02/FINAL_MAPPED_PROOF/**` only.

## Current correction — 2026-10-23

The 2026-10-13 counts below are historical. Current catalog partition is **141 FULL_PROOF_CLOSED, 1 CONDITIONAL_INACTIVE, 98 SEMANTIC_REVIEW_REQUIRED, 21 PROOF_INCOMPLETE = 261**. No requirement or test was removed.

MSG027 Table57 REQ3 previously claimed executable `conditional_fixed_value` proof. The authoritative current classifier contains07365 (Decision92 p15; Decision148 p4), so REQ2 applies and REQ3's classifier-absent condition is false. The canonical REQ3 row and source remain; current proof checks condition applicability and rejects the obsolete fallback via active REQ2. This is not an executable REQ3/full-closure claim. Production was unchanged.

Exact before/after rows, sources, traceback, actual positive/negative XML and current tests: [MSG027 proof-catalog correction](../MSG027_PROOF_CATALOG_FIX/FINAL.md).

## Historical result

The historical strict proof baseline remains **1263**. The current historical OPEN queue contains **261** requirements with a current production mapping and **85** still-unmapped blockers.

For the 261 mapped candidates, strict closure was attempted with the same requirement-specific proof standard used for the historical 1263: canonical source linkage, concrete current production mechanism, positive runtime proof, targeted negative runtime proof, and requirement-specific attribution of the executed mechanism.

Final partition of the 261:

| Verdict | Count |
|---|---:|
| FULL_PROOF_CLOSED | 142 |
| PROOF_INCOMPLETE | 21 |
| SEMANTIC_REVIEW_REQUIRED | 98 |
| **Total** | **261** |

Therefore:

- `FULL_PROOF_AFTER = 1263 + 142 = 1405`.
- The remaining 119 mapped candidates were **not** promoted to closed merely because a range/aggregate production rule covers their table item numerically.

## What closed

The 142 closed rows consist of:

- **123 exact mappings** whose current rule/mechanism has canonical source coverage and deterministic `PASS -> FAIL` proof.
- **19 aggregated/inherited mappings** that additionally resolve to a confirmed atomic inherited source item before runtime proof is accepted.

The runtime proof loads the current OP22 production rules through `EaeuXmlEngine` and evaluates the concrete structured rule with `StructuredRuleEvaluator`. Each closed row has a valid constructed value set producing `PASS` and a targeted semantic mutation producing `FAIL`.

## Why 98 require semantic review

These 98 rows have an executable aggregate/range mechanism and the mechanism itself can be exercised with deterministic positive and targeted-negative runtime proof. However, the production trace provides only a current-table range source reference and **does not provide a confirmed atomic source link that attributes a specific executable component to the canonical requirement item**.

Because `mapped != closed`, these rows remain `SEMANTIC_REVIEW_REQUIRED`.

## Why 21 are proof incomplete

These 21 rows have the same missing atomic source attribution as the semantic-review group. In addition, the aggregate mechanism does not complete the targeted-negative gate for every evaluated component: at least one component remains `PASS` after the attempted targeted mutation.

They remain `PROOF_INCOMPLETE`; no production change was made to force closure.

## Blocked 85

The 85 unmapped blockers remain unchanged:

| Category | Count |
|---|---:|
| CLASSIFIER | 66 |
| EXTERNAL | 7 |
| SOURCE_CONFLICT | 7 |
| OTHER / normative ambiguity | 5 |
| **Total** | **85** |

`TRUE_MAPPING_MISSING = 0` remains unchanged from the prior reconciliation: these 85 are evidence/source blockers, not unexplained missing-production rows.

## Table 49 REQ 19 guard

`P.SP.02.MSG.031:49:19` is **not** part of the candidate 261. It remains in `OP22_FINAL_BLOCKED85.csv` as:

- current state: `UNMAPPED_BLOCKED`;
- category: `CLASSIFIER`;
- final blocker status: `BLOCKED_CONFIRMED`.

No evidence from Table 48 REQ 19 is used to close Table 49 REQ 19.

## Test matrix

`P.SP.02_OP_22/tests/test_old_open261_mapped_proof.py` adds one parameterized requirement-specific test case for each of the 261 candidate rows.

For `FULL_PROOF_CLOSED`, the test requires source-attributable runtime components and verifies `PASS -> FAIL` for every returned component.

For `SEMANTIC_REVIEW_REQUIRED` and `PROOF_INCOMPLETE`, the test explicitly requires the strict aggregated proof to stop at `NO_ATOMIC_SOURCE_LINK`, preventing range-only mapping from being silently promoted to full proof. The proof-incomplete rows additionally preserve the observed aggregate negative-proof failure.

## Verification

Targeted new proof matrix:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests/test_old_open261_mapped_proof.py -p no:cacheprovider`

Result on the final stable workspace state: **261 passed, 0 failed** in 0.23s.

Full OP22 suite:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests -p no:cacheprovider`

Result on the final stable workspace state: **4429 passed, 0 failed** in 146.55s.

Baseline before this task: **4168 passed**. The increase is exactly **261** new requirement-specific cases.

## Scope protection

No production rule, engine, or Knowledge Base file was changed by this task.

The workspace already contained unrelated parallel changes in OP23, OP26, OP49 and other paths before this task; they were preserved. During this task, separate parallel work also made `eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py` and `validator.py` dirty. Those engine changes were not made or edited by this task. The final targeted 261 proof and the full 4429-test OP22 suite were run after the latest observed engine change, and both engine file mtimes remained unchanged for the entire final full-suite run.

## Final state

STATUS: COMPLETE_WITH_REMAINING_MAPPED_PROOF_GAPS

TOTAL: 1609  
FULL_PROOF_BEFORE: 1263  
OLD_OPEN_NOW_MAPPED_TARGET: 261  
CLOSED_FROM_261: 142  
PROOF_INCOMPLETE: 21  
SEMANTIC_REVIEW_REQUIRED: 98  
FULL_PROOF_AFTER: 1405

BLOCKED_EXPECTED: 85  
BLOCKED_CONFIRMED: 85  
BLOCKED_CHANGED: 0

TRUE_MAPPING_MISSING: 0

PRODUCTION_CHANGED: 0  
ENGINE_CHANGED: 0  
KB_CHANGED: 0

NEW_TEST_CHECKS: 261  
FULL_OP22_TEST_RESULTS: 4429 passed, 0 failed

NEXT_ACTION: review the 98 range-only mappings against exact normative semantics/source lineage first; then address the 21 rows that additionally lack complete targeted-negative proof. Do not modify production until the atomic normative mapping is confirmed.
