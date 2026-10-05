# Process Package Validator Capability Registration Report for MSG012

## STATUS
COMPLETE

## VERDICT
READY

## ROOT_CAUSE
The process package validator (`ProcessPackageValidator` in `eaeu_xml/src/eaeu_xml/process_packages/validator.py`) maintained whitelist sets of supported structured rule kinds (`STRUCTURED_RULE_KINDS`) and assertion kinds (`FOR_EACH_ASSERTION_KINDS`). While the underlying rules engine (`StructuredRuleEvaluator`) had already been extended with Capability B (`condition` assertion) and Capability C (`cross_instance_comparison`), `ProcessPackageValidator` had not been synchronized with these two capabilities.
As a result, any package manifest containing `kind: cross_instance_comparison` or `for_each` assertions with `kind: condition` was rejected by `ProcessPackageValidator.validate()` during `ProcessPackageLoader.load()` with `UNKNOWN_STRUCTURED_RULE_KIND` before evaluation could take place.

## CHANGED_FILES
- `eaeu_xml/src/eaeu_xml/process_packages/validator.py` — registered `"cross_instance_comparison"` in `STRUCTURED_RULE_KINDS` with operator/operand validation; registered `"condition"` in `FOR_EACH_ASSERTION_KINDS` with recursive condition validation.
- `eaeu_xml/tests/test_process_package_validator.py` — created focused validator unit and loader integration tests covering valid forms, unknown kinds rejection, invalid shapes rejection, and real `ProcessPackageLoader -> ProcessPackageValidator` package loading.
- `codex_reports/MSG012_VALIDATOR_CAPABILITY_REPORT.md` — this authoritative report.

All other files (including `rules_engine.py`, `P.SP.02_OP_22/message_rules/P.SP.02.MSG.012.yaml`, and `test_msg012_*.py`) remained strictly unmodified and READ-ONLY.

## VALIDATOR_CHANGES
1. **Rule Kinds Whitelist Update:**
   - Added `"cross_instance_comparison"` to `STRUCTURED_RULE_KINDS`.
   - Added `"condition"` to `FOR_EACH_ASSERTION_KINDS`.
2. **Top-Level `cross_instance_comparison` Validation:**
   - Validates operator against `STRUCTURED_RULE_OPERATORS` (`EQ`, `NE`, `GT`, `GE`, `LT`, `LE`, `IN`, `NOT_IN`).
   - Validates both `left` and `right` operands as Mappings containing a valid `selector` (via `_validate_selector`) and a non-empty string `field`.
3. **`condition` Assertion Validation:**
   - Verifies presence of `condition` mapping.
   - Delegates condition shape validation to existing recursive `_validate_condition`, which validates `all`, `any`, `not`, leaf forms, valid operators, and list values for `IN`/`NOT_IN`.
4. **Rejection Safeguards Preserved:**
   - Unknown top-level structured rule kinds raise `ProcessPackageValidationError` (`UNKNOWN_STRUCTURED_RULE_KIND`).
   - Unknown `for_each` assertion kinds raise `ProcessPackageValidationError` (`UNKNOWN_STRUCTURED_RULE_KIND`).
   - `condition` at top level (outside `for_each`) is rejected.
   - `cross_instance_comparison` inside `for_each` assertions is rejected.

## PARENT_SELECTOR_VALIDATION
PARENT_SELECTOR_VALIDATOR_CHANGE_REQUIRED: NO

`_validate_selector` checks required keys (`collection` vs `qname`) and validates `under`/`where` clauses when present. It does not enforce a rigid closed set of allowed keys on selector mappings. Consequently, selectors containing Capability A syntax:
```yaml
selector:
  collection: "ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails"
  parent:
    collection: "ipcdo:TrademarkApplicationDetails"
    where:
      field: "ipcdo:IPEntityStatusDetails/csdo:StatusCode"
      operator: "EQ"
      value: "01"
```
are already permitted by `ProcessPackageValidator` without requiring any changes to selector validation logic.

## CONDITION_ASSERTION_VALIDATION
Condition assertions inside `for_each` are now validated via:
```python
if kind == "condition":
    if "condition" not in rule:
        self._fail("INVALID_STRUCTURED_RULE_CONDITION", f"Condition assertion {message_code} требует condition.")
    self._validate_condition(rule.get("condition"), message_code)
    return
```
This reuses the existing recursive boolean condition DSL (`all`, `any`, `not`, leaf conditions). No duplicate boolean validation logic was created.

## CROSS_INSTANCE_VALIDATION
Cross-instance comparisons at top level are now validated via:
```python
if kind == "cross_instance_comparison":
    self._validate_operator(rule.get("operator"), message_code)
    for side in ("left", "right"):
        operand = rule.get(side)
        if not isinstance(operand, Mapping):
            self._fail("INVALID_CROSS_INSTANCE_OPERAND", f"Cross-instance comparison {message_code}/{side} должен быть объектом.")
        self._validate_selector(operand.get("selector"), message_code)
        if not isinstance(operand.get("field"), str) or not operand.get("field"):
            self._fail("INVALID_CROSS_INSTANCE_FIELD", f"Cross-instance comparison {message_code}/{side} требует строковый field.")
    return
```
Matches the exact contract expected by `StructuredRuleEvaluator`.

## VALIDATOR_TESTS
Suite: `eaeu_xml/tests/test_process_package_validator.py`
Execution:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider
```
Result: **10 passed in 0.07s**

Tested cases:
1. `test_validator_accepts_for_each_with_parent_selector` (PASS)
2. `test_validator_accepts_for_each_with_condition_assertion` (PASS)
3. `test_validator_accepts_cross_instance_comparison` (PASS)
4. `test_validator_rejects_unknown_top_level_rule_kind` (PASS — code `UNKNOWN_STRUCTURED_RULE_KIND`)
5. `test_validator_rejects_unknown_for_each_assertion_kind` (PASS — code `UNKNOWN_STRUCTURED_RULE_KIND`)
6. `test_validator_rejects_condition_at_top_level` (PASS — code `UNKNOWN_STRUCTURED_RULE_KIND`)
7. `test_validator_rejects_cross_instance_inside_for_each` (PASS — code `UNKNOWN_STRUCTURED_RULE_KIND`)
8. `test_validator_rejects_invalid_cross_instance_shape` (PASS — operand, operator, and field checks)
9. `test_validator_rejects_invalid_condition_assertion` (PASS — missing/invalid condition checks)
10. `test_loader_to_validator_path_with_approved_capabilities` (PASS)

## ENGINE_REGRESSION
Suite: `eaeu_xml/tests/test_structured_rules.py`
Execution:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py -p no:cacheprovider
```
Result: **30 passed, 5 subtests passed in 0.08s**

## FULL_EAEU_XML_REGRESSION
Suite: `eaeu_xml/tests`
Execution:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests -p no:cacheprovider
```
Result: **291 passed, 43 skipped, 1052 subtests passed in 2.43s** (0 failed, 0 errors).

## FULL_OP22_REGRESSION
Suite: `P.SP.02_OP_22/tests`
Execution:
```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests -p no:cacheprovider
```
Result: **2101 passed in 81.67s (0:01:21)** (0 failed, 0 errors).

## LOADER_VALIDATION_PROOF
Verified in `test_loader_to_validator_path_with_approved_capabilities`:
A temporary process package fixture was populated with structured rules demonstrating all three capabilities:
- `for_each` with `selector.parent`
- `for_each` with assertion `kind: condition` (`any: [...]`)
- `cross_instance_comparison` with semantic role selectors (`StatusCode 01` vs `StatusCode 02`)
The package was loaded via `ProcessPackageLoader.load()`, which triggered full validation through `ProcessPackageValidator.validate(package)`. The package loaded successfully without errors. Production YAML files were not touched.

## GIT_DIFF_CHECK
Command:
```bash
git diff --check
```
Result: Clean exit code 0, no whitespace errors or merge conflict markers.

## MSG012_STATUS
STATUS: INCOMPLETE
VERDICT: NOT_READY

`P.SP.02_OP_22/message_rules/P.SP.02.MSG.012.yaml` was strictly NOT modified in this task. It remains in its safe partial state (REQ 1, 33, 34).
With the validator barrier now fully resolved and verified, activation of requirements 6–31 in MSG012 YAML can proceed in the next dedicated implementation task.

## REMAINING_ISSUES
None for the validator. Registration of capabilities A, B, and C in `ProcessPackageValidator` is complete, tested, and backward-compatible.
