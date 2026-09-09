# P.MM.06.MSG.016 requirements audit

- Structure: `R.HC.MM.06.002`
- Status: `TABLE_FOUND`
- Table: `18`
- Raw / structured: **6 / 6**
- Count integrity: **PASS**

## Requirement 1

если реквизит "Код страны" (csdo:UnifiedCountryCode) заполнен, то значение атрибута "Идентификатор классификатора" (атрибут codeListId) в его составе должно содержать кодовое обозначение классификатора стран мира, указанного в разделе VII Правил информационного взаимодействия

- Source: table 18, PDF page(s) 147–147
- Semantic category: `CONDITIONAL`
- Literal field references: `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 2

если реквизит "Код страны" (csdo:UnifiedCountryCode) заполнен, то его значение должно соответствовать коду страны согласно классификатору стран мира в соответствии со стандартом ISO 3166-1

- Source: table 18, PDF page(s) 147–147
- Semantic category: `CONDITIONAL`
- Literal field references: `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 3

в электронном сообщении должен быть заполнен реквизит "Код вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileCode) или реквизит "Наименование вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileName)

- Source: table 18, PDF page(s) 147–147
- Semantic category: `REQUIRED`
- Literal field references: `hcsdo:MedicalProductRegistrationFileCode`, `hcsdo:MedicalProductRegistrationFileName`
- Mapping: `PARTIAL`

## Requirement 4

если значение реквизита "Код вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileCode) соответствует значению "другое", то реквизит "Наименование вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileName) заполняется обязательно

- Source: table 18, PDF page(s) 147–147
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationFileCode`, `hcsdo:MedicalProductRegistrationFileName`
- Mapping: `PARTIAL`

## Requirement 5

значение реквизита "Код вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileCode) или реквизита "Наименование вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileName) должно соответствовать значению "Подтверждение признания (непризнания) экспертного заключения"

- Source: table 18, PDF page(s) 148–148
- Semantic category: `CROSS_FIELD`
- Literal field references: `hcsdo:MedicalProductRegistrationFileCode`, `hcsdo:MedicalProductRegistrationFileName`
- Mapping: `PARTIAL`

## Requirement 6

реквизит "Признак согласования документа" (hcsdo:DocAgreementIndicator) заполняется обязательно

- Source: table 18, PDF page(s) 148–148
- Semantic category: `REQUIRED`
- Literal field references: `hcsdo:DocAgreementIndicator`
- Mapping: `PARTIAL`
