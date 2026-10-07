---
generated_by: "knowledge_base/tools/build_kb.py"
generated_at: "2026-10-07T12:05:09+03:00"
---


# KB Enrichment Result

The canonical scope is migrated from the superseded 2849 known-scope checkpoint to 2894 atomic requirements by reconciling OP26 to 239 and importing the validated OP49 166-row re-audit.

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Known requirements scope | 2849 | 2894 | +45 |
| Requirements indexed | 2690 | 2894 | +204 |
| OP22 indexed | 1609 | 1609 | +0 |
| OP49 indexed | 0 | 166 | +166 |
| Source texts complete | 2690 | 2894 | +204 |
| Source page links complete | 2690 | 2894 | +204 |
| Structures indexed | 23 | 23 | +0 |
| Structures with field metadata | 0 | 18 | +18 |
| Fields indexed | 0 | 2030 | +2030 |
| Classifier entity notes | 11 | 10 | -1 |
| QName resolved | 2 | 20 | +18 |
| QName unresolved | 213 | 196 | -17 |
| QName conflicts | 37 | 72 | +35 |
| Gaps with closure criteria | 0 | 8685 | +8685 |

## Process inventory

- OP22: **1609 / 1609** (current recovered canonical inventory).
- OP23: **710 / 710**.
- OP26: **239 / 239**.
- OP32: **170 / 170**; atomic QName invariant remains 0 resolved / 170 unresolved.
- OP49: **166 / 166**; validated re-audit imported, strict IMPLEMENTED_CONFIRMED remains 0.

## Confirmed enrichment

- OP22 1609-row atomic identity/source inventory recovered from current business_rules/source_refs; all 63 message counts reconcile to FINAL_DELIVERY_MESSAGE_MATRIX.csv.
- OP26 source rows 50-87 for MSG.002 are materialized separately; MSG.028 duplicate source item 5 is represented as two canonical entities without inventing a new source number.
- OP49 166-row validated re-audit is imported with source text, PDF page, table/item trace and closure criteria for every requirement.
- Structure field rows indexed with provenance: **2030** across **18** structures.
- Exact Clark root QNames indexed where concrete namespace + local name + confirmed source_refs exist: **20** global QName entries.
- Classifier dependencies remain **59** rows; normalized classifier entity notes: **10**. Composite dependency cells are not treated as separate entities.
- Decision №5 navigation now includes RelatesAction, the common-process Action URI component order, and EAEU:// logical-address prefix with SOURCE-page evidence.
- PDF/printed-page mappings are indexed only when the extracted standalone page header follows a repeated stable offset.

## Remaining gap categories

- `CONFLICT`: 72
- `MISSING_CLASSIFIER`: 343
- `MISSING_CLASSIFIER_PAYLOAD`: 10
- `MISSING_EXTERNAL_REGISTRY`: 90
- `MISSING_IMPLEMENTATION_EVIDENCE`: 1328
- `MISSING_NAMESPACE`: 2822
- `MISSING_QNAME`: 2822
- `MISSING_STRUCTURE_VERSION`: 3
- `MISSING_XML_PATH`: 1168
- `UNVERIFIED`: 27

## Validation snapshot

- Stale sources: **0**.
- Broken internal links: **0**.
- Duplicate canonical IDs: **0**.
- Missing requirement files: **0**.
- Missing linked source pages: **0**.
- SOURCE extraction was reused after SHA-256 verification; PDFs were not re-extracted during enrichment rebuilds.
