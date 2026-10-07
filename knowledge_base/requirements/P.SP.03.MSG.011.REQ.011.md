---
id: "P.SP.03.MSG.011.REQ.011"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.011"
requirement: "011"
structure: "R.IP.SP.03.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 240
source_table: "Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.011; item 11"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "NOT_PROCESSED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.011.REQ.011

## Нормативное требование

если в составе электронного документа (сведений) заполнен экземпляр реквизита «Сведения записи Единого реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails), в составе которого значение одного из заполненных реквизитов «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) или «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) соответствует значению «Ходатайство о выдаче свидетельства о праве использования наименования места происхождения товара Евразийского экономического союза в отношении наименования места происхождения товара, зарегистрированного до вступления в силу Договора о товарных знаках, знаках обслуживания и наименованиях мест происхождения товаров Евразийского экономического союза от 3 февраля 2020 года», значение реквизита «Код вида записи общего информационного ресурса» (ipsdo:ResourceItemKindCode) соответствует значению «AO» – «сведения о НМПТ Союза», то в составе такого экземпляра реквизита «Сведения записи Единого реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails) (далее – экземпляр реквизита «Сведения записи Единого реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails), содержащий сведения о НМПТ Союза, зарегистрированном на основании национального НМПТ) должны быть заполнены реквизиты: «Номер документа» (csdo:DocId); «Дата поступления документа» (ipsdo:IPDocReceiptDate); «Сведения о национальной регистрации НМПТ» (ipcdo:ApellationOfOriginNationalRegistrationDetails)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование записано в OP23 YAML как нормативный текст, но исполняемое правило к нему не подключено. Поэтому валидатор сейчас не проверяет это условие, даже если общий rules engine уже умеет нужные операции.

## Trace

OP23 → P.SP.03.PRC.003 → P.SP.03.TRN.012 → P.SP.03.MSG.011 → P.SP.03.MSG.011.REQ.011

## XML

- Structure: R.IP.SP.03.002
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName; ipsdo:ResourceItemKindCode; csdo:DocId; ipsdo:IPDocReceiptDate; ipcdo:ApellationOfOriginNationalRegistrationDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:ApellationOfOriginRegisterItemDetails/ipsdo:IPDocKindCode/ipsdo:IPDocKindName/ipsdo:ResourceItemKindCode/csdo:DocId/ipsdo:IPDocReceiptDate/ipcdo:ApellationOfOriginNationalRegistrationDetails

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 240
- Printed page: 74
- Table/item: Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.011; item 11
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_240]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.011-11;23OP-TRN-P-SP-03-TRN-012;23OP-PRC-P-SP-03-PRC-003
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование присутствует только как DECLARATIVE_NOT_YET_EXECUTABLE business_rule; structured_rules/correlation_rules/fixed_values/field_usage для OP23 отсутствуют.
- Missing information: Production rule translation and requirement-specific positive/negative real XML proof are not yet completed.
- Required action: Добавить минимальный OP23 production structured rule на подтвержденном XML path/QName и два regression cases: корректный и нарушающий требование.
- Closure criterion: Production rule реально загружается и вызывается; корректный XML проходит; XML с нарушением отклоняется; requirement-specific regression test проходит.
