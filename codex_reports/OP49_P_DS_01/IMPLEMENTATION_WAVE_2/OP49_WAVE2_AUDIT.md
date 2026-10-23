# OP49 / P.DS.01 — Implementation Wave 2 Audit

Date: 2026-10-13

## ROOT_CAUSE

The shared-engine wave made the seven calendar-month / context-scoped aggregate requirements executable with existing generic primitives. Reverification of the full 21-row candidate set found that `MSG.005.REQ.041–054` are still not safely representable: item 41 requires selecting the previous `ChargedDistributedDutyReportDetails` by calendar month while simultaneously restricting the nested `ChargedDistributedDutyDetails` owner to `DailyInfoIndicator=0`. The current `relative_to_context` selector stays on the same context path/sibling family and does not provide a safe correlated nested-parent relation for that combination. A positional or broadcast workaround could compare daily records and would violate the normative scope.

Therefore Wave 2 implements seven requirements and leaves fourteen explicitly `STILL_ENGINE_BLOCKED`. No closure was forced.

## IMPLEMENTATION

Implemented and closed with production rule + positive proof + targeted negative proof + serialized XML proof:

- `OP49.P_DS_01.MSG_002.REQ.006` → `P.DS.01.MSG.002.R006` — 49_ОП.pdf p.86 table 11 item 6.
- `OP49.P_DS_01.MSG_005.REQ.023` → `P.DS.01.MSG.005.R023` — 49_ОП.pdf p.96 table 13 item 23.
- `OP49.P_DS_01.MSG_005.REQ.029` → `P.DS.01.MSG.005.R029` — 49_ОП.pdf p.97 table 13 item 29.
- `OP49.P_DS_01.MSG_005.REQ.036` → `P.DS.01.MSG.005.R036` — 49_ОП.pdf p.99 table 13 item 36.
- `OP49.P_DS_01.MSG_006.REQ.019` → `P.DS.01.MSG.006.R019` — 49_ОП.pdf p.105 table 14 item 19.
- `OP49.P_DS_01.MSG_006.REQ.025` → `P.DS.01.MSG.006.R025` — 49_ОП.pdf p.106 table 14 item 25.
- `OP49.P_DS_01.MSG_006.REQ.032` → `P.DS.01.MSG.006.R032` — 49_ОП.pdf p.108 table 14 item 32.

The aggregate rules use the existing `for_each` + context-scoped `aggregate_comparison` pattern so totals are checked within each report context. `MSG.002.REQ.006` uses the existing `CALENDAR_MONTH` comparison with `offset_months=1`.

## REVERIFIED / STILL ENGINE BLOCKED

- `OP49.P_DS_01.MSG_005.REQ.041` — `Scope rule: only reports having a previous report one calendar month earlier; checks 42-54 apply only to nested ChargedDistributedDutyDetails with DailyInfoIndicator=0.`; 49_ОП.pdf p.100 table 13 item 41; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.042` — `EnteredDutyAmount`; 49_ОП.pdf p.100 table 13 item 42; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.043` — `ScoreDutyDeptRepayReptDayAmount`; 49_ОП.pdf p.100 table 13 item 43; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.044` — `ScoreDutyDeptRepayCurrentDayAmount`; 49_ОП.pdf p.100 table 13 item 44; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.045` — `ReturnDutyReptDayAmount`; 49_ОП.pdf p.101 table 13 item 45; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.046` — `ReturnDutyCurrentDayAmount`; 49_ОП.pdf p.101 table 13 item 46; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.047` — `UnacceptedDutyReturnAmount`; 49_ОП.pdf p.101 table 13 item 47; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.048` — `DistributableDutyAmount`; 49_ОП.pdf p.101 table 13 item 48; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.049` — `TransferDistributedDutyAmount`; 49_ОП.pdf p.101 table 13 item 49; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.050` — `InternalRevenueDistributedDutyAmount`; 49_ОП.pdf p.102 table 13 item 50; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.051` — `StopTransferDistributedDutyAmount`; 49_ОП.pdf p.102 table 13 item 51; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.052` — `TotalExternalRevenueDistributedDutyAmount`; 49_ОП.pdf p.102 table 13 item 52; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.053` — `ExternalRevenueDistributedDutyAmount`; 49_ОП.pdf p.102 table 13 item 53; `STILL_ENGINE_BLOCKED`.
- `OP49.P_DS_01.MSG_005.REQ.054` — `DefaultInterestAmount`; 49_ОП.pdf p.102 table 13 item 54; `STILL_ENGINE_BLOCKED`.

For requirements 42-54 the blocking condition is inherited from the normative scope in item 41: each field comparison must use the previous monthly report and the nested monthly (`DailyInfoIndicator=0`) detail instance. Their confirmed source text is not the problem; the missing capability is a safe generic way to preserve both contexts simultaneously.

## NORMATIVE_BASIS

CONFIRMED from original `49_ОП.pdf` for all 21 reviewed candidates. The primary PDF SHA-256 checked during this Wave 2 review is `81f82f343650ea19bb293ef7f45d86c57e9195e0cef315e4d190ab47e6d8bae8`, matching the registered source. Relevant source locations: table 11 item 6; table 13 items 23, 29, 36, 41-54; table 14 items 19, 25, 32. Current `R.FP.DS.01.001/1.0.0` contains the prefixed field paths used by these candidates. No known `CountryCode`/`UnifiedCountryCode`, `ModificationDate`/`ModificationDateTime`, or `VerificationPro`/`VerificationProDetails` conflict is used to force any closure in this wave.

## CHANGED_FILES

Production/test files changed by Wave 2:

- `P.DS.01_OP_49/message_rules/P.DS.01.MSG.002.yaml` — added `R006`; pre-existing Wave 1 rules preserved.
- `P.DS.01_OP_49/message_rules/P.DS.01.MSG.005.yaml` — added `R023`, `R029`, `R036`.
- `P.DS.01_OP_49/message_rules/P.DS.01.MSG.006.yaml` — added `R019`, `R025`, `R032`; pre-existing Wave 1 rule preserved.
- `P.DS.01_OP_49/tests/test_process_pipeline.py` — adjusted valid baseline values so the new `R006` calendar-month invariant is satisfied; pre-existing Wave 1 tests preserved.
- `P.DS.01_OP_49/tests/test_wave2_implementation.py` — new requirement-specific positive, negative, and serialized XML proof for all seven implemented rules.

Wave 2 reports:

- `OP49_WAVE2_CANDIDATE_REVERIFY.csv`
- `OP49_WAVE2_RESULTS.csv`
- `OP49_WAVE2_AUDIT.md`
- `OP49_WAVE2_RECLASSIFIED.csv`
- `OP49_WAVE2_RUNTIME_PROOF.csv`

No Knowledge Base, shared-engine source/tests, GUI, OP49 structure files, or other OP packages were intentionally edited as part of the Wave 2 implementation. Existing unrelated working-tree changes were preserved.

## VERIFICATION

- Candidate set reviewed: **21**.
- `ALREADY_IMPLEMENTED`: **0**.
- `SAFE_TO_IMPLEMENT_NOW`: **7**.
- Implemented / strict-closure proof complete: **7**.
- `STILL_ENGINE_BLOCKED`: **14**.
- Structured production mapping count: **39 → 46**.
- Focused Wave 2: `pytest -q P.DS.01_OP_49/tests/test_wave2_implementation.py` → **14 passed in 0.21s**.
- Full OP49: `pytest -q P.DS.01_OP_49/tests` → **46 passed in 1.07s**.
- Relevant shared engine read-only regression: calendar-month relation + context-scoped aggregates → **3 passed, 15 deselected in 0.22s**.
- `graphify update .` completed successfully; graph rebuilt to 39,521 nodes / 49,745 edges / 5,145 communities. HTML regeneration remained stale because the graph exceeds the visualization node limit; `graph.json` and `GRAPH_REPORT.md` were updated.
- `git diff --check` → **PASS**.

## REMAINING_ISSUES

- `MSG.005.REQ.041–054`: require a shared generic selector/context capability that can correlate the previous report by calendar month and constrain the nested owner to `DailyInfoIndicator=0` without positional/broadcast assumptions.
- After that engine capability exists, reverify all 14 requirements against the same original source before adding production rules.
