---
id: "P.SP.02.MSG.044:62:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.044"
requirement: "4"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 771
source_table: "Table 62, item 4"
source_item: "REQ 4 (Table 62)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.044:62:4

## Нормативное требование

реквизит «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) должен быть заполнен. В информационных ресурсах национального патентного ведомства, содержащих сведения о заявках на ТЗ Союза, должна содержаться запись, у которой реквизит «Код статуса» (csdo:StatusCode) равен значению «01» – «новая заявка на ТЗ Союза» или «02» – «заявка на ТЗ Союза изменена», реквизит «Конечная дата и время» (csdo:EndDateTime) не заполнен и в составе которой значение реквизита «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) совпадает со значением реквизита «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) в составе сообщения

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.021 → P.SP.02.TRN.039 → P.SP.02.MSG.044 → P.SP.02.MSG.044:62:4

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:TrademarkApplicationId
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 771
- Printed page: 192
- Table/item: Table 62, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_771]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 62", "page": 771, "source_id": "22OP-RULE-P.SP.02.MSG.044-T62-4", "status": "CONFIRMED", "table": "62", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 62", "page": 771, "source_id": "22OP-RULE-P.SP.02.MSG.044-T62-4", "status": "CONFIRMED", "table": "62", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["62"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg044_end_to_end.py; P.SP.02_OP_22/tests/test_msg044_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg044_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
