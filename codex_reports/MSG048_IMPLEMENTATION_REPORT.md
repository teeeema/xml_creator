# MSG048 Implementation Report

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.048.yaml` — updated structured rules (24 rule objects for 23 executable requirements) and complete `mapping_audit` (12 captured rows, 25 expanded requirements).
- `P.SP.02_OP_22/tests/test_msg048_safe_mapping.py` — audit verification, inventory assertions, approved executable requirement set, unmapped requirement verification, and inherited dual-provenance checks.
- `P.SP.02_OP_22/tests/test_msg048_repeatable_xml.py` — unit tests for the structured rules and repeatable XML behaviors (cardinality 1..1, StatusCode "03", fallback document kind literal, Table 49 inherited rules, TransformationDetails per-instance validation, CollectiveMarkIndicator "1", validity EndDateTime forbidden, and signature mutual exclusion).
- `P.SP.02_OP_22/tests/test_msg048_end_to_end.py` — end-to-end roundtrip (build -> serialize -> parse -> extract -> validate), negative proofs, and message isolation.
- `codex_reports/MSG048_IMPLEMENTATION_REPORT.md` — this authoritative implementation report.

## IMPLEMENTATION
`P.SP.02.MSG.048` («Сведения о преобразовании товарного знака Союза в коллективный знак Союза») was implemented based on `R.IP.SP.02.007 v1.0.0` («сведения о ТЗ Союза из Единого реестра ТЗ Союза»).

Exactly 23 requirements (24 structured-rule objects) have been implemented:
1. `P.SP.02.MSG.048.T66.REQ.1` (SAFE_PARTIAL): `ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId` is REQUIRED locally.
2. `P.SP.02.MSG.048.T66.REQ.2` (FULLY_MAPPABLE): `selection_cardinality` on `ipcdo:UnifiedRegisterRecordsDetails`, `min_occurs: 1, max_occurs: 1`.
3. `P.SP.02.MSG.048.T66.REQ.3` (FULLY_MAPPABLE): In `ipcdo:IPEntityStatusDetails`, `csdo:StatusCode` == `"03"`, `csdo:EventDate` REQUIRED, `csdo:StatusCode/@codeListId` FORBIDDEN.
4. `P.SP.02.MSG.048.T66.REQ.4` (SAFE_PARTIAL): If `ipsdo:IPDocKindCode != null` then `ipsdo:IPDocKindName` FORBIDDEN.
5. `P.SP.02.MSG.048.T66.REQ.5` (SAFE_PARTIAL): If `ipsdo:IPDocKindCode == null` then `ipsdo:IPDocKindName` equals `"Ходатайство о преобразовании коллективного знака Евразийского экономического союза в товарный знак, знак обслуживания Евразийского экономического союза"` (exact literal text preserved from Table 66).
6. `P.SP.02.MSG.048.T66.REQ.6` (FULLY_MAPPABLE): Inherited from Table 49: `csdo:UnifiedCountryCode/@codeListId` == `"ВОИС ST.3"`.
7. `P.SP.02.MSG.048.T66.REQ.7` (FULLY_MAPPABLE): Inherited from Table 49: `ccdo:SubjectAddressDetails` requires `AddressKindCode`, `UnifiedCountryCode`, `CityName`, `StreetName`, `BuildingNumberId`.
8. `P.SP.02.MSG.048.T66.REQ.8` (FULLY_MAPPABLE): Inherited from Table 49: `ccdo:CommunicationDetails` requires `CommunicationChannelCode` and `CommunicationChannelId`, forbids `CommunicationChannelName`.
9. `P.SP.02.MSG.048.T66.REQ.9` (FULLY_MAPPABLE): Inherited from Table 49: `CommunicationChannelCode` IN `{"TE", "EM", "FX"}`.
10. `P.SP.02.MSG.048.T66.REQ.10` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:PatentAuthorityDetails` requires `UnifiedCountryCode`, `AuthorityName`, `AuthorityBriefName`.
11. `P.SP.02.MSG.048.T66.REQ.11` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:IPPartyDetails` (RH) cardinality 1..1.
12. `P.SP.02.MSG.048.T66.REQ.12` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:IPPartyDetails` requires `UnifiedCountryCode`, `IPSubjectName`, `SubjectAddressDetails`, `CommunicationDetails`.
13. `P.SP.02.MSG.048.T66.REQ.13` (FULLY_MAPPABLE): Inherited from Table 49: `IPPartyDetails/SubjectAddressDetails/csdo:AddressKindCode` == `"2"`.
14. `P.SP.02.MSG.048.T66.REQ.14` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:TrademarkDetails` requires `TrademarkPicture`, `TMDescriptionDetails`, `TrademarkKindName`, `CollectiveMarkIndicator`.
15. `P.SP.02.MSG.048.T66.REQ.15` (FULLY_MAPPABLE): Inherited from Table 49: `TMDescriptionDetails` requires `DescriptionText` and `TMElementDetails`; `TMElementDetails` requires `TrademarkCFECode`, `DesignationName`, `TMLocalizedName`, `TMTransliterationName`.
16. `P.SP.02.MSG.048.T66.REQ.16` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:GoodsBaseDetails` cardinality 1..*, requires `GoodsClassCode`, `GoodsClassName`, `GoodsName`, `TrademarkDecisionIndicator`, `TrademarkApplicationId`.
17. `P.SP.02.MSG.048.T66.REQ.17` (FULLY_MAPPABLE): Inherited from Table 49: `ipcdo:GoodsBaseDetails` forbids `TrademarkId`, `ApellationOfOriginEAEUId`, `TrademarkRegRefusalReasonText`.
18. `P.SP.02.MSG.048.T66.REQ.20` (FULLY_MAPPABLE): For each existing `ipcdo:TransformationDetails`, requires `ipsdo:TransformationKindName`, `ipsdo:IPObjectId`, `csdo:EventDate` (0 instances allowed; container existence not required).
19. `P.SP.02.MSG.048.T66.REQ.21` (FULLY_MAPPABLE): Under `ipcdo:TrademarkDetails`, `ipsdo:CollectiveMarkIndicator` must equal `"1"`.
20. `P.SP.02.MSG.048.T66.REQ.22` (FULLY_MAPPABLE): Under `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails`, `csdo:EndDateTime` is FORBIDDEN (no StartDateTime requirement).
21. `P.SP.02.MSG.048.T66.REQ.23.PRESENCE` & `BRANCH` (FULLY_MAPPABLE): `ipcdo:SignatureDetails` cardinality 1..*; if `OfficerDetails != null` then `FullNameDetails` FORBIDDEN.
22. `P.SP.02.MSG.048.T66.REQ.24` (FULLY_MAPPABLE): In same `SignatureDetails`, if `FullNameDetails != null` then `OfficerDetails` FORBIDDEN.
23. `P.SP.02.MSG.048.T66.REQ.25` (FULLY_MAPPABLE): Under `OfficerDetails` directly in signature: `LastName`, `FirstName`, `PositionName` REQUIRED; `CommunicationDetails` FORBIDDEN.

Requirements 18 and 19 are strictly unmapped.

## MAPPING_COUNTS
- `captured_row_count`: 12
- `expanded_requirement_count`: 25
- `FULLY_MAPPABLE`: 20 (`[2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25]`)
- `SAFE_PARTIAL`: 3 (`[1, 4, 5]`)
- `EXTERNAL`: 0 (`[]`)
- `AMBIGUOUS`: 0 (`[]`)
- `ENGINE_UNSUPPORTED`: 2 (`[18, 19]`)
- `SOURCE_CONFLICT`: 0 (`[]`)
- Arithmetic check: `20 + 3 + 0 + 0 + 2 + 0 = 25`.

## UNMAPPED_REQUIREMENTS
The 2 unmapped requirements remain strictly non-executable:
- **REQ 18 (ENGINE_UNSUPPORTED):** Conditional cross-collection dependency: if `CollectiveMarkIndicator == 1` then `IPPartyDetails` with kind `UE` required.
- **REQ 19 (ENGINE_UNSUPPORTED):** Conditional cross-collection dependency: if `CollectiveMarkIndicator == 1` then `AccompanyingDocumentsDetails` with charter document kind required.

Partial remainders:
- **REQ 1 (SAFE_PARTIAL):** Active registration status and value matching in national patent office external resources remain external dependencies.
- **REQ 4, 5 (SAFE_PARTIAL):** Document kind classifier presence/absence lookups remain external dependencies.

## OWNER_QNAME_SAFETY
- **Structure root:** Message operates on `R.IP.SP.02.007` (`ipcdo:UnifiedRegisterRecordsDetails`).
- **Status codes:** `csdo:StatusCode` == `"03"` (CRITICAL: distinguished from registration `"01"` and application changes `"02"`).
- **Collective mark indicator:** `ipsdo:CollectiveMarkIndicator` == `"1"` (CRITICAL: mark transformed into collective trademark, in contrast to MSG047 which requires `"0"`).
- **Transformation container:** `ipcdo:TransformationDetails` validates per existing instance; 0 instances cleanly evaluate to PASS without error.
- **Validity period:** `csdo:EndDateTime` is FORBIDDEN; no StartDateTime rule is fabricated.
- **Signatures:** Direct `SignatureDetails/OfficerDetails` and sibling `FullNameDetails` enforce same-parent mutual exclusion and required person fields without leaking across parents.

## NORMATIVE_BASIS
CONFIRMED:
- ОП_22.pdf, Table 66 (pp. 783–785), requirements 1–25.
- ОП_22.pdf, Table 49 (pp. 737–740), requirements 6–19 (inherited dual-provenance).

## MSG048_TESTS
Execution command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg048_*.py -p no:cacheprovider
```
Result:
```text
.................................
33 passed in 2.67s
```
Breakdown:
- `test_msg048_safe_mapping.py`: 12 passed
- `test_msg048_repeatable_xml.py`: 12 passed
- `test_msg048_end_to_end.py`: 9 passed

## OPTIONAL_FULL_REGRESSION
Catalog integrity suite:
```bash
python3.13 -m pytest -q P.SP.02_OP_22/tests/test_psp02_catalog.py -p no:cacheprovider
```
Result: 13 passed in 0.04s.

## CONCURRENT_CHANGES
Isolated strictly to MSG048 files. No modifications made to MSG001–047, MSG049+, or shared library code (`eaeu_xml`).

## GIT_DIFF_CHECK
Execution command:
```bash
git diff --check
```
Result: Clean exit code 0, no trailing whitespace or merge conflict markers.

## REMAINING_ISSUES
None
