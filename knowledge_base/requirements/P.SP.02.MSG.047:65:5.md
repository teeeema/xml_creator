---
id: "P.SP.02.MSG.047:65:5"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.047"
requirement: "5"
structure: "R.IP.SP.02.007"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 781
source_table: "Table 65, item 5"
source_item: "REQ 5 (Table 65)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.047:65:5

## Нормативное требование

при отсутствии в классификаторе видов документов, сведений и материалов значения, соответствующего виду документа «Ходатайство о преобразовании коллективного знака Евразийского экономического союза в товарный знак, знак обслуживания Евразийского экономического союза», реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) не заполняется, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) должен быть заполнен, и его значение должно соответствовать значению «Ходатайство о преобразовании коллективного знака Евразийского экономического союза в товарный знак, знак обслуживания Евразийского экономического союза»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.024 → P.SP.02.TRN.042 → P.SP.02.MSG.047 → P.SP.02.MSG.047:65:5

## XML

- Structure: R.IP.SP.02.007
- QName: ipsdo:IPDocKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:UnifiedRegisterRecordsDetails/ipsdo:IPDocKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 781
- Printed page: 202
- Table/item: Table 65, item 5
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_781]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.047.T65.REQ.5
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 65", "page": 781, "source_id": "22OP-RULE-P.SP.02.MSG.047-T65-5", "status": "CONFIRMED", "table": "65", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 65", "page": 781, "source_id": "22OP-RULE-P.SP.02.MSG.047-T65-5", "status": "CONFIRMED", "table": "65", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["65"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg047_end_to_end.py; P.SP.02_OP_22/tests/test_msg047_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg047_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
