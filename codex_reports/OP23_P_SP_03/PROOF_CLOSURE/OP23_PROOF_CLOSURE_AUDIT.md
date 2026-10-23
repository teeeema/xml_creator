# OP23 Proof Closure Audit

STATUS: **COMPLETE_WITH_2_PARTIAL_5MB**

## ROOT_CAUSE

The historical post-WAVE2 reconciliation understated current proof coverage. Of the 142 rows marked `MAPPED_TEST_PROOF_MISSING`, **141 already had requirement-specific positive, negative, real-XML runtime proof for their exact production rule IDs**. Their gap was stale report linkage. The only substantive proof gap was `P.SP.03.MSG.013.REQ.001`, whose two live rules (`.cardinality`, `.resource_kind`) lacked requirement-specific proof.

The latest implementation wave also changed current state after that reconciliation: **27 canonical requirements / 42 structured subrules** were implemented with source-traced rules and positive/negative real-XML runtime proof, moving mapped coverage from **474 to 501**. The other 99 candidates were reclassified as blockers and were not approximated.

## CHANGED_FILES

- `P.SP.03_OP_23/tests/test_b1_production.py` — added one parameterized real-XML proof test for `P.SP.03.MSG.013.REQ.001.cardinality` and `.resource_kind`.
- `codex_reports/OP23_P_SP_03/PROOF_CLOSURE/OP23_PROOF_CLOSURE_MATRIX.csv` — current 710-row strict state.
- `codex_reports/OP23_P_SP_03/PROOF_CLOSURE/OP23_PROOF_CLOSURE_AUDIT.md` — this audit.
- `codex_reports/OP23_P_SP_03/PROOF_CLOSURE/OP23_CURRENT_STRICT_STATE.md` — reconciled totals and blocker split.

Production rules, shared engine, Knowledge Base and other OP files were not changed by this proof-closure session.

## IMPLEMENTATION

### 141 link-only rows

No duplicate tests were added. Each row is recorded as `LINK_ONLY_RESOLVED` and linked to the existing pytest nodeid(s) from the prior direct proof trace. The accepted tests execute real XML extraction and the production validator and assert exact rule-level PASS/failure behavior.

### P.SP.03.MSG.013.REQ.001

Added one parameterized test, `test_msg013_req001_two_items_same_resource_kind_real_xml`, with two cases:

- `.cardinality`: a valid two-item document passes; removing the second `ipcdo:ApellationOfOriginRegisterItemDetails` produces `STRUCTURED_RULE_FAILED` for the exact rule ID.
- `.resource_kind`: a valid two-item document passes; changing the second `ipsdo:ResourceItemKindCode` from the matching value to `AO` produces `STRUCTURED_RULE_FAILED` for the exact rule ID.

The test uses the existing real-XML helpers and production validator. No production mapping was rewritten.

### Latest 27 implementation-wave requirements

Reverified from the current artifacts: all **27 canonical requirements** have runtime-proof rows, covering **42 structured subrules**, and the current `test_next_implementation.py` suite passes all **42** cases. These 27 are included in `FULL_PROOF`.

### B1 5 MB

`P.SP.03.MSG.023.REQ.019` and `P.SP.03.MSG.024.REQ.019` remain `PARTIAL`. Current tests prove binary presence/media type behavior, but the normative decoded `<= 5 MB` constraint is still not closed because generic decoded-byte-length semantics and the exact MB multiplier are unresolved. This session does not depend on any parallel shared-engine work.

## NORMATIVE_BASIS

**CONFIRMED** for `P.SP.03.MSG.013.REQ.001`: ОП_23.pdf, Table 22 item 1, PDF page 261, source ref `23OP-RULE-P.SP.03.MSG.013-1`. The requirement requires exactly two `ipcdo:ApellationOfOriginRegisterItemDetails` instances and equal `ipsdo:ResourceItemKindCode` values between them.

For the two 5 MB rows, the normative threshold is confirmed by OP23 Table 27 item 19 (MSG.023, PDF page 286) and Table 28 inheritance (MSG.024, PDF page 287), but exact byte multiplier semantics remain unresolved, so they are not promoted to full proof.

## STRICT STATE

| State | Count |
|---|---:|
| FULL_PROOF | 357 |
| LINK_ONLY_RESOLVED | 141 |
| NEW_TEST_ADDED | 1 |
| PARTIAL | 2 |
| BLOCKED_SOURCE | 203 |
| BLOCKED_ENGINE | 4 |
| BLOCKED_MULTIPLE | 2 |
| **TOTAL** | **710** |

Strict fully proven total before this reconciliation, including the latest 27 implementation-wave closures but excluding the 141 stale links, the missing MSG.013 test, and the 2 semantic partials: **357**.

Strict fully proven total after reconciliation: **499** = 357 `FULL_PROOF` + 141 `LINK_ONLY_RESOLVED` + 1 `NEW_TEST_ADDED`.

Mapped current: **501** = 499 strict-full + 2 `PARTIAL` 5 MB rows.

Blocked current: **209** = 203 source + 4 engine + 2 multiple.

## VERIFICATION

Executed in the current worktree:

- Focused MSG.013 REQ.001: `python3.13 -m pytest -q -p no:cacheprovider P.SP.03_OP_23/tests/test_b1_production.py::test_msg013_req001_two_items_same_resource_kind_real_xml` → **2 passed**.
- Relevant existing proof suite: `... P.SP.03_OP_23/tests/test_b1_production.py` → **633 passed**.
- Latest 27 requirement proof suite: `... P.SP.03_OP_23/tests/test_next_implementation.py` → **42 passed**.
- Full OP23 suite: `... P.SP.03_OP_23/tests` → **678 passed, 27 subtests passed**.
- `git diff --check` → **PASS**.

The repository instruction to run `graphify update .` after code changes was not executed because this task explicitly authorizes writes only under `P.SP.03_OP_23/tests/**` and `codex_reports/OP23_P_SP_03/PROOF_CLOSURE/**`; updating `graphify-out/**` would exceed the user-authorized write scope.

## REMAINING_ISSUES

- `P.SP.03.MSG.023.REQ.019` — decoded binary `<= 5 MB` semantics remain PARTIAL.
- `P.SP.03.MSG.024.REQ.019` — inherited decoded binary `<= 5 MB` semantics remain PARTIAL.
- 209 blocked requirements remain outside this proof-only scope: 203 source/evidence, 4 engine, 2 combined source+engine.

## PREEXISTING_PARALLEL_CHANGES

The initial worktree already contained parallel changes. This session preserved them. Relevant OP23 entries were:

- `P.SP.03_OP_23/message_rules/P.SP.03.MSG.004.yaml`
- `P.SP.03_OP_23/message_rules/P.SP.03.MSG.006.yaml`
- `P.SP.03_OP_23/message_rules/P.SP.03.MSG.007.yaml`
- `P.SP.03_OP_23/message_rules/P.SP.03.MSG.008.yaml`
- `P.SP.03_OP_23/message_rules/P.SP.03.MSG.011.yaml`
- `P.SP.03_OP_23/message_rules/P.SP.03.MSG.014.yaml`
- `P.SP.03_OP_23/message_rules/P.SP.03.MSG.015.yaml`
- `P.SP.03_OP_23/tests/test_b1_production.py (already modified before this session; this session adds only the MSG.013 REQ.001 proof test)`
- `P.SP.03_OP_23/tests/test_psp03_package.py`
- `P.SP.03_OP_23/tests/test_next_implementation.py (pre-existing untracked parallel-wave test file)`
- `codex_reports/OP23_P_SP_03/NEXT_IMPLEMENTATION/**`
- `codex_reports/OP23_P_SP_03/PROOF_COMPLETION/**`
- `plus unrelated pre-existing OP22/OP26/OP32/OP49 and eaeu_xml/.DS_Store changes visible in initial git status`

During this session, additional parallel shared-engine changes appeared in the worktree that were **not** present in the initial status snapshot: `eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py`, `eaeu_xml/src/eaeu_xml/process_packages/validator.py`, and `eaeu_xml/tests/test_shared_engine_capabilities.py`. This proof-closure session did not edit those files and does not use those in-progress changes to promote the two 5 MB rows or any engine-blocked requirement.
