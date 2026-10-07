# OP23 / P.SP.03 — POST-WAVE2 RECONCILIATION

Date: 2026-10-07. Scope: read-only reconciliation of the current workspace after WAVE 2. Product code, tests, engine, GUI and Knowledge Base were not edited by this audit.

## STATUS

`PARTIAL_RECONCILED_WITH_FINDINGS`.

The historical 710-requirement inventory and batch reproduction remain arithmetically stable: 608 old-SAFE requirements are split B1/B2/B3/B4 = 162/214/159/73, and 102 baseline blocked requirements remain outside that historical SAFE cohort (44 classifier + 39 external registry + 18 source conflict + 1 missing normative structure/XSD).

The live workspace does **not** support the expected statement `B1 = 162/162 CLOSED_CONFIRMED`. Two B1 requirements, `P.SP.03.MSG.023.REQ.019` and `P.SP.03.MSG.024.REQ.019`, have live `mapping_status: PARTIAL`: current rules prove binary presence and allowed `mediaTypeCode`, but do not implement/prove the normative binary-size limit `<= 5 MB`. Therefore current B1 closure is **160/162**, with 2 `MAPPED_BUT_SEMANTICS_NEED_REVIEW`.

## LIVE RECONCILIATION

- TOTAL canonical requirements: **710**.
- Historical SAFE cohort audited: **608**.
- Baseline blocked outside SAFE: **102**.
- Current canonical SAFE requirements with at least one production `structured_rule`: **474**.
- Current canonical SAFE requirements with no production structured rule: **134**.
- Existing mapped rules with complete real-XML proof and no known semantic-partial marker: **330**.
- Existing mapped rules needing requirement-specific test proof: **142**.
- Existing mapped rules needing runtime proof after test proof: **0**.
- Existing mapped rules whose semantics remain partial: **2**.
- Actual new implementation queue: **126**.
- Evidence-blocked requirements found inside the old SAFE map: **8**.

### Verdict distribution

| Verdict | Count |
|---|---:|
| CLOSED_CONFIRMED | 160 |
| MAPPED_PROOF_COMPLETE | 170 |
| MAPPED_TEST_PROOF_MISSING | 142 |
| MAPPED_RUNTIME_PROOF_MISSING | 0 |
| MAPPED_BUT_SEMANTICS_NEED_REVIEW | 2 |
| NOT_MAPPED | 126 |
| EVIDENCE_BLOCKED | 8 |
| **TOTAL SAFE cohort** | **608** |

## BATCH COUNTS

| Batch | TOTAL | RULE_ALREADY_EXISTS | FULL_PROOF | TEST_PROOF_MISSING | RUNTIME_PROOF_MISSING | ACTUAL_NEW_IMPLEMENTATION_REQUIRED | EVIDENCE_BLOCKED | SEMANTICS_NEED_REVIEW |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B1 | 162 | 162 | 160 | 0 | 0 | 0 | 0 | 2 |
| B2 | 214 | 166 | 101 | 65 | 0 | 40 | 8 | 0 |
| B3 | 159 | 107 | 57 | 50 | 0 | 52 | 0 | 0 |
| B4 | 73 | 39 | 12 | 27 | 0 | 34 | 0 | 0 |


## REQ.004 / REQ.005 SPECIAL CASE

The supplied special audit establishes for MSG.022 REQ.004/.005: structure `R.IP.SP.03.003` and the prefixed fields are confirmed, while the exact `ipsdo` namespace still requires the missing XSD and classifier payload/state is unknown. Full implementation is therefore not justified.

Current canonical inheritance extends that blocker to **8** old-SAFE requirements:

- `P.SP.03.MSG.021.REQ.004/.005` — direct Table 25 semantics.
- `P.SP.03.MSG.022.REQ.004/.005` — Table 26 inherits requirements 1–6 from Table 25.
- `P.SP.03.MSG.023.REQ.004/.005` — Table 27 inherits requirements 1–6 from Table 25.
- `P.SP.03.MSG.024.REQ.004/.005` — Table 28 inherits requirements 1–19 from Table 27; the current safe-map already records `INHERITED_SEMANTIC_SOURCE` back to MSG.021 REQ.004/.005.

All eight are `EVIDENCE_BLOCKED`, not `NOT_MAPPED` implementation work and not closed.

## TRACE CHECK

- Canonical requirement inventory: **710 unique IDs**, duplicates 0.
- Live structured rules: **598 rule objects** mapped onto **474 canonical IDs**.
- Structured rule canonical bases outside the 710 inventory: **0**.
- Mapped SAFE canonical requirements whose live rule source IDs fail to intersect the canonical batch trace or whose source status is not CONFIRMED: **0**.
- Inherited requirements are evaluated by canonical expanded REQ IDs. Range-row business-rule numbering is not treated as canonical truth.
- MSG.014 collision check: live `P.SP.03.MSG.014.REQ.005` points to Table 23 range `3-34` plus inherited `MSG.013` item 5; it is not confused with business-rule row `REQ.005`, whose `requirement_code` is source item 36. `REQ.035` remains the separate source-conflict requirement for Table 23 item 35.
- MSG.022 collision check: canonical `REQ.001..REQ.009` mappings use expanded canonical numbering. For example canonical `REQ.002` traces to Table 26 range `1-6` + MSG.021 item 2, while canonical `REQ.007.*` traces to local Table 26 item 7. Old four-row business IDs are not used as canonical truth.

## PROOF POLICY

A green aggregate suite is not treated as requirement-specific proof by itself. `FULL_PROOF` requires a live production rule plus recorded positive and negative real-XML proof for that canonical requirement, and the current OP23 suite must still pass. Current verification: `634 passed, 27 subtests passed`.

For the 142 live mappings without requirement-specific recorded positive/negative proof, the verdict remains `MAPPED_TEST_PROOF_MISSING`. No item was promoted merely because another test exercised the same message or because the aggregate suite is green.

## NEXT WORK

- New implementation required in B2/B3/B4: **126** requirements (`B2=40`, `B3=52`, `B4=34`).
- Existing mappings needing requirement-specific proof: **142** (`B2=65`, `B3=50`, `B4=27`).
- B1 semantic completion/review: **2** REQ.019 rules; this audit does not modify B1.
- Evidence blockers inside old SAFE: **8**; do not place them in an implementation queue until evidence is obtained.

## FINAL

STATUS: PARTIAL_RECONCILED_WITH_FINDINGS

TOTAL: 710
SAFE: 608
BLOCKED: 102

B1_TOTAL: 162
B1_CLOSED: 160

B2_TOTAL: 214
B2_ALREADY_MAPPED: 166
B2_FULL_PROOF: 101
B2_NEEDS_PROOF: 65
B2_NEEDS_IMPLEMENTATION: 40

B3_TOTAL: 159
B3_ALREADY_MAPPED: 107
B3_FULL_PROOF: 57
B3_NEEDS_PROOF: 50
B3_NEEDS_IMPLEMENTATION: 52

B4_TOTAL: 73
B4_ALREADY_MAPPED: 39
B4_FULL_PROOF: 12
B4_NEEDS_PROOF: 27
B4_NEEDS_IMPLEMENTATION: 34

EVIDENCE_BLOCKED_INSIDE_OLD_SAFE_MAP: 8

REQ004_REQ005_STATUS: EVIDENCE_BLOCKED for MSG.021-.024 REQ.004/.005 (8 canonical requirements; MSG.024 is transitive inheritance discovered by this reconciliation)

BROKEN_RULE_IDS: 0
BROKEN_SOURCE_REFS: 0

NEXT_SAFE_IMPLEMENTATION_QUEUE: 126

FILES_CHANGED_OUTSIDE_REPORTS: 0
