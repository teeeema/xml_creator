---
id: "P.SP.02.MSG.055:73:7"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.055"
requirement: "7"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 803
source_table: "Table 73, item 7"
source_item: "REQ 7 (Table 73)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.055:73:7

## Нормативное требование

реквизит «Сведения о пошлине за осуществление юридически значимых действий» (ipcdo:IPPaymentDetails) должен быть заполнен, в его составе реквизит «Банковский счет» (ccdo:BankAccountDetails) и (или) «Счет в платежной системе» (ccdo:PaymentSystemAccountDetails) должен быть заполнен

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.033 → P.SP.02.TRN.049 → P.SP.02.MSG.055 → P.SP.02.MSG.055:73:7

## XML

- Structure: R.IP.SP.03.003
- QName: ccdo:BankAccountDetails; ccdo:PaymentSystemAccountDetails; ipcdo:IPPaymentDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:IPPaymentDetails; ipcdo:IPPaymentDetails/ccdo:BankAccountDetails; ipcdo:IPPaymentDetails/ccdo:PaymentSystemAccountDetails

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 803
- Printed page: 224
- Table/item: Table 73, item 7
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_803]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.055.T73.REQ.7.PRESENCE; P.SP.02.MSG.055.T73.REQ.7.ACCOUNTS
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "7", "location": "Таблица 73", "page": 803, "source_id": "22OP-RULE-P.SP.02.MSG.055-T73-7", "status": "CONFIRMED", "table": "73", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "7", "location": "Таблица 73", "page": 803, "source_id": "22OP-RULE-P.SP.02.MSG.055-T73-7", "status": "CONFIRMED", "table": "73", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["73"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[False-False-True]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[False-True-False]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[False-True-True]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[False-False-False]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[True-False-False]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[True-False-True]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[True-True-False]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[True-True-True]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_payment_presence_is_not_created_by_rule
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[False-False-False]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[False-False-True]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[False-True-False]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[False-True-True]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[True-False-False]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[True-False-True]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[True-True-False]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner[True-True-True]; P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_payment_presence_is_not_created_by_rule

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
