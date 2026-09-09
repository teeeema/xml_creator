# P.MM.06.MSG.003 requirements audit

- Structure: `R.HC.MM.06.001`
- Status: `TABLE_FOUND`
- Table: `15`
- Raw / structured: **10 / 10**
- Count integrity: **PASS**

## Requirement 1

в электронном сообщении должен передаваться 1 экземпляр реквизита "Сведения о зарегистрированном медицинском изделии" (hccdo:MedicalProductDetails)

- Source: table 15, PDF page(s) 116–116
- Semantic category: `CARDINALITY`
- Literal field references: `hccdo:MedicalProductDetails`
- Mapping: `PARTIAL`

## Requirement 2

реквизит "Сведения о заявлении на проведение процедур экспертизы и регистрации медицинского изделия" (hccdo:MedicalProductApplicationDetails) заполняется обязательно

- Source: table 15, PDF page(s) 116–116
- Semantic category: `REQUIRED`
- Literal field references: `hccdo:MedicalProductApplicationDetails`
- Mapping: `PARTIAL`

## Requirement 3

реквизит "Конечная дата и время" (csdo: EndDateTime) заполняется обязательно

- Source: table 15, PDF page(s) 116–116
- Semantic category: `REQUIRED`
- Literal field references: `csdo:EndDateTime`
- Mapping: `PARTIAL`

## Requirement 4

реквизит "Начальная дата и время" (csdo:StartDateTime) заполняется обязательно

- Source: table 15, PDF page(s) 116–116
- Semantic category: `REQUIRED`
- Literal field references: `csdo:StartDateTime`
- Mapping: `PARTIAL`

## Requirement 5

сведения о регистрации медицинских изделий, хранящиеся в Комиссии, должны включать в себя сведения, совпадающие по значению реквизита "Номер заявления на регистрацию медицинского изделия" (hcsdo:MedicalProductApplicationId) и с незаполненным реквизитом "Конечная дата и время" (csdo:EndDateTime)

- Source: table 15, PDF page(s) 116–116
- Semantic category: `EXISTENCE`
- Literal field references: `hcsdo:MedicalProductApplicationId`, `csdo:EndDateTime`
- Mapping: `PARTIAL`

## Requirement 6

в электронном сообщении значение реквизита "Конечная дата и время" (csdo:EndDateTime) должно быть больше значения реквизита "Начальная дата и время" (csdo:StartDateTime)

- Source: table 15, PDF page(s) 116–116
- Semantic category: `CROSS_FIELD`
- Literal field references: `csdo:EndDateTime`, `csdo:StartDateTime`
- Mapping: `PARTIAL`

## Requirement 7

если реквизит "Код референтного государства" (hcsdo:ReferenceUnifiedCountryCode), "Код государства признания" (hcsdo:RecognitionUnifiedCountryCode) или "Код страны" (csdo:UnifiedCountryCode) заполнен, то значение атрибута "Идентификатор классификатора" (атрибут codeListId) в его составе должно содержать кодовое обозначение классификатора стран мира, указанного в разделе VII Правил информационного взаимодействия

- Source: table 15, PDF page(s) 116–116
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:ReferenceUnifiedCountryCode`, `hcsdo:RecognitionUnifiedCountryCode`, `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 8

если реквизит "Код референтного государства" (hcsdo:ReferenceUnifiedCountryCode), "Код государства признания" (hcsdo:RecognitionUnifiedCountryCode) или "Код страны" (csdo:UnifiedCountryCode) заполнен, то его значение должно соответствовать коду страны согласно классификатору стран мира в соответствии со стандартом ISO 3166-1

- Source: table 15, PDF page(s) 116–117
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:ReferenceUnifiedCountryCode`, `hcsdo:RecognitionUnifiedCountryCode`, `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 9

если реквизит "Сведения о заявлении на проведение процедур экспертизы и регистрации медицинского изделия" (hccdo:MedicalProductApplicationDetails) заполнен, то должен быть заполнен один из реквизитов "Код статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusCode) или "Наименование статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusName)

- Source: table 15, PDF page(s) 117–117
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductApplicationDetails`, `hcsdo:MedicalProductRegistrationStatusCode`, `hcsdo:MedicalProductRegistrationStatusName`
- Mapping: `PARTIAL`

## Requirement 10

если значение реквизита "Код статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusCode) соответствует значению "другое", то реквизит "Наименование статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusName) заполняется обязательно

- Source: table 15, PDF page(s) 117–117
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationStatusCode`, `hcsdo:MedicalProductRegistrationStatusName`
- Mapping: `PARTIAL`
