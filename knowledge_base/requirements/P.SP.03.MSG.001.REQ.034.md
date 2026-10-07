---
id: "P.SP.03.MSG.001.REQ.034"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.001"
requirement: "034"
structure: "R.IP.SP.03.001"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 348
source_table: "Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001; item 34"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "NOT_PROCESSED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.001.REQ.034

## Нормативное требование

если в составе реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» (ipcdo:ApellationOfOriginApplicationDetails) значение реквизита «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) или реквизита «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) соответствует значению «Заявка на регистрацию и предоставление права использования наименования места происхождения товара Евразийского экономического союза», в составе реквизита «НМПТ Союза» (ipcdo:ApellationOfOriginDetails) реквизит «Регистрационный номер НМПТ Союза» (ipsdo:ApellationOfOriginEAEUId) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование записано в OP23 YAML как нормативный текст, но исполняемое правило к нему не подключено. Поэтому валидатор сейчас не проверяет это условие, даже если общий rules engine уже умеет нужные операции.

## Trace

OP23 → P.SP.03.PRC.001 → P.SP.03.TRN.001 → P.SP.03.MSG.001 → P.SP.03.MSG.001.REQ.034

## XML

- Structure: R.IP.SP.03.001
- QName: ipcdo:ApellationOfOriginApplicationDetails; ipsdo:IPDocKindCode; ipsdo:IPDocKindName; ipcdo:ApellationOfOriginDetails; ipsdo:ApellationOfOriginEAEUId
- Namespace: MISSING / UNRESOLVED
- Path: UNCONFIRMED_NOT_MAPPED

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 348
- Printed page: 59
- Table/item: Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001; item 34
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_348]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.001-34;23OP-TRN-P-SP-03-TRN-001;23OP-PRC-P-SP-03-PRC-001
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование присутствует только как DECLARATIVE_NOT_YET_EXECUTABLE business_rule; structured_rules/correlation_rules/fixed_values/field_usage для OP23 отсутствуют.
- Missing information: Production rule translation and requirement-specific positive/negative real XML proof are not yet completed.
- Required action: Добавить минимальный OP23 production structured rule на подтвержденном XML path/QName и два regression cases: корректный и нарушающий требование.
- Closure criterion: Production rule реально загружается и вызывается; корректный XML проходит; XML с нарушением отклоняется; requirement-specific regression test проходит.
