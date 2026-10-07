---
id: "P.SP.02.MSG.001:34:33"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.001"
requirement: "33"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 521
source_table: "Table 34, item 33"
source_item: "REQ 33 (Table 34)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.001:34:33

## Нормативное требование

если в состав электронного документа (сведений) включен экземпляр реквизита «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails), то в составе такого экземпляра реквизита должны быть заполнены реквизиты: «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode); «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName); «Номер документа» (csdo:DocId); «Дата документа» (csdo:DocCreationDate); «Описание» (csdo:DescriptionText); «Количество листов» (csdo:PageQuantity)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.001 → P.SP.02.TRN.001 → P.SP.02.MSG.001 → P.SP.02.MSG.001:34:33

## XML

- Structure: R.IP.SP.02.002
- QName: csdo:DescriptionText; csdo:DocCreationDate; csdo:DocId; csdo:PageQuantity; ipcdo:AccompanyingDocumentsDetails; ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails; ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DescriptionText; ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocCreationDate; ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId; ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:PageQuantity; ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindCode; ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindName

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 521
- Printed page: 109
- Table/item: Table 34, item 33
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_521]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.001.REQ.033
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "33", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 521, "source_id": "22OP-RULE-P.SP.02.MSG.001-33", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "33", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 521, "source_id": "22OP-RULE-P.SP.02.MSG.001-33", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_document_fields_stay_with_each_document[positive]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_document_fields_stay_with_each_document[negative]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_document_fields_stay_with_each_document[negative]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_document_fields_stay_with_each_document[positive]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
