---
id: "P.SP.02.MSG.020:53:3"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.020"
requirement: "3"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 569
source_table: "Table 53, item 3"
source_item: "REQ 3 (Table 53)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.020:53:3

## Нормативное требование

Если CancellationStatusIndicator хотя бы для одного GoodsBaseDetails = «1», должен быть второй экземпляр с регистрацией нового ТЗ Союза.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.029 → P.SP.02.TRN.018 → P.SP.02.MSG.020 → P.SP.02.MSG.020:53:3

## XML

- Structure: R.IP.SP.02.007
- QName: csdo:StatusCode; ipcdo:GoodsBaseDetails; ipcdo:UnifiedRegisterRecordsDetails; ipsdo:CancellationStatusIndicator
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:UnifiedRegisterRecordsDetails; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:GoodsBaseDetails; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:GoodsBaseDetails/ipsdo:CancellationStatusIndicator; ipcdo:UnifiedRegisterRecordsDetails/ipcdo:IPEntityStatusDetails/csdo:StatusCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 569
- Printed page: 157
- Table/item: Table 53, item 3
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_569]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.020.T53.REQ.3
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 53", "page": 569, "source_id": "22OP-RULE-P.SP.02.MSG.020-T53-3", "status": "CONFIRMED", "table": "53", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 53", "page": 569, "source_id": "22OP-RULE-P.SP.02.MSG.020-T53-3", "status": "CONFIRMED", "table": "53", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["53"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records0-True-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records2-True-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records3-True-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records4-True-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records5-True-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records7-True-020-53]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records1-False-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records6-False-020-53]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records0-True-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records1-False-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records2-True-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records3-True-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records4-True-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records5-True-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records6-False-020-53]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg052_new_record_required_after_cancel_goods_filter[records7-True-020-53]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
