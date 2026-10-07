---
id: "P.SP.02.MSG.029:45:16"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.029"
requirement: "16"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 717
source_table: "Table 44, item 16"
source_item: "REQ 16 (Table 45)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.029:45:16

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то значение атрибута «код вида представления наименования» (атрибут nameRepresentationKindCode) в составе реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName) должно соответствовать одному из следующих значений: «OR» – «сведения, представленные на исходном (оригинальном) языке»; «LA» – «транслитерация сведений на исходном (оригинальном) языке буквами латинского алфавита»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.003 → P.SP.02.TRN.024 → P.SP.02.MSG.029 → P.SP.02.MSG.029:45:16

## XML

- Structure: R.IP.SP.02.002
- QName: @nameRepresentationKindCode; ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ipsdo:IPSubjectName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPSubjectName; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPSubjectName/@nameRepresentationKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 717
- Printed page: 138
- Table/item: Table 44, item 16
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 45 item 16 via range 6-29 (PDF p.725)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_717]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.029.T45.REQ.16
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 45", "page": 725, "source_id": "22OP-RULE-P.SP.02.MSG.029-T45-6-29", "status": "CONFIRMED", "table": "45", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "16", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 717, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-16", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-positive-16-P.SP.02.MSG.029-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-positive-16-P.SP.02.MSG.029-45]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-negative-16-P.SP.02.MSG.029-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-negative-16-P.SP.02.MSG.029-45]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-negative-16-P.SP.02.MSG.029-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-positive-16-P.SP.02.MSG.029-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-negative-16-P.SP.02.MSG.029-45]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-positive-16-P.SP.02.MSG.029-45]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
