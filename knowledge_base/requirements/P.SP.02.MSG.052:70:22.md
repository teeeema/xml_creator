---
id: "P.SP.02.MSG.052:70:22"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.052"
requirement: "22"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 795
source_table: "Table 70, item 22"
source_item: "REQ 22 (Table 70)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.052:70:22

## Нормативное требование

в составе экземпляра реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), содержащего сведения об аннулировании регистрации ТЗ Союза, реквизит «Конечная дата и время» (csdo:EndDateTime) должен быть заполнен, и значение этого реквизита должно быть больше значения реквизита «Начальная дата и время» (csdo:StartDateTime) в составе этого же экземпляра «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails) и меньше значения реквизита «Начальная дата и время» (csdo:StartDateTime) в составе экземпляра реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), содержащего сведения о регистрации нового ТЗ Союза

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.029 → P.SP.02.TRN.047 → P.SP.02.MSG.052 → P.SP.02.MSG.052:70:22

## XML

- Structure: R.IP.SP.02.007
- QName: csdo:EndDateTime; csdo:StartDateTime; csdo:StatusCode; ipcdo:UnifiedRegisterRecordsDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:UnifiedRegisterRecordsDetails; ipcdo:UnifiedRegisterRecordsDetails/ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime; ipcdo:UnifiedRegisterRecordsDetails/ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:IPEntityStatusDetails/csdo:StatusCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 795
- Printed page: 216
- Table/item: Table 70, item 22
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_795]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.052.T70.REQ.22.CANCEL; P.SP.02.MSG.052.T70.REQ.22.NEW
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 70", "page": 795, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-22", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 70", "page": 795, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-22", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["70"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[valid-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[valid-NEW_CANCEL]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[after_new-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[after_new-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[equal_new-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[equal_new-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[equal_start-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[equal_start-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[invalid-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[invalid-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[missing_end-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[missing_end-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[wrong_date_qname-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[wrong_date_qname-NEW_CANCEL]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[after_new-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[after_new-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[equal_new-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[equal_new-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[equal_start-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[equal_start-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[invalid-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[invalid-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[missing_end-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[missing_end-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[valid-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[valid-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[wrong_date_qname-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[wrong_date_qname-NEW_CANCEL]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
