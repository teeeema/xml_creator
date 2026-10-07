# WAVE 2 — Mapping report

## MAPPING_RECONSTRUCTION

TOTAL_CANDIDATES: 710
B1: 162
B2: 214
B3: 159
B4: 73
BLOCKED: 102
UNCLASSIFIED: 0

EXPECTED_IF_REPRODUCIBLE: B1=162, B2=214, B3=159, B4=73

MAPPING_REPRODUCED: **YES**

608 safe candidates are reproduced from `OP23_SAFE_IMPLEMENTATION_BATCH_MAP.csv`; the remaining 102 of 710 are the existing non-safe groups: 44 classifier, 39 external registry, 18 source conflict, 1 missing normative data. No blocked row was promoted into B1 to reach the target count.

Consistency checks: 608 unique mapping rows, no duplicate canonical requirement IDs, and the B1 set exactly matches `OP23_B1_REQUIREMENT_IDS.txt`. All 162 B1 IDs currently have production rule wiring.

## B1 by message

| MSG | B1 cases |
|---|---:|
| P.SP.03.MSG.001 | 18 |
| P.SP.03.MSG.003 | 18 |
| P.SP.03.MSG.004 | 1 |
| P.SP.03.MSG.005 | 18 |
| P.SP.03.MSG.006 | 2 |
| P.SP.03.MSG.007 | 3 |
| P.SP.03.MSG.008 | 3 |
| P.SP.03.MSG.009 | 18 |
| P.SP.03.MSG.010 | 17 |
| P.SP.03.MSG.011 | 1 |
| P.SP.03.MSG.012 | 15 |
| P.SP.03.MSG.013 | 4 |
| P.SP.03.MSG.014 | 5 |
| P.SP.03.MSG.015 | 1 |
| P.SP.03.MSG.016 | 1 |
| P.SP.03.MSG.018 | 2 |
| P.SP.03.MSG.021 | 4 |
| P.SP.03.MSG.022 | 6 |
| P.SP.03.MSG.023 | 11 |
| P.SP.03.MSG.024 | 11 |
| P.SP.03.MSG.025 | 3 |

## Exact WAVE 2 set

The exact 162-row registry is `WAVE_2_B1_CASES.csv`. Each row contains CASE_ID, PROCESS, PRC, TRN, MSG, REQ, STRUCTURE, QName/path, rule type, expected valid/invalid behavior, executable status, normative source/version/page/table when present in the current confirmed source record, source refs, and implementation layer.

## Classification basis

B1 is limited to simple presence/comparison behavior already assigned by the deterministic safe batch map. B2/B3/B4 rows and the 102 classifier/external/source blockers remain outside WAVE 2. Production code is not used as normative proof; source metadata comes from the existing OP23 canonical requirement/source records.
