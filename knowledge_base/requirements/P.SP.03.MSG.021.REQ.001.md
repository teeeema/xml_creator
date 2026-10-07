---
id: "P.SP.03.MSG.021.REQ.001"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.021"
requirement: "001"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 281
source_table: "Таблица 25. Требования к электронному документу (сведениям) P.SP.03.MSG.021; item 1"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.021.REQ.001

## Нормативное требование

в составе реквизита «Национальное патентное ведомство» (ipcdo:PatentAuthorityDetails) должен быть заполнены реквизиты «Код страны» (csdo:UnifiedCountryCode) и «Наименование уполномоченного органа» (csdo:AuthorityName)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.008 → P.SP.03.TRN.017 → P.SP.03.MSG.021 → P.SP.03.MSG.021.REQ.001

## XML

- Structure: R.IP.SP.03.003
- QName: ipcdo:PatentAuthorityDetails; csdo:UnifiedCountryCode; csdo:AuthorityName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:PatentAuthorityDetails => ipcdo:PatentAuthorityDetails || ipcdo:IPPaymentDetails/ipcdo:PatentAuthorityDetails; csdo:UnifiedCountryCode => ipcdo:PatentAuthorityDetails/csdo:UnifiedCountryCode || ipcdo:PatentAuthorityDetails/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:PatentAuthorityDetails/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:PatentAuthorityDetails/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ccdo:IdentityDocV3Details/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ccdo:SubjectAddressDetails/csdo:UnifiedCountryCode || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ipcdo:LetterOfAttorneyDetails/csdo:UnifiedCountryCode; csdo:AuthorityName => ipcdo:PatentAuthorityDetails/csdo:AuthorityName || ipcdo:IPPaymentDetails/ipcdo:PatentAuthorityDetails/csdo:AuthorityName || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ccdo:IdentityDocV3Details/csdo:AuthorityName || ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ipcdo:LetterOfAttorneyDetails/csdo:AuthorityName

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 281
- Printed page: 115
- Table/item: Таблица 25. Требования к электронному документу (сведениям) P.SP.03.MSG.021; item 1
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_281]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.021.REQ.001
- Wiring: 23OP-RULE-P.SP.03.MSG.021-1;23OP-TRN-P-SP-03-TRN-017;23OP-PRC-P-SP-03-PRC-008;23OP-R.IP.SP.03.003-2;23OP-R.IP.SP.03.003-8-5;23OP-R.IP.SP.03.003-2-1;23OP-R.IP.SP.03.003-2-5-2;23OP-R.IP.SP.03.003-8-5-1;23OP-R.IP.SP.03.003-8-5-5-2;23OP-R.IP.SP.03.003-8-9-2;23OP-R.IP.SP.03.003-8-9-11-1;23OP-R.IP.SP.03.003-8-9-12-2;23OP-R.IP.SP.03.003-8-9-15-1;23OP-R.IP.SP.03.003-2-3;23OP-R.IP.SP.03.003-8-5-3;23OP-R.IP.SP.03.003-8-9-11-9;23OP-R.IP.SP.03.003-8-9-15-11
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg021_req001_authority_fields_required_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
