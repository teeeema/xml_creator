---
id: "P.SP.02.MSG.001:34:14"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.001"
requirement: "14"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 515
source_table: "Table 34, item 14"
source_item: "REQ 14 (Table 34)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.001:34:14

## Нормативное требование

в электронном документе (сведениях) «Сведения о заявке, ходатайстве для прохождения процедур регистрации ТЗ Союза» (R.IP.SP.02.002) должен быть заполнен 1 экземпляр реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), в составе которого значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.001 → P.SP.02.TRN.001 → P.SP.02.MSG.001 → P.SP.02.MSG.001:34:14

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails; ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 515
- Printed page: 103
- Table/item: Table 34, item 14
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_515]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.001.REQ.014
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "14", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 515, "source_id": "22OP-RULE-P.SP.02.MSG.001-14", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "14", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 515, "source_id": "22OP-RULE-P.SP.02.MSG.001-14", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_cardinality_counts_ap_after_filter[1]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_cardinality_counts_ap_after_filter[0]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_cardinality_counts_ap_after_filter[2]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_cardinality_counts_ap_after_filter[0]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_cardinality_counts_ap_after_filter[1]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_cardinality_counts_ap_after_filter[2]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
