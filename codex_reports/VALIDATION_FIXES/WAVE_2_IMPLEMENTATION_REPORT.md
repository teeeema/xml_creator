# WAVE 2 — OP23 B1 implementation report

## STATUS

`B1_SIMPLE_PRESENCE_AND_COMPARISON` is reproduced as exactly **162** canonical OP23 B1 requirements. The deterministic safe batch map contains **608** safe candidates: B1=162, B2=214, B3=159, B4=73. The remaining **102** of 710 canonical requirements remain outside the safe batches: 44 classifier, 39 external registry, 18 source conflict, 1 missing normative data.

`OP23_B1_IMPLEMENTATION_RESULTS.csv` is synchronized to **162/162 CLOSED_CONFIRMED**. No blocked row was promoted into B1 to reach the expected count.

## ROOT CAUSE 1 — historical row-level mapping blocker

The historical triage snapshot did not contain a complete REQ → B1/B2/B3/B4 row-level assignment. The current checkout contains `OP23_SAFE_IMPLEMENTATION_BATCH_MAP.csv`, which deterministically reproduces the agreed 162/214/159/73 split.

## ROOT CAUSE 2 — stale B1 implementation snapshot

Twenty-two B1 rows were still marked `NOT_PROCESSED`, although the current production rule files already contained executable structured-rule wiring and the current B1 test suite contained requirement-specific real-XML positive/negative coverage. The result CSV was stale relative to the current worktree and was synchronized only after verification.

## ROOT CAUSE 3 — MSG.022 positive generation failed before the intended B1 assertion

MSG.022 requirements REQ.001, REQ.002, REQ.006, REQ.007, REQ.008 and REQ.009 are in the reproduced B1 scope. Before the WAVE 2 generator fix, the B1 suite had **617 passed, 14 failed**. All 14 failures were in the MSG.022 positive-document path and occurred while building the supposedly valid baseline, before the negative mutation under test.

The shared `TestDataGenerator` did not fully materialize a complex branch selected by a `for_each` `condition.any` rule of the form `complex-group NE null`. MSG.022 REQ.007 requires `ipcdo:IPPaymentDetails` and at least one of `ccdo:BankAccountDetails` / `ccdo:PaymentSystemAccountDetails`. The generator could select safe scalar alternatives, but a complex alternative with required descendants was not materialized generically.

The shared generator now treats a selected complex `NE null` alternative as structural presence and walks its required descendants. Structural-presence materialization is tracked separately from ordinary cardinality paths, so a generic cardinality rule keeps the existing `[None]` minimum-instance representation. This narrowing is covered by a regression test.

The old MSG.022 helper fallback that manually created `IPPaymentDetails` / account data after `build_body()` was removed. The helper now depends on the shared generator for REQ.007 baseline validity.

## IMPLEMENTATION

- B1 mapping: **162/162 confirmed**.
- B1 production wiring: **162/162 present**.
- B1 result rows: **162/162 CLOSED_CONFIRMED**.
- Shared generator: complex `condition.any` `NE null` branches can materialize a complex group and its required descendants.
- Cardinality compatibility: generic cardinality-only complex groups retain the established `[None]` minimum-instance representation.
- MSG.022 fixture: no payment/account post-build fallback remains.
- Validator logic and OP23 normative rules were not weakened or relaxed.

## NORMATIVE BASIS

The per-case source/version/page/table fields remain in `WAVE_2_B1_CASES.csv` only where confirmed by current canonical records.

For the generator defect that exposed MSG.022 REQ.007:

- Trace: OP23 → P.SP.03.PRC.008 → P.SP.03.TRN.017 → P.SP.03.MSG.022 → REQ.007.
- Structure: `R.IP.SP.03.003`.
- Paths: `ipcdo:IPPaymentDetails`; `ipcdo:IPPaymentDetails/ccdo:BankAccountDetails`; `ipcdo:IPPaymentDetails/ccdo:PaymentSystemAccountDetails`.
- Source: `ОП_23.pdf`, version context `P.SP.03 1.0.0`, Table 26, PDF page 283, item 7.
- Evidence level in KB: `CONFIRMED_PDF`.

No QName namespace URI, classifier, source ref, page, table, point, literal or version was invented. Knowledge Base content was not changed by WAVE 2.

## CHANGED FILES

- `eaeu_xml/src/eaeu_xml/application/services.py` — shared test-data generator rule materialization, including complex non-null alternatives and the cardinality-preserving structural-presence distinction.
- `eaeu_xml/tests/test_required_form_data.py` — shared generator regression for complex `condition.any` non-null branches; existing cardinality regression protects old semantics.
- `P.SP.03_OP_23/tests/test_b1_production.py` — removed the obsolete MSG.022 payment/account fallback so the positive baseline proves shared generator behavior.
- `codex_reports/OP23_P_SP_03/OP23_B1_IMPLEMENTATION_RESULTS.csv` — synchronized stale B1 statuses to 162/162 closed.
- `codex_reports/VALIDATION_FIXES/WAVE_2_MAPPING_REPORT.md` — deterministic mapping summary.
- `codex_reports/VALIDATION_FIXES/WAVE_2_B1_CASES.csv` — exact 162-case WAVE 2 registry.
- `codex_reports/VALIDATION_FIXES/WAVE_2_REGRESSION_RESULTS.md` — final verification record.
- `codex_reports/OP23_P_SP_03/OP23_B1_IMPLEMENTATION_AUDIT.md` — final B1 audit summary.
