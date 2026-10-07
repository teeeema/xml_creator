---
layer: "KNOWLEDGE"
structure_id: "R.HC.MM.01.003"
generated_by: "knowledge_base/tools/build_kb.py"
---


# R.HC.MM.01.003 Fields

| ID | Path | Datatype | Cardinality | Source | Evidence |
|---|---|---|---|---|---|
| 1 | EDocHeader | ccdo:EDocHeaderType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.424 table 16 item 1 | CONFIRMED_PDF_SOURCE_REF |
| 1.1 | EDocHeader/InfEnvelopeCode | csdo:InfEnvelopeCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.424 table 16 item 1.1 | CONFIRMED_PDF_SOURCE_REF |
| 1.2 | EDocHeader/EDocCode | csdo:EDocCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.424 table 16 item 1.2 | CONFIRMED_PDF_SOURCE_REF |
| 1.3 | EDocHeader/EDocId | csdo:UniversallyUniqueIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.425 table 16 item 1.3 | CONFIRMED_PDF_SOURCE_REF |
| 1.4 | EDocHeader/EDocRefId | csdo:UniversallyUniqueIdType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.425 table 16 item 1.4 | CONFIRMED_PDF_SOURCE_REF |
| 1.5 | EDocHeader/EDocDateTime | bdt:DateTimeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.425 table 16 item 1.5 | CONFIRMED_PDF_SOURCE_REF |
| 1.6 | EDocHeader/LanguageCode | csdo:LanguageCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.425 table 16 item 1.6 | CONFIRMED_PDF_SOURCE_REF |
| 2 | UnifiedCountryCode | csdo:UnifiedCountryCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.425 table 16 item 2 | CONFIRMED_PDF_SOURCE_REF |
| 2.а | UnifiedCountryCode/@codeListId | csdo:ReferenceDataIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.426 table 16 item 2.а | CONFIRMED_PDF_SOURCE_REF |
| 3 | RegistrationNumberId | hcsdo:RegistrationNumberIdType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.426 table 16 item 3 | CONFIRMED_PDF_SOURCE_REF |
| 4 | ApplicationId | csdo:Id50Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.426 table 16 item 4 | CONFIRMED_PDF_SOURCE_REF |
| 5 | RegistrationKindCode | csdo:Code10Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.426 table 16 item 5 | CONFIRMED_PDF_SOURCE_REF |
| 6 | RegistrationDossierDocDetails | hccdo:RegistrationDossierDocDetails | 0..None | Решение Коллегии ЕЭК от 19.04.2022 №68 p.427 table 16 item 6 | CONFIRMED_PDF_SOURCE_REF |
| 6.1 | RegistrationDossierDocDetails/RegistrationFileIndicator | bdt:IndicatorType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.427 table 16 item 6.1 | CONFIRMED_PDF_SOURCE_REF |
| 6.2 | RegistrationDossierDocDetails/DocId | csdo:Id50Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.427 table 16 item 6.2 | CONFIRMED_PDF_SOURCE_REF |
| 6.3 | RegistrationDossierDocDetails/DocName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.427 table 16 item 6.3 | CONFIRMED_PDF_SOURCE_REF |
| 6.4 | RegistrationDossierDocDetails/DrugRegistrationDocCode | hcsdo:DrugRegistrationDocCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.428 table 16 item 6.4 | CONFIRMED_PDF_SOURCE_REF |
| 6.4.а | RegistrationDossierDocDetails/DrugRegistrationDocCode/@codeListId | csdo:ReferenceDataIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.428 table 16 item 6.4.а | CONFIRMED_PDF_SOURCE_REF |
| 6.5 | RegistrationDossierDocDetails/DrugRegistrationDocName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.428 table 16 item 6.5 | CONFIRMED_PDF_SOURCE_REF |
| 6.6 | RegistrationDossierDocDetails/DrugRegistrationFileCode | hcsdo:DrugRegistrationFileCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.428 table 16 item 6.6 | CONFIRMED_PDF_SOURCE_REF |
| 6.6.а | RegistrationDossierDocDetails/DrugRegistrationFileCode/@codeListId | csdo:ReferenceDataIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.429 table 16 item 6.6.а | CONFIRMED_PDF_SOURCE_REF |
| 6.7 | RegistrationDossierDocDetails/DrugRegistrationFileName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.429 table 16 item 6.7 | CONFIRMED_PDF_SOURCE_REF |
| 6.8 | RegistrationDossierDocDetails/DocCreationDate | bdt:DateType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.429 table 16 item 6.8 | CONFIRMED_PDF_SOURCE_REF |
| 6.9 | RegistrationDossierDocDetails/DocValidityDate | bdt:DateType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.429 table 16 item 6.9 | CONFIRMED_PDF_SOURCE_REF |
| 6.10 | RegistrationDossierDocDetails/BusinessEntityName | csdo:Name300Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.429 table 16 item 6.10 | CONFIRMED_PDF_SOURCE_REF |
| 6.11 | RegistrationDossierDocDetails/DrugAttributeEnumText | hcsdo:AttributeTextType | 0..None | Решение Коллегии ЕЭК от 19.04.2022 №68 p.430 table 16 item 6.11 | CONFIRMED_PDF_SOURCE_REF |
| 6.11.а | RegistrationDossierDocDetails/DrugAttributeEnumText/@DrugAttributeKindEnumCode | csdo:Code10Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.430 table 16 item 6.11.а | CONFIRMED_PDF_SOURCE_REF |
| 6.11.б | RegistrationDossierDocDetails/DrugAttributeEnumText/@AttributeKindName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.430 table 16 item 6.11.б | CONFIRMED_PDF_SOURCE_REF |
| 6.12 | RegistrationDossierDocDetails/DocCopyBinaryText | csdo:BinaryTextType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.430 table 16 item 6.12 | CONFIRMED_PDF_SOURCE_REF |
| 6.12.а | RegistrationDossierDocDetails/DocCopyBinaryText/@mediaTypeCode | csdo:MediaTypeCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.430 table 16 item 6.12.а | CONFIRMED_PDF_SOURCE_REF |
| 6.13 | RegistrationDossierDocDetails/AnyDetails | ccdo:AnyDetailsType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.431 table 16 item 6.13 | CONFIRMED_PDF_SOURCE_REF |
| 6.13.1 | RegistrationDossierDocDetails/AnyDetails/* | ANY_XML | 1..None | Решение Коллегии ЕЭК от 19.04.2022 №68 p.431 table 16 item 6.13.1 | CONFIRMED_PDF_SOURCE_REF |
| 6.14 | RegistrationDossierDocDetails/SubmissionSequenceCode | csdo:Code10Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.431 table 16 item 6.14 | CONFIRMED_PDF_SOURCE_REF |
| 6.15 | RegistrationDossierDocDetails/OperationAtributeCode | csdo:Code20Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.431 table 16 item 6.15 | CONFIRMED_PDF_SOURCE_REF |
| 6.16 | RegistrationDossierDocDetails/ActiveSubstanceName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.431 table 16 item 6.16 | CONFIRMED_PDF_SOURCE_REF |
| 6.17 | RegistrationDossierDocDetails/AuxiliarySubstanceName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.431 table 16 item 6.17 | CONFIRMED_PDF_SOURCE_REF |
| 6.18 | RegistrationDossierDocDetails/DrugProductName | csdo:Name250Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.432 table 16 item 6.18 | CONFIRMED_PDF_SOURCE_REF |
| 6.19 | RegistrationDossierDocDetails/IndicationText | csdo:Text4000Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.432 table 16 item 6.19 | CONFIRMED_PDF_SOURCE_REF |
| 6.20 | RegistrationDossierDocDetails/ManufacturerName | csdo:Name300Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.432 table 16 item 6.20 | CONFIRMED_PDF_SOURCE_REF |
