---
id: "P.SP.02.MSG.049:67:21"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.049"
requirement: "21"
structure: "R.IP.SP.02.007"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 786
source_table: "Table 67, item 21"
source_item: "REQ 21 (Table 67)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.049:67:21

## Нормативное требование

при включении в классификатор видов документов, сведений и материалов значения, соответствующего виду документа «Заявление о внесении изменений в сведения Единого реестра товарных знаков, знаков обслуживания Евразийского экономического союза», реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) должен быть заполнен и должен содержать кодовое обозначение указанного вида документа, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.026 → P.SP.02.TRN.044 → P.SP.02.MSG.049 → P.SP.02.MSG.049:67:21

## XML

- Structure: R.IP.SP.02.007
- QName: ipsdo:IPDocKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:UnifiedRegisterRecordsDetails/ipsdo:IPDocKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 786
- Printed page: 207
- Table/item: Table 67, item 21
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_786]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.049.T67.REQ.21
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "21", "location": "Таблица 67", "page": 786, "source_id": "22OP-RULE-P.SP.02.MSG.049-T67-21", "status": "CONFIRMED", "table": "67", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "21", "location": "Таблица 67", "page": 786, "source_id": "22OP-RULE-P.SP.02.MSG.049-T67-21", "status": "CONFIRMED", "table": "67", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["67"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg049_end_to_end.py; P.SP.02_OP_22/tests/test_msg049_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg049_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
