---
id: "P.SP.03.MSG.009.REQ.010"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.009"
requirement: "010"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 223
source_table: "Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 10"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.009.REQ.010

## Нормативное требование

реквизит «Номер документа» (csdo:DocId)DocId) в составе реквизита «Заявка на НМПТ Союза» (ipcdo:ApellationOfOriginApplicationDetails) должен быть заполнен

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Обязательное поле проверяется production presence rule; удаление только этого поля вызывает ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.001 → P.SP.03.TRN.010 → P.SP.03.MSG.009 → P.SP.03.MSG.009.REQ.010

## XML

- Structure: R.IP.SP.03.001
- QName: csdo:DocId; ipcdo:ApellationOfOriginApplicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: csdo:DocId => ipcdo:ApellationOfOriginApplicationDetails/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:IPEntityStatusDetails/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:IPPartyDetails/ccdo:IdentityDocV3Details/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:IPPartyDetails/ipcdo:LetterOfAttorneyDetails/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:ApellationOfOriginNationalRegistrationDetails/ipcdo:IPRightDetails/ipcdo:IPPartyDetails/ccdo:IdentityDocV3Details/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:ApellationOfOriginNationalRegistrationDetails/ipcdo:IPRightDetails/ipcdo:IPPartyDetails/ipcdo:LetterOfAttorneyDetails/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId; ipcdo:ApellationOfOriginApplicationDetails => ipcdo:ApellationOfOriginApplicationDetails

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 223
- Printed page: 57
- Table/item: Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 10
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_223]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.009.REQ.010
- Wiring: 23OP-RULE-P.SP.03.MSG.009-10;23OP-TRN-P-SP-03-TRN-010;23OP-PRC-P-SP-03-PRC-001
- Positive test: PASS — real XML accepted
- Negative test: PASS — field removal produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_required_application_identifiers_real_xml[10-DocId-P.SP.03.MSG.009]

## Gap

- Reason: Production structured rule wired; positive and negative real XML verified.
- Missing information: None for implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production wiring, positive and negative XML proof.
