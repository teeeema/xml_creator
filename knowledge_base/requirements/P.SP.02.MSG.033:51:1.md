---
id: "P.SP.02.MSG.033:51:1"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.033"
requirement: "1"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 565
source_table: "Table 51, item 1"
source_item: "REQ 1 (Table 51)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.033:51:1

## Нормативное требование

реквизит «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) должен быть заполнен. В Едином реестре ТЗ Союза должна содержаться запись, у которой реквизит «Код статуса» (csdo:StatusCode) равен значению «01» – «ТЗ Союза зарегистрирован» или «03» – «сведения о ТЗ Союза изменены», реквизит «Конечная дата и время» (csdo:EndDateTime) не заполнен, а значение реквизита «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) совпадает со значением реквизита «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) в составе сообщения

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.007 → P.SP.02.TRN.028 → P.SP.02.MSG.033 → P.SP.02.MSG.033:51:1

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 565
- Printed page: MISSING / UNRESOLVED
- Table/item: Table 51, item 1
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_565]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 51", "page": 743, "source_id": "22OP-RULE-P.SP.02.MSG.033-T51-1", "status": "CONFIRMED", "table": "51", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 51. Требования к заполнению реквизитов P.SP.02.MSG.018", "page": 565, "source_id": "22OP-RULE-P.SP.02.MSG.018-T51-1", "status": "CONFIRMED", "table": "51", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["51"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
