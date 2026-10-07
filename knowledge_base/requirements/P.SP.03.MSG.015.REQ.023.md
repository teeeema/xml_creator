---
id: "P.SP.03.MSG.015.REQ.023"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.015"
requirement: "023"
structure: "R.IP.SP.03.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 279
source_table: "Таблица 24. Требования к электронному документу (сведениям) P.SP.03.MSG.015; item 23; inherited from Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.011 item 23"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "NOT_PROCESSED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.015.REQ.023

## Нормативное требование

если в составе электронного документа (сведений) заполнен экземпляр реквизита «Сведения записи Единого реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails), содержащий сведения о праве использования НМПТ Союза, или если в составе электронного документа (сведений) заполнен экземпляр реквизита «Сведения записи Единого реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails), содержащий сведения о предоставленном на основании национального свидетельства праве использования НМПТ Союза, то в составе такого экземпляра реквизита «Сведения записи Единого реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails) реквизит «НМПТ Союза» (ipcdo:ApellationOfOriginDetails) должен быть заполнен и в его составе должны быть заполнены следующие реквизиты: «Регистрационный номер НМПТ Союза» (ipsdo:ApellationOfOriginEAEUId); «Указание товара, в отношении которого осуществляется регистрация и (или) предоставление права использования НМПТ» (ipsdo:ApellationOfOriginGoodsText); «Описание особого свойства товара» (ipsdo:GoodsPropertiesDescriptionText); «Описание географического объекта или его границ» (ipsdo:GeographicRegionDescriptionText) Inherited semantic requirement 23 from P.SP.03.MSG.011 as stated by range 3-29 in P.SP.03.MSG.015.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование записано в OP23 YAML как нормативный текст, но исполняемое правило к нему не подключено. Поэтому валидатор сейчас не проверяет это условие, даже если общий rules engine уже умеет нужные операции.

## Trace

OP23 → P.SP.03.PRC.007 → P.SP.03.TRN.016 → P.SP.03.MSG.015 → P.SP.03.MSG.015.REQ.023

## XML

- Structure: R.IP.SP.03.002
- QName: ipcdo:ApellationOfOriginDetails; ipsdo:ApellationOfOriginEAEUId; ipsdo:ApellationOfOriginGoodsText; ipsdo:GoodsPropertiesDescriptionText; ipsdo:GeographicRegionDescriptionText
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:ApellationOfOriginRegisterItemDetails/ipcdo:ApellationOfOriginDetails/ipsdo:ApellationOfOriginEAEUId/ipsdo:ApellationOfOriginGoodsText/ipsdo:GoodsPropertiesDescriptionText/ipsdo:GeographicRegionDescriptionText

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 279
- Printed page: 113
- Table/item: Таблица 24. Требования к электронному документу (сведениям) P.SP.03.MSG.015; item 23; inherited from Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.011 item 23
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_279]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.015-3-29;23OP-RULE-P.SP.03.MSG.011-23;23OP-TRN-P-SP-03-TRN-016;23OP-PRC-P-SP-03-PRC-007
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование присутствует только как DECLARATIVE_NOT_YET_EXECUTABLE business_rule; structured_rules/correlation_rules/fixed_values/field_usage для OP23 отсутствуют.
- Missing information: Production rule translation and requirement-specific positive/negative real XML proof are not yet completed.
- Required action: Добавить минимальный OP23 production structured rule на подтвержденном XML path/QName и два regression cases: корректный и нарушающий требование.
- Closure criterion: Production rule реально загружается и вызывается; корректный XML проходит; XML с нарушением отклоняется; requirement-specific regression test проходит.
