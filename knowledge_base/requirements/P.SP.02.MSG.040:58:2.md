---
id: "P.SP.02.MSG.040:58:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.040"
requirement: "2"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 759
source_table: "Table 58, item 2"
source_item: "REQ 2 (Table 58)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.040:58:2

## Нормативное требование

при включении в классификатор видов документов, сведений и материалов значения, соответствующего виду документа «Ходатайство о преобразовании заявки на регистрацию товарного знака, знака обслуживания Евразийского экономического союза в национальную заявку на регистрацию товарного знака, знака обслуживания», в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails) реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) должен быть заполнен и должен содержать кодовое обозначение указанного вида документа, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.016 → P.SP.02.TRN.035 → P.SP.02.MSG.040 → P.SP.02.MSG.040:58:2

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:TrademarkApplicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 759
- Printed page: 180
- Table/item: Table 58, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_759]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 58", "page": 759, "source_id": "22OP-RULE-P.SP.02.MSG.040-T58-2", "status": "CONFIRMED", "table": "58", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 58", "page": 759, "source_id": "22OP-RULE-P.SP.02.MSG.040-T58-2", "status": "CONFIRMED", "table": "58", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["58"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg040_end_to_end.py; P.SP.02_OP_22/tests/test_msg040_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg040_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
