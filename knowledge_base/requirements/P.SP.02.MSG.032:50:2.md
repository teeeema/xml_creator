---
id: "P.SP.02.MSG.032:50:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.032"
requirement: "2"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 563
source_table: "Table 50, item 2"
source_item: "REQ 2 (Table 50)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.032:50:2

## Нормативное требование

Должен быть заполнен 1 экземпляр ipcdo:UnifiedRegisterRecordsDetails.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.006 → P.SP.02.TRN.027 → P.SP.02.MSG.032 → P.SP.02.MSG.032:50:2

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPDocKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPDocKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 563
- Printed page: 151
- Table/item: Table 50, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_563]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.032.T50.REQ.2
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 50", "page": 741, "source_id": "22OP-RULE-P.SP.02.MSG.032-T50-2", "status": "CONFIRMED", "table": "50", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 50", "page": 563, "source_id": "22OP-RULE-P.SP.02.MSG.017-T50-2", "status": "CONFIRMED", "table": "50", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["50"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg032_end_to_end.py; P.SP.02_OP_22/tests/test_msg032_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg032_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
