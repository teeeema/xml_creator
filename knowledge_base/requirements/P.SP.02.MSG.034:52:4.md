---
id: "P.SP.02.MSG.034:52:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.034"
requirement: "4"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 567
source_table: "Table 52, item 4"
source_item: "REQ 4 (Table 52)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.034:52:4

## Нормативное требование

При наличии вида ходатайства об отказе от исключительного права ipsdo:IPDocKindCode заполняется кодом, ipsdo:IPDocKindName не заполняется.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.010 → P.SP.02.TRN.029 → P.SP.02.MSG.034 → P.SP.02.MSG.034:52:4

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:TrademarkApplicationId
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 567
- Printed page: 155
- Table/item: Table 52, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_567]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.034.T52.REQ.4
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 52", "page": 747, "source_id": "22OP-RULE-P.SP.02.MSG.034-T52-4", "status": "CONFIRMED", "table": "52", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 52", "page": 567, "source_id": "22OP-RULE-P.SP.02.MSG.019-T52-4", "status": "CONFIRMED", "table": "52", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["52"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg034_end_to_end.py; P.SP.02_OP_22/tests/test_msg034_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg034_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
