# IMPLEMENTATION REPORT: P.SP.02.MSG.015

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
1. `P.SP.02_OP_22/message_rules/P.SP.02.MSG.015.yaml` — Added 6 structured executable rule objects and exact mapping audit with 6 captured rows, 6 expanded requirements, classification counts, and provenance tracking.
2. `P.SP.02_OP_22/tests/test_msg015_safe_mapping.py` — Safe mapping tests verifying audit inventory, classification arithmetic, provenance, and structured rule properties.
3. `P.SP.02_OP_22/tests/test_msg015_repeatable_xml.py` — Repeatable XML and unit tests verifying per-record isolation, national application details presence and fields, status code and event date, end date-time, and extraction from real XML elements.
4. `P.SP.02_OP_22/tests/test_msg015_end_to_end.py` — Full pipeline tests (build -> serialize -> parse -> extract -> validate) covering roundtrip validation, negative cases, and message isolation.
5. `codex_reports/MSG015_IMPLEMENTATION_REPORT.md` — Authoritative final implementation report.

## IMPLEMENTATION
`P.SP.02.MSG.015` («Сведения о преобразовании аннулированной регистрации ТЗ Союза в национальную заявку на регистрацию ТЗ») is governed by structure `R.IP.SP.02.007 v1.0.0` (Root: `{urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}TrademarkRegisterDetails`).
Normative requirements are specified in Table 48 (ОП_22, physical pp. 559–560; 6 captured requirements, expanded into 6 discrete requirements).

- **REQ.1–2 (EXTERNAL)**: Mandate lookups against external unified classifier resources for document kind code or normative name. Preserved as non-executable (0 structured rules).
- **REQ.3 (SAFE_PARTIAL)**: Within each `ipcdo:UnifiedRegisterRecordsDetails` record, `ipsdo:TrademarkId` is REQUIRED. The external registry lookup for record status "04", populated `EndDateTime`, and matching `TrademarkId` remains non-executable remainder.
- **REQ.4 (FULLY_MAPPABLE)**: Within each `ipcdo:UnifiedRegisterRecordsDetails` record, `ipcdo:TrademarkNationalApplicationDetails` is REQUIRED (`.PRESENCE`). Within `ipcdo:TrademarkNationalApplicationDetails`, `csdo:UnifiedCountryCode`, `ipsdo:NationalApplicationId`, and `ipsdo:NationalApplicationReceiptDate` are REQUIRED (`.FIELDS`).
- **REQ.5 (FULLY_MAPPABLE)**: Within each `ipcdo:UnifiedRegisterRecordsDetails` record, `ipcdo:IPEntityStatusDetails` is REQUIRED (`.PRESENCE`). Within `ipcdo:IPEntityStatusDetails`, `csdo:StatusCode` must equal `"06"`, `csdo:EventDate` is REQUIRED, and `csdo:StatusCode/@codeListId` is FORBIDDEN (`.FIELDS`).
- **REQ.6 (FULLY_MAPPABLE)**: Within each `ipcdo:UnifiedRegisterRecordsDetails` record, `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime` is REQUIRED.

## MAPPING_COUNTS
- `captured_row_count`: 6
- `expanded_requirement_count`: 6
- `counts`:
  - `FULLY_MAPPABLE`: 3 (REQ 4, 5, 6)
  - `SAFE_PARTIAL`: 1 (REQ 3)
  - `EXTERNAL`: 2 (REQ 1, 2)
  - `ENGINE_UNSUPPORTED`: 0
  - `AMBIGUOUS`: 0
  - `SOURCE_CONFLICT`: 0
- Executable requirement set: `{3, 4, 5, 6}`
- Unmapped requirement set: `{1, 2}`
- Total structured rule objects: 6

## PARTIAL_REMAINDERS
- **REQ.3**: External Unified Register record lookup, verification of canceled status `"04"`, populated external `csdo:EndDateTime`, and `TrademarkId` equality against the external registry are non-executable remainder.

## UNMAPPED_REQUIREMENTS
- **REQ.1**: `EXTERNAL`. Look up document kind code in the unified classifier of IP document kinds.
- **REQ.2**: `EXTERNAL`. Look up document kind absence in the unified classifier and assign normative text name.

## OWNER_QNAME_SAFETY
- All rules are scoped to the repeated collection `ipcdo:UnifiedRegisterRecordsDetails` using exact QNames.
- National application details (`ipcdo:TrademarkNationalApplicationDetails`), entity status (`ipcdo:IPEntityStatusDetails`), and validity period (`ccdo:ValidityPeriodDetails`) are evaluated exclusively under their declared parent records.
- No descendant leakage, local-name fallback, or sibling repair.

## REPEATABLE_SAFETY
- Every per-record rule was tested under repeatable record scenarios:
  - good + good -> PASS
  - good + bad -> FAIL
  - bad + good -> FAIL
- Invalid fields in one record are not cured by valid values in sibling records.

## MESSAGE_ISOLATION
- MSG015 validation evaluates exclusively `P.SP.02.MSG.015.*` rules.
- Other messages using structure `R.IP.SP.02.007` (e.g. MSG046, MSG016–019, MSG053) remain completely isolated.

## NORMATIVE_BASIS
CONFIRMED:
- Direct: Table 48 (ОП_22.pdf, physical pp. 559–560, items 1–6).
- Structure: `R.IP.SP.02.007 v1.0.0` (ОП_22.pdf, Table 13, physical pp. 950–975).
- Transaction: `P.SP.02.TRN.013`, Procedure: `P.SP.02.PRC.023`, Initiating Operation: `P.SP.02.OPR.115`, Responding Operation: `P.SP.02.OPR.116`.

## MSG015_TESTS
- `P.SP.02_OP_22/tests/test_msg015_safe_mapping.py`: 7 passed
- `P.SP.02_OP_22/tests/test_msg015_repeatable_xml.py`: 8 passed
- `P.SP.02_OP_22/tests/test_msg015_end_to_end.py`: 6 passed
- Total: 21 passed, 0 failed in 1.27s.

Command:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg015_*.py -p no:cacheprovider
```

## FULL_OP22_REGRESSION
- Command:
  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests -p no:cacheprovider
  ```
- Summary: 2081 passed in 98.84s (0 failed, 0 errors).

## GIT_DIFF_CHECK
- Command:
  ```bash
  git diff --check
  ```
- Result: Clean (exit code 0).

## REMAINING_ISSUES
None
