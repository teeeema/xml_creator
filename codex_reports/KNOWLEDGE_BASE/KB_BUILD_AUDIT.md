---
generated_by: "knowledge_base/tools/build_kb.py"
generated_at: "2026-10-07T12:05:09+03:00"
---

# KB Build Audit

- Status: **COMPLETE**
- PDF processed: 6/6
- Pages extracted: 2562/2562
- OP indexed: 5/5
- Requirements indexed: 2894/2894 known scope
- Structures indexed: 23 (with field metadata: 18)
- Field rows indexed: 2030
- Classifier dependency rows: 59; unique notes: 10
- QName resolved/unresolved: 20/196
- Gaps indexed: 1321
- Broken internal links: 0
- Stale sources after extraction: 0

## Deliberate knowledge incompleteness

- OP22: current inventory is 1609/1609. It is deterministically recovered from current business_rules/source_refs, including explicit inherited ranges, and reconciled to FINAL_DELIVERY_MESSAGE_MATRIX.csv. FINAL_DELIVERY_AUDIT.md explicitly states that this is not a new independent row-by-row PDF re-audit.
- OP26: source-reconciled atomic scope is 239. Table 19 MSG.002 items 50-87 are separate atomic requirements; Table 21 MSG.028 preserves two distinct source rows both numbered 5 using source-occurrence metadata.
- OP49: validated canonical scope is 166 (35+38+2+54+37). All 166 rows have primary-source trace and remain OPEN under strict closure.
- Source sections/tables are not auto-created when exact table boundaries cannot be proven from page extraction. Source pages remain available.

## Consistency

```json
{
  "duplicate_requirement_ids": [],
  "missing_requirement_markdown": [],
  "missing_requirement_source_pages": [],
  "source_hashes_complete": true
}
```

