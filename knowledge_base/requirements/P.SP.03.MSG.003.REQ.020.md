---
id: "P.SP.03.MSG.003.REQ.020"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.003"
requirement: "020"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 352
source_table: "Таблица 17. Требования к электронному документу (сведениям) P.SP.03.MSG.003; item 20; inherited from Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001 item 20"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.003.REQ.020

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то значение атрибута «Код вида представления наименования» (атрибут nameRepresentationKindCode) в составе реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка (ipsdo:IPSubjectName) должно соответствовать одному из следующих значений: «OR» – «сведения, представленные на исходном (оригинальном) языке»; «LA» – «транслитерация сведений на исходном (оригинальном) языке буквами латинского алфавита» Inherited semantic requirement 20 from P.SP.03.MSG.001 as stated by range 4-45 in P.SP.03.MSG.003.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.002 → P.SP.03.TRN.002 → P.SP.03.MSG.003 → P.SP.03.MSG.003.REQ.020

## XML

- Structure: R.IP.SP.03.001
- QName: ipsdo:IPPartyKindCode; ipsdo:IPSubjectName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode/ipsdo:IPSubjectName

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 352
- Printed page: 63
- Table/item: Таблица 17. Требования к электронному документу (сведениям) P.SP.03.MSG.003; item 20; inherited from Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001 item 20
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_352]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.003.REQ.020
- Wiring: 23OP-RULE-P.SP.03.MSG.003-4-45;23OP-RULE-P.SP.03.MSG.001-20;23OP-TRN-P-SP-03-TRN-002;23OP-PRC-P-SP-03-PRC-002
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py (message-specific/parametrized real-XML regression)

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
