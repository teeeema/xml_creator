# OP49 / P.DS.01 — Safe Implementation Wave 1 Audit

Date: 2026-10-07

## ROOT_CAUSE

The historical safe queue over-classified three of the six Wave 1 rows. Reverification against the original `49_ОП.pdf` showed that only three are message-local rules supported by the current OP49 structure and evaluator. The other three require respectively an unmodeled amount attribute, prior-message/history state, and authoritative country-to-currency reference data.

At the start of this run, the working tree already contained in-scope uncommitted structured rules and regression tests for `MSG.002.REQ.001`, `MSG.002.REQ.007`, and `MSG.006.REQ.006`. Those changes were preserved and verified rather than rewritten.

## IMPLEMENTED / CLOSED

- `OP49.P_DS_01.MSG_002.REQ.001` — `P.DS.01.MSG.002.R001`, cardinality 1..1 for `ChargedDistributedDutyReportDetails`. Normative basis: `49_ОП.pdf`, p.85, table 11, item 1.
- `OP49.P_DS_01.MSG_002.REQ.007` — `P.DS.01.MSG.002.R007`, `ReportDate > EventDate`. Normative basis: p.86, table 11, item 7.
- `OP49.P_DS_01.MSG_006.REQ.006` — `P.DS.01.MSG.006.R006`, `ReportDate > EventDate`. Normative basis: p.103, table 14, item 6.

For these three, the prefixed field paths are also present in the current OP49 `R.FP.DS.01.001` StructureDefinition with source references to the normative structure table. No namespace/QName fallback or local-name-only matching was introduced.

## RECLASSIFIED

### `OP49.P_DS_01.MSG_002.REQ.034` → `ENGINE_GAP`

`49_ОП.pdf`, p.91, table 11, item 34 requires `currencyCode` on `ds01sdo:StopTransferDistributedDutyAmount`. The current `R.FP.DS.01.001` StructureDefinition contains the amount element but no `.../StopTransferDistributedDutyAmount/@currencyCode` field. A direct runtime probe with that path returns `UNKNOWN_FIELD`. Implementing a rule alone would create a permanently failing/unsatisfiable production rule, and fixing the responsible structure/shared layer is outside this wave scope.

### `OP49.P_DS_01.MSG_005.REQ.001` → `EXTERNAL_REGISTRY_BLOCKED`

`49_ОП.pdf`, p.93, table 13, item 1 requires one report instance for every month whose information had previously been sent, starting with the month being changed. This is not a plain message cardinality check: it needs authoritative historical state identifying previously sent months. No such state is available in the allowed OP49 message-rule/test scope.

### `OP49.P_DS_01.MSG_005.REQ.018` → `CLASSIFIER_BLOCKED`

`49_ОП.pdf`, p.96, table 13, item 18 requires `currencyCode` to correspond to the currency of the member state identified by `ReportCountryCode`. That requires authoritative country-to-currency classifier/reference data and its version. The task explicitly excludes classifier dependencies from implementation in this wave.

## NORMATIVE_BASIS

CONFIRMED for the three closed rows from the original `49_ОП.pdf` at the pages/items listed above.

CONFIRMED blocker semantics for the three reclassified rows from the same original PDF. No normative behavior was inferred to force 6/6 closure.

## CHANGED_FILES

Wave outputs created by this run:

- `codex_reports/OP49_P_DS_01/IMPLEMENTATION_WAVE_1/OP49_WAVE1_RESULTS.csv`
- `codex_reports/OP49_P_DS_01/IMPLEMENTATION_WAVE_1/OP49_WAVE1_AUDIT.md`
- `codex_reports/OP49_P_DS_01/IMPLEMENTATION_WAVE_1/OP49_WAVE1_RECLASSIFIED.csv`

Existing in-scope working-tree changes verified as the implementation under review:

- `P.DS.01_OP_49/message_rules/P.DS.01.MSG.002.yaml`
- `P.DS.01_OP_49/message_rules/P.DS.01.MSG.006.yaml`
- `P.DS.01_OP_49/tests/test_process_pipeline.py`

No shared engine files, Knowledge Base files, other OP packages, or OP49 structure files were changed by this run.

## VERIFICATION

- Original `49_ОП.pdf` re-read for Wave 1 evidence: pp.85, 86, 91, 93, 96, 103; OP49 structure source was also checked.
- Runtime blocker probe for `MSG.002.REQ.034`: `StopTransferDistributedDutyAmount/@currencyCode` is rejected with `UNKNOWN_FIELD` because it is absent from `StructureDefinition R.FP.DS.01.001`.
- Structured production mapping count after current Wave 1 implementation: **39**; the three closed Wave 1 rule IDs are loaded.
- Targeted Wave 1 tests: `pytest -q P.DS.01_OP_49/tests/test_process_pipeline.py -k wave1` → **6 passed, 12 deselected**.
- Full OP49 package tests: `pytest -q P.DS.01_OP_49/tests` → **32 passed**.

Multi-agent read-only review was requested and attempted. The Codex environment rejected all spawned subagent turns with `stream disconnected before completion: ChatGPT Web supports at most 5 simultaneous browser turns`; therefore no subagent conclusion was used as evidence. The final review was performed locally from original normative evidence, current source, runtime behavior, tests, and final diff.

## FINAL DIFF REVIEW

The implemented rules are limited to current OP49 message-rule files and use existing `cardinality` / `comparison` primitives. Regression coverage contains both PASS and FAIL cases for each closed rule. No special-case evaluator behavior or shared-engine modification was introduced.

## REMAINING_ISSUES

- `MSG.002.REQ.034`: structure/attribute capability must be resolved at the responsible layer.
- `MSG.005.REQ.001`: authoritative prior-message/history state is required.
- `MSG.005.REQ.018`: authoritative member-state currency mapping/classifier is required.
