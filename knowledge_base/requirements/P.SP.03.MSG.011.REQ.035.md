---
id: "P.SP.03.MSG.011.REQ.035"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.011"
requirement: "035"
structure: "R.IP.SP.03.002"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 252
source_table: "Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.011; item 35"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.011.REQ.035

## Нормативное требование

если в составе электронного документа (сведений) заполнен экземпляр реквизита «Сведения записи Единого реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails), содержащий сведения о предоставленном на основании национального свидетельства праве использования НМПТ Союза, то для каждого заполненного в его составе экземпляра реквизита «Сведения о национальной регистрации НМПТ» (ipcdo:ApellationOfOriginNationalRegistrationDetails) должно выполняться правило: в информационных ресурсах национального патентного ведомства, содержащих сведения о НМПТ, зарегистрированных до вступления в силу Договора, должна содержаться запись, в составе которой значение реквизита «Код вида записи общего информационного ресурса» (ipsdo:ResourceItemKindCode) соответствует значению «RN» – «сведения о праве использования национального НМПТ», «Код статуса» (csdo:StatusCode) соответствует значению «30» – «национальное право использования НМПТ действует», реквизит «Конечная дата и время» (csdo:EndDateTime) в составе реквизита «Технологические характеристики записи общего ресурса» (ccdo:ResourceItemStatusDetails) не заполнен, а совокупность значений реквизитов «Код страны» (csdo:UnifiedCountryCode) и «Регистрационный номер свидетельства» (ipsdo:CertificateId) в составе реквизита «Сведения о национальной регистрации НМПТ» (ipcdo:ApellationOfOriginNationalRegistrationDetails) совпадает со значением соответствующих реквизитов в составе реквизита «Сведения о национальной регистрации НМПТ» (ipcdo:ApellationOfOriginNationalRegistrationDetails) в представляемых сведениях

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Правило нельзя проверить только по текущему XML: оно требует найти или сопоставить запись во внешнем информационном ресурсе Комиссии/национального ведомства. В проекте нет подтвержденного локального реестра или интерфейса, который дает эти данные.

## Trace

OP23 → P.SP.03.PRC.003 → P.SP.03.TRN.012 → P.SP.03.MSG.011 → P.SP.03.MSG.011.REQ.035

## XML

- Structure: R.IP.SP.03.002
- QName: ipcdo:ApellationOfOriginNationalRegistrationDetails; ipsdo:ResourceItemKindCode; csdo:StatusCode; csdo:EndDateTime; ccdo:ResourceItemStatusDetails; csdo:UnifiedCountryCode; ipsdo:CertificateId
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:ApellationOfOriginRegisterItemDetails/ipcdo:ApellationOfOriginNationalRegistrationDetails/ipsdo:ResourceItemKindCode/csdo:StatusCode/csdo:EndDateTime/ccdo:ResourceItemStatusDetails/csdo:UnifiedCountryCode/ipsdo:CertificateId

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 252
- Printed page: 86
- Table/item: Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.011; item 35
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_252]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.011-35;23OP-TRN-P-SP-03-TRN-012;23OP-PRC-P-SP-03-PRC-003
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование требует сверки с внешним информационным ресурсом; локального источника реестровых данных и исполняемого OP23 rule нет.
- Missing information: Доступные и нормативно подтвержденные данные внешнего информационного ресурса и правила их актуальности.
- Required action: Определить нормативный источник внешних данных и способ офлайн-проверки/fixture, затем подключить production rule и tests.
- Closure criterion: Внешний источник подтвержден и доступен валидатору; lookup/correlation реализованы; positive/negative registry cases покрыты тестами.
