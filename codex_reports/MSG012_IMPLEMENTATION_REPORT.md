# MSG012 Implementation Report

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.012.yaml` — updated mapping audit (11 captured rows, 34 expanded requirements, 23 fully mappable, 5 external, 1 ambiguous, 5 engine unsupported) and structured rules (28 rules implementing all approved capabilities: parent-scoped selectors for inherited Table 34 child collections under Role B StatusCode 01, inclusive OR condition assertion for REQ 26, cross-instance comparison for REQ 30, semantic role uniqueness for REQ 31, and exact cardinality/dates for REQs 1, 33, 34).
- `P.SP.02_OP_22/tests/test_msg012_safe_mapping.py` — audit inventory tests, exact classification assertions, REQ 26 condition assertion verification, REQ 30 cross-instance comparison checks, REQ 31 semantic role checks, and unmapped requirement assertions.
- `P.SP.02_OP_22/tests/test_msg012_repeatable_xml.py` — tests for exact cardinality (2..2), start/end validity dates, parent context isolation, cross-instance matching/mismatch, REQ 26 truth table, and proof of XML order independence without positional heuristics.
- `P.SP.02_OP_22/tests/test_msg012_end_to_end.py` — production roundtrip (build -> serialize -> parse -> extract -> validate) for both physical orders (Role A then B, and Role B then A), negative proofs, and message isolation.
- `codex_reports/MSG012_IMPLEMENTATION_REPORT.md` — this authoritative implementation report.

## NORMATIVE_INVENTORY
Normative source: `ОП_22.pdf`, IX. Требования к заполнению электронных документов и сведений, Таблица 45. Требования к электронному документу (сведениям) P.SP.02.MSG.012, physical pages 550–552.
- Structure: `R.IP.SP.02.002`, version `1.0.0` (`{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails`).
- Captured rows: 11 (REQ 1, 2, 3, 4, 5, 6_29, 30, 31, 32, 33, 34).
- Expanded requirements: 34 (REQ 1 to 34). Inherited requirements 6–29 from Table 34 (pp. 514–520, P.SP.02.MSG.001) apply exclusively to the divided application instance («выделенная заявка») with status `01`.

## SEMANTIC_ROLE_BINDING
Table 45 governs exactly two `ipcdo:TrademarkApplicationDetails` instances under root with distinct semantic roles:
- **Role A («ранее поданная заявка» / initial application):**
  - XML predicate: `ipcdo:IPEntityStatusDetails/csdo:StatusCode == "02"` («заявка на ТЗ Союза изменена»).
  - Attribute constraint: `csdo:StatusCode/@codeListId` is FORBIDDEN (REQ 31.ATTR).
  - Cardinality constraint: exactly 1 instance with `StatusCode == "02"` (REQ 31.ROLE02).
  - Doc-kind rules: REQ 2 / REQ 3 (EXTERNAL).
- **Role B («выделенная заявка» / divided application):**
  - XML predicate: `ipcdo:IPEntityStatusDetails/csdo:StatusCode == "01"` («новая заявка на ТЗ Союза»).
  - Cardinality constraint: exactly 1 instance with `StatusCode == "01"` (REQ 31.ROLE01).
  - Required identifier: `ipsdo:SourceTrademarkApplicationId` is required and matches `ipsdo:TrademarkApplicationId` of Role A (REQ 30 via `cross_instance_comparison`).
  - Inherited rules: governed exclusively by Table 34 REQs 6–29, bound via Capability A (`selector.parent.where: StatusCode == "01"`).

**Confirmation:**
NO POSITIONAL [0]/[1] ROLE BINDING.
Neither the schema nor Table 45 distinguishes the two application instances by ordinal index, order of appearance, or parent position. They are identical repeatable `ipcdo:TrademarkApplicationDetails` siblings. Order A/B and Order B/A produce 100% identical evaluation and validation results.

## IMPLEMENTATION
The 28 executable structured rules in `P.SP.02.MSG.012.yaml` implement 23 fully mappable requirements:
1. `P.SP.02.MSG.012.T45.REQ.1`: `selection_cardinality` on `ipcdo:TrademarkApplicationDetails`, `min_occurs: 2, max_occurs: 2`.
2. `P.SP.02.MSG.012.T45.REQ.6`: `for_each` presence REQUIRED on `ipsdo:ApplicationReceiptDate` for Role B (`StatusCode == "01"`).
3. `P.SP.02.MSG.012.T45.REQ.7`: `for_each` fixed_value `"ВОИС ST.3"` on `PatentAuthorityDetails/csdo:UnifiedCountryCode/@codeListId` (Capability A scoped to Role B).
4. `P.SP.02.MSG.012.T45.REQ.8`: `for_each` presence REQUIRED on `CorrespondenceAddressDetails/SubjectAddressDetails` fields (Capability A scoped to Role B).
5. `P.SP.02.MSG.012.T45.REQ.9`: `for_each` presence REQUIRED on `CommunicationChannelCode`, `CommunicationChannelId` and FORBIDDEN on `CommunicationChannelName` (Capability A scoped to Role B).
6. `P.SP.02.MSG.012.T45.REQ.10`: `for_each` fixed_value `"EM"` on `CommunicationChannelCode` (Capability A scoped to Role B).
7. `P.SP.02.MSG.012.T45.REQ.11`: `for_each` presence REQUIRED on `PatentAuthorityDetails/csdo:UnifiedCountryCode` (Capability A scoped to Role B).
8. `P.SP.02.MSG.012.T45.REQ.12`: `for_each` presence REQUIRED on `PatentAuthorityDetails/csdo:AuthorityName` and fixed_value `"2"` on `AddressKindCode` (Capability A scoped to Role B).
9. `P.SP.02.MSG.012.T45.REQ.14`: `selection_cardinality` min 1, max 1 on `IPPartyDetails` where `IPPartyKindCode == "AP"` (Capability A scoped to Role B).
10. `P.SP.02.MSG.012.T45.REQ.15`: `for_each` presence REQUIRED on applicant (`AP`) fields (Capability A scoped to Role B).
11. `P.SP.02.MSG.012.T45.REQ.21`: `for_each` presence REQUIRED on patent attorney (`PA`) fields (Capability A scoped to Role B).
12. `P.SP.02.MSG.012.T45.REQ.22`: `for_each` presence REQUIRED on representative (`RE`) fields (Capability A scoped to Role B).
13. `P.SP.02.MSG.012.T45.REQ.23`: `for_each` fixed_value `"3"` on `CorrespondenceAddressDetails/SubjectAddressDetails/csdo:AddressKindCode` (Capability A scoped to Role B).
14. `P.SP.02.MSG.012.T45.REQ.24`: `for_each` comparison IN `["AM", "BY", "KZ", "KG", "RU"]` on `CorrespondenceAddressDetails/SubjectAddressDetails/csdo:UnifiedCountryCode` (Capability A scoped to Role B).
15. `P.SP.02.MSG.012.T45.REQ.25.CARD`: `selection_cardinality` min 1, max 1 on `TrademarkDetails` (Capability A scoped to Role B).
16. `P.SP.02.MSG.012.T45.REQ.25.DESC`: `selection_cardinality` min 1, max 1 on `TMDescriptionDetails` (Capability A scoped to Role B).
17. `P.SP.02.MSG.012.T45.REQ.25`: `for_each` presence REQUIRED on `TrademarkKindCode`, `TrademarkKindName`, `CollectiveMarkIndicator`, `TMDescriptionDetails/DescriptionText` (Capability A scoped to Role B).
18. `P.SP.02.MSG.012.T45.REQ.26`: `for_each` condition assertion with `any` (inclusive OR) across `ipsdo:TrademarkKindCode` and `ipsdo:TrademarkKindName` (Capability A + Capability B).
19. `P.SP.02.MSG.012.T45.REQ.27`: `for_each` conditional presence REQUIRED on `TrademarkPicture` when `TrademarkKindCode IN ["140", "150", "160", "170", "180"]` (Capability A scoped to Role B).
20. `P.SP.02.MSG.012.T45.REQ.28`: `for_each` comparison IN `["0", "1"]` on `CollectiveMarkIndicator` (Capability A scoped to Role B).
21. `P.SP.02.MSG.012.T45.REQ.29.CARD`: `selection_cardinality` min 1 on `GoodsBaseDetails` (Capability A scoped to Role B).
22. `P.SP.02.MSG.012.T45.REQ.29`: `for_each` presence REQUIRED on `GoodsClassCode`, `GoodsClassName`, `GoodsName` (Capability A scoped to Role B).
23. `P.SP.02.MSG.012.T45.REQ.30`: `cross_instance_comparison` EQ between Role B `SourceTrademarkApplicationId` and Role A `TrademarkApplicationId` (Capability C).
24. `P.SP.02.MSG.012.T45.REQ.31.ATTR`: `for_each` presence FORBIDDEN on `StatusCode/@codeListId` for Role A (`StatusCode == "02"`).
25. `P.SP.02.MSG.012.T45.REQ.31.ROLE01`: `selection_cardinality` min 1, max 1 for Role B (`StatusCode == "01"`).
26. `P.SP.02.MSG.012.T45.REQ.31.ROLE02`: `selection_cardinality` min 1, max 1 for Role A (`StatusCode == "02"`).
27. `P.SP.02.MSG.012.T45.REQ.33`: `for_each` presence REQUIRED on `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime`.
28. `P.SP.02.MSG.012.T45.REQ.34`: `for_each` presence FORBIDDEN on `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime`.

## MAPPING_COUNTS
- exact captured: 11
- exact expanded: 34
- exact counts:
  - `FULLY_MAPPABLE`: 23
  - `SAFE_PARTIAL`: 0
  - `EXTERNAL`: 5
  - `AMBIGUOUS`: 1
  - `ENGINE_UNSUPPORTED`: 5
  - `SOURCE_CONFLICT`: 0
- exact executable requirement set: {1, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34}
- exact unmapped requirement set: {2, 3, 4, 5, 13, 16, 17, 18, 19, 20, 32}
- structured-rule object count: 28

Arithmetic check: `23 + 0 + 5 + 1 + 5 + 0 = 34`.

## PARTIAL_REMAINDERS
None.

## UNMAPPED_REQUIREMENTS
- **REQ 2–5, 32 (EXTERNAL):** Rely on external classifier resolution and external national patent office database checks.
- **REQ 13 (AMBIGUOUS):** Ambiguous normative definition in isolation; IPPartyKindCode AP is enforced as part of requirement 14.
- **REQ 16–20 (ENGINE_UNSUPPORTED):** Require ordinal positional indexing of multiple repeated `IPSubjectName` instances within a repeatable parent, which is unsupported by the engine.

## REQ26_ANALYSIS
- **REQ26_NORMATIVE_FORM:**
  `(ipsdo:TrademarkKindCode IN ["110", "120", "130", "140", "150", "160", "170", "180"]) OR (ipsdo:TrademarkKindName IN ["Словесный знак", "Буквенный знак", "Цифровой знак", "Изобразительный знак", "Объемный знак", "Знак, представляющий собой цвет", "Знак, представляющий собой сочетание цветов", "Комбинированный знак"])`
- **REQ26_ENGINE_CAPABILITY:**
  Fully supported via Capability B (`kind: "condition"` assertion delegating to `evaluate_condition` with `any: [...]`).
- **REQ26_FINAL_CLASSIFICATION:**
  FULLY_MAPPABLE
- **REQ26_EXECUTABLE_RULE_COUNT:**
  1 (`P.SP.02.MSG.012.T45.REQ.26`)

## OWNER_QNAME_SAFETY
- Cardinality applies to exact root collection `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}TrademarkApplicationDetails`.
- Status codes apply to `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}IPEntityStatusDetails/{urn:EEC:M:SimpleDataObjects:vX.X.X}StatusCode`.
- Child collections use exact QName paths with parent filtering:
  - `PatentAuthorityDetails`: `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}PatentAuthorityDetails`
  - `CorrespondenceAddressDetails`: `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}CorrespondenceAddressDetails`
  - `IPPartyDetails`: `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}IPPartyDetails`
  - `TrademarkDetails`: `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}TrademarkDetails`
  - `GoodsBaseDetails`: `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}GoodsBaseDetails`
- Resource validity dates apply to `{urn:EEC:M:ComplexDataObjects:vX.X.X}ResourceItemStatusDetails/{urn:EEC:M:ComplexDataObjects:vX.X.X}ValidityPeriodDetails`.
- No local-name-only fallback matching is used.

## REPEATABLE_RECORD_SAFETY
- Exactly two application records are required.
- Physical order of records is completely independent: Order A/B (initial + divided) and Order B/A (divided + initial) produce identical validation results.
- No positional indexing `[0]`/`[1]` or ordinal assumptions (`first`, `second`) exist in rules or tests.
- Sibling isolation is fully verified: children under Role A do not contaminate or repair children under Role B.

## MESSAGE_ISOLATION
All structured rules use strict prefix `P.SP.02.MSG.012.T45.REQ.*`. Verification confirms rules from other messages sharing structure `R.IP.SP.02.002` (such as MSG.001, MSG.004, MSG.010, MSG.014) do not execute for MSG.012.

## NORMATIVE_BASIS
- CONFIRMED — `ОП_22.pdf`, Таблица 45 (physical pp. 550–552), requirements 1–34.
- CONFIRMED — `ОП_22.pdf`, Таблица 34 (physical pp. 514–520), requirements 6–29 (dual provenance for divided application).

## MSG012_TESTS
Execution command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg012_*.py -p no:cacheprovider
```
Result: **28 passed in 0.40s**.
- `test_msg012_safe_mapping.py`: 8 passed
- `test_msg012_repeatable_xml.py`: 11 passed
- `test_msg012_end_to_end.py`: 9 passed

## ENGINE_AND_VALIDATOR_TESTS
Execution command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider
```
Result: **40 passed, 5 subtests passed in 0.12s**.

## FULL_EAEU_XML_REGRESSION
Execution command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests -p no:cacheprovider
```
Result: **291 passed, 43 skipped, 1052 subtests passed in 2.62s** (0 failed, 0 errors).

## FULL_OP22_REGRESSION
Execution command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests -p no:cacheprovider
```
Result: **2109 passed in 84.83s (0:01:24)** (0 failed, 0 errors).
Baseline before MSG012: 2101 passed.
Increase: +8 passed (28 total MSG012 tests replacing previous 20 tests).

## GIT_DIFF_CHECK
Execution command:
```bash
git diff --check
```
Result: Clean exit code 0, no trailing whitespace or merge conflict markers.

## REMAINING_ISSUES
None.
