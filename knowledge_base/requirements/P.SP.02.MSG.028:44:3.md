---
id: "P.SP.02.MSG.028:44:3"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.028"
requirement: "3"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 548
source_table: "Table 44, item 3"
source_item: "REQ 3 (Table 44)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.028:44:3

## Нормативное требование

при отсутствии такого вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется нормативным наименованием ходатайства

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.002 → P.SP.02.TRN.023 → P.SP.02.MSG.028 → P.SP.02.MSG.028:44:3

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:TrademarkApplicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 548
- Printed page: 136
- Table/item: Table 44, item 3
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_548]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.028.T44.REQ.3
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 714, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-3", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 44. Требования к электронному документу (сведениям) P.SP.02.MSG.011", "page": 548, "source_id": "22OP-RULE-P.SP.02.MSG.011-T44-3", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg028_end_to_end.py; P.SP.02_OP_22/tests/test_msg028_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg028_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
