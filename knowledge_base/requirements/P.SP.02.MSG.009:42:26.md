---
id: "P.SP.02.MSG.009:42:26"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.009"
requirement: "26"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 519
source_table: "Table 34, item 26"
source_item: "REQ 26 (Table 42)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.009:42:26

## Нормативное требование

в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails), в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида товарного знака» (ipsdo:TrademarkKindCode) или реквизита «Наименование вида товарного знака» (ipsdo:TrademarkKindName) должны соответствовать одному из следующих значений: «110» – «Словесный знак»; «120» – «Буквенный знак»; «130» – «Цифровой знак»; «140» – «Изобразительный знак»; «150» – «Объемный знак»; «160» – «Знак, представляющий собой цвет»; «170» – «Знак, представляющий собой сочетание цветов»; «180» – «Комбинированный знак» в соответствии со справочником основных характеристик товарного знака и знака обслуживания Евразийского экономического союза (по виду и приоритету), утвержденным Решением Коллегии Комиссии от 29 ноября 2022 г. № 184

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.017 → P.SP.02.TRN.007 → P.SP.02.MSG.009 → P.SP.02.MSG.009:42:26

## XML

- Structure: R.IP.SP.02.002
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
- Applied by current table: Table 42 item 26 via range 6-29 (PDF p.545)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_519]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.009.T42.REQ.6_29
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 42. Требования к электронному документу (сведениям) P.SP.02.MSG.009", "page": 545, "source_id": "22OP-RULE-P.SP.02.MSG.009-T42-6-29", "status": "CONFIRMED", "table": "42", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "26", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 519, "source_id": "22OP-RULE-P.SP.02.MSG.001-26", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Full source condition requires classifier/reference data; no invented membership/code/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
