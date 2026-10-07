---
id: "P.SP.03.MSG.003.REQ.049"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.003"
requirement: "049"
structure: "R.IP.SP.03.001"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 353
source_table: "Таблица 17. Требования к электронному документу (сведениям) P.SP.03.MSG.003; item 49"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.003.REQ.049

## Нормативное требование

при отсутствии в классификаторе видов документов, сведений и материалов значения, соответствующего виду документа «Ходатайство о внесении изменений в заявку на регистрацию и (или) предоставление права использования наименования места происхождения товара Евразийского экономического союза», в составе экземпляра реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)», в составе экземпляра реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» (ipcdo:ApellationOfOriginApplicationDetails), содержащего измененные сведения о заявке на НМПТ Союза, в составе реквизита «Сведения о статусном состоянии» (ipcdo:IPStatusDetails) реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) не заполняется, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) должен быть заполнен, и его значение должно соответствовать значению «Ходатайство о внесении изменений в заявку на регистрацию и (или) предоставление права использования наименования места происхождения товара Евразийского экономического союза»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Правило зависит от того, присутствует ли нужное значение в официальном классификаторе. В текущем репозитории нет подтвержденного snapshot/версии этого классификатора, поэтому валидатор не может достоверно выбрать нормативную ветку и проверить правило.

## Trace

OP23 → P.SP.03.PRC.002 → P.SP.03.TRN.002 → P.SP.03.MSG.003 → P.SP.03.MSG.003.REQ.049

## XML

- Structure: R.IP.SP.03.001
- QName: ipcdo:IPStatusDetails; ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:ApellationOfOriginApplicationDetails/ipcdo:IPStatusDetails/ipsdo:IPDocKindCode/ipsdo:IPDocKindName

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 353
- Printed page: 64
- Table/item: Таблица 17. Требования к электронному документу (сведениям) P.SP.03.MSG.003; item 49
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_353]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.003-49;23OP-TRN-P-SP-03-TRN-002;23OP-PRC-P-SP-03-PRC-002
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Нормативный текст захвачен, но исполняемого OP23 production rule нет; проверка зависит от фактического состояния официального классификатора.
- Missing information: Подтвержденное актуальное содержимое и версия соответствующего официального классификатора.
- Required action: Получить и зафиксировать официальный classifier snapshot/version, затем добавить OP23 structured rule и regression tests.
- Closure criterion: Есть подтвержденный classifier source/version; production rule вызывается; positive XML проходит; negative XML отклоняется.
