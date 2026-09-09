# P.MM.06.MSG.021 requirements audit

- Structure: `R.HC.MM.06.003`
- Status: `TABLE_FOUND`
- Table: `22`
- Raw / structured: **11 / 11**
- Count integrity: **PASS**

## Requirement 1

если реквизит "Код страны" (csdo:UnifiedCountryCode) заполнен, то значение атрибута "Идентификатор классификатора" (атрибут codeListId) в его составе должно содержать кодовое обозначение классификатора стран мира, указанного в разделе VII Правил информационного взаимодействия

- Source: table 22, PDF page(s) 153–153
- Semantic category: `CONDITIONAL`
- Literal field references: `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 2

если реквизит "Код страны" (csdo:UnifiedCountryCode) заполнен, то его значение должно соответствовать коду страны согласно классификатору стран мира в соответствии со стандартом ISO 3166-1

- Source: table 22, PDF page(s) 153–153
- Semantic category: `CONDITIONAL`
- Literal field references: `csdo:UnifiedCountryCode`
- Mapping: `PARTIAL`

## Requirement 3

в электронном сообщении должен быть заполнен реквизит "Номер заявления на регистрацию медицинского изделия" (hcsdo:MedicalProductApplicationId) или реквизит "Номер регистрационного удостоверения" (hcsdo:RegistrationCertificateId)

- Source: table 22, PDF page(s) 153–153
- Semantic category: `REQUIRED`
- Literal field references: `hcsdo:MedicalProductApplicationId`, `hcsdo:RegistrationCertificateId`
- Mapping: `PARTIAL`

## Requirement 4

если значение реквизита "Признак принадлежности документа к регистрационному досье" (hcsdo:RegistrationFileIndicator) соответствует значению "документ, содержащийся в регистрационном досье на медицинское изделие", то должен быть заполнен реквизит "Код вида документа, содержащегося в регистрационном досье на медицинское изделие" (hcsdo:MedicalProductRegistrationDocCode) или реквизит "Наименование вида документа, содержащегося в регистрационном досье на медицинское изделие" (hcsdo:MedicalProductRegistrationDocName)

- Source: table 22, PDF page(s) 153–153
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:RegistrationFileIndicator`, `hcsdo:MedicalProductRegistrationDocCode`, `hcsdo:MedicalProductRegistrationDocName`
- Mapping: `PARTIAL`

## Requirement 5

если значение реквизита "Признак принадлежности документа к регистрационному досье" (hcsdo:RegistrationFileIndicator) соответствует значению "документ, оформленный при рассмотрении регистрационного досье", то должен быть заполнен реквизит "Код вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileCode) или реквизит "Наименование вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileName)

- Source: table 22, PDF page(s) 153–154
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:RegistrationFileIndicator`, `hcsdo:MedicalProductRegistrationFileCode`, `hcsdo:MedicalProductRegistrationFileName`
- Mapping: `PARTIAL`

## Requirement 6

если значение реквизита "Код вида документа, содержащегося в регистрационном досье на медицинское изделие" (hcsdo:MedicalProductRegistrationDocCode) соответствует значению "другое", то реквизит "Наименование вида документа, содержащегося в регистрационном досье на медицинское изделие" (hcsdo:MedicalProductRegistrationDocName) заполняется обязательно

- Source: table 22, PDF page(s) 154–154
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationDocCode`, `hcsdo:MedicalProductRegistrationDocName`
- Mapping: `PARTIAL`

## Requirement 7

если значение реквизита "Код вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileCode) соответствует значению "другое", то реквизит "Наименование вида документа, оформленного при рассмотрении регистрационного досье на медицинское изделие" (hcsdo:MedicalProductRegistrationFileName) заполняется обязательно

- Source: table 22, PDF page(s) 154–154
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductRegistrationFileCode`, `hcsdo:MedicalProductRegistrationFileName`
- Mapping: `PARTIAL`

## Requirement 8

если реквизит "Описание элемента документа, оформленного при рассмотрении регистрационного досье на медицинское изделие, или документа, содержащегося в регистрационном досье на медицинское изделие" (hcsdo:MedicalProductAttributeText) заполнен, то должен быть заполнен реквизит "Код вида элемента документа" (атрибут MedicalProductAttributeKindCode) или реквизит "Наименование вида элемента документа" (атрибут MedicalProductAttributeKindName)

- Source: table 22, PDF page(s) 154–154
- Semantic category: `CONDITIONAL`
- Literal field references: `hcsdo:MedicalProductAttributeText`
- Mapping: `PARTIAL`

## Requirement 9

если значение реквизита "Код вида элемента документа" (атрибут MedicalProductAttributeKindCode) соответствует значению "другое", то реквизит "Наименование вида элемента документа" (атрибут MedicalProductAttributeKindName) заполняется обязательно

- Source: table 22, PDF page(s) 154–154
- Semantic category: `CONDITIONAL`
- Literal field references: none explicitly stated
- Mapping: `UNRESOLVED`

## Requirement 10

реквизит "Документ в формате PDF" (hcsdo:PdfBinaryText) не заполняется

- Source: table 22, PDF page(s) 154–154
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:PdfBinaryText`
- Mapping: `RESOLVED`

## Requirement 11

реквизит "Документ в формате XML" не заполняется

- Source: table 22, PDF page(s) 154–154
- Semantic category: `PROHIBITED`
- Literal field references: none explicitly stated
- Mapping: `UNRESOLVED`
