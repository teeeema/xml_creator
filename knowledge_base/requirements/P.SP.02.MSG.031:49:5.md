---
id: "P.SP.02.MSG.031:49:5"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.031"
requirement: "5"
structure: "R.010"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 562
source_table: "Table 49, item 5"
source_item: "REQ 5 (Table 49)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.031:49:5

## Нормативное требование

При отсутствии такого вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется нормативным наименованием.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.026 → P.SP.02.MSG.031 → P.SP.02.MSG.031:49:5

## XML

- Structure: R.010
- QName: ipcdo:TrademarkApplicationDetails; ipcdo:IPEntityStatusDetails; ipsdo:IPDocKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails; ipcdo:IPEntityStatusDetails; ipsdo:IPDocKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 562
- Printed page: 150
- Table/item: Table 49, item 5
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_562]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.031.T49.REQ.5
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 49", "page": 736, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-5", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 49", "page": 562, "source_id": "22OP-RULE-P.SP.02.MSG.016-T49-5", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg031_end_to_end.py; P.SP.02_OP_22/tests/test_msg031_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg031_rule_execution.py; P.SP.02_OP_22/tests/test_msg031_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
