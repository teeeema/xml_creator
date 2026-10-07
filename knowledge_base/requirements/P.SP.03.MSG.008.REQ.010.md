---
id: "P.SP.03.MSG.008.REQ.010"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.008"
requirement: "010"
structure: "R.IP.SP.03.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 398
source_table: "Таблица 22. Требования к электронному документу (сведениям) P.SP.03.MSG.008; item 10; inherited from Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.006 item 10"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "NOT_PROCESSED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.008.REQ.010

## Нормативное требование

если в составе экземпляров реквизита «Сведения записи Единого реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails) заполнены реквизиты «Регистрационный номер заявки на НМПТ Союза» (ipsdo:ApellationOfOriginApplicationId) и «Дата подачи заявки» (ipsdo:ApplicationReceiptDate), значение реквизитов «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) или «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) в составе таких экземпляров реквизитов должны совпадать, и должны соответствовать значению «Заявка на предоставление права использования зарегистрированного наименования места происхождения товара Евразийского экономического союза» или «Заявка на регистрацию и предоставление права использования наименования места происхождения товара Евразийского экономического союза» Inherited semantic requirement 10 from P.SP.03.MSG.006 as stated by range 3-31 in P.SP.03.MSG.008.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование записано в OP23 YAML как нормативный текст, но исполняемое правило к нему не подключено. Поэтому валидатор сейчас не проверяет это условие, даже если общий rules engine уже умеет нужные операции.

## Trace

OP23 → P.SP.03.PRC.007 → P.SP.03.TRN.007 → P.SP.03.MSG.008 → P.SP.03.MSG.008.REQ.010

## XML

- Structure: R.IP.SP.03.002
- QName: ipsdo:ApellationOfOriginApplicationId; ipsdo:ApplicationReceiptDate; ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:ApellationOfOriginRegisterItemDetails/ipsdo:ApellationOfOriginApplicationId/ipsdo:ApplicationReceiptDate/ipsdo:IPDocKindCode/ipsdo:IPDocKindName

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 398
- Printed page: 109
- Table/item: Таблица 22. Требования к электронному документу (сведениям) P.SP.03.MSG.008; item 10; inherited from Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.006 item 10
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_398]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.008-3-31;23OP-RULE-P.SP.03.MSG.006-10;23OP-TRN-P-SP-03-TRN-007;23OP-PRC-P-SP-03-PRC-007
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование присутствует только как DECLARATIVE_NOT_YET_EXECUTABLE business_rule; structured_rules/correlation_rules/fixed_values/field_usage для OP23 отсутствуют.
- Missing information: Production rule translation and requirement-specific positive/negative real XML proof are not yet completed.
- Required action: Добавить минимальный OP23 production structured rule на подтвержденном XML path/QName и два regression cases: корректный и нарушающий требование.
- Closure criterion: Production rule реально загружается и вызывается; корректный XML проходит; XML с нарушением отклоняется; requirement-specific regression test проходит.
