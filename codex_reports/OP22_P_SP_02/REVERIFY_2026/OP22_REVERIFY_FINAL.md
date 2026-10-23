# OP22 / P.SP.02 — Source-first re-verification 2026

Date: 2026-10-14  
Scope: OP22 / P.SP.02 only  
Canonical requirements: 1609

## Final requirement classification

| Status | Count |
|---|---:|
| DONE | 117 |
| FIX_CODE | 0 |
| FIX_MAPPING_OR_PROOF | 1454 |
| BLOCKED_BY_NORMATIVE_SOURCE | 38 |
| **TOTAL** | **1609** |

`DONE` is deliberately strict. Only 117 rows retain complete requirement-level trace and belong to messages that pass the fresh 2026 runtime serialization/validation probe. Twenty-four historical `FULL_TRACE` rows were downgraded because their message currently fails that fresh runtime probe.

## Source inventory

- Files scanned recursively in `/Users/tema/Documents/Work/Документы_xml`: 59.
- SHA256 calculated: 59 files.
- `ОП_22.pdf`: primary OP22 source; 1035 pages; SHA256 `99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3`.
- `52 решение.pdf` is actually Decision №152 dated 10.09.2019 and is the local source for P.CLS.024. It was not renamed.
- Decision №92 + №148 make the old blanket “P.CLS.027 payload missing” conclusion obsolete.
- Decision №184 confirms P.P.SP.02.CLS.001.
- WIPO Standard ST.3 is authoritative for fields explicitly requiring `codeListId = "ВОИС ST.3"`.
- Decision №89 is present, but no direct current OP22 requirement-level applicability was proven; it was not applied retroactively.

## Classifier re-verification

| Metric | Before | After |
|---|---:|---:|
| CLASSIFIER blockers | 61 | 14 |
| Source conflicts | 7 | 7 |

P.CLS.027 old blocker rows split into 40 exact matches, 8 no-exact-match cases, 6 semantic ambiguities, and 3 stale/no-usage-row blocker classifications. P.P.SP.02.CLS.001 contributes 3 old source blockers now reclassified because Decision №184 is present. The old ST.3/P.P.SP.03.CLS.001 source blocker is also reclassified because the WIPO standard is present.

The historical MSG048 direction mapping was corrected in the new REVERIFY evidence: Decision №92 p.11 gives `07245 = collective → ordinary` and `07250 = ordinary → collective`, so `P.SP.02.MSG.048:66:4/5` uses `07250`. Historical CSVs were kept unchanged as history.

## Remaining normative blockers

- Classifier semantic/no-exact-match: 14 requirements.
- External registry contracts: 11 requirements.
- XSD/model source conflicts: 7 requirements.
- Other normative ambiguity: 6 requirements.
- Total `BLOCKED_BY_NORMATIVE_SOURCE`: 38.

All 7 historical source conflicts remain open because the required physical XSD/model payloads are still absent. No QName/path side was chosen by similarity.

## XSD and model status

OP22 lists exactly these relevant structures at p.828: R.006, R.010, R.IP.SP.02.002, R.IP.SP.02.007, R.IP.SP.02.008, R.IP.SP.03.003. No physical XSD files were found locally for any of them.

Confirmed structure roots from OP22/local runtime evidence include:

- R.IP.SP.02.002 v1.0.0 → `TrademarkRegistrationDetails`.
- R.IP.SP.02.007 v1.0.0 → `TrademarkRegisterDetails`.
- R.IP.SP.02.008 v1.0.0 → `TrademarkRegisterRequestDetails`.
- R.IP.SP.03.003 v1.0.0 → `IPDutyDetails`.
- R.010 uses placeholder version Y.Y.Y → `GenericEDocDetails`.
- R.006 uses placeholder version Y.Y.Y → `ProcessingResultDetails`.

Missing imported model packages: EEC_M_ComplexDataObjects, EEC_M_SimpleDataObjects, EEC_M_IP_ComplexDataObjects, EEC_M_IP_SimpleDataObjects. Exact X.X.X/Y.Y.Y/Z.Z.Z numeric versions remain unresolved.

## MSG001 policy recheck

Before:

- REQUIRED 20
- OPTIONAL 145
- FORBIDDEN 147
- FIXED 16
- CONDITIONAL 76

After source-confirmed P.CLS.027 resolution:

- REQUIRED 20
- OPTIONAL 145
- FORBIDDEN 148
- FIXED 17
- CONDITIONAL 74

Two old conditions are resolved: root `IPDocKindCode` is fixed to `07220`, and root `IPDocKindName` is forbidden. The 74 remaining conditional fields are rechecked row-by-row in `OP22_MSG001_POLICY_RECHECK.csv`; they are retained only for runtime/cardinality or still-unresolved source semantics.

## Safe production/test changes

- MSG001 root `IPDocKindCode` fixed to `07220` with source-backed policy.
- MSG001 root `IPDocKindName` forbidden for that classifier-resolved branch.
- P.CLS.027 local normative data includes and regression-tests `07250` with the correct transformation direction.
- Stale OP22-specific GUI test expectation updated from `Условно` to the fixed `07220` policy already displayed by the application.

No speculative classifier value, QName, namespace, version, XSD fact, external registry contract, or normative behavior was added.

## Missing-document rebuild

- Total artifacts still to find: 22.
- P0: 10.
- P1: 9.
- P2: 3.

P0 is dominated by 6 physical XSDs and 4 imported model packages. P1 contains P.CLS.051/Decision №53, Decision №190 as a second-order Decision №89 dependency, four external registry contracts, and three unresolved normative semantics. P2 records the exact numeric version metadata hidden behind X.X.X/Y.Y.Y/Z.Z.Z placeholders.

## Metrics

- NEW_DOCUMENTS_DISCOVERED: 9
- NEW_SOURCES_USED: 8
- OLD_BLOCKERS_RESOLVED_BY_NEW_SOURCE: 44
- OLD_BLOCKERS_RECLASSIFIED_OUT_OF_SOURCE_BLOCKED: 47
- SOURCE_CONFLICTS_RESOLVED: 0
- SOURCE_CONFLICTS_REMAINING: 7
- MSG001_CONDITIONAL_RESOLVED: 2
- MSG001_CONDITIONAL_REMAINING: 74
- NORMATIVE_DATA_INVENTED: 0

## KB updates recommended, not applied

The Knowledge Base should eventually be refreshed to reflect the local Decision №92/148 P.CLS.027 source, Decision №184, WIPO ST.3, Decision №152 hidden behind `52 решение.pdf`, the 2026 source inventory, and the stale historical 111/111 runtime matrix. `knowledge_base/**` was intentionally not changed in this task.

## Next manual source check

Start with `P.SP.02.MSG.003:37:4` and `P.SP.02.MSG.003:37:5`. Current local P.CLS.027 review yields an unresolved `09030 | 09035` ambiguity. Manually reconcile Table 37 wording against the exact Decision №92/148 classifier entries before changing production or proof status.
