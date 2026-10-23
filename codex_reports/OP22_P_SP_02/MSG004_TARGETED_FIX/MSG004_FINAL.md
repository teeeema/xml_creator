# MSG004 targeted correction — 2026-10-23

STATUS: TARGETED_FIX_VERIFIED; OP22_REGRESSION_NOT_GREEN
MSG004_STATUS = VERIFIED

## ROOT_CAUSE

The local P.CLS.027 subset omitted independently confirmed entry07320. MSG004 had no executable Table38 REQ2/3 and no effective Code/Name policy. Missing/arbitrary Code and direct Code+Name passed actual validation. before.json was collected before product edits; MSG004_ROOT_CAUSE.md records the read-only phase. Classifier presence is established by the source, not inferred from XML field presence.

## Trace and normative basis

OP22 → P.SP.02.PRC.008 → P.SP.02.TRN.003 → P.SP.02.MSG.004 → Table38 REQ2/3 → R.IP.SP.02.002 → direct ipcdo:TrademarkApplicationDetails owner → ipsdo:IPDocKindCode / ipsdo:IPDocKindName. Expanded QNames are in MSG004_REQUIREMENT_TRACE.csv.

CONFIRMED in supplied sources: ОП_22.pdf physical p532, Table38 REQ2/3; Table38 begins p531, REQ5/inherited6–29/attached-document REQ30 on p533, further rules p534. Readable RTF section49/Table38 agrees. Decision92 physical p13 and Decision148 p3 independently identify07320 for the Article8 interested-party objection. Original extracted text and hashes: sources.json. No PDF/RTF modified. No normative value borrowed from another message.

## EXPECTED / ACTUAL

| Aspect | Expected | Before | After |
|---|---|---|---|
| direct Code | REQUIRED, FIXED07320, readonly | editable, no effective policy | required=True, fixed07320, editable=False |
| direct Name | FORBIDDEN | editable, no effective policy | forbidden, hidden, editable=False |
| attached document Name | REQUIRED by REQ30 per owner | populated | remains populated; not globally forbidden |
| raw XML missing/wrong Code or Code+Name | reject | accepted | fails P.SP.02.MSG.004.REQ.2 |
| stale form values | fixed Code, no direct Name | arbitrary values emitted |07320/no direct Name |
| direct serializer bad input | reject | invalid values emitted | BodyValidationError, REQ2 |

## IMPLEMENTATION / CHANGED_FILES

- P.SP.02_OP_22/normative_classifier_data/P.CLS.027.yaml: add source-traced07320, preserving existing entries.
- P.SP.02_OP_22/message_rules/P.SP.02.MSG.004.yaml: add exact-owner structured REQ2 (fixed Code and forbidden Name). REQ3 fallback remains inactive in the confirmed current classifier revision; source text retained. Keep legacy fixed_values empty to prevent missing XML being silently defaulted before validation.
- P.SP.02_OP_22/message_field_policies/P.SP.02.MSG.004.yaml: explicit fixed/forbidden application/form overlay on exact direct paths.
- P.SP.02_OP_22/tests/test_msg004_end_to_end.py and test_msg004_safe_mapping.py: source-correct Code fixture and mapping classification.
- P.SP.02_OP_22/tests/test_msg004_classifier_policy.py: raw XML positive/negative, wrong namespace, nested Name isolation, real form/resolver and sanitization coverage.
- eaeu_xml/tests/test_structured_rule_form_policy.py: adjust only MSG004 expected sanitized result for the new confirmed Code policy; preserve assertions that derived StatusCode policies do not sanitize input.
- knowledge_base/decisions/MSG004_TARGETED_FIX_2026_10_23.md: source/evidence note.
- Requested report directory; CONTROL_VERIFICATION_FINAL.md updated only historical MSG004 bullet. CONTROL_CASES.csv and its 14 PASS / 1 SOURCE_BLOCKED unchanged.
- graphify-out: mandatory AST refresh; HTML remains stale above rendering limit.

No shared runtime component changed. Other OP files and closed MSG001/005/027 files match session baseline hashes (scope_check.json, diff_check.json). Existing parallel changes preserved. No forbidden Git operation, commit or push.

## GUI / VALIDATOR / XML PROOF

MSG004_RUNTIME_EVIDENCE.md summarizes every expected/actual scenario. before.json / after.json contain actual get_form(), resolver, GuiController controls and validator IDs. gui_evidence.json and GUI_GENERATED.xml prove real Qt offscreen GuiViewModel selection, blocked readonly edits and generation. No manual desktop visual inspection is claimed.

Actual body positive and four negative XML scenarios plus form-sanitized XML are persisted. Direct serializer tampering is rejected before XML output. Namespace-aware parse/extract/validation is independent of form sanitization. Wrong-namespace Code does not satisfy REQ2. VERSION_PLACEHOLDER_TEST is explicitly test generation, not production-XSD certification. xml_manifest.json contains artifact hashes.

## VERIFICATION

Executed from repository root with PYTHONPATH=eaeu_xml/src, python3.13:

1. `-m pytest -q P.SP.02_OP_22/tests/test_msg004* --tb=short`: **58 passed in 4.31s** (focused_tests.log).
2. `-m pytest -q eaeu_xml/tests/test_structured_rule_form_policy.py eaeu_xml/tests/test_op22_visual_engine.py eaeu_xml/tests/test_gui_controller.py eaeu_xml/tests/test_gui_qt_view_model.py --tb=short`: **42 passed in 5.21s** (policy_gui_tests.log).
3. `-m pytest -q P.SP.02_OP_22/tests --tb=short`: **4460 passed, 1 failed in119.28s** (op22_regression.log).
4. probe.py before / after and gui_probe.py: runtime artifacts generated and post-fix expectations verified.
5. `git diff --check`: PASS; new untracked code/policy whitespace checked independently. Final diff reviewed. Original source hashes and unrelated product hashes rechecked.
6. `graphify update .`: exit0, AST refreshed; HTML exceeds5000-community visualization limit.

Full cross-OP regression NOT RUN: no cross-process runtime component changed. Requested full OP22 regression was run without excluding the failing test.

## REMAINING_BLOCKERS

OP22 full regression failure: test_old_open261_mapped_proof.py::test_old_open_now_mapped_requirement_matches_strict_proof_verdict[P.SP.02.MSG.027:57:3]. Old strict-proof catalog expects P.SP.02.MSG.027.T57.REQ.3, removed in the preceding source-confirmed classifier-present fix. This task did not change MSG027; its rule hash equals the pre-fix baseline and lacks that fallback already. See regression_blocker.json. Do not reinterpret this failure as PASS or modify MSG027/catalog under the MSG004 task.

MSG004 external Commission registry portion of REQ4 remains partial, as do existing unrelated normative gaps. This correction certifies selected REQ2 classifier behavior, not entire-message normative closure, registry access, current live classifier service or production XSD validation. The prior CONTROL_VERIFICATION external classifier blocker is unchanged.
