# MSG037 IMPLEMENTATION REPORT

## STATUS

COMPLETE

## VERDICT

READY

## CHANGED_FILES

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.037.yaml` — added executable structured rules and complete mapping audit for P.SP.02.MSG.037 only.
- `P.SP.02_OP_22/tests/test_msg037_safe_mapping.py` — validates inventory, classification, executable/unmapped sets, provenance, rule shape, and message identity.
- `P.SP.02_OP_22/tests/test_msg037_repeatable_xml.py` — validates repeatable/sparse owner alignment, same-parent REQ27 semantics, REQ5 ownership/namespace behavior, and related repeated structures.
- `P.SP.02_OP_22/tests/test_msg037_end_to_end.py` — validates production generation/evaluation path, mapped-rule negatives, transaction metadata, and message isolation.
- `codex_reports/MSG037_IMPLEMENTATION_REPORT.md` — this implementation report.

## IMPLEMENTATION

Implemented P.SP.02.MSG.037 from the approved `codex_reports/MSG037_PREP.md` scope without changing shared Python, StructureDefinitions, classifiers, source refs, process metadata, or other messages.

Key behavior implemented:

- REQ1 exact `TrademarkApplicationDetails` cardinality `1..1`.
- REQ4 safe partial mapping: local `TrademarkApplicationId` presence only.
- REQ5 exactly one `IPEntityStatusDetails`, `StatusCode = "31"`, and `StatusCode/@codeListId` forbidden.
- Executable inherited Table 44 requirements for REQ6-12, REQ14-15, REQ21-25, REQ27-29 with dual provenance retained.
- REQ27 preserves same-parent correlation semantics.
- REQ30 requires `ValidityPeriodDetails/csdo:StartDateTime` per existing `ResourceItemStatusDetails`.
- REQ31 requires `ValidityPeriodDetails/csdo:EndDateTime` per existing `ResourceItemStatusDetails`.
- No executable rules were added for requirements classified as EXTERNAL, AMBIGUOUS, or ENGINE_UNSUPPORTED.

The initial end-to-end baseline exposed one test-data issue: `TMDescriptionDetails` was represented as `[None]`, which the evaluator correctly treated as absent for REQ25. The test fixture was corrected to use the established present-container representation `[""]`; no normative rule change was needed.

## MAPPING_COUNTS

- Captured source rows: 8
- Expanded requirements: 31
- Structured rules: 25
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

- REQ2, REQ3 — EXTERNAL classifier-dependent semantics.
- REQ13 — AMBIGUOUS owner/instance scope.
- REQ16-20 — ENGINE_UNSUPPORTED exact ordinal/language/repeated-instance correlation semantics.
- REQ26 — ENGINE_UNSUPPORTED same-parent disjunctive `TrademarkKindCode OR TrademarkKindName` semantics.

REQ4 remains PARTIAL_EXECUTABLE only for the independently safe local `TrademarkApplicationId` presence fragment; its external-resource remainder remains explicitly unmapped.

## NORMATIVE_BASIS

CONFIRMED — implementation follows `codex_reports/MSG037_PREP.md`, using direct Table 55 references for MSG037 and inherited Table 44 references where the preparation audit classified the requirement as safely executable. No normative source references were fabricated or altered.

Message/process identity retained:

- Message: `P.SP.02.MSG.037`
- Structure: `R.IP.SP.02.002` v1.0.0
- Transaction: `P.SP.02.TRN.032`
- Procedure: `P.SP.02.PRC.013`
- Operation transition: `P.SP.02.OPR.050 -> P.SP.02.OPR.051`
- Participant transition: `P.SP.02.ACT.001 -> P.SP.02.ACT.002`
- Response: `P.SP.02.MSG.002`

## MSG037_TESTS

Command executed:

`PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests/test_msg037_*.py -p no:cacheprovider`

Result:

`58 passed in 1.70s`

Additional focused end-to-end diagnostic/fix verification executed before the required wildcard run:

`PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests/test_msg037_end_to_end.py -x -vv -p no:cacheprovider`

Result:

`28 passed in 1.13s`

## PSP02_TESTS

Command executed:

`PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests -p no:cacheprovider`

Result:

`1571 passed in 51.89s`

Baseline before MSG037 was 1507 passed; the package suite now includes the new MSG037 coverage.

## GIT_DIFF_CHECK

Command executed:

`git diff --check`

Result:

PASS — no output, exit code 0.

Final diff review was limited to the allowed MSG037 files. No MSG035/MSG036 or shared implementation files were modified by this task.

## REMAINING_ISSUES

None within the approved MSG037 implementation scope. The intentionally unmapped requirements remain documented in `mapping_audit` and are not treated as implemented.
