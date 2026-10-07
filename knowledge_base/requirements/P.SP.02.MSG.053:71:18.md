---
id: "P.SP.02.MSG.053:71:18"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.053"
requirement: "18"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 739
source_table: "Table 49, item 18"
source_item: "REQ 18 (Table 71)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.053:71:18

## Нормативное требование

если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) соответствует значению «1» – «товарный знак является коллективным», то должен быть заполнен хотя бы 1 экземпляр реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), в составе которого значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «UE» – «лицо, имеющее право использования коллективного знака Союза»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.030 → P.SP.02.TRN.048 → P.SP.02.MSG.053 → P.SP.02.MSG.053:71:18

## XML

- Structure: R.IP.SP.02.007
- QName: ipcdo:IPPartyDetails; ipcdo:UnifiedRegisterRecordsDetails; ipsdo:CollectiveMarkIndicator; ipsdo:IPPartyKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:UnifiedRegisterRecordsDetails; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:IPPartyDetails; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:TrademarkDetails/ipsdo:CollectiveMarkIndicator

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 739
- Printed page: 160
- Table/item: Table 49, item 18
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 71 item 18 via range 6-19 (PDF p.799)
- Inherited source chain: 49
- Source page: [[sources/OP22_P_SP_02/pages/page_739]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.053.T71.REQ.18
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 71", "page": 799, "source_id": "22OP-RULE-P.SP.02.MSG.053-T71-6-19", "status": "CONFIRMED", "table": "71", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "18", "location": "Таблица 49", "page": 739, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-18", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[False-inactive-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[False-valid-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[True-inactive-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[True-valid-053-71]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[False-missing_role-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[False-wrong_owner-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[True-missing_role-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[True-wrong_owner-053-71]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[False-inactive-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[False-missing_role-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[False-valid-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[False-wrong_owner-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[True-inactive-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[True-missing_role-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[True-valid-053-71]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record[True-wrong_owner-053-71]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
