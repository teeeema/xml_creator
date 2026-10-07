---
id: "P.SP.03.MSG.001.REQ.017"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.001"
requirement: "017"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 343
source_table: "Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001; item 17"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.001.REQ.017

## Нормативное требование

значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) должно соответствовать одному из следующих значений: «AP» – «заявитель»; «PA» – «представитель заявителя, являющийся патентным поверенным»; «RE» – «представитель заявителя, не являющийся патентным поверенным»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.001 → P.SP.03.TRN.001 → P.SP.03.MSG.001 → P.SP.03.MSG.001.REQ.017

## XML

- Structure: R.IP.SP.03.001
- QName: ipsdo:IPPartyKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPPartyKindCode

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 343
- Printed page: 54
- Table/item: Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001; item 17
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_343]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.001.REQ.017
- Wiring: 23OP-RULE-P.SP.03.MSG.001-17;23OP-TRN-P-SP-03-TRN-001;23OP-PRC-P-SP-03-PRC-001
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py (message-specific/parametrized real-XML regression)

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
