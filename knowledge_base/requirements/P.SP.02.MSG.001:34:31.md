---
id: "P.SP.02.MSG.001:34:31"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.001"
requirement: "31"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 521
source_table: "Table 34, item 31"
source_item: "REQ 31 (Table 34)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.001:34:31

## Нормативное требование

если в состав электронного документа (сведений) включен экземпляр реквизита «Приоритет товарного знака Союза» (ipcdo:TrademarkPriorityDetails), то в составе такого экземпляра реквизита «Приоритет товарного знака Союза» должны быть заполнены реквизиты: «Код вида приоритета товарного знака Союза» (ipsdo:PriorityKindCode); «Наименование вида приоритета товарного знака Союза» (ipsdo:PriorityKindName); «Дата приоритета товарного знака» (ipsdo:PriorityDate); «Код страны» (csdo:UnifiedCountryCode). Реквизиты «Место проведения выставки» (ipsdo:ExhibitionSiteText), «Регистрационный номер первой заявки на товарный знак при испрашивании конвенционного приоритета» (ipsdo:FirstTrademarkApplicationId) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.001 → P.SP.02.TRN.001 → P.SP.02.MSG.001 → P.SP.02.MSG.001:34:31

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 521
- Printed page: 109
- Table/item: Table 34, item 31
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_521]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "31", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 521, "source_id": "22OP-RULE-P.SP.02.MSG.001-31", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "31", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 521, "source_id": "22OP-RULE-P.SP.02.MSG.001-31", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
