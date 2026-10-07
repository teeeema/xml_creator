---
id: "P.SP.02.MSG.014:47:5"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.014"
requirement: "5"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 557
source_table: "Table 47, item 5"
source_item: "REQ 5 (Table 47)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.014:47:5

## Нормативное требование

при отсутствии соответствующего вида ходатайства ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется соответствующим нормативным наименованием

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.022 → P.SP.02.TRN.012 → P.SP.02.MSG.014 → P.SP.02.MSG.014:47:5

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPDocKindCode; ipsdo:IPDocKindName

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 557
- Printed page: 145
- Table/item: Table 47, item 5
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_557]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 47. Требования к электронному документу (сведениям) P.SP.02.MSG.014", "page": 557, "source_id": "22OP-RULE-P.SP.02.MSG.014-T47-5", "status": "CONFIRMED", "table": "47", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 47. Требования к электронному документу (сведениям) P.SP.02.MSG.014", "page": 557, "source_id": "22OP-RULE-P.SP.02.MSG.014-T47-5", "status": "CONFIRMED", "table": "47", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["47"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Required document/priority kind or membership needs confirmed classifier/reference data.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
