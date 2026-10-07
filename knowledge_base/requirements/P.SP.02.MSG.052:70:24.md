---
id: "P.SP.02.MSG.052:70:24"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.052"
requirement: "24"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 795
source_table: "Table 70, item 24"
source_item: "REQ 24 (Table 70)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.052:70:24

## Нормативное требование

значение реквизита «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) в составе экземпляра реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), содержащего сведения о регистрации нового ТЗ Союза, должно быть заполнено и его значение должно совпадать со значением реквизита «Новый регистрационный номер товарного знака Союза» (ipsdo:TrademarkNewId) в составе экземпляра реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), содержащего сведения об аннулировании регистрации ТЗ Союза

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.029 → P.SP.02.TRN.047 → P.SP.02.MSG.052 → P.SP.02.MSG.052:70:24

## XML

- Structure: R.IP.SP.02.007
- QName: csdo:StatusCode; ipcdo:UnifiedRegisterRecordsDetails; ipsdo:TrademarkId; ipsdo:TrademarkNewId
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:UnifiedRegisterRecordsDetails; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:IPEntityStatusDetails/csdo:StatusCode; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:RegistrationCancellationDetails/ipcdo:ComplaintInvalidateProtectionTrademarkDetails/ipsdo:TrademarkNewId; ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 795
- Printed page: 216
- Table/item: Table 70, item 24
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_795]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.052.T70.REQ.24
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "24", "location": "Таблица 70", "page": 795, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-24", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "24", "location": "Таблица 70", "page": 795, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-24", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["70"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[valid-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[valid-NEW_CANCEL]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[different_id-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[different_id-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[misowned_id-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[misowned_id-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[missing_id-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[missing_id-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[wrong_id_qname-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[wrong_id_qname-NEW_CANCEL]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[different_id-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[different_id-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[misowned_id-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[misowned_id-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[missing_id-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[missing_id-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[valid-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[valid-NEW_CANCEL]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[wrong_id_qname-CANCEL_NEW]; P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py::test_msg052_production_date_and_equality[wrong_id_qname-NEW_CANCEL]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
