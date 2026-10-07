# OP26 / P.MM.01 — Negative Validation QA

Scope: functional QA of the local validator against canonical requirements from Decision of the EEC Board No. 68. No implementation files were modified.

## Result

- Negative test cases recorded: 10
- EXPECTED_REJECT_AND_REJECTED: 4
- UNEXPECTED_ACCEPTANCE: 4
- ENGINE_NOT_REACHED: 2
- CANNOT_TEST_MISSING_EVIDENCE: 0 recorded as executable mutations
- RUNTIME_ERROR: 0

## Unexpected acceptance 1 — empty required StartDateTime

Canonical requirement: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.003`.

Source: Decision of the EEC Board No. 68, PDF page 208, Table 18 item 3.

Requirement: `csdo:StartDateTime` must be filled.

Modified test XML: populated `StartDateTime` changed to an empty element; production extraction yields `None` at the existing path.

EXPECTED: REJECT. ACTUAL: ACCEPT.

Rule expected to catch it: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.003`.

Cause: shared REQUIRED-presence key-membership check.

Severity: HIGH.

## Unexpected acceptance 2 — DrugApplicationKindCode=TEST

Canonical requirement: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.005`.

Source: page 208, Table 18 item 5.

Allowed normative values: `01`, `02`, `03`, `04`, `99`.

Modified test XML/value: `DrugApplicationKindCode=TEST`.

EXPECTED: REJECT. ACTUAL in TEST validation mode: ACCEPT.

Rule expected to catch it: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.005`.

Cause: the executable structured rule explicitly accepts literal `TEST` in an OR branch before the normative allowlist. A control value `ZZ` is correctly rejected, showing this is a specific bypass in the rule data rather than a non-operational enum check.

Severity: HIGH.

## Unexpected acceptance 3 — CountryKindCode=TEST

Canonical requirement: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.008`.

Source: page 209, Table 18 item 8.

Allowed normative values: `01`, `02`.

Modified test XML/value: `CountryKindCode=TEST`.

EXPECTED: REJECT. ACTUAL in TEST validation mode: ACCEPT.

Rule expected to catch it: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.008`.

Cause: the executable structured rule explicitly accepts literal `TEST` in addition to the normative values. Control `ZZ` is rejected.

Severity: HIGH.

## Unexpected acceptance 4 — GUI validation of edited XML

Canonical requirement used for reproduction: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.003`, page 208, Table 18 item 3.

Reproduction:

1. Select OP26 / `P.MM.01.TRN.001` / `P.MM.01.MSG.001`.
2. Generate a baseline XML from valid controller values.
3. Edit only the XML and make `StartDateTime` empty.
4. Keep the controller/form values unchanged.
5. Run `GuiViewModel.validate()`.

EXPECTED: REJECT.

ACTUAL: GUI reports `Проверка пройдена`; only existing non-fatal classifier/version warnings remain.

Why it escaped:

- `XmlValidationService.validate()` checks XML parsing, SOAP envelope/header, Action and Body root QName, then returns; it does not run body business rules (`xml_validation_service.py:101-151`).
- `GuiViewModel.validate()` then calls `self.controller.validate()` (`view_model.py:298-312`).
- `controller.validate()` validates `controller.values`, not the edited XML text.
- `saveXml()` writes the current edited XML directly (`view_model.py:371-374`).

This establishes a user-facing validation defect: a body edit can violate a canonical requirement while the GUI validation summary remains successful.

Severity: CRITICAL because the local application can mark the edited XML as valid and the same XML can be saved/exported.

## Successful rejection controls

Direct TEST-mode production validation correctly rejected:

- missing `StartDateTime` (`REQ.003`);
- forbidden `EndDateTime` (`REQ.004`);
- `DrugApplicationKindCode=ZZ` (`REQ.005`);
- `CountryKindCode=ZZ` (`REQ.008`).

This distinction is important: absence is rejected, but an existing empty required scalar is accepted.

## STRICT-mode limitation

Both `TEST` enum cases were also submitted in STRICT mode. The business rule was not reached: validation returned `UNRESOLVED_STRUCTURE_VERSION`. They are classified `ENGINE_NOT_REACHED`, not as pass or reject for the enum requirement.

## Classifier limitation

The baseline OP26 validation emits `CLASSIFIER_DATASET_NOT_AVAILABLE`. No classifier-dependent negative case was invented without the required classifier payload.

## Traceability note

The canonical OP26 files still describe several `MSG.001` requirements as `OPEN_PRODUCTION_MAPPING`, although the current `message_rules/P.MM.01.MSG.001.yaml` contains executable structured rules for those IDs. Runtime conclusions here use canonical text as normative evidence and current runtime rules as implementation evidence; KB metadata was not changed.

## OP26 verdict

OP26 contains three distinct functional validation problems confirmed by this QA pass: the shared empty-required-element defect, explicit non-normative `TEST` enum allowances in TEST mode, and the GUI edited-XML/body-validation split.

