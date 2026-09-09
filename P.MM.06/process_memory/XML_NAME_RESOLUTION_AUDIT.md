# P.MM.06 — explicit XML name resolution audit

Source: only `32_ОП.pdf`. `STRUCTURES_AUDIT.*` was used only as an index and was not modified. No production files were used or changed.

## Summary

| Structure | Total nodes | EXPLICIT_DIRECT | EXPLICIT_CONTEXTUAL | AMBIGUOUS | UNRESOLVED |
| --- | ---: | ---: | ---: | ---: | ---: |
| `R.HC.MM.06.001` | 116 | 0 | 1 | 3 | 112 |
| `R.HC.MM.06.002` | 19 | 0 | 1 | 0 | 18 |
| `R.HC.MM.06.003` | 25 | 0 | 1 | 1 | 23 |
| `R.HC.MM.06.004` | 9 | 0 | 2 | 0 | 7 |
| `R.HC.MM.06.005` | 17 | 1 | 1 | 0 | 15 |
| **TOTAL** | **186** | **1** | **6** | **4** | **175** |

## Resolved mappings

| Structure / row | Model ID | Normative node | QName | Evidence | Source |
| --- | --- | --- | --- | --- | --- |
| `.001 / 2.1.1` | `M.HC.SDE.00660` | Номер заявления на регистрацию или проведение иных процедур, связанных с регистрацией медицинского изделия | `hcsdo:MedicalProductApplicationId` | EXPLICIT_CONTEXTUAL: requirement names this Russian реквизит and QName; table 10 has one node with this exact normative name and model ID | PDF стр. 170, table 10; PDF стр. 117, table 16 requirements |
| `.002 / 11` | `M.HC.SDE.00302` | Документ в формате PDF | `hcsdo:PdfBinaryText` | EXPLICIT_CONTEXTUAL: the requirements name this record and QName; table 13 row 11 is that record | PDF стр. 192, table 13; PDF стр. 146–148, tables 16–18 |
| `.003 / 5.12` | `M.HC.SDE.00302` | Документ в формате PDF | `hcsdo:PdfBinaryText` | EXPLICIT_CONTEXTUAL: the requirements explicitly pair this record name and QName; table 16 row 5.12 is the same record | PDF стр. 200, table 16; PDF стр. 150–156, tables 19–23 |
| `.004 / 2` | `M.HC.SDE.00660` | Номер заявления на регистрацию или проведение иных процедур, связанных с регистрацией медицинского изделия | `hcsdo:MedicalProductApplicationId` | EXPLICIT_CONTEXTUAL | PDF стр. 203, table 19; PDF стр. 117, table 16 |
| `.004 / 3` | `M.HC.SDE.00045` | Номер регистрационного удостоверения | `hcsdo:RegistrationCertificateId` | EXPLICIT_CONTEXTUAL | PDF стр. 203, table 19; PDF стр. 117, table 16 |
| `.005 / 3` | `M.HC.SDE.00447` | Код вида медицинского изделия | `hcsdo:MedicalProductClassificationCode` | EXPLICIT_CONTEXTUAL | PDF стр. 206, table 22; PDF стр. 156–157, tables 24–25 |
| `.005 / 4` | `M.HC.SDE.00448` | Наименование вида медицинского изделия | `hcsdo:MedicalProductClassificationName` | EXPLICIT_DIRECT: PDF directly places the Russian record name and QName together in the requirement and table 22 has one matching node | PDF стр. 207, table 22; PDF стр. 157, table 24 |

## Ambiguous mappings

| Structure | QName | Reason |
| --- | --- | --- |
| `.001` | `csdo:UnifiedCountryCode` | Explicitly named many times in requirements, but table 10 contains multiple country-code structural nodes; a single row cannot be selected without guessing. |
| `.001` | `csdo:StartDateTime` | Requirements name the QName, but table 10 contains time-related nodes and the evidence does not identify a unique structural row. |
| `.001` | `csdo:EndDateTime` | Same issue; relative `*.n` numbering also prevents an absolute row assignment. |
| `.003` | `hccdo:MedicalProductRegistrationFileDetails` | Explicitly named in requirements, but the requirement context does not identify one unique table-16 row with sufficient certainty. |

## Attributes

| Attribute | Owner | Status | Evidence |
| --- | --- | --- | --- |
| `code` | `.005`, row 3 | EXPLICIT_DIRECT | Table 22 explicitly labels it «атрибут code» under row 3 (PDF стр. 207). |
| `codeListId` | UNRESOLVED | UNRESOLVED | Requirements mention the attribute, but do not use an unambiguous `owner QName/@codeListId` form for a table-10 structural row. |
| `codeListVersionId` | UNRESOLVED | UNRESOLVED | No unambiguous owner mapping found. |
| `media` | UNRESOLVED | UNRESOLVED | Table material mentions «атрибут media», but its owner cannot be bound to a QName without guessing. |

## Integrity

- No resolved structural node has two QName values.
- No QName is assigned to two sibling nodes in one structure.
- Every resolved QName prefix agrees with the normative node's prefix.
- No mapping was inferred from Russian name alone, model-ID similarity, production code or external XSD.
- Conflicts: none.
