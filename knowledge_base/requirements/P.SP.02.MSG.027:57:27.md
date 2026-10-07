---
id: "P.SP.02.MSG.027:57:27"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.027"
requirement: "27"
structure: "R.IP.SP.02.002"
status: "OPEN_SOURCE_CONFLICT"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 520
source_table: "Table 34, item 27"
source_item: "REQ 27 (Table 57)"
qname_status: "CONFLICT"
implementation_status: "OPEN_SOURCE_CONFLICT"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.027:57:27

## Нормативное требование

если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида товарного знака» (ipsdo:TrademarkKindCode) или реквизита «Наименование вида товарного знака» (ipsdo:TrademarkKindName) соответствует одному из приведённых значений: «140» – «Изобразительный знак»; «150» – «Объемный знак»; «160» – «Знак, представляющий собой цвет»; «170» – «Знак, представляющий собой сочетание цветов»; «180» – «Комбинированный знак», то реквизит «Изображение товарного знака» (ipsdo:TrademarkColourName) и реквизит «Описание цвета товарного знака» должны быть заполнены

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_SOURCE_CONFLICT

## Trace

OP22 → P.SP.02.PRC.034 → P.SP.02.TRN.022 → P.SP.02.MSG.027 → P.SP.02.MSG.027:57:27

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:TrademarkColourName; ipsdo:TrademarkColourPictureImage
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkDetails/ipsdo:TrademarkColourName; ipcdo:TrademarkDetails/ipsdo:TrademarkColourPictureImage

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 520
- Printed page: 108
- Table/item: Table 34, item 27
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 57 item 27 via range 6-29 (PDF p.579)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_520]]

## Project state

- Status: OPEN_SOURCE_CONFLICT
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 57. Требования к заполнению реквизитов P.SP.02.MSG.027", "page": 579, "source_id": "22OP-RULE-P.SP.02.MSG.027-T57-6-29", "status": "CONFIRMED", "table": "57", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "27", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 520, "source_id": "22OP-RULE-P.SP.02.MSG.001-27", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg027_end_to_end.py; P.SP.02_OP_22/tests/test_msg027_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg027_safe_mapping.py

## Gap

- Reason: OPEN_SOURCE_CONFLICT
- Missing information: Source/StructureDefinition owner or QName conflict retained; see source refs and original gap notes.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: A higher-priority authoritative source resolves the conflicting values; provenance is recorded and the conflicting mapping is replaced with the confirmed one.
