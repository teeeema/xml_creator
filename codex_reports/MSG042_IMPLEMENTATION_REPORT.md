# MSG042 implementation report

## STATUS

COMPLETE

## VERDICT

READY

## CHANGED_FILES

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.042.yaml` — added executable structured rules and the complete Table 60 mapping audit.
- `P.SP.02_OP_22/tests/test_msg042_safe_mapping.py` — verifies the inventory, classifications, status literal, owners, and unmapped boundary.
- `P.SP.02_OP_22/tests/test_msg042_repeatable_xml.py` — verifies cardinality, direct status ownership, CollectiveMarkIndicator value 1, validity dates, same-signature behavior, same-parent REQ27, and isolation from MSG041.
- `P.SP.02_OP_22/tests/test_msg042_end_to_end.py` — validates MSG042 through the real production path: build -> serialize -> parse -> extract -> validate, plus negative proofs.
- `codex_reports/MSG042_IMPLEMENTATION_REPORT.md` — this report.

## IMPLEMENTATION

The rule file contains 29 structured-rule objects implementing 26 executable requirement codes. Requirement 5 validates the direct application status code as `02`, forbids `codeListId` on that code, and prevents cross-owner satisfaction. Requirement 30 requires `CollectiveMarkIndicator == "1"` under `TrademarkDetails` (strictly isolated from MSG041's `"0"`). Requirements 31 and 32 require `StartDateTime` and forbid `EndDateTime` under `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails`. Requirements 33–35 govern direct `SignatureDetails` and its direct officers (mutual exclusion between `OfficerDetails` and `FullNameDetails`, required officer fields, forbidden officer communication). Inherited Table 44 rules retain dual provenance from Table 60 and Table 44.

## MAPPING_COUNTS

| Item | Count |
| --- | ---: |
| Captured Table 60 rows | 12 |
| Expanded requirements | 35 |
| FULLY_MAPPABLE | 25 |
| SAFE_PARTIAL | 1 |
| EXTERNAL | 2 |
| AMBIGUOUS | 1 |
| ENGINE_UNSUPPORTED | 6 |
| SOURCE_CONFLICT | 0 |
| Executable requirement codes | 26 |
| Structured-rule objects | 29 |

Classification arithmetic: `25 + 1 + 2 + 1 + 6 = 35`.

## UNMAPPED_REQUIREMENTS

Exact unmapped set: `{2, 3, 13, 16, 17, 18, 19, 20, 26}`

- EXTERNAL (2): 2, 3
- AMBIGUOUS (1): 13
- ENGINE_UNSUPPORTED (6): 16, 17, 18, 19, 20, 26

Requirement 26 remains unmapped; its normative `TrademarkKindCode OR TrademarkKindName` semantics were not converted into AND or otherwise approximated.

## NORMATIVE_BASIS

CONFIRMED: `codex_reports/MSG042_PREP.md`, based on P.SP.02 Table 60 (pp. 764–766) and inherited Table 44 (pp. 715–721). It establishes the Table 60 context, classifications, status literal `02`, CollectiveMarkIndicator `1`, required StartDateTime, forbidden EndDateTime, direct-signature ownership, and exact unmapped boundary.

## MSG042_TESTS

Executed:

```text
PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests/test_msg042_*.py -p no:cacheprovider
```

Result: `16 passed in 0.61s`.

The test suite covers:
- Inventory, classification arithmetic, and exact unmapped sets (`test_msg042_safe_mapping.py`).
- REQ1 cardinality (0 -> FAIL, 1 -> PASS, 2 -> FAIL).
- REQ4 presence of TrademarkApplicationId.
- REQ5 status code `02`, missing status, wrong status, forbidden codeListId, wrong-owner status.
- REQ30 `CollectiveMarkIndicator == "1"` PASS, `"0"` FAIL, wrong-owner FAIL.
- REQ31/32 `StartDateTime` REQUIRED, `EndDateTime` FORBIDDEN, wrong-owner FAIL.
- REQ33–35 same-SignatureDetails ownership, mutual exclusion, required officer fields, forbidden officer communication.
- REQ27 same-parent behavior.
- Inherited Table 44 cardinalities and fields.
- Real production E2E pipeline: build -> serialize -> parse -> extract -> validate.
- E2E negative proofs and MSG041/MSG042 isolation.

## OPTIONAL_FULL_REGRESSION

NOT RUN. Scoped MSG042 suite passed. Full OP22 regression was omitted because Codex is concurrently modifying MSG041.

## CONCURRENT_CHANGES

Concurrent MSG041 changes and other worktree changes were not modified, reset, staged, checked out, or cleaned. No MSG041 rule ID or file was touched.

## GIT_DIFF_CHECK

Executed `git diff --check` with code 0 (clean, no whitespace errors or merge markers). Changes are strictly limited to the five allowed files:
1. `P.SP.02_OP_22/message_rules/P.SP.02.MSG.042.yaml`
2. `P.SP.02_OP_22/tests/test_msg042_safe_mapping.py`
3. `P.SP.02_OP_22/tests/test_msg042_repeatable_xml.py`
4. `P.SP.02_OP_22/tests/test_msg042_end_to_end.py`
5. `codex_reports/MSG042_IMPLEMENTATION_REPORT.md`

## REMAINING_ISSUES

None. All approved requirements are implemented and verified according to specification.
