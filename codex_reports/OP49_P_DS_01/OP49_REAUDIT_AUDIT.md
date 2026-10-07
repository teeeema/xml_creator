# OP49 / P.DS.01 normative re-audit

Generated: 2026-10-07. Scope: audit/report only. Production YAML, engine, GUI and production tests were not edited.

## Normative scope

Primary source: `/Users/tema/Documents/Work/Документы_xml/49_ОП.pdf`, SHA-256 `81f82f343650ea19bb293ef7f45d86c57e9195e0cef315e4d190ab47e6d8bae8`, **205 PDF pages**. The KB extraction has the same source hash. Boundary pages 85, 92, 102 and 108 were also visually checked against the original PDF.

The previous 159-row checkpoint is stale. The original PDF proves **166** message-specific requirements:

| Message | Normative requirements | Package business_rules | Package structured_rules | Strict IMPLEMENTED_CONFIRMED | OPEN |
|---|---:|---:|---:|---:|---:|
| P.DS.01.MSG.001 | 35 | 34 | 34 | 0 | 35 |
| P.DS.01.MSG.002 | 38 | 38 | 0 | 0 | 38 |
| P.DS.01.MSG.003 | 0 | 0 | 0 | 0 | 0 |
| P.DS.01.MSG.004 | 2 | 2 | 2 | 0 | 2 |
| P.DS.01.MSG.005 | 54 | 23 | 0 | 0 | 54 |
| P.DS.01.MSG.006 | 37 | 14 | 0 | 0 | 37 |

Total = 35 + 38 + 2 + 54 + 37 = **166**. MSG.003 has no separate message-specific filling table. The old checkpoint missed Table 10 requirement 35 and Table 14 requirements 32-37.

Strict `IMPLEMENTED_CONFIRMED` is **0**. This is intentionally stricter than “rule object exists”: exact imported leaf Clark QNames/XSD closure is incomplete and the existing test suite does not provide a dedicated positive+negative regression pair for every normative requirement. There are 20 locally executable MSG.001 mappings with positive runtime proof, but they remain open under this audit's closure criterion.

## Architecture

Process: **P.DS.01 v1.0.0**. Confirmed package topology: **ACT 3 / PRC 7 / OPR 21 / TRN 7 / MSG 6**.

| Transaction | Procedure | Initiating message | Response | retries | source PDF page |
|---|---|---|---|---:|---:|
| P.DS.01.TRN.001 | P.DS.01.PRC.001 | P.DS.01.MSG.001 | P.DS.01.MSG.003 | 6 | 67 |
| P.DS.01.TRN.002 | P.DS.01.PRC.003 | P.DS.01.MSG.002 | P.DS.01.MSG.003 | 6 | 69 |
| P.DS.01.TRN.003 | P.DS.01.PRC.002 | P.DS.01.MSG.002 | P.DS.01.MSG.003 | 3 | 119 |
| P.DS.01.TRN.004 | P.DS.01.PRC.004 | P.DS.01.MSG.004 | P.DS.01.MSG.003 | 6 | 71 |
| P.DS.01.TRN.005 | P.DS.01.PRC.005 | P.DS.01.MSG.005 | P.DS.01.MSG.003 | 3 | 121 |
| P.DS.01.TRN.006 | P.DS.01.PRC.006 | P.DS.01.MSG.005 | P.DS.01.MSG.003 | 6 | 73 |
| P.DS.01.TRN.007 | P.DS.01.PRC.007 | P.DS.01.MSG.006 | P.DS.01.MSG.003 | 6 | 75 |

## Package versus normative discrepancies

The package contains **111** business-rule rows and **36** structured rules. Normative inventory contains **166** requirements. Therefore **55** normative requirements are absent even as business-rule rows. Another **75** rows exist only as text business rules without structured production rules.

Missing business-rule ranges: MSG.001 requirement 35; MSG.005 requirements 24-54; MSG.006 requirements 15-37. Existing tests that hard-code 34/38/2/23/14 are implementation snapshots and are not normative proof.

Against the canonical primary-PDF text, **63/111** existing package `source_text` values are exact normalized-text matches; **48** differ and therefore are not reused as canonical source text. One existing business-rule source page is wrong: MSG.006 requirement 7 points to PDF p.103, while the requirement starts on p.104. In `messages.yaml`, MSG.006 `message_rules_source_refs` points to p.96/table 14; the primary PDF shows p.96 belongs to table 13 and table 14 starts on p.103. These are package trace discrepancies, not normative evidence.

## Structures

- R.FP.DS.01.001 v1.0.0: 70/70 normative rows indexed; root Clark QName confirmed as `{urn:EEC:R:FP:DS:01:ChargedDistributedReport:v1.0.0}ChargedDistributedReport`.
- R.FP.DS.01.003 v1.0.0: 15/15 normative rows indexed; root Clark QName confirmed as `{urn:EEC:R:FP:DS:01:VerificationProtocol:v1.0.0}VerificationProtocol`.
- R.006 version `Y.Y.Y`: 10/10 structure rows indexed. Root local name `ProcessingResultDetails` is present, but the namespace/version contains placeholders (`vY.Y.Y` and imported `vX.X.X`), so an exact normative Clark QName is **UNRESOLVED**.

## QName and XSD state

- R.FP.DS.01.001 1.0.0: root=ChargedDistributedReport; namespace=urn:EEC:R:FP:DS:01:ChargedDistributedReport:v1.0.0; declared XSD=EEC_R_FP_DS_01_ChargedDistributedReport_v1.0.0.xsd; payload in primary normative directory: **MISSING**.
- R.FP.DS.01.003 1.0.0: root=VerificationProtocol; namespace=urn:EEC:R:FP:DS:01:VerificationProtocol:v1.0.0; declared XSD=EEC_R_FP_DS_01_VerificationProtocol_v1.0.0.xsd; payload in primary normative directory: **MISSING**.
- R.006 Y.Y.Y: root=ProcessingResultDetails; namespace=urn:EEC:R:ProcessingResultDetails:vY.Y.Y; declared XSD=EEC_R_ProcessingResultDetails_vY.Y.Y.xsd; payload in primary normative directory: **MISSING**.

No `.xsd` or XML schema payload was found recursively in the primary normative directory. A declared XSD filename is not treated as a found schema. For R.FP structures, prefixed field names and normative paths are evidenced by the structure tables, while exact imported data-model namespace versions remain unresolved without the payloads.

Three source-conflict patterns affect **35** requirement rows:

- FILLING_TABLE ds01sdo:ModificationDate vs STRUCTURE_TABLE ds01sdo:ModificationDateTime
- FILLING_TABLE csdo:CountryCode vs STRUCTURE_TABLE csdo:UnifiedCountryCode
- FILLING_TABLE ds01cd0:VerificationPro vs STRUCTURE_TABLE ds01cdo:VerificationProDetails

Per repository policy, the audit does not silently normalize either side into a normative fact. The existing package normalization of `CountryCode` to `UnifiedCountryCode` is recorded as implementation behavior only.

## Classifier dependencies

Requirements that state that `currencyCode` must correspond to the currency of the member state need an authoritative country→currency reference source/version. No machine-readable classifier payload was found in the primary normative directory. The audit therefore uses descriptive dependency id `OFFICIAL_MEMBER_STATE_CURRENCY_CODE_MAPPING` and does not invent a classifier number or values.

## External dependencies

Rules referencing the “информационная база” are `EXTERNAL_REGISTRY`: they require state outside one XML document. Rules requiring “следующий рабочий день” use dependency type `EXTERNAL_CALENDAR`; they are counted in `OTHER` rather than being mislabeled as a registry dependency.

## Engine capabilities

Observed engine kinds include cardinality, selection_cardinality, presence, conditional_presence, comparison, aggregate_comparison (SUM), for_each, cross_instance_comparison and group_distinctness. Current aggregate support does not implement MAX, and current selectors do not express “the record whose EventDate is exactly one calendar month earlier”. Therefore month-relative/previous-month semantics and the MAX/all-equal cases are not reported as already solved merely because cross-instance helpers exist.

- B1: **16**
- B2: **57**
- B3: **14**
- B4: **62**
- ENGINE_GAP: **17**

`ENGINE_GAP` is an engine-capability bucket; primary gap-category `ENGINE` is used when engine capability is the main unresolved blocker. Some source-conflict rows also have engine blockers in `secondary_dependencies`.

## Gap categories

All **166** canonical requirements remain OPEN under strict closure. Primary categories are mutually exclusive and sum to 166:

- PRODUCTION_MAPPING: **42**
- ENGINE: **15**
- CLASSIFIER: **52**
- EXTERNAL_REGISTRY: **5**
- SOURCE_CONFLICT: **35**
- NORMATIVE_AMBIGUITY: **0**
- MISSING_STRUCTURE: **0**
- MISSING_NORMATIVE_DATA: **15**
- OTHER: **2**

## Source conflicts

`SOURCE_CONFLICT` means the original filling-requirement table and the original structure table expose different XML names. It is not a parser error and it is not auto-resolved by current package normalization. Each affected row carries its exact conflict and closure criterion in the requirements/gaps CSV.

## Safe implementation now

It is safe to prepare production mappings only for rows whose primary blocker is `PRODUCTION_MAPPING`, while preserving the prefixed normative path and keeping the unresolved exact imported namespace/XSD dependency explicit. Existing structured rules can be tested further, but strict normative closure still requires the official schema/imported model namespace evidence.

No production YAML was changed in this session because the user requested audit/report only.

## Blocked items

- Official XSD payloads / exact imported data-model namespace versions are missing.
- Country→currency classifier/reference payload and version are missing.
- External information-base state/interface is not available in the repository.
- Working-day calendar semantics/provider are not supplied.
- Three source-conflict patterns need authoritative resolution.
- Relative previous-month selection and MAX/all-equal repeated-context semantics are not fully represented by the current structured-rule engine.

## Arithmetic and KB import readiness

Canonical IDs: **166 unique / 166 rows**. Duplicate canonical IDs: **0**. Missing source text: **0**. Missing PDF page/source trace: **0**. Message arithmetic: **PASS**. Gap arithmetic: **PASS**.

`KB_IMPORT_READY = YES` for the audit dataset itself: canonical IDs are stable, total scope is reconciled to the primary PDF, every row has source trace, duplicate count is zero, arithmetic passes, and source conflicts are explicitly represented. This does **not** mean normative implementation is complete, and this session does not import the reports into the KB.
