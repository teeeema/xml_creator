---
id: "P.SP.02.MSG.021:54:1"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.021"
requirement: "1"
structure: "R.IP.SP.02.007"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 574
source_table: "Table 54, item 1"
source_item: "REQ 1 (Table 54)"
qname_status: "UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.021:54:1

## Нормативное требование

TrademarkId обязателен и должен соответствовать активной записи реестра со статусом «01» или «03».

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.030 → P.SP.02.TRN.019 → P.SP.02.MSG.021 → P.SP.02.MSG.021:54:1

## XML

- Structure: R.IP.SP.02.007
- QName: UNRESOLVED: see canonical source row
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 574
- Printed page: 162
- Table/item: Table 54, item 1
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_574]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: P.SP.02.MSG.021.T54.REQ.1
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 54", "page": 574, "source_id": "22OP-RULE-P.SP.02.MSG.021-T54-1", "status": "CONFIRMED", "table": "54", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 54", "page": 574, "source_id": "22OP-RULE-P.SP.02.MSG.021-T54-1", "status": "CONFIRMED", "table": "54", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["54"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg021_end_to_end.py; P.SP.02_OP_22/tests/test_msg021_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg021_safe_mapping.py

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Full source condition includes external resource/registry state; only local fragments, if any, execute.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
