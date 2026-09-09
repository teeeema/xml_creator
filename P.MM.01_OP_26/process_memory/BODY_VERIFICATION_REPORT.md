# Body verification report

Source: Decision No. 68, tables 4, 7, 10, 13, 16, 19, 22 and 25.
Audit method: page-level text inventory followed by visual PDFKit review of
table layout, page continuations, indentation and merged cells. Every page had
an exact cardinality-count match with its field-row count.

| Structure | Rows | Verified | External | Unresolved fields | Attrs | Repeatable | Nested complex | Rule rows / unresolved | Serialization | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| R.006 | 10 | 9 | 1 | 0 | 0 | 0 | 0 | 0 / 0 | version blocked | VERIFIED_WITH_EXTERNAL_DEPENDENCIES |
| R.007 | 11 | 10 | 1 | 0 | 1 | 1 | 0 | 0 / 0 | version blocked | VERIFIED_WITH_EXTERNAL_DEPENDENCIES |
| R.HC.MM.01.001 | 405 | 353 | 52 | 0 | 69 | 50 | 107 | 105 / 1 conflict | MSG.002 blocked explicitly | VERIFIED_WITH_EXTERNAL_DEPENDENCIES |
| R.HC.MM.01.002 | 23 | 21 | 2 | 0 | 3 | 1 | 0 | 19 / 4 conflicts | MSG.023/.024 blocked explicitly | VERIFIED_WITH_EXTERNAL_DEPENDENCIES |
| R.HC.MM.01.003 | 39 | 36 | 3 | 0 | 6 | 3 | 5 | 59 / 0 | verified | VERIFIED_WITH_EXTERNAL_DEPENDENCIES |
| R.HC.MM.01.004 | 11 | 10 | 1 | 0 | 1 | 0 | 0 | 6 / 0 | verified + SOAP E2E | VERIFIED_WITH_EXTERNAL_DEPENDENCIES |
| R.HC.MM.01.006 | 42 | 39 | 3 | 0 | 6 | 3 | 6 | 5 / 0 | verified | VERIFIED_WITH_EXTERNAL_DEPENDENCIES |
| R.HC.MM.01.007 | 14 | 13 | 1 | 0 | 1 | 1 | 0 | 7 / 0 | verified | VERIFIED_WITH_EXTERNAL_DEPENDENCIES |

Coverage remains 555/555: 491 verified field rows, 64 rows needing an external
classifier dataset for membership validation, and zero field-interpretation
ambiguities. All 87 attribute names/owners and all cardinalities were
recalculated; corrected cardinalities yield 59 repeatable fields. Four rows are
confirmed arbitrary XML children (`ANY_XML`).

Message rules: 201 total; 195 verified, 1 external-registry dependency, 5
`INTERNAL_NORMATIVE_CONFLICT`, and zero unresolved interpretations. See
`INTERPRETATION_UNRESOLVED_REPORT.md`.

Baseline: 79 tests. Final: 63 engine + 17 package = 80 tests. Import and compile
checks pass. Package status is `BODY_MODEL_CONFIRMED_WITH_EXTERNAL_CONFLICTS`.
It is not production-ready.
