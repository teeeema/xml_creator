---
id: "P.SP.03.MSG.024.REQ.002"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.024"
requirement: "002"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 287
source_table: "Таблица 28. Требования к электронному документу (сведениям) P.SP.03.MSG.024; item 2"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.024.REQ.002

## Нормативное требование

соответствуют требованиям 1-19 таблицы 27 настоящего Регламента (значения кодов требований в таблице 27 и таблице 28 совпадают)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.009 → P.SP.03.TRN.018 → P.SP.03.MSG.024 → P.SP.03.MSG.024.REQ.002

## XML

- Structure: R.IP.SP.03.003
- QName: ipsdo:OriginOfficeIndicator; ipcdo:PatentAuthorityDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:OriginOfficeIndicator => ipcdo:PatentAuthorityDetails/ipsdo:OriginOfficeIndicator || ipcdo:IPPaymentDetails/ipcdo:PatentAuthorityDetails/ipsdo:OriginOfficeIndicator; ipcdo:PatentAuthorityDetails => ipcdo:PatentAuthorityDetails || ipcdo:IPPaymentDetails/ipcdo:PatentAuthorityDetails

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 287
- Printed page: 121
- Table/item: Таблица 28. Требования к электронному документу (сведениям) P.SP.03.MSG.024; item 2
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_287]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.024.REQ.002
- Wiring: 23OP-RULE-P.SP.03.MSG.024-1-19;23OP-TRN-P-SP-03-TRN-018;23OP-PRC-P-SP-03-PRC-009;23OP-RULE-P.SP.03.MSG.021-2;23OP-TRN-P-SP-03-TRN-017;23OP-PRC-P-SP-03-PRC-008;23OP-R.IP.SP.03.003-2-6;23OP-R.IP.SP.03.003-8-5-6;23OP-R.IP.SP.03.003-2;23OP-R.IP.SP.03.003-8-5;INHERITED_SEMANTIC_SOURCE:P.SP.03.MSG.021.REQ.002
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg024_inherited_req001_to_req018_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
