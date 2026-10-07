---
id: "P.SP.02.MSG.013:46:3"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.013"
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

# P.SP.02.MSG.013:46:3

## Нормативное требование

при отсутствии указанного вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется нормативным наименованием ходатайства

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.021 → P.SP.02.TRN.011 → P.SP.02.MSG.013 → P.SP.02.MSG.013:46:3

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPDocKindCode; ipsdo:IPDocKindName

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
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 46. Требования к электронному документу (сведениям) P.SP.02.MSG.013", "page": 553, "source_id": "22OP-RULE-P.SP.02.MSG.013-T46-3", "status": "CONFIRMED", "table": "46", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 46. Требования к электронному документу (сведениям) P.SP.02.MSG.013", "page": 553, "source_id": "22OP-RULE-P.SP.02.MSG.013-T46-3", "status": "CONFIRMED", "table": "46", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["46"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Required document/priority kind or membership needs confirmed classifier/reference data.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
