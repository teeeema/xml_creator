---
id: "P.SP.02.MSG.045:63:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.045"
requirement: "2"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 773
source_table: "Table 63, item 2"
source_item: "REQ 2 (Table 63)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.045:63:2

## Нормативное требование

в информационных ресурсах национального патентного ведомства, содержащих сведения о заявках на ТЗ Союза, должна содержаться запись, в составе которой реквизит «Код статуса» (csdo:StatusCode) равен значению «01» – «новая заявка на ТЗ Союза» или «02» – «заявка на ТЗ Союза изменена», реквизит «Конечная дата и время» (csdo:EndDateTime) не заполнен и в составе которой совокупность значений реквизитов «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId), «Код статуса» (csdo:StatusCode) и «Начальная дата и время» (csdo:StartDateTime) совпадает с совокупностью значений соответствующих реквизитов в представляемых изменяемых сведениях о заявке на ТЗ Союза

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.022 → P.SP.02.TRN.040 → P.SP.02.MSG.045 → P.SP.02.MSG.045:63:2

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:TrademarkApplicationId
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 773
- Printed page: 194
- Table/item: Table 63, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_773]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 63", "page": 773, "source_id": "22OP-RULE-P.SP.02.MSG.045-T63-2", "status": "CONFIRMED", "table": "63", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 63", "page": 773, "source_id": "22OP-RULE-P.SP.02.MSG.045-T63-2", "status": "CONFIRMED", "table": "63", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["63"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg045_end_to_end.py; P.SP.02_OP_22/tests/test_msg045_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg045_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
