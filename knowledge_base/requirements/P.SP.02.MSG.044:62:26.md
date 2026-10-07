---
id: "P.SP.02.MSG.044:62:26"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.044"
requirement: "26"
structure: "R.IP.SP.02.002"
status: "OPEN_SOURCE_CONFLICT"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 720
source_table: "Table 44, item 26"
source_item: "REQ 26 (Table 62)"
qname_status: "CONFLICT"
implementation_status: "OPEN_SOURCE_CONFLICT"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.044:62:26

## Нормативное требование

в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails), в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида товарного знака» (ipsdo:TrademarkKindCode) или реквизита «Наименование вида товарного знака» (ipsdo:TrademarkKindName) должны соответствовать одному из следующих значений: «110» – «Словесный знак»; «120» – «Буквенный знак»; «130» – «Цифровой знак»; «140» – «Изобразительный знак»; «150» – «Объемный знак»; «160» – «Знак, представляющий собой цвет»; «170» – «Знак, представляющий собой сочетание цветов»; «180» – «Комбинированный знак» в соответствии со справочником основных характеристик товарного знака и знака обслуживания Евразийского экономического союза (по виду и приоритету), утвержденным Решением Коллегии Комиссии от 29 ноября 2022 г. № 184

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_SOURCE_CONFLICT

## Trace

OP22 → P.SP.02.PRC.021 → P.SP.02.TRN.039 → P.SP.02.MSG.044 → P.SP.02.MSG.044:62:26

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:TrademarkApplicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 720
- Printed page: 141
- Table/item: Table 44, item 26
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 62 item 26 via range 6-29 (PDF p.772)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_720]]

## Project state

- Status: OPEN_SOURCE_CONFLICT
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 62", "page": 772, "source_id": "22OP-RULE-P.SP.02.MSG.044-T62-6-29", "status": "CONFIRMED", "table": "62", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "26", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 720, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-26", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg044_end_to_end.py; P.SP.02_OP_22/tests/test_msg044_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg044_safe_mapping.py

## Gap

- Reason: OPEN_SOURCE_CONFLICT
- Missing information: MSG044 captured source_refs identify Table58/physical760 instead of current Table62; no production rule for this requirement.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: A higher-priority authoritative source resolves the conflicting values; provenance is recorded and the conflicting mapping is replaced with the confirmed one.
