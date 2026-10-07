---
generated_by: "knowledge_base/tools/build_kb.py"
---

# Rules for Agents

1. **KB FIRST.** Search the KB before opening a PDF.
2. Before PDF, look for the OP/PRC/TRN/MSG/REQ/Structure/QName note and its source link.
3. Check `evidence_level` before using a statement as normative proof.
4. `AUDIT_DERIVED` is not normative proof.
5. `HISTORICAL` is not current truth.
6. `UNVERIFIED` cannot close a gap.
7. `CONFLICT` must not be resolved by inference.
8. `MISSING` must not be guessed.
9. When sources conflict, official source hierarchy wins.
10. Open the original PDF when KB evidence is insufficient.
11. After confirming new knowledge, update the KB with evidence and source page.
12. Never replace SOURCE text with interpretation.

Evidence priority: official XSD > official normative PDF/table > official XML/schema material > package source_refs > current verified audit > production YAML > historical audit > historical notes.
