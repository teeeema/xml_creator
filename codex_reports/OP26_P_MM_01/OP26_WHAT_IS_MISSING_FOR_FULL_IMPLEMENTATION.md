# OP26 / P.MM.01 — what is missing for full normative implementation

## Executive summary

For full OP26 implementation, the project is missing **concrete schema/model versions and XSD bytes, authoritative P.CLS.019 data, an external unified-registry contract, resolution of five source conflicts, the missing tail of one truncated normative rule, 80 atomic executable mappings, requirement-level negative tests, and strict runtime proof**.

The headline `201 requirements` is not a complete atomic inventory. All **201/201 canonical records were reviewed**, but Table 19 for MSG.002 has source rows 50–87 collapsed into canonical REQ.050 (+37 omitted atomic rows), and Table 21 for MSG.028 repeats source code 5 with two different rules collapsed into one canonical REQ.005 (+1 atomic row). The source-based audit baseline is therefore **239 atomic requirements**.

Current workspace has 201 business-rule records and 159 structured executable mappings. The canonical 42 unmapped records expand to **80 unmapped atomic requirements**. Of those, **52 can be mapped now from existing source text**; **28 need missing/contradictory external information** (11 classifier memberships + 11 registry lookups + 5 source conflicts + 1 truncated rule). Separately, exact field namespaces are not closed: **196/201 canonical records have `PREFIXED_NAMESPACE_UNRESOLVED` field QNames**, and the remaining five are source conflicts. This prevents a 100% strict normative XML claim even for locally expressible rules.

### Audit issue counts

| Category | Count | Highest severity | Meaning |
|---|---:|---|---|
| MISSING_NORMATIVE_DATA | 0 | — | No separate unclassified missing-text bucket; the one incomplete rule is counted as NORMATIVE_AMBIGUITY. |
| MISSING_XSD | 8 | HIGH | All eight declared structure XSD payloads are absent. |
| VERSION_PLACEHOLDER | 4 | BLOCKER | R.006, R.007, base model, healthcare model. |
| UNRESOLVED_QNAME | 198 | BLOCKER | 196 requirement field QNames + 2 service-root QNames. |
| CLASSIFIER_PAYLOAD_MISSING | 11 | BLOCKER | P.CLS.019 membership checks only; 11 paired codeListId rules are safe now. |
| EXTERNAL_REGISTRY_CONTRACT_MISSING | 11 | BLOCKER | Corrected from historical 14. |
| SOURCE_CONFLICT | 5 | BLOCKER | Confirmed against both filling tables and structure tables. |
| NORMATIVE_AMBIGUITY | 1 | BLOCKER | MSG.002 Table 19 item 84 is truncated. |
| ENGINE_CAPABILITY_MISSING | 0 | — | No confirmed generic local-rule primitive gap. |
| PRODUCTION_MAPPING_MISSING | 80 | HIGH | Atomic source count, not the stale 42-canonical count. |
| TEST_COVERAGE_MISSING | 159 | MEDIUM | No dedicated negative test per mapped requirement. |
| RUNTIME_PROOF_MISSING | 159 | HIGH | TEST-mode invocation exists; strict normative branch proof does not. |
| OTHER | 5 | HIGH | Two canonicalization defects, two source-numbering anomalies, one stale classifier KB provenance issue. |

Total issue records in `OP26_MISSING_INFORMATION.csv`: **641**. Categories intentionally overlap because one requirement may have multiple independent problems.

## High-priority gap table

| # | Category | MSG / REQ | What is missing | Where visible | Criticality | What resolves it | Temporary option |
|---:|---|---|---|---|---|---|---|
| 1 | VERSION_PLACEHOLDER / UNRESOLVED_QNAME | R.006; MSG.004/009/018 | concrete version/root namespace | PDF 309 / printed 308 / Table 2 | BLOCKER | official R.006 schema release/version | NON-NORMATIVE TEST namespace `vY.Y.Y` |
| 2 | VERSION_PLACEHOLDER / UNRESOLVED_QNAME | R.007; MSG.005/006 | concrete version/root namespace | PDF 314 / printed 313 / Table 5 | BLOCKER | official R.007 schema release/version | NON-NORMATIVE TEST namespace `vY.Y.Y` |
| 3 | VERSION_PLACEHOLDER / UNRESOLVED_QNAME | 196 canonical requirements | concrete `ccdo/csdo/hccdo/hcsdo` namespace versions | PDF 309/Table 3; PDF 319–320/Table 9; current profile `X.X.X` | BLOCKER | exact base/healthcare model releases | keep prefix templates in TEST mode |
| 4 | MISSING_XSD | all 8 structures | actual schema bytes/imports | structure-description tables; recursive search found none | HIGH | official XSD package | PDF-derived structures only |
| 5 | CLASSIFIER_PAYLOAD_MISSING | 11 membership REQs | full P.CLS.019 code set/version | filling tables + PDF 39/Table 10 | BLOCKER | official machine-readable classifier | injected ISO snapshot (NON-NORMATIVE) |
| 6 | EXTERNAL_REGISTRY_CONTRACT_MISSING | 11 atomic REQs | authoritative lookup/API/schema semantics | filling tables listed below | BLOCKER | registry contract or official snapshot spec | injected adapter/snapshot (NON-NORMATIVE) |
| 7 | SOURCE_CONFLICT | MSG.002/REQ.022 | ChildJuvenileIndicator vs ChildIndicator/JuvenileIndicator | PDF 219 vs 351 | BLOCKER | official correction/clarification | alias hypothesis only |
| 8 | SOURCE_CONFLICT | MSG.023/REQ.004-.005 | fields absent from R.HC.MM.01.002 | PDF 298 vs Table 13 PDF 415–421 | BLOCKER | corrected rule or revised schema | virtual alias (NON-NORMATIVE) |
| 9 | SOURCE_CONFLICT | MSG.024/REQ.006-.007 | fields absent from R.HC.MM.01.002 | PDF 300 vs Table 13 PDF 415–421 | BLOCKER | corrected rule or revised schema | virtual alias (NON-NORMATIVE) |
| 10 | NORMATIVE_AMBIGUITY | MSG.002 source item 84 | missing tail after “...обязательны для заполнения и” | PDF 230 / printed 229 / Table 19 | BLOCKER | corrected publication | infer symmetry (NON-NORMATIVE) |
| 11 | PRODUCTION_MAPPING_MISSING | 80 atomic rules | executable mappings | current 159 structured rules vs 239 atomic source rows | HIGH | map after/source-safe subset now | external markers for blocked rules only |
| 12 | TEST/RUNTIME PROOF | 159 mapped rules | dedicated negative + strict proof | current tests/runtime matrix | MEDIUM/HIGH | source-traced tests + strict XSD-valid E2E | TEST-mode proof only |

## 1. Inventory defect: why 201 is not the atomic total

### MSG.002 / Table 19

Canonical `MSG.002.REQ.050` contains the text of source items **50 through 87**. The primary PDF shows them as separate numbered rows over PDF 224–231. Therefore current canonical inventory is missing 37 atomic entries 051–087. Item 84 is itself truncated in the publication. Item 87 is an external-registry check, while the other source rows mostly describe local conditional presence/value logic. A single `REQ.050` cannot be used as proof that all 38 were implemented/tested.

### MSG.028 / Table 21

PDF 233 has item 5: if `RegistrationFileIndicator=1`, dossier document code is required and registration-file code is forbidden. PDF 234 begins **another item 5**: the unified registry must contain matching `RegistrationNumberId + ApplicationId`. Current canonical REQ.005 concatenates both. The audit uses report-only labels `005A` and `005B`; these suffixes are not normative identifiers.

Result: **201 canonical records = 239 atomic source requirements**.

## 2. XSD, versions and QName closure

Eight XSD filenames are declared and none of their bytes were found. Recursive search covered `/Users/tema/Documents/Work/Документы_xml` for `*.xsd`, `*.xml`, `*.zip`, `*.rar`, `*.7z` and schema/structure/classifier names; the OP26 subdirectory contains markdown extracts only.

| Structure | Version in source | Declared XSD | Actual bytes | Source |
|---|---|---|---|---|
| `R.006` | `Y.Y.Y` | `EEC_R_ProcessingResultDetails_vY.Y.Y.xsd` | **NOT FOUND** | PDF 309 / printed 308 / Table 2 |
| `R.007` | `Y.Y.Y` | `EEC_R_ResourceStatusDetails_vY.Y.Y.xsd` | **NOT FOUND** | PDF 314 / printed 313 / Table 5 |
| `R.HC.MM.01.001` | `1.1.0` | `EEC_R_HC_MM_01_DrugRegistrationDetails_v1.1.0.xsd` | **NOT FOUND** | PDF 319 / printed 318 / Table 8 |
| `R.HC.MM.01.002` | `1.1.0` | `EEC_R_HC_MM_01_DrugRegistrationExpertReportDetails_v1.1.0.xsd` | **NOT FOUND** | PDF 413 / printed 412 / Table 11 |
| `R.HC.MM.01.003` | `1.1.0` | `EEC_R_HC_MM_01_DrugRegistrationDocContentDetails_v1.1.0.xsd` | **NOT FOUND** | PDF 422 / printed 421 / Table 14 |
| `R.HC.MM.01.004` | `1.1.0` | `EEC_R_HC_MM_01_DrugRegistrationNumberRequestDetails_v1.1.0.xsd` | **NOT FOUND** | PDF 433 / printed 432 / Table 17 |
| `R.HC.MM.01.006` | `1.1.0` | `EEC_R_HC_MM_01_DrugApprovalApplicationDetails_v1.1.0.xsd` | **NOT FOUND** | PDF 438 / printed 437 / Table 20 |
| `R.HC.MM.01.007` | `1.0.0` | `EEC_R_HC_MM_01_DrugRegistrationStatusDetails_v1.0.0.xsd` | **NOT FOUND** | PDF 450 / printed 449 / Table 23 |

The missing XSDs are needed for byte-level proof of imports, element declarations, concrete namespace bindings, XSD datatypes/cardinalities and schema-valid XML. They must not be replaced by guessed schemas.

R.006 and R.007 explicitly use `Y.Y.Y`. The six healthcare roots have concrete structure versions, but their imported base/healthcare namespaces use `vX.X.X`. Current `version_profiles/current.yaml` also records `base=X.X.X` and `healthcare=X.X.X`. That is why 196 canonical requirement field QNames remain prefix-qualified rather than concrete Clark QNames.

## 3. Classifier dependencies: 23 historical -> 22 actual

The historical count 23 incorrectly included `MSG.014.REQ.002`. PDF 235/Table 22/item 2 itself lists allowed `ApplicationStatusCode` values 01–08 and 99, so that rule does not require an external classifier.

The corrected 22 P.CLS.019-dependent rules form 11 pairs. For each pair, the `codeListId` rule is safe now because PDF 39/Table 10 identifies the world-country classifier as **P.CLS.019**. The membership rule remains blocked because no official machine-readable payload/version/effective date is available.

| Message | codeListId rule (safe now) | membership rule (blocked) |
|---|---|---|
| `P.MM.01.MSG.001` | `034` | `035` |
| `P.MM.01.MSG.002` | `006` | `007` |
| `P.MM.01.MSG.003` | `008` | `009` |
| `P.MM.01.MSG.007` | `003` | `004` |
| `P.MM.01.MSG.010` | `002` | `003` |
| `P.MM.01.MSG.016` | `001` | `002` |
| `P.MM.01.MSG.019` | `004` | `005` |
| `P.MM.01.MSG.020` | `004` | `005` |
| `P.MM.01.MSG.021` | `009` | `010` |
| `P.MM.01.MSG.023` | `007` | `008` |
| `P.MM.01.MSG.024` | `004` | `005` |

**Possible technical option:** inject a frozen ISO 3166-1 list. **Why it is not normative:** the project still would not know the exact official EEC payload/version/effective date applicable to this OP26 release.

## 4. External registry: corrected 14 -> 11

Historical `MSG.001.REQ.046`, `MSG.002.REQ.013` and `MSG.020.REQ.011` are local filling rules, not registry lookups. The corrected registry dependencies are:

| Atomic requirement | PDF | Lookup needed | Expected registry fact |
|---|---:|---|---|
| `P.MM.01.MSG.001/011` | 209 | ApplicationId + UnifiedCountryCode | No active matching record; EndDateTime must be empty for active-state check |
| `P.MM.01.MSG.001/014` | 210 | DrugApplicationKindCode=02 + registration certificate identity/details | Stored registration-certificate details must match incoming certificate data |
| `P.MM.01.MSG.001/015` | 210 | DrugApplicationKindCode=03 + ApplicationChangeId / certificate change details | Stored change/certificate details must match incoming data |
| `P.MM.01.MSG.001/028` | 212 | ApplicationId | Matching active registry record must exist; EndDateTime empty |
| `P.MM.01.MSG.002/009` | 217 | ApplicationId + RegistrationNumberId + UnifiedCountryCode + CountryKindCode | Matching active record; EndDateTime empty; stored StartDateTime < incoming StartDateTime |
| `MSG.002 source item 87` | 230–231 | ApplicationId + UnifiedCountryCode + reference-state role | Matching registry data and PDF documents present in five named document groups |
| `P.MM.01.MSG.003/007` | 232 | ApplicationId + UnifiedCountryCode | Matching active record; EndDateTime empty; stored StartDateTime < exclusion StartDateTime |
| `P.MM.01.MSG.014/003` | 235 | ApplicationId + UnifiedCountryCode | Matching record with ApplicationStatusCode=06 and reference-state country matching incoming country |
| `P.MM.01.MSG.025/003` | 236 | ApplicationId and/or RegistrationNumberId | Matching registry record must exist |
| `P.MM.01.MSG.027/008` | 238 | RegistrationNumberId + DrugRegistrationDocCode or DrugRegistrationFileCode | Matching stored document entry must exist |
| `MSG.028 source item 5 (second occurrence)` | 234 | RegistrationNumberId + ApplicationId | Matching registry record must exist |

No authoritative registry API/contract/schema was found. The existing rule engine can mark an external dependency as not evaluated, but that is not the same as performing the normative lookup.

## 5. Source conflicts

Five are confirmed. See `OP26_SOURCE_CONFLICTS_DETAILED.md` for both source sides and non-normative hypotheses. No field substitution was selected.

## 6. Production mapping status

Current files contain **159 structured rules**. The old statement “159 production mapping gaps” is stale. However, the remaining **42 canonical unmapped records expand to 80 atomic source requirements**.

- 52 are safe to map now from current source text.
- 11 are blocked by classifier membership payload.
- 11 are blocked by external registry contract.
- 5 are blocked by source conflict.
- 1 is blocked by truncated normative text.

The 52 safe rules are not a claim of full normative closure: exact imported namespace versions/XSD still have to be obtained.

## 7. Tests and runtime

Executed during this audit:

- `PYTHONPATH=eaeu_xml/src pytest -q -p no:cacheprovider P.MM.01_OP_26/tests/test_pmm01_catalog.py P.MM.01_OP_26/tests/test_all_transactions_e2e.py` → **28 passed, 64 subtests passed**.
- `PYTHONPATH=eaeu_xml/src pytest -q -p no:cacheprovider P.MM.01_OP_26/tests` → **87 passed, 83 subtests passed**.
- `PYTHONPATH=eaeu_xml/src pytest -q -p no:cacheprovider eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_repeatable_xml_alignment.py eaeu_xml/tests/test_process_package_validator.py` → **81 passed, 5 subtests passed**.
- Live rule invocation check → **159/159 current structured rules evaluated in TEST mode: 153 PASS, 6 FAIL** on the generic generated values.

The six generic-value failures are `MSG.023.REQ.001/.006/.009` and `MSG.024.REQ.003/.008/.010`. The existing branch suite still passes because those messages are already classified as normative conflicts, so it does not provide direct positive proof for those six local rules.

There are no direct OP26 tests referencing individual canonical `REQ`/`Rxx` rule IDs. Therefore all 159 mapped rules still lack dedicated requirement-level negative proof. The strict E2E matrix also has zero `VERIFIED_SOAP` branches: 37 placeholder-test branches, 3 conflict branches and 3 initial-message-blocked branches.

## 8. Possible technical workarounds and why they are not normative

- **Placeholder namespaces:** useful for TEST mode, but `X.X.X`/`Y.Y.Y` are not concrete published namespaces.
- **Static country list:** useful for development, but without the official P.CLS.019 version/effective date it cannot establish normative membership.
- **Injected registry snapshot/adapter:** useful for designing the interface, but key/history/document semantics are assumptions until the official contract is known.
- **Aliases for conflicting fields:** technically possible, but choosing a replacement for `ChildJuvenileIndicator` or fields absent from R.HC.MM.01.002 changes the normative mapping.
- **Inference for Table 19 item 84:** neighboring rules suggest a possible symmetric constraint, but the missing published tail cannot be reconstructed as normative fact.

## 9. Minimum external materials to request

1. The eight declared XSDs listed above, plus their authoritative imported schema set.
2. Concrete R.006 and R.007 versions.
3. Concrete base/healthcare model releases used by `ccdo`, `csdo`, `hccdo`, `hcsdo`. Exact imported schema filenames are not established by the current audit and must not be invented.
4. Official P.CLS.019 machine-readable payload with version/effective date.
5. Official unified-registry integration contract/API/schema or authoritative offline snapshot specification for the 11 lookups.
6. Official clarification/corrigendum for the five source conflicts.
7. Official corrected text for MSG.002/Table 19/item 84.

## 10. Files with detailed evidence

- `OP26_MISSING_INFORMATION.csv` — 641 issue rows, source-traced and severity-coded.
- `OP26_AUDIT_EVIDENCE.csv` — exactly 201 canonical rows answering A–Q for each current canonical requirement.
- `OP26_SOURCE_CONFLICTS_DETAILED.md` — five two-sided conflict cards.
- `OP26_FULL_IMPLEMENTATION_READINESS.md` — readiness by work/data category and minimum material package.
