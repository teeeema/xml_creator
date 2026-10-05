# MSG029_POST_MAINTENANCE_REPORT

STATUS = COMPLETE

ROOT_CAUSE
The only failing regression was a stale isolation assertion in the MSG028 end-to-end test. Before MSG029 received structured_rules, `assert not result029.rule_evaluations` was a valid proxy for isolation. After MSG029 implementation, both MSG028 and MSG029 legitimately produce structured-rule evaluations for the same R.IP.SP.02.002 values, so isolation must be proven by message-specific rule identity instead of absence of neighboring-message evaluations.

STALE_TEST
`P.SP.02_OP_22/tests/test_msg028_end_to_end.py::test_same_r002_values_execute_only_rules_for_requested_message_code`

OLD_SEMANTICS
The test already verified MSG028 and MSG027 rule-id prefixes, then asserted:

`assert not result029.rule_evaluations`

That assertion became stale as soon as MSG029 gained executable structured_rules.

NEW_SEMANTICS
The test now preserves the existing MSG028 and MSG027 checks and additionally proves that:

- MSG029 has rule evaluations;
- every MSG029 evaluation has prefix `P.SP.02.MSG.029.`;
- the MSG028 evaluation set contains no MSG029-prefixed rule ids;
- the MSG029 evaluation set contains no MSG028-prefixed rule ids;
- MSG028 and MSG029 rule-id sets are disjoint.

No production behavior was changed.

CHANGED_FILES
- `P.SP.02_OP_22/tests/test_msg028_end_to_end.py`
  - Replaced only the stale `assert not result029.rule_evaluations` isolation proxy with explicit two-message rule-id isolation assertions.
- `codex_reports/MSG029_POST_MAINTENANCE_REPORT.md`
  - Added this maintenance report as explicitly allowed service output.

MESSAGE_ISOLATION_PROOF
For one extracted R.IP.SP.02.002 value set:

- MSG028 evaluations are present and all rule ids start with `P.SP.02.MSG.028.`;
- MSG029 evaluations are present and all rule ids start with `P.SP.02.MSG.029.`;
- no MSG029-prefixed rule id appears in the MSG028 evaluation set;
- no MSG028-prefixed rule id appears in the MSG029 evaluation set;
- the two rule-id sets are disjoint;
- the pre-existing MSG027 prefix assertion remains unchanged and still passes.

DIRECT_TEST
Command:
`pytest -q P.SP.02_OP_22/tests/test_msg028_end_to_end.py::test_same_r002_values_execute_only_rules_for_requested_message_code`

Result:
`1 passed in 0.13s`

MSG028_TESTS
Command:
`pytest -q P.SP.02_OP_22/tests/test_msg028_*.py`

Result:
`113 passed in 3.05s`

MSG029_TESTS
Command:
`pytest -q P.SP.02_OP_22/tests/test_msg029_*.py`

Result:
`84 passed in 1.92s`

MSG027_TESTS
Command:
`pytest -q P.SP.02_OP_22/tests/test_msg027_*.py`

Result:
`96 passed in 2.29s`

MSG020_024_REGRESSION
Command:
`pytest -q P.SP.02_OP_22/tests/test_msg02[0-4]_*.py`

Result:
`148 passed in 3.47s`

PSP02_TESTS
Command:
`pytest -q P.SP.02_OP_22/tests`

Result:
`1049 passed in 31.92s`

EAEU_XML_TESTS
Command:
`pytest -q eaeu_xml/tests`

Result:
`265 passed, 43 skipped, 1042 subtests passed in 2.38s`

ROOT_TESTS
Command:
`pytest -q`

Result:
`1438 passed, 43 skipped, 1152 subtests passed in 40.61s`

Root regression is fully green with 0 failed.

PROTECTED_FILES
The following six files were hashed and stat'ed before the maintenance edit, then checked again after all tests. SHA-256 and mtime values were identical before and after:

| File | SHA-256 | mtime epoch |
| --- | --- | ---: |
| `P.SP.02_OP_22/message_rules/P.SP.02.MSG.029.yaml` | `485cf7e7f21f827ec0f4f3f4c7db555b956957c20aca97feeaa7bee361b93cfe` | 1790755412 |
| `P.SP.02_OP_22/message_rules/P.SP.02.MSG.028.yaml` | `d22fa7c9a4dd8dfd6185dadf845ddd645a78d907a8b1ddbd7fa8f1b54c49d7f6` | 1790252958 |
| `eaeu_xml/src/eaeu_xml/process_packages/body.py` | `fa48d5724426f19d1555db2e9b36471fe241a6c100e0c465e98e7c43d795353c` | 1790246637 |
| `eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py` | `4779a799a4783020751101bc536562500c9da5c52cae3c6e78cdbe0c2c4b3da4` | 1790243780 |
| `eaeu_xml/src/eaeu_xml/process_packages/engine.py` | `01e1ef79e87cc6369cd43bddad3db8b1c76d5159a001d9f7b784bd29c878d7d9` | 1789732904 |
| `eaeu_xml/src/eaeu_xml/process_packages/validator.py` | `2f7865177055c4745a425f664f804d3a9542621eebb1d7590d827dccefe97bdc` | 1789732904 |

Protected-file verdict: unchanged.

PREEXISTING_CHANGES
The repository was already dirty before this maintenance batch. The pre-edit status contained pre-existing tracked changes to AGENTS.md, multiple P.SP.02 message-rule YAMLs, shared process-package Python files and `eaeu_xml/tests/test_structured_rules.py`, plus many untracked earlier-message tests and `codex_reports/`.

The target `P.SP.02_OP_22/tests/test_msg028_end_to_end.py` itself already existed as an untracked file before this batch. No pre-existing work was reset, cleaned, stashed, checked out, added or committed.

CURRENT_BATCH_CHANGES
Only the following were changed by this maintenance batch:

- the stale isolation assertion block inside `P.SP.02_OP_22/tests/test_msg028_end_to_end.py`;
- the new service report `codex_reports/MSG029_POST_MAINTENANCE_REPORT.md`.

No mapping, production Python, other test, or protected file was changed.

GIT_DIFF_CHECK
Command:
`git diff --check`

Result:
PASS, no output.

UNEXPECTED_FAILURES
None in the requested regression suites.

One initial shell invocation accidentally escaped the wildcard in the MSG028 suite path and therefore returned `file or directory not found` with no tests run. The command was immediately rerun with the requested glob and passed `113 passed`. This was a command-entry issue, not a repository/test failure.

VERDICT
READY.

The stale MSG028 isolation assertion has been replaced with direct rule-id isolation proof, all requested regression suites are green, root has 0 failed, protected files are unchanged, and the strict implementation scope was preserved.

STATUS = COMPLETE
VERDICT = READY
