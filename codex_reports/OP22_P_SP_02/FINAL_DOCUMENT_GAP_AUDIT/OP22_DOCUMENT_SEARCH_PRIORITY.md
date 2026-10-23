# OP22 / P.SP.02 — Document Search Priority

Current basis: **1609 requirements = 117 DONE + 1454 PROOF_ONLY (`FIX_MAPPING_OR_PROOF`) + 38 source-blocked**. The 38 source blockers are requirement-level. The 21 items below are distinct external artifacts/materials and are not additive to 38.

## P0 — schema/model artifacts

| Artifact | Expected number | Why needed | Direct current blockers | OP22 reference | Best search query |
|---|---:|---|---:|---|---|
| `EEC_R_ProcessingResultDetails_vY.Y.Y.xsd` (R.006) | UNKNOWN | Physical XSD required for complete schema proof; exact Y.Y.Y unresolved | 0 | pp.829-830 | `EEC_R_ProcessingResultDetails_vY.Y.Y.xsd` |
| `EEC_R_GenericEDocDetails_vY.Y.Y.xsd` (R.010) | UNKNOWN | Resolves three active R.010 source conflicts and schema proof | 3 | pp.834-835 | `EEC_R_GenericEDocDetails_vY.Y.Y.xsd` |
| `EEC_R_IP_SP_02_TrademarkRegistrationDetails_v1.0.0.xsd` | n/a | Resolves three active structural conflicts; core OP22 payload schema | 3 | pp.838-839 | exact filename |
| `EEC_R_IP_SP_02_TrademarkRegisterDetails_v1.0.0.xsd` | n/a | Complete schema proof for R.IP.SP.02.007 | 0 | pp.929-930 | exact filename |
| `EEC_R_IP_SP_02_TrademarkRegisterRequestDetails_v1.0.0.xsd` | n/a | Resolves MSG.024 REQ 2 conflict | 1 | pp.985-986 | exact filename |
| `EEC_R_IP_SP_03_IPDutyDetails_v1.0.0.xsd` | n/a | Complete schema proof for referenced structure | 0 | pp.993-994 | exact filename |
| `EEC_M_ComplexDataObjects` | UNKNOWN | Common complex model imported by OP22 structures | 0 | imports on pp.830/835/839/929-930/986/994 | `EEC_M_ComplexDataObjects X.X.X EAEU` |
| `EEC_M_SimpleDataObjects` | UNKNOWN | Common simple model imported by OP22 structures | 0 | same import pages | `EEC_M_SimpleDataObjects X.X.X EAEU` |
| `EEC_M_IP_ComplexDataObjects` | UNKNOWN | Subject model required for exact IP hierarchy; two current direct links | 2 | IP structure imports | `EEC_M_IP_ComplexDataObjects Z.Z.Z EAEU` |
| `EEC_M_IP_SimpleDataObjects` | UNKNOWN | Subject simple model required for full IP schema proof | 0 | IP structure imports | `EEC_M_IP_SimpleDataObjects Z.Z.Z EAEU` |

## P1 — classifier, contracts and clarifications

- **P.CLS.051 / Decision №53 dated 02.04.2019** — classifier “классификатор видов документов, удостоверяющих личность”, registry code **2053**. OP22 p.70 directly states application under Decision №53. Current blocked requirements: **0**; the referenced source itself is missing locally.
- **Commission application resource contract** — blocks 2 requirements: MSG.012 REQ 32 and MSG.014 REQ 2.
- **Unified trademark register contract** — blocks 2 requirements: MSG.021 REQ 22/23.
- **National application resource contract** — blocks 3 requirements: MSG.043 REQ 31, MSG.044 REQ 4, MSG.045 REQ 2.
- **National patent trademark resource contract** — blocks 4 requirements: MSG.052 REQ 21, MSG.053 REQ 21/22/23.
- **IPPartyKindCode semantic authority** — affects 3 ambiguity rows using AP/AS. OP22 literals are present; a separate authoritative code-list/model source may still be required for domain proof.
- **MSG.038 Table 56 REQ 2 exact classifier mapping** — affects 1 row. P.CLS.027 exists locally; the long document-kind label still lacks a proven exact classifier match.
- **Tables 78/79 REQ 5 scope clarification** — affects 2 rows; the clause is exactly “другие реквизиты не заполняются”.

## P2 — exact version metadata

- R.006 / R.010 exact **Y.Y.Y**.
- Common model packages exact **X.X.X**.
- IP model packages exact **Z.Z.Z**.

## Already present; do not search again

OP22 package / Decision №14 embedded in `ОП_22.pdf`; Decisions №92 and №148 for P.CLS.027; Decision №184 for P.P.SP.02.CLS.001; WIPO ST.3; Decision №192 for P.CLS.008; Decisions №378, №54, №152 (the local file named `52 решение.pdf` is actually №152), №89, and Decision №5. Decision №89 is present but is not a direct resolver of a current OP22 blocker.
