---
id: "P.SP.03.MSG.007.REQ.016"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.007"
requirement: "016"
structure: "R.IP.SP.03.002"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf; semantic source ОП_23.pdf"
source_pages: 395
source_table: "Таблица 21. Требования к электронному документу (сведениям) P.SP.03.MSG.007; item 16; inherited from Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.006 item 16"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.007.REQ.016

## Нормативное требование

если в экземплярах реквизита «Сведения записи Единого реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails) значение реквизита «Код вида записи общего информационного ресурса» (ipsdo:ResourceItemKindCode) соответствует значению «RH» – «сведения о праве использования НМПТ Союза», то в информационных ресурсах Комиссии, содержащих сведения Единого реестра НМПТ Союза, должна содержаться запись, в составе которой значение реквизита «Код вида записи общего информационного ресурса» (ipsdo:ResourceItemKindCode) соответствует значению «RH» – «сведения о праве использования НМПТ Союза», значение свокупности реквизитов «Регистрационный номер свидетельства о праве использования НМПТ Союза» (ipsdo:ApellationOfOriginEAEUCertificateId), «Дата истечения срока действия документа» (csdo:DocValidityDate), «Код статуса» (csdo:StatusCode) и «Начальная дата и время» (csdo:StartDateTime) совпадают со значениями совокупности соответствующих реквизитов в представляемых изменяемых сведениях Единого реестра НМПТ Союза, а реквизит «Конечная дата и время» (csdo:EndDateTime) в составе реквизита «Технологические характеристики записи общего ресурса» (ccdo:ResourceItemStatusDetails) не заполнен Inherited semantic requirement 16 from P.SP.03.MSG.006 as stated by range 3-31 in P.SP.03.MSG.007.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Правило нельзя проверить только по текущему XML: оно требует найти или сопоставить запись во внешнем информационном ресурсе Комиссии/национального ведомства. В проекте нет подтвержденного локального реестра или интерфейса, который дает эти данные.

## Trace

OP23 → P.SP.03.PRC.006 → P.SP.03.TRN.006 → P.SP.03.MSG.007 → P.SP.03.MSG.007.REQ.016

## XML

- Structure: R.IP.SP.03.002
- QName: ipsdo:ResourceItemKindCode; ipsdo:ApellationOfOriginEAEUCertificateId; csdo:DocValidityDate; csdo:StatusCode; csdo:StartDateTime; csdo:EndDateTime; ccdo:ResourceItemStatusDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:ApellationOfOriginRegisterItemDetails/ipsdo:ResourceItemKindCode/ipsdo:ApellationOfOriginEAEUCertificateId/csdo:DocValidityDate/csdo:StatusCode/csdo:StartDateTime/csdo:EndDateTime/ccdo:ResourceItemStatusDetails

## Source

- Document: ОП_23.pdf; semantic source ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 395
- Printed page: 106
- Table/item: Таблица 21. Требования к электронному документу (сведениям) P.SP.03.MSG.007; item 16; inherited from Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.006 item 16
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_395]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.007-3-31;23OP-RULE-P.SP.03.MSG.006-16;23OP-TRN-P-SP-03-TRN-006;23OP-PRC-P-SP-03-PRC-006
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование требует сверки с внешним информационным ресурсом; локального источника реестровых данных и исполняемого OP23 rule нет.
- Missing information: Доступные и нормативно подтвержденные данные внешнего информационного ресурса и правила их актуальности.
- Required action: Определить нормативный источник внешних данных и способ офлайн-проверки/fixture, затем подключить production rule и tests.
- Closure criterion: Внешний источник подтвержден и доступен валидатору; lookup/correlation реализованы; positive/negative registry cases покрыты тестами.
