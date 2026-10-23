# P.SP.02.MSG.001 — policy test results

This report is updated after verification. Current implementation metrics:

- Table 34 requirements: 39
- Effective fields: 404
- Policy counts: REQUIRED=20, OPTIONAL=145, FORBIDDEN=147, FIXED=16, CONDITIONAL=76
- Fields without effective policy: 0
- Conditional fields with unresolved external/source dependency markers: 6

Executed so far:

- `P.SP.02_OP_22/tests/test_msg001_effective_field_policy.py` — **9 passed**.
- `eaeu_xml/tests/test_gui_qt_view_model.py` — **22 passed**.
- `P.SP.02_OP_22/tests/test_msg001_structured_rules.py` — **44 passed**.
- `eaeu_xml/tests/test_application_facade.py eaeu_xml/tests/test_gui_controller.py` — **16 passed**.
- Full `P.SP.02_OP_22/tests` — **4438 passed**, 0 failed.
- Full `eaeu_xml/tests` — **418 passed, 63 521 subtests passed**, 0 failed.
- `graphify update .` — PASS: `graph.json` and `GRAPH_REPORT.md` rebuilt. The optional HTML visualization was not regenerated because the aggregated graph has 5221 nodes, above the configured 5000-node visualization limit.
- `git diff --check` — PASS.
