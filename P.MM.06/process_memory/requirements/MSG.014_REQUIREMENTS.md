# P.MM.06.MSG.014 requirements audit

- Structure: `R.HC.MM.06.002`
- Status: `TABLE_FOUND`
- Table: `16`
- Raw / structured: **4 / 4**
- Count integrity: **PASS**

## Requirement 1

если реквизит "Код страны" (csdo:UnifiedCountryCode) заполнен, то значение атрибута "Идентификатор классификатора" (атрибут codeListId) в его составе должно содержать кодовое обозначение классификатора стран мира, указанного в разделе VII Правил информационного взаимодействия

- Source: table 16, PDF page(s) 145–146
- Semantic category: `CONDITIONAL`
- Literal field references: `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 2

если реквизит "Код страны" (csdo:UnifiedCountryCode) заполнен, то его значение должно соответствовать коду страны согласно классификатору стран мира в соответствии со стандартом ISO 3166-1

- Source: table 16, PDF page(s) 146–146
- Semantic category: `CONDITIONAL`
- Literal field references: `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 3

в электронном сообщении должен быть заполнен реквизит "Код вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileCode) или реквизит "Наименование вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileName)

- Source: table 16, PDF page(s) 146–146
- Semantic category: `REQUIRED`
- Literal field references: `hcsdo:MedicalProductRegistrationFileCode`, `hcsdo:MedicalProductRegistrationFileName`
- Mapping: `PARTIAL`

## Requirement 4

если значение реквизита "Код вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileCode) соответствует значению "другое", то реквизит "Наименование вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileName) заполняется обязательно

- Source: table 16, PDF page(s) 146–146
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationFileCode`, `hcsdo:MedicalProductRegistrationFileName`
- Mapping: `PARTIAL`
