---
id: "P.SP.02.MSG.016:49:1"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.016"
requirement: "1"
structure: "R.IP.SP.02.007"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 561
source_table: "Table 49, item 1"
source_item: "REQ 1 (Table 49)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.016:49:1

## Нормативное требование

ipsdo:TrademarkId должен быть заполнен; в Едином реестре должна быть активная запись со статусом «01» или «03» и совпадающим TrademarkId.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.024 → P.SP.02.TRN.014 → P.SP.02.MSG.016 → P.SP.02.MSG.016:49:1

## XML

- Structure: R.IP.SP.02.007
- QName: ipsdo:TrademarkId
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 561
- Printed page: 149
- Table/item: Table 49, item 1
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_561]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: P.SP.02.MSG.016.REQ.1
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 49", "page": 561, "source_id": "22OP-RULE-P.SP.02.MSG.016-T49-1", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 49", "page": 561, "source_id": "22OP-RULE-P.SP.02.MSG.016-T49-1", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg016_019_end_to_end.py; P.SP.02_OP_22/tests/test_msg016_019_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg016_019_safe_mapping.py

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Full source condition includes external resource/registry state; only local fragments, if any, execute.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
