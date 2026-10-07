# Independent Functional Validation Regression Audit Report

**Auditor Role:** Independent Functional Validation Regression Auditor  
**Inspection Mode:** READ ONLY  
**Project Root:** `/Users/tema/Documents/Work/xml_creator`  
**Report Directory:** `/Users/tema/Documents/Work/xml_creator/codex_reports/VALIDATION_RECHECK`  
**Target:** Independent functional reproduction and recheck of the 6 historically confirmed UNEXPECTED_ACCEPTANCE cases across 3 root defects.

---

## 1. Executive Summary

All 6 previously confirmed UNEXPECTED_ACCEPTANCE cases were independently reproduced and rechecked against the current workspace implementation. Existing tests were not trusted blindly; each scenario was executed with independent reproduction scripts directly against the active processing engines, structure extractors, rule evaluators, and the GUI ViewModel / editor buffer pipeline.

**Summary Verdict:**
- `OLD_UNEXPECTED_ACCEPTANCES:` 6
- `NOW_REJECTED:` 6
- `STILL_UNEXPECTED_ACCEPTANCE:` 0
- `CRITICAL_REMAINING:` 0
- `HIGH_REMAINING:` 0
- `PRODUCTION_CHANGED:` 0
- `TESTS_CHANGED:` 0
- `KB_CHANGED:` 0

---

## 2. Check 1 — Shared REQUIRED Presence Semantics

### Root Defect 1 Background
Previously, `StructuredRuleEvaluator` evaluated `presence: REQUIRED` based solely on dictionary key existence. When an XML scalar element was present but empty (e.g., `<csdo:UpdateDateTime/>`), the XML extractor populated the dictionary key with `None`. Because the key was present, the REQUIRED rule erroneously passed.

### Recheck Methodology & Results
Representative scalar leaf elements were tested with 4 distinct states:
1. `missing element` (key completely absent)
2. `empty element` (`<element/>` or empty text `""`, extracted as `None`)
3. `whitespace-only element` (`"   \t\n"`, whitespace text)
4. `valid non-empty element` (canonical valid value)

#### Case OP22 (UA-01, Case OP22-02)
- **Message:** `P.SP.02.MSG.024`
- **Canonical Requirement:** `P.SP.02.MSG.024:56:1` (`ОП_22.pdf`, p. 577, Table 56 item 1)
- **Target Field:** `csdo:UpdateDateTime`
- **Rule ID:** `P.SP.02.MSG.024.T56.REQ.1`
- **Observed Behavior:**
  - Missing element: `RuleStatus.FAIL`, `is_valid: False` (REJECTED)
  - Empty element (`<csdo:UpdateDateTime/>`): `RuleStatus.FAIL`, `is_valid: False` (REJECTED)
  - Whitespace-only (`"   \t\n"`): `RuleStatus.FAIL`, `is_valid: False` (REJECTED)
  - Valid non-empty (`"2026-09-24T12:01:00+03:00"`): `RuleStatus.PASS`, `is_valid: True` (ACCEPTED)
- **Status:** **NOW_REJECTED**

#### Case OP23 (UA-02, Case OP23-01)
- **Message:** `P.SP.03.MSG.001`
- **Canonical Requirement:** `P.SP.03.MSG.001.REQ.010` (`ОП_23.pdf`, p. 342, Table 16 item 10)
- **Target Field:** `ipcdo:ApellationOfOriginApplicationDetails/csdo:DocId`
- **Rule ID:** `P.SP.03.MSG.001.REQ.010`
- **Observed Behavior:**
  - Missing element: `RuleStatus.FAIL` (REJECTED)
  - Empty element (`<csdo:DocId/>`): `RuleStatus.FAIL` (REJECTED)
  - Whitespace-only (`"   \t\n"`): `RuleStatus.FAIL` (REJECTED)
  - Valid non-empty (`"12345"`): `RuleStatus.PASS` (ACCEPTED)
- **Status:** **NOW_REJECTED**

#### Case OP26 (UA-03, Case OP26-02)
- **Message:** `P.MM.01.MSG.001`
- **Canonical Requirement:** `OP26.P_MM_01.P.MM.01.MSG.001.REQ.003` (Decision No. 68, p. 208, Table 18 item 3)
- **Target Field:** `DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime`
- **Rule ID:** `OP26.P_MM_01.P.MM.01.MSG.001.REQ.003`
- **Observed Behavior:**
  - Missing element: `RuleStatus.FAIL` (REJECTED)
  - Empty element (`<csdo:StartDateTime/>` / `None`): `RuleStatus.FAIL` (REJECTED)
  - Whitespace-only (`"   \t\n"`): `RuleStatus.FAIL` (REJECTED)
  - Valid non-empty (`"2026-10-07T12:00:00+03:00"`): `RuleStatus.PASS` (ACCEPTED)
- **Status:** **NOW_REJECTED**

---

## 3. Check 2 — OP26 TEST Mode Validation Bypass

### Root Defect 2 Background
Previously, in `P.MM.01_OP_26/message_rules/P.MM.01.MSG.001.yaml`, executable rules for `DrugApplicationKindCode` (REQ.005) and `CountryKindCode` (REQ.008) contained an explicit `#text == TEST` allowlist branch. This allowed test-generator placeholder values to pass validation, effectively bypassing normative enumerations in TEST mode.

### Recheck Methodology & Results
- Verified that the rules in `P.MM.01.MSG.001.yaml` contain only the normative allowed values:
  - REQ.005 allowed: `['01', '02', '03', '04', '99']` (Decision No. 68, Table 18 item 5)
  - REQ.008 allowed: `['01', '02']` (Decision No. 68, Table 18 item 8)
- Evaluated body validation in `GenerationMode.TEST` when passing `TEST`:

#### Case OP26 DrugApplicationKindCode = TEST (UA-04, Case OP26-05)
- **Tested Value:** `DrugApplicationKindCode = "TEST"`
- **Observed Status for REQ.005:** `RuleStatus.FAIL`
- **Body Validation Result:** `is_valid: False`
- **Normative Values Verification:** Values `'01'`, `'02'`, `'03'`, `'04'`, `'99'` evaluated to `RuleStatus.PASS`.
- **Status:** **NOW_REJECTED**

#### Case OP26 CountryKindCode = TEST (UA-05, Case OP26-07)
- **Tested Value:** `CountryKindCode = "TEST"`
- **Observed Status for REQ.008:** `RuleStatus.FAIL`
- **Body Validation Result:** `is_valid: False`
- **Normative Values Verification:** Values `'01'`, `'02'` evaluated to `RuleStatus.PASS`.
- **Status:** **NOW_REJECTED**

`TEST` mode does not bypass validation. Non-normative placeholder values are strictly rejected.

---

## 4. Check 3 — GUI Stale XML State & Current Editor Buffer Validation

### Root Defect 3 Background
Previously, when a valid XML was generated and passed validation in the GUI, editing the visible XML in the editor buffer did not invalidate the validation result. Furthermore, calling `Validate` re-ran business rules against the old `controller.values` form state instead of parsing the modified XML text. This resulted in a false `"Проверка пройдена"` for an invalid XML.

### Recheck Methodology & 8-Step Verification
The complete 8-step verification cycle was tested directly with `GuiViewModel` as well as the native editor widget (`NativeXmlEditor` / `NativeXmlEditorBinding`):

1. **Step 1 — Valid XML:** Generated valid XML for `P.MM.01.MSG.001` (`length = 3376` chars).
2. **Step 2 — Validate PASS:** Executed `model.validate()`. Result: `validationSummary == "Проверка пройдена"`, `controller.validation.is_valid == True`.
3. **Step 3 — Manually edit visible XML:** Replaced text in the editor buffer via document text edit / `setXml`.
4. **Step 4 — Make required StartDateTime empty:** Changed `<csdo:StartDateTime>...</csdo:StartDateTime>` to `<csdo:StartDateTime/>`.
5. **Step 5 — Check stale result invalidation:**
   - Immediately upon text change / buffer flush, `model.validationSummary` transitions to `"Проверка ещё не выполнялась."`.
   - `model.controller.validation` is cleared to `None`.
6. **Step 6 — Validate:** Called `model.validate()`.
7. **Step 7 — Actual current XML must FAIL:**
   - `XmlValidationService` parsed the current XML and extracted body values (`StartDateTime` extracted as `None`).
   - `controller.set_values()` synchronized form values from the exact current XML buffer.
   - Business validation ran and flagged `OP26.P_MM_01.P.MM.01.MSG.001.REQ.003` as `FAIL`.
   - `model.validationSummary` displayed `"Ошибки: 1 · Предупреждения: 2"`.
   - `model.controller.validation.is_valid == False`.
8. **Step 8 — Save must not rely on PASS for previous snapshot:**
   - Saved XML via `binding.saveXml(path)` and `model.saveXml(path)`.
   - Output file was inspected: contains empty `<csdo:StartDateTime/>`.
   - `model.validationSummary` remains invalid (`!= "Проверка пройдена"`).

- **Status:** **NOW_REJECTED**

---

## 5. Summary Matrix of Rechecked Cases

| UA ID | Case ID | OP | Process | Message | Target Requirement | Test Mutation | Old Actual | Recheck Actual | Status | Severity |
|---|---|---|---|---|---|---|---|---|---|---|
| UA-01 | OP22-02 | OP22 | P.SP.02 | P.SP.02.MSG.024 | P.SP.02.MSG.024:56:1 | Empty `<csdo:UpdateDateTime/>` | ACCEPT | REJECT | NOW_REJECTED | HIGH |
| UA-02 | OP23-01 | OP23 | P.SP.03 | P.SP.03.MSG.001 | P.SP.03.MSG.001.REQ.010 | Empty `<csdo:DocId/>` | ACCEPT | REJECT | NOW_REJECTED | HIGH |
| UA-03 | OP26-02 | OP26 | P.MM.01 | P.MM.01.MSG.001 | REQ.003 (Table 18 item 3) | Empty `<csdo:StartDateTime/>` | ACCEPT | REJECT | NOW_REJECTED | HIGH |
| UA-04 | OP26-05 | OP26 | P.MM.01 | P.MM.01.MSG.001 | REQ.005 (Table 18 item 5) | `DrugApplicationKindCode = "TEST"` | ACCEPT | REJECT | NOW_REJECTED | HIGH |
| UA-05 | OP26-07 | OP26 | P.MM.01 | P.MM.01.MSG.001 | REQ.008 (Table 18 item 8) | `CountryKindCode = "TEST"` | ACCEPT | REJECT | NOW_REJECTED | HIGH |
| UA-06 | OP26-10 | OP26 | P.MM.01 | P.MM.01.MSG.001 | REQ.003 (Table 18 item 3) | Manual empty edit in editor buffer | ACCEPT | REJECT | NOW_REJECTED | CRITICAL |

---

## 6. Audit Conclusion & Compliance Check

The functional validation regression audit confirmed:
1. All 3 underlying root defects are completely resolved in the current workspace.
2. No unexpected acceptances remain among the rechecked cases.
3. No security terminology was used in reporting.
4. No production code, tests, or knowledge base entries were modified during this audit (`READ ONLY` policy strictly respected).
