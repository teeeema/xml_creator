# MSG043 Implementation Report

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.043.yaml` — added 7 executable structured rules for the 6 approved requirement codes, and complete `mapping_audit` (14 captured rows, 37 expanded requirements).
- `P.SP.02_OP_22/tests/test_msg043_safe_mapping.py` — audit verification, inventory assertions, exact approved requirement set, and exclusion of unmapped/positional rules.
- `P.SP.02_OP_22/tests/test_msg043_repeatable_xml.py` — unit tests for the 7 structured rules and repeatable XML behaviors (cardinality 2..2, resource dates, signature branches, officer requirements, and absence of positional status assignment).
- `P.SP.02_OP_22/tests/test_msg043_end_to_end.py` — end-to-end roundtrip (build -> serialize -> parse -> extract -> validate), negative proofs, and message isolation.
- `codex_reports/MSG043_IMPLEMENTATION_REPORT.md` — this authoritative implementation report.

## IMPLEMENTATION
`P.SP.02.MSG.043` («сведения о выделении заявки на ТЗ Союза из ранее поданной заявки на ТЗ Союза») was implemented strictly following `codex_reports/MSG043_PREP.md`.

Exactly 6 requirements (7 structured-rule objects) have been implemented:
1. `P.SP.02.MSG.043.T61.REQ.1`: `selection_cardinality` on `ipcdo:TrademarkApplicationDetails`, `min_occurs: 2, max_occurs: 2`.
2. `P.SP.02.MSG.043.T61.REQ.33`: `for_each` presence REQUIRED on `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime`.
3. `P.SP.02.MSG.043.T61.REQ.34`: `for_each` presence FORBIDDEN on `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime`.
4. `P.SP.02.MSG.043.T61.REQ.35.PRESENCE`: `selection_cardinality` on `ipcdo:TrademarkApplicationDetails/ipcdo:SignatureDetails`, `min_occurs: 1`.
5. `P.SP.02.MSG.043.T61.REQ.35.BRANCH`: `for_each` conditional_presence under `ipcdo:TrademarkApplicationDetails/ipcdo:SignatureDetails` (if `ipcdo:OfficerDetails != null` then `ccdo:FullNameDetails` FORBIDDEN).
6. `P.SP.02.MSG.043.T61.REQ.36`: `for_each` conditional_presence under `ipcdo:TrademarkApplicationDetails/ipcdo:SignatureDetails` (if `ccdo:FullNameDetails != null` then `ipcdo:OfficerDetails` FORBIDDEN).
7. `P.SP.02.MSG.043.T61.REQ.37`: `for_each` presence on `ipcdo:OfficerDetails` under signature requiring `csdo:LastName`, `csdo:FirstName`, `csdo:PositionName` and forbidding `ccdo:CommunicationDetails`.

All remaining requirements (REQ 2–32) are strictly unmapped.

## MAPPING_COUNTS
- `captured_row_count`: 14
- `expanded_requirement_count`: 37
- `FULLY_MAPPABLE`: 6 (`[1, 33, 34, 35, 36, 37]`)
- `SAFE_PARTIAL`: 0 (`[]`)
- `EXTERNAL`: 5 (`[2, 3, 4, 5, 31]`)
- `AMBIGUOUS`: 0 (`[]`)
- `ENGINE_UNSUPPORTED`: 26 (`[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32]`)
- `SOURCE_CONFLICT`: 0 (`[]`)
- Arithmetic check: `6 + 0 + 5 + 0 + 26 + 0 = 37`.

## UNMAPPED_REQUIREMENTS
The 31 unmapped requirements (`2..32`) cannot be safely mapped with the existing engine:
- **REQ 2–5 (EXTERNAL):** Rely on document-kind classifier resolution and prior/allocated role assignment.
- **REQ 6–29 (ENGINE_UNSUPPORTED):** Table 44 semantics apply exclusively to the *allocated application* instance (выделенная заявка). In `R.IP.SP.02.002`, both applications are identical repeatable `ipcdo:TrademarkApplicationDetails` siblings without any machine-readable discriminator (QName, attribute, or element). Assigning rules to both instances would alter normative semantics; binding by index (`[0]`, `[1]`) is strictly forbidden.
- **REQ 30 (ENGINE_UNSUPPORTED):** Requires that `SourceTrademarkApplicationId` of the allocated application match `TrademarkApplicationId` of the prior application. Cross-instance equality and role selection are engine-unsupported.
- **REQ 31 (EXTERNAL):** Resource existence and absence checks against external patent office resources require role binding.
- **REQ 32 (ENGINE_UNSUPPORTED):** Specifies status code `02` (no `codeListId`) for prior application vs `01` for allocated application. Without an instance discriminator, this cannot be bound.

## ROLE_BINDING_SAFETY
No positional heuristics or ordinal assumptions (`[0]`, `[1]`, "first application", "second application") were implemented or tested. The rule engine preserves XML semantics without inventing machine discriminators.

## NORMATIVE_BASIS
CONFIRMED:
- ОП_22.pdf, Table 61 (pp. 767–770), requirements 1–37.
- ОП_22.pdf, Table 44 (pp. 715–721), requirements 6–29 (inherited dual-provenance for allocated application).

## MSG043_TESTS
Execution command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg043_*.py -p no:cacheprovider
```
Result:
```text
....................
20 passed in 1.62s
```
Breakdown:
- `test_msg043_safe_mapping.py`: 7 passed
- `test_msg043_repeatable_xml.py`: 5 passed
- `test_msg043_end_to_end.py`: 8 passed

## OPTIONAL_FULL_REGRESSION
All 20 targeted tests for MSG043 passed.

## CONCURRENT_CHANGES
Isolated strictly to MSG043 files. No modifications made to MSG001–042, MSG044+, or shared library code (`eaeu_xml`).

## GIT_DIFF_CHECK
Execution command:
```bash
git diff --check
```
Result: Clean exit code 0, no trailing whitespace or merge conflict markers.

## REMAINING_ISSUES
None
