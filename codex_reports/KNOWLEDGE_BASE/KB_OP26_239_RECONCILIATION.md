# OP26 Canonical Reconciliation: 201 → 239

The original `26_ОП.pdf` is authoritative for this reconciliation.

- Before: **201** canonical records.
- After: **239** atomic canonical requirements.
- New atomic requirements: **38**.
- MSG.002: **50 → 87** canonical atomic rows. Old REQ.050 had collapsed source items 50–87; the primary PDF shows 38 separately numbered rows across PDF pages 224–231.
- MSG.028: **7 → 8** canonical atomic rows. Table 21 contains two different source rows numbered `5` on PDF pages 233 and 234.
- Table 19 item 84 remains `OPEN_NORMATIVE_AMBIGUITY` because the primary publication is truncated at PDF page 230. No missing tail was inferred.
- Source trace complete: **239 / 239**.

## Duplicate source item 5

- First canonical entity: `OP26.P_MM_01.P.MM.01.MSG.028.REQ.005`, source item `5`, occurrence `1`.
- Second canonical entity: `OP26.P_MM_01.P.MM.01.MSG.028.REQ.005.2`, source item `5`, occurrence `2`.
- The `.2` suffix is a canonical disambiguator only. It is not a normative requirement number.

Project-state implementation evidence was not copied from the old merged rows into newly split atomic rows. Their status remains open until requirement-level implementation/runtime proof is synchronized.

## Project-state snapshot from the completed re-audit

These are audit/project-state counts, not additional normative requirements:

- Atomic source requirements: **239**.
- Current production structured rules observed by the re-audit: **159**.
- Atomic production mappings missing at that checkpoint: **80**.
- Classified as safe to implement from already-confirmed local normative text: **52**.
- Classified as blocked by missing/conflicting external information: **28**.
- `MISSING_XSD`: **8** structure payloads.
- Version placeholders: **4**.
- `UNRESOLVED_QNAME`: **198** audit items.
- Classifier dependencies: **22** atomic checks (11 `codeListId` + 11 membership).
- External-registry dependencies: **11**.
- Source conflicts: **5**.
- Normative ambiguity: **1** (Table 19 item 84).

These counts remain PROJECT_STATE/AUDIT_DERIVED and are not promoted to normative proof.
