---
layer: "KNOWLEDGE"
structure_id: "R.FP.DS.01.003"
generated_by: "knowledge_base/tools/build_kb.py"
---


# R.FP.DS.01.003 Fields

| ID | Path | Datatype | Cardinality | Source | Evidence |
|---|---|---|---|---|---|
| 1 | VerificationProtocol/ccdo:EDocHeader | ccdo:EDocHeaderType | 1..1 | 49 ОП.pdf p.190 table 10 item 1 | CONFIRMED_PDF_SOURCE_REF |
| 1.1 | VerificationProtocol/ccdo:EDocHeader/csdo:InfEnvelopeCode | csdo:InfEnvelopeCodeType | 1..1 | 49 ОП.pdf p.190 table 10 item 1.1 | CONFIRMED_PDF_SOURCE_REF |
| 1.2 | VerificationProtocol/ccdo:EDocHeader/csdo:EDocCode | csdo:EDocCodeType | 1..1 | 49 ОП.pdf p.190 table 10 item 1.2 | CONFIRMED_PDF_SOURCE_REF |
| 1.3 | VerificationProtocol/ccdo:EDocHeader/csdo:EDocId | csdo:UniversallyUniqueIdType | 1..1 | 49 ОП.pdf p.190 table 10 item 1.3 | CONFIRMED_PDF_SOURCE_REF |
| 1.4 | VerificationProtocol/ccdo:EDocHeader/csdo:EDocRefId | csdo:UniversallyUniqueIdType | 0..1 | 49 ОП.pdf p.190 table 10 item 1.4 | CONFIRMED_PDF_SOURCE_REF |
| 1.5 | VerificationProtocol/ccdo:EDocHeader/csdo:EDocDateTime | bdt:DateTimeType | 1..1 | 49 ОП.pdf p.190 table 10 item 1.5 | CONFIRMED_PDF_SOURCE_REF |
| 1.6 | VerificationProtocol/ccdo:EDocHeader/csdo:LanguageCode | csdo:LanguageCodeType | 0..1 | 49 ОП.pdf p.190 table 10 item 1.6 | CONFIRMED_PDF_SOURCE_REF |
| 2 | VerificationProtocol/ds01sdo:ReportCountryCode | csdo:UnifiedCountryCodeType | 1..1 | 49 ОП.pdf p.190 table 10 item 2 | CONFIRMED_PDF_SOURCE_REF |
| 2.@codeListId | VerificationProtocol/ds01sdo:ReportCountryCode/codeListId | csdo:ReferenceDataIdType | 1..1 | 49 ОП.pdf p.190 table 10 item 2.@codeListId | CONFIRMED_PDF_SOURCE_REF |
| 3 | VerificationProtocol/ds01sdo:ReportDate | bdt:DateType | 1..1 | 49 ОП.pdf p.190 table 10 item 3 | CONFIRMED_PDF_SOURCE_REF |
| 4 | VerificationProtocol/csdo:EventDate | bdt:DateType | 1..1 | 49 ОП.pdf p.190 table 10 item 4 | CONFIRMED_PDF_SOURCE_REF |
| 5 | VerificationProtocol/ds01cdo:DifferencesDetails | ds01cdo:DifferencesDetailsType | 0..None | 49 ОП.pdf p.190 table 10 item 5 | CONFIRMED_PDF_SOURCE_REF |
| 5.1 | VerificationProtocol/ds01cdo:DifferencesDetails/ds01sdo:GraphDifferenceText | csdo:Text250Type | 1..1 | 49 ОП.pdf p.190 table 10 item 5.1 | CONFIRMED_PDF_SOURCE_REF |
| 5.2 | VerificationProtocol/ds01cdo:DifferencesDetails/ds01sdo:DescriptionDifferenceText | csdo:Text250Type | 1..1 | 49 ОП.pdf p.190 table 10 item 5.2 | CONFIRMED_PDF_SOURCE_REF |
| 5.3 | VerificationProtocol/ds01cdo:DifferencesDetails/ds01sdo:ExpectedValueText | csdo:Text250Type | 0..1 | 49 ОП.pdf p.190 table 10 item 5.3 | CONFIRMED_PDF_SOURCE_REF |
