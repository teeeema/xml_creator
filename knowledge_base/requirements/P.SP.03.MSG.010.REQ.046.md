---
id: "P.SP.03.MSG.010.REQ.046"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.010"
requirement: "046"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 234
source_table: "Таблица 19. Требования к электронному документу (сведениям) P.SP.03.MSG.010; item 46; inherited from Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009 item 46"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.010.REQ.046

## Нормативное требование

если в составе реквизита «Сведения о подписании документа» (ipcdo:SignatureDetails) заполнен реквизит «Сотрудник организации» (ipcdo:OfficerDetails), то в составе реквизита «Сотрудник организации» (ipcdo:OfficerDetails) должны быть заполнены подчиненные реквизиты «Фамилия» (csdo:LastName), «Имя» (csdo:FirstName) и «Наименование должности» (csdo:PositionName), а реквизит «Контактный реквизит» (ccdo:CommunicationDetails) не заполняется Inherited semantic requirement 46 from P.SP.03.MSG.009 as stated by range 4-50 in P.SP.03.MSG.010.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.002 → P.SP.03.TRN.011 → P.SP.03.MSG.010 → P.SP.03.MSG.010.REQ.046

## XML

- Structure: R.IP.SP.03.001
- QName: ipcdo:SignatureDetails; ipcdo:OfficerDetails; csdo:LastName; csdo:FirstName; csdo:PositionName; ccdo:CommunicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: UNCONFIRMED_NOT_MAPPED

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 234
- Printed page: 68
- Table/item: Таблица 19. Требования к электронному документу (сведениям) P.SP.03.MSG.010; item 46; inherited from Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009 item 46
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_234]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.010.REQ.046
- Wiring: 23OP-RULE-P.SP.03.MSG.010-4-50;23OP-RULE-P.SP.03.MSG.009-46;23OP-TRN-P-SP-03-TRN-011;23OP-PRC-P-SP-03-PRC-002
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py (message-specific/parametrized real-XML regression)

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
