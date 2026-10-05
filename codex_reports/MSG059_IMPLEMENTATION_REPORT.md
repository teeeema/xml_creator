# P.SP.02.MSG.059 IMPLEMENTATION REPORT

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.059.yaml`
- `P.SP.02_OP_22/tests/test_msg059_safe_mapping.py`
- `P.SP.02_OP_22/tests/test_msg059_repeatable_xml.py`
- `P.SP.02_OP_22/tests/test_msg059_end_to_end.py`
- `codex_reports/MSG059_IMPLEMENTATION_REPORT.md`

## NORMATIVE_INVENTORY
- **Authoritative Source**: Decision No. 22 (`ОП_22.pdf`), Sections 88, 89, 90, physical pages 810–812 (document pages 231–233).
- **Separate Rule Tables**:
  - Table 77: `R.010` generic document container (Item 1, p. 810).
  - Table 78: `R.IP.SP.02.002` v1.0.0 (`TrademarkRegistrationDetails`) (Items 1–5, pp. 810–811).
  - Table 79: `R.IP.SP.02.007` v1.0.0 (`TrademarkRegisterDetails`) (Items 1–5, p. 812).
- **Captured Table Rows**: 11 total
  - Table 77: 1 row (item 1)
  - Table 78: 5 rows (items 1, 2, 3, 4, 5)
  - Table 79: 5 rows (items 1, 2, 3, 4, 5)
- **Expanded Requirements**: 11 total
  - Table 77: Item 1 (`R.010`)
  - Table 78: Items 1, 2, 3, 4, 5 (`R.IP.SP.02.002`)
  - Table 79: Items 1, 2, 3, 4, 5 (`R.IP.SP.02.007`)

## STRUCTURE
- **Root Container**: `R.010` (active version `Y.Y.Y`), namespace `urn:EEC:R:GenericEDocDetails:vY.Y.Y`, root element `GenericEDocDetails`.
- **Embedded Structures**: Selection `ONE_OF` over:
  - `R.IP.SP.02.002` (version `1.0.0`), namespace `urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0`, root element `TrademarkRegistrationDetails`.
  - `R.IP.SP.02.007` (version `1.0.0`), namespace `urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0`, root element `TrademarkRegisterDetails`.
- **Transaction**: `P.SP.02.TRN.051` ("получение материалов и документов, используемых в ходе регистрации или иных процедур, связанных с ТЗ Союза").
- **Procedure**: `P.SP.02.PRC.036`.
- **Initiating Message**: `P.SP.02.MSG.058` (initiating operation `P.SP.02.OPR.186`).
- **Response Message**: `P.SP.02.MSG.059` (responding operation `P.SP.02.OPR.187`).
- **Direction**: `RESPONSE`.

## INHERITANCE
- None. Tables 77, 78, and 79 do not reference any parent or shared tables (no range rows like 6–29, no Table 44 inheritance). All requirements are direct.

## MAPPING_COUNTS
- **Captured Row Count**: 11
- **Expanded Requirement Count**: 11
- **Arithmetic Verification**: 7 + 2 + 0 + 2 + 0 + 0 = 11
  - `FULLY_MAPPABLE`: 7
  - `SAFE_PARTIAL`: 2
  - `EXTERNAL`: 0
  - `AMBIGUOUS`: 2
  - `ENGINE_UNSUPPORTED`: 0
  - `SOURCE_CONFLICT`: 0

## FULLY_MAPPABLE
- **Table 77 REQ 1** (`R.010`): Exactly one instance of `R.IP.SP.02.002` OR `R.IP.SP.02.007`. Enforced natively by existing embedded `ONE_OF` production infrastructure.
- **Table 78 REQ 1** (`R.IP.SP.02.002`): `ipsdo:TrademarkApplicationId` is REQUIRED inside `ipcdo:TrademarkApplicationDetails`.
- **Table 78 REQ 2** (`R.IP.SP.02.002`): `ipcdo:AccompanyingDocumentsDetails` is REQUIRED inside `ipcdo:TrademarkApplicationDetails`.
- **Table 78 REQ 3** (`R.IP.SP.02.002`): Within `ipcdo:AccompanyingDocumentsDetails`:
  - Inclusive OR: at least one of `ipsdo:IPDocKindCode` or `ipsdo:IPDocKindName` is REQUIRED (`kind: condition`, `condition.any`).
  - `csdo:DocName` is REQUIRED.
  - `csdo:DocId` is REQUIRED.
  - `csdo:DocCreationDate` is REQUIRED.
  - `csdo:DocBinaryText` is REQUIRED.
- **Table 79 REQ 1** (`R.IP.SP.02.007`): `ipsdo:TrademarkId` is REQUIRED inside `ipcdo:UnifiedRegisterRecordsDetails`.
- **Table 79 REQ 2** (`R.IP.SP.02.007`): `ipcdo:AccompanyingDocumentsDetails` is REQUIRED inside `ipcdo:UnifiedRegisterRecordsDetails`.
- **Table 79 REQ 3** (`R.IP.SP.02.007`): Within `ipcdo:AccompanyingDocumentsDetails`:
  - Inclusive OR: at least one of `ipsdo:IPDocKindCode` or `ipsdo:IPDocKindName` is REQUIRED (`kind: condition`, `condition.any`).
  - `csdo:DocName` is REQUIRED.
  - `csdo:DocId` is REQUIRED.
  - `csdo:DocCreationDate` is REQUIRED.
  - `csdo:DocBinaryText` is REQUIRED.

## SAFE_PARTIAL
- **Table 78 REQ 4** (`R.IP.SP.02.002`):
  - *Safe Fragment*: `csdo:DocBinaryText` presence REQUIRED, and `csdo:DocBinaryText/@mediaTypeCode` IN allowed list `['tif', 'tiff', 'bmp', 'jpg', 'jpeg', 'png', 'gif', 'doc', 'docx', 'rtf', 'pdf']`.
  - *Unmapped Remainder*: Binary payload decoded size <= 5 MB.
- **Table 79 REQ 4** (`R.IP.SP.02.007`):
  - *Safe Fragment*: `csdo:DocBinaryText` presence REQUIRED, and `csdo:DocBinaryText/@mediaTypeCode` IN allowed list `['tif', 'tiff', 'bmp', 'jpg', 'jpeg', 'png', 'gif', 'doc', 'docx', 'rtf', 'pdf']`.
  - *Unmapped Remainder*: Binary payload decoded size <= 5 MB.

## EXTERNAL
- None (0).

## AMBIGUOUS
- **Table 78 REQ 5** (`R.IP.SP.02.002`): "другие реквизиты не заполняются". The normative statement does not identify which elements or nesting levels constitute "other requisites" (e.g., fields within `AccompanyingDocumentsDetails`, within `TrademarkApplicationDetails`, or across `R.IP.SP.02.002`). Guessing the list of forbidden elements is prohibited. Also noted: engine lacks closed-world negative constraints (`CLOSED_WORLD_NEGATIVE_CONSTRAINTS_NOT_SUPPORTED`).
- **Table 79 REQ 5** (`R.IP.SP.02.007`): "другие реквизиты не заполняются". The normative statement does not identify which elements or nesting levels constitute "other requisites" (e.g., fields within `AccompanyingDocumentsDetails`, within `UnifiedRegisterRecordsDetails`, or across `R.IP.SP.02.007`). Guessing the list of forbidden elements is prohibited. Also noted: engine lacks closed-world negative constraints (`CLOSED_WORLD_NEGATIVE_CONSTRAINTS_NOT_SUPPORTED`).

## ENGINE_UNSUPPORTED
- None (0). (Closed-world constraint gap documented under AMBIGUOUS scope for REQ 5).

## SOURCE_CONFLICT
- None (0).

## EXECUTABLE_REQUIREMENTS
- `P.SP.02.MSG.059.T78.REQ.1`
- `P.SP.02.MSG.059.T78.REQ.2`
- `P.SP.02.MSG.059.T78.REQ.3`
- `P.SP.02.MSG.059.T78.REQ.4`
- `P.SP.02.MSG.059.T79.REQ.1`
- `P.SP.02.MSG.059.T79.REQ.2`
- `P.SP.02.MSG.059.T79.REQ.3`
- `P.SP.02.MSG.059.T79.REQ.4`
Plus Table 77 REQ 1 executed natively via `ONE_OF` container infrastructure.

## UNMAPPED_REQUIREMENTS
- Table 78 REQ 4 (remainder: binary payload decoded size <= 5 MB)
- Table 78 REQ 5 (ambiguous scope / unlisted other fields)
- Table 79 REQ 4 (remainder: binary payload decoded size <= 5 MB)
- Table 79 REQ 5 (ambiguous scope / unlisted other fields)

## IMPLEMENTATION
1. `P.SP.02_OP_22/message_rules/P.SP.02.MSG.059.yaml`:
   - Retained all 11 captured business rules from Tables 77, 78, 79.
   - Added 8 exact structured rules (4 under `R.IP.SP.02.002`, 4 under `R.IP.SP.02.007`).
   - Structured rules use `for_each` over `collection: "ipcdo:TrademarkApplicationDetails"`, `collection: "ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails"`, `collection: "ipcdo:UnifiedRegisterRecordsDetails"`, and `collection: "ipcdo:UnifiedRegisterRecordsDetails/ipcdo:AccompanyingDocumentsDetails"`.
   - Used `kind: "condition"` with recursive `any` for exact normative inclusive-OR semantics on IPDocKindCode / IPDocKindName.
   - Added complete `mapping_audit` with `counts`, `classification_counts`, `summary`, and 11-item `inventory`.

## OWNER_QNAME_SAFETY
- Every target path uses exact qualified names with confirmed namespace prefixes (`ipcdo:`, `ipsdo:`, `csdo:`, `ccdo:`).
- Element child containers and attributes (`@mediaTypeCode`) are resolved in the context of their respective collection selectors without global collision.

## REPEATABLE_RECORD_SAFETY
- Rules are evaluated inside `for_each` contexts bound to repeated parents (`TrademarkApplicationDetails`, `UnifiedRegisterRecordsDetails`) and nested repeatable documents (`AccompanyingDocumentsDetails`).
- Tested that invalid governed records fail and valid sibling records cannot repair them.
- Tested that order of records or child elements does not affect validation where order is non-normative.
- No positional indexing `[0]`/`[1]` is used.

## MESSAGE_ISOLATION
- All rules are strictly scoped by `rule_id` prefix `P.SP.02.MSG.059.` and `applies_to_structure`.
- When validating an `R.IP.SP.02.002` payload, zero rules from Table 79 (`R.IP.SP.02.007`) are evaluated.
- When validating an `R.IP.SP.02.007` payload, zero rules from Table 78 (`R.IP.SP.02.002`) are evaluated.
- Adjacent message MSG.058 was neither modified nor referenced as normative authority.

## NORMATIVE_BASIS
CONFIRMED — Decision No. 22 (`ОП_22.pdf`), Sections 88, 89, 90, Table 77 (p. 810), Table 78 (pp. 810–811), Table 79 (p. 812), Table 10 (pp. 840–928), and Table 15 (pp. 950–985).

## MSG059_TESTS
- `P.SP.02_OP_22/tests/test_msg059_safe_mapping.py`: 48 passed.
- `P.SP.02_OP_22/tests/test_msg059_repeatable_xml.py`: 22 passed.
- `P.SP.02_OP_22/tests/test_msg059_end_to_end.py`: 12 passed.
- **Total Scoped Tests**: 82 passed in 1.14s.

## ENGINE_VALIDATOR_REGRESSION
- `eaeu_xml/tests/test_structured_rules.py`
- `eaeu_xml/tests/test_process_package_validator.py`
- **Result**: 40 passed, 5 subtests passed in 0.12s.

## FULL_OP22_REGRESSION
- `P.SP.02_OP_22/tests`
- Starting baseline: 2173 passed.
- Result with MSG059: 2258 passed in 90.29s (2173 baseline + 82 MSG059 + 3 concurrent MSG058), 0 failed, 0 errors.

## GIT_DIFF_CHECK
- Run: `git diff --check`
- Result: 0 whitespace/conflict errors.
- Modified files strictly scoped to MSG059 ownership:
  - `P.SP.02_OP_22/message_rules/P.SP.02.MSG.059.yaml`
  - `P.SP.02_OP_22/tests/test_msg059_safe_mapping.py`
  - `P.SP.02_OP_22/tests/test_msg059_repeatable_xml.py`
  - `P.SP.02_OP_22/tests/test_msg059_end_to_end.py`
  - `codex_reports/MSG059_IMPLEMENTATION_REPORT.md`
- No concurrent MSG058 files were touched, reverted, stashed, or modified.

## REMAINING_ISSUES
None.
