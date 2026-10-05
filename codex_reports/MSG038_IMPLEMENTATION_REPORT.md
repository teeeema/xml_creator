# MSG038 implementation report

## STATUS

COMPLETE

## VERDICT

READY

## CHANGED_FILES

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.038.yaml` — added the confirmed and safe-partial structured rules plus the complete Table 56 mapping audit.
- `P.SP.02_OP_22/tests/test_msg038_safe_mapping.py` — verifies the audit inventory, classification boundary, and exact rule targets.
- `P.SP.02_OP_22/tests/test_msg038_repeatable_xml.py` — verifies per-parent priority and document-child validation.
- `P.SP.02_OP_22/tests/test_msg038_end_to_end.py` — verifies MSG038 build, serialization, parsing, extraction, and validation with an MSG038-local fixture.
- `codex_reports/MSG038_IMPLEMENTATION_REPORT.md` — this report.

## IMPLEMENTATION

The message rule file now contains 30 structured-rule objects covering the 27 executable requirements: 26 `FULLY_MAPPABLE` requirements and safe-partial requirement 4. Rule 30 is scoped to each `ipcdo:TrademarkPriorityDetails` parent. Rule 32 is scoped by the exact `ipcdo:AccompanyingDocumentsDetails` QName and requires exactly `DocName`, `DocId`, `DocCreationDate`, `DescriptionText`, and `PageQuantity`; it does not require `DocBinaryText`. Requirements 33 and 34 implement the validity-period start/forbidden-end semantics, and requirements 35–37 implement the direct application signature rules.

## MAPPING_COUNTS

| Item | Count |
| --- | ---: |
| Captured Table 56 rows | 14 |
| Expanded requirements | 37 |
| FULLY_MAPPABLE | 26 |
| SAFE_PARTIAL | 1 |
| EXTERNAL | 3 |
| AMBIGUOUS | 1 |
| ENGINE_UNSUPPORTED | 6 |
| SOURCE_CONFLICT | 0 |
| Executable requirement codes | 27 |
| Structured-rule objects | 30 |

The classification arithmetic is exact: 26 + 1 + 3 + 1 + 6 + 0 = 37.

## UNMAPPED_REQUIREMENTS

`{2, 3, 13, 16, 17, 18, 19, 20, 26, 31}`

- EXTERNAL: 2, 3, 31
- AMBIGUOUS: 13
- ENGINE_UNSUPPORTED: 16, 17, 18, 19, 20, 26

No structured rule was added for these requirements.

## NORMATIVE_BASIS

CONFIRMED: `codex_reports/MSG038_PREP.md`, derived from P.SP.02 Table 56 and inherited Table 44. It confirms the message context `P.SP.02.MSG.038`, structure `R.IP.SP.02.002`, the expanded 37-requirement inventory, classifications, exact requirement 30 and 32 semantics, validity-period semantics, and signature scope.

## MSG038_TESTS

Executed:

```text
PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests/test_msg038_*.py -p no:cacheprovider
```

Result: `6 passed in 0.15s`.

The tests cover the audit arithmetic and unmapped boundary, safe requirement 4, repeated priority-parent failure behavior, exact QName document-child behavior, and the production build → serialize → parse → extract → validate path.

## OPTIONAL_FULL_REGRESSION

NOT RUN. The requested scoped MSG038 test command passed. A full regression run is intentionally omitted while concurrent MSG037 work is in progress.

## CONCURRENT_CHANGES

The repository contains concurrent changes outside this task. They were not edited, reset, staged, or otherwise modified. The MSG038 end-to-end fixture is self-contained and does not import another message's test fixture.

## GIT_DIFF_CHECK

Executed `git diff --check` for the allowed MSG038 paths and for the worktree. Both produced no output (clean).

## REMAINING_ISSUES

None within the approved MSG038 scope. The explicitly unmapped requirements remain declarative audit entries and are not treated as executable rules.
