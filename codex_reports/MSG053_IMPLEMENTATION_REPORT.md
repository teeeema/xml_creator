# P.SP.02.MSG.053 Implementation Report

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.053.yaml` (executable rules and mapping audit for MSG.053)
- `P.SP.02_OP_22/tests/test_msg053_safe_mapping.py` (safe mapping and rule structure tests)
- `P.SP.02_OP_22/tests/test_msg053_repeatable_xml.py` (repeatable parent and positional XML tests)
- `P.SP.02_OP_22/tests/test_msg053_end_to_end.py` (roundtrip build-serialize-parse-extract-validate, negative proofs, and message isolation tests)
- `codex_reports/MSG053_IMPLEMENTATION_REPORT.md` (this report)

## IMPLEMENTATION
`P.SP.02.MSG.053` («Заявление о продлении срока действия исключительного права на товарный знак, знак обслуживания Евразийского экономического союза») operates over the unified trademark register record container `ipcdo:UnifiedRegisterRecordsDetails` under the root message structure `R.IP.SP.02.007 v1.0.0` (`urn:eeu:information:customs:trademark_register_message:1.0.0`).

All 24 structured rule objects and complete `mapping_audit` were authored in strict adherence to the authoritative handoff based on Table 71 of ОП_22.pdf (pp. 798–801) and inherited requirements from Table 49 (pp. 737–740).

Specific rule implementations:
1. **REQ 1 (SAFE_PARTIAL):** Requires `TrademarkId` locally within the governed register record; external active status check deferred to external unmapped remainder.
2. **REQ 2 (FULL):** Governed record `ipcdo:UnifiedRegisterRecordsDetails` cardinality constrained to exactly `1..1`.
3. **REQ 3 (FULL):** Forbids `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime` under the governed record.
4. **REQ 4 (SAFE_PARTIAL):** IF direct `ipsdo:IPDocKindCode != null` THEN direct `ipsdo:IPDocKindName` is forbidden.
5. **REQ 5 (SAFE_PARTIAL):** IF direct `ipsdo:IPDocKindCode == null` THEN direct `ipsdo:IPDocKindName` is required and must match exact normative literal:
   `"Заявление о продлении срока действия исключительного права на товарный знак, знак обслуживания Евразийского экономического союза"`.
6. **REQ 6–17 (FULL):** Inherited Table 49 rules covering `DocKindCode`, `DocId`, `DocCreationDate`, `ContractDetails`, `RegistrationNumberId`, `ApplicationRegistrationKeyId`, `ApplicationDetails`, `RegistrationDetails`, `InternationalRegistrationDetails`, `RightHolderDetails`, `RepresentativeDetails`, and `PaymentDocDetails`.
7. **REQ 20 (FULL):** In `ipcdo:IPEntityStatusDetails`: `csdo:EventDate` is required, `csdo:StatusCode` must equal `"03"`, and attribute `@codeListId` is forbidden.
8. **REQ 24 (FULL):** In `ipcdo:SignatureDetails`: `min_occurs: 1`; if `ipcdo:OfficerDetails` is present, sibling `ccdo:FullNameDetails` is forbidden.
9. **REQ 25 (FULL):** In `ipcdo:SignatureDetails`: if direct `ccdo:FullNameDetails` is present, direct `ipcdo:OfficerDetails` is forbidden.
10. **REQ 26 (FULL):** Under `ipcdo:OfficerDetails` directly within signature: `LastName`, `FirstName`, `PositionName` are required; `CommunicationDetails` is forbidden. Correctly scoped with `qname: "ipcdo:OfficerDetails"` and `under: f"{R007}/ipcdo:SignatureDetails"` to preserve multiple signatures without false failures when another signature uses `FullNameDetails`.

## MAPPING_COUNTS
- `captured_row_count`: 14
- `expanded_requirement_count`: 26
- `FULLY_MAPPABLE`: 18 (`{2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 24, 25, 26}`)
- `SAFE_PARTIAL`: 3 (`{1, 4, 5}`)
- `ENGINE_UNSUPPORTED`: 5 (`{18, 19, 21, 22, 23}`)
- `EXTERNAL`: 0
- `AMBIGUOUS`: 0
- `SOURCE_CONFLICT`: 0
- **Total requirements**: 26 (`18 + 3 + 5 = 26`)
- **Executable requirement codes**: 21
- **Structured rule objects**: 24 (REQ 15 has 2 objects, REQ 16 has 2 objects, REQ 24 has 2 objects)
- **Unmapped requirement codes**: 5

## PARTIAL_REMAINDERS
- **REQ 1:**
  - *Safe fragment:* `ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId` is required in the message record.
  - *Unmapped remainder:* External registry lookup confirming trademark registration is active in the national patent office registry.
- **REQ 4:**
  - *Safe fragment:* IF `ipsdo:IPDocKindCode != null` THEN `ipsdo:IPDocKindName` is forbidden.
  - *Unmapped remainder:* External national/union document classifier validation for `IPDocKindCode`.
- **REQ 5:**
  - *Safe fragment:* IF `ipsdo:IPDocKindCode == null` THEN `ipsdo:IPDocKindName` is required and must match exact normative string literal.
  - *Unmapped remainder:* None; classified SAFE_PARTIAL because it forms a paired conditional branch with REQ 4.

## UNMAPPED_REQUIREMENTS
- **REQ 18 (ENGINE_UNSUPPORTED):**
  - *Reason:* Cross-collection conditional check requiring `csdo:CollectiveMarkIndicator` to govern whether multiple `RightHolderDetails` are allowed or forbidden.
  - *Unmapped remainder:* Cross-collection dependency between `CollectiveMarkIndicator` and multiple `RightHolderDetails`.
- **REQ 19 (ENGINE_UNSUPPORTED):**
  - *Reason:* Conditional requirement requiring `ipcdo:CollectiveMarkRegulationsDetails` when `csdo:CollectiveMarkIndicator == true`.
  - *Unmapped remainder:* Conditional requirement of `CollectiveMarkRegulationsDetails` based on `CollectiveMarkIndicator`.
- **REQ 21 (ENGINE_UNSUPPORTED):**
  - *Reason:* External patent office register check requiring the register to contain exactly one fewer `csdo:DocValidityDate` entries than in the message.
  - *Unmapped remainder:* External registry matching and `DocValidityDate` set cardinality comparison.
- **REQ 22 (ENGINE_UNSUPPORTED):**
  - *Reason:* External patent office register check requiring all `csdo:DocValidityDate` entries in the register to match values in the message except for one new entry.
  - *Unmapped remainder:* External registry `DocValidityDate` set intersection comparison.
- **REQ 23 (ENGINE_UNSUPPORTED):**
  - *Reason:* External patent office register check requiring the new non-matching `csdo:DocValidityDate` in the message to be strictly greater than all other `DocValidityDate` instances.
  - *Unmapped remainder:* External registry comparative date ordering for the new validity date.

## OWNER_QNAME_SAFETY
All rules use full, exact QNames:
- Root namespace: `urn:eeu:information:customs:trademark_register_message:1.0.0`
- Prefixes: `ipcdo:`, `ipsdo:`, `ccdo:`, `csdo:`
- Governed record owner: `ipcdo:UnifiedRegisterRecordsDetails`
- Signatures owner: `ipcdo:SignatureDetails`
- Officer details scoped explicitly under signature details to prevent leakage to/from other entity officers.

## REPEATABLE_RECORD_SAFETY
- Tests verify single record, multiple records, and heterogeneous records.
- Per-parent positional indexing is strictly tested and maintained.
- Sibling exclusivity between `FullNameDetails` and `OfficerDetails` is enforced per signature instance without cross-signature pollution.

## MESSAGE_ISOLATION
- Roundtrip tests verify that valid MSG053 documents pass validation against MSG053 rules.
- Isolation tests verify that MSG053 documents are rejected or cleanly segregated by sibling message rules (MSG001, MSG051, MSG052) without collision.

## NORMATIVE_BASIS
CONFIRMED — ОП_22.pdf Table 71 (pp. 798–801) and Table 49 items 6–17 (pp. 737–740).

## MSG053_TESTS
Executed command:
`PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg053_*.py -p no:cacheprovider`

Results:
- `test_msg053_safe_mapping.py`: 9 passed
- `test_msg053_repeatable_xml.py`: 10 passed
- `test_msg053_end_to_end.py`: 7 passed
- **Total: 26 passed in 3.25s**

## OPTIONAL_FULL_REGRESSION
Targeted test suite for MSG053 executed and passed completely (26 passed). Full regression suite across all messages was not run to maintain test execution efficiency and strict scope isolation.

## CONCURRENT_CHANGES
Strict scope boundaries were maintained:
- No concurrent files or work by other agents (such as MSG052) were modified or deleted.
- Only the 5 authorized files for MSG053 were modified/created.

## GIT_DIFF_CHECK
Executed command:
`git diff --check`
Result: Clean (exit code 0, no trailing whitespace or format issues).

## REMAINING_ISSUES
None
