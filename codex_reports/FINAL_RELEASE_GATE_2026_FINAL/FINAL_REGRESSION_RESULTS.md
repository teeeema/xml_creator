# FINAL REGRESSION RESULTS

All listed regression results were executed during this final gate against the synchronized workspace snapshot.

- `pytest -q eaeu_xml/tests` -> **416 passed, 62259 subtests passed in 10.83s**
- `pytest -q P.SP.02_OP_22/tests` -> **4429 passed in 158.50s**
- `pytest -q P.SP.03_OP_23/tests` -> **680 passed, 27 subtests passed in 161.30s**
- `pytest -q P.MM.01_OP_26/tests` -> **853 passed, 83 subtests passed in 19.90s**
- `pytest -q P.MM.06_OP_32/tests` -> **8 passed in 0.17s**
- `pytest -q P.DS.01_OP_49/tests` -> **46 passed in 0.35s**
- `git diff --check` -> **PASS**, no output

Additional final-gate evidence:

- Representative generator-validator selection refreshed after the main suites: **36 passed in 3.22s**.
- Functional negative QA selection: **23 passed in 1.44s**.
- OP26 `OP26.P_MM_01.P.MM.01.MSG.001.REQ.001`: serialized XML -> parse -> extract -> validate = PASS; removing nested `DrugRegistrationDetails`, reserializing/reparsing/extracting -> rule = FAIL.

PRODUCTION_REGRESSIONS: **0 detected**.
