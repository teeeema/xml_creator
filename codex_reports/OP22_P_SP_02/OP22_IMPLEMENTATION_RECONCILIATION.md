# OP22 IMPLEMENTATION / EVIDENCE RECONCILIATION

Date: 2026-10-07  
Scope: OP22 / P.SP.02  
Mode: READ ONLY for production, tests, engine, and Knowledge Base. Only files in `codex_reports/OP22_P_SP_02` were created by this audit.

## Result

The Production Readiness statement that only 141 of 1263 historical `IMPLEMENTED_CONFIRMED` requirements have full requirement-level proof is supported as a proof/linkage statement. It is **not** supported as evidence that the other 1122 requirements have no production implementation.

Current reconciliation of all 1263 historical `IMPLEMENTED_CONFIRMED` rows:

- `RULE_EXISTS_EXACT`: **1019**
- `RULE_EXISTS_AGGREGATED`: **241**
- `RULE_IMPLEMENTED_BY_GENERIC_MECHANISM`: **3**
- `RULE_NOT_FOUND`: **0**

Therefore the 1122 rows outside the previous 141 full-proof set split into evidence/linkage gaps rather than 1122 missing implementations:

- B — exact production implementation exists and indirect negative evidence exists, but requirement-level proof is not linked: **108**
- C — exact production implementation exists, but no exact or rule-id-linked negative proof was found: **770**
- D — current coverage is only aggregated/inherited or generic and needs atomic review: **244**
- E — no production implementation found among historical `IMPLEMENTED_CONFIRMED`: **0**

The three generic-mechanism rows are the R.010 ONE_OF requirements:

- `P.SP.02.MSG.003:35:1`
- `P.SP.02.MSG.031:47:1`
- `P.SP.02.MSG.059:77:1`

They are implemented by the existing `embedded_structures` / ONE_OF infrastructure and have dedicated one-of tests, so absence of a `structured_rules` row is not evidence of missing production behavior.

## Classification method

`RULE_EXISTS_EXACT` requires either an exact current-table requirement rule id (for example `...T45.REQ.16`, including suffixed fragments) or an exact current-table/item `source_ref` on a current structured rule.

`RULE_EXISTS_AGGREGATED` is used only when an atomic canonical requirement is covered through a range such as `6-29` and no exact rule id or exact current-table/item source reference exists for that atomic row.

`RULE_IMPLEMENTED_BY_GENERIC_MECHANISM` is used only where the requirement is owned by established generic infrastructure rather than `structured_rules`. In OP22 this applies to the three R.010 ONE_OF requirements listed above.

Proof was kept deliberately stricter than implementation detection:

- `POSITIVE_TEST_EXACT`: requirement-specific traceability proof exists.
- `POSITIVE_TEST_INDIRECT`: no requirement-specific positive proof is linked, but the message has passing runtime/XML execution evidence.
- `NEGATIVE_TEST_EXACT`: requirement-specific negative proof exists.
- `NEGATIVE_TEST_INDIRECT`: the current rule id is referenced in an OP22 test file containing explicit fail/reject/invalid assertions, or the row is one of the three verified generic ONE_OF cases.
- `NEGATIVE_TEST_MISSING`: neither exact nor the above rule-linked indirect negative proof was found. A green global suite alone is not promoted to negative proof for a specific requirement.
- `REAL_XML_PROOF_EXACT` / `RUNTIME_PROOF_EXACT`: requirement-specific proof only.
- indirect real-XML/runtime proof comes from the current OP22 runtime matrix at message level and is not treated as atomic certification.

This avoids both failure modes: treating an empty KB `production_rules` list as missing production, and treating a general green test suite as full requirement-level certification.

## A-E groups for 1263 IMPLEMENTED_CONFIRMED

| Group | Meaning | Count |
|---|---|---:|
| A | REAL_IMPLEMENTATION_AND_FULL_PROOF | 141 |
| B | REAL_IMPLEMENTATION_BUT_PROOF_NOT_LINKED | 108 |
| C | REAL_IMPLEMENTATION_BUT_NEGATIVE_PROOF_MISSING | 770 |
| D | ONLY_GENERIC/AGGREGATED_COVERAGE_NEEDS_REVIEW | 244 |
| E | NO_PRODUCTION_IMPLEMENTATION_FOUND | 0 |
|  | **Total** | **1263** |

Implementation/proof detail for the 1263 rows:

| Evidence dimension | Status | Count |
|---|---|---:|
| Production | RULE_EXISTS_EXACT | 1019 |
| Production | RULE_EXISTS_AGGREGATED | 241 |
| Production | RULE_IMPLEMENTED_BY_GENERIC_MECHANISM | 3 |
| Positive tests | POSITIVE_TEST_EXACT | 141 |
| Positive tests | POSITIVE_TEST_INDIRECT | 1122 |
| Negative tests | NEGATIVE_TEST_EXACT | 141 |
| Negative tests | NEGATIVE_TEST_INDIRECT | 166 |
| Negative tests | NEGATIVE_TEST_MISSING | 956 |
| Real XML | REAL_XML_PROOF_EXACT | 141 |
| Real XML | REAL_XML_PROOF_INDIRECT_MESSAGE_RUNTIME | 1122 |
| Runtime | RUNTIME_PROOF_EXACT | 141 |
| Runtime | RUNTIME_PROOF_INDIRECT_MESSAGE_RUNTIME | 1122 |
| KB | KB_LINK_CORRECT | 141 |
| KB | KB_LINK_STALE | 1122 |

The 166 indirect negative rows consist of 108 exact-rule rows, 55 aggregated rows, and the 3 generic ONE_OF rows. Group C remains conservative: its 770 rows have real current exact production rules, but this audit did not find requirement-specific or rule-id-linked negative proof for them.

## Why the previous readiness result looked like 1122 false implementations

The previous proof gate correctly identified only 141 rows with a complete requirement-specific chain. However, production discovery based on KB `production_rules` / narrow current linkage missed current implementation patterns that are present in the repository:

- exact current structured rules whose KB requirement records still have no production linkage;
- inherited requirements represented through current-table rule ids plus range/current and leaf/original source references;
- range-based aggregated mappings such as `6-29`;
- generic R.010 ONE_OF semantics implemented in shared body/embedded-structure infrastructure.

After reconstructing production linkage from current `message_rules/*.yaml` rule ids and all structured-rule `source_refs`, the historical `IMPLEMENTED_CONFIRMED` set has 1260 structured-rule-backed rows plus 3 generic ONE_OF rows. No row in that 1263 set remained as `RULE_NOT_FOUND`.

## OPEN 346 review

The 346 historical OPEN rows were not closed or reclassified. The audit only checked whether a current production mapping is now present.

Current structured-rule mappings exist for **261 / 346** OPEN rows:

| Historical OPEN status | Now has mapping | No current structured-rule mapping |
|---|---:|---:|
| OPEN_CLASSIFIER | 99 | 66 |
| OPEN_EXTERNAL_REGISTRY | 14 | 7 |
| OPEN_NORMATIVE_AMBIGUITY | 20 | 5 |
| OPEN_PRODUCTION_MAPPING | 121 | 0 |
| OPEN_SOURCE_CONFLICT | 7 | 7 |
| **Total** | **261** | **85** |

A current mapping does not close these rows. Classifier, external-registry, normative ambiguity, and source-conflict blockers remain separate concerns. In particular, all 121 historical `OPEN_PRODUCTION_MAPPING` rows now have a current exact or aggregated structured-rule mapping and should be reconciled in the KB/status layer before any status change is considered.

## Special trace: P.SP.02.MSG.031 Table 49 REQ 19

Result: **CONFIRMED_BROKEN_TRACE**.

The original normative source `/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf`, PDF page **740**, confirms Table 49 requirement 19. It states the conditional requirement for a collective mark (`ipsdo:CollectiveMarkIndicator = 1`) to include `ipcdo:AccompanyingDocumentsDetails` with the required document kind code/name for the collective mark charter/regulation.

The current trace evidence for canonical row `P.SP.02.MSG.031:49:19` points to test parameters for `P.SP.02.MSG.031-48`, i.e. **Table 48 requirement 19**. The Table 49 row is historical `OPEN_CLASSIFIER`, has `WRONG_TEST_LINK`, and no current Table 49 requirement 19 structured-rule mapping was found. No correction was made.

This one broken trace is listed separately in `OP22_KB_STALE_LINKS.csv` as `BROKEN_REQUIREMENT_TEST_TRACE` so it is not confused with the 1122 historical implemented rows whose KB production linkage is missing/stale.

## KB reconciliation

For the 1263 historical implemented rows:

- `KB_LINK_CORRECT`: **141**
- `KB_LINK_STALE`: **1122**

`OP22_KB_STALE_LINKS.csv` contains those 1122 implemented rows plus the separately confirmed OPEN Table 49 / REQ 19 broken test trace. Therefore the CSV has 1123 data rows, while the final `KB_STALE_LINKS` metric below remains scoped to the required 1263 `IMPLEMENTED_CONFIRMED` review.

`OP22_TRUE_MISSING_IMPLEMENTATION.csv` intentionally contains only its header because E = 0 for the historical implemented set.

## Verification

Read-only/current-state evidence used:

- canonical inventory: 1609 rows = 1263 `IMPLEMENTED_CONFIRMED` + 346 OPEN;
- current OP22 `message_rules`: 57 files and 1643 structured-rule objects;
- existing OP22 GUI/XML runtime matrix: 111 rows, 61 distinct messages, **111 PASS**;
- canonical requirements span 57 messages and every one of those messages appears in the passing runtime matrix;
- original `ОП_22.pdf` page 740 visually checked for the Table 49 / REQ 19 special trace;
- current full OP22 test suite executed during this audit:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests -p no:cacheprovider`
  → **3110 passed, 0 failed** in 118.28s.

The 3110-pass result is supporting runtime/regression evidence. It is not treated as automatic requirement-level proof for rows without an explicit linkage.

## Final status

STATUS: COMPLETE

TOTAL: 1609  
IMPLEMENTED_CONFIRMED_REVIEWED: 1263  
OPEN_REVIEWED: 346

A_FULL_PROOF: 141  
B_IMPLEMENTED_PROOF_NOT_LINKED: 108  
C_IMPLEMENTED_NEGATIVE_MISSING: 770  
D_AGGREGATED_NEEDS_REVIEW: 244  
E_NO_IMPLEMENTATION_FOUND: 0

OLD_OPEN_NOW_HAS_MAPPING: 261

TABLE49_TRACE_RESULT: CONFIRMED_BROKEN_TRACE — source is Table 49 REQ 19, original PDF page 740; existing requirement-specific test/runtime references point to Table 48 REQ 19; no fix applied.

KB_STALE_LINKS: 1122 historical IMPLEMENTED_CONFIRMED rows (plus 1 separately listed OPEN wrong-test trace in the stale-links CSV)  
TRUE_MISSING_IMPLEMENTATION: 0

PRODUCTION_CHANGED: 0  
TESTS_CHANGED: 0  
KB_CHANGED: 0
