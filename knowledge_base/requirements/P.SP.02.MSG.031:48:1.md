---
id: "P.SP.02.MSG.031:48:1"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.031"
requirement: "1"
structure: "R.010"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 559
source_table: "Table 48, item 1"
source_item: "REQ 1 (Table 48)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.031:48:1

## Нормативное требование

При наличии в классификаторе вида документа «Ходатайство о преобразовании аннулированной регистрации ... в национальную заявку ...» ipsdo:IPDocKindCode заполняется кодом, ipsdo:IPDocKindName не заполняется.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.026 → P.SP.02.MSG.031 → P.SP.02.MSG.031:48:1

## XML

- Structure: R.010
- QName: ipcdo:TrademarkApplicationDetails; ipcdo:UnifiedRegisterRecordsDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails; ipcdo:UnifiedRegisterRecordsDetails

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 559
- Printed page: 147
- Table/item: Table 48, item 1
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_559]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.031.T48.REQ.1
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 48", "page": 733, "source_id": "22OP-RULE-P.SP.02.MSG.031-T48-1", "status": "CONFIRMED", "table": "48", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 48", "page": 559, "source_id": "22OP-RULE-P.SP.02.MSG.015-T48-1", "status": "CONFIRMED", "table": "48", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["48"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg031_end_to_end.py; P.SP.02_OP_22/tests/test_msg031_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg031_rule_execution.py; P.SP.02_OP_22/tests/test_msg031_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
