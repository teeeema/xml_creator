---
id: "P.SP.03.MSG.010.REQ.052"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.010"
requirement: "052"
structure: "R.IP.SP.03.001"
status: "OPEN_SOURCE_CONFLICT"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 235
source_table: "Таблица 19. Требования к электронному документу (сведениям) P.SP.03.MSG.010; item 52"
source_item: ""
qname_status: "CONFLICT"
implementation_status: "BLOCKED_SOURCE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.010.REQ.052

## Нормативное требование

в составе экземпляра реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» (ipcdo:ApellationOfOriginApplicationDetails), содержащего измененные сведения о заявке на НМПТ Союза, реквизит «Сведения о статусном состоянии» (ipcdo:IPStatusDetails) должен быть заполнен, значение реквизита «Код статуса» (csdo:StatusCode) в его составе должно соответствовать значению «02» – «изменена», а атрибут «идентификатор справочника (классификатора)» (атрибут codeListId) в составе реквизита «Код статуса» (csdo:StatusCode) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Таблица требования (PDF стр. 235) указывает ipcdo:IPStatusDetails, а таблица реквизитного состава (PDF стр. 418, таблица 7, реквизит 2.7) для того же статуса указывает ipcdo:IPEntityStatusDetails. Оба находятся в официальном ОП23; без официального разрешения нельзя выбрать QName для production rule.

## Trace

OP23 → P.SP.03.PRC.002 → P.SP.03.TRN.011 → P.SP.03.MSG.010 → P.SP.03.MSG.010.REQ.052

## XML

- Structure: R.IP.SP.03.001
- QName: ipcdo:IPStatusDetails; csdo:StatusCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:ApellationOfOriginApplicationDetails/ipcdo:IPStatusDetails/csdo:StatusCode

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 235
- Printed page: 69
- Table/item: Таблица 19. Требования к электронному документу (сведениям) P.SP.03.MSG.010; item 52
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_235]]

## Project state

- Status: OPEN_SOURCE_CONFLICT
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.010-52;23OP-TRN-P-SP-03-TRN-011;23OP-PRC-P-SP-03-PRC-002
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование присутствует только как DECLARATIVE_NOT_YET_EXECUTABLE business_rule; structured_rules/correlation_rules/fixed_values/field_usage для OP23 отсутствуют.
- Missing information: Официальное исправление/разъяснение расхождения и опубликованная XSD структуры версии 1.0.0.
- Required action: Добавить минимальный OP23 production structured rule на подтвержденном XML path/QName и два regression cases: корректный и нарушающий требование.
- Closure criterion: Официально подтверждён один QName и path; правило реально вызывается; корректный XML проходит, нарушающий отклоняется.
