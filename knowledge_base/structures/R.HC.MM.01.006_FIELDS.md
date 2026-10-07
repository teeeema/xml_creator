---
layer: "KNOWLEDGE"
structure_id: "R.HC.MM.01.006"
generated_by: "knowledge_base/tools/build_kb.py"
---


# R.HC.MM.01.006 Fields

| ID | Path | Datatype | Cardinality | Source | Evidence |
|---|---|---|---|---|---|
| 1 | EDocHeader | ccdo:EDocHeaderType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.440 table 22 item 1 | CONFIRMED_PDF_SOURCE_REF |
| 1.1 | EDocHeader/InfEnvelopeCode | csdo:InfEnvelopeCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.440 table 22 item 1.1 | CONFIRMED_PDF_SOURCE_REF |
| 1.2 | EDocHeader/EDocCode | csdo:EDocCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.440 table 22 item 1.2 | CONFIRMED_PDF_SOURCE_REF |
| 1.3 | EDocHeader/EDocId | csdo:UniversallyUniqueIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.441 table 22 item 1.3 | CONFIRMED_PDF_SOURCE_REF |
| 1.4 | EDocHeader/EDocRefId | csdo:UniversallyUniqueIdType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.441 table 22 item 1.4 | CONFIRMED_PDF_SOURCE_REF |
| 1.5 | EDocHeader/EDocDateTime | bdt:DateTimeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.441 table 22 item 1.5 | CONFIRMED_PDF_SOURCE_REF |
| 1.6 | EDocHeader/LanguageCode | csdo:LanguageCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.441 table 22 item 1.6 | CONFIRMED_PDF_SOURCE_REF |
| 2 | ApplicationId | csdo:Id50Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.442 table 22 item 2 | CONFIRMED_PDF_SOURCE_REF |
| 3 | RegistrationNumberId | hcsdo:RegistrationNumberIdType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.442 table 22 item 3 | CONFIRMED_PDF_SOURCE_REF |
| 4 | CountryDrugRegistrationDetails | hccdo:CountryDrugRegistrationDetails | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.442 table 22 item 4 | CONFIRMED_PDF_SOURCE_REF |
| 4.1 | CountryDrugRegistrationDetails/UnifiedCountryCode | csdo:UnifiedCountryCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.442 table 22 item 4.1 | CONFIRMED_PDF_SOURCE_REF |
| 4.1.а | CountryDrugRegistrationDetails/UnifiedCountryCode/@codeListId | csdo:ReferenceDataIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.443 table 22 item 4.1.а | CONFIRMED_PDF_SOURCE_REF |
| 4.2 | CountryDrugRegistrationDetails/CountryKindCode | hcsdo:CountryKindCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.443 table 22 item 4.2 | CONFIRMED_PDF_SOURCE_REF |
| 5 | ApprovalImpossibilityReasonCode | csdo:Code2Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.443 table 22 item 5 | CONFIRMED_PDF_SOURCE_REF |
| 6 | NoteText | csdo:Text4000Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.443 table 22 item 6 | CONFIRMED_PDF_SOURCE_REF |
| 7 | RegistrationDossierDocDetails | hccdo:RegistrationDossierDocDetails | 0..None | Решение Коллегии ЕЭК от 19.04.2022 №68 p.444 table 22 item 7 | CONFIRMED_PDF_SOURCE_REF |
| 7.1 | RegistrationDossierDocDetails/RegistrationFileIndicator | bdt:IndicatorType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.444 table 22 item 7.1 | CONFIRMED_PDF_SOURCE_REF |
| 7.2 | RegistrationDossierDocDetails/DocId | csdo:Id50Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.444 table 22 item 7.2 | CONFIRMED_PDF_SOURCE_REF |
| 7.3 | RegistrationDossierDocDetails/DocName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.444 table 22 item 7.3 | CONFIRMED_PDF_SOURCE_REF |
| 7.4 | RegistrationDossierDocDetails/DrugRegistrationDocCode | hcsdo:DrugRegistrationDocCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.445 table 22 item 7.4 | CONFIRMED_PDF_SOURCE_REF |
| 7.4.а | RegistrationDossierDocDetails/DrugRegistrationDocCode/@codeListId | csdo:ReferenceDataIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.445 table 22 item 7.4.а | CONFIRMED_PDF_SOURCE_REF |
| 7.5 | RegistrationDossierDocDetails/DrugRegistrationDocName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.445 table 22 item 7.5 | CONFIRMED_PDF_SOURCE_REF |
| 7.6 | RegistrationDossierDocDetails/DrugRegistrationFileCode | hcsdo:DrugRegistrationFileCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.446 table 22 item 7.6 | CONFIRMED_PDF_SOURCE_REF |
| 7.6.а | RegistrationDossierDocDetails/DrugRegistrationFileCode/@codeListId | csdo:ReferenceDataIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.446 table 22 item 7.6.а | CONFIRMED_PDF_SOURCE_REF |
| 7.7 | RegistrationDossierDocDetails/DrugRegistrationFileName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.446 table 22 item 7.7 | CONFIRMED_PDF_SOURCE_REF |
| 7.8 | RegistrationDossierDocDetails/DocCreationDate | bdt:DateType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.446 table 22 item 7.8 | CONFIRMED_PDF_SOURCE_REF |
| 7.9 | RegistrationDossierDocDetails/DocValidityDate | bdt:DateType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.446 table 22 item 7.9 | CONFIRMED_PDF_SOURCE_REF |
| 7.10 | RegistrationDossierDocDetails/BusinessEntityName | csdo:Name300Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.447 table 22 item 7.10 | CONFIRMED_PDF_SOURCE_REF |
| 7.11 | RegistrationDossierDocDetails/DrugAttributeEnumText | hcsdo:AttributeTextType | 0..None | Решение Коллегии ЕЭК от 19.04.2022 №68 p.447 table 22 item 7.11 | CONFIRMED_PDF_SOURCE_REF |
| 7.11.а | RegistrationDossierDocDetails/DrugAttributeEnumText/@DrugAttributeKindEnumCode | csdo:Code10Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.447 table 22 item 7.11.а | CONFIRMED_PDF_SOURCE_REF |
| 7.11.б | RegistrationDossierDocDetails/DrugAttributeEnumText/@AttributeKindName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.447 table 22 item 7.11.б | CONFIRMED_PDF_SOURCE_REF |
| 7.12 | RegistrationDossierDocDetails/DocCopyBinaryText | csdo:BinaryTextType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.447 table 22 item 7.12 | CONFIRMED_PDF_SOURCE_REF |
| 7.12.а | RegistrationDossierDocDetails/DocCopyBinaryText/@mediaTypeCode | csdo:MediaTypeCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.448 table 22 item 7.12.а | CONFIRMED_PDF_SOURCE_REF |
| 7.13 | RegistrationDossierDocDetails/AnyDetails | ccdo:AnyDetailsType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.448 table 22 item 7.13 | CONFIRMED_PDF_SOURCE_REF |
| 7.13.1 | RegistrationDossierDocDetails/AnyDetails/* | ANY_XML | 1..None | Решение Коллегии ЕЭК от 19.04.2022 №68 p.448 table 22 item 7.13.1 | CONFIRMED_PDF_SOURCE_REF |
| 7.14 | RegistrationDossierDocDetails/SubmissionSequenceCode | csdo:Code10Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.448 table 22 item 7.14 | CONFIRMED_PDF_SOURCE_REF |
| 7.15 | RegistrationDossierDocDetails/OperationAtributeCode | csdo:Code20Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.448 table 22 item 7.15 | CONFIRMED_PDF_SOURCE_REF |
| 7.16 | RegistrationDossierDocDetails/ActiveSubstanceName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.448 table 22 item 7.16 | CONFIRMED_PDF_SOURCE_REF |
| 7.17 | RegistrationDossierDocDetails/AuxiliarySubstanceName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.449 table 22 item 7.17 | CONFIRMED_PDF_SOURCE_REF |
| 7.18 | RegistrationDossierDocDetails/DrugProductName | csdo:Name250Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.449 table 22 item 7.18 | CONFIRMED_PDF_SOURCE_REF |
| 7.19 | RegistrationDossierDocDetails/IndicationText | csdo:Text4000Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.449 table 22 item 7.19 | CONFIRMED_PDF_SOURCE_REF |
| 7.20 | RegistrationDossierDocDetails/ManufacturerName | csdo:Name300Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.449 table 22 item 7.20 | CONFIRMED_PDF_SOURCE_REF |
