# MSG040 implementation report

## STATUS

COMPLETE

## VERDICT

READY

## CHANGED_FILES

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.040.yaml` — added executable structured rules and the complete Table 58 mapping audit.
- `P.SP.02_OP_22/tests/test_msg040_safe_mapping.py` — verifies the inventory, classifications, status literal, owners, and unmapped boundary.
- `P.SP.02_OP_22/tests/test_msg040_repeatable_xml.py` — verifies cardinality, direct status ownership, same-signature behavior, same-parent REQ27, and both validity dates.
- `P.SP.02_OP_22/tests/test_msg040_end_to_end.py` — validates MSG040 through build, serialization, parsing, extraction, and validation.
- `codex_reports/MSG040_IMPLEMENTATION_REPORT.md` — this report.

## IMPLEMENTATION

The rule file contains 28 structured-rule objects for 25 executable requirement codes. Requirement 5 validates the direct application status code as `30`, forbids `codeListId` on that code, and cannot be satisfied by another owner. Requirements 30–32 are scoped to direct `SignatureDetails` and its direct officers. Requirements 33 and 34 require both dates under the same resource-status owner. The inherited Table 44 rules retain Table 58 and Table 44 provenance.

## MAPPING_COUNTS

| Item | Count |
| --- | ---: |
| Captured Table 58 rows | 11 |
| Expanded requirements | 34 |
| FULLY_MAPPABLE | 24 |
| SAFE_PARTIAL | 1 |
| EXTERNAL | 2 |
| AMBIGUOUS | 1 |
| ENGINE_UNSUPPORTED | 6 |
| SOURCE_CONFLICT | 0 |
| Executable requirement codes | 25 |
| Structured-rule objects | 28 |

Classification arithmetic: `24 + 1 + 2 + 1 + 6 = 34`.

## UNMAPPED_REQUIREMENTS

`{2, 3, 13, 16, 17, 18, 19, 20, 26}`

- EXTERNAL: 2, 3
- AMBIGUOUS: 13
- ENGINE_UNSUPPORTED: 16, 17, 18, 19, 20, 26

Requirement 26 remains unmapped; its normative `TrademarkKindCode OR TrademarkKindName` semantics were not approximated.

## NORMATIVE_BASIS

CONFIRMED: `codex_reports/MSG040_PREP.md`, based on P.SP.02 Table 58 and inherited Table 44. It establishes the Table 58 context, classifications, status literal `30`, direct-signature ownership, and required StartDateTime and EndDateTime semantics.

## MSG040_TESTS

Executed:

```text
PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests/test_msg040_*.py -p no:cacheprovider
```

Result: `9 passed in 0.36s`.

The suite covers the audit arithmetic, external/ambiguous/unsupported boundary, REQ1 0/1/2 cardinality, missing and invalid direct status behavior, forbidden status classifier attribute, same-signature mutual exclusion, required officer fields, forbidden officer communication, same-parent REQ27 behavior, correct-owner date requirements, and the production E2E path.

## OPTIONAL_FULL_REGRESSION

NOT RUN. The requested scoped MSG040 suite passed. Full OP22 regression is omitted while concurrent MSG039 work is in progress.

## CONCURRENT_CHANGES

Concurrent MSG039 and other worktree changes were not modified, reset, staged, or otherwise altered. No MSG039 file or test was read as an implementation dependency.

## GIT_DIFF_CHECK

`git diff --check` is clean for the MSG040 scope and for the worktree at the time of verification.

## REMAINING_ISSUES

None within the approved MSG040 scope. The nine intentionally unmapped requirements remain audit-only entries.
