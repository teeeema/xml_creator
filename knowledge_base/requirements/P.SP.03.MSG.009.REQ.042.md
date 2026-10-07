---
id: "P.SP.03.MSG.009.REQ.042"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.009"
requirement: "042"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 231
source_table: "Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 42"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.009.REQ.042

## Нормативное требование

реквизит «Признак согласия на обработку представленных сведений» (ipsdo:ConsentToDataProcessingIndicator)) должен быть заполнен

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.001 → P.SP.03.TRN.010 → P.SP.03.MSG.009 → P.SP.03.MSG.009.REQ.042

## XML

- Structure: R.IP.SP.03.001
- QName: ipsdo:ConsentToDataProcessingIndicator
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:ConsentToDataProcessingIndicator => ipcdo:ApellationOfOriginApplicationDetails/ipsdo:ConsentToDataProcessingIndicator

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 231
- Printed page: 65
- Table/item: Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 42
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_231]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.009.REQ.042
- Wiring: 23OP-RULE-P.SP.03.MSG.009-42;23OP-TRN-P-SP-03-TRN-010;23OP-PRC-P-SP-03-PRC-001
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_required_application_field_real_xml[P.SP.03.MSG.009-42-ConsentToDataProcessingIndicator]

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
