# P.SP.02.MSG.044 Implementation Report

## STATUS

COMPLETE

## VERDICT

READY

## CHANGED_FILES

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.044.yaml` — MSG.044 structured rules, audit metadata, normative context, and exact executable mapping.
- `P.SP.02_OP_22/tests/test_msg044_safe_mapping.py` — exact classification/mapping/provenance assertions.
- `P.SP.02_OP_22/tests/test_msg044_repeatable_xml.py` — repeatable-owner, status/event, signature, validity, and same-parent regression coverage.
- `P.SP.02_OP_22/tests/test_msg044_end_to_end.py` — production build/serialize/parse/extract/validate coverage and negative proofs.
- `codex_reports/MSG044_IMPLEMENTATION_REPORT.md` — this report.

## IMPLEMENTATION

MSG.044 is implemented from the prepared mapping for Table 62 while preserving the existing MSG.044 business rules. The structured-rule set contains 27 rule objects and 24 distinct executable requirement codes.

REQ.4 remains completely unmapped because its record-state lookup depends on external national patent-office information resources. REQ.5 is mapped to the status data owned by each `ipcdo:TrademarkApplicationDetails`: `csdo:StatusCode` is required and fixed to `30`, `@codeListId` is forbidden, and `csdo:EventDate` is required. The explicit container-presence assertion for `ipcdo:IPEntityStatusDetails` was omitted because the evaluator's pre-build value shape represents that repeatable parent separately; the required nested fields still make a missing status instance fail without adding an unsupported parent-scalar check.

REQ.27 is evaluated under the same `ipcdo:TrademarkDetails` parent. REQ.30–32 preserve the prepared `SignatureDetails` ownership/semantics. REQ.33 requires `StartDateTime`; REQ.34 requires `EndDateTime`.

## MAPPING_COUNTS

- Captured requirements: 11 source rows, expanded to 34 requirements.
- FULL: 24 — {1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34}.
- SAFE_PARTIAL: 0.
- EXTERNAL: 3 — {2, 3, 4}.
- AMBIGUOUS: 1 — {13}.
- ENGINE_UNSUPPORTED: 6 — {16, 17, 18, 19, 20, 26}.
- SOURCE_CONFLICT: 0.
- Structured rule objects: 27.
- Distinct executable requirement codes: 24.

## UNMAPPED_REQUIREMENTS

- REQ.2, REQ.3, REQ.4 — EXTERNAL.
- REQ.13 — AMBIGUOUS.
- REQ.16, REQ.17, REQ.18, REQ.19, REQ.20, REQ.26 — ENGINE_UNSUPPORTED.
- REQ.4 has no executable structured mapping.

## NORMATIVE_BASIS

CONFIRMED — direct MSG.044 requirements are from `ОП_22.pdf`, P.SP.02.MSG.044, Table 62, physical pages 770–772. Inherited structural requirements retain Table 44 provenance where applicable. Transaction context is P.SP.02.TRN.039 / P.SP.02.PRC.021, OPR096 → OPR097, ACT001 → ACT002, with MSG.044 as the initiating message and P.SP.02.MSG.002 as the response.

## MSG044_TESTS

Executed:

`PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests/test_msg044_*.py -p no:cacheprovider`

Result: **45 passed in 1.75s**.

Coverage includes mapping classifications, REQ.4 absence from executable rules, Table 62/Table 44 provenance, production body build and XML roundtrip, status value/attribute/date negatives, wrong-owner cases, duplicate application parents, REQ.27 same-parent semantics, signature rules, inherited requirements, and MSG.044 isolation.

## OPTIONAL_FULL_REGRESSION

NOT RUN. The requested scope only requires MSG.044 tests, and MSG.043 is under concurrent Gemini work. Running the full repository suite was intentionally avoided to prevent conflating unrelated concurrent failures with MSG.044 verification.

## CONCURRENT_CHANGES

MSG.043 is concurrent Gemini work and was not modified. No shared engine, shared normative data, or graphify output was changed for this task.

## GIT_DIFF_CHECK

`git diff --check` executed successfully with no whitespace errors.

Scoped status before this report showed only the allowed MSG.044 YAML and three MSG.044 test files as modified/untracked. This report is the only additional allowed file created by the task.

## REMAINING_ISSUES

None for the executable MSG.044 scope. Requirements classified EXTERNAL, AMBIGUOUS, or ENGINE_UNSUPPORTED remain intentionally unmapped as documented above.
