---
id: "P.SP.03.MSG.025.REQ.006"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.025"
requirement: "006"
structure: "R.IP.SP.03.007"
status: "OPEN_MISSING_NORMATIVE_DATA"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 288
source_table: "Таблица 29. Требования к электронному документу (сведениям) P.SP.03.MSG.025; item 6"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "BLOCKED_SOURCE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.025.REQ.006

## Нормативное требование

в составе реквизита «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails) реквизиты «Документ в бинарном формате» (csdo:DocBinaryText) и «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) не заполняются

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

PDF стр. 288, таблица 29, требование 6 запрещает csdo:DocBinaryText. Таблица 16 структуры R.IP.SP.03.007 (PDF стр. 573-574) не перечисляет этот дочерний элемент, но контейнер имеет тип ipcdo:IPDocDetailsType. В других структурах ОП23 этот же тип содержит DocBinaryText (PDF стр. 468/531/565). Без официальной XSD и импортированного определения типа нельзя определить фактический XML content model для MSG.025.

## Trace

OP23 → P.SP.03.PRC.012 → P.SP.03.TRN.019 → P.SP.03.MSG.025 → P.SP.03.MSG.025.REQ.006

## XML

- Structure: R.IP.SP.03.007
- QName: ipcdo:AccompanyingDocumentsDetails; csdo:DocBinaryText; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: UNCONFIRMED_NOT_MAPPED

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 288
- Printed page: 122
- Table/item: Таблица 29. Требования к электронному документу (сведениям) P.SP.03.MSG.025; item 6
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_288]]

## Project state

- Status: OPEN_MISSING_NORMATIVE_DATA
- Production rule: NONE — message_rules has no structured_rules/correlation_rules/fixed_values/field_usage mapping for this requirement.
- Wiring: 23OP-RULE-P.SP.03.MSG.025-6;23OP-TRN-P-SP-03-TRN-019;23OP-PRC-P-SP-03-PRC-012
- Positive test: MISSING — add XML/value case satisfying this exact requirement after production mapping.
- Negative test: MISSING — add XML/value case violating this exact requirement and assert rejection.
- Runtime proof: NONE requirement-specific. Existing P.SP.03_OP_23/tests/test_psp03_package.py validates catalog/counts/generation only.

## Gap

- Reason: Требование присутствует только как DECLARATIVE_NOT_YET_EXECUTABLE business_rule; structured_rules/correlation_rules/fixed_values/field_usage для OP23 отсутствуют.
- Missing information: Опубликованная XSD EEC_R_IP_SP_03_ApellationOfOriginRegisterRequestDetails_v1.0.0.xsd и импортированная схема с ipcdo:IPDocDetailsType (M.IP.CDT.00003).
- Required action: Добавить минимальный OP23 production structured rule на подтвержденном XML path/QName и два regression cases: корректный и нарушающий требование.
- Closure criterion: Официальные XSD разрешают состав контейнера; positive XML без DocBinaryText проходит; negative XML с точным QName отклоняется валидатором.
