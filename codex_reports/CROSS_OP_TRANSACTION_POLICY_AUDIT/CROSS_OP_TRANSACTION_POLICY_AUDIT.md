# CROSS-OP Transaction / Message / GUI Policy Audit

Generated from the current worktree. Production code was not modified by this audit builder.

## Scope

- Runtime OP packages: 5 (P.DS.01, P.MM.01, P.MM.06, P.SP.02, P.SP.03).
- Runtime transactions: 114.
- Runtime messages: 146.
- Unique MSG/structure field paths reviewed: 27351.
- TRN/MSG/field matrix rows: 28528.
- Unique effective field-policy rows after TRN reuse deduplication: 27351.
- Source directory files inventoried by path/content-candidate scope: 60.
- OP35.1 / P.TS.01 is not a runtime package in the discovered process set; it remains SOURCE/REPORT_ONLY unless a package is added.
- UNREVIEWED_TRN: 0.
- UNREVIEWED_MSG: 0.
- UNKNOWN_POLICY: 0.

## Result counts

- PASS (unique effective field-policy rows): 27351.
- GUI_DEFECT: 0.
- POLICY_DEFECT: 0.
- DEFAULT_VALUE_DEFECT: 0.
- VALIDATOR_DEFECT: 0.
- GUI_VALIDATOR_DIVERGENCE: 0.
- SOURCE_BLOCKED runtime requirements: 511.
- SOURCE/REPORT_ONLY blocked OP35.1 messages: 11.
- AMBIGUOUS: 0.
- P0 unique defects: 0.
- P1 unique defects: 0.
- P2 unique defects: 0.

Raw branch-level matrix counts are retained only in `CROSS_OP_TRN_MSG_MATRIX.csv`; the headline defect counts above are deduplicated by effective MSG/structure/field policy semantics.

## Message review coverage

- PASS branches: 63.
- EXPLICIT_DEFECT branches: 20.
- SOURCE_BLOCKED branches: 63.
- Coverage gate: UNREVIEWED_TRN=0, UNREVIEWED_MSG=0, UNKNOWN_POLICY=0.

## Requirement/source blocker accounting

- SOURCE_BLOCKED: 507.
- SOURCE_AND_ENGINE_BLOCKED: 4.
- ENGINE_BLOCKED: 25.
- PARTIAL_PROOF: 2.
- REVIEWED_BLOCKER: 2.
- SOURCE_RESOLVED_RUNTIME_UNIMPLEMENTED: 44.
- SOURCE_REPORT_ONLY_BLOCKED: 11.
- OP23 Decision №92 historical classifier source blockers resolved by current exact-name evidence: 44.

## Classifier resolution rows

- RESOLVED_FIXED_CODE: 8.
- RESOLVED_CODE_OR_NAME: 14.
- STILL_EXTERNAL: 162.
- AMBIGUOUS: 0.
- SOURCE_CONFLICT: 0.

## Per-OP matrix summary

- OP22: status=AUDITED_SOURCE_BLOCKED, unique_field_policies=17865, unique_runtime_defects=0, source_blocked_requirements=38.
- OP23: status=AUDITED_WITH_EXPLICIT_DEFECTS, unique_field_policies=5066, unique_runtime_defects=0, source_blocked_requirements=161.
- OP26: status=AUDITED_SOURCE_BLOCKED, unique_field_policies=2960, unique_runtime_defects=0, source_blocked_requirements=35.
- OP32: status=AUDITED_SOURCE_BLOCKED, unique_field_policies=1155, unique_runtime_defects=0, source_blocked_requirements=170.
- OP49: status=AUDITED_WITH_EXPLICIT_DEFECTS, unique_field_policies=305, unique_runtime_defects=0, source_blocked_requirements=107.

## Method and limits

The matrix starts from structure cardinality and overlays current source-referenced message rules in increasing authority: `field_usage`, `fixed_values`, reducible `structured_rules`, then explicit `MessageFieldPolicy`. GUI state is taken from the actual `EaeuXmlApplication.get_form()` result for every real TRN/MSG branch. Validator state records enforcement through `field_usage`, `fixed_values`, structured rules, explicit `MessageFieldPolicy` sanitization/required checks, or structure semantics.

Conditional FIXED/FORBIDDEN structured rules are treated as context-dependent policies and do not create unconditional `DEFAULT_VALUE_DEFECT` rows. Complex structured rules that cannot be safely reduced to one static field policy are retained in `UNRESOLVED_STRUCTURED_RULE_TARGETS.csv`; they are explicitly reviewed rather than guessed.

Source state is kept separate from runtime policy state in `CROSS_OP_SOURCE_BLOCKERS.csv`. OP32 remains source-blocked because exact imported model/XSD versions and Clark QNames are unresolved. OP49 source conflicts remain source conflicts. OP26 input/UI policies are treated as current project behavior and are not promoted to normative fixed values without source proof. OP35.1 remains source/report-only.

Classifier resolution is exact-name only. For local P.CLS.027 data, only one exact name-to-code match yields `RESOLVED_FIXED_CODE`; ambiguous or absent exact names are not force-resolved. Current Decision №92 evidence in `/Users/tema/Documents/Work/Документы_xml/92 решение.pdf` supersedes the stale OP23 historical “classifier unavailable” premise for the exact document-kind names found on pp.13-14 and 17, while runtime enforcement/proof remains a separate question.
