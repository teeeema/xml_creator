---
id: "P.SP.02.MSG.052:70:3"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.052"
requirement: "3"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 793
source_table: "Table 70, item 3"
source_item: "REQ 3 (Table 70)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.052:70:3

## Нормативное требование

в случае, если в составе экземпляра реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), содержащего сведения об аннулировании регистрации ТЗ Союза, значение реквизита «Признак аннулирования товарного знака Союза» (ipsdo:CancellationStatusIndicator) хотя бы для одного экземпляра реквизита «Товар в соответствии с МКТУ» (ipcdo:GoodsBaseDetails) соответствует значению «1» – «ТЗ Союза аннулирован, решение о досрочном прекращении действия (о признание недействительным) правовой охраны в отношении товара не принято», то в электронном документе (сведениях) должен быть заполнен второй экземпляр реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), содержащий сведения о регистрации нового ТЗ Союза

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.029 → P.SP.02.TRN.047 → P.SP.02.MSG.052 → P.SP.02.MSG.052:70:3

## XML

- Structure: R.IP.SP.02.007
- QName: csdo:StatusCode; ipcdo:GoodsBaseDetails; ipcdo:UnifiedRegisterRecordsDetails; ipsdo:CancellationStatusIndicator
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:UnifiedRegisterRecordsDetails; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:GoodsBaseDetails; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:GoodsBaseDetails/ipsdo:CancellationStatusIndicator; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:IPEntityStatusDetails/csdo:StatusCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 793
- Printed page: 214
- Table/item: Table 70, item 3
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_793]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.052.T70.REQ.3
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 70", "page": 793, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-3", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 70", "page": 793, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-3", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["70"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records0-True-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records2-True-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records3-True-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records4-True-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records5-True-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records7-True-052-70]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records1-False-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records6-False-052-70]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records0-True-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records1-False-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records2-True-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records3-True-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records4-True-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records5-True-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records6-False-052-70]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records7-True-052-70]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
