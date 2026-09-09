# P.MM.06.MSG.002 requirements audit

- Structure: `R.HC.MM.06.001`
- Status: `TABLE_FOUND`
- Table: `14`
- Raw / structured: **47 / 47**
- Count integrity: **PASS**

## Requirement 1

в электронном сообщении должен передаваться 1 экземпляр реквизита "Сведения о зарегистрированном медицинском изделии" (hccdo:MedicalProductDetails)

- Source: table 14, PDF page(s) 110–110
- Semantic category: `CARDINALITY`
- Literal field references: `hccdo:MedicalProductDetails`
- Mapping: `PARTIAL`

## Requirement 2

реквизит "Начальная дата и время" (csdo:StartDateTime) заполняется обязательно

- Source: table 14, PDF page(s) 110–110
- Semantic category: `REQUIRED`
- Literal field references: `csdo:StartDateTime`
- Mapping: `PARTIAL`

## Requirement 3

реквизит "Конечная дата и время" (csdo:EndDateTime) не заполняется

- Source: table 14, PDF page(s) 110–110
- Semantic category: `PROHIBITED`
- Literal field references: `csdo:EndDateTime`
- Mapping: `PARTIAL`

## Requirement 4

значение реквизита "Код статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusCode) не должно быть равно значению "прием заявки"

- Source: table 14, PDF page(s) 110–110
- Semantic category: `CROSS_FIELD`
- Literal field references: `hcsdo:MedicalProductRegistrationStatusCode`
- Mapping: `PARTIAL`

## Requirement 5

если значение реквизита "Код вида заявления на проведение регистрации медицинского изделия и (или) связанных процедур" (hcsdo:MedicalProductApplicationKindV2Code) соответствует значению "заявление об отмене (аннулировании) регистрационного удостоверения медицинского изделия", то реквизиты "Дата истечения срока действия документа" (csdo:DocValidityDate) и "Код статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusCode) заполняются обязательно

- Source: table 14, PDF page(s) 110–110
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductApplicationKindV2Code`, `csdo:DocValidityDate`, `hcsdo:MedicalProductRegistrationCertificateStatusCode`
- Mapping: `PARTIAL`

## Requirement 6

если значение реквизита "Код вида заявления на проведение регистрации медицинского изделия и (или) связанных процедур" (hcsdo:MedicalProductApplicationKindV2Code) соответствует значению "заявление о выдаче дубликата регистрационного удостоверения на медицинское изделие", то реквизит "Дата выдачи дубликата регистрационного удостоверения" (hcsdo:CertificateDuplicateDate) заполняется обязательно

- Source: table 14, PDF page(s) 110–111
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductApplicationKindV2Code`, `hcsdo:CertificateDuplicateDate`
- Mapping: `PARTIAL`

## Requirement 7

если значение реквизита "Код вида заявления на проведение регистрации медицинского изделия и (или) связанных процедур" (hcsdo:MedicalProductApplicationKindV2Code) соответствует значению "заявление о внесении изменений в регистрационное досье медицинского изделия" и значение реквизита "Код статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusCode) соответствует значению "одобрение экспертного заключения", то реквизит "Дата внесения изменений в регистрационное досье медицинского изделия" (hcsdo:RegistrationCertificateModificationDate) заполняется обязательно

- Source: table 14, PDF page(s) 111–111
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductApplicationKindV2Code`, `hcsdo:MedicalProductRegistrationStatusCode`, `hcsdo:RegistrationCertificateModificationDate`
- Mapping: `PARTIAL`

## Requirement 8

если значение реквизита "Код статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusCode) соответствует значению "одобрение экспертного заключения", то реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) заполняется обязательно

- Source: table 14, PDF page(s) 111–111
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationStatusCode`, `hccdo:MedicalProductRegistrationCertificateDetails`
- Mapping: `PARTIAL`

## Requirement 9

если реквизит "Код референтного государства" (hcsdo:ReferenceUnifiedCountryCode), "Код государства признания" (hcsdo:RecognitionUnifiedCountryCode) или "Код страны" (csdo:UnifiedCountryCode) заполнен, то значение атрибута "Идентификатор классификатора" (атрибут codeListId) в его составе должно содержать кодовое обозначение классификатора стран мира, указанного в разделе VII Правил информационного взаимодействия

- Source: table 14, PDF page(s) 111–111
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:ReferenceUnifiedCountryCode`, `hcsdo:RecognitionUnifiedCountryCode`, `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 10

если реквизит "Код референтного государства" (hcsdo:ReferenceUnifiedCountryCode), "Код государства признания" (hcsdo:RecognitionUnifiedCountryCode) или "Код страны" (csdo:UnifiedCountryCode) заполнен, то его значение должно соответствовать коду страны согласно классификатору стран мира в соответствии со стандартом ISO 3166-1

- Source: table 14, PDF page(s) 111–111
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:ReferenceUnifiedCountryCode`, `hcsdo:RecognitionUnifiedCountryCode`, `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 11

если реквизит "Сведения о заявлении на проведение процедур экспертизы и регистрации медицинского изделия" (hccdo:MedicalProductApplicationDetails) заполнен, то должен быть заполнен один из реквизитов "Код статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusCode) или "Наименование статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusName)

- Source: table 14, PDF page(s) 111–111
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductApplicationDetails`, `hcsdo:MedicalProductRegistrationStatusCode`, `hcsdo:MedicalProductRegistrationStatusName`
- Mapping: `PARTIAL`

## Requirement 12

если значение реквизита "Код статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusCode) соответствует значению "другое", то реквизит "Наименование статуса для отслеживания хода рассмотрения заявления о регистрации медицинского изделия" (hcsdo:MedicalProductRegistrationStatusName) заполняется обязательно

- Source: table 14, PDF page(s) 111–111
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationStatusCode`, `hcsdo:MedicalProductRegistrationStatusName`
- Mapping: `PARTIAL`

## Requirement 13

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то должен быть заполнен один из реквизитов "Код статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusCode) или "Наименование статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusName)

- Source: table 14, PDF page(s) 111–112
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hcsdo:MedicalProductRegistrationCertificateStatusCode`, `hcsdo:MedicalProductRegistrationCertificateStatusName`
- Mapping: `PARTIAL`

## Requirement 14

если значение реквизита "Код статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusCode) соответствует значению "другое", то реквизит "Наименование статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusName) заполняется обязательно

- Source: table 14, PDF page(s) 112–112
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationCertificateStatusCode`, `hcsdo:MedicalProductRegistrationCertificateStatusName`
- Mapping: `PARTIAL`

## Requirement 15

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) не заполнен, то реквизит "Сведения о составной части медицинского изделия" (hccdo:MedicalProductSetDetails) не заполняется

- Source: table 14, PDF page(s) 112–112
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hccdo:MedicalProductSetDetails`
- Mapping: `PARTIAL`

## Requirement 16

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) не заполнен, то реквизит "Код вида медицинского изделия" (hcsdo:MedicalProductClassificationCode) не заполняется

- Source: table 14, PDF page(s) 112–112
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hcsdo:MedicalProductClassificationCode`
- Mapping: `PARTIAL`

## Requirement 17

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) не заполнен, то реквизит "Код класса потенциального риска медицинского изделия" (hcsdo:RiskClassCode) не заполняется

- Source: table 14, PDF page(s) 112–112
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hcsdo:RiskClassCode`
- Mapping: `PARTIAL`

## Requirement 18

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) не заполнен, то реквизит "Сведения о производителе медицинского изделия" (hccdo:MedicalProductManufacturingAuthorizationHolderDetails) не заполняется

- Source: table 14, PDF page(s) 112–112
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hccdo:MedicalProductManufacturingAuthorizationHolderDetails`
- Mapping: `PARTIAL`

## Requirement 19

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) не заполнен, то реквизит "Сведения об уполномоченном представителе производителя медицинского изделия" (hccdo:MedicalProductManufacturerAgentDetails) не заполняется

- Source: table 14, PDF page(s) 112–112
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hccdo:MedicalProductManufacturerAgentDetails`
- Mapping: `PARTIAL`

## Requirement 20

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) не заполнен, то реквизит "Инструкция по применению медицинского изделия" (hcsdo:UserGuidePdfBinaryText) не заполняется

- Source: table 14, PDF page(s) 112–112
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hcsdo:UserGuidePdfBinaryText`
- Mapping: `PARTIAL`

## Requirement 21

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) не заполнен, то реквизит "Изображение маркировки медицинского изделия" (hcsdo:ImageMarkingPdfBinaryText) не заполняется

- Source: table 14, PDF page(s) 112–112
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hcsdo:ImageMarkingPdfBinaryText`
- Mapping: `PARTIAL`

## Requirement 22

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то реквизит "Код класса потенциального риска медицинского изделия" (hcsdo:RiskClassCode) заполняется обязательно

- Source: table 14, PDF page(s) 113–113
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hcsdo:RiskClassCode`
- Mapping: `PARTIAL`

## Requirement 23

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то реквизит "Инструкция по применению медицинского изделия" (hcsdo:UserGuidePdfBinaryText) заполняется обязательно

- Source: table 14, PDF page(s) 113–113
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hcsdo:UserGuidePdfBinaryText`
- Mapping: `PARTIAL`

## Requirement 24

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то реквизит "Изображение маркировки медицинского изделия" (hcsdo:ImageMarkingPdfBinaryText) заполняется обязательно

- Source: table 14, PDF page(s) 113–113
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hcsdo:ImageMarkingPdfBinaryText`
- Mapping: `PARTIAL`

## Requirement 25

если значение реквизита "Код статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusCode) не соответствует значению "действует", то реквизит "Дата" (csdo:EventDate) в составе реквизита "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) заполняется обязательно

- Source: table 14, PDF page(s) 113–113
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationCertificateStatusCode`, `csdo:EventDate`, `hccdo:MedicalProductRegistrationCertificateDetails`
- Mapping: `PARTIAL`

## Requirement 26

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то в составе реквизита "Сведения о производителе медицинского изделия" (hccdo:MedicalProductManufacturingAuthorizationHolderDetails) реквизит "Наименование хозяйствующего субъекта" (csdo:BusinessEntityName) заполняется обязательно

- Source: table 14, PDF page(s) 113–113
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hccdo:MedicalProductManufacturingAuthorizationHolderDetails`, `csdo:BusinessEntityName`
- Mapping: `PARTIAL`

## Requirement 27

если значение реквизита "Код статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusCode) не равно значению "аннулировано", то реквизит "Дата истечения срока действия документа" (csdo:DocValidityDate) не заполняется

- Source: table 14, PDF page(s) 113–113
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationCertificateStatusCode`, `csdo:DocValidityDate`
- Mapping: `PARTIAL`

## Requirement 28

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то должен быть заполнен один из реквизитов "Код статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusCode) или "Наименование статуса регистрационного удостоверения медицинского изделия" (hcsdo:MedicalProductRegistrationCertificateStatusName)

- Source: table 14, PDF page(s) 113–113
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hcsdo:MedicalProductRegistrationCertificateStatusCode`, `hcsdo:MedicalProductRegistrationCertificateStatusName`
- Mapping: `PARTIAL`

## Requirement 29

в сведениях о регистрации медицинских изделий, хранящихся в Комиссии, должны содержаться сведения с таким же значением реквизита "Номер заявления на регистрацию медицинского изделия" (hcsdo:MedicalProductApplicationId), в которых реквизит "Конечная дата и время" (csdo:EndDateTime) не заполнен, а также меньшим значением реквизита "Начальная дата и время" (csdo:StartDateTime)

- Source: table 14, PDF page(s) 113–113
- Semantic category: `CONSTRAINT`
- Literal field references: `hcsdo:MedicalProductApplicationId`, `csdo:EndDateTime`, `csdo:StartDateTime`
- Mapping: `PARTIAL`

## Requirement 30

если реквизит "Сведения о регистрационном удостоверении медицинского изделия" (hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то должен быть заполнен реквизит "Код вида медицинского изделия" (hcsdo:MedicalProductClassificationCode)

- Source: table 14, PDF page(s) 114–114
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductRegistrationCertificateDetails`, `hcsdo:MedicalProductClassificationCode`
- Mapping: `PARTIAL`

## Requirement 31

если реквизит "Сведения об уполномоченном представителе производителя медицинского изделия" (hccdo:MedicalProductManufacturerAgentDetails) заполнен, то в его составе реквизит "Наименование хозяйствующего субъекта" (csdo:BusinessEntityName) заполняется обязательно

- Source: table 14, PDF page(s) 114–114
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductManufacturerAgentDetails`, `csdo:BusinessEntityName`
- Mapping: `PARTIAL`

## Requirement 32

в составе реквизитов "Сведения о производителе медицинского изделия" (hccdo:MedicalProductManufacturingAuthorizationHolderDetails) и "Сведения об уполномоченном представителе производителя медицинского изделия" (hccdo:MedicalProductManufacturerAgentDetails) может быть заполнен только один из реквизитов "Код организационно-правовой формы" (csdo:BusinessEntityTypeCode) или "Наименование организационно- правовой формы" (csdo:BusinessEntityTypeName)

- Source: table 14, PDF page(s) 114–114
- Semantic category: `CONSTRAINT`
- Literal field references: `hccdo:MedicalProductManufacturingAuthorizationHolderDetails`, `hccdo:MedicalProductManufacturerAgentDetails`, `csdo:BusinessEntityTypeCode`, `csdo:BusinessEntityTypeName`
- Mapping: `PARTIAL`

## Requirement 33

если реквизит "Код организационно-правовой формы" (csdo:BusinessEntityTypeCode) заполнен, то его значение должно соответствовать коду организационно-правовой формы согласно классификатору, указанному в разделе VII Правил информационного взаимодействия

- Source: table 14, PDF page(s) 114–114
- Semantic category: `CONDITIONAL`
- Literal field references: `csdo:BusinessEntityTypeCode`
- Mapping: `PARTIAL`

## Requirement 34

реквизит "Идентификатор налогоплательщика" (csdo:TaxpayerId) не заполняется

- Source: table 14, PDF page(s) 114–114
- Semantic category: `PROHIBITED`
- Literal field references: `csdo:TaxpayerId`
- Mapping: `PARTIAL`

## Requirement 35

реквизит "Код причины постановки на учет" (csdo:TaxRegistrationReasonCode) не заполняется

- Source: table 14, PDF page(s) 114–114
- Semantic category: `PROHIBITED`
- Literal field references: `csdo:TaxRegistrationReasonCode`
- Mapping: `PARTIAL`

## Requirement 36

если реквизит "Адрес" (ccdo:SubjectAddressDetails) в составе любых реквизитов заполнен, то реквизит "Код страны" (csdo:UnifiedCountryCode) в его составе заполняется обязательно

- Source: table 14, PDF page(s) 114–114
- Semantic category: `CONDITIONAL`
- Literal field references: `ccdo:SubjectAddressDetails`, `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 37

если в составе любого реквизита реквизит "Адрес" (ccdo:SubjectAddressDetails) заполнен, то в его составе должен быть заполнен реквизит "Код вида адреса" (csdo:AddressKindCode)

- Source: table 14, PDF page(s) 114–114
- Semantic category: `CONDITIONAL`
- Literal field references: `ccdo:SubjectAddressDetails`, `csdo:AddressKindCode`
- Mapping: `PARTIAL`

## Requirement 38

если реквизит "Код вида адреса" (csdo:AddressKindCode) в составе реквизита "Адрес" (ccdo:SubjectAddressDetails) заполнен, то его значение должно соответствовать одному из следующих значений: 1 – "адрес регистрации"; 2 – "фактический адрес"; 3 – "почтовый адрес"

- Source: table 14, PDF page(s) 114–114
- Semantic category: `CONDITIONAL`
- Literal field references: `csdo:AddressKindCode`, `ccdo:SubjectAddressDetails`
- Mapping: `PARTIAL`

## Requirement 39

если в составе любого реквизита реквизит "Адрес" (ccdo:SubjectAddressDetails) заполнен, то в его составе должен быть заполнен один из следующих реквизитов: "Город" (csdo:CityName); "Населенный пункт" (csdo:SettlementName)

- Source: table 14, PDF page(s) 114–114
- Semantic category: `CONDITIONAL`
- Literal field references: `ccdo:SubjectAddressDetails`, `csdo:CityName`, `csdo:SettlementName`
- Mapping: `PARTIAL`

## Requirement 40

если реквизиты "Сведения о производителе медицинского изделия" (hccdo:MedicalProductManufacturingAuthorizationHolderDetails) и (или) "Сведения об уполномоченном представителе производителя медицинского изделия" (hccdo:MedicalProductManufacturerAgentDetails) заполнены, то в их составе должны быть заполнен хотя бы один экземпляр реквизита "Контактный реквизит" (ccdo:CommunicationDetails), в котором значение реквизита "Код вида связи" (csdo:CommunicationChannelCode) или "Наименование вида связи" (csdo:CommunicationChannelName) должно соответствовать значению "телефон"

- Source: table 14, PDF page(s) 114–115
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductManufacturingAuthorizationHolderDetails`, `hccdo:MedicalProductManufacturerAgentDetails`, `ccdo:CommunicationDetails`, `csdo:CommunicationChannelCode`, `csdo:CommunicationChannelName`
- Mapping: `PARTIAL`

## Requirement 41

если значение реквизита "Код вида связи" (ccdo:CommunicationChannelCode) или "Наименование вида связи" (csdo:CommunicationChannelName) соответствует значению "электронная почта", значение реквизита "Идентификатор канала связи" (ccdo:CommunicationChannelId) должно соответствовать шаблону ".+@.+\..+"

- Source: table 14, PDF page(s) 115–115
- Semantic category: `CONDITIONAL`
- Literal field references: `ccdo:CommunicationChannelCode`, `csdo:CommunicationChannelName`, `ccdo:CommunicationChannelId`
- Mapping: `PARTIAL`

## Requirement 42

если реквизит "Код вида связи" (csdo:CommunicationChannelCode) заполнен, то его значение должно соответствовать одному из следующих значений: AO – "адрес сайта в сети Интернет"; TE – "телефон"; EM – "электронная почта"; FX – "телефакс"

- Source: table 14, PDF page(s) 115–115
- Semantic category: `CONDITIONAL`
- Literal field references: `csdo:CommunicationChannelCode`
- Mapping: `PARTIAL`

## Requirement 43

если реквизит "Количество составных частей медицинского изделия" (hcsdo:MedicalProductSetMeasure) заполнен, то значение реквизита в его составе "единица измерения" (атрибут measurementUnitCode) должно соответствовать коду единицы измерения согласно классификатору, указанному в разделе VII Правил информационного взаимодействия

- Source: table 14, PDF page(s) 115–115
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductSetMeasure`
- Mapping: `PARTIAL`

## Requirement 44

если реквизит "Наименование медицинского изделия" (hcsdo:MedicalProductName) заполнен, то его значение не должно совпадать с наименованием медицинских изделий в существующих записях реестра медицинских изделий и в существующих записях единого реестра зарегистрированных лекарственных средств Евразийского экономического союза, а также не должно совпадать с наименованием биологически активных добавок к пище, сведения о которых содержатся в едином реестре свидетельств о государственной регистрации продукции

- Source: table 14, PDF page(s) 115–115
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductName`
- Mapping: `PARTIAL`

## Requirement 45

если реквизит "Сведения об уполномоченном представителе производителя медицинского изделия" (hccdo:MedicalProductManufacturerAgentDetails) заполнен, то в его составе реквизит "Код страны" (csdo:UnifiedCountryCode) заполняется обязательно и его значение должно соответствовать коду государства- члена Союза

- Source: table 14, PDF page(s) 115–115
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductManufacturerAgentDetails`, `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 46

если реквизит "Сведения о производителе медицинского изделия" (hccdo:MedicalProductManufacturingAuthorizationHolderDetails) заполнен, то в его составе реквизит "Код страны" (csdo:UnifiedCountryCode) заполняется обязательно

- Source: table 14, PDF page(s) 115–115
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductManufacturingAuthorizationHolderDetails`, `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 47

если реквизит "Сведения о производителе медицинского изделия" (hccdo:MedicalProductManufacturingAuthorizationHolderDetails) заполнен, и в его составе реквизит "Код страны" (csdo:UnifiedCountryCode) не соответствует коду государства-члена Союза, то если реквизит "Сведения об уполномоченном представителе производителя медицинского изделия" (hccdo:MedicalProductManufacturerAgentDetails) заполняется обязательно

- Source: table 14, PDF page(s) 115–116
- Semantic category: `CONDITIONAL`
- Literal field references: `hccdo:MedicalProductManufacturingAuthorizationHolderDetails`, `csdo:UnifiedCountryCode`, `hccdo:MedicalProductManufacturerAgentDetails`
- Mapping: `PARTIAL`
