---
id: "P.SP.03.MSG.021.REQ.007"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.021"
requirement: "007"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 282
source_table: "Таблица 25. Требования к электронному документу (сведениям) P.SP.03.MSG.021; item 7"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.021.REQ.007

## Нормативное требование

реквизиты «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId), «Номер документа» (csdo:DocId), «Сведения о пошлине за осуществление юридически значимых действий» (ipcdo:IPPaymentDetails), «Признак подтверждения уплаты пошлины» (ipsdo:DutyPaymentIndicator), «Сумма платежа» (csdo:PaymentAmount) не заполняются

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.008 → P.SP.03.TRN.017 → P.SP.03.MSG.021 → P.SP.03.MSG.021.REQ.007

## XML

- Structure: R.IP.SP.03.003
- QName: ipsdo:TrademarkApplicationId; csdo:DocId; ipcdo:IPPaymentDetails; ipsdo:DutyPaymentIndicator; csdo:PaymentAmount
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:TrademarkApplicationId => ipsdo:TrademarkApplicationId; csdo:DocId => csdo:DocId || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ccdo:IdentityDocV3Details/csdo:DocId || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ipcdo:LetterOfAttorneyDetails/csdo:DocId || ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId; ipcdo:IPPaymentDetails => ipcdo:IPPaymentDetails; ipsdo:DutyPaymentIndicator => ipsdo:DutyPaymentIndicator; csdo:PaymentAmount => ipcdo:IPPaymentDetails/csdo:PaymentAmount || csdo:PaymentAmount

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 282
- Printed page: 116
- Table/item: Таблица 25. Требования к электронному документу (сведениям) P.SP.03.MSG.021; item 7
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_282]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.021.REQ.007.trademark_application_id;P.SP.03.MSG.021.REQ.007.doc_id;P.SP.03.MSG.021.REQ.007.payment_details;P.SP.03.MSG.021.REQ.007.duty_payment_indicator;P.SP.03.MSG.021.REQ.007.payment_amount
- Wiring: 23OP-RULE-P.SP.03.MSG.021-7;23OP-TRN-P-SP-03-TRN-017;23OP-PRC-P-SP-03-PRC-008;23OP-R.IP.SP.03.003-5;23OP-R.IP.SP.03.003-7;23OP-R.IP.SP.03.003-8-9-11-5;23OP-R.IP.SP.03.003-8-9-15-6;23OP-R.IP.SP.03.003-8-10-4;23OP-R.IP.SP.03.003-8;23OP-R.IP.SP.03.003-9;23OP-R.IP.SP.03.003-8-4;23OP-R.IP.SP.03.003-11
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg021_req007_forbidden_fields_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
