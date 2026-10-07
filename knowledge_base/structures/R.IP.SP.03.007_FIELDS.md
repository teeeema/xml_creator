---
layer: "KNOWLEDGE"
structure_id: "R.IP.SP.03.007"
generated_by: "knowledge_base/tools/build_kb.py"
---


# R.IP.SP.03.007 Fields

| ID | Path | Datatype | Cardinality | Source | Evidence |
|---|---|---|---|---|---|
| 1 | ccdo:EDocHeader | ccdo:EDocHeaderType | 1..1 | ОП_23.pdf p.570 table 16 item 1 | CONFIRMED_PDF_SOURCE_REF |
| 1.1 | ccdo:EDocHeader/csdo:InfEnvelopeCode | csdo:InfEnvelopeCodeType | 1..1 | ОП_23.pdf p.570 table 16 item 1.1 | CONFIRMED_PDF_SOURCE_REF |
| 1.2 | ccdo:EDocHeader/csdo:EDocCode | csdo:EDocCodeType | 1..1 | ОП_23.pdf p.570 table 16 item 1.2 | CONFIRMED_PDF_SOURCE_REF |
| 1.3 | ccdo:EDocHeader/csdo:EDocId | csdo:UniversallyUniqueIdType | 1..1 | ОП_23.pdf p.571 table 16 item 1.3 | CONFIRMED_PDF_SOURCE_REF |
| 1.4 | ccdo:EDocHeader/csdo:EDocRefId | csdo:UniversallyUniqueIdType | 0..1 | ОП_23.pdf p.571 table 16 item 1.4 | CONFIRMED_PDF_SOURCE_REF |
| 1.5 | ccdo:EDocHeader/csdo:EDocDateTime | bdt:DateTimeType | 1..1 | ОП_23.pdf p.571 table 16 item 1.5 | CONFIRMED_PDF_SOURCE_REF |
| 1.6 | ccdo:EDocHeader/csdo:LanguageCode | csdo:LanguageCodeType | 0..1 | ОП_23.pdf p.571 table 16 item 1.6 | CONFIRMED_PDF_SOURCE_REF |
| 2 | csdo:UpdateDateTime | bdt:DateTimeType | 0..1 | ОП_23.pdf p.571 table 16 item 2 | CONFIRMED_PDF_SOURCE_REF |
| 3 | csdo:UnifiedCountryCode | csdo:UnifiedCountryCodeType | 0..None | ОП_23.pdf p.572 table 16 item 3 | CONFIRMED_PDF_SOURCE_REF |
| 3@codeListId | csdo:UnifiedCountryCode/@codeListId | csdo:ReferenceDataIdType | 1..1 | ОП_23.pdf p.572 table 16 item 3@codeListId | CONFIRMED_PDF_SOURCE_REF |
| 4 | ipsdo:ApellationOfOriginEAEUId | ipsdo:ApellationOfOriginEAEUIdType | 0..1 | ОП_23.pdf p.572 table 16 item 4 | CONFIRMED_PDF_SOURCE_REF |
| 5 | ipsdo:ApellationOfOriginEAEUCertificateId | ipsdo:ApellationOfOriginEAEUCertificateIdType | 0..1 | ОП_23.pdf p.572 table 16 item 5 | CONFIRMED_PDF_SOURCE_REF |
| 6 | ipsdo:ApellationOfOriginApplicationId | ipsdo:ApplicationIdType | 0..1 | ОП_23.pdf p.573 table 16 item 6 | CONFIRMED_PDF_SOURCE_REF |
| 7 | ipcdo:AccompanyingDocumentsDetails | ipcdo:IPDocDetailsType | 0..1 | ОП_23.pdf p.573 table 16 item 7 | CONFIRMED_PDF_SOURCE_REF |
| 7.1 | ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindCode | ipsdo:IPDocKindCodeType | 0..1 | ОП_23.pdf p.573 table 16 item 7.1 | CONFIRMED_PDF_SOURCE_REF |
| 7.2 | ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindName | csdo:Name500Type | 0..1 | ОП_23.pdf p.574 table 16 item 7.2 | CONFIRMED_PDF_SOURCE_REF |
| 7.3 | ipcdo:AccompanyingDocumentsDetails/csdo:DocName | csdo:Name500Type | 0..1 | ОП_23.pdf p.574 table 16 item 7.3 | CONFIRMED_PDF_SOURCE_REF |
| 7.4 | ipcdo:AccompanyingDocumentsDetails/csdo:DocId | csdo:Id50Type | 0..1 | ОП_23.pdf p.574 table 16 item 7.4 | CONFIRMED_PDF_SOURCE_REF |
| 7.5 | ipcdo:AccompanyingDocumentsDetails/csdo:DocCreationDate | bdt:DateType | 0..1 | ОП_23.pdf p.574 table 16 item 7.5 | CONFIRMED_PDF_SOURCE_REF |
| 7.6 | ipcdo:AccompanyingDocumentsDetails/csdo:DocValidityDate | bdt:DateType | 0..1 | ОП_23.pdf p.574 table 16 item 7.6 | CONFIRMED_PDF_SOURCE_REF |
