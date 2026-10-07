---
layer: "KNOWLEDGE"
structure_id: "R.HC.MM.01.002"
generated_by: "knowledge_base/tools/build_kb.py"
---


# R.HC.MM.01.002 Fields

| ID | Path | Datatype | Cardinality | Source | Evidence |
|---|---|---|---|---|---|
| 1 | EDocHeader | ccdo:EDocHeaderType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.415 table 13 item 1 | CONFIRMED_PDF_SOURCE_REF |
| 1.1 | EDocHeader/InfEnvelopeCode | csdo:InfEnvelopeCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.415 table 13 item 1.1 | CONFIRMED_PDF_SOURCE_REF |
| 1.2 | EDocHeader/EDocCode | csdo:EDocCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.415 table 13 item 1.2 | CONFIRMED_PDF_SOURCE_REF |
| 1.3 | EDocHeader/EDocId | csdo:UniversallyUniqueIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.416 table 13 item 1.3 | CONFIRMED_PDF_SOURCE_REF |
| 1.4 | EDocHeader/EDocRefId | csdo:UniversallyUniqueIdType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.416 table 13 item 1.4 | CONFIRMED_PDF_SOURCE_REF |
| 1.5 | EDocHeader/EDocDateTime | bdt:DateTimeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.416 table 13 item 1.5 | CONFIRMED_PDF_SOURCE_REF |
| 1.6 | EDocHeader/LanguageCode | csdo:LanguageCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.416 table 13 item 1.6 | CONFIRMED_PDF_SOURCE_REF |
| 2 | UnifiedCountryCode | csdo:UnifiedCountryCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.416 table 13 item 2 | CONFIRMED_PDF_SOURCE_REF |
| 2.а | UnifiedCountryCode/@codeListId | csdo:ReferenceDataIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.417 table 13 item 2.а | CONFIRMED_PDF_SOURCE_REF |
| 3 | ApplicationId | csdo:Id50Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.417 table 13 item 3 | CONFIRMED_PDF_SOURCE_REF |
| 4 | RegistrationNumberId | hcsdo:RegistrationNumberIdType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.417 table 13 item 4 | CONFIRMED_PDF_SOURCE_REF |
| 5 | DocId | csdo:Id50Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.417 table 13 item 5 | CONFIRMED_PDF_SOURCE_REF |
| 6 | DocName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.418 table 13 item 6 | CONFIRMED_PDF_SOURCE_REF |
| 7 | DrugRegistrationFileCode | hcsdo:DrugRegistrationFileCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.418 table 13 item 7 | CONFIRMED_PDF_SOURCE_REF |
| 7.а | DrugRegistrationFileCode/@codeListId | csdo:ReferenceDataIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.418 table 13 item 7.а | CONFIRMED_PDF_SOURCE_REF |
| 8 | DrugRegistrationFileName | csdo:Name500Type | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.418 table 13 item 8 | CONFIRMED_PDF_SOURCE_REF |
| 9 | DocCreationDate | bdt:DateType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.419 table 13 item 9 | CONFIRMED_PDF_SOURCE_REF |
| 10 | DocAgreementIndicator | bdt:IndicatorType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.419 table 13 item 10 | CONFIRMED_PDF_SOURCE_REF |
| 11 | AuthorityDrugConditionalRegistrationIndicator | bdt:IndicatorType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.419 table 13 item 11 | CONFIRMED_PDF_SOURCE_REF |
| 12 | PdfBinaryText | csdo:BinaryTextType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.420 table 13 item 12 | CONFIRMED_PDF_SOURCE_REF |
| 12.а | PdfBinaryText/@mediaTypeCode | csdo:MediaTypeCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.420 table 13 item 12.а | CONFIRMED_PDF_SOURCE_REF |
| 13 | AnyDetails | ccdo:AnyDetailsType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.420 table 13 item 13 | CONFIRMED_PDF_SOURCE_REF |
| 13.1 | AnyDetails/* | ANY_XML | 1..None | Решение Коллегии ЕЭК от 19.04.2022 №68 p.421 table 13 item 13.1 | CONFIRMED_PDF_SOURCE_REF |
