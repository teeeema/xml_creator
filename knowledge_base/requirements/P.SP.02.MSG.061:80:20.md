---
id: "P.SP.02.MSG.061:80:20"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.061"
requirement: "20"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 718
source_table: "Table 44, item 20"
source_item: "REQ 20 (Table 80)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.061:80:20

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) в составе реквизита «Адрес» (ccdo:SubjectAddressDetails) значение реквизита «Код вида адреса» (csdo:AddressKindCode) должно соответствовать значению «2» – «фактический адрес (адрес места нахождения или места жительства)»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.008 → P.SP.02.TRN.052 → P.SP.02.MSG.061 → P.SP.02.MSG.061:80:20

## XML

- Structure: R.IP.SP.02.002
- QName: ccdo:SubjectAddressDetails; csdo:AddressKindCode; ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ccdo:SubjectAddressDetails; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ccdo:SubjectAddressDetails/csdo:AddressKindCode; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 718
- Printed page: 139
- Table/item: Table 44, item 20
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 80 item 20 via range 6-29 (PDF p.814)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_718]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.061.T80.REQ.20
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 80", "page": 814, "source_id": "22OP-RULE-P.SP.02.MSG.061-T80-6-29", "status": "CONFIRMED", "table": "80", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "20", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 718, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-20", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-positive-20-P.SP.02.MSG.061-80]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-positive-20-P.SP.02.MSG.061-80]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-negative-20-P.SP.02.MSG.061-80]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-negative-20-P.SP.02.MSG.061-80]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-negative-20-P.SP.02.MSG.061-80]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-positive-20-P.SP.02.MSG.061-80]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-negative-20-P.SP.02.MSG.061-80]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-positive-20-P.SP.02.MSG.061-80]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
