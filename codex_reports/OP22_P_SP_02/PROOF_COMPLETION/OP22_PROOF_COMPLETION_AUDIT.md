# OP22 PROOF COMPLETION AUDIT

Date: 2026-10-07  
Scope: OP22 / P.SP.02  
Write scope used: `P.SP.02_OP_22/tests/**` and `codex_reports/OP22_P_SP_02/PROOF_COMPLETION/**` only.

## Result

Strict requirement-level proof for the historical `IMPLEMENTED_CONFIRMED` set increased from **141** to **1263 / 1263**.

- Group A retained: **141**.
- Group B closed: **108 / 108** = **62** existing requirement-id test linkages + **46** new data-driven runtime proofs.
- Group C closed: **770 / 770** with a deterministic parameterized positive/targeted-negative matrix.
- Group D confirmed: **244 / 244** = **241** aggregated/inherited atomic proofs + **3** R.010 ONE_OF generic proofs.
- Group D review required: **0**.

The data-driven proof does not use arbitrary invalid XML. It loads the current production rule objects through `EaeuXmlEngine`, constructs a value set that satisfies each concrete rule, then mutates the exact semantic condition owned by that rule (`presence`, `fixed_value`, comparison, conditional presence/fixed value, cardinality, or cross-instance comparison). A row closes only when the production evaluator returns `PASS` before the mutation and `FAIL` after it and the rule source reference covers the canonical table/item.

## Group B linkage

Existing tests were reused when a pre-wave OP22 test named the current complete rule id and contained both positive and negative validation assertions. That closed **62** rows by linkage without duplicate tests. The remaining **46** rows receive the same deterministic requirement-specific runtime proof used for Group C.

## Group C negative proof

All **770** rows have current exact implementation. The proof matrix covers all current C rule shapes and source links. Targeted execution: **770/770 PASS** during development; these cases are also included in the final 1058-test proof-completion test file.

## Group D aggregated / generic review

For the **241** aggregated/inherited rows, a covering range alone was not accepted. Each canonical row had to resolve to at least one current executable rule carrying either an exact current-table item source ref or a covering current-table range plus a `CONFIRMED` inherited exact-item source ref. All **241** then passed positive + targeted-negative runtime proof.

The **3** generic rows are the R.010 ONE_OF requirements for MSG.003 Table 35 REQ 1, MSG.031 Table 47 REQ 1, and MSG.059 Table 77 REQ 1. Existing positive coverage binds all three messages to the ONE_OF mechanism. MSG.031 and MSG.059 already had requirement-specific negative neither/both-payload tests. MSG.003 lacked the matching OP22 negative test, so this wave adds only that missing rejection proof.

## Historical OPEN 346

Historical OPEN total: **346**. Current mappings now exist for **261**. The remaining **85** have no current mapping and reconcile to:

| Category | Count |
|---|---:|
| CLASSIFIER | 66 |
| EXTERNAL | 7 |
| SOURCE_CONFLICT | 7 |
| OTHER (preserved normative ambiguity) | 5 |
| XSD | 0 |
| TRUE_MAPPING_MISSING | 0 |
| **Total** | **85** |

The five `OTHER` rows remain `OPEN_NORMATIVE_AMBIGUITY`; they were not guessed into another category. This wave does not implement any of the 85.

## Broken trace: Table 49 REQ 19

`P.SP.02.MSG.031:49:19` remains **OPEN_CLASSIFIER**. The previously linked evidence belongs to **Table 48 REQ 19** and is explicitly excluded from proof completion for Table 49 REQ 19.

## Verification

Targeted proof-completion test:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests/test_proof_completion.py -p no:cacheprovider`

Result: **1058 passed, 0 failed** in 7.38s.

Full OP22 suite:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests -p no:cacheprovider`

Result: **4168 passed, 0 failed** in 532.52s. The prior baseline was **3110 passed**; 4168 = 3110 + 1058 new proof checks.

The requested four read-only subagent roles were launched, but the Codex/ChatGPT Web agent service terminated each before producing findings with: `stream disconnected before completion: ChatGPT Web supports at most 5 simultaneous browser turns; close or finish a browser tab before starting another`. Root therefore performed and independently verified all four evidence streams. No subagent write occurred.

`graphify update .` was not run because it would write `graphify-out/**`, outside the user's explicit write scope for this wave.

## Final

STATUS: COMPLETE

TOTAL: 1609  
FULL_PROOF_BEFORE: 141  
FULL_PROOF_AFTER: 1263

GROUP_B_CLOSED: 108  
GROUP_C_CLOSED: 770  
GROUP_D_CONFIRMED: 244  
GROUP_D_REVIEW_REQUIRED: 0

OLD_OPEN_TOTAL: 346  
OLD_OPEN_NOW_MAPPED: 261  
TRUE_MISSING_MAPPING: 0  
BLOCKED: 85 (CLASSIFIER 66; EXTERNAL 7; SOURCE_CONFLICT 7; OTHER 5; XSD 0)

TABLE49_REQ19: OPEN_CLASSIFIER

PRODUCTION_CHANGED: 0  
ENGINE_CHANGED: 0  
KB_CHANGED: 0

TEST_RESULTS: targeted 1058 passed; full OP22 4168 passed, 0 failed.
