# EXTERNAL MATERIALS REQUEST MANIFEST — OP26 / P.MM.01
Чтобы довести OP26 до нормативного closure, нужно запросить следующие материалы. Этот список основан на последнем OP26-аудите, Knowledge Base и повторной проверке локального нормативного каталога. Ничего из отсутствующего ниже не восстановлено по догадке.
## Приоритет и порядок запроса
**P0:** восемь официальных XSD с импортируемым schema set; конкретные версии R.006/R.007; конкретные base/healthcare model releases; пять официальных разрешений source conflicts; исправленный текст MSG.002/Table 19/item 84. **P1:** официальный payload P.CLS.019 и контракт единого реестра. P2/P3 отдельных внешних материалов по текущему scope не выявлено.
Практически лучше запросить одним пакетом **официальный OP26 schema release bundle**: 8 схем + все реально импортируемые XSD + release/version manifest. Если такой пакет содержит concrete R.006/R.007 и concrete base/healthcare model versions, он одновременно закрывает несколько P0-позиций.
## GROUP 1 — OFFICIAL XSD
### XSD-R006 — R.006 — P0
- **MATERIAL:** official XSD for `R.006` plus the imported schema set actually referenced by that XSD.
- **EXACT NAME if known:** `EEC_R_ProcessingResultDetails_vY.Y.Y.xsd (template declared by source; concrete filename depends on version)`.
- **CURRENT PLACEHOLDER:** version `Y.Y.Y (placeholder)`; local XSD bytes are absent.
- **SOURCE REFERENCE:** `26_ОП.pdf`, PDF 309, Table 2; imports Table 3 on PDF 309.
- **NAMESPACE stated by source:** `urn:EEC:R:ProcessingResultDetails:vY.Y.Y`.
- **DIRECT IMPORT NAMESPACES stated by source:** `ccdo=urn:EEC:M:ComplexDataObjects:vX.X.X; csdo=urn:EEC:M:SimpleDataObjects:vX.X.X`. Exact imported **schema filenames/schemaLocation values are not stated in the audited PDF** and must come from the official XSD/package.
- **WHY NEEDED:** byte-level proof of element declarations, exact imports, datatypes, cardinalities, QName binding and schema-valid XML; PDF-derived StructureDefinition alone cannot prove those.
- **REQUIREMENTS / MESSAGES UNBLOCKED:** No filling-rule records in the current 201 canonical inventory; blocks strict schema/root-QName validation for MSG.004/009/018. Messages using the structure: P.MM.01.MSG.004, P.MM.01.MSG.009, P.MM.01.MSG.018.
- **WHAT IT MUST CONTAIN:** authoritative XSD bytes, targetNamespace/root declaration, `xs:import` namespace and schemaLocation values, and all imported schemas required for offline validation.
- **WHO LIKELY OWNS IT if provable:** the normative source is an EEC act; the audited material does not prove the technical repository/owner of the XSD package. Request via the EEC/EAEU normative/integration-data owner.
- **CAN DEVELOPMENT CONTINUE WITHOUT IT?** Yes in TEST/PDF-derived mode; **normative closure and strict XSD validation cannot**.
- **TEMPORARY TECHNICAL OPTION:** current PDF-derived structure metadata and test namespaces.
- **WHY TEMPORARY OPTION IS NOT NORMATIVE:** it is not the official schema byte set and cannot prove imports/types/QNames.
- **SHARED BENEFIT:** YES — the same R.006 is used by OP22 (MSG.002/025), OP23 (MSG.002/020), and OP49 (MSG.003).
### XSD-R007 — R.007 — P0
- **MATERIAL:** official XSD for `R.007` plus the imported schema set actually referenced by that XSD.
- **EXACT NAME if known:** `EEC_R_ResourceStatusDetails_vY.Y.Y.xsd (template declared by source; concrete filename depends on version)`.
- **CURRENT PLACEHOLDER:** version `Y.Y.Y (placeholder)`; local XSD bytes are absent.
- **SOURCE REFERENCE:** `26_ОП.pdf`, PDF 314, Table 5; imports Table 6 on PDF 315.
- **NAMESPACE stated by source:** `urn:EEC:R:ResourceStatusDetails:vY.Y.Y`.
- **DIRECT IMPORT NAMESPACES stated by source:** `ccdo=urn:EEC:M:ComplexDataObjects:vX.X.X; csdo=urn:EEC:M:SimpleDataObjects:vX.X.X`. Exact imported **schema filenames/schemaLocation values are not stated in the audited PDF** and must come from the official XSD/package.
- **WHY NEEDED:** byte-level proof of element declarations, exact imports, datatypes, cardinalities, QName binding and schema-valid XML; PDF-derived StructureDefinition alone cannot prove those.
- **REQUIREMENTS / MESSAGES UNBLOCKED:** No filling-rule records in the current 201 canonical inventory; blocks strict schema/root-QName validation for MSG.005/006. Messages using the structure: P.MM.01.MSG.005, P.MM.01.MSG.006.
- **WHAT IT MUST CONTAIN:** authoritative XSD bytes, targetNamespace/root declaration, `xs:import` namespace and schemaLocation values, and all imported schemas required for offline validation.
- **WHO LIKELY OWNS IT if provable:** the normative source is an EEC act; the audited material does not prove the technical repository/owner of the XSD package. Request via the EEC/EAEU normative/integration-data owner.
- **CAN DEVELOPMENT CONTINUE WITHOUT IT?** Yes in TEST/PDF-derived mode; **normative closure and strict XSD validation cannot**.
- **TEMPORARY TECHNICAL OPTION:** current PDF-derived structure metadata and test namespaces.
- **WHY TEMPORARY OPTION IS NOT NORMATIVE:** it is not the official schema byte set and cannot prove imports/types/QNames.
- **SHARED BENEFIT:** No shared benefit proven for OP22/OP23/OP49; KB also shows use by OP32.
### XSD-RHC001 — R.HC.MM.01.001 — P0
- **MATERIAL:** official XSD for `R.HC.MM.01.001` plus the imported schema set actually referenced by that XSD.
- **EXACT NAME if known:** `EEC_R_HC_MM_01_DrugRegistrationDetails_v1.1.0.xsd`.
- **CURRENT PLACEHOLDER:** version `1.1.0`; local XSD bytes are absent.
- **SOURCE REFERENCE:** `26_ОП.pdf`, PDF 319, Table 8; imports Table 9 on PDF 319–320.
- **NAMESPACE stated by source:** `urn:EEC:R:HC:MM:01:DrugRegistrationDetails:v1.1.0`.
- **DIRECT IMPORT NAMESPACES stated by source:** `ccdo=urn:EEC:M:ComplexDataObjects:vX.X.X; hccdo=urn:EEC:M:HC:ComplexDataObjects:vX.X.X; hcsdo=urn:EEC:M:HC:SimpleDataObjects:vX.X.X; csdo=urn:EEC:M:SimpleDataObjects:vX.X.X`. Exact imported **schema filenames/schemaLocation values are not stated in the audited PDF** and must come from the official XSD/package.
- **WHY NEEDED:** byte-level proof of element declarations, exact imports, datatypes, cardinalities, QName binding and schema-valid XML; PDF-derived StructureDefinition alone cannot prove those.
- **REQUIREMENTS / MESSAGES UNBLOCKED:** 105 current canonical requirements: MSG.001 REQ.001–046; MSG.002 REQ.001–050 (REQ.050 aggregates source items 50–87); MSG.003 REQ.001–009; plus schema validation of .008/.011/.026. Messages using the structure: P.MM.01.MSG.001, .002, .003, .008, .011, .026.
- **WHAT IT MUST CONTAIN:** authoritative XSD bytes, targetNamespace/root declaration, `xs:import` namespace and schemaLocation values, and all imported schemas required for offline validation.
- **WHO LIKELY OWNS IT if provable:** the normative source is an EEC act; the audited material does not prove the technical repository/owner of the XSD package. Request via the EEC/EAEU normative/integration-data owner.
- **CAN DEVELOPMENT CONTINUE WITHOUT IT?** Yes in TEST/PDF-derived mode; **normative closure and strict XSD validation cannot**.
- **TEMPORARY TECHNICAL OPTION:** current PDF-derived structure metadata and test namespaces.
- **WHY TEMPORARY OPTION IS NOT NORMATIVE:** it is not the official schema byte set and cannot prove imports/types/QNames.
- **SHARED BENEFIT:** No shared benefit proven for OP22/OP23/OP49.
### XSD-RHC002 — R.HC.MM.01.002 — P0
- **MATERIAL:** official XSD for `R.HC.MM.01.002` plus the imported schema set actually referenced by that XSD.
- **EXACT NAME if known:** `EEC_R_HC_MM_01_DrugRegistrationExpertReportDetails_v1.1.0.xsd`.
- **CURRENT PLACEHOLDER:** version `1.1.0`; local XSD bytes are absent.
- **SOURCE REFERENCE:** `26_ОП.pdf`, PDF 413, Table 11; imports Table 12 on PDF 413–414.
- **NAMESPACE stated by source:** `urn:EEC:R:HC:MM:01:DrugRegistrationExpertReportDetails:v1.1.0`.
- **DIRECT IMPORT NAMESPACES stated by source:** `ccdo=urn:EEC:M:ComplexDataObjects:vX.X.X; hccdo=urn:EEC:M:HC:ComplexDataObjects:vX.X.X; hcsdo=urn:EEC:M:HC:SimpleDataObjects:vX.X.X; csdo=urn:EEC:M:SimpleDataObjects:vX.X.X`. Exact imported **schema filenames/schemaLocation values are not stated in the audited PDF** and must come from the official XSD/package.
- **WHY NEEDED:** byte-level proof of element declarations, exact imports, datatypes, cardinalities, QName binding and schema-valid XML; PDF-derived StructureDefinition alone cannot prove those.
- **REQUIREMENTS / MESSAGES UNBLOCKED:** 19 current canonical requirements: MSG.023 REQ.001–010; MSG.024 REQ.002–010; five of these are also source conflicts. Messages using the structure: P.MM.01.MSG.023, .024.
- **WHAT IT MUST CONTAIN:** authoritative XSD bytes, targetNamespace/root declaration, `xs:import` namespace and schemaLocation values, and all imported schemas required for offline validation.
- **WHO LIKELY OWNS IT if provable:** the normative source is an EEC act; the audited material does not prove the technical repository/owner of the XSD package. Request via the EEC/EAEU normative/integration-data owner.
- **CAN DEVELOPMENT CONTINUE WITHOUT IT?** Yes in TEST/PDF-derived mode; **normative closure and strict XSD validation cannot**.
- **TEMPORARY TECHNICAL OPTION:** current PDF-derived structure metadata and test namespaces.
- **WHY TEMPORARY OPTION IS NOT NORMATIVE:** it is not the official schema byte set and cannot prove imports/types/QNames.
- **SHARED BENEFIT:** No shared benefit proven for OP22/OP23/OP49.
### XSD-RHC003 — R.HC.MM.01.003 — P0
- **MATERIAL:** official XSD for `R.HC.MM.01.003` plus the imported schema set actually referenced by that XSD.
- **EXACT NAME if known:** `EEC_R_HC_MM_01_DrugRegistrationDocContentDetails_v1.1.0.xsd`.
- **CURRENT PLACEHOLDER:** version `1.1.0`; local XSD bytes are absent.
- **SOURCE REFERENCE:** `26_ОП.pdf`, PDF 422, Table 14; imports Table 15 on PDF 422–423.
- **NAMESPACE stated by source:** `urn:EEC:R:HC:MM:01:DrugRegistrationDocContentDetails:v1.1.0`.
- **DIRECT IMPORT NAMESPACES stated by source:** `ccdo=urn:EEC:M:ComplexDataObjects:vX.X.X; hccdo=urn:EEC:M:HC:ComplexDataObjects:vX.X.X; hcsdo=urn:EEC:M:HC:SimpleDataObjects:vX.X.X; csdo=urn:EEC:M:SimpleDataObjects:vX.X.X`. Exact imported **schema filenames/schemaLocation values are not stated in the audited PDF** and must come from the official XSD/package.
- **WHY NEEDED:** byte-level proof of element declarations, exact imports, datatypes, cardinalities, QName binding and schema-valid XML; PDF-derived StructureDefinition alone cannot prove those.
- **REQUIREMENTS / MESSAGES UNBLOCKED:** 59 current canonical requirements: MSG.012 001–005; MSG.019 001–013; MSG.020 001,003–011; MSG.021 001–016; MSG.027 001–008; MSG.028 001–007. Messages using the structure: P.MM.01.MSG.012, .019, .020, .021, .027, .028.
- **WHAT IT MUST CONTAIN:** authoritative XSD bytes, targetNamespace/root declaration, `xs:import` namespace and schemaLocation values, and all imported schemas required for offline validation.
- **WHO LIKELY OWNS IT if provable:** the normative source is an EEC act; the audited material does not prove the technical repository/owner of the XSD package. Request via the EEC/EAEU normative/integration-data owner.
- **CAN DEVELOPMENT CONTINUE WITHOUT IT?** Yes in TEST/PDF-derived mode; **normative closure and strict XSD validation cannot**.
- **TEMPORARY TECHNICAL OPTION:** current PDF-derived structure metadata and test namespaces.
- **WHY TEMPORARY OPTION IS NOT NORMATIVE:** it is not the official schema byte set and cannot prove imports/types/QNames.
- **SHARED BENEFIT:** No shared benefit proven for OP22/OP23/OP49.
### XSD-RHC004 — R.HC.MM.01.004 — P0
- **MATERIAL:** official XSD for `R.HC.MM.01.004` plus the imported schema set actually referenced by that XSD.
- **EXACT NAME if known:** `EEC_R_HC_MM_01_DrugRegistrationNumberRequestDetails_v1.1.0.xsd`.
- **CURRENT PLACEHOLDER:** version `1.1.0`; local XSD bytes are absent.
- **SOURCE REFERENCE:** `26_ОП.pdf`, PDF 433, Table 17; imports Table 18 on PDF 433–434.
- **NAMESPACE stated by source:** `urn:EEC:R:HC:MM:01:DrugRegistrationNumberRequestDetails:v1.1.0`.
- **DIRECT IMPORT NAMESPACES stated by source:** `ccdo=urn:EEC:M:ComplexDataObjects:vX.X.X; hccdo=urn:EEC:M:HC:ComplexDataObjects:vX.X.X; hcsdo=urn:EEC:M:HC:SimpleDataObjects:vX.X.X; csdo=urn:EEC:M:SimpleDataObjects:vX.X.X`. Exact imported **schema filenames/schemaLocation values are not stated in the audited PDF** and must come from the official XSD/package.
- **WHY NEEDED:** byte-level proof of element declarations, exact imports, datatypes, cardinalities, QName binding and schema-valid XML; PDF-derived StructureDefinition alone cannot prove those.
- **REQUIREMENTS / MESSAGES UNBLOCKED:** 6 current canonical requirements: MSG.014 REQ.001–003; MSG.025 REQ.001–003; plus schema validation of .013/.015. Messages using the structure: P.MM.01.MSG.013, .014, .015, .025.
- **WHAT IT MUST CONTAIN:** authoritative XSD bytes, targetNamespace/root declaration, `xs:import` namespace and schemaLocation values, and all imported schemas required for offline validation.
- **WHO LIKELY OWNS IT if provable:** the normative source is an EEC act; the audited material does not prove the technical repository/owner of the XSD package. Request via the EEC/EAEU normative/integration-data owner.
- **CAN DEVELOPMENT CONTINUE WITHOUT IT?** Yes in TEST/PDF-derived mode; **normative closure and strict XSD validation cannot**.
- **TEMPORARY TECHNICAL OPTION:** current PDF-derived structure metadata and test namespaces.
- **WHY TEMPORARY OPTION IS NOT NORMATIVE:** it is not the official schema byte set and cannot prove imports/types/QNames.
- **SHARED BENEFIT:** No shared benefit proven for OP22/OP23/OP49.
### XSD-RHC006 — R.HC.MM.01.006 — P0
- **MATERIAL:** official XSD for `R.HC.MM.01.006` plus the imported schema set actually referenced by that XSD.
- **EXACT NAME if known:** `EEC_R_HC_MM_01_DrugApprovalApplicationDetails_v1.1.0.xsd`.
- **CURRENT PLACEHOLDER:** version `1.1.0`; local XSD bytes are absent.
- **SOURCE REFERENCE:** `26_ОП.pdf`, PDF 438, Table 20; imports Table 21 on PDF 439.
- **NAMESPACE stated by source:** `urn:EEC:R:HC:MM:01:DrugApprovalApplicationDetails:v1.1.0`.
- **DIRECT IMPORT NAMESPACES stated by source:** `ccdo=urn:EEC:M:ComplexDataObjects:vX.X.X; hccdo=urn:EEC:M:HC:ComplexDataObjects:vX.X.X; hcsdo=urn:EEC:M:HC:SimpleDataObjects:vX.X.X; csdo=urn:EEC:M:SimpleDataObjects:vX.X.X`. Exact imported **schema filenames/schemaLocation values are not stated in the audited PDF** and must come from the official XSD/package.
- **WHY NEEDED:** byte-level proof of element declarations, exact imports, datatypes, cardinalities, QName binding and schema-valid XML; PDF-derived StructureDefinition alone cannot prove those.
- **REQUIREMENTS / MESSAGES UNBLOCKED:** 5 current canonical requirements: MSG.016 REQ.001–005; plus schema validation of .017/.022. Messages using the structure: P.MM.01.MSG.016, .017, .022.
- **WHAT IT MUST CONTAIN:** authoritative XSD bytes, targetNamespace/root declaration, `xs:import` namespace and schemaLocation values, and all imported schemas required for offline validation.
- **WHO LIKELY OWNS IT if provable:** the normative source is an EEC act; the audited material does not prove the technical repository/owner of the XSD package. Request via the EEC/EAEU normative/integration-data owner.
- **CAN DEVELOPMENT CONTINUE WITHOUT IT?** Yes in TEST/PDF-derived mode; **normative closure and strict XSD validation cannot**.
- **TEMPORARY TECHNICAL OPTION:** current PDF-derived structure metadata and test namespaces.
- **WHY TEMPORARY OPTION IS NOT NORMATIVE:** it is not the official schema byte set and cannot prove imports/types/QNames.
- **SHARED BENEFIT:** No shared benefit proven for OP22/OP23/OP49.
### XSD-RHC007 — R.HC.MM.01.007 — P0
- **MATERIAL:** official XSD for `R.HC.MM.01.007` plus the imported schema set actually referenced by that XSD.
- **EXACT NAME if known:** `EEC_R_HC_MM_01_DrugRegistrationStatusDetails_v1.0.0.xsd`.
- **CURRENT PLACEHOLDER:** version `1.0.0`; local XSD bytes are absent.
- **SOURCE REFERENCE:** `26_ОП.pdf`, PDF 450, Table 23; imports Table 24 on PDF 451.
- **NAMESPACE stated by source:** `urn:EEC:R:HC:MM:01:DrugRegistrationStatusDetails:v1.0.0`.
- **DIRECT IMPORT NAMESPACES stated by source:** `ccdo=urn:EEC:M:ComplexDataObjects:vX.X.X; hccdo=urn:EEC:M:HC:ComplexDataObjects:vX.X.X; hcsdo=urn:EEC:M:HC:SimpleDataObjects:vX.X.X; csdo=urn:EEC:M:SimpleDataObjects:vX.X.X`. Exact imported **schema filenames/schemaLocation values are not stated in the audited PDF** and must come from the official XSD/package.
- **WHY NEEDED:** byte-level proof of element declarations, exact imports, datatypes, cardinalities, QName binding and schema-valid XML; PDF-derived StructureDefinition alone cannot prove those.
- **REQUIREMENTS / MESSAGES UNBLOCKED:** 7 current canonical requirements: MSG.007 REQ.001–004; MSG.010 REQ.001–003. Messages using the structure: P.MM.01.MSG.007, .010.
- **WHAT IT MUST CONTAIN:** authoritative XSD bytes, targetNamespace/root declaration, `xs:import` namespace and schemaLocation values, and all imported schemas required for offline validation.
- **WHO LIKELY OWNS IT if provable:** the normative source is an EEC act; the audited material does not prove the technical repository/owner of the XSD package. Request via the EEC/EAEU normative/integration-data owner.
- **CAN DEVELOPMENT CONTINUE WITHOUT IT?** Yes in TEST/PDF-derived mode; **normative closure and strict XSD validation cannot**.
- **TEMPORARY TECHNICAL OPTION:** current PDF-derived structure metadata and test namespaces.
- **WHY TEMPORARY OPTION IS NOT NORMATIVE:** it is not the official schema byte set and cannot prove imports/types/QNames.
- **SHARED BENEFIT:** No shared benefit proven for OP22/OP23/OP49.
## GROUP 2 — R.006 / R.007 CONCRETE VERSIONS
### VERSION-R006 — P0
- **MATERIAL:** official release identity for R.006.
- **EXACT NAME:** source only declares template `EEC_R_ProcessingResultDetails_vY.Y.Y.xsd`; a concrete filename/version is not stated.
- **CURRENT PLACEHOLDER:** `Y.Y.Y`; namespace `urn:EEC:R:ProcessingResultDetails:vY.Y.Y`.
- **SOURCE REFERENCE:** `26_ОП.pdf` PDF 309 / printed 308 / Table 2; Table 3 ties `X.X.X` to the base-model version used to build the technical schema.
- **WHY NEEDED:** forms the concrete root QName and schema identity for MSG.004/009/018.
- **WHAT IT MUST CONTAIN:** concrete R.006 version, concrete targetNamespace, matching official XSD/release, and import bindings.
- **SHARED BENEFIT:** OP22, OP23 and OP49 all use R.006 according to KB message indexes.
- **TEMPORARY OPTION:** `vY.Y.Y` only in TEST mode; this is not a published concrete namespace.
### VERSION-R007 — P0
- **MATERIAL:** official release identity for R.007.
- **EXACT NAME:** source only declares template `EEC_R_ResourceStatusDetails_vY.Y.Y.xsd`; a concrete filename/version is not stated.
- **CURRENT PLACEHOLDER:** `Y.Y.Y`; namespace `urn:EEC:R:ResourceStatusDetails:vY.Y.Y`.
- **SOURCE REFERENCE:** `26_ОП.pdf` PDF 314 / printed 313 / Table 5; imports in Table 6 on PDF 315.
- **WHY NEEDED:** forms the concrete root QName and schema identity for MSG.005/006.
- **WHAT IT MUST CONTAIN:** concrete R.007 version, targetNamespace, matching official XSD/release, import bindings.
- **SHARED BENEFIT:** none proven for OP22/OP23/OP49; KB also shows use by OP32.
- **TEMPORARY OPTION:** `vY.Y.Y` only in TEST mode; not normative.
## GROUP 3 — COMMON MODEL VERSIONS
### MODEL-BASE — P0
- **MATERIAL:** exact **base data model** release used to build the OP26 technical schemas.
- **CURRENT PLACEHOLDER:** `X.X.X`.
- **SOURCE REFERENCE:** R.006 Table 3 PDF 309, R.007 Table 6 PDF 315, and healthcare import tables.
- **PREFIXES / unresolved namespaces:** `ccdo → urn:EEC:M:ComplexDataObjects:vX.X.X`, `csdo → urn:EEC:M:SimpleDataObjects:vX.X.X`.
- **WHY NEEDED:** exact namespace URIs for common complex/simple data objects cannot be proven while `X.X.X` remains.
- **REQUIREMENTS UNBLOCKED:** together with healthcare release/imports, this closes the model-version cause behind **196/201 canonical requirement field-QName issues**. Two additional unresolved QName issues are R.006/R.007 roots; the remaining five canonical requirements are source conflicts.
- **WHAT IT MUST CONTAIN:** concrete model version/release plus official XSD modules corresponding to the `ccdo`/`csdo` namespaces. Exact module filenames are UNKNOWN from the current PDF and must not be guessed.
- **SHARED BENEFIT:** YES — at least OP22/OP23/OP49 through shared R.006, which imports `ccdo`/`csdo`.
- **TEMPORARY OPTION:** retain `vX.X.X` templates in TEST mode; not normative.
### MODEL-HEALTHCARE — P0
- **MATERIAL:** exact **healthcare domain model** release used to build the OP26 healthcare schemas.
- **CURRENT PLACEHOLDER:** `X.X.X`.
- **SOURCE REFERENCE:** `26_ОП.pdf` Table 9 PDF 319–320 and equivalent Tables 12/15/18/21/24.
- **PREFIXES / unresolved namespaces:** `hccdo → urn:EEC:M:HC:ComplexDataObjects:vX.X.X`, `hcsdo → urn:EEC:M:HC:SimpleDataObjects:vX.X.X`; healthcare schemas also import `ccdo` and `csdo`.
- **OTHER RELATED NAMESPACES:** datatype notation in structure rows can reference prefixes such as `bdt`, but the audited OP26 direct-import tables list only `ccdo`, `csdo`, `hccdo`, `hcsdo`. Whether `bdt` or other modules are transitive XSD imports cannot be proven without the official schema/model packages.
- **WHAT IT MUST CONTAIN:** concrete healthcare model version/release and official XSD modules for `hccdo`/`hcsdo`, plus transitive imports required by those modules.
- **SHARED BENEFIT:** no shared benefit proven for OP22/OP23/OP49; KB shows the healthcare model is relevant to other healthcare processes such as OP32.
## GROUP 4 — P.CLS.019
### CLASSIFIER-P.CLS.019 — P1
- **MATERIAL:** official machine-readable payload of classifier `P.CLS.019` (классификатор стран мира).
- **CURRENT PLACEHOLDER:** classifier identity is confirmed, payload/version/effective date are missing.
- **SOURCE REFERENCE:** `26_ОП.pdf` PDF 39 / printed 38 / Table 10: P.CLS.019 contains country names and country codes according to ISO 3166-1.
- **WHY NEEDED:** 11 membership checks cannot be proven from examples; paired `codeListId=P.CLS.019` checks are already source-confirmed.
- **REQUIREMENTS UNBLOCKED:** 11 membership rules: P.MM.01.MSG.001.REQ.035, P.MM.01.MSG.002.REQ.007, P.MM.01.MSG.003.REQ.009, P.MM.01.MSG.007.REQ.004, P.MM.01.MSG.010.REQ.003, P.MM.01.MSG.016.REQ.002, P.MM.01.MSG.019.REQ.005, P.MM.01.MSG.020.REQ.005, P.MM.01.MSG.021.REQ.010, P.MM.01.MSG.023.REQ.008, P.MM.01.MSG.024.REQ.005. The paired 11 codeListId rules are: P.MM.01.MSG.001.REQ.034, P.MM.01.MSG.002.REQ.006, P.MM.01.MSG.003.REQ.008, P.MM.01.MSG.007.REQ.003, P.MM.01.MSG.010.REQ.002, P.MM.01.MSG.016.REQ.001, P.MM.01.MSG.019.REQ.004, P.MM.01.MSG.020.REQ.004, P.MM.01.MSG.021.REQ.009, P.MM.01.MSG.023.REQ.007, P.MM.01.MSG.024.REQ.004.
- **WHAT IT MUST CONTAIN:** `P.CLS.019` identifier metadata, applicable edition/version, effective date/validity metadata, complete code set, country names as the classifier itself declares them, and enough lifecycle/status information to know which codes are valid for the applicable date. **The normative PDF does not prescribe a machine-readable file format**, so XML/JSON/CSV must not be demanded as if normative; request the owner’s official export format. Language requirements are not specified by the audited table.
- **WHO LIKELY OWNS IT if provable:** exact dataset owner is not proven by the audited source; request the official EEC/EAEU reference-data/NSI source.
- **CAN DEVELOPMENT CONTINUE WITHOUT IT?** Yes with external/not-evaluated status or a test snapshot; production membership validation cannot be normative.
- **TEMPORARY TECHNICAL OPTION:** frozen ISO 3166-1 snapshot.
- **WHY TEMPORARY OPTION IS NOT NORMATIVE:** applicable EEC payload edition/effective date and lifecycle are unknown.
- **SHARED BENEFIT:** no shared benefit proven for OP22/OP23/OP49; KB separately records P.CLS.019 dependencies in OP32.
## GROUP 5 — EXTERNAL UNIFIED-REGISTRY CONTRACT
### REGISTRY-CONTRACT — P1
- **MATERIAL:** authoritative integration/data-access contract or authoritative offline snapshot specification for the unified registry of registered medicinal products.
- **CURRENT PLACEHOLDER:** 11 normative lookup dependencies are known; no API/schema/contract is present locally.
- **WHY NEEDED:** existence/absence, identity, active-state, status, time comparison and document-presence checks cannot be executed normatively without authoritative registry semantics.
- **WHAT IT MUST CONTAIN:** canonical record identifiers and key normalization; field/schema names for the values below; active-record definition and EndDateTime null/empty semantics; StartDateTime/history semantics; reference-state role semantics; document group/document identity semantics; not-found vs unavailable vs stale-data behavior; version/effective-date/snapshot semantics; and the official access shape (API or offline snapshot) actually supported by the owner. Do **not** invent endpoint URLs or methods.
- **CAN DEVELOPMENT CONTINUE WITHOUT IT?** local mapping/interface stubs can; the 11 business validations cannot close.
- **TEMPORARY TECHNICAL OPTION:** injected adapter/test snapshot returning controlled facts.
- **WHY TEMPORARY OPTION IS NOT NORMATIVE:** key/history/document/failure semantics remain assumptions until the owner supplies the contract.

| Canonical requirement | PDF/table | Key sent | Registry fact/comparison | Historical date needed | Contract found | Expected failure behavior |
|---|---|---|---|---|---|---|
| `OP26.P_MM_01.P.MM.01.MSG.001.REQ.011` | 209, Table 18 item 11 | ApplicationId + UnifiedCountryCode | No active matching record; active-state interpretation uses empty EndDateTime | NO | NO | comparison/lookup false ⇒ requirement violation; behavior when the registry itself is unavailable/erroring is **UNKNOWN** until the contract defines it |
| `OP26.P_MM_01.P.MM.01.MSG.001.REQ.014` | 210, Table 18 item 14 | DrugApplicationKindCode=02 + registration-certificate identity/details | Stored registration-certificate details must match incoming certificate data | NO | NO | comparison/lookup false ⇒ requirement violation; behavior when the registry itself is unavailable/erroring is **UNKNOWN** until the contract defines it |
| `OP26.P_MM_01.P.MM.01.MSG.001.REQ.015` | 210, Table 18 item 15 | DrugApplicationKindCode=03 + ApplicationChangeId / certificate-change details | Stored change/certificate details must match incoming data | NO | NO | comparison/lookup false ⇒ requirement violation; behavior when the registry itself is unavailable/erroring is **UNKNOWN** until the contract defines it |
| `OP26.P_MM_01.P.MM.01.MSG.001.REQ.028` | 212, Table 18 item 28 | ApplicationId | Matching active registry record must exist; EndDateTime empty | NO | NO | comparison/lookup false ⇒ requirement violation; behavior when the registry itself is unavailable/erroring is **UNKNOWN** until the contract defines it |
| `OP26.P_MM_01.P.MM.01.MSG.002.REQ.009` | 217, Table 19 item 9 | ApplicationId + RegistrationNumberId + UnifiedCountryCode + CountryKindCode | Matching active record; EndDateTime empty; stored StartDateTime < incoming StartDateTime | YES | NO | comparison/lookup false ⇒ requirement violation; behavior when the registry itself is unavailable/erroring is **UNKNOWN** until the contract defines it |
| `OP26.P_MM_01.P.MM.01.MSG.002.REQ.087 [source row; embedded in current REQ.050]` | 230–231, Table 19 item 87 | ApplicationId + UnifiedCountryCode + reference-state role | Matching registry data and PDF documents present in five named document groups | UNKNOWN | NO | comparison/lookup false ⇒ requirement violation; behavior when the registry itself is unavailable/erroring is **UNKNOWN** until the contract defines it |
| `OP26.P_MM_01.P.MM.01.MSG.003.REQ.007` | 232, Table 20 item 7 | ApplicationId + UnifiedCountryCode | Matching active record; EndDateTime empty; stored StartDateTime < exclusion StartDateTime | YES | NO | comparison/lookup false ⇒ requirement violation; behavior when the registry itself is unavailable/erroring is **UNKNOWN** until the contract defines it |
| `OP26.P_MM_01.P.MM.01.MSG.014.REQ.003` | 235, Table 22 item 3 | ApplicationId + UnifiedCountryCode | Matching record with ApplicationStatusCode=06 and reference-state country matching incoming country | NO | NO | comparison/lookup false ⇒ requirement violation; behavior when the registry itself is unavailable/erroring is **UNKNOWN** until the contract defines it |
| `OP26.P_MM_01.P.MM.01.MSG.025.REQ.003` | 236, Table 23 item 3 | ApplicationId and/or RegistrationNumberId | Matching registry record must exist | NO | NO | comparison/lookup false ⇒ requirement violation; behavior when the registry itself is unavailable/erroring is **UNKNOWN** until the contract defines it |
| `OP26.P_MM_01.P.MM.01.MSG.027.REQ.008` | 238, Table 24 item 8 | RegistrationNumberId + DrugRegistrationDocCode or DrugRegistrationFileCode | Matching stored document entry must exist | UNKNOWN | NO | comparison/lookup false ⇒ requirement violation; behavior when the registry itself is unavailable/erroring is **UNKNOWN** until the contract defines it |
| `OP26.P_MM_01.P.MM.01.MSG.028.REQ.005#SOURCE_ROW_5B` | 234, Table 21 item 5 (second occurrence) | RegistrationNumberId + ApplicationId | Matching registry record must exist | NO | NO | comparison/lookup false ⇒ requirement violation; behavior when the registry itself is unavailable/erroring is **UNKNOWN** until the contract defines it |

## GROUP 6 — FIVE SOURCE CONFLICTS
### CONFLICT-002-022 — OP26.P_MM_01.P.MM.01.MSG.002.REQ.022 — P0
- **FILLING TABLE:** `26_ОП.pdf` PDF 219, Table 19 item 22.
- **STRUCTURE TABLE:** PDF 351, R.HC.MM.01.001 Table 10 fields *.2.3.2/*.2.3.3.
- **SIDE A:** filling side: hcsdo:ChildJuvenileIndicator.
- **SIDE B:** structure side: separate hcsdo:ChildIndicator and hcsdo:JuvenileIndicator; ChildJuvenileIndicator absent.
- **WHY CONFLICT:** the filling rule targets data that the declared message structure does not expose under the same normative structure.
- **WHAT CANNOT BE AUTOMATICALLY CHOSEN:** field alias/replacement, cross-structure borrowing, or revised schema authority.
- **REGULATOR QUESTION:** Confirm which field(s) the rule shall target: ChildIndicator, JuvenileIndicator, both, or a corrected field name; provide corrigendum/revised XSD if applicable.
- **TEMPORARY OPTION:** alias/virtual-field hypothesis for tests only.
- **WHY NOT NORMATIVE:** no audited source authorizes the substitution.
### CONFLICT-023-004 — OP26.P_MM_01.P.MM.01.MSG.023.REQ.004 — P0
- **FILLING TABLE:** `26_ОП.pdf` PDF 298, Table 21 item 4.
- **STRUCTURE TABLE:** PDF 415–421, R.HC.MM.01.002 Table 13.
- **SIDE A:** filling side: DrugAttributeEnumText with AttributeKindCode or AttributeKindName.
- **SIDE B:** structure side: none of DrugAttributeEnumText/AttributeKindCode/AttributeKindName is declared.
- **WHY CONFLICT:** the filling rule targets data that the declared message structure does not expose under the same normative structure.
- **WHAT CANNOT BE AUTOMATICALLY CHOSEN:** field alias/replacement, cross-structure borrowing, or revised schema authority.
- **REGULATOR QUESTION:** Confirm the authoritative target element/attributes, or provide corrected filling table / revised R.HC.MM.01.002 XSD.
- **TEMPORARY OPTION:** alias/virtual-field hypothesis for tests only.
- **WHY NOT NORMATIVE:** no audited source authorizes the substitution.
### CONFLICT-023-005 — OP26.P_MM_01.P.MM.01.MSG.023.REQ.005 — P0
- **FILLING TABLE:** `26_ОП.pdf` PDF 298, Table 21 item 5.
- **STRUCTURE TABLE:** PDF 415–421, R.HC.MM.01.002 Table 13.
- **SIDE A:** filling side: AttributeKindCode/AttributeKindName inside DrugAttributeEnumText must denote “Номер документа основания”.
- **SIDE B:** structure side: referenced element/attributes absent.
- **WHY CONFLICT:** the filling rule targets data that the declared message structure does not expose under the same normative structure.
- **WHAT CANNOT BE AUTOMATICALLY CHOSEN:** field alias/replacement, cross-structure borrowing, or revised schema authority.
- **REGULATOR QUESTION:** Confirm the intended field(s) that carry “Номер документа основания”, or provide corrected filling table / revised schema.
- **TEMPORARY OPTION:** alias/virtual-field hypothesis for tests only.
- **WHY NOT NORMATIVE:** no audited source authorizes the substitution.
### CONFLICT-024-006 — OP26.P_MM_01.P.MM.01.MSG.024.REQ.006 — P0
- **FILLING TABLE:** `26_ОП.pdf` PDF 300, Table 22 item 6.
- **STRUCTURE TABLE:** PDF 415–421, R.HC.MM.01.002 Table 13.
- **SIDE A:** filling side: DrugAttributeEnumText requires AttributeKindCode or AttributeKindName.
- **SIDE B:** structure side: referenced element/attributes absent.
- **WHY CONFLICT:** the filling rule targets data that the declared message structure does not expose under the same normative structure.
- **WHAT CANNOT BE AUTOMATICALLY CHOSEN:** field alias/replacement, cross-structure borrowing, or revised schema authority.
- **REGULATOR QUESTION:** Confirm the authoritative target element/attributes, or provide corrected filling table / revised schema.
- **TEMPORARY OPTION:** alias/virtual-field hypothesis for tests only.
- **WHY NOT NORMATIVE:** no audited source authorizes the substitution.
### CONFLICT-024-007 — OP26.P_MM_01.P.MM.01.MSG.024.REQ.007 — P0
- **FILLING TABLE:** `26_ОП.pdf` PDF 300, Table 22 item 7.
- **STRUCTURE TABLE:** PDF 415–421, R.HC.MM.01.002 Table 13.
- **SIDE A:** filling side: AttributeKindName mandatory when AttributeKindCode is “другое”.
- **SIDE B:** structure side: DrugAttributeEnumText and the referenced attribute context are absent.
- **WHY CONFLICT:** the filling rule targets data that the declared message structure does not expose under the same normative structure.
- **WHAT CANNOT BE AUTOMATICALLY CHOSEN:** field alias/replacement, cross-structure borrowing, or revised schema authority.
- **REGULATOR QUESTION:** Confirm where AttributeKindCode/AttributeKindName are defined for this message and whether a revised R.HC.MM.01.002 schema is authoritative.
- **TEMPORARY OPTION:** alias/virtual-field hypothesis for tests only.
- **WHY NOT NORMATIVE:** no audited source authorizes the substitution.
## GROUP 7 — MSG.002 / TABLE 19 / ITEM 84
### ITEM84-CORRECTION — P0
- **MATERIAL:** official corrected/complete wording of `P.MM.01.MSG.002`, Table 19, item 84.
- **CURRENT STATE:** `26_ОП.pdf` PDF 230 / printed 229 visibly ends item 84 at `«...обязательны для заполнения и»`; item 85 starts immediately after it on the same page. PDF 231 / printed 230 continues item 87, not item 84. The same truncation is present in KB source extraction.
- **LOCAL CORRIGENDUM/ALTERNATE EDITION:** NOT FOUND. The normative directory contains only one `26_ОП.pdf`; no local PDF/filename indicating a corrigendum/alternate OP26 edition was found. `XML/ГИС_ИШ/ОП 26/Решение №68.md` is a local explanatory note, not an alternate official source.
- **WHY NEEDED:** one atomic business rule cannot be mapped or tested without its missing predicate/consequence tail.
- **WHAT IT MUST CONTAIN:** the complete authoritative text of item 84 and, if corrected by another act, the act/revision/date that supersedes the truncated publication.
- **TEMPORARY OPTION:** infer a symmetric condition from item 83.
- **WHY TEMPORARY OPTION IS NOT NORMATIVE:** symmetry is not source evidence.
## Official-source discovery
A targeted web search was limited to official EEC/EAEU domains and exact schema/classifier identifiers. It did **not** surface a confirmed official payload for any of the eight XSDs, P.CLS.019 dataset, concrete R.006/R.007 release, model package, registry contract, or item-84 corrigendum. An official EEC PDF for Decision No. 79 of 30 June 2017 surfaced contextual use of `P.CLS.019`, but it is not the missing classifier payload/version for this OP26 release and is therefore rejected as a match. `CONFIRMED_MATCH=0`, suitable `CANDIDATE_ONLY=0`.
