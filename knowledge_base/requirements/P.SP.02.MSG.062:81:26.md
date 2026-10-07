---
id: "P.SP.02.MSG.062:81:26"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.062"
requirement: "26"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 818
source_table: "Table 81, item 26"
source_item: "REQ 26 (Table 81)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.062:81:26

## Нормативное требование

в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails), в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида товарного знака» (ipsdo:TrademarkKindCode) или реквизита «Наименование вида товарного знака» (ipsdo:TrademarkKindName) должны соответствовать одному из следующих значений: «110» – «Словесный знак»; «120» – «Буквенный знак»; «130» – «Цифровой знак»; «140» – «Изобразительный знак»; «150» – «Объемный знак»; «160» – «Знак, представляющий собой цвет»; «170» – «Знак, представляющий собой сочетание цветов»; «180» – «Комбинированный знак» в соответствии со справочником основных характеристик товарного знака и знака обслуживания Евразийского экономического союза (по виду и приоритету), утвержденным Решением Коллегии Комиссии от 29 ноября 2022 г. № 184

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.009 → P.SP.02.TRN.053 → P.SP.02.MSG.062 → P.SP.02.MSG.062:81:26

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 818
- Printed page: 239
- Table/item: Table 81, item 26
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_818]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 81. Требования к заполнению реквизитов структуры данных R.IP.SP.02.002 при передаче сведений об обращении о несоответствии заявки на товарный знак Союза требованиям Договора (P.SP.02.MSG.062)", "page": 818, "source_id": "22OP-RULE-P.SP.02.MSG.062-T81-6-29", "status": "CONFIRMED", "table": "81", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 81. Требования к заполнению реквизитов структуры данных R.IP.SP.02.002 при передаче сведений об обращении о несоответствии заявки на товарный знак Союза требованиям Договора (P.SP.02.MSG.062)", "page": 818, "source_id": "22OP-RULE-P.SP.02.MSG.062-T81-6-29", "status": "CONFIRMED", "table": "81", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["81"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
