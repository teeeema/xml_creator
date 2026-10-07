---
id: "P.SP.03.MSG.015.REQ.001"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.015"
requirement: "001"
structure: "R.IP.SP.03.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 279
source_table: "Таблица 24. Требования к электронному документу (сведениям) P.SP.03.MSG.015; item 1"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "NOT_PROCESSED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.015.REQ.001

## Нормативное требование

в электронном документе (сведениях) должно быть заполнено 2 экземпляра реквизита «Сведения записи Единого реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails), содержащих соответственно изменяемые сведения Единого реестра НМПТ Союза и измененные сведения Единого реестра НМПТ Союза, содержащие информацию о прекращении действия свидетельства о праве использования НМПТ Союза (далее – измененные сведения Единого реестра НМПТ Союза)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование записано в OP23 YAML как нормативный текст, но исполняемое правило к нему не подключено. Поэтому валидатор сейчас не проверяет это условие, даже если общий rules engine уже умеет нужные операции.

## Trace

OP23 → P.SP.03.PRC.007 → P.SP.03.TRN.016 → P.SP.03.MSG.015 → P.SP.03.MSG.015.REQ.001

## XML

- Structure: R.IP.SP.03.002
- QName: ipcdo:ApellationOfOriginRegisterItemDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:ApellationOfOriginRegisterItemDetails

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 279
- Printed page: 113
- Table/item: Таблица 24. Требования к электронному документу (сведениям) P.SP.03.MSG.015; item 1
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_279]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.015-1;23OP-TRN-P-SP-03-TRN-016;23OP-PRC-P-SP-03-PRC-007
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование присутствует только как DECLARATIVE_NOT_YET_EXECUTABLE business_rule; structured_rules/correlation_rules/fixed_values/field_usage для OP23 отсутствуют.
- Missing information: Production rule translation and requirement-specific positive/negative real XML proof are not yet completed.
- Required action: Добавить минимальный OP23 production structured rule на подтвержденном XML path/QName и два regression cases: корректный и нарушающий требование.
- Closure criterion: Production rule реально загружается и вызывается; корректный XML проходит; XML с нарушением отклоняется; requirement-specific regression test проходит.
