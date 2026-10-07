---
id: "P.SP.03.MSG.006.REQ.027"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.006"
requirement: "027"
structure: "R.IP.SP.03.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 388
source_table: "Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.006; item 27"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "NOT_PROCESSED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.006.REQ.027

## Нормативное требование

если реквизит «Адрес» (ccdo:SubjectAddressDetails) заполнен в составе любых реквизитов, в его составе должны быть заполнены реквизиты «Код вида адреса» (csdo:AddressKindCode)», «Код страны» (csdo:UnifiedCountryCode), «Город» (csdo:CityName), «Улица» (csdo:StreetName) и «Номер дома» (csdo:BuildingNumberId)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование записано в OP23 YAML как нормативный текст, но исполняемое правило к нему не подключено. Поэтому валидатор сейчас не проверяет это условие, даже если общий rules engine уже умеет нужные операции. Старый аудит относил это требование к ENGINE_UNSUPPORTED, но текущий rules_engine уже содержит нужные общие примитивы; открытым остается именно отсутствие OP23 mapping.

## Trace

OP23 → P.SP.03.PRC.005 → P.SP.03.TRN.005 → P.SP.03.MSG.006 → P.SP.03.MSG.006.REQ.027

## XML

- Structure: R.IP.SP.03.002
- QName: csdo:AddressKindCode; csdo:UnifiedCountryCode; csdo:CityName; csdo:StreetName; csdo:BuildingNumberId
- Namespace: MISSING / UNRESOLVED
- Path: ccdo:SubjectAddressDetails/csdo:AddressKindCode/csdo:UnifiedCountryCode/csdo:CityName/csdo:StreetName/csdo:BuildingNumberId

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 388
- Printed page: 99
- Table/item: Таблица 20. Требования к электронному документу (сведениям) P.SP.03.MSG.006; item 27
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_388]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.006-27;23OP-TRN-P-SP-03-TRN-005;23OP-PRC-P-SP-03-PRC-005
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование присутствует только как DECLARATIVE_NOT_YET_EXECUTABLE business_rule; structured_rules/correlation_rules/fixed_values/field_usage для OP23 отсутствуют. Старый аудит относил это требование к ENGINE_UNSUPPORTED, но текущий rules_engine уже содержит нужные общие примитивы; открытым остается именно отсутствие OP23 mapping.
- Missing information: Production rule translation and requirement-specific positive/negative real XML proof are not yet completed.
- Required action: Добавить минимальный OP23 production structured rule на подтвержденном XML path/QName и два regression cases: корректный и нарушающий требование.
- Closure criterion: Production rule реально загружается и вызывается; корректный XML проходит; XML с нарушением отклоняется; requirement-specific regression test проходит.
