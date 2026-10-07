---
id: "P.SP.03.MSG.022.REQ.002"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.022"
requirement: "002"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 283
source_table: "Таблица 26. Требования к электронному документу (сведениям) P.SP.03.MSG.022; item 2; inherited from Таблица 25. Требования к электронному документу (сведениям) P.SP.03.MSG.021 item 2"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.022.REQ.002

## Нормативное требование

значение реквизита «Признак ведомства подачи» (ipsdo:OriginOfficeIndicator) в составе реквизита «Национальное патентное ведомство» (ipcdo:PatentAuthorityDetails)должно соответствовать значению «1» – ведомство подачи Inherited semantic requirement 2 from P.SP.03.MSG.021 as stated by range 1-6 in P.SP.03.MSG.022.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.008 → P.SP.03.TRN.017 → P.SP.03.MSG.022 → P.SP.03.MSG.022.REQ.002

## XML

- Structure: R.IP.SP.03.003
- QName: ipsdo:OriginOfficeIndicator; ipcdo:PatentAuthorityDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:OriginOfficeIndicator => ipcdo:PatentAuthorityDetails/ipsdo:OriginOfficeIndicator || ipcdo:IPPaymentDetails/ipcdo:PatentAuthorityDetails/ipsdo:OriginOfficeIndicator; ipcdo:PatentAuthorityDetails => ipcdo:PatentAuthorityDetails || ipcdo:IPPaymentDetails/ipcdo:PatentAuthorityDetails

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 283
- Printed page: 117
- Table/item: Таблица 26. Требования к электронному документу (сведениям) P.SP.03.MSG.022; item 2; inherited from Таблица 25. Требования к электронному документу (сведениям) P.SP.03.MSG.021 item 2
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_283]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.022.REQ.002
- Wiring: 23OP-RULE-P.SP.03.MSG.022-1-6;23OP-RULE-P.SP.03.MSG.021-2;23OP-TRN-P-SP-03-TRN-017;23OP-PRC-P-SP-03-PRC-008;23OP-R.IP.SP.03.003-2-6;23OP-R.IP.SP.03.003-8-5-6;23OP-R.IP.SP.03.003-2;23OP-R.IP.SP.03.003-8-5
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg022_req002_inherited_origin_office_indicator_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
