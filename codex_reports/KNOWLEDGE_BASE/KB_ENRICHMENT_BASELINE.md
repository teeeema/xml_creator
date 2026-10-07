# KB Enrichment Baseline

> **SUPERSEDED / HISTORICAL.** This file records the pre-migration checkpoint. The current canonical baseline is 2894 requirements: OP22 1609, OP23 710, OP26 239, OP32 170, OP49 166. See `KB_CANONICAL_SCOPE_2894_MIGRATION.md` and `KB_CANONICAL_SCOPE_2894_VALIDATION.json`.

Captured: `2026-10-06T15:24:54+03:00`  
Git HEAD: `5df76609131e9ce88fea5502fdc942238ab2c792`  
Git dirty entries: **71**

## Baseline metrics

- Requirements indexed: **1427 / 2797**
- OP22: **346 / 1557**
- OP23: **710 / 710**
- OP26: **201 / 201**
- OP32: **170 / 170**
- OP49: **0 / 159**
- Source pages extracted: **2562 / 2562**
- Structures indexed: **23**
- Classifier notes: **11** from **59** dependency rows
- QName resolved / unresolved / conflicts: **2 / 213 / 37**
- Broken internal links: **0**
- Stale sources: **0**

## Gap inventory

Total gap rows: **3755**. Canonical inventory deficits are aggregate rows when the missing identities cannot be proven safely.

| Category | Rows |
|---|---:|
| `MISSING_QNAME` | 1411 |
| `MISSING_NAMESPACE` | 1411 |
| `MISSING_IMPLEMENTATION_EVIDENCE` | 570 |
| `MISSING_XML_PATH` | 321 |
| `CONFLICT` | 37 |
| `MISSING_STRUCTURE_VERSION` | 3 |
| `MISSING_CANONICAL_REQUIREMENT` | 2 |

## Guardrails

- No production file is writable in this task.
- OP49 re-audit directory is read-only for this task.
- Missing canonical IDs are not synthesized.
- `AUDIT_DERIVED` and historical evidence cannot become normative proof without source provenance.
