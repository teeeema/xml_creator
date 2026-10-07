---
id: "P.SP.03.MSG.001.REQ.002"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.001"
requirement: "002"
structure: "R.IP.SP.03.001"
status: "OPEN_SOURCE_CONFLICT"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 339
source_table: "Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001; item 2"
source_item: ""
qname_status: "CONFLICT"
implementation_status: "BLOCKED_SOURCE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.001.REQ.002

## Нормативное требование

в составе реквизита «Сведения о статусном состоянии» (ipcdo:IPStatusDetails) должен быть заполнен реквизит «Дата» (csdo:EventDate), значение реквизита «Код статуса» (csdo:StatusCode) должно соответствовать значению «01» – «новая», атрибут «идентификатор справочника (классификатора)» (атрибут codeListId) в составе реквизита «Код статуса» (csdo:StatusCode) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Таблица требования (PDF стр. 339) указывает ipcdo:IPStatusDetails, а таблица реквизитного состава (PDF стр. 418, таблица 7, реквизит 2.7) для того же статуса указывает ipcdo:IPEntityStatusDetails. Оба находятся в официальном ОП23; без официального разрешения нельзя выбрать QName для production rule.

## Trace

OP23 → P.SP.03.PRC.001 → P.SP.03.TRN.001 → P.SP.03.MSG.001 → P.SP.03.MSG.001.REQ.002

## XML

- Structure: R.IP.SP.03.001
- QName: csdo:EventDate; csdo:StatusCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:IPStatusDetails/csdo:EventDate/csdo:StatusCode

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 339
- Printed page: 50
- Table/item: Таблица 16. Требования к электронному документу (сведениям) P.SP.03.MSG.001; item 2
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_339]]

## Project state

- Status: OPEN_SOURCE_CONFLICT
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.001-2;23OP-TRN-P-SP-03-TRN-001;23OP-PRC-P-SP-03-PRC-001
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование присутствует только как DECLARATIVE_NOT_YET_EXECUTABLE business_rule; structured_rules/correlation_rules/fixed_values/field_usage для OP23 отсутствуют.
- Missing information: Официальное исправление/разъяснение расхождения и опубликованная XSD структуры версии 1.0.0.
- Required action: Добавить минимальный OP23 production structured rule на подтвержденном XML path/QName и два regression cases: корректный и нарушающий требование.
- Closure criterion: Официально подтверждён один QName и path; правило реально вызывается; корректный XML проходит, нарушающий отклоняется.
