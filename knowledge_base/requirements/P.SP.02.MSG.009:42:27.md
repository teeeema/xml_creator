---
id: "P.SP.02.MSG.009:42:27"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.009"
requirement: "27"
structure: "R.IP.SP.02.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 520
source_table: "Table 34, item 27"
source_item: "REQ 27 (Table 42)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.009:42:27

## Нормативное требование

если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида товарного знака» (ipsdo:TrademarkKindCode) или реквизита «Наименование вида товарного знака» (ipsdo:TrademarkKindName) соответствует одному из приведённых значений: «140» – «Изобразительный знак»; «150» – «Объемный знак»; «160» – «Знак, представляющий собой цвет»; «170» – «Знак, представляющий собой сочетание цветов»; «180» – «Комбинированный знак», то реквизит «Изображение товарного знака» (ipsdo:TrademarkColourName) и реквизит «Описание цвета товарного знака» должны быть заполнены

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.017 → P.SP.02.TRN.007 → P.SP.02.MSG.009 → P.SP.02.MSG.009:42:27

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:TrademarkDetails; ipsdo:TrademarkKindCode; ipsdo:TrademarkKindName; ipsdo:TrademarkColourName
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 520
- Printed page: 108
- Table/item: Table 34, item 27
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 42 item 27 via range 6-29 (PDF p.545)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_520]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 42. Требования к электронному документу (сведениям) P.SP.02.MSG.009", "page": 545, "source_id": "22OP-RULE-P.SP.02.MSG.009-T42-6-29", "status": "CONFIRMED", "table": "42", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "27", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 520, "source_id": "22OP-RULE-P.SP.02.MSG.001-27", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OTHER_OPEN
- Missing information: No executable production rule for this expanded source row. Generic capability availability is not production integration.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
