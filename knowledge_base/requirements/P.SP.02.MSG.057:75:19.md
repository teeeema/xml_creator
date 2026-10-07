---
id: "P.SP.02.MSG.057:75:19"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.057"
requirement: "19"
structure: "R.IP.SP.03.003"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 807
source_table: "Table 74, item 19"
source_item: "REQ 19 (Table 75)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.057:75:19

## Нормативное требование

в составе реквизита «Прилагаемый документ» реквизит «Документ в бинарном формате» (csdo:DocBinaryText) заполняется обязательно, атрибут «код формата данных» (атрибут mediaTypeCode) должен соответствовать одному из следующих значений: «tif», «tiff», «bmp», «jpg», «jpeg», «png», «gif», «doc», «docx», «rtf», «pdf», и размер документа в бинарном текстовом формате не должен превышать 5 Мб

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.035 → P.SP.02.TRN.050 → P.SP.02.MSG.057 → P.SP.02.MSG.057:75:19

## XML

- Structure: R.IP.SP.03.003
- QName: csdo:DocBinaryText
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 807
- Printed page: 228
- Table/item: Table 74, item 19
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 75 item 19 via range 1-19 (PDF p.807)
- Inherited source chain: 74
- Source page: [[sources/OP22_P_SP_02/pages/page_807]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.057.T75.REQ.19
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1-19", "location": "Таблица 75", "page": 807, "source_id": "22OP-RULE-P.SP.02.MSG.057-T75-1-19", "status": "CONFIRMED", "table": "75", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "19", "location": "Таблица 74", "page": 807, "source_id": "22OP-RULE-P.SP.02.MSG.056-T74-19", "status": "CONFIRMED", "table": "74", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["74"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg057_end_to_end.py; P.SP.02_OP_22/tests/test_msg057_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg057_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
