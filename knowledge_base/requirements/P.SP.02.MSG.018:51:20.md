---
id: "P.SP.02.MSG.018:51:20"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.018"
requirement: "20"
structure: "R.IP.SP.02.007"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 566
source_table: "Table 51, item 20"
source_item: "REQ 20 (Table 51)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.018:51:20

## Нормативное требование

при включении в классификатор видов документов, сведений и материалов значения, соответствующего виду документа «Заявление о внесении изменений в сведения Единого реестра товарных знаков, знаков обслуживания Евразийского экономического союза», реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) должен быть заполнен и должен содержать кодовое обозначение указанного вида документа, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.026 → P.SP.02.TRN.016 → P.SP.02.MSG.018 → P.SP.02.MSG.018:51:20

## XML

- Structure: R.IP.SP.02.007
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 566
- Printed page: 154
- Table/item: Table 51, item 20
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_566]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.018.REQ.20
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "20", "location": "Таблица 51. Требования к заполнению реквизитов P.SP.02.MSG.018", "page": 566, "source_id": "22OP-RULE-P.SP.02.MSG.018-T51-20", "status": "CONFIRMED", "table": "51", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "20", "location": "Таблица 51. Требования к заполнению реквизитов P.SP.02.MSG.018", "page": 566, "source_id": "22OP-RULE-P.SP.02.MSG.018-T51-20", "status": "CONFIRMED", "table": "51", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["51"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Full source condition requires classifier/reference data; no invented membership/code/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
