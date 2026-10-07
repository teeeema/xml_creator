---
id: "P.SP.03.MSG.024.REQ.022"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.024"
requirement: "022"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 287
source_table: "Таблица 28. Требования к электронному документу (сведениям) P.SP.03.MSG.024; item 22"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.024.REQ.022

## Нормативное требование

если значение реквизита реквизит «Признак подтверждения уплаты пошлины» (ipsdo:DutyPaymentIndicator) соответствует значению «ложь (false)», значение реквизита «Сумма платежа» (csdo:PaymentAmount) должно быть заполнено и содержать значение, большее, чем «0»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.009 → P.SP.03.TRN.018 → P.SP.03.MSG.024 → P.SP.03.MSG.024.REQ.022

## XML

- Structure: R.IP.SP.03.003
- QName: ipsdo:DutyPaymentIndicator; csdo:PaymentAmount
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:DutyPaymentIndicator => ipsdo:DutyPaymentIndicator; csdo:PaymentAmount => ipcdo:IPPaymentDetails/csdo:PaymentAmount || csdo:PaymentAmount

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 287
- Printed page: 121
- Table/item: Таблица 28. Требования к электронному документу (сведениям) P.SP.03.MSG.024; item 22
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_287]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.024.REQ.022
- Wiring: 23OP-RULE-P.SP.03.MSG.024-22;23OP-TRN-P-SP-03-TRN-018;23OP-PRC-P-SP-03-PRC-009;23OP-R.IP.SP.03.003-9;23OP-R.IP.SP.03.003-8-4;23OP-R.IP.SP.03.003-11
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg024_req022_false_requires_positive_amount_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
