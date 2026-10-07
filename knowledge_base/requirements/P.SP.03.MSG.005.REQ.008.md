---
id: "P.SP.03.MSG.005.REQ.008"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.005"
requirement: "008"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 375
source_table: "Таблица 19. Требования к электронному документу (сведениям) P.SP.03.MSG.005; item 8; inherited from Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001 item 8"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.005.REQ.008

## Нормативное требование

если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) заполнен в составе любых реквизитов, в его составе значение реквизита «Код вида связи» (csdo:CommunicationChannelCode) должно соответствовать одному из следующих значений: «TE», «EM» или «FX» в соответствии с перечнем видов средств (каналов) связи, утвержденным Решением Коллегии Комиссии от 6 декабря 2022 г. № 192 Inherited semantic requirement 8 from P.SP.03.MSG.001 as stated by range 4-45 in P.SP.03.MSG.005.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.004 → P.SP.03.TRN.004 → P.SP.03.MSG.005 → P.SP.03.MSG.005.REQ.008

## XML

- Structure: R.IP.SP.03.001
- QName: ccdo:CommunicationDetails; csdo:CommunicationChannelCode
- Namespace: MISSING / UNRESOLVED
- Path: UNCONFIRMED_NOT_MAPPED

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 375
- Printed page: 86
- Table/item: Таблица 19. Требования к электронному документу (сведениям) P.SP.03.MSG.005; item 8; inherited from Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001 item 8
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_375]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.005.REQ.008
- Wiring: 23OP-RULE-P.SP.03.MSG.005-4-45;23OP-RULE-P.SP.03.MSG.001-8;23OP-TRN-P-SP-03-TRN-004;23OP-PRC-P-SP-03-PRC-004
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py (message-specific/parametrized real-XML regression)

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
