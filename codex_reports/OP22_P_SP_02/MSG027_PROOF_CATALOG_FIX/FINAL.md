# OP22 MSG027 proof-catalog correction — 2026-10-23

## ROOT_CAUSE / A–B–C diagnosis

**A — stale proof catalog: CONFIRMED.** The 2026-10-13 proof matrix and reconciliation row classify P.SP.02.MSG.027:57:3 as RULE_EXISTS_EXACT / FULL_PROOF_CLOSED, expecting executable P.SP.02.MSG.027.T57.REQ.3 (conditional_fixed_value). Negative-results CSV claims historical PASS→FAIL for that old component. Subsequent source-confirmed classifier-present implementation removed the inapplicable executable fallback, but these proof artifacts and the regression gate retained their old expectations.

**B — production-validator error: NOT CONFIRMED for this failure.** Actual raw XML Code07365 passes REQ2, wrong99999/missing Code/Code+Name/Name-only fallback fail. Current production files were not changed in this task (production_scope_check.json). The catalog failure was a missing old rule ID during component lookup, not an incorrect validator result.

**C — normative-source trace error: NOT CONFIRMED.** Canonical Table57 REQ3 and its business-rule source text remain intact. The stale catalog incorrectly conflated source existence with branch applicability and executable closure. Correct trace explicitly relates the inactive REQ3 condition to current active REQ2; it does not pretend REQ2 is a direct executable source mapping of REQ3.

## Exact failing test and traceback

P.SP.02_OP_22/tests/test_old_open261_mapped_proof.py::test_old_open_now_mapped_requirement_matches_strict_proof_verdict[P.SP.02.MSG.027:57:3]

Reproduced command: `PYTHONPATH=eaeu_xml/src python3.13 -m pytest -vv --tb=long --showlocals 'P.SP.02_OP_22/tests/test_old_open261_mapped_proof.py::test_old_open_now_mapped_requirement_matches_strict_proof_verdict[P.SP.02.MSG.027:57:3]'`.

Original failure: AssertionError at line58: `P.SP.02.MSG.027:57:3: ['P.SP.02.MSG.027.T57.REQ.3']`. Full traceback and locals are preserved in before_traceback.log, not replaced by a summary-only result.

## NORMATIVE_EXPECTATION

OP22 / P.SP.02.PRC.034 / P.SP.02.TRN.022 / P.SP.02.MSG.027 / R.IP.SP.02.002. Direct XML owner ipcdo:TrademarkApplicationDetails; fields ipsdo:IPDocKindCode and ipsdo:IPDocKindName. QName handling is namespace-aware; nested same-name fields are not the direct fields.

ОП_22.pdf physical pp578–579, Table57: REQ2 requires the document-kind code and omits Name when the classifier contains the corresponding entry. REQ3 requires the prescribed Name-only fallback only when the classifier lacks that entry. Decision92 physical p15 and Decision148 p4 confirm07365 for the withdrawn-application notification; the actual local P.CLS.027 snapshot contains the same entry. Original PDF excerpts/hashes and snapshot entry: sources.json. No code was borrowed from another message. The condition concerns classifier contents, not Code absence in a submitted XML.

## FIX

Retain all261 canonical requirements and their parametrized tests. Reclassify only MSG027:57:3 as CONDITIONAL_INACTIVE. Replace the stale component mapping with an explicit applicability relationship to active REQ2. The gate now verifies classifier07365, retained REQ3 condition/source, inactive executable fallback and full serialized/reparsed/extracted positive/negative XML under current REQ2. This is an executed assertion path, not pytest.skip/xfail, test deletion or a forced PASS.

The current partition is141 FULL_PROOF_CLOSED +1 CONDITIONAL_INACTIVE +98 SEMANTIC_REVIEW_REQUIRED +21 PROOF_INCOMPLETE =261. Historical142 full closures are preserved as historical in the audit, with an explicit supersession note. No new FULL_PROOF_CLOSED claim is made for inactive REQ3.

Exact old/new rows: catalog_changes.json. Canonical source table/item/page remain57/3/579; no source_ref is fabricated or rewritten to make the test pass.

## ACTUAL XML / regression proof

runtime.json records five actual serialized XML bodies and hashes:

| Scenario | Expected / actual | Active rule |
|---|---|---|
| Code07365, no direct Name | accept / accept | T57.REQ.2 PASS |
| Code99999 | reject / reject | T57.REQ.2 FAIL |
| no Code | reject / reject | T57.REQ.2 FAIL |
| Code+Name | reject / reject | T57.REQ.2 FAIL |
| prescribed legacy Name-only fallback | reject / reject | T57.REQ.2 FAIL |

MSG027 focused tests include exact nested document-kind collision/isolation cases and real form/resolver/sanitization checks. Test-mode XML body proof is not production-XSD proof.

## CHANGED_FILES

- P.SP.02_OP_22/tests/test_old_open261_mapped_proof.py: one conditional-inactive verdict in the partition; meaningful applicability/raw-XML proof for that preserved canonical test.
- codex_reports/OP22_P_SP_02/OP22_IMPLEMENTATION_RECONCILIATION.csv: only MSG027:57:3 row, current applicability/mechanism/proof trace.
- codex_reports/OP22_P_SP_02/FINAL_MAPPED_PROOF/OP22_OLD_OPEN261_PROOF_MATRIX.csv: only MSG027:57:3 row.
- codex_reports/OP22_P_SP_02/FINAL_MAPPED_PROOF/OP22_OLD_OPEN261_NEGATIVE_RESULTS.csv: only MSG027:57:3 row and related current evidence.
- codex_reports/OP22_P_SP_02/FINAL_MAPPED_PROOF/OP22_OLD_OPEN261_PROOF_AUDIT.md: current correction note over preserved historical report.
- This evidence directory; graphify-out AST refresh.

No production validator/classifier/message policy was edited. Other OP and parallel changes preserved. No commit/push/reset/restore/clean. CONTROL_VERIFICATION counters14 PASS /1 SOURCE_BLOCKED are not modified by this separate catalog correction.

## VERIFICATION

Focused command: `PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests/test_old_open261_mapped_proof.py P.SP.02_OP_22/tests/test_msg027* --tb=short` — **361 passed in4.25s** (100 MSG027 tests plus261 catalog cases), focused.log.

Sibling command: `PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg001* P.SP.02_OP_22/tests/test_msg004* P.SP.02_OP_22/tests/test_msg005* --tb=short` — **187 passed in11.81s**, msg001_004_005.log.

Full OP22 result is recorded below after completion. Graphify AST refresh completed; HTML remains stale above the visualization size limit. Production source hashes checked unchanged. Cross-OP regression not required because production/shared behavior is unchanged.


Final full command: `PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests --tb=short` — **4461 passed in121.58s**, op22_full.log. No failures, skips or xfails were introduced to bypass the old case.

`git diff --check`: PASS (exit0). New untracked test whitespace checked separately. Catalog partition and full final diff reviewed;217 existing production/source files match pre-task hashes. No production behavior change.

REMAINING_BLOCKERS: None for this regression correction. Existing unrelated normative/external-source limitations remain outside scope; green regression is not whole-project normative certification.

**OP22_REGRESSION_STATUS = PASS**
