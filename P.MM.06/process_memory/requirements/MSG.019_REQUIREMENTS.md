# P.MM.06.MSG.019 requirements audit

- Structure: `R.HC.MM.06.003`
- Status: `TABLE_FOUND`
- Table: `20`
- Raw / structured: **10 / 10**
- Count integrity: **PASS**

## Requirement 1

если реквизит "Код страны" (csdo:UnifiedCountryCode) заполнен, то значение атрибута "Идентификатор классификатора" (атрибут codeListId) в его составе должно содержать кодовое обозначение классификатора стран мира, указанного в разделе VII Правил информационного взаимодействия

- Source: table 20, PDF page(s) 150–150
- Semantic category: `CONDITIONAL`
- Literal field references: `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 2

если реквизит "Код страны" (csdo:UnifiedCountryCode) заполнен, то его значение должно соответствовать коду страны согласно классификатору стран мира в соответствии со стандартом ISO 3166-1

- Source: table 20, PDF page(s) 150–150
- Semantic category: `CONDITIONAL`
- Literal field references: `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 3

в электронном сообщении должен быть заполнен реквизит "Номер заявления на регистрацию медицинского изделия" (hcsdo:MedicalProductApplicationId) или реквизит "Номер регистрационного удостоверения" (hcsdo:RegistrationCertificateId)

- Source: table 20, PDF page(s) 150–150
- Semantic category: `REQUIRED`
- Literal field references: `hcsdo:MedicalProductApplicationId`, `hcsdo:RegistrationCertificateId`
- Mapping: `PARTIAL`

## Requirement 4

реквизит "Код вида документа, содержащегося в регистрационном досье на медицинское изделие" (hcsdo:MedicalProductRegistrationDocCode) не заполняется

- Source: table 20, PDF page(s) 150–150
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:MedicalProductRegistrationDocCode`
- Mapping: `PARTIAL`

## Requirement 5

реквизит "Наименование вида документа, содержащегося в регистрационном досье на медицинское изделие" (hcsdo:MedicalProductRegistrationDocName) не заполняется

- Source: table 20, PDF page(s) 150–150
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:MedicalProductRegistrationDocName`
- Mapping: `PARTIAL`

## Requirement 6

реквизит "Код вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileCode) не заполняется

- Source: table 20, PDF page(s) 150–150
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:MedicalProductRegistrationFileCode`
- Mapping: `PARTIAL`

## Requirement 7

реквизит "Наименование вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileName) не заполняется

- Source: table 20, PDF page(s) 151–151
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:MedicalProductRegistrationFileName`
- Mapping: `PARTIAL`

## Requirement 8

реквизит "Описание элемента документа, оформленного при рассмотрении регистрационного досье на медицинское изделие, или документа, содержащегося в регистрационном досье на медицинское изделие" (hcsdo:MedicalProductAttributeText) не заполняется

- Source: table 20, PDF page(s) 151–151
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:MedicalProductAttributeText`
- Mapping: `PARTIAL`

## Requirement 9

реквизит "Документ в формате PDF" (hcsdo:PdfBinaryText) не заполняется

- Source: table 20, PDF page(s) 151–151
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:PdfBinaryText`
- Mapping: `RESOLVED`

## Requirement 10

реквизит "Документ в формате XML" не заполняется

- Source: table 20, PDF page(s) 151–151
- Semantic category: `PROHIBITED`
- Literal field references: none explicitly stated
- Mapping: `UNRESOLVED`
