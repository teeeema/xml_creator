# WAVE 1 / AGENT B — Validation fixes root cause

## STATUS

The three confirmed WAVE 1 functional validation defects are fixed.

Knowledge Base and normative source files were not modified.

## DEFECT 1 — REQUIRED empty value

### ROOT_CAUSE

`StructuredRuleEvaluator` treated `presence: REQUIRED` primarily as structural/key presence. A scalar XML element could therefore satisfy a REQUIRED rule even when its extracted value was `None`, an empty string, or whitespace in paths where normative semantics require a filled value.

A blanket "all empty elements are invalid" rule would be incorrect because complex XML containers use structural presence semantics and their child requirements are validated separately.

### FIX

The evaluator now distinguishes scalar and complex element semantics using the active `StructureDefinition`:

- scalar leaf REQUIRED targets must contain a non-empty value;
- whitespace-only scalar values are empty;
- repeated scalar lists containing only empty values are empty;
- scalar attributes do not make empty element text filled;
- complex REQUIRED targets use structural container presence;
- missing complex containers are not reconstructed from orphan descendant keys;
- FORBIDDEN remains structural presence semantics.

`StructuredProcessBodyProvider` supplies the evaluator with the set of complex paths derived from element descendants in the active structure, including the selected embedded structure when applicable.

### REGRESSION COVERAGE

- OP22: empty REQUIRED `UpdateDateTime` is rejected.
- OP23: empty REQUIRED `DocId` is rejected.
- OP26: empty REQUIRED `StartDateTime` is rejected.
- Shared evaluator coverage includes `None`, empty text, whitespace, repeated empty scalar values, complex containers, and FORBIDDEN behavior.

## DEFECT 2 — OP26 TEST semantics

### ROOT_CAUSE

The OP26 executable rules for `DrugApplicationKindCode` and `CountryKindCode` explicitly accepted the literal `TEST`. This made TEST generation behavior part of normative validation and allowed non-normative values through the validator.

Separately, test-data helpers defaulted many values to `TEST`, so removing the validator bypass required generation to choose an already-confirmed executable-rule literal instead.

### FIX

- Removed the `TEST` acceptance branch from OP26 MSG.001 REQ.005 (`DrugApplicationKindCode`).
- Removed the `TEST` acceptance branch from OP26 MSG.001 REQ.008 (`CountryKindCode`).
- Shared test-data generation selects a known literal from an executable `IN` rule when available.
- Conditional REQUIRED values activated by that choice are materialized using their own executable rule literals.
- The OP26 all-transactions test matrix uses the same generic principle rather than preserving `TEST` as a validator bypass.

### NORMATIVE BASIS

CONFIRMED from existing project mappings; no new normative facts were introduced:

- `P.MM.01.MSG.001.R5` / REQ.005 — `SRC-PMM01-068`, Decision No. 68, table 18, item 5, P.MM.01 1.1.0. Allowed values: `01`, `02`, `03`, `04`, `99`.
- `P.MM.01.MSG.001.R8` / REQ.008 — `SRC-PMM01-068`, Decision No. 68, table 18, item 8, page 209, P.MM.01 1.1.0. Allowed values: `01`, `02`.
- The dependent generated `RegistrationKindCode` is based on existing REQ.019/REQ.020 mappings, Decision No. 68, table 18, items 19-20, page 211.

## DEFECT 3 — GUI stale values

### ROOT_CAUSE

The XML editor buffer and `controller.values` could diverge after manual editing. `Validate` structurally checked the current XML text, then ran business rules against the older controller values. A previously valid generated snapshot could therefore remain displayed as PASS after the visible XML changed.

### FIX

- `XmlValidationService` reuses the existing body extractor and returns values extracted from the current serialized XML body.
- `GuiViewModel.validate()` first validates the current editor XML, then synchronizes controller values from that exact XML snapshot before business-rule validation.
- Any editor XML change invalidates the previous validation result immediately.
- Changing validation mode also invalidates the previous result.
- Formatting routes through `setXml()`, so formatting cannot retain stale validation state.
- Saving continues to use the current editor XML text.

### REGRESSION COVERAGE

The GUI regression verifies:

1. generated XML validates as PASS;
2. manual edit makes required `StartDateTime` empty;
3. old PASS is invalidated immediately;
4. Validate evaluates the edited XML and returns FAIL;
5. a valid manual edit can validate as PASS after resynchronization.

## ARCHITECTURAL RESULT

The fixes are shared-layer fixes. No process/message-specific validation exception was added. The only normative production configuration change is removal of the two confirmed OP26 `TEST` bypass branches.

