---
id: "P.SP.03.MSG.023.REQ.006"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.023"
requirement: "006"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 284
source_table: "Таблица 27. Требования к электронному документу (сведениям) P.SP.03.MSG.023; item 6; inherited from Таблица 25. Требования к электронному документу (сведениям) P.SP.03.MSG.021 item 6"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.023.REQ.006

## Нормативное требование

реквизит «Регистрационный номер заявки на НМПТ Союза» (ipsdo:ApellationOfOriginApplicationId) должен быть заполнен Inherited semantic requirement 6 from P.SP.03.MSG.021 as stated by range 1-6 in P.SP.03.MSG.023.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.009 → P.SP.03.TRN.018 → P.SP.03.MSG.023 → P.SP.03.MSG.023.REQ.006

## XML

- Structure: R.IP.SP.03.003
- QName: ipsdo:ApellationOfOriginApplicationId
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:ApellationOfOriginApplicationId => ipsdo:ApellationOfOriginApplicationId

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 284
- Printed page: 118
- Table/item: Таблица 27. Требования к электронному документу (сведениям) P.SP.03.MSG.023; item 6; inherited from Таблица 25. Требования к электронному документу (сведениям) P.SP.03.MSG.021 item 6
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_284]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.023.REQ.006
- Wiring: 23OP-RULE-P.SP.03.MSG.023-1-6;23OP-RULE-P.SP.03.MSG.021-6;23OP-TRN-P-SP-03-TRN-018;23OP-PRC-P-SP-03-PRC-009;23OP-R.IP.SP.03.003-6
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg023_req006_inherited_application_id_required_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
