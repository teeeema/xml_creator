# Agent Start Here

1. Start with the Knowledge Base; open the original PDF/XSD only when KB evidence is insufficient, conflicting, stale, or ambiguous.
2. Keep `SOURCE`, `KNOWLEDGE`, and `PROJECT_STATE` separate.
3. `AUDIT_DERIVED` and `HISTORICAL` are not normative proof.
4. Never invent QName, namespace, version, classifier code, page, table, field path, or other missing normative data.
5. Before any production edit, inspect the current Git state because OP23/OP26 and shared code may be changing in parallel.
6. A production YAML rule by itself does not close a normative requirement.
7. Closure requires normative evidence + production mapping + positive test + negative test + runtime proof.
8. Canonical schema v1.0 data is under `data/`; generated machine indexes are under `indexes/`.
