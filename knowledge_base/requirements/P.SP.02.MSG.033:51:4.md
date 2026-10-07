---
id: "P.SP.02.MSG.033:51:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.033"
requirement: "4"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 565
source_table: "Table 51, item 4"
source_item: "REQ 4 (Table 51)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.033:51:4

## Нормативное требование

в составе реквизита «Сведения записи Единого реестра ТЗ Союза» реквизит «Конечная дата и время» (csdo:EndDateTime) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.007 → P.SP.02.TRN.028 → P.SP.02.MSG.033 → P.SP.02.MSG.033:51:4

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPDocKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPDocKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 565
- Printed page: MISSING / UNRESOLVED
- Table/item: Table 51, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_565]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.033.T51.REQ.4
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 51", "page": 744, "source_id": "22OP-RULE-P.SP.02.MSG.033-T51-4", "status": "CONFIRMED", "table": "51", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 51. Требования к заполнению реквизитов P.SP.02.MSG.018", "page": 565, "source_id": "22OP-RULE-P.SP.02.MSG.018-T51-4", "status": "CONFIRMED", "table": "51", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["51"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg033_end_to_end.py; P.SP.02_OP_22/tests/test_msg033_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg033_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
