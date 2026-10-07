---
id: "P.SP.02.MSG.004:38:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.004"
requirement: "4"
structure: "R.IP.SP.02.002"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 532
source_table: "Table 38, item 4"
source_item: "REQ 4 (Table 38)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.004:38:4

## Нормативное требование

реквизит «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) должен быть заполнен. В информационных ресурсах Комиссии, содержащих сведения о заявках на ТЗ Союза, должна содержаться запись, у которой значение реквизита «Код статуса» (csdo:StatusCode) соответствует значениям «01» – «новая заявка на ТЗ Союза» или «02» – «заявка на ТЗ Союза изменена», в составе которой значение реквизита «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) совпадает со значением реквизита «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) в составе сообщения

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.008 → P.SP.02.TRN.003 → P.SP.02.MSG.004 → P.SP.02.MSG.004:38:4

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:TrademarkApplicationId; csdo:StatusCode
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 532
- Printed page: 120
- Table/item: Table 38, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_532]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: P.SP.02.MSG.004.REQ.4
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 38. Требования к электронному документу (сведениям) P.SP.02.MSG.004", "page": 532, "source_id": "22OP-RULE-P.SP.02.MSG.004-4", "status": "CONFIRMED", "table": "38", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 38. Требования к электронному документу (сведениям) P.SP.02.MSG.004", "page": 532, "source_id": "22OP-RULE-P.SP.02.MSG.004-4", "status": "CONFIRMED", "table": "38", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["38"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg004_end_to_end.py; P.SP.02_OP_22/tests/test_msg004_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg004_safe_mapping.py

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Full source condition includes external resource/registry state; only local fragments, if any, execute.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
