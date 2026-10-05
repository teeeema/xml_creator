# MSG050 Implementation Report

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.050.yaml` — updated structured rules (24 rule objects for 21 executable requirements) and complete `mapping_audit` (10 captured rows, 23 expanded requirements).
- `P.SP.02_OP_22/tests/test_msg050_safe_mapping.py` — audit verification, inventory assertions, approved executable requirement set, unmapped requirement verification, and inherited dual-provenance checks.
- `P.SP.02_OP_22/tests/test_msg050_repeatable_xml.py` — unit tests for the structured rules and repeatable XML behaviors (cardinality 1..1, EndDateTime REQUIRED, fallback document kind literal, Table 49 inherited rules, StatusCode "05", and signature mutual exclusion).
- `P.SP.02_OP_22/tests/test_msg050_end_to_end.py` — end-to-end roundtrip (build -> serialize -> parse -> extract -> validate), negative proofs, and critical message isolation.
- `codex_reports/MSG050_IMPLEMENTATION_REPORT.md` — this authoritative implementation report.

## IMPLEMENTATION
`P.SP.02.MSG.050` («Сведения об отказе от исключительного права на товарный знак Союза») was implemented based on `R.IP.SP.02.007 v1.0.0` («сведения о ТЗ Союза из Единого реестра ТЗ Союза»).

Exactly 21 requirement codes (24 structured-rule objects) have been implemented:
1. `P.SP.02.MSG.050.T68.REQ.1` (SAFE_PARTIAL): `ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId` is REQUIRED locally.
2. `P.SP.02.MSG.050.T68.REQ.2` (FULLY_MAPPABLE): `selection_cardinality` on `ipcdo:UnifiedRegisterRecordsDetails`, `min_occurs: 1, max_occurs: 1`.
3. `P.SP.02.MSG.050.T68.REQ.3` (FULLY_MAPPABLE): Under `ipcdo:UnifiedRegisterRecordsDetails`, `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime` is REQUIRED. No StartDateTime requirement was invented.
4. `P.SP.02.MSG.050.T68.REQ.4` (SAFE_PARTIAL): If `ipsdo:IPDocKindCode != null` then `ipsdo:IPDocKindName` FORBIDDEN.
5. `P.SP.02.MSG.050.T68.REQ.5` (SAFE_PARTIAL): If `ipsdo:IPDocKindCode == null` then `ipsdo:IPDocKindName` equals `"Ходатайство об отказе от исключительного права на товарный знак, знак обслуживания Евразийского экономического союза"` (exact literal text from Table 68).
6. `P.SP.02.MSG.050.T68.REQ.6` (FULLY_MAPPABLE): Inherited from Table 49: `csdo:UnifiedCountryCode/@codeListId` == `"ВОИС ST.3"`.
7. `P.SP.02.MSG.050.T68.REQ.7` (FULLY_MAPPABLE): Inherited from Table 49: `ccdo:SubjectAddressDetails` requires `AddressKindCode`, `UnifiedCountryCode`, `CityName`, `StreetName`, `BuildingNumberId`.
8. `P.SP.02.MSG.050.T68.REQ.8` (FULLY_MAPPABLE): Inherited from Table 49: `ccdo:CommunicationDetails` requires `CommunicationChannelCode` and `CommunicationChannelId`, forbids `CommunicationChannelName`.
9. `P.SP.02.MSG.050.T68.REQ.9` (FULLY_MAPPABLE): Inherited from Table 49: `CommunicationChannelCode` IN `{"TE", "EM", "FX"}`.
10. `P.SP.02.MSG.050.T68.REQ.10` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:PatentAuthorityDetails` requires `UnifiedCountryCode`, `AuthorityName`, `AuthorityBriefName`.
11. `P.SP.02.MSG.050.T68.REQ.11` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:IPPartyDetails` (RH) cardinality 1..1.
12. `P.SP.02.MSG.050.T68.REQ.12` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:IPPartyDetails` requires `UnifiedCountryCode`, `IPSubjectName`, `SubjectAddressDetails`, `CommunicationDetails`.
13. `P.SP.02.MSG.050.T68.REQ.13` (FULLY_MAPPABLE): Inherited from Table 49: `IPPartyDetails/SubjectAddressDetails/csdo:AddressKindCode` == `"2"`.
14. `P.SP.02.MSG.050.T68.REQ.14` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:TrademarkDetails` requires `TrademarkPicture`, `TMDescriptionDetails`, `TrademarkKindName`, `CollectiveMarkIndicator`.
15. `P.SP.02.MSG.050.T68.REQ.15` (FULLY_MAPPABLE): Inherited from Table 49: `TMDescriptionDetails` requires `DescriptionText` and `TMElementDetails`; `TMElementDetails` requires `TrademarkCFECode`, `DesignationName`, `TMLocalizedName`, `TMTransliterationName`.
16. `P.SP.02.MSG.050.T68.REQ.16` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:GoodsBaseDetails` cardinality 1..*, requires `GoodsClassCode`, `GoodsClassName`, `GoodsName`, `TrademarkDecisionIndicator`, `TrademarkApplicationId`.
17. `P.SP.02.MSG.050.T68.REQ.17` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:GoodsBaseDetails` forbids `TrademarkId`, `ApellationOfOriginEAEUId`, `TrademarkRegRefusalReasonText`.
18. `P.SP.02.MSG.050.T68.REQ.20` (FULLY_MAPPABLE): In `ipcdo:IPEntityStatusDetails`: `csdo:EventDate` REQUIRED, `csdo:StatusCode` == `"05"` (EXACTLY "05"), `csdo:StatusCode/@codeListId` FORBIDDEN.
19. `P.SP.02.MSG.050.T68.REQ.21.PRESENCE` & `BRANCH` (FULLY_MAPPABLE): `ipcdo:SignatureDetails` cardinality 1..*; if `OfficerDetails != null` then `FullNameDetails` FORBIDDEN.
20. `P.SP.02.MSG.050.T68.REQ.22` (FULLY_MAPPABLE): In same `SignatureDetails`, if `FullNameDetails != null` then `OfficerDetails` FORBIDDEN.
21. `P.SP.02.MSG.050.T68.REQ.23` (FULLY_MAPPABLE): Under `OfficerDetails` directly in signature: `LastName`, `FirstName`, `PositionName` REQUIRED; `CommunicationDetails` FORBIDDEN.

Requirements 18 and 19 are strictly unmapped.

## MAPPING_COUNTS
- `captured_row_count`: 10
- `expanded_requirement_count`: 23
- `FULLY_MAPPABLE`: 18 (`[2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23]`)
- `SAFE_PARTIAL`: 3 (`[1, 4, 5]`)
- `EXTERNAL`: 0 (`[]`)
- `AMBIGUOUS`: 0 (`[]`)
- `ENGINE_UNSUPPORTED`: 2 (`[18, 19]`)
- `SOURCE_CONFLICT`: 0 (`[]`)
- Arithmetic check: `18 + 3 + 0 + 0 + 2 + 0 = 23`.
- Executable requirement codes: exactly 21 (`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23]`).
- Structured-rule object count: 24.

## PARTIAL_REMAINDERS
- **REQ 1 (SAFE_PARTIAL):** Active registration status and value matching in national patent office external resources remain external dependencies.
- **REQ 4, 5 (SAFE_PARTIAL):** Document kind classifier presence/absence lookups remain external dependencies.

## UNMAPPED_REQUIREMENTS
The 2 unmapped requirements remain strictly non-executable:
- **REQ 18 (ENGINE_UNSUPPORTED):** Conditional cross-collection dependency: if `CollectiveMarkIndicator == 1` then `IPPartyDetails` with kind `UE` required.
- **REQ 19 (ENGINE_UNSUPPORTED):** Conditional cross-collection dependency: if `CollectiveMarkIndicator == 1` then `AccompanyingDocumentsDetails` with charter document kind required.

## OWNER_QNAME_SAFETY
- **Structure root:** Message operates on `R.IP.SP.02.007` (`ipcdo:UnifiedRegisterRecordsDetails`).
- **Validity period:** `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime` is REQUIRED. No StartDateTime rule is fabricated.
- **Status codes:** `csdo:StatusCode` == `"05"` (CRITICAL: distinguished from registration `"01"`, application changes `"02"`, trademark changes `"03"`, and termination `"04"`).
- **Event date:** `csdo:EventDate` in `IPEntityStatusDetails` is REQUIRED.
- **Code list identifier:** `csdo:StatusCode/@codeListId` is FORBIDDEN.
- **Signatures:** Direct `SignatureDetails/OfficerDetails` and sibling `FullNameDetails` enforce same-parent mutual exclusion and required person fields without leaking across parents.

## MESSAGE_ISOLATION
Explicit isolation confirmed across related messages on `R.IP.SP.02.007`:
- **MSG047:** `StatusCode` == `"03"`, `EndDateTime` FORBIDDEN.
- **MSG048:** `StatusCode` == `"03"`, `CollectiveMarkIndicator` == `"1"`, `EndDateTime` FORBIDDEN.
- **MSG049:** `StatusCode` == `"03"`, `StartDateTime` REQUIRED, `EndDateTime` FORBIDDEN.
- **MSG050:** `StatusCode` == `"05"`, `EndDateTime` REQUIRED.
MSG050 validation uses only `P.SP.02.MSG.050.*` rules, with zero rule leakage or cross-contamination.

## NORMATIVE_BASIS
CONFIRMED:
- ОП_22.pdf, Table 68 (pp. 788–789), requirements 1–23.
- ОП_22.pdf, Table 49 (pp. 737–740), requirements 6–19 (inherited dual-provenance).

## MSG050_TESTS
Execution command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg050_*.py -p no:cacheprovider
```
Result:
```text
...........................
27 passed in 4.48s
```
Breakdown:
- `test_msg050_safe_mapping.py`: 10 passed
- `test_msg050_repeatable_xml.py`: 10 passed
- `test_msg050_end_to_end.py`: 7 passed

## OPTIONAL_FULL_REGRESSION
Catalog integrity suite:
```bash
python3.13 -m pytest -q P.SP.02_OP_22/tests/test_psp02_catalog.py -p no:cacheprovider
```
Result: 13 passed in 0.04s.

## CONCURRENT_CHANGES
Isolated strictly to MSG050 files. No modifications made to MSG001–049, MSG051+, or shared library code (`eaeu_xml`).

## GIT_DIFF_CHECK
Execution command:
```bash
git diff --check
```
Result: Clean exit code 0, no trailing whitespace or merge conflict markers.

## REMAINING_ISSUES
None
