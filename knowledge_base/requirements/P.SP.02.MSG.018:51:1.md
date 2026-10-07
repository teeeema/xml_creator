---
id: "P.SP.02.MSG.018:51:1"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.018"
requirement: "1"
structure: "R.IP.SP.02.007"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 565
source_table: "Table 51, item 1"
source_item: "REQ 1 (Table 51)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.018:51:1

## Нормативное требование

реквизит «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) должен быть заполнен. В Едином реестре ТЗ Союза должна содержаться запись, у которой реквизит «Код статуса» (csdo:StatusCode) равен значению «01» – «ТЗ Союза зарегистрирован» или «03» – «сведения о ТЗ Союза изменены», реквизит «Конечная дата и время» (csdo:EndDateTime) не заполнен, а значение реквизита «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) совпадает со значением реквизита «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) в составе сообщения

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.026 → P.SP.02.TRN.016 → P.SP.02.MSG.018 → P.SP.02.MSG.018:51:1

## XML

- Structure: R.IP.SP.02.007
- QName: ipsdo:TrademarkId; csdo:StatusCode; csdo:EndDateTime
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 565
- Printed page: MISSING / UNRESOLVED
- Table/item: Table 51, item 1
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_565]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: P.SP.02.MSG.018.REQ.1
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 51. Требования к заполнению реквизитов P.SP.02.MSG.018", "page": 565, "source_id": "22OP-RULE-P.SP.02.MSG.018-T51-1", "status": "CONFIRMED", "table": "51", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 51. Требования к заполнению реквизитов P.SP.02.MSG.018", "page": 565, "source_id": "22OP-RULE-P.SP.02.MSG.018-T51-1", "status": "CONFIRMED", "table": "51", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["51"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Full source condition includes external resource/registry state; only local fragments, if any, execute.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
