# Shared Engine Capability Wave — Regression Results

All mandatory regression gates executed successfully.

| Gate | Result |
| --- | --- |
| ENGINE — `eaeu_xml/tests` | **416 passed, 62,259 subtests passed** |
| OP22 — `P.SP.02_OP_22/tests` | **4,429 passed** |
| OP23 — `P.SP.03_OP_23/tests` | **678 passed, 27 subtests passed** |
| OP26 — `P.MM.01_OP_26/tests` | **853 passed, 83 subtests passed** |
| OP49 — `P.DS.01_OP_49/tests` | **32 passed** |
| OP32 — `P.MM.06_OP_32/tests` | **8 passed** |
| `git diff --check` | **PASS — no output** |

Focused shared-engine checks executed earlier in the wave also passed:

- `eaeu_xml/tests/test_shared_engine_capabilities.py` — 18 passed.
- `eaeu_xml/tests/test_structured_rules.py` — 49 passed, 5 subtests passed.
- `eaeu_xml/tests/test_process_package_validator.py` — 10 passed.
- `eaeu_xml/tests/test_repeatable_xml_alignment.py` — 22 passed.
- `eaeu_xml/tests/test_required_form_data.py` — 25 passed, 2 subtests passed.

## Failure classification

- `REGRESSIONS_INTRODUCED: None observed.`
- `PREEXISTING_OR_PARALLEL_FAILURES: None encountered in the executed regression gates.`
- `TOOLING_BLOCKS_ENCOUNTERED: One polling attempt for the already-running OP23 test was blocked by the platform's automatic safety review. After explicit user authorization, a separate simple poll returned the completed successful result. The test itself did not fail and was not restarted.`

## Parallel-work preservation

The repository contained numerous pre-existing modified/untracked OP22/OP23/OP26/OP49 rule, test, and report files. They were preserved. This wave did not restore, reset, clean, checkout, add, commit, push, or overwrite those parallel changes.
