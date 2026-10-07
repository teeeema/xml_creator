---
id: "P.SP.02.MSG.007:41:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.007"
requirement: "2"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 541
source_table: "Table 41, item 2"
source_item: "REQ 2 (Table 41)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.007:41:2

## Нормативное требование

при наличии вида документа «Другие документы, подтверждающие правомочность требования установления приоритета более раннего, чем дата подачи заявки на товарный знак (знак обслуживания) Евразийского экономического союза» ipsdo:IPDocKindCode заполняется его кодом, ipsdo:IPDocKindName не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.014 → P.SP.02.TRN.006 → P.SP.02.MSG.007 → P.SP.02.MSG.007:41:2

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPDocKindCode; ipsdo:IPDocKindName

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 541
- Printed page: 129
- Table/item: Table 41, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_541]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 41. Требования к электронному документу (сведениям) P.SP.02.MSG.007", "page": 541, "source_id": "22OP-RULE-P.SP.02.MSG.007-T41-2", "status": "CONFIRMED", "table": "41", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 41. Требования к электронному документу (сведениям) P.SP.02.MSG.007", "page": 541, "source_id": "22OP-RULE-P.SP.02.MSG.007-T41-2", "status": "CONFIRMED", "table": "41", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["41"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Required document/priority kind or membership needs confirmed classifier/reference data.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
