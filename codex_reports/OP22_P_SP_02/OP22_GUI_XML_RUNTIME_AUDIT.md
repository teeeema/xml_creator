# OP22 / P.SP.02 GUI XML runtime audit

Status: **COMPLETE** for the OP22 / P.SP.02 GUI → form data → production validation → XML runtime matrix.

The current evidence file is `OP22_GUI_XML_RUNTIME_MATRIX.csv`. It contains all 54 GUI-visible transactions and all 111 transaction/message combinations. Every row was rerun after the last production change in both **Test Data** and **Required Data** modes.

## Progression

- Initial historical audit: **4 PASS**, 54 FAIL_FORM_DATA, 53 NOT_APPLICABLE.
- Intermediate checkpoint: **91 PASS**.
- Pre-continuation checkpoint: **103 PASS**, 3 FAIL_FORM_DATA, 3 FAIL_EXCEPTION, 2 NOT_APPLICABLE.
- Final: **111 PASS**, 0 FAIL_FORM_DATA, 0 FAIL_EXCEPTION, 0 NOT_APPLICABLE.

The intermediate 91-PASS checkpoint is retained as a historical milestone; this audit does not reconstruct category counts that were not preserved at that checkpoint.

## Root causes and fixes

### Nested `for_each`

Optional ancestors selected indirectly by descendant rule paths were not always materialized, so nested `for_each` assertions could have no usable owner context. The shared `TestDataGenerator` now treats an optional ancestor as selected when a descendant rule requires data beneath it. Sparse repeated-instance alignment remains positional.

### `condition.any` / count

Rules that require one of several count branches, for example `count(Payment/Bank) >= 1 OR count(Payment/System) >= 1`, were evaluated but the helper did not materialize a safe branch. The generator now creates one satisfiable branch from the declarative rule metadata. No process/message identifiers are hardcoded.

### Embedded `ONE_OF` / `xs:any`

For R.010 messages with `embedded_structures.selection = ONE_OF`, the ordinary form helper previously generated scalar `"TEST"` for the required `xs:any` wildcard. That produced `DATATYPE_INVALID` and `EMBEDDED_STRUCTURE_CARDINALITY` for P.SP.02.MSG.003, P.SP.02.MSG.031, and P.SP.02.MSG.059.

The application layer now resolves the allowed embedded structures from `MessageDefinition.embedded_structures`, chooses the first branch that can be generated and validated using existing metadata/rules, generates its required form values with the shared `TestDataGenerator`, builds the exact embedded XML root, and places that `ET.Element` into the wildcard. The body provider accepts an already materialized, unambiguous allowed root through its existing QName selector. A generic top-level structured `fixed_value` is also applied by the helper so synthetic/real embedded branches can satisfy literal rules without message-specific code.

The embedded element is copied directly rather than serialized and reparsed during materialization. This preserves the generator's structural empty-text markers used for elements whose attributes/descendants establish presence.

Result in both data modes:

- `P.SP.02.MSG.003`: PASS; selected allowed root `{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails`.
- `P.SP.02.MSG.031`: PASS; same allowed branch selected deterministically and all scoped rules pass before generation.
- `P.SP.02.MSG.059`: PASS; same allowed branch selected deterministically and all scoped rules pass before generation.

### Matrix session/state isolation

The final matrix harness creates a fresh `GuiViewModel` / transaction session for every independent `message × data-mode` attempt. Test Data and Required Data never share mutable transaction state.

Response branches also follow the transaction state machine. `MUTUAL_OBLIGATIONS` transactions such as TRN.049 and TRN.050 begin in `WAITING_RECEIVED`; the harness advances the required `RECEIVED → ACCEPTED_FOR_PROCESSING → WAITING_RESPONSE` transitions before generating the selected response. Production transaction/state-machine code was not changed for this matrix issue.

This removes the former `InvalidStateTransitionError: response ... WAITING_RECEIVED` failures while preserving the normative transaction pattern implementation.

## Final matrix gates

- TOTAL: 111
- PASS: 111
- FAIL_FORM_DATA: 0
- FAIL_EXCEPTION: 0
- NOT_APPLICABLE: 0
- Test Data: 111 PASS / 0 FAIL
- Required Data: 111 PASS / 0 FAIL
- Response branches: 57 checked / 57 PASS / 0 FAIL
- Form build: 111 / 111
- Production validation: 111 / 111 in Test Data and 111 / 111 in Required Data
- XML non-empty: 111 / 111 in both modes
- XML parse: 111 / 111 in both modes
- container/root QName: 111 / 111 in both modes
- embedded allowed-root QName: 111 / 111 in both modes (non-embedded rows are vacuously true; embedded rows require exactly one allowed root)

## Normative basis

**CONFIRMED / implementation-neutral.** The allowed embedded structures, exact namespaces/QNames, transaction patterns, and structured rules come from the existing OP22 package metadata and source-traced mappings. This work did not modify normative mappings, source references, process definitions, transaction definitions, message definitions, or rule semantics. `VALIDATOR_WEAKENED: NO`. `NORMATIVE_RULES_WEAKENED: NO`.

## Regression evidence after the last production change

- Required-data regression: `24 passed, 2 subtests passed`.
- Generic embedded ONE_OF regression: `12 passed`.
- OP22 embedded/generation focused set: `28 passed`.
- GUI controller/view-model focused set: `21 passed`.
- Engine/form-data focused set: `107 passed, 7 subtests passed`.
- Full `P.SP.02_OP_22/tests`: `3109 passed`.
- Runtime matrix: `111 PASS`.
- `eaeu_xml/tests`: `387 passed, 1 failed, 62247 subtests passed`.
- Full repository: `4058 passed, 4 failed, 62357 subtests passed`.

The non-OP22 failures are classified **PREEXISTING_OR_PARALLEL_FAILURE**. They are in the concurrently modified P.MM.01 / OP26 area:

- `P.MM.01/tests/test_all_transactions_e2e.py`: two expected artifact/count mismatches against changed `P.MM.01_OP_26` outputs.
- `P.MM.01_OP_26/tests/test_restored_session_xml_e2e.py`: TRN.008 initial MSG.019 is currently INVALID, so no generated message id exists.
- `eaeu_xml/tests/test_session_restore.py`: the same P.MM.01 TRN.008 / MSG.019 condition.

Direct inspection shows P.MM.01.MSG.019 fails its existing `OP26.P_MM_01.P.MM.01.MSG.019.REQ.001` rule and contains no top-level structured `fixed_value`, so the final ONE_OF helper change did not introduce that failure. The OP26 files were left untouched by this task.

## Files changed by this continuation

- `eaeu_xml/src/eaeu_xml/application/facade.py` — generic embedded ONE_OF materialization from message/structure metadata.
- `eaeu_xml/src/eaeu_xml/application/services.py` — generic top-level structured `fixed_value` completion, in addition to the previously accumulated shared form-data fixes.
- `eaeu_xml/src/eaeu_xml/process_packages/body.py` — accept an already materialized, uniquely identifiable allowed embedded payload.
- `eaeu_xml/tests/test_embedded_one_of.py` — generic R.010 + `xs:any` + ONE_OF regression in test and required modes.
- `P.SP.02_OP_22/tests/test_embedded_one_of_form_generation.py` — OP22 integration regression for MSG.003 / MSG.031 / MSG.059 in both modes.
- `codex_reports/OP22_P_SP_02/OP22_GUI_XML_RUNTIME_MATRIX.csv` — final 111-row evidence matrix.
- `codex_reports/OP22_P_SP_02/OP22_GUI_XML_RUNTIME_AUDIT.md` — this final audit.

`graphify update .` was run after production code changes.
