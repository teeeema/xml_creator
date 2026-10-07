# FINAL TRACEABILITY GATE

REQUIREMENTS_CHECKED: 2520

FULL_TRACE: 451
PARTIAL_TRACE: 1867
BROKEN_TRACE: 202

ORPHAN_RULES: 0
ORPHAN_TESTS: 0

WRONG_SOURCE_LINKS: 0
WRONG_RULE_LINKS: 0
WRONG_TEST_LINKS: 202
STALE_PROJECT_STATE_LINKS: 159

CRITICAL: 0
HIGH: 202

PRODUCTION_CHANGED: 0
KB_CHANGED: 0

VERDICT: FAIL — end-to-end traceability is not complete; 1867 requirements are partial and 202 contain confirmed broken linkage.

## By OP

| OP | Requirements | FULL_TRACE | PARTIAL_TRACE | BROKEN_TRACE |
|---|---:|---:|---:|---:|
| OP22 | 1609 | 141 | 1467 | 1 |
| OP23 | 710 | 310 | 400 | 0 |
| OP26 | 201 | 0 | 0 | 201 |

## Confirmed broken linkage

- OP22: **1** wrong requirement/test linkage — `P.SP.02.MSG.031:49:19` points positive/negative/runtime evidence to Table 48 requirement 19 instead of Table 49 requirement 19.
- OP26: **201** runtime-proof links are not requirement-specific. `test_pmm01_catalog.py` does not assert individual structured-rule execution; all 201 canonical rows still have `Negative test: NOT_WIRED`.
- OP26: within those 201 broken rows, **159** also have stale project-state linkage: current YAML now contains a structured rule while the canonical KB still says `OPEN_PRODUCTION_MAPPING`.

No current structured-rule object in OP22/OP23/OP26 was orphaned from the canonical inventory by ID/source linkage. No independently orphaned requirement-specific test was confirmed; the OP22 test defect calls the wrong existing rule and is therefore counted as WRONG_TEST_LINK, while the OP26 catalog test is valid package-level testing but invalid as per-requirement runtime proof.

## Normative/source verification

Original-source SHA256 values match `knowledge_base/02_SOURCE_REGISTRY.md` for `ОП_22.pdf`, `ОП_23.pdf`, and `26_ОП.pdf`. All 2520 canonical notes contain source text, PDF page, and table/item metadata. Inherited source chains were not treated as wrong merely because the current table-range page differs from the semantic leaf page; both provenance roles are preserved in OP22 wiring.

## Runtime verification

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests P.SP.03_OP_23/tests P.MM.01_OP_26/tests -p no:cacheprovider`

Result: **3829 passed, 110 subtests passed, 0 failed**.

A green aggregate suite is evidence that the current code is internally regression-safe; it does not substitute for a requirement-specific positive/negative/runtime trace.
