---
id: "P.SP.02.MSG.038:56:31"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.038"
requirement: "31"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 756
source_table: "Table 56, item 31"
source_item: "REQ 31 (Table 56)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.038:56:31

## Нормативное требование

значение реквизита «Код вида приоритета товарного знака Союза» (ipsdo:PriorityKindCode) должно соответствовать значению кода характеристики товарного знака по приоритету из справочника основных характеристик товарного знака и знака обслуживания Евразийского экономического союза (по виду и приоритету), утвержденного Решением Коллегии Комиссии от 29 ноября 2022 г. №184

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.014 → P.SP.02.TRN.033 → P.SP.02.MSG.038 → P.SP.02.MSG.038:56:31

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:TrademarkApplicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 756
- Printed page: 177
- Table/item: Table 56, item 31
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_756]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "31", "location": "Таблица 56", "page": 756, "source_id": "22OP-RULE-P.SP.02.MSG.038-T56-31", "status": "CONFIRMED", "table": "56", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "31", "location": "Таблица 56", "page": 756, "source_id": "22OP-RULE-P.SP.02.MSG.038-T56-31", "status": "CONFIRMED", "table": "56", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["56"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg038_end_to_end.py; P.SP.02_OP_22/tests/test_msg038_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg038_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
