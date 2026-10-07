---
id: "P.SP.02.MSG.034:52:33"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.034"
requirement: "33"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 748
source_table: "Table 52, item 33"
source_item: "REQ 33 (Table 52)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.034:52:33

## Нормативное требование

в составе реквизита «Технологические характеристики записи общего ресурса» (ccdo:ResourceItemStatusDetails) реквизит «Начальная дата и время» (csdo:StartDateTime) заполняется обязательно

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.010 → P.SP.02.TRN.029 → P.SP.02.MSG.034 → P.SP.02.MSG.034:52:33

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 748
- Printed page: 169
- Table/item: Table 52, item 33
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_748]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "33", "location": "Таблица 52", "page": 748, "source_id": "22OP-RULE-P.SP.02.MSG.034-T52-33", "status": "CONFIRMED", "table": "52", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "33", "location": "Таблица 52", "page": 748, "source_id": "22OP-RULE-P.SP.02.MSG.034-T52-33", "status": "CONFIRMED", "table": "52", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["52"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
