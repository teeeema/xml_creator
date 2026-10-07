---
id: "P.SP.03.MSG.018.REQ.002"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.018"
requirement: "002"
structure: "R.IP.SP.03.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 399
source_table: "Таблица 24. Требования к электронному документу (сведениям) P.SP.03.MSG.018; item 2"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.018.REQ.002

## Нормативное требование

реквизиты «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails) и «Регистрационный номер заявки на НМПТ Союза» (ipsdo:ApellationOfOriginApplicationId) не заполняются

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.011 → P.SP.03.TRN.009 → P.SP.03.MSG.018 → P.SP.03.MSG.018.REQ.002

## XML

- Structure: R.IP.SP.03.007
- QName: ipcdo:AccompanyingDocumentsDetails; ipsdo:ApellationOfOriginApplicationId
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:AccompanyingDocumentsDetails => ipcdo:AccompanyingDocumentsDetails; ipsdo:ApellationOfOriginApplicationId => ipsdo:ApellationOfOriginApplicationId

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 399
- Printed page: 110
- Table/item: Таблица 24. Требования к электронному документу (сведениям) P.SP.03.MSG.018; item 2
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_399]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.018.REQ.002.application_id;P.SP.03.MSG.018.REQ.002.accompanying_document
- Wiring: 23OP-RULE-P.SP.03.MSG.018-2;23OP-TRN-P-SP-03-TRN-009;23OP-PRC-P-SP-03-PRC-011
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg018_req002_both_forbidden_fields_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
