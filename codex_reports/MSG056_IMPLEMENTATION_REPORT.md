# MSG056 implementation report

## STATUS

INCOMPLETE

## VERDICT

NOT_READY

## CHANGED_FILES

`P.SP.02_OP_22/message_rules/P.SP.02.MSG.056.yaml`; three MSG056 test files; this report.

## NORMATIVE_INVENTORY

Message `P.SP.02.MSG.056`; Table 74; PDF physical pages 804–807. Table 74 row 1–6 inherits Table 72 rows 1–6 on pages 801–803. Captured rows: 15. Expanded numbered requirements: 20.

## STRUCTURE

`R.IP.SP.03.003`, version `1.0.0`, root `{urn:EEC:R:IP:SP:03:IPDutyDetails:v1.0.0}IPDutyDetails`; transaction `P.SP.02.TRN.050`, procedure `P.SP.02.PRC.035`, request to MSG057.

## MAPPING_COUNTS

FULLY_MAPPABLE 17: 1,2,3,6–18,20. SAFE_PARTIAL 1: 19. EXTERNAL 2: 4,5. Arithmetic: 20. Structured-rule objects: 18.

## FULLY_MAPPABLE

Implemented exact owners for authority, payment, party, document, and forbidden-root fields. Table 74 direct requirements are scoped under `ipcdo:IPPaymentDetails`.

## SAFE_PARTIAL

REQ19 validates required binary document and allowed `mediaTypeCode`; the 5 MB payload-size limit has no safe current evaluator expression.

## EXTERNAL

REQ4–5 remain unmapped because both require the external legal-action classifier presence predicate and authoritative classifier correspondence.

## AMBIGUOUS

None.

## ENGINE_UNSUPPORTED

None.

## SOURCE_CONFLICT

None.

## EXECUTABLE_REQUIREMENTS

`{1,2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20}`

## UNMAPPED_REQUIREMENTS

`{4,5}`

## IMPLEMENTATION

Rules retain Table 74 provenance; inherited rules retain the Table 74 inherited-row reference. REQ7 forbids both account types. REQ9 is an exact one-of-three-role selection. REQ13/14 use per-party semantic predicates; REQ15–19 use direct payment-document ownership.

## OWNER_QNAME_SAFETY

Collection paths use exact namespace-prefixed fields, direct payment ownership, and relative child targets. No local-name fallback is used.

## REPEATABLE_RECORD_SAFETY

REQ18 has an actual repeatable document matrix proving an invalid document cannot be repaired by a sibling.

## MESSAGE_ISOLATION

The scoped test confirms every loaded rule ID starts with `P.SP.02.MSG.056.`.

## NORMATIVE_BASIS

Direct PDF reread: OP_22 pages 801–803 (Table 72) and 804–807 (Table 74), plus repository message and transaction metadata.

## MSG056_TESTS

`PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg056_*.py -p no:cacheprovider` — `4 passed in 0.14s`. This includes a valid production-shaped fixture through build, serialize, parse, extract, and validate.

## ENGINE_VALIDATOR_REGRESSION

`PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider` — `40 passed, 5 subtests passed in 0.11s`.

## FULL_OP22_REGRESSION

Attempted twice, but the bounded shell execution returned before completion and did not retain a pytest process. No complete result is asserted.

## GIT_DIFF_CHECK

Executed. The working tree contains extensive pre-existing concurrent changes, including MSG057 and shared infrastructure. The MSG056 task changed only its allowed mapping, three MSG056 tests, and this report.

## REMAINING_ISSUES

The required full OP22 regression did not complete under the bounded execution environment; therefore READY is not asserted.
