---
id: "P.SP.03.MSG.009.REQ.003"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.009"
requirement: "003"
structure: "R.IP.SP.03.001"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 221
source_table: "Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 3"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.009.REQ.003

## Нормативное требование

в информационных ресурсах национального патентного ведомства, содержащих сведения о заявках на НМПТ Союза, не должно содержаться записи, в составе которой значение реквизита «Регистрационный номер заявки на НМПТ Союза» (ipsdo:ApellationOfOriginApplicationId) совпадает со значением реквизита «Регистрационный номер заявки на НМПТ Союза» (ipsdo:ApellationOfOriginApplicationId) в представляемых сведениях, реквизит «Код статуса» (csdo:StatusCode) равен значению «01» – «новая» или «02» – «изменена», а реквизит «Конечная дата и время» (csdo:EndDateTime) в составе реквизита «Технологические характеристики записи общего ресурса» (ccdo:ResourceItemStatusDetails) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Правило нельзя проверить только по текущему XML: оно требует найти или сопоставить запись во внешнем информационном ресурсе Комиссии/национального ведомства. В проекте нет подтвержденного локального реестра или интерфейса, который дает эти данные.

## Trace

OP23 → P.SP.03.PRC.001 → P.SP.03.TRN.010 → P.SP.03.MSG.009 → P.SP.03.MSG.009.REQ.003

## XML

- Structure: R.IP.SP.03.001
- QName: csdo:StatusCode; csdo:EndDateTime; ccdo:ResourceItemStatusDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:ApellationOfOriginApplicationId/csdo:StatusCode/csdo:EndDateTime/ccdo:ResourceItemStatusDetails

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 221
- Printed page: 55
- Table/item: Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.009; item 3
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_221]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.009-3;23OP-TRN-P-SP-03-TRN-010;23OP-PRC-P-SP-03-PRC-001
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование требует сверки с внешним информационным ресурсом; локального источника реестровых данных и исполняемого OP23 rule нет.
- Missing information: Доступные и нормативно подтвержденные данные внешнего информационного ресурса и правила их актуальности.
- Required action: Определить нормативный источник внешних данных и способ офлайн-проверки/fixture, затем подключить production rule и tests.
- Closure criterion: Внешний источник подтвержден и доступен валидатору; lookup/correlation реализованы; positive/negative registry cases покрыты тестами.
