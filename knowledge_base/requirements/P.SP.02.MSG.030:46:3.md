---
id: "P.SP.02.MSG.030:46:3"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.030"
requirement: "3"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 553
source_table: "Table 46, item 3"
source_item: "REQ 3 (Table 46)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.030:46:3

## Нормативное требование

при отсутствии указанного вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется нормативным наименованием ходатайства

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.004 → P.SP.02.TRN.025 → P.SP.02.MSG.030 → P.SP.02.MSG.030:46:3

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPDocKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPDocKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 553
- Printed page: 141
- Table/item: Table 46, item 3
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_553]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.030.T46.REQ.3
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 46", "page": 729, "source_id": "22OP-RULE-P.SP.02.MSG.030-T46-3", "status": "CONFIRMED", "table": "46", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 46. Требования к электронному документу (сведениям) P.SP.02.MSG.013", "page": 553, "source_id": "22OP-RULE-P.SP.02.MSG.013-T46-3", "status": "CONFIRMED", "table": "46", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["46"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg030_end_to_end.py; P.SP.02_OP_22/tests/test_msg030_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg030_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
