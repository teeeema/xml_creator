---
id: "P.SP.02.MSG.041:59:32"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.041"
requirement: "32"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 763
source_table: "Table 59, item 32"
source_item: "REQ 32 (Table 59)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.041:59:32

## Нормативное требование

в составе реквизита «Технологические характеристики записи общего ресурса» (ccdo:ResourceItemStatusDetails) реквизит «Конечная дата и время» (csdo:EndDateTime) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.018 → P.SP.02.TRN.036 → P.SP.02.MSG.041 → P.SP.02.MSG.041:59:32

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 763
- Printed page: 184
- Table/item: Table 59, item 32
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_763]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 59", "page": 763, "source_id": "22OP-RULE-P.SP.02.MSG.041-T59-32", "status": "CONFIRMED", "table": "59", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 59", "page": 763, "source_id": "22OP-RULE-P.SP.02.MSG.041-T59-32", "status": "CONFIRMED", "table": "59", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["59"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
