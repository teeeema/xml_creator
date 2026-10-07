---
id: "P.SP.02.MSG.032:50:1"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.032"
requirement: "1"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 563
source_table: "Table 50, item 1"
source_item: "REQ 1 (Table 50)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.032:50:1

## Нормативное требование

ipsdo:TrademarkId должен быть заполнен; в Едином реестре должна быть активная запись со статусом «01» или «03» и совпадающим TrademarkId.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.006 → P.SP.02.TRN.027 → P.SP.02.MSG.032 → P.SP.02.MSG.032:50:1

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 563
- Printed page: 151
- Table/item: Table 50, item 1
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_563]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 50", "page": 741, "source_id": "22OP-RULE-P.SP.02.MSG.032-T50-1", "status": "CONFIRMED", "table": "50", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 50", "page": 563, "source_id": "22OP-RULE-P.SP.02.MSG.017-T50-1", "status": "CONFIRMED", "table": "50", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["50"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
