# KB Final Sync Audit

STATUS: PASS

KB_FINAL_SYNC: COMPLETE
READY_FOR_FINAL_GATE: YES

The reconciliation preserves the architecture `SOURCE -> KNOWLEDGE -> PROJECT_STATE`. Normative/source fields were not promoted from production state. Unknown QName/model/classifier/registry facts remain unresolved or blocked.

## Canonical state

- Requirements synchronized: **2894 / 2894**
- FULL_PROOF total: **2029**
- Open/non-full project-state requirements: **865**
- OP32 process knowledge: normative OPR count **46**; package exposes **44**; missing `P.MM.06.OPR.007` and `P.MM.06.OPR.008`; five structure roots are confirmed, `R.006`/`R.007` remain unresolved; child payload QName/path remains unresolved for 170/170.

## Integrity

- Duplicate canonical IDs: **0**
- Missing requirement files: **0**
- Broken canonical relations: **0**
- Broken internal links: **0**
- Stale source references: **0**
- Stale PROJECT_STATE references: **0**
- Semantic stale-state rows fixed: **893**
- Missing evidence files referenced by current PROJECT_STATE: **0**

## Graph

- Nodes: **39613**
- Edges: **49882**
- Status: **UPDATED**
- Visualization note: graph.html visualization remains stale because the aggregated community view exceeds the 5000-node HTML limit.

## Reproducibility

- Status: **PASS**
- New fingerprint: `ae3376e0b6f83700da6465d24d529447b921f3782d5e8bfe1463feb25f8e5aa5`

## Safety boundary

- Production changed by this sync: **0**
- Engine changed by this sync: **0**
- GUI changed by this sync: **0**
- Pre-existing/parallel non-KB dirty entries preserved: **104**
- Relevant production/test/engine dirty files preserved: **36**

See `KB_FINAL_SYNC_REQUIREMENT_STATE.csv` for the 2894-row reconciliation and `KB_FINAL_SYNC_STALE_STATE_FIXED.csv` for semantic corrections.
