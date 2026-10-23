# Shared Engine Capability Wave — Implementation Report

## Scope

Implemented and verified eight requested generic shared-engine capabilities without changing OP-specific production rules, knowledge-base files, classifier data, normative identifiers, or threshold constants.

## Implemented capabilities

1. **TYPED_DATE** — `comparison` supports `value_type: DATE` using ISO date parsing. Invalid or missing values fail deterministically. Untyped comparison behavior is unchanged.
2. **CONDITIONAL_CROSS_INSTANCE** — existing `cross_instance_comparison` now accepts an optional document-scope `when` guard. If the condition does not apply the rule passes as not applicable; when it applies, the previous exact-one selection semantics remain.
3. **SET_EQUIVALENCE** — new generic `set_equivalence` compares selected values as mathematical sets, so order and duplicate occurrences do not alter membership equality. Missing selector sources remain distinct from present-but-empty collections unless `allow_both_missing` is explicitly set.
4. **CALENDAR_MONTH_RELATION** — typed comparisons can use `value_type: CALENDAR_MONTH` with signed integer `offset_months`, including year rollover.
5. **CONTEXT_RELATIVE_SELECTOR** — `relative_to_context` selects sibling instances by data values relative to the current `for_each` context. Selection is independent of physical XML ordering and remains within the same repeated-owner context.
6. **DECIMAL_VALIDATOR** — the evaluator already supported `DECIMAL`; the validator now admits that existing generic runtime behavior instead of rejecting it.
7. **CONTEXT_SCOPED_AGGREGATE** — `aggregate_comparison` is now valid inside `for_each`; selected aggregate values are limited to the current repeated owner. Existing document-scope aggregate behavior remains available.
8. **DECODED_BINARY_BYTE_LENGTH** — new `decoded_binary_length` strictly decodes Base64 and compares the actual decoded byte count with a caller-supplied value. No 5 MB interpretation is hardcoded.

## Already-existing capabilities reused

- Base `cross_instance_comparison` runtime and exact-one selected-owner semantics.
- `DECIMAL` numeric comparison in the evaluator.
- Document-scope `aggregate_comparison`.
- Existing rule composition for the OP49 ALL_EQUAL-shaped requirement.
- Existing reduction for the known singleton MAX-shaped OP49 scope; no speculative MAX primitive was added.

## Files changed by this wave

- `eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py` — shared evaluator/runtime support.
- `eaeu_xml/src/eaeu_xml/process_packages/validator.py` — strict grammar for the new shared forms and existing DECIMAL support.
- `eaeu_xml/tests/test_shared_engine_capabilities.py` — focused regression coverage for all eight capabilities and preserved behavior.
- `codex_reports/SHARED_ENGINE_WAVE/*` — implementation, matrix, regression, and next-rule reports.

## Safety and scope invariants

- `VALIDATOR_WEAKENED: NO` — new forms are explicitly validated; unknown comparison types and malformed relative selectors remain rejected.
- `OP_SPECIFIC_HARDCODE: NO` — no process/message identifiers or classifier values were placed in shared runtime code.
- `PRODUCTION_OP_RULES_CHANGED: 0` by this wave.
- `KB_CHANGED: 0` by this wave.
- No Base64 size threshold is embedded in the engine; the unresolved normative meaning of “5 MB” stays outside the generic primitive.

## Normative basis

The implementation is a generic engine capability layer supporting previously audited requirement shapes. This wave does not claim any OP requirement closed solely because the engine can now express it. Requirement closure still requires the applicable canonical source trace, exact structure/QName/classifier evidence, production rule mapping, and runtime proof.
