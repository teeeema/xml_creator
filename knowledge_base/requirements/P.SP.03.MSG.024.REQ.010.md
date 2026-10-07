---
id: "P.SP.03.MSG.024.REQ.010"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.024"
requirement: "010"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 287
source_table: "Таблица 28. Требования к электронному документу (сведениям) P.SP.03.MSG.024; item 10; inherited from Таблица 27. Требования к электронному документу (сведениям) P.SP.03.MSG.023 item 10"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.024.REQ.010

## Нормативное требование

в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должны быть заполнены реквизиты: «Код страны» (csdo:UnifiedCountryCode); «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName) Inherited semantic requirement 10 from P.SP.03.MSG.023 as stated by range 1-19 in P.SP.03.MSG.024.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.009 → P.SP.03.TRN.018 → P.SP.03.MSG.024 → P.SP.03.MSG.024.REQ.010

## XML

- Structure: R.IP.SP.03.003
- QName: ipcdo:IPPartyDetails; csdo:UnifiedCountryCode; ipsdo:IPSubjectName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:IPPartyDetails => ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails; csdo:UnifiedCountryCode => ipcdo:PatentAuthorityDetails/csdo:UnifiedCountryCode || ipcdo:PatentAuthorityDetails/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:PatentAuthorityDetails/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:PatentAuthorityDetails/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ccdo:IdentityDocV3Details/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ipcdo:LetterOfAttorneyDetails/csdo:UnifiedCountryCode; ipsdo:IPSubjectName => ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ipsdo:IPSubjectName

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 287
- Printed page: 121
- Table/item: Таблица 28. Требования к электронному документу (сведениям) P.SP.03.MSG.024; item 10; inherited from Таблица 27. Требования к электронному документу (сведениям) P.SP.03.MSG.023 item 10
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_287]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.024.REQ.010
- Wiring: 23OP-RULE-P.SP.03.MSG.024-1-19;23OP-RULE-P.SP.03.MSG.023-10;23OP-TRN-P-SP-03-TRN-018;23OP-PRC-P-SP-03-PRC-009;23OP-R.IP.SP.03.003-8-9;23OP-R.IP.SP.03.003-2-1;23OP-R.IP.SP.03.003-2-5-2;23OP-R.IP.SP.03.003-8-5-1;23OP-R.IP.SP.03.003-8-5-5-2;23OP-R.IP.SP.03.003-8-9-2;23OP-R.IP.SP.03.003-8-9-11-1;23OP-R.IP.SP.03.003-8-9-12-2;23OP-R.IP.SP.03.003-8-9-15-1;23OP-R.IP.SP.03.003-8-9-3
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg024_inherited_req001_to_req018_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
