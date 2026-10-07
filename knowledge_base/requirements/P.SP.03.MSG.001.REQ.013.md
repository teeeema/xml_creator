---
id: "P.SP.03.MSG.001.REQ.013"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.001"
requirement: "013"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 342
source_table: "Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001; item 13"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.001.REQ.013

## Нормативное требование

реквизит «Регистрационный номер заявки на НМПТ Союза» (ipsdo:ApellationOfOriginApplicationId)» (csdo:DocId) в составе реквизита «Заявка на НМПТ Союза» (ipcdo:ApellationOfOriginApplicationDetails) должен быть заполнен

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Обязательное поле проверяется production presence rule; удаление только этого поля вызывает ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.001 → P.SP.03.TRN.001 → P.SP.03.MSG.001 → P.SP.03.MSG.001.REQ.013

## XML

- Structure: R.IP.SP.03.001
- QName: ipsdo:ApellationOfOriginApplicationId; csdo:DocId; ipcdo:ApellationOfOriginApplicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:ApellationOfOriginApplicationId => ipcdo:ApellationOfOriginApplicationDetails/ipsdo:ApellationOfOriginApplicationId; csdo:DocId => ipcdo:ApellationOfOriginApplicationDetails/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:IPEntityStatusDetails/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:IPPartyDetails/ccdo:IdentityDocV3Details/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:IPPartyDetails/ipcdo:LetterOfAttorneyDetails/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:ApellationOfOriginNationalRegistrationDetails/ipcdo:IPRightDetails/ipcdo:IPPartyDetails/ccdo:IdentityDocV3Details/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:ApellationOfOriginNationalRegistrationDetails/ipcdo:IPRightDetails/ipcdo:IPPartyDetails/ipcdo:LetterOfAttorneyDetails/csdo:DocId || ipcdo:ApellationOfOriginApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId; ipcdo:ApellationOfOriginApplicationDetails => ipcdo:ApellationOfOriginApplicationDetails

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 342
- Printed page: 53
- Table/item: Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001; item 13
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_342]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.001.REQ.013
- Wiring: 23OP-RULE-P.SP.03.MSG.001-13;23OP-TRN-P-SP-03-TRN-001;23OP-PRC-P-SP-03-PRC-001
- Positive test: PASS — real XML accepted
- Negative test: PASS — field removal produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_required_application_identifiers_real_xml[13-ApellationOfOriginApplicationId-P.SP.03.MSG.001]

## Gap

- Reason: Production structured rule wired; positive and negative real XML verified.
- Missing information: None for implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production wiring, positive and negative XML proof.
