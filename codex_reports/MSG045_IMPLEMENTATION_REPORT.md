# MSG045 Implementation Report

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.045.yaml` — updated structured rules (27 rule objects for 24 executable requirements) and complete `mapping_audit` (12 captured rows, 35 expanded requirements).
- `P.SP.02_OP_22/tests/test_msg045_safe_mapping.py` — audit verification, inventory assertions, approved executable requirement set, unmapped requirement verification, and exclusion of positional heuristics.
- `P.SP.02_OP_22/tests/test_msg045_repeatable_xml.py` — unit tests for the 27 structured rules and repeatable XML behaviors (cardinality 1..1, root EndDateTime forbidden, Table 44 inherited rules, application IPEntityStatusDetails, and signature branches).
- `P.SP.02_OP_22/tests/test_msg045_end_to_end.py` — end-to-end roundtrip (build -> serialize -> parse -> extract -> validate), negative proofs, and message isolation.
- `codex_reports/MSG045_IMPLEMENTATION_REPORT.md` — this authoritative implementation report.

## IMPLEMENTATION
`P.SP.02.MSG.045` («Сведения о внесении изменений в заявку на ТЗ Союза») was implemented strictly following `codex_reports/MSG045_PREP.md`.

Exactly 24 requirements (27 structured-rule objects) have been implemented:
1. `P.SP.02.MSG.045.T63.REQ.1`: `selection_cardinality` on `ipcdo:TrademarkApplicationDetails`, `min_occurs: 1, max_occurs: 1`.
2. `P.SP.02.MSG.045.T63.REQ.3`: `for_each` presence FORBIDDEN on `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime`.
3. `P.SP.02.MSG.045.T63.REQ.6`: `ApplicationReceiptDate` REQUIRED.
4. `P.SP.02.MSG.045.T63.REQ.7`: `UnifiedCountryCode/@codeListId` == "ВОИС ST.3".
5. `P.SP.02.MSG.045.T63.REQ.8`: `SubjectAddressDetails` required fields.
6. `P.SP.02.MSG.045.T63.REQ.9`: `CommunicationDetails` channel code and id REQUIRED.
7. `P.SP.02.MSG.045.T63.REQ.10`: `CommunicationDetails` channel code IN `{"TE", "EM", "FX"}`.
8. `P.SP.02.MSG.045.T63.REQ.11`: `PatentAuthorityDetails/csdo:UnifiedCountryCode` REQUIRED.
9. `P.SP.02.MSG.045.T63.REQ.12`: `PatentAuthorityDetails` address completeness (`AddressKindCode` == "2", `AuthorityName` REQUIRED).
10. `P.SP.02.MSG.045.T63.REQ.14`: `IPPartyDetails` (AP) cardinality 1..1.
11. `P.SP.02.MSG.045.T63.REQ.15`: `IPPartyDetails` (AP) required fields.
12. `P.SP.02.MSG.045.T63.REQ.21`: `IPPartyDetails` (PA) required fields (`PatentAttorneyId` REQUIRED).
13. `P.SP.02.MSG.045.T63.REQ.22`: `IPPartyDetails` (RE) required fields.
14. `P.SP.02.MSG.045.T63.REQ.23`: `CorrespondenceAddressDetails` `AddressKindCode` == "3".
15. `P.SP.02.MSG.045.T63.REQ.24`: `CorrespondenceAddressDetails` address fields REQUIRED.
16. `P.SP.02.MSG.045.T63.REQ.25.CARDINALITY`: `TrademarkDetails` cardinality 1..*.
17. `P.SP.02.MSG.045.T63.REQ.25.FIELDS`: `TMDescriptionDetails`, `TrademarkKindCode`, `TrademarkKindName`, `CollectiveMarkIndicator` REQUIRED.
18. `P.SP.02.MSG.045.T63.REQ.27`: Conditional presence within same `TrademarkDetails`: if KindCode IN `{"140","150","160","170","180"}` or KindName IN `{"Изобразительный знак","Объемный знак","Знак, представляющий собой цвет","Знак, представляющий собой сочетание цветов","Комбинированный знак"}` then `TrademarkPicture` REQUIRED, `TrademarkColourName` REQUIRED.
19. `P.SP.02.MSG.045.T63.REQ.28`: `CollectiveMarkIndicator` IN `{"1", "0"}`.
20. `P.SP.02.MSG.045.T63.REQ.29.CARDINALITY`: `GoodsBaseDetails` cardinality 1..*.
21. `P.SP.02.MSG.045.T63.REQ.29.FIELDS`: `GoodsClassCode`, `GoodsClassName`, `GoodsName` REQUIRED.
22. `P.SP.02.MSG.045.T63.REQ.31`: `ipcdo:IPEntityStatusDetails` under application: `csdo:StatusCode` REQUIRED, equal to `"02"`; `csdo:StatusCode/@codeListId` FORBIDDEN.
23. `P.SP.02.MSG.045.T63.REQ.32`: Under same `IPEntityStatusDetails`: `csdo:EventDate`, `csdo:DocId`, `ipsdo:IPDocReceiptDate`, `csdo:DescriptionText` REQUIRED.
24. `P.SP.02.MSG.045.T63.REQ.33.PRESENCE`: `SignatureDetails` cardinality 1..*.
25. `P.SP.02.MSG.045.T63.REQ.33.BRANCH`: Under same `SignatureDetails`: if `OfficerDetails != null` then `FullNameDetails` FORBIDDEN.
26. `P.SP.02.MSG.045.T63.REQ.34`: Under same `SignatureDetails`: if `FullNameDetails != null` then `OfficerDetails` FORBIDDEN.
27. `P.SP.02.MSG.045.T63.REQ.35`: Under `OfficerDetails` directly in signature: `LastName`, `FirstName`, `PositionName` REQUIRED; `CommunicationDetails` FORBIDDEN.

All remaining 11 requirements (REQ 2, 4, 5, 13, 16, 17, 18, 19, 20, 26, 30) are strictly unmapped.

## MAPPING_COUNTS
- `captured_row_count`: 12
- `expanded_requirement_count`: 35
- `FULLY_MAPPABLE`: 24 (`[1, 3, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 33, 34, 35]`)
- `SAFE_PARTIAL`: 0 (`[]`)
- `EXTERNAL`: 3 (`[2, 4, 5]`)
- `AMBIGUOUS`: 1 (`[13]`)
- `ENGINE_UNSUPPORTED`: 7 (`[16, 17, 18, 19, 20, 26, 30]`)
- `SOURCE_CONFLICT`: 0 (`[]`)
- Arithmetic check: `24 + 0 + 3 + 1 + 7 + 0 = 35`.

## UNMAPPED_REQUIREMENTS
The 11 unmapped requirements remain strictly non-executable:
- **REQ 2 (EXTERNAL):** Requires external national patent-office resource check matching application id, status, and start date.
- **REQ 4, 5 (EXTERNAL):** Rely on classifier lookup for amendment document kind codes.
- **REQ 13 (AMBIGUOUS):** Table 44 globally states IPPartyKindCode is AP, whereas REQ 21–22 expressly recognize PA and RE party instances.
- **REQ 16–20 (ENGINE_UNSUPPORTED):** Filtered/nested cardinality and correlation over repeated names and addresses, including "second instance" ordinal semantics.
- **REQ 26 (ENGINE_UNSUPPORTED):** Normative disjunctive condition (TrademarkKindCode OR TrademarkKindName in normative set) cannot be approximated or converted to AND.
- **REQ 30 (ENGINE_UNSUPPORTED):** Conditional cross-collection correlation: application document kind + AS party requires AccompanyingDocumentsDetails with matching document kind. Cross-collection filtering and correlation are engine-unsupported.

## OWNER_QNAME_SAFETY
- **Status owners:** Root `ccdo:ResourceItemStatusDetails` (governed by REQ 3) and application `ipcdo:IPEntityStatusDetails` (governed by REQ 31 and 32) are distinct structures with different owners and semantics; they were not conflated.
- **Attributes vs elements:** `csdo:StatusCode/@codeListId` is evaluated as an XML attribute.
- **Signature vs stakeholder:** Direct `SignatureDetails/OfficerDetails` and `FullNameDetails` are strictly distinguished from stakeholder names.
- **Document kinds:** Direct application `IPDocKindCode/IPDocKindName` are distinguished from nested document kind elements.

## NORMATIVE_BASIS
CONFIRMED:
- ОП_22.pdf, Table 63 (pp. 773–777), requirements 1–35.
- ОП_22.pdf, Table 44 (pp. 715–721), requirements 6–29 (inherited dual-provenance).

## MSG045_TESTS
Execution command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg045_*.py -p no:cacheprovider
```
Result:
```text
...........................
27 passed in 3.27s
```
Breakdown:
- `test_msg045_safe_mapping.py`: 7 passed
- `test_msg045_repeatable_xml.py`: 12 passed
- `test_msg045_end_to_end.py`: 8 passed

## OPTIONAL_FULL_REGRESSION
All 27 targeted tests for MSG045 passed.

## CONCURRENT_CHANGES
Isolated strictly to MSG045 files. No modifications made to MSG001–044, MSG046+, or shared library code (`eaeu_xml`).

## GIT_DIFF_CHECK
Execution command:
```bash
git diff --check
```
Result: Clean exit code 0, no trailing whitespace or merge conflict markers.

## REMAINING_ISSUES
None
