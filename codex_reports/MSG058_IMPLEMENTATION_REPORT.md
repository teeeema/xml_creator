# MSG058 implementation report

## STATUS

INCOMPLETE

## VERDICT

NOT_READY

## CHANGED_FILES

`P.SP.02_OP_22/message_rules/P.SP.02.MSG.058.yaml`; three MSG058 test files; this report.

## NORMATIVE_INVENTORY

Message `P.SP.02.MSG.058`; Table 76; PDF physical pages 808–809. Captured rows and expanded requirements: 7. No inherited table applies.

## STRUCTURE

`R.IP.SP.02.008`, version `1.0.0`, root `{urn:EEC:R:IP:SP:02:TrademarkRegisterRequestDetails:v1.0.0}TrademarkRegisterRequestDetails`; initiating request in TRN050, procedure `P.SP.02.PRC.035`, response MSG059.

## INHERITANCE

None.

## MAPPING_COUNTS

FULLY_MAPPABLE 7; SAFE_PARTIAL, EXTERNAL, AMBIGUOUS, ENGINE_UNSUPPORTED, and SOURCE_CONFLICT: 0. Arithmetic: 7.

## FULLY_MAPPABLE

REQ1 forbids two root fields; REQ2–3 enforce mutual exclusion; REQ4 requires a document; REQ5 forbids binary content; REQ6 uses inclusive OR for document kind code/name; REQ7 requires document name, ID, and date.

## SAFE_PARTIAL

None.

## EXTERNAL

None.

## AMBIGUOUS

None.

## ENGINE_UNSUPPORTED

None.

## SOURCE_CONFLICT

None.

## EXECUTABLE_REQUIREMENTS

`{1,2,3,4,5,6,7}`

## UNMAPPED_REQUIREMENTS

`{}`

## IMPLEMENTATION

Each rule has exact Table 76 provenance. REQ6 is an `any` condition, preserving the normative inclusive “one of” meaning rather than requiring both fields.

## OWNER_QNAME_SAFETY

Uses the resolved R.IP.SP.02.008 paths and namespace prefixes; document rules are scoped to `ipcdo:AccompanyingDocumentsDetails`.

## REPEATABLE_RECORD_SAFETY

REQ7 sparse sibling proof confirms a missing field in one document is not repaired by another document.

## MESSAGE_ISOLATION

The production fixture confirms only `P.SP.02.MSG.058.*` structured rules load for MSG058.

## NORMATIVE_BASIS

Direct PDF reread: OP_22 physical pages 808–809, Table 76. Repository metadata independently confirmed message, transaction, procedure, structure, version, and QName.

## MSG058_TESTS

`PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg058_*.py -p no:cacheprovider` — `3 passed in 0.13s`, including build → serialize → parse → extract → validate.

## ENGINE_VALIDATOR_REGRESSION

`PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider` — `40 passed, 5 subtests passed in 0.09s`.

## FULL_OP22_REGRESSION

NOT RUN. The required complete OP22 suite was not completed in this bounded run.

## GIT_DIFF_CHECK

`git diff --check` passed for task-owned mapping and tests.

## REMAINING_ISSUES

Full OP22 regression is required before READY can be asserted.
