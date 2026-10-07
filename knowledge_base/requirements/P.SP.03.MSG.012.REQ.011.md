---
id: "P.SP.03.MSG.012.REQ.011"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.012"
requirement: "011"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 258
source_table: "Таблица 21. Требования к электронному документу (сведениям) P.SP.03.MSG.012; item 11; inherited from Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009 item 11"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.012.REQ.011

## Нормативное требование

реквизит «Дата поступления документа» (ipsdo:IPDocReceiptDate) в составе реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» (ipcdo:ApellationOfOriginApplicationDetails) должен быть заполнен Inherited semantic requirement 11 from P.SP.03.MSG.009 as stated by range 4-45 in P.SP.03.MSG.012.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.004 → P.SP.03.TRN.013 → P.SP.03.MSG.012 → P.SP.03.MSG.012.REQ.011

## XML

- Structure: R.IP.SP.03.001
- QName: ipsdo:IPDocReceiptDate; ipcdo:ApellationOfOriginApplicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: UNCONFIRMED_NOT_MAPPED

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 258
- Printed page: 92
- Table/item: Таблица 21. Требования к электронному документу (сведениям) P.SP.03.MSG.012; item 11; inherited from Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009 item 11
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_258]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.012.REQ.011
- Wiring: 23OP-RULE-P.SP.03.MSG.012-4-45;23OP-RULE-P.SP.03.MSG.009-11;23OP-TRN-P-SP-03-TRN-013;23OP-PRC-P-SP-03-PRC-004
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py (message-specific/parametrized real-XML regression)

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
