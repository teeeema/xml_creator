---
id: "P.SP.02.MSG.049:67:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.049"
requirement: "2"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 786
source_table: "Table 67, item 2"
source_item: "REQ 2 (Table 67)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.049:67:2

## Нормативное требование

в электронном документе (сведениях) должен быть заполнен 1 экземпляр реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.026 → P.SP.02.TRN.044 → P.SP.02.MSG.049 → P.SP.02.MSG.049:67:2

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 786
- Printed page: 207
- Table/item: Table 67, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_786]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 67", "page": 786, "source_id": "22OP-RULE-P.SP.02.MSG.049-T67-2", "status": "CONFIRMED", "table": "67", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 67", "page": 786, "source_id": "22OP-RULE-P.SP.02.MSG.049-T67-2", "status": "CONFIRMED", "table": "67", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["67"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
