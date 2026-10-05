# MSG043 Remediation Report

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.043.yaml` — updated mapping audit (14 captured rows, 37 expanded requirements, 26 fully mappable, 5 external, 1 ambiguous, 5 engine unsupported) and structured rules (32 rules implementing all approved capabilities: parent-scoped selectors for inherited Table 44 child collections under allocated application StatusCode 01, inclusive OR condition assertion for REQ 26, cross-instance comparison for REQ 30, semantic role uniqueness for REQ 32, and exact cardinality/dates/signatures for REQs 1, 33–37).
- `P.SP.02_OP_22/tests/test_msg043_safe_mapping.py` — audit inventory tests, exact classification assertions, REQ 26 condition assertion verification, REQ 30 cross-instance comparison checks, REQ 32 semantic role checks, parent-scoped selector checks, and unmapped requirement assertions.
- `P.SP.02_OP_22/tests/test_msg043_repeatable_xml.py` — tests for exact cardinality (2..2), start/end validity dates, signature branches and officer details, parent context isolation, cross-instance matching/mismatch, REQ 26 truth table (TT, TF, FT -> PASS; FF, None -> FAIL), semantic role uniqueness and attribute, and proof of XML order independence without positional heuristics.
- `P.SP.02_OP_22/tests/test_msg043_end_to_end.py` — production roundtrip (build -> serialize -> parse -> extract -> validate) for both physical orders (Role A then B, and Role B then A), negative proofs (REQ 1, REQ 30, REQ 32, REQ 33, REQ 34, REQ 35/36, REQ 37), and message isolation.
- `codex_reports/MSG043_REMEDIATION_REPORT.md` — this authoritative remediation report.

## PREVIOUS_STATE
Under the old engine without capabilities A/B/C:
- Captured requirements: 14
- Expanded requirements: 37
- `FULLY_MAPPABLE`: 6 ({1, 33, 34, 35, 36, 37})
- `EXTERNAL`: 5 ({2, 3, 4, 5, 31})
- `ENGINE_UNSUPPORTED`: 26 ({6..30, 32})
- Structured rules: 7
The previous implementation intentionally did not bind the two application records positionally, leaving all inherited Table 44 requirements and cross-instance requirements unsupported.

## NORMATIVE_INVENTORY
Normative source: `ОП_22.pdf`, IX. Требования к заполнению электронных документов и сведений:
- Primary Table: Таблица 61. Требования к электронному документу (сведениям) P.SP.02.MSG.043, physical pages 767–770.
- Inherited Table: Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028, physical pages 714–721.
- Structure: `R.IP.SP.02.002`, version `1.0.0` (`{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails`).
- Captured rows: 14 (REQ 1, 2, 3, 4, 5, 6_29, 30, 31, 32, 33, 34, 35, 36, 37).
- Expanded requirements: 37 (REQ 1 to 37). Inherited requirements 6–29 from Table 44 apply exclusively to the allocated/divided application instance («выделенная заявка») with status `01`.

## SEMANTIC_ROLES
Table 61 governs exactly two `ipcdo:TrademarkApplicationDetails` instances under root with distinct semantic roles:
- **Prior application («ранее поданная заявка»):**
  - XML predicate: `ipcdo:IPEntityStatusDetails/csdo:StatusCode == "02"` («заявка на ТЗ Союза изменена»).
  - Attribute constraint: `csdo:StatusCode/@codeListId` is FORBIDDEN (REQ 32.ATTR).
  - Cardinality constraint: exactly 1 instance with `StatusCode == "02"` (REQ 32.ROLE02).
  - Doc-kind rules: REQ 2 / REQ 3 (EXTERNAL).
- **Allocated / divided application («выделенная заявка»):**
  - XML predicate: `ipcdo:IPEntityStatusDetails/csdo:StatusCode == "01"` («новая заявка на ТЗ Союза»).
  - Cardinality constraint: exactly 1 instance with `StatusCode == "01"` (REQ 32.ROLE01).
  - Required identifier: `ipsdo:SourceTrademarkApplicationId` is required and matches `ipsdo:TrademarkApplicationId` of the prior application (REQ 30 via `cross_instance_comparison`).
  - Inherited rules: governed exclusively by Table 44 REQs 6–29, bound via Capability A (`selector.parent.where: StatusCode == "01"`).

**Strict Confirmation:**
NO POSITIONAL [0]/[1] ROLE BINDING.
Neither the schema nor Table 61 distinguishes the two application instances by ordinal index, order of appearance, or parent position. They are identical repeatable `ipcdo:TrademarkApplicationDetails` siblings. Order A/B and Order B/A produce 100% identical evaluation and validation results.

## CAPABILITY_A_IMPACT
Capability A (`selector.parent`) enables scoping nested child collections to the allocated application parent (`StatusCode == "01"`):
- Governs REQs 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 29.
- Verified: invalid children under Role A (`StatusCode == "02"`) do not contaminate or poison rules governing Role B (`StatusCode == "01"`).
- Verified: reverse physical XML order produces identical evaluation results.

## CAPABILITY_B_IMPACT
Capability B (`kind: condition` with `any` block) enables exact expression of inclusive OR semantics:
- Governs REQ 26: `ipsdo:TrademarkKindCode IN ["110", "120", "130", "140", "150", "160", "170", "180"] OR ipsdo:TrademarkKindName IN ["Словесный знак", "Буквенный знак", "Цифровой знак", "Изобразительный знак", "Объемный знак", "Знак, представляющий собой цвет", "Знак, представляющий собой сочетание цветов", "Комбинированный знак"]`.
- Verified truth table: TT -> PASS, TF -> PASS, FT -> PASS, FF -> FAIL, None -> FAIL.

## CAPABILITY_C_IMPACT
Capability C (`cross_instance_comparison`) enables exact cross-instance equality evaluation:
- Governs REQ 30: `SourceTrademarkApplicationId` of allocated application (`StatusCode == "01"`) EQ `TrademarkApplicationId` of prior application (`StatusCode == "02"`).
- Verified: matching -> PASS, mismatch -> FAIL, reversed physical XML order -> PASS, duplicate role -> FAIL.

## FINAL_MAPPING_COUNTS
- Captured row count: 14
- Expanded requirement count: 37
- Classification counts:
  - `FULLY_MAPPABLE`: 26
  - `SAFE_PARTIAL`: 0
  - `EXTERNAL`: 5
  - `AMBIGUOUS`: 1
  - `ENGINE_UNSUPPORTED`: 5
  - `SOURCE_CONFLICT`: 0
- Executable requirement set: {1, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 37}
- Unmapped requirement set: {2, 3, 4, 5, 13, 16, 17, 18, 19, 20, 31}
- Structured-rule object count: 32

Arithmetic check: `26 + 0 + 5 + 1 + 5 + 0 = 37`.

## NEWLY_EXECUTABLE_REQUIREMENTS
20 newly executable requirements:
1. `P.SP.02.MSG.043.T61.REQ.6`: ApplicationReceiptDate REQUIRED for allocated app (StatusCode 01).
2. `P.SP.02.MSG.043.T61.REQ.7`: UnifiedCountryCode/@codeListId fixed to "ВОИС ST.3" (Capability A).
3. `P.SP.02.MSG.043.T61.REQ.8`: Correspondence address required fields (Capability A).
4. `P.SP.02.MSG.043.T61.REQ.9`: Communication channel code & id required, name forbidden (Capability A).
5. `P.SP.02.MSG.043.T61.REQ.10`: Communication channel code IN ["TE", "EM", "FX"] (Capability A).
6. `P.SP.02.MSG.043.T61.REQ.11`: PatentAuthorityDetails UnifiedCountryCode required (Capability A).
7. `P.SP.02.MSG.043.T61.REQ.12`: PatentAuthorityDetails AuthorityName and AddressKindCode "2" (Capability A).
8. `P.SP.02.MSG.043.T61.REQ.14`: IPPartyDetails AP cardinality 1..1 (Capability A).
9. `P.SP.02.MSG.043.T61.REQ.15`: IPPartyDetails AP required fields (Capability A).
10. `P.SP.02.MSG.043.T61.REQ.21`: IPPartyDetails PA required fields (Capability A).
11. `P.SP.02.MSG.043.T61.REQ.22`: IPPartyDetails RE required fields (Capability A).
12. `P.SP.02.MSG.043.T61.REQ.23`: Correspondence address AddressKindCode "3" (Capability A).
13. `P.SP.02.MSG.043.T61.REQ.24`: Correspondence address UnifiedCountryCode IN member states (Capability A).
14. `P.SP.02.MSG.043.T61.REQ.25.CARD`: TrademarkDetails cardinality 1..1 (Capability A).
15. `P.SP.02.MSG.043.T61.REQ.25.DESC`: TMDescriptionDetails cardinality 1..1 (Capability A).
16. `P.SP.02.MSG.043.T61.REQ.25`: TrademarkDetails required fields (Capability A).
17. `P.SP.02.MSG.043.T61.REQ.26`: Inclusive OR across TrademarkKindCode and TrademarkKindName (Capability A + B).
18. `P.SP.02.MSG.043.T61.REQ.27`: Conditional presence of TrademarkPicture & TrademarkColourName (Capability A).
19. `P.SP.02.MSG.043.T61.REQ.28`: CollectiveMarkIndicator IN ["1", "0"] (Capability A).
20. `P.SP.02.MSG.043.T61.REQ.29.CARD`: GoodsBaseDetails cardinality min 1 (Capability A).
21. `P.SP.02.MSG.043.T61.REQ.29`: GoodsBaseDetails required fields (Capability A).
22. `P.SP.02.MSG.043.T61.REQ.30`: SourceTrademarkApplicationId matches TrademarkApplicationId of prior application (Capability C).
23. `P.SP.02.MSG.043.T61.REQ.32.ATTR`: CodeListId forbidden on StatusCode 02.
24. `P.SP.02.MSG.043.T61.REQ.32.ROLE01`: Allocated application (StatusCode 01) cardinality 1..1.
25. `P.SP.02.MSG.043.T61.REQ.32.ROLE02`: Prior application (StatusCode 02) cardinality 1..1.

## UNMAPPED_REQUIREMENTS
- **REQ 2–5, 31 (EXTERNAL):** Document-kind classifier resolution and national patent-office application database checks.
- **REQ 13 (AMBIGUOUS):** Ambiguous normative definition in isolation; IPPartyKindCode AP is enforced as part of requirement 14.
- **REQ 16–20 (ENGINE_UNSUPPORTED):** Require ordinal positional indexing of multiple repeated `IPSubjectName` instances within a repeatable parent, which is unsupported by the engine.

## PARENT_CONTEXT_SAFETY
- Tested that invalid children under Role A (`StatusCode == "02"`) do not cause rules governing Role B (`StatusCode == "01"`) to fail.
- Tested that multiple children under Role B are each evaluated.
- Verified no sibling cross-repair.

## ORDER_INDEPENDENCE
- Evaluated all 32 structured rules under physical order A/B (prior app then allocated app) and order B/A (allocated app then prior app). Both produce identical results (32 PASS).
- Roundtrip production testing confirms build -> serialize -> parse -> extract -> validate produces valid result in both physical XML orders.

## PRODUCTION_TESTS
Roundtrip executed via `EaeuXmlEngine`:
`build_body -> serialize_xml_element -> parse -> _values_from_element -> validate_body`
Result: valid for standard order and reversed order.

## MSG043_TESTS
Command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg043_*.py -p no:cacheprovider
```
Result: **33 passed in 0.63s**.
- `test_msg043_safe_mapping.py`: 13 passed
- `test_msg043_repeatable_xml.py`: 9 passed
- `test_msg043_end_to_end.py`: 11 passed

## ENGINE_VALIDATOR_REGRESSION
Command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider
```
Result: **40 passed, 5 subtests passed in 0.11s**.

Command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests -p no:cacheprovider
```
Result: **291 passed, 43 skipped, 1052 subtests passed in 2.92s**.

## FULL_OP22_REGRESSION
Command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests -p no:cacheprovider
```
Result: **2128 passed in 84.23s, 0 failed, 0 errors**.

## GIT_DIFF_CHECK
Command:
```bash
git diff --check
```
Clean. No whitespace or formatting issues.
Files modified by this task:
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.043.yaml`
- `P.SP.02_OP_22/tests/test_msg043_safe_mapping.py`
- `P.SP.02_OP_22/tests/test_msg043_repeatable_xml.py`
- `P.SP.02_OP_22/tests/test_msg043_end_to_end.py`
- `codex_reports/MSG043_REMEDIATION_REPORT.md`

Concurrent foreign files (MSG028 and shared files) were untouched.

## REMAINING_ISSUES
None.
