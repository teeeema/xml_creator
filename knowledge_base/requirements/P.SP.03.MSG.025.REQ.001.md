---
id: "P.SP.03.MSG.025.REQ.001"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.025"
requirement: "001"
structure: "R.IP.SP.03.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 288
source_table: "Таблица 29. Требования к электронному документу (сведениям) P.SP.03.MSG.025; item 1"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.025.REQ.001

## Нормативное требование

реквизиты «Дата и время обновления» (csdo:UpdateDateTime) и «Код страны» (csdo:UnifiedCountryCode) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.012 → P.SP.03.TRN.019 → P.SP.03.MSG.025 → P.SP.03.MSG.025.REQ.001

## XML

- Structure: R.IP.SP.03.007
- QName: csdo:UpdateDateTime; csdo:UnifiedCountryCode
- Namespace: MISSING / UNRESOLVED
- Path: csdo:UpdateDateTime => csdo:UpdateDateTime; csdo:UnifiedCountryCode => csdo:UnifiedCountryCode

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 288
- Printed page: 122
- Table/item: Таблица 29. Требования к электронному документу (сведениям) P.SP.03.MSG.025; item 1
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_288]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.025.REQ.001.update_datetime;P.SP.03.MSG.025.REQ.001.country_code
- Wiring: 23OP-RULE-P.SP.03.MSG.025-1;23OP-TRN-P-SP-03-TRN-019;23OP-PRC-P-SP-03-PRC-012
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_msg025_req001_both_forbidden_fields_real_xml

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
