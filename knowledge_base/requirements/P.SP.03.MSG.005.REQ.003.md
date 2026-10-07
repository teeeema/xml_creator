---
id: "P.SP.03.MSG.005.REQ.003"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.005"
requirement: "003"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 375
source_table: "Таблица 19. Требования к электронному документу (сведениям) P.SP.03.MSG.005; item 3"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.005.REQ.003

## Нормативное требование

в составе экземпляра реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» (ipcdo:ApellationOfOriginApplicationDetails), содержащего изменяемые сведения о заявке на НМПТ Союза, реквизит «Конечная дата и время» (csdo:EndDateTime) должен быть заполнен, и значение этого реквизита должно быть больше значения реквизита «Начальная дата и время» (csdo:StartDateTime) в составе этого экземпляра реквизита «Заявка на НМПТ Союза» (ipcdo:ApellationOfOriginApplicationDetails), и меньше, чем значение реквизита «Начальная дата и время» (csdo:StartDateTime) в составе экземпляра реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» (ipcdo:ApellationOfOriginApplicationDetails), содержащего измененные сведения о заявке на НМПТ Союза

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.004 → P.SP.03.TRN.004 → P.SP.03.MSG.005 → P.SP.03.MSG.005.REQ.003

## XML

- Structure: R.IP.SP.03.001
- QName: ipcdo:ApellationOfOriginApplicationDetails; csdo:EndDateTime; csdo:StartDateTime
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:ApellationOfOriginApplicationDetails => ipcdo:ApellationOfOriginApplicationDetails; csdo:EndDateTime => ipcdo:ApellationOfOriginApplicationDetails/ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime; csdo:StartDateTime => ipcdo:ApellationOfOriginApplicationDetails/ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 375
- Printed page: 86
- Table/item: Таблица 19. Требования к электронному документу (сведениям) P.SP.03.MSG.005; item 3
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_375]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.005.REQ.003.after_old_start;P.SP.03.MSG.005.REQ.003.before_new_start
- Wiring: 23OP-RULE-P.SP.03.MSG.005-3;23OP-TRN-P-SP-03-TRN-004;23OP-PRC-P-SP-03-PRC-004
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py::test_req003_ordered_typed_datetime_real_xml[P.SP.03.MSG.005]

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
