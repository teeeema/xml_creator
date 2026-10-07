---
id: "P.SP.03.MSG.003.REQ.010"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.003"
requirement: "010"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 352
source_table: "Таблица 17. Требования к электронному документу (сведениям) P.SP.03.MSG.003; item 10; inherited from Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001 item 10"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.003.REQ.010

## Нормативное требование

реквизит «Номер документа» (csdo:DocId) составе реквизита «Заявка на НМПТ Союза» (ipcdo:ApellationOfOriginApplicationDetails) должен быть заполнен Inherited semantic requirement 10 from P.SP.03.MSG.001 as stated by range 4-45 in P.SP.03.MSG.003.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.002 → P.SP.03.TRN.002 → P.SP.03.MSG.003 → P.SP.03.MSG.003.REQ.010

## XML

- Structure: R.IP.SP.03.001
- QName: csdo:DocId; ipcdo:ApellationOfOriginApplicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: UNCONFIRMED_NOT_MAPPED

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 352
- Printed page: 63
- Table/item: Таблица 17. Требования к электронному документу (сведениям) P.SP.03.MSG.003; item 10; inherited from Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001 item 10
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_352]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.003.REQ.010
- Wiring: 23OP-RULE-P.SP.03.MSG.003-4-45;23OP-RULE-P.SP.03.MSG.001-10;23OP-TRN-P-SP-03-TRN-002;23OP-PRC-P-SP-03-PRC-002
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py (message-specific/parametrized real-XML regression)

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
