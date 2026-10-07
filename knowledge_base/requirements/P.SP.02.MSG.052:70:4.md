---
id: "P.SP.02.MSG.052:70:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.052"
requirement: "4"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 794
source_table: "Table 70, item 4"
source_item: "REQ 4 (Table 70)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.052:70:4

## Нормативное требование

в составе экземпляра реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), содержащего сведения о регистрации нового ТЗ Союза, в составе реквизита «Сведения о статусном состоянии» (ipcdo:IPEntityStatusDetails) реквизит «Дата» (csdo:EventDate) должен быть заполнен, значение реквизита «Код статуса» (csdo:StatusCode) должно соответствовать значению «01» – «ТЗ Союза зарегистрирован», а атрибут «идентификатор справочника (классификатора)» (атрибут codeListId) в составе реквизита «Код статуса» (csdo:StatusCode) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.029 → P.SP.02.TRN.047 → P.SP.02.MSG.052 → P.SP.02.MSG.052:70:4

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 794
- Printed page: 215
- Table/item: Table 70, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_794]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 70", "page": 794, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-4", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 70", "page": 794, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-4", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["70"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
