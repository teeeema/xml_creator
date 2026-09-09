# P.MM.06 Structures Row-Level Audit

Normative source: `32_ОП.pdf` only. P.MM.01, P.DS.01, other processes, external XSDs and the internet were not used as normative evidence.

Integrity: **PASS**.

| Structure | Table | PDF pages | Rows | Count gate |
|---|---:|---:|---:|---|
| R.HC.MM.06.001 | 10 | 169–188 | 116/116 | PASS |
| R.HC.MM.06.002 | 13 | 189–193 | 19/19 | PASS |
| R.HC.MM.06.003 | 16 | 194–201 | 25/25 | PASS |
| R.HC.MM.06.004 | 19 | 202–203 | 9/9 | PASS |
| R.HC.MM.06.005 | 22 | 205–208 | 17/17 | PASS |

## Coverage

- Hierarchy: 135 resolved; 51 unresolved.
- Cardinality: 186 resolved; 0 unresolved.
- Model element IDs: 184.
- Model type IDs: 184.
- QName overlay accounting: 7 resolved; 4 ambiguous mapping records; 175 residual unresolved.
- Raw node QName statuses: 7 resolved; 179 unresolved.
- Attribute owners: 1 resolved; 3 unresolved.
- Relative-number rows: 51.
- Multi-page rows: 30.
- Uncertain rows: 0.
- Numbering gaps: 0.
- Duplicate numeric row numbers: 0.

## Verification notes

TXT/table geometry was used for extraction; PNG pages were used to verify table starts/ends, page continuations, first/last rows, hierarchy columns and multiplicity. Multi-page continuations were merged into one node.

Relative `*.n` parents remain unresolved unless the table provides a provable absolute parent. No QName was created from a Russian normative name, model ID or datatype.

The four ambiguous QName records cannot be assigned to four individual nodes without guessing. They are preserved as overlay records; this explains the distinction between 179 unresolved node statuses and the requested 175 residual-unresolved overlay accounting.

Two prior QName-overlay records for the PDF document rows carry model element ID `M.HC.SDE.00302`, while tables 13 and 16 explicitly contain `M.HC.SDE.00326`. The row-level table value prevails; the QName mapping is retained because its exact structure, row and normative name still identify the node.

R.006 and R.007 were not reconstructed. X.X.X, Y.Y.Y and Z.Z.Z were not resolved or replaced.
