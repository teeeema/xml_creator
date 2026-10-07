---
id: "P.SP.02.MSG.001:34:22"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.001"
requirement: "22"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 518
source_table: "Table 34, item 22"
source_item: "REQ 22 (Table 34)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.001:34:22

## Нормативное требование

если в состав электронного документа (сведений) включен экземпляр реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), в составе которого значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «RE» – «представитель заявителя, не являющийся патентным поверенным», то в составе такого экземпляра реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должны быть заполнены реквизиты: «Код страны» (csdo:UnifiedCountryCode); «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName); «Адрес» (ccdo:SubjectAddressDetails); «Контактный реквизит» (ccdo:CommunicationDetails)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.001 → P.SP.02.TRN.001 → P.SP.02.MSG.001 → P.SP.02.MSG.001:34:22

## XML

- Structure: R.IP.SP.02.002
- QName: ccdo:CommunicationDetails; ccdo:SubjectAddressDetails; csdo:UnifiedCountryCode; ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ipsdo:IPSubjectName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ccdo:CommunicationDetails; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ccdo:SubjectAddressDetails; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/csdo:UnifiedCountryCode; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPSubjectName

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 518
- Printed page: 106
- Table/item: Table 34, item 22
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_518]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.001.REQ.022
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 518, "source_id": "22OP-RULE-P.SP.02.MSG.001-22", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 518, "source_id": "22OP-RULE-P.SP.02.MSG.001-22", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_filtered_fields_cannot_be_borrowed[positive-22-RE]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_filtered_fields_cannot_be_borrowed[negative-22-RE]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_filtered_fields_cannot_be_borrowed[negative-22-RE]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_filtered_fields_cannot_be_borrowed[positive-22-RE]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
