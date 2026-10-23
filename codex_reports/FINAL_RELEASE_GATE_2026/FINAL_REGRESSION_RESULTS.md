# FINAL REGRESSION RESULTS

STATUS: **BLOCKED_PRECONDITION**

No Gate 5 test suite was executed. The task explicitly requires the final gate to start only after `KB_FINAL_SYNC = COMPLETE` and `READY_FOR_FINAL_GATE = YES`; current KB PROJECT_STATE is tied to `5df76609131e9ce88fea5502fdc942238ab2c792` while current HEAD is `ac0dd6f24e5e2536b20cb1ae7936aa0cd370a16b` and there are 37 relevant dirty files.

| Suite | Result |
|---|---|
| `eaeu_xml/tests` | NOT RUN |
| `P.SP.02_OP_22/tests` | NOT RUN |
| `P.SP.03_OP_23/tests` | NOT RUN |
| `P.MM.01_OP_26/tests` | NOT RUN |
| `P.MM.06_OP_32/tests` | NOT RUN |
| `P.DS.01_OP_49/tests` | NOT RUN |
| `git diff --check` | NOT RUN as Gate 5 |

Precondition-only check actually executed: `python3 knowledge_base/tools/build_kb.py --check-stale` → `{"stale_sources": [], "count": 0}`. This validates source hashes only; it does not synchronize PROJECT_STATE.
