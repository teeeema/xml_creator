---
id: "P.SP.02.MSG.050:68:1"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.050"
requirement: "1"
structure: "R.IP.SP.02.007"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 788
source_table: "Table 68, item 1"
source_item: "REQ 1 (Table 68)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.050:68:1

## Нормативное требование

реквизит «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) должен быть заполнен. В информационных ресурсах национального патентного ведомства, содержащих сведения о ТЗ Союза, должна содержаться запись, у которой реквизит «Код статуса» (csdo:StatusCode) равен значению «01» – «ТЗ Союза зарегистрирован», «03» – «сведения о ТЗ Союза изменены», реквизит «Конечная дата и время» (csdo:EndDateTime) не заполнен, а значение реквизита «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) совпадает со значением реквизита «Регистрационный номер товарного знака Союза» в составе сообщения

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.027 → P.SP.02.TRN.045 → P.SP.02.MSG.050 → P.SP.02.MSG.050:68:1

## XML

- Structure: R.IP.SP.02.007
- QName: ipsdo:TrademarkId
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 788
- Printed page: 209
- Table/item: Table 68, item 1
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_788]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.050.T68.REQ.1
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 68", "page": 788, "source_id": "22OP-RULE-P.SP.02.MSG.050-T68-1", "status": "CONFIRMED", "table": "68", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 68", "page": 788, "source_id": "22OP-RULE-P.SP.02.MSG.050-T68-1", "status": "CONFIRMED", "table": "68", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["68"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg050_end_to_end.py; P.SP.02_OP_22/tests/test_msg050_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg050_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
