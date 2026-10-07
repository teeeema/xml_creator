---
layer: "KNOWLEDGE"
structure_id: "R.IP.SP.02.008"
generated_by: "knowledge_base/tools/build_kb.py"
---


# R.IP.SP.02.008 Fields

| ID | Path | Datatype | Cardinality | Source | Evidence |
|---|---|---|---|---|---|
| 1 | ccdo:EDocHeader | ccdo:EDocHeaderType | 1..1 | ОП_22.pdf p.987 table 16 item 1 | CONFIRMED_PDF_SOURCE_REF |
| 1.1 | ccdo:EDocHeader/csdo:InfEnvelopeCode | csdo:InfEnvelopeCodeType | 1..1 | ОП_22.pdf p.987 table 16 item 1.1 | CONFIRMED_PDF_SOURCE_REF |
| 1.2 | ccdo:EDocHeader/csdo:EDocCode | csdo:EDocCodeType | 1..1 | ОП_22.pdf p.987 table 16 item 1.2 | CONFIRMED_PDF_SOURCE_REF |
| 1.3 | ccdo:EDocHeader/csdo:EDocId | csdo:UniversallyUniqueIdType | 1..1 | ОП_22.pdf p.988 table 16 item 1.3 | CONFIRMED_PDF_SOURCE_REF |
| 1.4 | ccdo:EDocHeader/csdo:EDocRefId | csdo:UniversallyUniqueIdType | 0..1 | ОП_22.pdf p.988 table 16 item 1.4 | CONFIRMED_PDF_SOURCE_REF |
| 1.5 | ccdo:EDocHeader/csdo:EDocDateTime | bdt:DateTimeType | 1..1 | ОП_22.pdf p.988 table 16 item 1.5 | CONFIRMED_PDF_SOURCE_REF |
| 1.6 | ccdo:EDocHeader/csdo:LanguageCode | csdo:LanguageCodeType | 0..1 | ОП_22.pdf p.988 table 16 item 1.6 | CONFIRMED_PDF_SOURCE_REF |
| 2 | csdo:UpdateDateTime | bdt:DateTimeType | 0..1 | ОП_22.pdf p.988 table 16 item 2 | CONFIRMED_PDF_SOURCE_REF |
| 3 | csdo:UnifiedCountryCode | csdo:UnifiedCountryCodeType | 0..* | ОП_22.pdf p.989 table 16 item 3 | CONFIRMED_PDF_SOURCE_REF |
| 3.a | csdo:UnifiedCountryCode/@codeListId | csdo:ReferenceDataIdType | 1..1 | ОП_22.pdf p.989 table 16 item 3.a | CONFIRMED_PDF_SOURCE_REF |
| 4 | ipsdo:TrademarkId | ipsdo:TrademarkCertificateIdType | 0..1 | ОП_22.pdf p.989 table 16 item 4 | CONFIRMED_PDF_SOURCE_REF |
| 5 | ipsdo:TrademarkApplicationId | ipsdo:ApplicationIdType | 0..1 | ОП_22.pdf p.989 table 16 item 5 | CONFIRMED_PDF_SOURCE_REF |
| 6 | ipcdo:AccompanyingDocumentsDetails | ipcdo:IPDocDetailsType | 0..1 | ОП_22.pdf p.990 table 16 item 6 | CONFIRMED_PDF_SOURCE_REF |
| 6.1 | ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindCode | ipsdo:IPDocKindCodeType | 0..1 | ОП_22.pdf p.990 table 16 item 6.1 | CONFIRMED_PDF_SOURCE_REF |
| 6.2 | ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindName | csdo:Name500Type | 0..1 | ОП_22.pdf p.990 table 16 item 6.2 | CONFIRMED_PDF_SOURCE_REF |
| 6.3 | ipcdo:AccompanyingDocumentsDetails/csdo:DocName | csdo:Name500Type | 0..1 | ОП_22.pdf p.990 table 16 item 6.3 | CONFIRMED_PDF_SOURCE_REF |
| 6.4 | ipcdo:AccompanyingDocumentsDetails/csdo:DocId | csdo:Id50Type | 0..1 | ОП_22.pdf p.991 table 16 item 6.4 | CONFIRMED_PDF_SOURCE_REF |
| 6.5 | ipcdo:AccompanyingDocumentsDetails/csdo:DocCreationDate | bdt:DateType | 0..1 | ОП_22.pdf p.991 table 16 item 6.5 | CONFIRMED_PDF_SOURCE_REF |
| 6.6 | ipcdo:AccompanyingDocumentsDetails/csdo:DocValidityDate | bdt:DateType | 0..1 | ОП_22.pdf p.991 table 16 item 6.6 | CONFIRMED_PDF_SOURCE_REF |
| 6.7 | ipcdo:AccompanyingDocumentsDetails/csdo:DescriptionText | csdo:Text4000Type | 0..1 | ОП_22.pdf p.991 table 16 item 6.7 | CONFIRMED_PDF_SOURCE_REF |
| 6.8 | ipcdo:AccompanyingDocumentsDetails/csdo:PageQuantity | csdo:Quantity4Type | 0..1 | ОП_22.pdf p.991 table 16 item 6.8 | CONFIRMED_PDF_SOURCE_REF |
| 6.9 | ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText | csdo:BinaryTextType | 0..1 | ОП_22.pdf p.991 table 16 item 6.9 | CONFIRMED_PDF_SOURCE_REF |
| 6.9.a | ipcdo:AccompanyingDocumentsDetails/csdo:DocBinaryText/@mediaTypeCode | csdo:MediaTypeCodeType | 0..1 | ОП_22.pdf p.992 table 16 item 6.9.a | CONFIRMED_PDF_SOURCE_REF |
