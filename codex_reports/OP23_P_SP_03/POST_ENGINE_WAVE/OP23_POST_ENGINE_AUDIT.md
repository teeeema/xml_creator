# OP23 P.SP.03 — POST-ENGINE FOLLOW-UP

## Scope and authoritative starting state

This wave reviewed exactly the eight post-engine candidates requested by the user. Starting strict state: `TOTAL=710`, `MAPPED=501`, `FULL_PROOF=499`, `PARTIAL=2`, `BLOCKED=209`. Writes were limited to `P.SP.03_OP_23/message_rules/**`, `P.SP.03_OP_23/tests/**`, and this report directory. No shared-engine, Knowledge Base, or other OP package file was edited by this follow-up.

Pre-existing dirty work from parallel tasks was preserved. No reset, clean, stash, checkout, commit, merge, or push was performed.

## DATE targets

### P.SP.03.MSG.007.REQ.036 — CLOSED_FULL_PROOF

- Normative source: `ОП_23.pdf`, p.397, table 21, item 36, source ref `23OP-RULE-P.SP.03.MSG.007-36`.
- Confirmed structure: `R.IP.SP.03.002`.
- Confirmed field: `ipcdo:ApellationOfOriginRegisterItemDetails/ipcdo:ApellationOfOriginEAEURightDetails/csdo:DocValidityDate`, datatype `bdt:DateType`.
- Production rule now compares position 1 (old/original) with position 2 (new/changed) using `LT` and `value_type: DATE`.
- Positive real XML proof: old date earlier than new date passes.
- Negative real XML proof: equal dates fail with `P.SP.03.MSG.007.REQ.036`.

### P.SP.03.MSG.014.REQ.039 — CLOSED_FULL_PROOF

- Normative source: `ОП_23.pdf`, p.278, table 23, item 39, source ref `23OP-RULE-P.SP.03.MSG.014-39`.
- Confirmed structure and field are the same `R.IP.SP.03.002` `DocValidityDate` path above.
- Production rule compares position 1 with position 2 using `LT` and `value_type: DATE`.
- Positive real XML proof passes; equal-date negative XML fails with the exact rule ID.

The first full `test_b1_production.py` run exposed 20 old positive `MSG.014` fixtures that duplicated the first register item and therefore gave both instances the same `DocValidityDate`. That fixture state became invalid once REQ.039 was executable. The fixture was corrected so the changed/new register item has a later date. The affected subset then passed `40/40`, and the complete B1 file passed `633/633`.

## Secondary review — other six candidates

| Requirement | Classification | Result |
| --- | --- | --- |
| `P.SP.03.MSG.004.REQ.007` | `ENGINE_SOLVED_BUT_SOURCE_BLOCKED` | Conditional cross-instance capability is available, but the authoritative task state says source evidence remains a blocker and no new closure-grade source was found. Not implemented. |
| `P.SP.03.MSG.004.REQ.034` | `ENGINE_SOLVED_BUT_CLASSIFIER_BLOCKED` | Set equivalence is now available. The application condition still depends on authoritative Decision No. 92 IP document-kind classifier evidence/code-name mapping. Not implemented. |
| `P.SP.03.MSG.011.REQ.007` | `ENGINE_SOLVED_BUT_SOURCE_BLOCKED` | Conditional cross-instance capability is available, but the known source blocker remains. Not implemented. |
| `P.SP.03.MSG.011.REQ.034` | `ENGINE_SOLVED_BUT_CLASSIFIER_BLOCKED` | Set equivalence is available; authoritative classifier evidence is still missing. Not implemented. |
| `P.SP.03.MSG.023.REQ.019` | `ENGINE_SOLVED_BUT_THRESHOLD_AMBIGUOUS` | `ОП_23.pdf` p.286 confirms `<= 5 Мб`; decoded-byte length is available, but the source does not resolve decimal vs binary megabytes. Remains `PARTIAL`. |
| `P.SP.03.MSG.024.REQ.019` | `ENGINE_SOLVED_BUT_THRESHOLD_AMBIGUOUS` | `ОП_23.pdf` p.287 inherits item 19 from table 27; the same byte-multiplier ambiguity remains. Remains `PARTIAL`. |

No `5 MB` byte threshold was hardcoded. Neither `5,000,000` nor `5,242,880` bytes is treated as normative without an authoritative source resolving the multiplier.

## Strict closure accounting

Only the two DATE requirements changed strict state:

- `MAPPED: 501 -> 503`
- `FULL_PROOF: 499 -> 501`
- `PARTIAL: 2 -> 2`
- `BLOCKED: 209 -> 207`

The four MSG.004/MSG.011 candidates remain blocked by source/classifier evidence. The two 5 MB requirements remain partial.

## Verification

- Focused DATE proof: `2 passed, 42 deselected`.
- Affected MSG.014 fixture subset after correction: `40 passed, 593 deselected`.
- `test_b1_production.py`: `633 passed`.
- `test_next_implementation.py`: `44 passed`.
- Full `P.SP.03_OP_23/tests`: `680 passed, 27 subtests passed`.
- Relevant shared-engine DATE tests: `2 passed, 16 deselected`.
- `git diff --check`: PASS (exit 0, no output).

## Remaining closure blockers

1. Obtain closure-grade source evidence for `MSG.004.REQ.007` and `MSG.011.REQ.007` before production mapping.
2. Obtain the authoritative Decision No. 92 classifier snapshot/version and required code/name mapping before closing `MSG.004.REQ.034` and `MSG.011.REQ.034`.
3. Obtain an authoritative definition of `5 Мб` for `MSG.023.REQ.019` and `MSG.024.REQ.019` before adding the decoded-byte threshold rule.

`graphify update .` was intentionally not run because it would write `graphify-out/**`, outside the user-approved write scope.
