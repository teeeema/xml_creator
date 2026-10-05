# MSG039 IMPLEMENTATION REPORT

## STATUS

COMPLETE

## VERDICT

READY

## CHANGED_FILES

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.039.yaml` — added executable structured rules and complete mapping audit for P.SP.02.MSG.039 only.
- `P.SP.02_OP_22/tests/test_msg039_safe_mapping.py` — validates inventory, classification, executable/unmapped sets, provenance, rule shape, and message identity.
- `P.SP.02_OP_22/tests/test_msg039_repeatable_xml.py` — validates repeatable/sparse owner alignment, REQ27 same-parent semantics, REQ5 owner/QName behavior, and wrong-owner StartDateTime/EndDateTime behavior.
- `P.SP.02_OP_22/tests/test_msg039_end_to_end.py` — validates production build → serialize → parse → extract → validate behavior, mapped-rule negatives, transaction metadata, and message isolation.
- `codex_reports/MSG039_IMPLEMENTATION_REPORT.md` — this report.

## IMPLEMENTATION

Implemented P.SP.02.MSG.039 from the approved `codex_reports/MSG039_PREP.md` scope without changing shared Python, StructureDefinitions, classifiers, source refs, process metadata, other messages, or MSG040 files.

Implemented behavior:

- REQ1 exact `TrademarkApplicationDetails` cardinality `1..1`.
- REQ4 safe partial mapping: local `TrademarkApplicationId` presence only.
- REQ5 exactly one direct `IPEntityStatusDetails`; `StatusCode == "21"`; `StatusCode/@codeListId` forbidden; wrong-owner and wrong-namespace values cannot satisfy the rule.
- Executable inherited Table 44 requirements for REQ6-12, REQ14-15, REQ21-25, REQ27-29 with dual Table 57 + Table 44 provenance.
- REQ27 preserves same-`TrademarkDetails` parent correlation and rejects cross-parent satisfaction.
- REQ30 requires `ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime`.
- REQ31 requires the matching `ResourceItemStatusDetails/ValidityPeriodDetails/EndDateTime`.
- Wrong-owner StartDateTime and EndDateTime do not satisfy REQ30/REQ31.
- No executable rules were created for REQ2-3, REQ13, REQ16-20, or REQ26.
- MSG039 validation uses only MSG039 rule IDs and remains isolated from other messages using `R.IP.SP.02.002`.

## MAPPING_COUNTS

- Captured source rows: 8
- Expanded requirements: 31
- Structured-rule objects: 25
- Executable requirement codes: 22
- FULLY_MAPPABLE: 21
- SAFE_PARTIAL: 1
- EXTERNAL: 2
- AMBIGUOUS: 1
- ENGINE_UNSUPPORTED: 6
- SOURCE_CONFLICT: 0

Executable requirement codes:
`1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31`

## UNMAPPED_REQUIREMENTS

Exact unmapped set:
`2, 3, 13, 16, 17, 18, 19, 20, 26`

- REQ2-3 — EXTERNAL classifier-dependent semantics.
- REQ13 — AMBIGUOUS owner/instance invariant.
- REQ16-20 — ENGINE_UNSUPPORTED exact ordinal/language/repeated-instance correlation semantics.
- REQ26 — ENGINE_UNSUPPORTED exact same-parent `TrademarkKindCode OR TrademarkKindName` semantics; no AND approximation was introduced.

REQ4 is PARTIAL_EXECUTABLE only for the independently safe local `TrademarkApplicationId` presence fragment; the external resource/status/equality remainder remains unmapped.

## NORMATIVE_BASIS

CONFIRMED — implementation follows `codex_reports/MSG039_PREP.md`, which is the implementation authority for this task.

Retained identity:

- Message: `P.SP.02.MSG.039`
- Structure: `R.IP.SP.02.002` v1.0.0
- Transaction: `P.SP.02.TRN.034`
- Procedure: `P.SP.02.PRC.015`
- Operation transition: `P.SP.02.OPR.061 -> P.SP.02.OPR.062`
- Participant transition: `P.SP.02.ACT.001 -> P.SP.02.ACT.002`
- Response: `P.SP.02.MSG.002`
- Direct source: Table 57, pp. 757-759
- Inherited source: matching Table 44 requirements

No normative audit was repeated and no source reference was fabricated.

## MSG039_TESTS

Required command executed:

`PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests/test_msg039_*.py -p no:cacheprovider`

Final result:

`60 passed in 1.98s`

An earlier adaptation run produced `57 passed, 1 failed` because one copied test still expected Table 55/page 753 provenance. The test expectation was corrected to Table 57/page 758; production behavior was not changed for that failure.

## OPTIONAL_FULL_REGRESSION

NOT RUN.

The task explicitly makes full OP22 regression optional because MSG040 is being modified concurrently. The required MSG039-only suite passed completely.

## CONCURRENT_CHANGES

The repository already contained many unrelated modified/untracked files before this task, including concurrent work outside MSG039. They were treated as foreign changes and left untouched.

No MSG040 file or MSG040 test was modified.

## GIT_DIFF_CHECK

Commands executed:

`git diff --check`

`git diff --check -- P.SP.02_OP_22/message_rules/P.SP.02.MSG.039.yaml P.SP.02_OP_22/tests/test_msg039_safe_mapping.py P.SP.02_OP_22/tests/test_msg039_repeatable_xml.py P.SP.02_OP_22/tests/test_msg039_end_to_end.py`

Result:

PASS — both commands produced no output and exited successfully.

## REMAINING_ISSUES

None within the approved MSG039 implementation scope.

The intentionally unmapped requirements remain documented in `mapping_audit` and are not treated as implemented.
