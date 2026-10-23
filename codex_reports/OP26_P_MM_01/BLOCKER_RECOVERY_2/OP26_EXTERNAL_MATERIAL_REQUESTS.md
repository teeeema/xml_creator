# OP26 External Material Requests Manifest

**Process:** P.MM.01 (OP26) — «Формирование, ведение и использование единого реестра зарегистрированных лекарственных средств Евразийского экономического союза»  
**Regulatory Base:** Decision of the EEC Board dated April 19, 2022 No. 68  
**Purpose:** Formal specification of external missing authoritative materials required to achieve 100% normative closure and unblock the 35 remaining requirements.

---

## Group 1: Official XML Schema Release Bundle (XSD)
- **Priority:** P0 (Critical Blocker for Closure-Grade Validation)
- **Target Items:** All 8 OP26 message structures and imported data models:
  1. `EEC_R_ProcessingResultDetails_vY.Y.Y.xsd` (R.006)
  2. `EEC_R_ResourceStatusDetails_vY.Y.Y.xsd` (R.007)
  3. `EEC_R_HC_MM_01_DrugRegistrationDetails_v1.1.0.xsd` (R.HC.MM.01.001)
  4. `EEC_R_HC_MM_01_DrugRegistrationExpertReportDetails_v1.1.0.xsd` (R.HC.MM.01.002)
  5. `EEC_R_HC_MM_01_DrugRegistrationDocContentDetails_v1.1.0.xsd` (R.HC.MM.01.003)
  6. `EEC_R_HC_MM_01_DrugRegistrationNumberRequestDetails_v1.1.0.xsd` (R.HC.MM.01.004)
  7. `EEC_R_HC_MM_01_DrugApprovalApplicationDetails_v1.1.0.xsd` (R.HC.MM.01.006)
  8. `EEC_R_HC_MM_01_DrugRegistrationStatusDetails_v1.0.0.xsd` (R.HC.MM.01.007)
  9. Complete set of imported XSD modules for Base Data Model (`urn:EEC:M:ComplexDataObjects:vX.X.X`, `urn:EEC:M:SimpleDataObjects:vX.X.X`) and Healthcare Data Model (`urn:EEC:M:HC:ComplexDataObjects:vX.X.X`, `urn:EEC:M:HC:SimpleDataObjects:vX.X.X`).
- **Required Details:** Concrete version numbers replacing placeholders `vX.X.X` and `vY.Y.Y`, authoritative namespace bindings, Clark QName closure.

---

## Group 2: Official Machine-Readable Classifier Datasets
- **Priority:** P1 (Blocks 14 Canonical Requirements)
- **Target Materials:**
  1. **P.CLS.019 (World Countries Classifier):**
     - Official machine-readable dataset (XML/JSON/CSV) of country codes conforming to the EEC-approved release of ISO 3166-1 alpha-2.
     - Release version, effective date, and lifecycle status of historical/reserved codes.
     - *Blocks:* 11 membership rules (`MSG.001.REQ.035`, `MSG.002.REQ.007`, `MSG.003.REQ.009`, `MSG.007.REQ.004`, `MSG.010.REQ.003`, `MSG.016.REQ.002`, `MSG.019.REQ.005`, `MSG.020.REQ.005`, `MSG.021.REQ.010`, `MSG.023.REQ.008`, `MSG.024.REQ.005`).
  2. **Drug Registration Document Kind Classifier (`hcsdo:DrugRegistrationDocCodeType`):**
     - Official code assignment corresponding to the semantic value 'другое' (other).
     - *Blocks:* 3 conditional rules (`MSG.001.REQ.046`, `MSG.002.REQ.050`, `MSG.020.REQ.011`).

---

## Group 3: External Unified Registry Integration Contract
- **Priority:** P1 (Blocks 11 Canonical Requirements)
- **Target Materials:**
  1. Technical integration specification, WSDL/OpenAPI contract, or database snapshot schema for performing lookups against the EAEU unified drug register.
  2. Query semantics for:
     - Uniqueness checks for active records by `ApplicationId` + `UnifiedCountryCode` with empty `EndDateTime` (`MSG.001.REQ.011`).
     - State verification of registration certificates (`MSG.001.REQ.014`, `MSG.001.REQ.015`, `MSG.028.REQ.005#B`).
     - Verification of prior record versions and historical `StartDateTime` comparisons (`MSG.002.REQ.009`, `MSG.003.REQ.007`).
     - Multi-document attachment presence verification across 5 document groups (`MSG.002.REQ.087`).
     - Stage code verification (`ApplicationStatusCode == 06`) and reference member state verification (`MSG.014.REQ.003`).
     - Query existence verification (`MSG.025.REQ.003`, `MSG.027.REQ.008`).

---

## Group 4: Official Normative Clarifications & Corrigenda
- **Priority:** P1 (Blocks 10 Canonical Requirements)
- **Target Clarifications:**
  1. **Table 19, Item 22 (`MSG.002.REQ.022`):** Official resolution regarding `hcsdo:ChildJuvenileIndicator` vs separate `ChildIndicator` / `JuvenileIndicator`.
  2. **Table 19, Item 13 (`MSG.002.REQ.013`):** Official clarification regarding the word 'только' excluding mandatory elements `UnifiedCountryCode` and `CountryKindCode`.
  3. **Table 19, Item 61 (`MSG.002.REQ.061`):** Official corrigendum confirming whether `ccdo:SubjectAddressDetails` should be read as `ccdo:AddressV4Details`.
  4. **Table 19, Item 84 (`MSG.002.REQ.084`):** Complete normative text of the truncated rule ending in '...обязательны для заполнения и'.
  5. **Table 19, Item 86 (`MSG.002.REQ.086`):** Clarification on placement of `DrugSecondaryPackageKindCode`/`Name` (`PackageDetails` vs `PackageFormDetails`).
  6. **Table 22, Item 2 (`MSG.014.REQ.002`):** Clarification regarding `ApplicationStatusCode` absent from structure `R.HC.MM.01.004`.
  7. **Table 21, Items 4–5 (`MSG.023.REQ.004`, `MSG.023.REQ.005`) & Table 22, Items 6–7 (`MSG.024.REQ.006`, `MSG.024.REQ.007`):** Official corrigendum regarding references to `DrugAttributeEnumText` and `AttributeKindCode`/`Name` absent from `R.HC.MM.01.002`.
