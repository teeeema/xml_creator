---
id: "P.SP.02.MSG.043:61:27"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.043"
requirement: "27"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 721
source_table: "Table 44, item 27"
source_item: "REQ 27 (Table 61)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.043:61:27

## Нормативное требование

если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида товарного знака» (ipsdo:TrademarkKindCode) или реквизита «Наименование вида товарного знака» (ipsdo:TrademarkKindName) соответствует одному из приведённых значений: «140» – «Изобразительный знак»; «150» – «Объемный знак»; «160» – «Знак, представляющий собой цвет»; «170» – «Знак, представляющий собой сочетание цветов»; «180» – «Комбинированный знак», то реквизит «Изображение товарного знака» (ipsdo:TrademarkPicture) и реквизит «Описание цвета товарного знака» (ipsdo:TrademarkColourName) должны быть заполнены

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.020 → P.SP.02.TRN.038 → P.SP.02.MSG.043 → P.SP.02.MSG.043:61:27

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 721
- Printed page: 142
- Table/item: Table 44, item 27
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 61 item 27 via range 6-29 (PDF p.768)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_721]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 61", "page": 768, "source_id": "22OP-RULE-P.SP.02.MSG.043-T61-6-29", "status": "CONFIRMED", "table": "61", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "27", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 721, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-27", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
