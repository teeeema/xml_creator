# OP22 / P.SP.02 — Final Document Gap Audit

## Status

**AUDIT COMPLETE — SOURCE/MATERIAL GAP INVENTORY ONLY.** No production code, tests, knowledge base, mappings, blocker statuses, or production requirement statuses were modified.

## Baseline

- OP22_TOTAL_REQUIREMENTS: **1609**
- DONE: **117**
- PROOF_ONLY_TOTAL: **1454** (`FIX_MAPPING_OR_PROOF`)
- ACTUAL_SOURCE_BLOCKED_REQUIREMENTS: **38**
- Split of 38: **7 SOURCE_CONFLICT + 20 NORMATIVE_AMBIGUITY + 11 EXTERNAL_REGISTRY**

The 1454 rows are not missing-document rows. They need mapping/test/runtime/XML proof with the sources already available.

## Distinct external material gaps

`ACTUAL_EXTERNAL_MATERIAL_GAPS_TOTAL = 21` on an artifact/material basis:

- 6 missing physical XSDs;
- 4 missing common/IP model packages;
- 1 missing classifier source (P.CLS.051 / Decision №53);
- 4 missing external-registry technical contracts;
- 3 unresolved semantic source/official clarification artifacts;
- 3 unresolved exact-version metadata families.

This 21 is **not additive** to the 38 blocked requirements. One artifact can resolve multiple requirement rows; some schema artifacts have zero direct current blocker rows but are still required for complete schema-level proof.

## P.CLS.051

OP22 p.70 identifies **P.CLS.051 — “классификатор видов документов, удостоверяющих личность”**, registry code **2053**, and says it is applied according to **Decision of the EEC Collegium dated 2 April 2019 №53**. Decision №53 / the classifier payload is absent in the current local normative set. Current reverify shows **NO_CANONICAL_OLD85_REQUIREMENT_LINK**, therefore `requirements_blocked_count = 0`. It is a real referenced artifact gap, but it is not part of the 38 requirement blockers.

## Missing XSDs

1. `EEC_R_ProcessingResultDetails_vY.Y.Y.xsd` — R.006, namespace `urn:EEC:R:ProcessingResultDetails:vY.Y.Y`, root `ProcessingResultDetails`, OP22 p.829; Y.Y.Y unresolved.
2. `EEC_R_GenericEDocDetails_vY.Y.Y.xsd` — R.010, namespace `urn:EEC:R:GenericEDocDetails:vY.Y.Y`, root `GenericEDocDetails`, p.834; Y.Y.Y unresolved.
3. `EEC_R_IP_SP_02_TrademarkRegistrationDetails_v1.0.0.xsd` — R.IP.SP.02.002, namespace `urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0`, root `TrademarkRegistrationDetails`, p.838.
4. `EEC_R_IP_SP_02_TrademarkRegisterDetails_v1.0.0.xsd` — R.IP.SP.02.007, namespace `urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0`, root `TrademarkRegisterDetails`, p.929.
5. `EEC_R_IP_SP_02_TrademarkRegisterRequestDetails_v1.0.0.xsd` — R.IP.SP.02.008, namespace `urn:EEC:R:IP:SP:02:TrademarkRegisterRequestDetails:v1.0.0`, root `TrademarkRegisterRequestDetails`, p.985.
6. `EEC_R_IP_SP_03_IPDutyDetails_v1.0.0.xsd` — R.IP.SP.03.003, namespace `urn:EEC:R:IP:SP:03:IPDutyDetails:v1.0.0`, root `IPDutyDetails`, p.993.

## Missing model packages

- `EEC_M_ComplexDataObjects` — namespace pattern `urn:EEC:M:ComplexDataObjects:vX.X.X`; exact X.X.X unresolved.
- `EEC_M_SimpleDataObjects` — `urn:EEC:M:SimpleDataObjects:vX.X.X`; exact X.X.X unresolved.
- `EEC_M_IP_ComplexDataObjects` — `urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z`; exact Z.Z.Z unresolved; 2 direct current blocker links.
- `EEC_M_IP_SimpleDataObjects` — `urn:EEC:M:IP:SimpleDataObjects:vZ.Z.Z`; exact Z.Z.Z unresolved.

## Seven source conflicts

| MSG / REQ | Business page | Structure evidence | Needed resolver |
|---|---:|---|---|
| MSG.001 / REQ 27 | 520 | R.IP.SP.02.002 pp.869/871 | R.IP.SP.02.002 XSD; then clarification if contradiction remains |
| MSG.005 / REQ 33 | 537 | pp.887/898 | R.IP.SP.02.002 XSD + exact IP model |
| MSG.024 / REQ 2 | 577 | R.IP.SP.02.008 | R.IP.SP.02.008 XSD |
| MSG.029 / REQ 32 | **726** | pp.872/876 | R.IP.SP.02.002 XSD + exact IP model/newer description |
| MSG.031 / REQ 2 | **733** | R.010 | R.010 XSD / exact payload semantics |
| MSG.031 / REQ 30 | 734 | R.010 + IP structure | R.010 XSD + exact IP model |
| MSG.031 / REQ 32 | 734 | R.010 + IP structure | R.010 XSD + exact IP model / clarification |

The corrected active pages above supersede stale inherited provenance in the requirement reverify for MSG.029 REQ 32 and MSG.031 REQ 2.

## Twenty normative ambiguities

Fourteen are P.CLS.027 semantic/no-exact-match rows: MSG.003 REQ 4/5; MSG.004 REQ 2/3; MSG.005 REQ 2/3; MSG.014 REQ 4/5; MSG.045 REQ 4/5; MSG.061 REQ 2/3; MSG.062 REQ 2/3. **P.CLS.027 is present locally**, so these are not `CLASSIFIER_MISSING`.

The other six are: MSG.001 REQ 13 (p.515), MSG.028 REQ 13 (p.716), MSG.045 REQ 30 (p.776) for IPPartyKind AP/AS semantic authority; MSG.038 REQ 2 on corrected p.754 for the long priority-document kind; and MSG.059 Table 78 REQ 5 (p.811) plus Table 79 REQ 5 (p.812), where “другие реквизиты не заполняются” has unresolved scope. Exact row-level details are in `OP22_NORMATIVE_AMBIGUITIES.csv`.

## Eleven external-registry requirements

- Commission application resource: MSG.012 REQ 32 p.552; MSG.014 REQ 2 p.555.
- Unified trademark register: MSG.021 REQ 22/23 p.576.
- National application resource: MSG.043 REQ 31 p.769; MSG.044 REQ 4 p.771; MSG.045 REQ 2 p.773.
- National patent trademark resource: MSG.052 REQ 21 p.795; MSG.053 REQ 21 p.799 and REQ 22/23 p.800.

These cannot be closed by static PDF/XSD alone. They require an official lookup/API contract and runtime data source such as a registry snapshot or test environment.

## Already present; do not search again

OP22 / Decision №14 package; Decisions №92 and №148; Decision №184; WIPO ST.3; Decision №192; Decision №378; Decision №54; Decision №152 (the local file named `52 решение.pdf` is actually №152); Decision №89; Decision №5.

## Verification boundary

This was an audit-only task. No code test suite was run because execution tests were not needed to establish the document/source inventory. Verification is limited to current reverify counts, report row/count checks, source-page rechecks, local artifact-presence checks already performed during the audit, and a final Git status/diff scope check.
