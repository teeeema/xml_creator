---
id: "P.SP.02.MSG.007:41:31"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.007"
requirement: "31"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 543
source_table: "Table 41, item 31"
source_item: "REQ 31 (Table 41)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.007:41:31

## Нормативное требование

ipsdo:PriorityKindCode должен соответствовать коду характеристики товарного знака по приоритету из нормативного справочника

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.014 → P.SP.02.TRN.006 → P.SP.02.MSG.007 → P.SP.02.MSG.007:41:31

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:PriorityKindCode
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 543
- Printed page: 131
- Table/item: Table 41, item 31
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_543]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.007.REQ.31
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "31", "location": "Таблица 41. Требования к электронному документу (сведениям) P.SP.02.MSG.007", "page": 543, "source_id": "22OP-RULE-P.SP.02.MSG.007-T41-31", "status": "CONFIRMED", "table": "41", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "31", "location": "Таблица 41. Требования к электронному документу (сведениям) P.SP.02.MSG.007", "page": 543, "source_id": "22OP-RULE-P.SP.02.MSG.007-T41-31", "status": "CONFIRMED", "table": "41", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["41"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Full source condition requires classifier/reference data; no invented membership/code/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
