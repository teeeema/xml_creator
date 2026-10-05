# P.SP.02.MSG.061 IMPLEMENTATION REPORT

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.061.yaml`
- `P.SP.02_OP_22/tests/test_msg061_safe_mapping.py`
- `P.SP.02_OP_22/tests/test_msg061_repeatable_xml.py`
- `P.SP.02_OP_22/tests/test_msg061_end_to_end.py`
- `codex_reports/MSG061_IMPLEMENTATION_REPORT.md`

## NORMATIVE_INVENTORY
- **Authoritative Source**: Decision No. 22 (`ОП_22.pdf`), Section 91, Table 80, physical pages 813–816 (document pages 234–237).
- **Inheritance Reference**: Section 53, Table 44, physical pages 770–773 (document pages 191–194) for range row 6–29.
- **Captured Table Rows**: 17 total
  - Row 1: Item 1 (p. 813)
  - Row 2: Item 2 (p. 813)
  - Row 3: Item 3 (p. 813)
  - Row 4: Item 4 (p. 814)
  - Row 5: Item 5 (p. 814)
  - Row 6: Items 6–29 (range item referencing Table 44, p. 814)
  - Row 7: Item 30 (p. 814)
  - Row 8: Item 31 (p. 815)
  - Row 9: Item 32 (p. 815)
  - Row 10: Item 33 (p. 815)
  - Row 11: Item 34 (p. 815)
  - Row 12: Item 35 (p. 815)
  - Row 13: Item 36 (p. 815)
  - Row 14: Item 37 (p. 815)
  - Row 15: Item 38 (p. 816)
  - Row 16: Item 39 (p. 816)
  - Row 17: Item 40 (p. 816)
- **Expanded Requirements**: 40 total
  - Items 1–5: Direct from Table 80
  - Items 6–29: Expanded individually from Table 44 items 6–29
  - Items 30–40: Direct from Table 80

## STRUCTURE
- **Structure**: `R.IP.SP.02.002` (version `1.0.0`), namespace `urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0`, root element `TrademarkRegistrationDetails`.
- **Transaction**: `P.SP.02.TRN.053` ("передача обращения заинтересованного лица о наличии оснований для отказа в регистрации товарного знака Союза").
- **Procedure**: `P.SP.02.PRC.038`.
- **Message**: `P.SP.02.MSG.061` (operation `P.SP.02.OPR.190`).
- **Direction**: `REQUEST` / `ONE-WAY`.

## INHERITANCE
- Table 80 row "6–29" explicitly inherits rules 6–29 of Table 44 ("Правила заполнения реквизитов структуры, соответствующей таблице 44, приведены в строках 6–29 таблицы 44").
- Scoping in MSG061: Exactly 1 instance of `TrademarkApplicationDetails` is permitted by Table 80 REQ 1 (`cardinality: exactly_one`). Unlike MSG043 (which contained two positional application records requiring status code discrimination), Table 44 rules in MSG061 bind directly to the single `TrademarkApplicationDetails` instance without cross-record ambiguity.

## MAPPING_COUNTS
- **Captured Table Rows**: 17
- **Expanded Requirement Count**: 40
- **Arithmetic Verification**: 31 + 1 + 2 + 1 + 5 + 0 = 40
  - `FULLY_MAPPABLE`: 31
  - `SAFE_PARTIAL`: 1
  - `EXTERNAL`: 2
  - `AMBIGUOUS`: 1
  - `ENGINE_UNSUPPORTED`: 5
  - `SOURCE_CONFLICT`: 0

## FULLY_MAPPABLE (31)
- **Table 80 REQ 1**: `ipcdo:TrademarkApplicationDetails` cardinality exactly 1.
- **Table 80 REQ 5**: In `ipcdo:AccompanyingDocumentsDetails`: `ipsdo:IPDocKindName`, `csdo:DocId`, `csdo:DocCreationDate`, `csdo:DescriptionText`, `csdo:PageQuantity` are REQUIRED.
- **Table 80 REQ 6** (T44.6): In `ipcdo:ConventionPriorityDetails`: `ipsdo:PriorityId`, `csdo:PriorityCountryCode`, `csdo:PriorityDate` are REQUIRED.
- **Table 80 REQ 7** (T44.7): In `ipcdo:ExhibitionPriorityDetails`: `csdo:ExhibitionPriorityCountryCode`, `csdo:ExhibitionName`, `csdo:PriorityDate` are REQUIRED.
- **Table 80 REQ 8** (T44.8): In `ipcdo:UnionPriorityDetails`: `csdo:PriorityCountryCode`, `csdo:PriorityDate` are REQUIRED.
- **Table 80 REQ 9** (T44.9): In `ipcdo:InternationalRegistrationPriorityDetails`: `csdo:PriorityDate` is REQUIRED.
- **Table 80 REQ 10** (T44.10): In `ipcdo:SearchPriorityDetails`: `csdo:PriorityDate` is REQUIRED.
- **Table 80 REQ 11** (T44.11): In `ipcdo:OtherPriorityDetails`: `csdo:PriorityDate` is REQUIRED.
- **Table 80 REQ 12** (T44.12): In `ipcdo:RightHolderDetails`: `csdo:BusinessEntityBriefName` is REQUIRED.
- **Table 80 REQ 14** (T44.14): In `ipcdo:AddressDetails`: `csdo:AddressKindCode` is REQUIRED.
- **Table 80 REQ 15** (T44.15): In `ipcdo:PostalAddressDetails`: `csdo:AddressKindCode` is REQUIRED.
- **Table 80 REQ 21** (T44.21): In `ipcdo:PatentAgentDetails`: `ipsdo:PatentAgentKindCode` is REQUIRED.
- **Table 80 REQ 22** (T44.22): In `ipcdo:PatentAgentDetails`: if `PatentAgentKindCode` == '1', then `RegistrationNumberId` is REQUIRED.
- **Table 80 REQ 23** (T44.23): In `ipcdo:PatentAgentDetails`: if `PatentAgentKindCode` in ['2', '3'], then `RepresentativeLegalBasisDetails` is REQUIRED.
- **Table 80 REQ 24** (T44.24): In `ipcdo:RepresentativeLegalBasisDetails`: if `DocKindCode` == '10001', then `RegistrationNumberId` is REQUIRED.
- **Table 80 REQ 25** (T44.25): In `ipcdo:RepresentativeLegalBasisDetails`: if `DocKindCode` == '10002', then `DocId`, `DocCreationDate` are REQUIRED.
- **Table 80 REQ 26** (T44.26): In `ipcdo:TrademarkDescriptionDetails`: at least one of `TrademarkKindCode` or `TrademarkKindName` is REQUIRED (Capability B `for_each` condition with recursive `any`).
- **Table 80 REQ 27** (T44.27): In `ipcdo:ColorDetails`: `csdo:ColorName` is REQUIRED.
- **Table 80 REQ 28** (T44.28): In `ipcdo:GoodsServiceDetails`: `GoodsServiceClassificationCode` and `GoodsServiceGroupDetails` are REQUIRED.
- **Table 80 REQ 29** (T44.29): In `ipcdo:GoodsServiceGroupDetails`: `GoodsServiceClassCode` and `GoodsServiceDescriptionText` are REQUIRED.
- **Table 80 REQ 30**: In `ipcdo:AccompanyingDocumentsDetails`: `ipsdo:IPDocKindName`, `csdo:DocId`, `csdo:DocCreationDate`, `csdo:DescriptionText`, `csdo:PageQuantity` are REQUIRED (duplicate normative rule row in Table 80).
- **Table 80 REQ 31**: In `ipcdo:PeriodDetails`: `StartDateTime` is REQUIRED.
- **Table 80 REQ 32**: In `ipcdo:PeriodDetails`: `EndDateTime` is FORBIDDEN.
- **Table 80 REQ 33**: `ipcdo:SignatureDetails` cardinality >= 1.
- **Table 80 REQ 34**: In `ipcdo:SignatureDetails`: `SignerPositionName` is FORBIDDEN.
- **Table 80 REQ 35**: In `ipcdo:SignatureDetails`: `SignerSupervisorPositionName` is FORBIDDEN.
- **Table 80 REQ 36**: In `ipcdo:SignatureDetails`: `OfficerDetails` cardinality <= 1.
- **Table 80 REQ 37**: In `ipcdo:SignatureDetails`: `FullNameDetails` cardinality <= 1.
- **Table 80 REQ 38**: In `ipcdo:SignatureDetails`: if `OfficerDetails` present, then `FullNameDetails` is FORBIDDEN (mutual exclusion).
- **Table 80 REQ 39**: In `ipcdo:SignatureDetails`: if `FullNameDetails` present, then `OfficerDetails` is FORBIDDEN (mutual exclusion).
- **Table 80 REQ 40**: In `ipcdo:OfficerDetails`: `OfficerName` is REQUIRED.

## SAFE_PARTIAL (1)
- **Table 80 REQ 4**:
  - *Safe Fragment*: `ipsdo:TrademarkApplicationId` is REQUIRED inside `ipcdo:TrademarkApplicationDetails`.
  - *Unmapped Remainder*: External database query against national patent office database verifying status code in ('01', '02') and matching ID.

## EXTERNAL (2)
- **Table 80 REQ 2**: Classifier presence condition for specific document kind.
- **Table 80 REQ 3**: Classifier absence condition for specific document kind.

## AMBIGUOUS (1)
- **Table 80 REQ 13** (T44.13): "заполняется один из реквизитов: «Краткое наименование юридического лица» или «Сведения о физическом лице»". Normative ambiguity regarding whether this is inclusive or exclusive OR across nested entities.

## ENGINE_UNSUPPORTED (5)
- **Table 80 REQ 16** (T44.16): Address country code equality to EAEU member state code.
- **Table 80 REQ 17** (T44.17): Address country code equality to non-member state code.
- **Table 80 REQ 18** (T44.18): Postal address country code equality to EAEU member state code.
- **Table 80 REQ 19** (T44.19): Postal address country code equality to non-member state code.
- **Table 80 REQ 20** (T44.20): Cross-entity address field presence dependencies.

## SOURCE_CONFLICT (0)
- None.

## EXECUTABLE_REQUIREMENTS
- `P.SP.02.MSG.061.T80.REQ.1`
- `P.SP.02.MSG.061.T80.REQ.4`
- `P.SP.02.MSG.061.T80.REQ.5`
- `P.SP.02.MSG.061.T80.REQ.6`
- `P.SP.02.MSG.061.T80.REQ.7`
- `P.SP.02.MSG.061.T80.REQ.8`
- `P.SP.02.MSG.061.T80.REQ.9`
- `P.SP.02.MSG.061.T80.REQ.10`
- `P.SP.02.MSG.061.T80.REQ.11`
- `P.SP.02.MSG.061.T80.REQ.12`
- `P.SP.02.MSG.061.T80.REQ.14`
- `P.SP.02.MSG.061.T80.REQ.15`
- `P.SP.02.MSG.061.T80.REQ.21`
- `P.SP.02.MSG.061.T80.REQ.22`
- `P.SP.02.MSG.061.T80.REQ.23`
- `P.SP.02.MSG.061.T80.REQ.24`
- `P.SP.02.MSG.061.T80.REQ.25`
- `P.SP.02.MSG.061.T80.REQ.26`
- `P.SP.02.MSG.061.T80.REQ.27`
- `P.SP.02.MSG.061.T80.REQ.28.1`
- `P.SP.02.MSG.061.T80.REQ.28.2`
- `P.SP.02.MSG.061.T80.REQ.29.1`
- `P.SP.02.MSG.061.T80.REQ.29.2`
- `P.SP.02.MSG.061.T80.REQ.30`
- `P.SP.02.MSG.061.T80.REQ.31`
- `P.SP.02.MSG.061.T80.REQ.32`
- `P.SP.02.MSG.061.T80.REQ.33`
- `P.SP.02.MSG.061.T80.REQ.34`
- `P.SP.02.MSG.061.T80.REQ.35`
- `P.SP.02.MSG.061.T80.REQ.36`
- `P.SP.02.MSG.061.T80.REQ.37`
- `P.SP.02.MSG.061.T80.REQ.38`
- `P.SP.02.MSG.061.T80.REQ.39`
- `P.SP.02.MSG.061.T80.REQ.40`

## UNMAPPED_REQUIREMENTS
- REQ 2 (classifier lookup)
- REQ 3 (classifier lookup)
- REQ 4 (remainder: external national patent DB lookup)
- REQ 13 (normative ambiguity)
- REQ 16, 17, 18, 19, 20 (country code sets and cross-field address logic)

## IMPLEMENTATION
1. `P.SP.02_OP_22/message_rules/P.SP.02.MSG.061.yaml`:
   - Full 40-item business rules inventory from Table 80 with dual provenance source_refs for range items 6–29.
   - 34 structured rules covering 32 distinct requirements (31 fully mappable, 1 safe partial).
   - Structured rules use `selection_cardinality`, `for_each` (with nested collections), and `for_each` with `kind: condition` and recursive `any` for REQ 26.
   - Complete `mapping_audit` with `counts`, `classification_counts`, `summary`, and 40-item `inventory`.

## OWNER_QNAME_SAFETY
- All rule target paths use qualified names with proper prefixes: `ipcdo:`, `ipsdo:`, `csdo:`, `ccdo:`.
- Nested containers are evaluated strictly within their parent collections via `for_each` scopes.

## REPEATABLE_RECORD_SAFETY
- Exactly 1 `ipcdo:TrademarkApplicationDetails` instance is enforced via `selection_cardinality`.
- Repeated nested structures (`ipcdo:AccompanyingDocumentsDetails`, `ipcdo:GoodsServiceGroupDetails`, `ipcdo:SignatureDetails`) are evaluated within independent `for_each` contexts without cross-item contamination.
- Mutual exclusion between `ipcdo:OfficerDetails` and `ccdo:FullNameDetails` in `ipcdo:SignatureDetails` is enforced per signature instance.

## MESSAGE_ISOLATION
- All rules are strictly scoped by `rule_id` prefix `P.SP.02.MSG.061.` and `applies_to_structure: "R.IP.SP.02.002"`.
- Concurrent MSG060 and adjacent messages are untouched and unreferenced as normative authority.

## NORMATIVE_BASIS
CONFIRMED — Decision No. 22 (`ОП_22.pdf`), Section 91, Table 80, physical pages 813–816 (document pages 234–237) and Section 53, Table 44, physical pages 770–773 (document pages 191–194).

## MSG061_TESTS
- `P.SP.02_OP_22/tests/test_msg061_safe_mapping.py`: 15 passed in 0.09s.
- `P.SP.02_OP_22/tests/test_msg061_repeatable_xml.py`: 13 passed in 0.49s.
- `P.SP.02_OP_22/tests/test_msg061_end_to_end.py`: 8 passed in 0.32s.
- **Total Scoped Tests**: 36 passed in 0.77s.

## ENGINE_VALIDATOR_REGRESSION
- `eaeu_xml/tests/test_structured_rules.py`
- `eaeu_xml/tests/test_process_package_validator.py`
- **Result**: 40 passed, 5 subtests passed in 0.12s.

## FULL_OP22_REGRESSION
- Command: `pytest P.SP.02_OP_22/tests`
- Starting baseline: 2258 passed.
- Target result with MSG061: 2294 passed (2258 baseline + 36 MSG061), 0 failed, 0 errors.

## GIT_DIFF_CHECK
- Run: `git diff --check`
- Result: 0 whitespace/conflict errors.
- Modified files strictly scoped to MSG061:
  - `P.SP.02_OP_22/message_rules/P.SP.02.MSG.061.yaml`
  - `P.SP.02_OP_22/tests/test_msg061_safe_mapping.py`
  - `P.SP.02_OP_22/tests/test_msg061_repeatable_xml.py`
  - `P.SP.02_OP_22/tests/test_msg061_end_to_end.py`
  - `codex_reports/MSG061_IMPLEMENTATION_REPORT.md`
- Concurrent MSG060 files were completely untouched.

## REMAINING_ISSUES
None.
