---
id: "P.SP.03.MSG.012.REQ.024"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.012"
requirement: "024"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 258
source_table: "Таблица 21. Требования к электронному документу (сведениям) P.SP.03.MSG.012; item 24; inherited from Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009 item 24"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.012.REQ.024

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) в составе реквизита «Адрес» (ccdo:SubjectAddressDetails) значение реквизита «Код вида адреса» (csdo:AddressKindCode) должно соответствовать значению «2» – «фактический адрес (адрес места нахождения или места жительства)» Inherited semantic requirement 24 from P.SP.03.MSG.009 as stated by range 4-45 in P.SP.03.MSG.012.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.004 → P.SP.03.TRN.013 → P.SP.03.MSG.012 → P.SP.03.MSG.012.REQ.024

## XML

- Structure: R.IP.SP.03.001
- QName: ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ccdo:SubjectAddressDetails; csdo:AddressKindCode
- Namespace: MISSING / UNRESOLVED
- Path: UNCONFIRMED_NOT_MAPPED

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 258
- Printed page: 92
- Table/item: Таблица 21. Требования к электронному документу (сведениям) P.SP.03.MSG.012; item 24; inherited from Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009 item 24
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_258]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.012.REQ.024
- Wiring: 23OP-RULE-P.SP.03.MSG.012-4-45;23OP-RULE-P.SP.03.MSG.009-24;23OP-TRN-P-SP-03-TRN-013;23OP-PRC-P-SP-03-PRC-004
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py (message-specific/parametrized real-XML regression)

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
