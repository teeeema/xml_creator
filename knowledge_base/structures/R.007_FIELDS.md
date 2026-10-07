---
layer: "KNOWLEDGE"
structure_id: "R.007"
generated_by: "knowledge_base/tools/build_kb.py"
---


# R.007 Fields

| ID | Path | Datatype | Cardinality | Source | Evidence |
|---|---|---|---|---|---|
| 1 | EDocHeader | ccdo:EDocHeaderType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.316 table 7 item 1 | CONFIRMED_PDF_SOURCE_REF |
| 1.1 | EDocHeader/InfEnvelopeCode | csdo:InfEnvelopeCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.316 table 7 item 1.1 | CONFIRMED_PDF_SOURCE_REF |
| 1.2 | EDocHeader/EDocCode | csdo:EDocCodeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.316 table 7 item 1.2 | CONFIRMED_PDF_SOURCE_REF |
| 1.3 | EDocHeader/EDocId | csdo:UniversallyUniqueIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.317 table 7 item 1.3 | CONFIRMED_PDF_SOURCE_REF |
| 1.4 | EDocHeader/EDocRefId | csdo:UniversallyUniqueIdType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.317 table 7 item 1.4 | CONFIRMED_PDF_SOURCE_REF |
| 1.5 | EDocHeader/EDocDateTime | bdt:DateTimeType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.317 table 7 item 1.5 | CONFIRMED_PDF_SOURCE_REF |
| 1.6 | EDocHeader/LanguageCode | csdo:LanguageCodeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.317 table 7 item 1.6 | CONFIRMED_PDF_SOURCE_REF |
| 2 | UpdateDateTime | bdt:DateTimeType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.317 table 7 item 2 | CONFIRMED_PDF_SOURCE_REF |
| 3 | UnifiedCountryCode | csdo:UnifiedCountryCodeType | 0..None | Решение Коллегии ЕЭК от 19.04.2022 №68 p.318 table 7 item 3 | CONFIRMED_PDF_SOURCE_REF |
| 3.а | UnifiedCountryCode/@codeListId | csdo:ReferenceDataIdType | 1..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.318 table 7 item 3.а | CONFIRMED_PDF_SOURCE_REF |
| 4 | InformationResourceId | csdo:InformationResourceIdType | 0..1 | Решение Коллегии ЕЭК от 19.04.2022 №68 p.318 table 7 item 4 | CONFIRMED_PDF_SOURCE_REF |
