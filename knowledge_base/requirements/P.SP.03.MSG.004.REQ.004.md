---
id: "P.SP.03.MSG.004.REQ.004"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.004"
requirement: "004"
structure: "R.IP.SP.03.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 355
source_table: "Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.004; item 4"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.004.REQ.004

## Нормативное требование

при включении в классификатор видов документов, сведений и материалов значений, соответствующих видам документов «Заявка на регистрацию и предоставление права использования наименования места происхождения товара Евразийского экономического союза», «Заявка на предоставление права использования зарегистрированного наименования места происхождения товара Евразийского экономического союза» и «Ходатайство о выдаче свидетельства о праве использования наименования места происхождения товара Евразийского экономического союза в отношении наименования места происхождения товара, зарегистрированного до вступления в силу Договора о товарных знаках, знаках обслуживания и наименованиях мест происхождения товаров Евразийского экономического союза от 3 февраля 2020 года», в составе реквизита «Сведения записи Единого реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails) реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) должен быть заполнен и должен содержать кодовое обозначение одного из перечисленных видов документов, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Правило зависит от того, присутствует ли нужное значение в официальном классификаторе. В текущем репозитории нет подтвержденного snapshot/версии этого классификатора, поэтому валидатор не может достоверно выбрать нормативную ветку и проверить правило.

## Trace

OP23 → P.SP.03.PRC.003 → P.SP.03.TRN.003 → P.SP.03.MSG.004 → P.SP.03.MSG.004.REQ.004

## XML

- Structure: R.IP.SP.03.002
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:ApellationOfOriginRegisterItemDetails/ipsdo:IPDocKindCode/ipsdo:IPDocKindName

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 355
- Printed page: 66
- Table/item: Таблица 18. Требования к электронному документу (сведениям) P.SP.03.MSG.004; item 4
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_355]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.004-4;23OP-TRN-P-SP-03-TRN-003;23OP-PRC-P-SP-03-PRC-003
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Нормативный текст захвачен, но исполняемого OP23 production rule нет; проверка зависит от фактического состояния официального классификатора.
- Missing information: Подтвержденное актуальное содержимое и версия соответствующего официального классификатора.
- Required action: Получить и зафиксировать официальный classifier snapshot/version, затем добавить OP23 structured rule и regression tests.
- Closure criterion: Есть подтвержденный classifier source/version; production rule вызывается; positive XML проходит; negative XML отклоняется.
