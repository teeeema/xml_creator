# OP32 / P.MM.06 — normative source recovery snapshot

**Baseline date:** 2026-10-06  
**Status:** COMPLETE_WITH_DOCUMENTED_BLOCKERS  
**Input baseline:** 170 atomic requirements from the completed strict re-audit. Historical `OP32_REAUDIT_*` files were not regenerated.

## Discovery scope

- Primary normative directory: `/Users/tema/Documents/Work/Документы_xml` — 48 files inspected by recursive inventory.
- Local normative PDFs inspected for cross-OP model/version evidence: **7** (`26_ОП`, `32_ОП`, `35.1_ОП`, `49_ОП`, Decision 5, OP22, OP23).
- XSD files found: **0** in the normative directory, **0** in the repository.
- Candidate archives (`zip/rar/7z/tar/gz/tgz`) found: **0** in the normative directory, **0** in the repository.
- Machine-readable classifier payload candidates in the normative directory: **0**; JSON files found there are Obsidian/plugin metadata, not classifier datasets.

## Import/version recovery

The 7 structures produce **24 owner→import edges**. Every edge is explicitly listed in `OP32_STRUCTURE_IMPORT_INVENTORY.csv`. The normative import tables keep base model versions as `X.X.X` and healthcare model versions as `Z.Z.Z`. Cross-search of the other local normative PDFs found no concrete `vN.N.N` version for these imported model namespaces.

- IMPORTS_TOTAL: **24**
- IMPORTS_VERSION_RESOLVED: **0**
- IMPORTS_VERSION_UNRESOLVED: **24**

## QName recovery

All 170 baseline requirements were checked. For 164 rows the previous audit already captured explicit prefixed XML tokens. Two more rows (`csdo: EndDateTime`) were normalized to the official token `csdo:EndDateTime` because the PDF inserts whitespace after the colon. Four `Документ в формате XML` rules still expose no XML local name in the requirement text.

This does **not** resolve exact QName: the namespace version remains a placeholder and no XSD/official XML instance with concrete namespace versions was found. Therefore every requirement stays `QNAME_UNRESOLVED`; the CSV records the recovered prefix/local-name evidence separately from the exact QName decision.

- QNAME_TOTAL: **170**
- QNAME_RESOLVED_XSD: **0**
- QNAME_RESOLVED_STRUCTURE_TABLE: **0** (structure tables confirm prefix/local-name vocabulary, but not a concrete namespace version)
- QNAME_RESOLVED_OFFICIAL_XML: **0**
- QNAME_UNRESOLVED: **170**
- QNAME_CONFLICT: **0**

## Classifier recovery

All **59** prior `OPEN_CLASSIFIER` rows are represented in `OP32_CLASSIFIER_SOURCE_INVENTORY.csv`. Table 9 of `32_ОП.pdf` confirms classifier metadata/identifiers used by the process; structure tables further connect the affected code fields to classifier semantics. The local source set contains no machine-readable code list and no authoritative dataset snapshot/version suitable for production validation.

A noteworthy normative detail was preserved literally: structure Table 10 p.171 describes `M.HC.SDE.00468` (the application-kind field) as using the classifier name corresponding to `P.MM.06.CLS.002`. Because that is what the official page says, the recovery records it without silently substituting another classifier.

- CLASSIFIER_TOTAL: **59 requirements**
- CLASSIFIER_MACHINE_READABLE_FOUND: **0**
- CLASSIFIER_PRODUCTION_READY: **0**
- CLASSIFIER_STILL_MISSING: **59**

## External registries / engine / ambiguity

- External registry requirements: **11**; reclassified: **0**; remaining: **11**. No official local registry snapshot was found.
- Previous engine gaps: **2**. Current shared engine was re-read and still has no regex/string-pattern rule kind and no PDF semantic-content inspection rule kind. ENGINE_NOW: **2**, reclassified: **0**.
- Normative ambiguity: Table 14 requirement 47 remains **1**. Cross-search of the local official PDFs found no corrected wording/clarification.

## Status after recovery

No production rule was added and no requirement became implemented. Exact QName/path remains the gating source requirement, so none of the 97 missing-normative-data rows can safely move to `OPEN_PRODUCTION_MAPPING` yet. Classifier metadata recovery is useful evidence but does not close the 59 classifier gaps without datasets.

- IMPLEMENTED_CONFIRMED: **0**
- OPEN_ENGINE: **2**
- OPEN_PRODUCTION_MAPPING: **0**
- OPEN_CLASSIFIER: **59**
- OPEN_EXTERNAL_REGISTRY: **11**
- OPEN_NORMATIVE_AMBIGUITY: **1**
- OPEN_SOURCE_CONFLICT: **0**
- OPEN_MISSING_STRUCTURE: **0**
- OPEN_MISSING_NORMATIVE_DATA: **97**
- OTHER_OPEN: **0**
- SAFE_PRODUCTION_MAPPING_TOTAL_AFTER_RECOVERY: **0**
- B1/B2/B3/B4: **0 / 0 / 0 / 0**

Arithmetic: **170 = 0 implemented + 170 open**; open-reason arithmetic remains **2 + 0 + 59 + 11 + 1 + 0 + 0 + 97 + 0 = 170**. Canonical IDs remain unique and all inherited OP→PRC→TRN→MSG→REQ trace fields are populated.

## OPR.007 / OPR.008

Both are normatively confirmed internal Commission operations in `P.MM.06.PRC.002` and are absent from the current package operation catalog. They do not have direct TRN/MSG references, so the current transaction runtime does not fail merely because they are missing; the package catalog is nevertheless normatively incomplete. See `OP32_MISSING_OPERATIONS_AUDIT.md`.

## Verification

- `python3.13 -m pytest P.MM.06_OP_32/tests -q` → **8 passed**.
- `P.MM.06_OP_32/**` production diff for this session: **0**.
- Historical `OP32_REAUDIT_*` baseline files: **unchanged by SHA-256 check**.
- Shared `rules_engine.py`, `services.py`, and `validator.py` were already dirty from parallel work before this recovery and were not edited by this session.
- GUI files were not edited by this session.

## Remaining material needed

1. Official technical XSD set for the seven OP32 structures, including concrete base/healthcare model namespace versions replacing `X.X.X`/`Z.Z.Z`.
2. Official machine-readable classifier datasets and applicable versions/snapshots for the 59 classifier-dependent requirements.
3. Official corrected wording or clarification for Table 14 requirement 47.
4. Authoritative external-registry interface/fixture for the 11 registry/history checks.
