# P.MM.06.MSG.012 requirements audit

- Structure: `R.HC.MM.06.004`
- Status: `TABLE_FOUND`
- Table: `16`
- Raw / structured: **2 / 2**
- Count integrity: **PASS**

## Requirement 1

реквизит "Номер регистрационного удостоверения" (hcsdo:RegistrationCertificateId) не заполняется

- Source: table 16, PDF page(s) 117–117
- Semantic category: `PROHIBITED`
- Literal field references: `hcsdo:RegistrationCertificateId`
- Mapping: `RESOLVED`

## Requirement 2

в сведениях о регистрации медицинских изделий, хранящихся в Комиссии, должны содержаться сведения с таким же значением реквизита "Номер заявления на регистрацию медицинского изделия" (hcsdo:MedicalProductApplicationId)

- Source: table 16, PDF page(s) 117–117
- Semantic category: `CONSTRAINT`
- Literal field references: `hcsdo:MedicalProductApplicationId`
- Mapping: `RESOLVED`
