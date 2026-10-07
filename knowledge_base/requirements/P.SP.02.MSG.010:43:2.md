---
id: "P.SP.02.MSG.010:43:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.010"
requirement: "2"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 546
source_table: "Table 43, item 2"
source_item: "REQ 2 (Table 43)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.010:43:2

## Нормативное требование

при наличии вида документа о преобразовании заявки на коллективный знак Союза в заявку на ТЗ Союза ipsdo:IPDocKindCode заполняется кодом, ipsdo:IPDocKindName не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.018 → P.SP.02.TRN.008 → P.SP.02.MSG.010 → P.SP.02.MSG.010:43:2

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPDocKindCode; ipsdo:IPDocKindName

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 546
- Printed page: 134
- Table/item: Table 43, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_546]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 43. Требования к электронному документу (сведениям) P.SP.02.MSG.010", "page": 546, "source_id": "22OP-RULE-P.SP.02.MSG.010-T43-2", "status": "CONFIRMED", "table": "43", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 43. Требования к электронному документу (сведениям) P.SP.02.MSG.010", "page": 546, "source_id": "22OP-RULE-P.SP.02.MSG.010-T43-2", "status": "CONFIRMED", "table": "43", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["43"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Required document/priority kind or membership needs confirmed classifier/reference data.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
