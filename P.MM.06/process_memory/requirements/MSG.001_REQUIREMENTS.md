# P.MM.06.MSG.001 requirements audit

- Structure: `R.HC.MM.06.001`
- Status: `TABLE_FOUND`
- Table: `13`
- Raw / structured: **24 / 24**
- Count integrity: **PASS**

## Requirement 1

в электронном сообщении должен передаваться 1 экземпляр реквизита "Сведения о зарегистрированном медицинском изделии" (hccdo:MedicalProductDetails)

- Source: table 13, PDF page(s) 108–108
- Semantic category: `CARDINALITY`
- Literal field references: `hccdo:MedicalProductDetails`
- Mapping: `PARTIAL`

## Requirement 2

реквизит "Сведения о заявлении на проведение процедур экспертизы и регистрации медицинского изделия" (hccdo:MedicalProductApplicationDetails) заполняется обязательно

- Source: table 13, PDF page(s) 108–108
- Semantic category: `REQUIRED`
- Literal field references: `hccdo:MedicalProductApplicationDetails`
- Mapping: `PARTIAL`

## Requirement 3

реквизит "Начальная дата и время" (csdo:StartDateTime) заполняется обязательно

- Source: table 13, PDF page(s) 108–108
- Semantic category: `REQUIRED`
- Literal field references: `csdo:StartDateTime`
- Mapping: `PARTIAL`

## Requirement 4

реквизит "Конечная дата и время" (csdo: EndDateTime) не заполняется

- Source: table 13, PDF page(s) 108–108
- Semantic category: `PROHIBITED`
- Literal field references: `csdo:EndDateTime`
- Mapping: `PARTIAL`

## Requirement 5

в сведениях о регистрации медицинских изделий, хранящихся в Комиссии, не должно быть записи, совпадающей по значению реквизита "Номер заявления на регистрацию медицинского изделия" (hcsdo:MedicalProductApplicationId) и с незаполненным реквизитом "Конечная дата и время" (csdo:EndDateTime)

- Source: table 13, PDF page(s) 108–108
- Semantic category: `EXISTENCE`
- Literal field references: `hcsdo:MedicalProductApplicationId`, `csdo:EndDateTime`
- Mapping: `PARTIAL`

## Requirement 6

если значение реквизита "Код вида заявления на проведение регистрации медицинского изделия и (или) связанных процедур" (hcsdo:MedicalProductApplicationKindV2Code) не соответствует значению "заявление на проведение регистрации медицинского изделия" или "заявление на проведение экспертизы медицинского изделия", то реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) заполняется обязательно

- Source: table 13, PDF page(s) 108–108
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductApplicationKindV2Code`, `hccdo:MedicalProductRegistrationCertificateDetails`
- Mapping: `PARTIAL`

## Requirement 7

если значение реквизита "Код вида заявления на проведение регистрации медицинского изделия и (или) связанных процедур" (hcsdo:MedicalProductApplicationKindV2Code) не соответствует значению "заявление на проведение регистрации медицинского изделия" или "заявление на проведение экспертизы медицинского изделия", то сведения о регистрации медицинских изделий, хранящиеся в Комиссии, должны включать в себя сведения, совпадающие по значению реквизита "Номер регистрационного удостоверения" (hcsdo:RegistrationCertificateId)

- Source: table 13, PDF page(s) 108–108
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductApplicationKindV2Code`, `hcsdo:RegistrationCertificateId`
- Mapping: `PARTIAL`

## Requirement 8

если реквизит "Сведения о заявлении на проведение процедур экспертизы и регистрации медицинского изделия" (hccdo:MedicalProductApplicationDetails) заполнен, то должен быть заполнен один из реквизитов "Код статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusCode) или "Наименование статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusName)

- Source: table 13, PDF page(s) 108–108
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductApplicationDetails`, `hcsdo:MedicalProductRegistrationStatusCode`, `hcsdo:MedicalProductRegistrationStatusName`
- Mapping: `PARTIAL`

## Requirement 9

если значение реквизита "Код статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusCode) соответствует значению "другое", то реквизит "Наименование статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusName) заполняется обязательно

- Source: table 13, PDF page(s) 108–108
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationStatusCode`, `hcsdo:MedicalProductRegistrationStatusName`
- Mapping: `PARTIAL`

## Requirement 10

если реквизит "Код референтного государства" (hcsdo:ReferenceUnifiedCountryCode) или "Код государства признания" (hcsdo:RecognitionUnifiedCountryCode) заполнен, то значение атрибута "Идентификатор классификатора" (атрибут codeListId) в его составе должно содержать кодовое обозначение классификатора стран мира, указанного в разделе VII Правил информационного взаимодействия

- Source: table 13, PDF page(s) 109–109
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:ReferenceUnifiedCountryCode`, `hcsdo:RecognitionUnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 11

если реквизит "Код референтного государства" (hcsdo:ReferenceUnifiedCountryCode) или "Код государства признания" (hcsdo:RecognitionUnifiedCountryCode) заполнен, то его значение должно соответствовать коду страны согласно классификатору стран мира в соответствии со стандартом ISO 3166-1

- Source: table 13, PDF page(s) 109–109
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:ReferenceUnifiedCountryCode`, `hcsdo:RecognitionUnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 12

реквизит "Сведения о составной части медицинского изделия" (hccdo:MedicalProductSetDetails) не заполняется

- Source: table 13, PDF page(s) 109–109
- Semantic category: `PROHIBITED`
- Literal field references: `hccdo:MedicalProductSetDetails`
- Mapping: `PARTIAL`

## Requirement 13

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то должен быть заполнен один из реквизитов "Код статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusCode) или "Наименование статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusName)

- Source: table 13, PDF page(s) 109–109
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hcsdo:MedicalProductRegistrationCertificateStatusCode`, `hcsdo:MedicalProductRegistrationCertificateStatusName`
- Mapping: `PARTIAL`

## Requirement 14

если значение реквизита "Код статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusCode) соответствует значению "другое", то реквизит "Наименование статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusName) заполняется обязательно

- Source: table 13, PDF page(s) 109–109
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationCertificateStatusCode`, `hcsdo:MedicalProductRegistrationCertificateStatusName`
- Mapping: `PARTIAL`

## Requirement 15

реквизит "Дата внесения изменений в регистрационное досье медицинского изделия" (hcsdo:RegistrationCertificateModificationDate) не заполняется

- Source: table 13, PDF page(s) 109–109
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:RegistrationCertificateModificationDate`
- Mapping: `PARTIAL`

## Requirement 16

реквизит "Код вида медицинского изделия" (hcsdo:MedicalProductClassificationCode) не заполняется

- Source: table 13, PDF page(s) 109–109
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:MedicalProductClassificationCode`
- Mapping: `PARTIAL`

## Requirement 17

реквизит "Наименование вида медицинского изделия" (hcsdo:MedicalProductClassificationName) не заполняется

- Source: table 13, PDF page(s) 109–109
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:MedicalProductClassificationName`
- Mapping: `PARTIAL`

## Requirement 18

реквизит "Код класса потенциального риска медицинского изделия" (hcsdo:RiskClassCode) не заполняется

- Source: table 13, PDF page(s) 109–109
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:RiskClassCode`
- Mapping: `PARTIAL`

## Requirement 19

реквизит "Сведения о производителе медицинского изделия" (hccdo:MedicalProductManufacturingAuthorizationHolderDetails) не заполняется

- Source: table 13, PDF page(s) 109–109
- Semantic category: `PROHIBITED`
- Literal field references: `hccdo:MedicalProductManufacturingAuthorizationHolderDetails`
- Mapping: `PARTIAL`

## Requirement 20

реквизит "Сведения об уполномоченном представителе производителя медицинского изделия" (hccdo:MedicalProductManufacturerAgentDetails) не заполняется

- Source: table 13, PDF page(s) 109–109
- Semantic category: `PROHIBITED`
- Literal field references: `hccdo:MedicalProductManufacturerAgentDetails`
- Mapping: `PARTIAL`

## Requirement 21

реквизит "Инструкция по применению медицинского изделия" (hcsdo:UserGuidePdfBinaryText) не заполняется

- Source: table 13, PDF page(s) 109–109
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:UserGuidePdfBinaryText`
- Mapping: `PARTIAL`

## Requirement 22

реквизит "Изображение маркировки медицинского изделия" (hcsdo:ImageMarkingPdfBinaryText) не заполняется

- Source: table 13, PDF page(s) 109–109
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:ImageMarkingPdfBinaryText`
- Mapping: `PARTIAL`

## Requirement 23

реквизит "Код государства признания" (hcsdo:RecognitionUnifiedCountryCode) заполняется обязательно

- Source: table 13, PDF page(s) 110–110
- Semantic category: `REQUIRED`
- Literal field references: `hcsdo:RecognitionUnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 24

если реквизит "Наименование медицинского изделия" (hcsdo:MedicalProductName) заполнен, то его значение не должно совпадать с наименованием медицинских изделий в существующих записях реестра медицинских изделий и в существующих записях единого реестра зарегистрированных лекарственных средств Евразийского экономического союза, а также не должно совпадать с наименованием биологически активных добавок к пище, сведения о которых содержатся в едином реестре свидетельств о государственной регистрации продукции

- Source: table 13, PDF page(s) 110–110
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductName`
- Mapping: `PARTIAL`
