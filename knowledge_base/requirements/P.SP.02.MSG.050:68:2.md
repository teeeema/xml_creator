---
id: "P.SP.02.MSG.050:68:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.050"
requirement: "2"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 788
source_table: "Table 68, item 2"
source_item: "REQ 2 (Table 68)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.050:68:2

## Нормативное требование

в электронном документе (сведениях) должен быть заполнен 1 экземпляр реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.027 → P.SP.02.TRN.045 → P.SP.02.MSG.050 → P.SP.02.MSG.050:68:2

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 788
- Printed page: 209
- Table/item: Table 68, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_788]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 68", "page": 788, "source_id": "22OP-RULE-P.SP.02.MSG.050-T68-2", "status": "CONFIRMED", "table": "68", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 68", "page": 788, "source_id": "22OP-RULE-P.SP.02.MSG.050-T68-2", "status": "CONFIRMED", "table": "68", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["68"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
