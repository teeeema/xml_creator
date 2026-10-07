---
id: "P.SP.02.MSG.001:34:32"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.001"
requirement: "32"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 521
source_table: "Table 34, item 32"
source_item: "REQ 32 (Table 34)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.001:34:32

## Нормативное требование

если в состав электронного документа (сведений) включен и заполнен экземпляр реквизита «Приоритет товарного знака Союза» (ipcdo:TrademarkPriorityDetails), то значение реквизита «Код вида приоритета товарного знака Союза» (ipsdo:PriorityKindCode) в его составе должно соответствовать значению кода характеристики товарного знака по приоритету из справочника основных характеристик товарного знака и знака обслуживания Евразийского экономического союза (по виду и приоритету), утвержденного Решением Коллегии Комиссии от 29 ноября 2022 г. №184

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.001 → P.SP.02.TRN.001 → P.SP.02.MSG.001 → P.SP.02.MSG.001:34:32

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:TrademarkPriorityDetails; ipsdo:PriorityKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkPriorityDetails; ipsdo:PriorityKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 521
- Printed page: 109
- Table/item: Table 34, item 32
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_521]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 521, "source_id": "22OP-RULE-P.SP.02.MSG.001-32", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 521, "source_id": "22OP-RULE-P.SP.02.MSG.001-32", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg001_structured_rules.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Required document/priority kind or membership needs confirmed classifier/reference data.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
