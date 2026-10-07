---
id: "P.SP.03.MSG.023.REQ.014"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.023"
requirement: "014"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 285
source_table: "Таблица 27. Требования к электронному документу (сведениям) P.SP.03.MSG.023; item 14"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.023.REQ.014

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «PA» – «представитель заявителя, являющийся патентным поверенным» или «RE» – «представитель заявителя, не являющийся патентным поверенным», то в составе такого экземпляра реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» в составе реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName) атрибут «код вида представления наименования» (атрибут nameRepresentationKindCode) не заполняется, а атрибут «код языка» (атрибут languageCode) должен быть заполнен и его значение должно соответствовать значению «RU»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.009 → P.SP.03.TRN.018 → P.SP.03.MSG.023 → P.SP.03.MSG.023.REQ.014

## XML

- Structure: R.IP.SP.03.003
- QName: ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ipsdo:IPSubjectName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:IPPartyDetails => ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode => ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode; ipsdo:IPSubjectName => ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails/ipsdo:IPSubjectName

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 285
- Printed page: 119
- Table/item: Таблица 27. Требования к электронному документу (сведениям) P.SP.03.MSG.023; item 14
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_285]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.023.REQ.014
- Wiring: 23OP-RULE-P.SP.03.MSG.023-14;23OP-TRN-P-SP-03-TRN-018;23OP-PRC-P-SP-03-PRC-009;23OP-R.IP.SP.03.003-8-9;23OP-R.IP.SP.03.003-8-9-1;23OP-R.IP.SP.03.003-8-9-3
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg023_req014_representative_name_attributes_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
