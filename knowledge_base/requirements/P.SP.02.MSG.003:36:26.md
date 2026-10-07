---
id: "P.SP.02.MSG.003:36:26"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.003"
requirement: "26"
structure: "R.010"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 519
source_table: "Table 34, item 26"
source_item: "REQ 26 (Table 36)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.003:36:26

## Нормативное требование

в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails), в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида товарного знака» (ipsdo:TrademarkKindCode) или реквизита «Наименование вида товарного знака» (ipsdo:TrademarkKindName) должны соответствовать одному из следующих значений: «110» – «Словесный знак»; «120» – «Буквенный знак»; «130» – «Цифровой знак»; «140» – «Изобразительный знак»; «150» – «Объемный знак»; «160» – «Знак, представляющий собой цвет»; «170» – «Знак, представляющий собой сочетание цветов»; «180» – «Комбинированный знак» в соответствии со справочником основных характеристик товарного знака и знака обслуживания Евразийского экономического союза (по виду и приоритету), утвержденным Решением Коллегии Комиссии от 29 ноября 2022 г. № 184

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.002 → P.SP.02.MSG.003 → P.SP.02.MSG.003:36:26

## XML

- Structure: R.010
- QName: ipcdo:TrademarkApplicationDetails; ipcdo:TrademarkDetails; ipsdo:TrademarkKindCode; ipsdo:TrademarkKindName
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 519
- Printed page: 107
- Table/item: Table 34, item 26
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 36 item 26 via range 6-29 (PDF p.525)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_519]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 36. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 525, "source_id": "22OP-RULE-P.SP.02.MSG.003-T36-6-29", "status": "CONFIRMED", "table": "36", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "26", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 519, "source_id": "22OP-RULE-P.SP.02.MSG.001-26", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg003_embedded_one_of.py; P.SP.02_OP_22/tests/test_msg003_repeatable_xml_alignment.py; P.SP.02_OP_22/tests/test_msg003_table36_full_rules.py; P.SP.02_OP_22/tests/test_msg003_table36_safe_partial_inherited.py; P.SP.02_OP_22/tests/test_msg003_table37_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Full source condition requires classifier/reference data; no invented membership/code/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
