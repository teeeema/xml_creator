---
id: "P.SP.02.MSG.043:61:33"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.043"
requirement: "33"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 769
source_table: "Table 61, item 33"
source_item: "REQ 33 (Table 61)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.043:61:33

## Нормативное требование

в составе реквизита «Технологические характеристики записи общего ресурса» (ccdo:ResourceItemStatusDetails) реквизит «Начальная дата и время» (csdo:StartDateTime) заполняется обязательно

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.020 → P.SP.02.TRN.038 → P.SP.02.MSG.043 → P.SP.02.MSG.043:61:33

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 769
- Printed page: 190
- Table/item: Table 61, item 33
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_769]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "33", "location": "Таблица 61", "page": 769, "source_id": "22OP-RULE-P.SP.02.MSG.043-T61-33", "status": "CONFIRMED", "table": "61", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "33", "location": "Таблица 61", "page": 769, "source_id": "22OP-RULE-P.SP.02.MSG.043-T61-33", "status": "CONFIRMED", "table": "61", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["61"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
