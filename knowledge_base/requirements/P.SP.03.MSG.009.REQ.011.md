---
id: "P.SP.03.MSG.009.REQ.011"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.009"
requirement: "011"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 223
source_table: "Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 11"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.009.REQ.011

## Нормативное требование

реквизит «Дата поступления документа» (ipsdo:IPDocReceiptDate) в составе реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» (ipcdo:ApellationOfOriginApplicationDetails) должен быть заполнен

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Обязательное поле проверяется production presence rule; удаление только этого поля вызывает ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.001 → P.SP.03.TRN.010 → P.SP.03.MSG.009 → P.SP.03.MSG.009.REQ.011

## XML

- Structure: R.IP.SP.03.001
- QName: ipsdo:IPDocReceiptDate; ipcdo:ApellationOfOriginApplicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPDocReceiptDate => ipcdo:ApellationOfOriginApplicationDetails/ipsdo:IPDocReceiptDate || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:IPEntityStatusDetails/ipsdo:IPDocReceiptDate; ipcdo:ApellationOfOriginApplicationDetails => ipcdo:ApellationOfOriginApplicationDetails

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 223
- Printed page: 57
- Table/item: Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 11
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_223]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.009.REQ.011
- Wiring: 23OP-RULE-P.SP.03.MSG.009-11;23OP-TRN-P-SP-03-TRN-010;23OP-PRC-P-SP-03-PRC-001
- Positive test: PASS — real XML accepted
- Negative test: PASS — field removal produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_required_application_identifiers_real_xml[11-IPDocReceiptDate-P.SP.03.MSG.009]

## Gap

- Reason: Production structured rule wired; positive and negative real XML verified.
- Missing information: None for implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production wiring, positive and negative XML proof.
