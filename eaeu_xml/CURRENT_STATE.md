# Current state — 2026-10-23

OP26 version infrastructure uses the existing isolated catalogs and readiness passport. Direct loading validates process/version identity and profile paths. Cached selections and engine generation recheck readiness; version catalogs cannot link legacy manifests.

OP26 1.1.0 remains the default. Its normative catalogs are unchanged. Stage 1 state (superseded in part by Stage 2 below): OP26 1.3.0 was source-only and DRAFT_NOT_READY: official 140/2025 and 77/2026 tables are imported; executable structures, rules, policies and application/GUI selection remain incomplete. Do not promote it.

Evidence and limitations: `../codex_reports/OP26_P_MM_01/V130_COMPLETION/FINAL_REPORT.md` and `verification/`. The target branch did not contain `project_memory/` or the KB index/rules/source text files; original instructions were consulted before switching from the initial checkout.

## Stage 2 — partial executable structures and rules

Seven source-table trees now bind all 710 imported fields. Effective imported model QNames remain unresolved (591 element rows); 119 attribute/arbitrary-XML source interpretations are verified. No structure has complete normative/XSD closure.

167 local constraints cover 148/481 rows fully and 2 partially; 87 external-context rows and 244 unimplemented rows remain. The shared Body provider preserves repeated-parent axes and missing slots, rejects scalar broadcast, and extracts exact QNames/order. Incomplete evaluations cannot produce is_complete=true. Forty-one synthetic TEST Body roundtrips are component proof only; normal 1.3.0 engine loading remains blocked.

Stage 2 evidence: `../codex_reports/OP26_P_MM_01/V130_STAGE2/FINAL_REPORT.md`. DRAFT_NOT_READY, promotion_allowed=false, default 1.1.0, official XSD NOT_EXECUTED.

## Stage 3 — additional rules, official classifier snapshots and read-only edition status

518 local constraints fully cover 270/481 rows; 10 partial, 71 source/external-context and 130 not implemented remain. 122 of the former 333 incomplete rows are closed; 211 remain. Exact expanded model QNames still unresolved for 591 element rows; official schema validation remains unavailable. Eight complete, dated NSI snapshots are loaded through the canonical loader, checked against official payload hashes/counts and used in real classifier predicates. Four custom-code datasets and ten failed data endpoints need further work; 25 catalog references have no explicit NSI binding.

The application/Qt information view exposes edition availability without selecting/loading draft generation. Default OP26 remains 1.1.0; production engine 1.3.0 remains blocked. Cardinality now counts emitted nodes rather than missing None slots, fixing a reproduced false acceptance. New reports: `../codex_reports/OP26_P_MM_01/V130_STAGE3/`.

Stage 3 completion (2026-10-26): focused 33 passed / 1231 subtests; Qt 14 passed; latest all-backend run 13 failed / 731 passed / 2424 subtests. Shared-tree regression remains open. Do not interpret earlier green counts as current whole-project readiness. Completeness must remain false for unresolved namespace/data diagnostics.

Final recorded Stage3 evidence: focused 12 failed / 33 passed / 1219 subtests; backend 31 failed / 725 passed / 2417 subtests; isolated Qt14 passed. Frozen logs under Stage3/verification/final_snapshot override earlier intermediate counts. Shared completeness semantics and concurrent changes remain unresolved; no release readiness claim.

## 2026-10-27 — divergence reconciliation (not a new validation run)

Merged report evidence retains the local c765269b historical baseline, including failed focused/backend runs; the 4a84426a report variants are archived byte-for-byte under `../codex_reports/OP26_P_MM_01/V130_STAGE3/provenance/4a84426aa627db649b9017dd26a7b073425f4e0c/`. Both parent versions are preserved there under full commit identifiers. Counts above describe their original runs, not the reconciled candidate. No fresh PASS, readiness promotion, or official XSD validation is asserted. OP26 1.3.0 remains DRAFT_NOT_READY and production-blocked; default remains 1.1.0. See the Stage3 provenance README for interpretation.
