---
id: "P.SP.02.MSG.014:47:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.014"
requirement: "4"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 556
source_table: "Table 47, item 4"
source_item: "REQ 4 (Table 47)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.014:47:4

## Нормативное требование

при наличии в классификаторе соответствующего вида ходатайства о внесении изменений ipsdo:IPDocKindCode заполняется его кодом, ipsdo:IPDocKindName не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.022 → P.SP.02.TRN.012 → P.SP.02.MSG.014 → P.SP.02.MSG.014:47:4

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPDocKindCode; ipsdo:IPDocKindName

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 556
- Printed page: 144
- Table/item: Table 47, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_556]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 47. Требования к электронному документу (сведениям) P.SP.02.MSG.014", "page": 556, "source_id": "22OP-RULE-P.SP.02.MSG.014-T47-4", "status": "CONFIRMED", "table": "47", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 47. Требования к электронному документу (сведениям) P.SP.02.MSG.014", "page": 556, "source_id": "22OP-RULE-P.SP.02.MSG.014-T47-4", "status": "CONFIRMED", "table": "47", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["47"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
