---
id: "P.SP.03.MSG.023.REQ.017"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.023"
requirement: "017"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 286
source_table: "Таблица 27. Требования к электронному документу (сведениям) P.SP.03.MSG.023; item 17"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.023.REQ.017

## Нормативное требование

в составе реквизита «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails) должен быть заполнен реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) и его значение должно соответствовать значению «07015»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.009 → P.SP.03.TRN.018 → P.SP.03.MSG.023 → P.SP.03.MSG.023.REQ.017

## XML

- Structure: R.IP.SP.03.003
- QName: ipcdo:AccompanyingDocumentsDetails; ipsdo:IPDocKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:AccompanyingDocumentsDetails => ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails; ipsdo:IPDocKindCode => ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindCode

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 286
- Printed page: 120
- Table/item: Таблица 27. Требования к электронному документу (сведениям) P.SP.03.MSG.023; item 17
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_286]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.023.REQ.017
- Wiring: 23OP-RULE-P.SP.03.MSG.023-17;23OP-TRN-P-SP-03-TRN-018;23OP-PRC-P-SP-03-PRC-009;23OP-R.IP.SP.03.003-8-10;23OP-R.IP.SP.03.003-8-10-1
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg023_req017_document_kind_code_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
