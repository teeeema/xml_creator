# OP35.1 / P.TS.01 — P0 source recovery final

STATUS: COMPLETE_WITH_EXPLICIT_P0_SOURCE_GAPS

## Scope

This recovery is limited to P0 blockers from `INITIAL_AUDIT` for `P.TS.01` / “Реестр сертификатов и деклараций соответствия”. The primary OP source is `/Users/tema/Documents/Work/Документы_xml/35.1 ОП.pdf`; all local files under `/Users/tema/Documents/Work/Документы_xml` were considered for source recovery. No production code, tests, GUI, shared engine, Knowledge Base or other OP materials were modified.

## Classifier/reference recheck

CLASSIFIERS_TOTAL=17

- PRESENT_COMPLETE=2
- PRESENT_DOCUMENT_ONLY=0
- PRESENT_PARTIAL=1
- EXTERNAL_ONLY=14
- MISSING=0

Recovered locally with complete payload:

1. `BUSINESS_ENTITY_LEGAL_FORM_REFERENCE` — Decision No. 54 dated 02.04.2019; registry/resource code `2049`; full classifier payload present in `54 решение.pdf`.
2. `COMMUNICATION_CHANNEL_KIND_REFERENCE` — Decision No. 192 dated 06.12.2022; registry/resource code `1041`; designation `ЕС 041-2022 (ред. 1)`; full payload present in `192 решение .pdf`.

`CODELIST_IDENTIFIER_META` is `PRESENT_PARTIAL`: OP35.1 defines the `codeListId` field contract and cardinality where used, but this is metadata pointing to concrete external reference resources, not a standalone classifier whose decision/registry code can be fabricated.

TRUE_MISSING_CLASSIFIERS: None. The other 14 rows are kept `EXTERNAL_ONLY` because OP35.1 confirms the external normative/reference dependency but the exact local act/payload/version was not recovered. `378 решение.pdf` contains customs reference material, including country/unit/TN-VED-related material, but without an explicit normative linkage to the exact OP35.1 dependency it is not accepted as closure.

## XSD recovery

XSD_MISSING=5

1. `EEC_R_DocDetails_vY.Y.Y.xsd`
2. `EEC_R_ProcessingResultDetails_vY.Y.Y.xsd`
3. `EEC_R_ResourceStatusDetails_vY.Y.Y.xsd`
4. `EEC_R_TR_TS_01_ConformityDocsRegistryDetails_v1.0.3.xsd`
5. `EEC_R_TR_TS_01_ConformityDocsRegistryRequestDetails_v1.0.0.xsd`

No `.xsd`, `.xml`, `.zip`, `.7z`, `.rar`, `.tar` or `.gz` file is present under the local `Документы_xml` tree, so no executable schema or archived schema package was recovered.

## Model packages

MODEL_PACKAGES_MISSING=2

1. Base data model package: `bdt` / `ccdo` / `csdo`, namespaces ending in `vX.X.X`.
2. Technical-regulation domain data model package: `trcdo` / `trsdo`, namespaces ending in `vZ.Z.Z`.

OP35.1 explicitly says `X.X.X` and `Z.Z.Z` are the versions of the base/domain models used to develop the technical schema that is to be included in the registry of electronic-document/data structures. Concrete package versions are not recoverable from the local source set.

## R.004 / R.006 / R.007 versions

- R.004_VERSION: `Y.Y.Y` — unresolved placeholder.
- R.006_VERSION: `Y.Y.Y` — unresolved placeholder.
- R.007_VERSION: `Y.Y.Y` — unresolved placeholder.

For all three, the PDF explicitly states that `Y.Y.Y` corresponds to the structure version determined according to the base-model version used to develop the technical schema to be included in the registry of electronic-document/data structures. The concrete version therefore needs the authoritative registry/XSD package and the matching concrete base-model version. It cannot be determined locally without guessing.

## PRC.002

PRC002_TABLE_ACTUALLY_PRESENT: NO

PDF page 25, clause 12 of the PRC.002 regulation says Figure 2 contains the transaction scheme and Table 2 contains the operation/state/transaction relation. The local PDF immediately starts the next approved document after that clause; the promised Figure 2/Table 2 are absent. This is a source-content truncation/gap, not an extraction-only problem.

No `OPR.004-.008`, `TRN.003` or `MSG.004-.006` is inferred.

## Integration and routing

Decision No. 5 locally recovers the generic integration-header contract, `EAEU://` logical-address grammar, and the Action component order. OP35.1 independently confirms process code/version `P.TS.01 / 2.0.0`, so the generic application Action pattern is:

`int://CP/P.TS.01/2.0.0/<PRC>/<TRN>/<MSG>`

Exact per-message Action constants remain blocked because complete source-confirmed transaction-to-message mappings are unavailable in the current consolidated source, especially for PRC.002.

The authority-routing blocker is a normative reference directory (`TYPE A`). OP35.1 pages 14-15 require the authority/organization identifier for multi-participant roles and point to the directory in section VII of the Rules; Decision No. 5 clauses 52-53 define the generic rule and maintenance of authority/organization lists. The actual directory identifier/version/payload is not local.

## One normative ambiguity

MSG: `P.TS.01.MSG.001` (the same structure is also used by MSG.007/.011/.014)

REQ: `P.TS.01::R.TR.TS.01.001::T13::ROW068::REFERENCE_DATA`

PAGE: 55

TABLE: Table 13

ORIGINAL_NORMATIVE_TEXT: Row 2.9.4 defines `csdo:BusinessEntityTypeCode` as optional `0..1`; when the code is present its value is taken from the reference resource identified by mandatory `codeListId`. Row 2.9.5 separately defines `csdo:BusinessEntityTypeName` as optional `0..1`. The table contains no explicit cross-field rule linking presence or consistency of the two fields.

INTERPRETATION_A: the code and name are independently optional; only `codeListId` is mandatory when the code exists.

INTERPRETATION_B: the code and name represent the same legal-form reference item and therefore must be paired and/or mutually consistent when both are used.

RESOLVING_SOURCE: authoritative XSD plus the concrete base-model semantic rule / normative usage rule for `BusinessEntityTypeCode` and `BusinessEntityTypeName` (and, if applicable, the exact reference-resource contract). No cross-field constraint is invented in this recovery.

## Actual P0 material still to find

1. The five executable XSD files listed above, including concrete-version resolution for R.004/R.006/R.007.
2. The concrete base data model package/version resolving `X.X.X`.
3. The concrete technical-regulation domain model package/version resolving `Z.Z.Z`.
4. Authoritative registry entries/package metadata for R.004, R.006 and R.007 resolving `Y.Y.Y` and linking each structure to the concrete base-model version.
5. Complete official PRC.002 regulation under Decision No. 39 with the Figure 2 / Table 2 referenced by clause 12.
6. Authoritative authority-routing directory identifier/version/payload referenced by OP35.1 Regulation clause 12 / section VII of the Rules.
7. Authoritative acts/registry records/payloads for the 13 unresolved external reference resources besides the routing directory: address kinds; business-entity identification methods; conformity-document kinds; conformity-document statuses; country codes; data formats; document kinds; processing results; standards; technical regulations list; technical-regulation object kinds; TN VED EAEU; units of measurement.

## Readiness

P0_GAPS_RESOLVED_BY_EXISTING_LOCAL_FILES: 2 classifier payloads fully recovered (Decision 54 / code 2049 and Decision 192 / code 1041); Decision No. 5 recovers the generic header/Action/address contract; OP35.1 itself confirms process version 2.0.0 and proves the PRC.002 source-content gap.

CAN_IMPLEMENTATION_START_AFTER_THIS_RECHECK: NO

Reason: all 11 source-confirmed messages remain blocked from source-complete normative implementation by missing executable XSD/model packages; R.004/R.006/R.007 additionally lack concrete versions, and exact per-message Action/routing closure is incomplete. This matches the initial implementability baseline (`READY_FOR_IMPLEMENTATION=0`).

RECOMMENDED_FIRST_MSG: `P.TS.01.MSG.002` after recovery of the concrete R.007 version/XSD, matching base-model package, its required reference data, and the source-confirmed integration/routing values. R.007 is the smallest currently relevant message structure.
