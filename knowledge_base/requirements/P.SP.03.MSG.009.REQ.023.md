---
id: "P.SP.03.MSG.009.REQ.023"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.009"
requirement: "023"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 226
source_table: "Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 23"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.009.REQ.023

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель» и если в составе реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка (ipsdo:IPSubjectName) значение атрибута «код языка» (атрибут languageCode) не соответствует значению «RU», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должен быть заполнен второй экземпляр реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка (ipsdo:IPSubjectName), в составе которого значение атрибута «код вида представления наименования» (атрибут nameRepresentationKindCode) должно соответствововать значению «LA» – «транслитерация сведений на исходном (оригинальном) языке буквами латинского алфавита» и атрибут «код языка» (атрибут languageCode) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.001 → P.SP.03.TRN.010 → P.SP.03.MSG.009 → P.SP.03.MSG.009.REQ.023

## XML

- Structure: R.IP.SP.03.001
- QName: ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ipsdo:IPSubjectName
- Namespace: MISSING / UNRESOLVED
- Path: UNCONFIRMED_NOT_MAPPED

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 226
- Printed page: 60
- Table/item: Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 23
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_226]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.009.REQ.023
- Wiring: 23OP-RULE-P.SP.03.MSG.009-23;23OP-TRN-P-SP-03-TRN-010;23OP-PRC-P-SP-03-PRC-001
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py (message-specific/parametrized real-XML regression)

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
