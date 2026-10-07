---
id: "P.SP.02.MSG.059:78:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.059"
requirement: "4"
structure: "R.010"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 811
source_table: "Table 78, item 4"
source_item: "REQ 4 (Table 78)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.059:78:4

## Нормативное требование

в составе «Документ в бинарном формате» (csdo:DocBinaryText) атрибут «код формата данных» (атрибут mediaTypeCode) должен соответствовать одному из следующих значений: «tif», «tiff», «bmp», «jpg», «jpeg», «png», «gif», «doc», «docx», «rtf», «pdf», и размер документа в бинарном текстовом формате не должен превышать 5 Мб

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.036 → P.SP.02.TRN.051 → P.SP.02.MSG.059 → P.SP.02.MSG.059:78:4

## XML

- Structure: R.010
- QName: csdo:DocBinaryText
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 811
- Printed page: 232
- Table/item: Table 78, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_811]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.059.T78.REQ.4
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 78", "page": 811, "source_id": "22OP-RULE-P.SP.02.MSG.059-T78-4", "status": "CONFIRMED", "table": "78", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 78", "page": 811, "source_id": "22OP-RULE-P.SP.02.MSG.059-T78-4", "status": "CONFIRMED", "table": "78", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["78"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg059_end_to_end.py; P.SP.02_OP_22/tests/test_msg059_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg059_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
