---
id: "P.SP.03.MSG.022.REQ.004"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.022"
requirement: "004"
structure: "R.IP.SP.03.003"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 283
source_table: "Таблица 26. Требования к электронному документу (сведениям) P.SP.03.MSG.022; item 4; inherited from Таблица 25. Требования к электронному документу (сведениям) P.SP.03.MSG.021 item 4"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "NOT_PROCESSED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.022.REQ.004

## Нормативное требование

при включении справочника видов юридически значимых действий при регистрации, правовой охране и использовании товарных знаков Союза, знаков обслуживания Союза и НМПТ Союза в состав ресурсов единой системы нормативно-справочной информации Союза, реквизит «Код вида юридически значимого действия» (ipsdo:IPLegalActionKindCode) должен быть заполнен и должен соответствовать значению «Регистрация и (или) выдача свидетельства о праве использования НМПТ Союза», а реквизит «Наименование вида юридически значимого действия» (ipsdo:IPLegalActionKindName) не заполняется Inherited semantic requirement 4 from P.SP.03.MSG.021 as stated by range 1-6 in P.SP.03.MSG.022.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование записано в OP23 YAML как нормативный текст, но исполняемое правило к нему не подключено. Поэтому валидатор сейчас не проверяет это условие, даже если общий rules engine уже умеет нужные операции.

## Trace

OP23 → P.SP.03.PRC.008 → P.SP.03.TRN.017 → P.SP.03.MSG.022 → P.SP.03.MSG.022.REQ.004

## XML

- Structure: R.IP.SP.03.003
- QName: ipsdo:IPLegalActionKindCode; ipsdo:IPLegalActionKindName
- Namespace: MISSING / UNRESOLVED
- Path: UNCONFIRMED_NOT_MAPPED

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 283
- Printed page: 117
- Table/item: Таблица 26. Требования к электронному документу (сведениям) P.SP.03.MSG.022; item 4; inherited from Таблица 25. Требования к электронному документу (сведениям) P.SP.03.MSG.021 item 4
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_283]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.022-1-6;23OP-RULE-P.SP.03.MSG.021-4;23OP-TRN-P-SP-03-TRN-017;23OP-PRC-P-SP-03-PRC-008
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование присутствует только как DECLARATIVE_NOT_YET_EXECUTABLE business_rule; structured_rules/correlation_rules/fixed_values/field_usage для OP23 отсутствуют.
- Missing information: Production rule translation and requirement-specific positive/negative real XML proof are not yet completed.
- Required action: Добавить минимальный OP23 production structured rule на подтвержденном XML path/QName и два regression cases: корректный и нарушающий требование.
- Closure criterion: Production rule реально загружается и вызывается; корректный XML проходит; XML с нарушением отклоняется; requirement-specific regression test проходит.
