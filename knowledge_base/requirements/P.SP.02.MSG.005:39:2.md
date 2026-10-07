---
id: "P.SP.02.MSG.005:39:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.005"
requirement: "2"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 535
source_table: "Table 39, item 2"
source_item: "REQ 2 (Table 39)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.005:39:2

## Нормативное требование

при включении в классификатор видов документов, сведений и материалов значения, соответствующего виду документа «Доводы заявителя в отношении обращения заинтересованного лица о наличии оснований для отказа в регистрации товарного знака, знака обслуживания Евразийского экономического союза, предусмотренных статьей 8 Договора о товарных знаках, знаках обслуживания и наименованиях мест происхождения товаров Евразийского экономического союза от 3 февраля 2020 года», реквизит ipsdo:IPDocKindCode должен быть заполнен кодовым обозначением указанного вида документа, а ipsdo:IPDocKindName не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.009 → P.SP.02.TRN.004 → P.SP.02.MSG.005 → P.SP.02.MSG.005:39:2

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPDocKindCode; ipsdo:IPDocKindName

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 535
- Printed page: 123
- Table/item: Table 39, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_535]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 39. Требования к электронному документу (сведениям) P.SP.02.MSG.005", "page": 535, "source_id": "22OP-RULE-P.SP.02.MSG.005-T39-2", "status": "CONFIRMED", "table": "39", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 39. Требования к электронному документу (сведениям) P.SP.02.MSG.005", "page": 535, "source_id": "22OP-RULE-P.SP.02.MSG.005-T39-2", "status": "CONFIRMED", "table": "39", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["39"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg005_end_to_end.py; P.SP.02_OP_22/tests/test_msg005_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg005_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
