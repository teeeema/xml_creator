# WAVE 1 / AGENT B — Regression results

## CONFIRMED NEGATIVE QA CASES

Dedicated rerun of the six previously confirmed unexpected acceptances:

```text
6 passed in 0.94s
```

Covered cases:

1. OP22 empty REQUIRED element — rejected.
2. OP23 empty REQUIRED element — rejected.
3. OP26 empty REQUIRED `StartDateTime` — rejected.
4. OP26 `DrugApplicationKindCode = TEST` — rejected.
5. OP26 `CountryKindCode = TEST` — rejected.
6. GUI manual invalid edit after previous PASS — stale PASS invalidated and current XML rejected.

`PREVIOUS_UNEXPECTED_ACCEPTANCES: 6`

`REMAINING_UNEXPECTED_ACCEPTANCES: 0` for those six confirmed cases.

The two original `ENGINE_NOT_REACHED` cases and one `CANNOT_TEST_MISSING_EVIDENCE` case were not converted into artificial PASS results.

## FOCUSED REGRESSION SET

```text
12 passed in 2.29s
```

Includes shared REQUIRED semantics, OP22/OP23/OP26 negative cases, OP26 normative TEST-data generation, and GUI current-snapshot validation.

## ENGINE TESTS

```text
pytest -q eaeu_xml/tests
391 passed, 62250 subtests passed in 15.43s
```

## GUI TESTS

```text
pytest -q eaeu_xml/tests/test_gui_qt_view_model.py P.MM.01_OP_26/tests/test_gui_xml_snapshot_validation.py
16 passed in 0.47s
```

## OP22 TESTS

```text
pytest -q --tb=no P.SP.02_OP_22/tests
3110 passed in 197.12s
```

## OP23 TESTS

Focused WAVE 1 OP23 regressions pass.

The broader parallel B1 production file produced:

```text
617 passed, 14 failed in 171.36s
```

All 14 failures are in the MSG.022 positive-document helper path. That helper calls `build_body()` on an incomplete generated baseline before it manually adds the required MSG.022 fields. The MSG.022 B1 rules/tests are part of pre-existing parallel/uncommitted OP23 work and are outside the three WAVE 1 defects, so they were not rewritten in this task.

## OP26 TESTS

```text
pytest -q --tb=no P.MM.01_OP_26/tests
93 passed, 83 subtests passed in 6.70s
```

The all-transactions matrix was updated generically so test generation chooses executable normative literals rather than relying on `TEST` being accepted by validation.

## GRAPH UPDATE

`graphify update .` completed after implementation. The code graph was rebuilt successfully. The repository is above the configured HTML visualization node limit, so `graph.html` was left unchanged; `graph.json` and `GRAPH_REPORT.md` were updated.

## SAFETY / SCOPE CHECK

- Validator weakened: **NO**.
- Message-specific validation hardcode: **NO**.
- Knowledge Base changed: **NO**.
- Normative source documents changed: **NO**.
- Commit/push/reset/restore/clean: **NO**.
- Existing uncommitted/parallel changes were preserved.

