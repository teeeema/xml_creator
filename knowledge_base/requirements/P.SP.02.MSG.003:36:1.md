---
id: "P.SP.02.MSG.003:36:1"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.003"
requirement: "1"
structure: "R.010"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 524
source_table: "Table 36, item 1"
source_item: "REQ 1 (Table 36)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.003:36:1

## Нормативное требование

реквизит «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) должен быть заполнен. В информационных ресурсах Комиссии, содержащих сведения о заявках на ТЗ Союза, должна содержаться запись, у которой реквизит «Код статуса» (csdo:StatusCode) равен значению «01» – «новая заявка на ТЗ Союза» или «02» – «заявка на ТЗ Союза изменена», реквизит «Конечная дата и время» (csdo:EndDateTime) не заполнен и в составе которой значение реквизита «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) совпадает со значением реквизита «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) в составе сообщения

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.002 → P.SP.02.MSG.003 → P.SP.02.MSG.003:36:1

## XML

- Structure: R.010
- QName: ipsdo:TrademarkApplicationId; csdo:StatusCode; csdo:EndDateTime
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 524
- Printed page: 112
- Table/item: Table 36, item 1
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_524]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: P.SP.02.MSG.003.T36.REQ.1
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 36. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 524, "source_id": "22OP-RULE-P.SP.02.MSG.003-T36-1", "status": "CONFIRMED", "table": "36", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 36. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 524, "source_id": "22OP-RULE-P.SP.02.MSG.003-T36-1", "status": "CONFIRMED", "table": "36", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["36"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg003_embedded_one_of.py; P.SP.02_OP_22/tests/test_msg003_repeatable_xml_alignment.py; P.SP.02_OP_22/tests/test_msg003_table36_full_rules.py; P.SP.02_OP_22/tests/test_msg003_table36_safe_partial_inherited.py; P.SP.02_OP_22/tests/test_msg003_table37_safe_mapping.py

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Full source condition includes external resource/registry state; only local fragments, if any, execute.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
