---
id: "P.SP.03.MSG.001.REQ.043"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.001"
requirement: "043"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 350
source_table: "Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001; item 43"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.001.REQ.043

## Нормативное требование

реквизит «Признак согласия на обработку представленных сведений» (ipsdo:ConsentToDataProcessingIndicator)) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.001 → P.SP.03.TRN.001 → P.SP.03.MSG.001 → P.SP.03.MSG.001.REQ.043

## XML

- Structure: R.IP.SP.03.001
- QName: ipsdo:ConsentToDataProcessingIndicator
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:ConsentToDataProcessingIndicator => ipcdo:ApellationOfOriginApplicationDetails/ipsdo:ConsentToDataProcessingIndicator

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 350
- Printed page: 61
- Table/item: Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001; item 43
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_350]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.001.REQ.043
- Wiring: 23OP-RULE-P.SP.03.MSG.001-43;23OP-TRN-P-SP-03-TRN-001;23OP-PRC-P-SP-03-PRC-001
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_forbidden_field_real_xml_positive_and_negative[P.SP.03.MSG.001-43]

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
