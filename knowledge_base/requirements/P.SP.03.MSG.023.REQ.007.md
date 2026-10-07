---
id: "P.SP.03.MSG.023.REQ.007"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.023"
requirement: "007"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 284
source_table: "Таблица 27. Требования к электронному документу (сведениям) P.SP.03.MSG.023; item 7"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.023.REQ.007

## Нормативное требование

реквизит «Сведения о пошлине за осуществление юридически значимых действий» (ipcdo:IPPaymentDetails) должен быть заполнен, в его составе реквизиты «Банковский счет» (ccdo:BankAccountDetails) и «Счет в платежной системе» (ccdo:PaymentSystemAccountDetails) не заполняются

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.009 → P.SP.03.TRN.018 → P.SP.03.MSG.023 → P.SP.03.MSG.023.REQ.007

## XML

- Structure: R.IP.SP.03.003
- QName: ipcdo:IPPaymentDetails; ccdo:BankAccountDetails; ccdo:PaymentSystemAccountDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:IPPaymentDetails => ipcdo:IPPaymentDetails; ccdo:BankAccountDetails => ipcdo:IPPaymentDetails/ccdo:BankAccountDetails; ccdo:PaymentSystemAccountDetails => ipcdo:IPPaymentDetails/ccdo:PaymentSystemAccountDetails

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 284
- Printed page: 118
- Table/item: Таблица 27. Требования к электронному документу (сведениям) P.SP.03.MSG.023; item 7
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_284]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.023.REQ.007.payment_details;P.SP.03.MSG.023.REQ.007.accounts_forbidden
- Wiring: 23OP-RULE-P.SP.03.MSG.023-7;23OP-TRN-P-SP-03-TRN-018;23OP-PRC-P-SP-03-PRC-009;23OP-R.IP.SP.03.003-8;23OP-R.IP.SP.03.003-8-6;23OP-R.IP.SP.03.003-8-7
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg023_req007_payment_required_and_accounts_forbidden_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
