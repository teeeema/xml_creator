---
id: "P.SP.02.MSG.036:54:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.036"
requirement: "2"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 574
source_table: "Table 54, item 2"
source_item: "REQ 2 (Table 54)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.036:54:2

## Нормативное требование

Должен быть заполнен 1 экземпляр ipcdo:UnifiedRegisterRecordsDetails.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.012 → P.SP.02.TRN.031 → P.SP.02.MSG.036 → P.SP.02.MSG.036:54:2

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPDocKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipsdo:IPDocKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 574
- Printed page: 162
- Table/item: Table 54, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_574]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.036.T54.REQ.2
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 54", "page": 750, "source_id": "22OP-RULE-P.SP.02.MSG.036-T54-2", "status": "CONFIRMED", "table": "54", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 54", "page": 574, "source_id": "22OP-RULE-P.SP.02.MSG.021-T54-2", "status": "CONFIRMED", "table": "54", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["54"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg036_end_to_end.py; P.SP.02_OP_22/tests/test_msg036_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg036_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
