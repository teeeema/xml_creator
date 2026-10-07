---
id: "P.SP.03.MSG.009.REQ.021"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.009"
requirement: "021"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 225
source_table: "Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 21"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.009.REQ.021

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должен быть заполнен 1 экземпляр реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка (ipsdo:IPSubjectName), в составе которого значение атрибута «код вида представления наименования» (атрибут nameRepresentationKindCode) должно соответствовать значению «OR» – «сведения, представленные на исходном (оригинальном) языке» и атрибут «код языка» (атрибут languageCode) должен быть заполнен

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.001 → P.SP.03.TRN.010 → P.SP.03.MSG.009 → P.SP.03.MSG.009.REQ.021

## XML

- Structure: R.IP.SP.03.001
- QName: ipsdo:IPPartyKindCode; ipsdo:IPSubjectName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode/ipsdo:IPSubjectName

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 225
- Printed page: 59
- Table/item: Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 21
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_225]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.009.REQ.021.or_cardinality;P.SP.03.MSG.009.REQ.021.or_language
- Wiring: 23OP-RULE-P.SP.03.MSG.009-21;23OP-TRN-P-SP-03-TRN-010;23OP-PRC-P-SP-03-PRC-001
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py (message-specific/parametrized real-XML regression)

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
