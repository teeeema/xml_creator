# MSG051 Implementation Report

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.051.yaml` — updated structured rules (24 rule objects for 21 executable requirements) and complete `mapping_audit` (10 captured rows, 23 expanded requirements).
- `P.SP.02_OP_22/tests/test_msg051_safe_mapping.py` — audit verification, inventory assertions, approved executable requirement set, unmapped requirement verification, and inherited dual-provenance checks.
- `P.SP.02_OP_22/tests/test_msg051_repeatable_xml.py` — unit tests for the structured rules and repeatable XML behaviors (cardinality 1..1, StartDateTime REQUIRED, fallback document kind literals, RegistrationCancellationDetails, Table 49 inherited rules, and signature mutual exclusion).
- `P.SP.02_OP_22/tests/test_msg051_end_to_end.py` — end-to-end roundtrip (build -> serialize -> parse -> extract -> validate), negative proofs, and critical message isolation.
- `codex_reports/MSG051_IMPLEMENTATION_REPORT.md` — this authoritative implementation report.

## IMPLEMENTATION
`P.SP.02.MSG.051` («Сведения о признании недействительным предоставления правовой охраны товарному знаку Союза или о прекращении правовой охраны товарного знака Союза») was implemented based on `R.IP.SP.02.007 v1.0.0` («сведения о ТЗ Союза из Единого реестра ТЗ Союза»).

Exactly 21 requirement codes (24 structured-rule objects) have been implemented:
1. `P.SP.02.MSG.051.T69.REQ.1` (SAFE_PARTIAL): `ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId` is REQUIRED locally.
2. `P.SP.02.MSG.051.T69.REQ.2` (FULLY_MAPPABLE): `selection_cardinality` on `ipcdo:UnifiedRegisterRecordsDetails`, `min_occurs: 1, max_occurs: 1`.
3. `P.SP.02.MSG.051.T69.REQ.3` (SAFE_PARTIAL): If `ipsdo:IPDocKindCode != null` then `ipsdo:IPDocKindName` FORBIDDEN.
4. `P.SP.02.MSG.051.T69.REQ.4` (SAFE_PARTIAL): If `ipsdo:IPDocKindCode == null` then `ipsdo:IPDocKindName` is REQUIRED and MUST equal one of two normative literals:
   - `"Решение о признании предоставления правовой охраны товарному знаку, знаку обслуживания Евразийского экономического союза недействительным"`
   - `"Решение о прекращении правовой охраны товарного знака, знака обслуживания Евразийского экономического союза"`
5. `P.SP.02.MSG.051.T69.REQ.5` (FULLY_MAPPABLE): Under governed record `ipcdo:UnifiedRegisterRecordsDetails`:
   - `ipcdo:RegistrationCancellationDetails` is REQUIRED;
   - `ipcdo:RegistrationCancellationDetails/ipsdo:CancellationTrademarkRegistrationReasonCode` is REQUIRED;
   - `ipcdo:RegistrationCancellationDetails/ipcdo:NationalPatentDecisionDetails` is REQUIRED.
6. `P.SP.02.MSG.051.T69.REQ.6` (FULLY_MAPPABLE): Inherited from Table 49: `csdo:UnifiedCountryCode/@codeListId` == `"ВОИС ST.3"`.
7. `P.SP.02.MSG.051.T69.REQ.7` (FULLY_MAPPABLE): Inherited from Table 49: `ccdo:SubjectAddressDetails` requires `AddressKindCode`, `UnifiedCountryCode`, `CityName`, `StreetName`, `BuildingNumberId`.
8. `P.SP.02.MSG.051.T69.REQ.8` (FULLY_MAPPABLE): Inherited from Table 49: `ccdo:CommunicationDetails` requires `CommunicationChannelCode` and `CommunicationChannelId`, forbids `CommunicationChannelName`.
9. `P.SP.02.MSG.051.T69.REQ.9` (FULLY_MAPPABLE): Inherited from Table 49: `CommunicationChannelCode` IN `{"TE", "EM", "FX"}`.
10. `P.SP.02.MSG.051.T69.REQ.10` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:PatentAuthorityDetails` requires `UnifiedCountryCode`, `AuthorityName`, `AuthorityBriefName`.
11. `P.SP.02.MSG.051.T69.REQ.11` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:IPPartyDetails` (RH) cardinality 1..1.
12. `P.SP.02.MSG.051.T69.REQ.12` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:IPPartyDetails` requires `UnifiedCountryCode`, `IPSubjectName`, `SubjectAddressDetails`, `CommunicationDetails`.
13. `P.SP.02.MSG.051.T69.REQ.13` (FULLY_MAPPABLE): Inherited from Table 49: `IPPartyDetails/SubjectAddressDetails/csdo:AddressKindCode` == `"2"`.
14. `P.SP.02.MSG.051.T69.REQ.14` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:TrademarkDetails` requires `TrademarkPicture`, `TMDescriptionDetails`, `TrademarkKindName`, `CollectiveMarkIndicator`.
15. `P.SP.02.MSG.051.T69.REQ.15` (FULLY_MAPPABLE): Inherited from Table 49: `TMDescriptionDetails` requires `DescriptionText` and `TMElementDetails`; `TMElementDetails` requires `TrademarkCFECode`, `DesignationName`, `TMLocalizedName`, `TMTransliterationName`.
16. `P.SP.02.MSG.051.T69.REQ.16` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:GoodsBaseDetails` cardinality 1..*, requires `GoodsClassCode`, `GoodsClassName`, `GoodsName`, `TrademarkDecisionIndicator`, `TrademarkApplicationId`.
17. `P.SP.02.MSG.051.T69.REQ.17` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:GoodsBaseDetails` forbids `TrademarkId`, `ApellationOfOriginEAEUId`, `TrademarkRegRefusalReasonText`.
18. `P.SP.02.MSG.051.T69.REQ.20.PRESENCE` & `BRANCH` (FULLY_MAPPABLE): `ipcdo:SignatureDetails` cardinality 1..*; if `OfficerDetails != null` then sibling `FullNameDetails` FORBIDDEN.
19. `P.SP.02.MSG.051.T69.REQ.21` (FULLY_MAPPABLE): In same `SignatureDetails`, if `FullNameDetails != null` then `OfficerDetails` FORBIDDEN.
20. `P.SP.02.MSG.051.T69.REQ.22` (FULLY_MAPPABLE): Under `OfficerDetails` directly in signature: `LastName`, `FirstName`, `PositionName` REQUIRED; `CommunicationDetails` FORBIDDEN.
21. `P.SP.02.MSG.051.T69.REQ.23` (FULLY_MAPPABLE): Under `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails`: `csdo:StartDateTime` is REQUIRED. No EndDateTime requirement or prohibition is fabricated.

Requirements 18 and 19 are strictly unmapped.

## MAPPING_COUNTS
- `captured_row_count`: 10
- `expanded_requirement_count`: 23
- `FULLY_MAPPABLE`: 18 (`[2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23]`)
- `SAFE_PARTIAL`: 3 (`[1, 3, 4]`)
- `EXTERNAL`: 0 (`[]`)
- `AMBIGUOUS`: 0 (`[]`)
- `ENGINE_UNSUPPORTED`: 2 (`[18, 19]`)
- `SOURCE_CONFLICT`: 0 (`[]`)
- Arithmetic check: `18 + 3 + 0 + 0 + 2 + 0 = 23`.
- Executable requirement codes: exactly 21 (`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23]`).
- Structured-rule object count: 24.

## PARTIAL_REMAINDERS
- **REQ 1 (SAFE_PARTIAL):** Active registration status and value matching in national patent office external resources remain external dependencies.
- **REQ 3, 4 (SAFE_PARTIAL):** Document kind classifier presence/absence lookups remain external dependencies.

## UNMAPPED_REQUIREMENTS
The 2 unmapped requirements remain strictly non-executable:
- **REQ 18 (ENGINE_UNSUPPORTED):** Conditional cross-collection dependency: if `CollectiveMarkIndicator == 1` then `IPPartyDetails` with kind `UE` required.
- **REQ 19 (ENGINE_UNSUPPORTED):** Conditional cross-collection dependency: if `CollectiveMarkIndicator == 1` then `AccompanyingDocumentsDetails` with charter document kind required.

## OWNER_QNAME_SAFETY
- **Structure root:** Message operates on `R.IP.SP.02.007` (`ipcdo:UnifiedRegisterRecordsDetails`).
- **Cancellation group:** `ipcdo:RegistrationCancellationDetails` is REQUIRED with child `ipsdo:CancellationTrademarkRegistrationReasonCode` and `ipcdo:NationalPatentDecisionDetails`.
- **Validity period:** `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime` is REQUIRED (no EndDateTime rule).
- **Document kind:** Strict pair of mutually exclusive rules (REQ 3 / REQ 4) with exact two normative fallback literals.
- **Signatures:** Direct `SignatureDetails/OfficerDetails` and sibling `FullNameDetails` enforce same-parent mutual exclusion and required officer name/position fields without leaking across parents.

## MESSAGE_ISOLATION
Explicit isolation confirmed across related messages on `R.IP.SP.02.007`:
- **MSG047:** `StatusCode` == `"03"`, `EndDateTime` FORBIDDEN.
- **MSG048:** `StatusCode` == `"03"`, `CollectiveMarkIndicator` == `"1"`, `EndDateTime` FORBIDDEN.
- **MSG049:** `StatusCode` == `"03"`, `StartDateTime` REQUIRED, `EndDateTime` FORBIDDEN.
- **MSG050:** `StatusCode` == `"05"`, `EndDateTime` REQUIRED.
- **MSG051:** `RegistrationCancellationDetails` REQUIRED, `CancellationTrademarkRegistrationReasonCode` REQUIRED, `NationalPatentDecisionDetails` REQUIRED, `StartDateTime` REQUIRED.
MSG051 validation uses only `P.SP.02.MSG.051.*` rules, with zero rule leakage or cross-contamination.

## NORMATIVE_BASIS
CONFIRMED:
- ОП_22.pdf, Table 69 (pp. 790–792), requirements 1–23.
- ОП_22.pdf, Table 49 (pp. 737–740), requirements 6–19 (inherited dual-provenance).

## MSG051_TESTS
Execution command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg051_*.py -p no:cacheprovider
```
Result:
```text
...........................                                              [100%]
27 passed in 2.07s
```
Breakdown:
- `test_msg051_safe_mapping.py`: 10 passed
- `test_msg051_repeatable_xml.py`: 10 passed
- `test_msg051_end_to_end.py`: 7 passed

## CONCURRENT_CHANGES
- Codex is concurrently working on MSG052 in `P.SP.02_OP_22/message_rules/P.SP.02.MSG.052.yaml`.
- All sibling files were left completely untouched (READ ONLY).
- Test execution was safely isolated from intermediate sibling syntax states.

## GIT_DIFF_CHECK
- Command: `git diff --check`
- Result: 0 errors (clean output).

## REMAINING_ISSUES
None
