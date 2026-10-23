# P.CLS.027 — test results

## Targeted verification

Command:

`pytest -q P.SP.02_OP_22/tests/test_msg001_effective_field_policy.py P.SP.02_OP_22/tests/test_pcls027_classifier.py`

Result: **13 passed in 1.48s**.

Covered:

- MSG.001 effective field policy resolves `IPDocKindCode` to fixed `07220`;
- `IPDocKindName` is forbidden/hidden;
- required/test data materialize `07220` and omit the forbidden name;
- P.CLS.027 entry `07220` has the confirmed name, AM/BY/KZ/KG/RU applicability, Decision №92 page 10 source and Decision №148 revision context;
- raw body validation reports `FIXED_VALUE_MISMATCH` for a wrong code and `FORBIDDEN_FIELD` when the name is supplied;
- XML serialization materializes `IPDocKindCode=07220` and omits `IPDocKindName`;
- every `EXACT_MATCH` row in the OP22 usage report points to a code present in the local OP22 P.CLS.027 dataset.

## Full OP22 regression

Command:

`pytest -q P.SP.02_OP_22/tests`

Result: **4442 passed in 122.60s (0:02:02)**.

No generic engine implementation was changed for this task, so a separate full cross-process engine regression was not required.
