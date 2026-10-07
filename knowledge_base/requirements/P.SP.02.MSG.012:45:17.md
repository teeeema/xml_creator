---
id: "P.SP.02.MSG.012:45:17"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.012"
requirement: "17"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 516
source_table: "Table 34, item 17"
source_item: "REQ 17 (Table 45)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.012:45:17

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должен быть заполнен 1 экземпляр реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName), в составе которого значение атрибута «код вида представления наименования» (атрибут nameRepresentationKindCode) должно соответствовать значению «OR» – «сведения, представленные на исходном (оригинальном) языке» и атрибут «код языка» (атрибут languageCode) должен быть заполнен

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.020 → P.SP.02.TRN.010 → P.SP.02.MSG.012 → P.SP.02.MSG.012:45:17

## XML

- Structure: R.IP.SP.02.002
- QName: @languageCode; @nameRepresentationKindCode; csdo:StatusCode; ipcdo:IPPartyDetails; ipcdo:TrademarkApplicationDetails; ipsdo:IPPartyKindCode; ipsdo:IPSubjectName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails; ipcdo:TrademarkApplicationDetails/ipcdo:IPEntityStatusDetails/csdo:StatusCode; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPSubjectName; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPSubjectName/@languageCode; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPSubjectName/@nameRepresentationKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 516
- Printed page: 104
- Table/item: Table 34, item 17
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 45 item 17 via range 6-29 (PDF p.551)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_516]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.012.T45.REQ.17; P.SP.02.MSG.012.T45.REQ.17.LANGUAGE
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 45. Требования к электронному документу (сведениям) P.SP.02.MSG.012", "page": 551, "source_id": "22OP-RULE-P.SP.02.MSG.012-T45-6-29", "status": "CONFIRMED", "table": "45", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "17", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 516, "source_id": "22OP-RULE-P.SP.02.MSG.001-17", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-positive-17-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-positive-17-P.SP.02.MSG.012-45]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_original_name_count_is_exactly_one_per_ap[NEW_OLD-duplicate_original-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_original_name_count_is_exactly_one_per_ap[NEW_OLD-missing_original-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_original_name_count_is_exactly_one_per_ap[OLD_NEW-duplicate_original-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_original_name_count_is_exactly_one_per_ap[OLD_NEW-missing_original-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-negative-17-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-negative-17-P.SP.02.MSG.012-45]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_original_name_count_is_exactly_one_per_ap[NEW_OLD-duplicate_original-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_original_name_count_is_exactly_one_per_ap[NEW_OLD-missing_original-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_original_name_count_is_exactly_one_per_ap[OLD_NEW-duplicate_original-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_original_name_count_is_exactly_one_per_ap[OLD_NEW-missing_original-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-negative-17-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-positive-17-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-negative-17-P.SP.02.MSG.012-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-positive-17-P.SP.02.MSG.012-45]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
