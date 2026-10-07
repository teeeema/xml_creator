---
id: "P.SP.02.MSG.037:55:5"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.037"
requirement: "5"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 753
source_table: "Table 55, item 5"
source_item: "REQ 5 (Table 55)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.037:55:5

## Нормативное требование

в составе реквизита «Сведения о статусном состоянии» (ipcdo:IPEntityStatusDetails) значение реквизита «Код статуса» (csdo:StatusCode) должно соответствовать значению «31» – «заявка на ТЗ Союза отозвана (непредставление заявителем документа о согласии)», атрибут «идентификатор справочника (классификатора)» (атрибут codeListId) в составе реквизита «Код статуса» (csdo:StatusCode) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.013 → P.SP.02.TRN.032 → P.SP.02.MSG.037 → P.SP.02.MSG.037:55:5

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 753
- Printed page: 174
- Table/item: Table 55, item 5
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_753]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 55", "page": 753, "source_id": "22OP-RULE-P.SP.02.MSG.037-T55-5", "status": "CONFIRMED", "table": "55", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 55", "page": 753, "source_id": "22OP-RULE-P.SP.02.MSG.037-T55-5", "status": "CONFIRMED", "table": "55", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["55"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
