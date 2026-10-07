---
id: "P.SP.02.MSG.032:50:18"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.032"
requirement: "18"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 718
source_table: "Table 44, item 18"
source_item: "REQ 18 (Table 50)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.032:50:18

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель» и, если в составе реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName) значение атрибута «код языка» (атрибут languageCode) соответствует значению «RU», второй экземпляр реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.006 → P.SP.02.TRN.027 → P.SP.02.MSG.032 → P.SP.02.MSG.032:50:18

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 718
- Printed page: 139
- Table/item: Table 44, item 18
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 50 item 18 via range 6-29 (PDF p.742)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_718]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.032.T50.REQ.18
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 50", "page": 742, "source_id": "22OP-RULE-P.SP.02.MSG.032-T50-6-29", "status": "CONFIRMED", "table": "50", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "18", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 718, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-18", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-positive-18-P.SP.02.MSG.032-50]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-positive-18-P.SP.02.MSG.032-50]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-negative-18-P.SP.02.MSG.032-50]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-negative-18-P.SP.02.MSG.032-50]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-negative-18-P.SP.02.MSG.032-50]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-positive-18-P.SP.02.MSG.032-50]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-negative-18-P.SP.02.MSG.032-50]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-positive-18-P.SP.02.MSG.032-50]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
