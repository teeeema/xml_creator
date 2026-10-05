# FIX_NOW_CODE — final OP22 audit

STATUS: PARTIAL_WITH_EXPLICIT_REASONS

## Outcome

Authoritative registry: `OP22_GAPS_REVIEWED.csv`, filtered only by `op == OP22` and `review_status == FIX_NOW_CODE`. Exactly 178 source records; no manual balancing. The source has no gap_id: IDs use CSV record ordinals including the header, not physical line numbers. Matrix membership is independent of implementation decisions.

```text
FIX_NOW_CODE_BEFORE: 178
FIXED: 141
FIX_NOW_CODE_AFTER: 37
IMPLEMENTED_NOT_INTEGRATED: 0
TESTS_INCOMPLETE: 0
STILL_UNSUPPORTED: 37
POSITIONAL_BEFORE: 60
POSITIONAL_FIXED: 58
POSITIONAL_AFTER: 2
FILTERING_BEFORE: 54
FILTERING_FIXED: 24
FILTERING_AFTER: 30
DISJUNCTION_BEFORE: 35
DISJUNCTION_FIXED: 31
DISJUNCTION_AFTER: 4
CARDINALITY_AFTER_PREDICATE_BEFORE: 26
CARDINALITY_AFTER_PREDICATE_FIXED: 26
CARDINALITY_AFTER_PREDICATE_AFTER: 0
TYPED_DATE_BEFORE: 2
TYPED_DATE_FIXED: 1
TYPED_DATE_AFTER: 1
CROSS_INSTANCE_EQUALITY_BEFORE: 1
CROSS_INSTANCE_EQUALITY_FIXED: 1
CROSS_INSTANCE_EQUALITY_AFTER: 0
NEW_UNIT_TESTS: 10
NEW_INTEGRATION_TESTS: 754
TOTAL_TESTS: 3586
TOTAL_SUBTESTS: 62348
FIX_NOW_RELATED_FAILED: 0
UNRELATED_CONCURRENT_FAILED: 0
REGRESSIONS_FROM_THIS_TASK: 0
FULL_SUITE_CLEAN: YES
```

Test totals refer to one full-suite invocation, not a sum of repeated gates. Historical baseline: 2806 passed + 1162 subtests. The checkout also contains concurrent GUI test additions, so the full-suite increase is not wholly attributed to this task.

## Root cause and implementation

Existing where/parent selectors and any/IN disjunction are reused. The missing generic pieces were ordinal access, predicate-count conditions, per-owner child cardinality, typed comparison, and uniquely selected operands inside for_each. A collection count also treated positional None placeholders as real children; a failing production MSG055 ownership test and a new unit regression reproduced that error before the fix.

`rules_engine.py` and `validator.py` now support validated one-based position (or last), scoped selection_cardinality assertions, guarded document cardinality, EQ/GE/LE predicate counts, DATETIME comparisons, and an exactly-one selected operand. Sparse None slots are not counted as children. Flattened child arrays under a single actual parent remain compatible; if multiple actual parents exist, index-prefix ownership is mandatory. No scalar broadcast across repeated owners is introduced. No MSG identifier is hardcoded in the engine.

Production message rules use their confirmed source_refs and exact StructureDefinition paths. MSG031 R010 is an outer envelope: Table48 rules apply to embedded R002; Table49 rules to embedded R007. REQ19 occurs in both tables and was audited separately, preventing one successful R002 proof from closing the externally blocked R007 requirement.

Registry capability labels are retained verbatim for arithmetic. They are not normative semantics: e.g. Table34 REQ20 specifies AddressKindCode value 2 under AP, not a second address. The rule uses a scoped literal check rather than inventing an ordinal restriction.

Production changes: MSG001,003,012,020,027–043,045,047–053,055,061,062. Existing unrelated rule subtrees retain their original text formatting. Snapshot tests are updated only for newly executable inventory and fixture fields required by confirmed rules; negative assertions and unrelated unmapped reasons remain.

## Normative basis

CONFIRMED — independently read local `/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf` with the already installed fitz library. Table34 original AP/name/address rows (physical514–520), inherited originals and current-table references, Table49 register originals, Table53 MSG020 conditional NEW requirement, Table70 MSG052 roles/dates/identifier, and Table73 MSG055 payment requirement were used. Exact page/table/item references accompany each production rule. Classifier/source-conflict resolution was deliberately excluded as requested.

- Name representation literals OR/LA, language literal RU; second-name rules stay within each AP owner. REQ17 counts OR names per AP and separately requires its language. Tests include absent and duplicate OR names, mixed AP/PA/RE, multiple applications, and both parent orders.
- Table34 REQ26 (physical519) says code **or** name from its enumerated list. MSG027 previously required a matching pair; that stronger condition was replaced with inclusive OR. False/false fails; either side or both valid pass. REQ25 can separately require the presence of both fields; the isolated REQ26 truth table does not erase REQ25.
- Collective UE participants must be in the same register record. NEW cardinality activates only on matching CANCEL goods. Existing IndicatorType boolean value/lexical forms 1, true and True are supported through explicit predicates, with no fabricated missing-value default.
- Table70: role04 is CANCEL; role01 is NEW. CANCEL EndDateTime > its StartDateTime; CANCEL EndDateTime < NEW StartDateTime. Timezone offsets compare parsed instants; equality, invalid, missing and mixed aware/naive inputs fail safely. REQ24 compares NEW TrademarkId to the exact CANCEL complaint TrademarkNewId owner. Missing/ambiguous selected owners fail, rather than borrowing values.
- Table73 REQ7 requires IPPaymentDetails and BankAccountDetails **or** PaymentSystemAccountDetails under that payment. Both account forms are allowed. Sparse missing accounts and accounts under another payment do not satisfy the owner.

## Verification

All commands use PYTHONDONTWRITEBYTECODE=1 and -p no:cacheprovider. XML proofs serialize exact-QName ElementTree production-shape documents, parse them, extract with the production body provider and evaluate actual production rule dictionaries. Existing end-to-end suites cover build/serialize/parse/extract/validate and message isolation. The new proof files intentionally evaluate targeted rules on minimal documents; a targeted PASS is not claimed as whole-message normative validation.

Overall OP22 command: `python3.13 -m pytest -q P.SP.02_OP_22/tests -p no:cacheprovider --junitxml=/tmp/fix_now_code_op22_final.xml` — **3103 passed**.

Unit files for each gate: `eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py`. Full suite for each gate: `python3.13 -m pytest -q -p no:cacheprovider`. Six final capability gates run sequentially on the completed code; they are final-state certification, not claimed as chronological per-edit runs.

| Capability | Engine unit | Production OP22 selection | Full suite |
|---|---|---|---|
| POSITIONAL | 50 passed, 5 subtests passed in 0.12s | 528 passed in 2.67s | 3586 passed, 62348 subtests passed in 120.97s (0:02:00) |
| FILTERING | 50 passed, 5 subtests passed in 0.13s | 518 passed in 2.69s | 3586 passed, 62348 subtests passed in 125.89s (0:02:05) |
| DISJUNCTION | 50 passed, 5 subtests passed in 0.13s | 96 passed in 0.56s | 3586 passed, 62348 subtests passed in 125.32s (0:02:05) |
| CARDINALITY_AFTER_PREDICATE | 50 passed, 5 subtests passed in 0.12s | 196 passed in 0.83s | 3586 passed, 62348 subtests passed in 131.38s (0:02:11) |
| TYPED_DATE | 50 passed, 5 subtests passed in 0.12s | 22 passed in 0.14s | 3586 passed, 62348 subtests passed in 126.49s (0:02:06) |
| CROSS_INSTANCE_EQUALITY | 50 passed, 5 subtests passed in 0.13s | 22 passed in 0.14s | 3586 passed, 62348 subtests passed in 149.06s (0:02:29) |

Exact gate commands:

- POSITIONAL/unit: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider --junitxml=/tmp/fix_now_POSITIONAL_unit.xml`
- POSITIONAL/op22: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_original_name_count_is_exactly_one_per_ap -p no:cacheprovider --junitxml=/tmp/fix_now_POSITIONAL_op22.xml`
- POSITIONAL/full: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q -p no:cacheprovider --junitxml=/tmp/fix_now_POSITIONAL_full.xml`
- FILTERING/unit: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider --junitxml=/tmp/fix_now_FILTERING_unit.xml`
- FILTERING/op22: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_filtered_fields_cannot_be_borrowed P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_collective_ue_party_is_required_in_same_record -p no:cacheprovider --junitxml=/tmp/fix_now_FILTERING_op22.xml`
- FILTERING/full: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q -p no:cacheprovider --junitxml=/tmp/fix_now_FILTERING_full.xml`
- DISJUNCTION/unit: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider --junitxml=/tmp/fix_now_DISJUNCTION_unit.xml`
- DISJUNCTION/op22: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_existing_production_inclusive_or_truth_table P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py::test_msg055_inclusive_account_or_per_payment_owner -p no:cacheprovider --junitxml=/tmp/fix_now_DISJUNCTION_op22.xml`
- DISJUNCTION/full: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q -p no:cacheprovider --junitxml=/tmp/fix_now_DISJUNCTION_full.xml`
- CARDINALITY_AFTER_PREDICATE/unit: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider --junitxml=/tmp/fix_now_CARDINALITY_AFTER_PREDICATE_unit.xml`
- CARDINALITY_AFTER_PREDICATE/op22: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_msg001_cardinality_counts_ap_after_filter P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_original_name_count_is_exactly_one_per_ap -p no:cacheprovider --junitxml=/tmp/fix_now_CARDINALITY_AFTER_PREDICATE_op22.xml`
- CARDINALITY_AFTER_PREDICATE/full: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q -p no:cacheprovider --junitxml=/tmp/fix_now_CARDINALITY_AFTER_PREDICATE_full.xml`
- TYPED_DATE/unit: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider --junitxml=/tmp/fix_now_TYPED_DATE_unit.xml`
- TYPED_DATE/op22: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py -p no:cacheprovider --junitxml=/tmp/fix_now_TYPED_DATE_op22.xml`
- TYPED_DATE/full: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q -p no:cacheprovider --junitxml=/tmp/fix_now_TYPED_DATE_full.xml`
- CROSS_INSTANCE_EQUALITY/unit: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider --junitxml=/tmp/fix_now_CROSS_INSTANCE_EQUALITY_unit.xml`
- CROSS_INSTANCE_EQUALITY/op22: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py -p no:cacheprovider --junitxml=/tmp/fix_now_CROSS_INSTANCE_EQUALITY_op22.xml`
- CROSS_INSTANCE_EQUALITY/full: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q -p no:cacheprovider --junitxml=/tmp/fix_now_CROSS_INSTANCE_EQUALITY_full.xml`

New unit regressions:

- `test_child_counts_skip_sparse_slots_and_preserve_owner`
- `test_conditional_presence_uses_positions_within_each_owner`
- `test_count_condition_and_guard_count_only_matching_children`
- `test_filtered_child_cardinality_is_per_selected_parent`
- `test_new_rule_syntax_rejects_ignored_guards_and_invalid_counts`
- `test_position_is_scoped_to_each_nested_parent`
- `test_position_qname_and_invalid_position`
- `test_position_selects_one_based_sibling_without_changing_plain_selector`
- `test_selected_operand_is_unique_and_does_not_use_other_owner`
- `test_typed_datetime_compares_instants_and_rejects_invalid_values`

The 754 new parametrized XML cases include both parent orders, per-owner positive/negative checks, OR truth tables, duplicate/missing original names, conditional counts and exact-QName/wrong-owner cases. Every implemented result names its precise passing test nodes in `FIX_NOW_CODE_RESULTS.csv`. Existing correct XML fixtures now carry the source-required data; no failure was silenced by weakening an assertion.

## Unrelated concurrent failures

Historical full checkpoint: 2807 passed, 6 failed. Read-only git status/diff inspection identified changed examples.py and GUI-owned tests as their cause. The shared engine changes are opt-in rule syntax and do not call ExampleValueResolver. This task did not edit the application, examples, field-help, presentation or GUI files. The concurrent task subsequently changed its examples/tests; current final full-suite gates are green. FULL_SUITE_CLEAN was not asserted at the failing checkpoint.

| test | failure at previous checkpoint | changed_file | related_to_fix_now_code | reason |
|---|---|---|---|---|
| PMM01 test_priority_field_examples_are_safe_and_origin_traced | expected fixed example datetime; received current-date example | application/examples.py; PMM01 test_application_facade_pmm01.py | NO | Example resolver changed independently; no structured-rule engine call in the example calculation |
| ExampleValueResolverTests.test_classifier_without_local_values_has_no_invented_example | instructional classifier placeholder differed | application/examples.py; tests/test_examples.py | NO | Concurrent example-selection behavior |
| ExampleValueResolverTests.test_datatype_safe_examples [DateType] | expected fixed example date; received current date | application/examples.py | NO | Concurrent date example generation |
| ExampleValueResolverTests.test_datatype_safe_examples [DateTimeType] | expected 2026-08-24T15:24:00+03:00; received 2026-10-05T14:30:00 | application/examples.py | NO | Concurrent datetime example generation |
| ExampleValueResolverTests.test_datatype_safe_examples [DecimalType] | expected 10.5; received 1250.50 | application/examples.py | NO | Concurrent decimal example generation |
| ExampleValueResolverTests.test_uuid_only_when_datatype_confirms_it | expected fixed UUID; received generated UUID | application/examples.py; tests/test_examples.py | NO | Concurrent UUID example generation |

Interim task-related regressions were investigated and fixed before the final runs: sparse child counting, obsolete inventory counts, omitted AP name attributes/UE participants in fixtures, and MSG027 pair-versus-OR semantics. The earlier suite run made while mappings were still changing is not used for final certification.

## Remaining 37 GAPs — explicit reasons

No external-resource or classifier comparison, invented document-kind code, alternative owner, or source conflict was added merely to pass a test. These remain STILL_UNSUPPORTED; that status is the delivery outcome, not a claim that all are engine defects.

| gap_id | message / requirement | reason |
|---|---|---|
| OP22_GAPS_REVIEWED.csv:4 | P.SP.02.MSG.001 / REQ 13 | AMBIGUOUS: blanket AP literal conflicts with separately defined PA/RE roles; resolving normative semantics is excluded. |
| OP22_GAPS_REVIEWED.csv:15 | P.SP.02.MSG.001 / REQ 27 | SOURCE_CONFLICT: PDF physical520 uses TrademarkColourName for the picture and omits the colour QName. Do not guess the two owners. |
| OP22_GAPS_REVIEWED.csv:16 | P.SP.02.MSG.001 / REQ 32 | EXTERNAL: priority/classifier information is required; no invented classifier code or local default. |
| OP22_GAPS_REVIEWED.csv:21 | P.SP.02.MSG.003 / REQ 19 | EXTERNAL: collective charter document-kind code is not confirmed locally. A document name alone cannot replace the normative code OR name condition. |
| OP22_GAPS_REVIEWED.csv:26 | P.SP.02.MSG.005 / REQ 33 | SOURCE_CONFLICT/SEMANTIC_ROLE: PDF physical537 requires ArgumentDetails under StakeholderDetails; a different APP-level argument owner is not interchangeable. |
| OP22_GAPS_REVIEWED.csv:29 | P.SP.02.MSG.007 / REQ 2 | EXTERNAL: required/prohibited document must first be identified by a confirmed document-kind classifier. No invented code or local-name shortcut. |
| OP22_GAPS_REVIEWED.csv:30 | P.SP.02.MSG.007 / REQ 3 | EXTERNAL: required/prohibited document must first be identified by a confirmed document-kind classifier. No invented code or local-name shortcut. |
| OP22_GAPS_REVIEWED.csv:31 | P.SP.02.MSG.009 / REQ 2 | EXTERNAL: required/prohibited document must first be identified by a confirmed document-kind classifier. No invented code or local-name shortcut. |
| OP22_GAPS_REVIEWED.csv:32 | P.SP.02.MSG.009 / REQ 3 | EXTERNAL: required/prohibited document must first be identified by a confirmed document-kind classifier. No invented code or local-name shortcut. |
| OP22_GAPS_REVIEWED.csv:33 | P.SP.02.MSG.010 / REQ 2 | EXTERNAL: required/prohibited document must first be identified by a confirmed document-kind classifier. No invented code or local-name shortcut. |
| OP22_GAPS_REVIEWED.csv:34 | P.SP.02.MSG.010 / REQ 3 | EXTERNAL: required/prohibited document must first be identified by a confirmed document-kind classifier. No invented code or local-name shortcut. |
| OP22_GAPS_REVIEWED.csv:35 | P.SP.02.MSG.011 / REQ 2 | EXTERNAL: required/prohibited document must first be identified by a confirmed document-kind classifier. No invented code or local-name shortcut. |
| OP22_GAPS_REVIEWED.csv:36 | P.SP.02.MSG.011 / REQ 3 | EXTERNAL: required/prohibited document must first be identified by a confirmed document-kind classifier. No invented code or local-name shortcut. |
| OP22_GAPS_REVIEWED.csv:48 | P.SP.02.MSG.013 / REQ 2 | EXTERNAL: required/prohibited document must first be identified by a confirmed document-kind classifier. No invented code or local-name shortcut. |
| OP22_GAPS_REVIEWED.csv:49 | P.SP.02.MSG.013 / REQ 3 | EXTERNAL: required/prohibited document must first be identified by a confirmed document-kind classifier. No invented code or local-name shortcut. |
| OP22_GAPS_REVIEWED.csv:50 | P.SP.02.MSG.014 / REQ 2 | EXTERNAL: Commission/resource state is absent from the current document. |
| OP22_GAPS_REVIEWED.csv:52 | P.SP.02.MSG.014 / REQ 5 | EXTERNAL: document-kind classifier data is required to identify the prohibited document. |
| OP22_GAPS_REVIEWED.csv:53 | P.SP.02.MSG.014 / REQ 30 | EXTERNAL: the AS attachment document kind requires confirmed classifier data. |
| OP22_GAPS_REVIEWED.csv:58 | P.SP.02.MSG.021 / REQ 22 | EXTERNAL: date relation depends on prior resource state and identifying the new status date. |
| OP22_GAPS_REVIEWED.csv:59 | P.SP.02.MSG.021 / REQ 23 | EXTERNAL: date/set inclusion depends on prior resource contents; current XML alone cannot prove it. |
| OP22_GAPS_REVIEWED.csv:60 | P.SP.02.MSG.024 / REQ 2 | SOURCE_CONFLICT: ApellationOfOriginApplicationId referenced by PDF physical577 is absent from the production StructureDefinition; no substituted field. |
| OP22_GAPS_REVIEWED.csv:121 | P.SP.02.MSG.031 / REQ 19 (Таблица 49) | EXTERNAL: collective charter document-kind code is not confirmed locally. A document name alone cannot replace the normative code OR name condition. |
| OP22_GAPS_REVIEWED.csv:246 | P.SP.02.MSG.044 / REQ 16 | SOURCE_CONFLICT: inherited source_refs point to physical760/Table58 (MSG040), while MSG044 is Table62. PDF/source-ref conflict resolution is explicitly excluded. |
| OP22_GAPS_REVIEWED.csv:247 | P.SP.02.MSG.044 / REQ 17 | SOURCE_CONFLICT: inherited source_refs point to physical760/Table58 (MSG040), while MSG044 is Table62. PDF/source-ref conflict resolution is explicitly excluded. |
| OP22_GAPS_REVIEWED.csv:248 | P.SP.02.MSG.044 / REQ 18 | SOURCE_CONFLICT: inherited source_refs point to physical760/Table58 (MSG040), while MSG044 is Table62. PDF/source-ref conflict resolution is explicitly excluded. |
| OP22_GAPS_REVIEWED.csv:249 | P.SP.02.MSG.044 / REQ 19 | SOURCE_CONFLICT: inherited source_refs point to physical760/Table58 (MSG040), while MSG044 is Table62. PDF/source-ref conflict resolution is explicitly excluded. |
| OP22_GAPS_REVIEWED.csv:250 | P.SP.02.MSG.044 / REQ 20 | SOURCE_CONFLICT: inherited source_refs point to physical760/Table58 (MSG040), while MSG044 is Table62. PDF/source-ref conflict resolution is explicitly excluded. |
| OP22_GAPS_REVIEWED.csv:251 | P.SP.02.MSG.044 / REQ 26 | SOURCE_CONFLICT: inherited source_refs point to physical760/Table58 (MSG040), while MSG044 is Table62. PDF/source-ref conflict resolution is explicitly excluded. |
| OP22_GAPS_REVIEWED.csv:262 | P.SP.02.MSG.045 / REQ 30 | EXTERNAL/SEMANTIC_ROLE: transfer-document kind and scope require classifier/normative clarification, excluded from this task. |
| OP22_GAPS_REVIEWED.csv:270 | P.SP.02.MSG.047 / REQ 19 | EXTERNAL: collective charter document-kind code is not confirmed locally. A document name alone cannot replace the normative code OR name condition. |
| OP22_GAPS_REVIEWED.csv:275 | P.SP.02.MSG.048 / REQ 19 | EXTERNAL: collective charter document-kind code is not confirmed locally. A document name alone cannot replace the normative code OR name condition. |
| OP22_GAPS_REVIEWED.csv:278 | P.SP.02.MSG.049 / REQ 19 | EXTERNAL: collective charter document-kind code is not confirmed locally. A document name alone cannot replace the normative code OR name condition. |
| OP22_GAPS_REVIEWED.csv:285 | P.SP.02.MSG.050 / REQ 19 | EXTERNAL: collective charter document-kind code is not confirmed locally. A document name alone cannot replace the normative code OR name condition. |
| OP22_GAPS_REVIEWED.csv:290 | P.SP.02.MSG.051 / REQ 19 | EXTERNAL: collective charter document-kind code is not confirmed locally. A document name alone cannot replace the normative code OR name condition. |
| OP22_GAPS_REVIEWED.csv:294 | P.SP.02.MSG.052 / REQ 19 | EXTERNAL: collective charter document-kind code is not confirmed locally. A document name alone cannot replace the normative code OR name condition. |
| OP22_GAPS_REVIEWED.csv:296 | P.SP.02.MSG.052 / REQ 21 | EXTERNAL: Table70 compares CANCEL start with the unified resource start; the external resource is not an input to the production rule. |
| OP22_GAPS_REVIEWED.csv:307 | P.SP.02.MSG.053 / REQ 19 | EXTERNAL: collective charter document-kind code is not confirmed locally. A document name alone cannot replace the normative code OR name condition. |

## Repository state and artifacts

Authoritative matrix and per-GAP results are at the repository root. The supplied root registry matches the user Downloads CSV byte-for-byte. No provisional registry contributes rows. Existing source references are preserved; classifier/StructureDefinition/GUI data was not edited. Source_refs on new executable rules are copied from the corresponding confirmed capture/inventory; existing provenance is preserved.

Changed task scope: rules_engine.py, validator.py, test_structured_rules.py; listed OP22 production message rules and corresponding normative regression fixtures/snapshots; three new XML proof files; FIX_NOW_CODE_BASELINE.md, FIX_NOW_CODE_MATRIX.csv, FIX_NOW_CODE_RESULTS.csv, this audit, and the supplied registry copy. No commit was created. Pre-existing/concurrent files remain dirty and are not attributed to this task.

Final `git diff --check`, `git status --short`, `git diff --name-only` and graphify update verification are recorded below after gates complete.

## Authoritative reviewed registry and date/equality preimplementation inventory
178 rows; original capability counts 60/54/35/26/2/1 confirmed. Source-line IDs are derived because reviewed CSV has no gap_id.

{"gap_id": "OP22_GAPS_REVIEWED.csv:296", "message": "P.SP.02.MSG.052", "requirement": "REQ 21", "source": "Таблица 70, п.21 (R.IP.SP.02.007)", "structure": "R.IP.SP.02.007", "xml_owner": "ipcdo:UnifiedRegisterRecordsDetails", "xml_qname": "ipcdo:UnifiedRegisterRecordsDetails", "xml_path": "ipcdo:UnifiedRegisterRecordsDetails", "required_engine_capability": "typed date comparison", "notes": "Cross-record typed/date relationship is not representable by current rules engine."}

{"gap_id": "OP22_GAPS_REVIEWED.csv:297", "message": "P.SP.02.MSG.052", "requirement": "REQ 22", "source": "Таблица 70, п.22 (R.IP.SP.02.007)", "structure": "R.IP.SP.02.007", "xml_owner": "ipcdo:UnifiedRegisterRecordsDetails", "xml_qname": "ipcdo:UnifiedRegisterRecordsDetails", "xml_path": "ipcdo:UnifiedRegisterRecordsDetails", "required_engine_capability": "typed date comparison", "notes": "Cross-record typed/date relationship is not representable by current rules engine."}

{"gap_id": "OP22_GAPS_REVIEWED.csv:298", "message": "P.SP.02.MSG.052", "requirement": "REQ 24", "source": "Таблица 70, п.24 (R.IP.SP.02.007)", "structure": "R.IP.SP.02.007", "xml_owner": "ipcdo:UnifiedRegisterRecordsDetails", "xml_qname": "ipcdo:UnifiedRegisterRecordsDetails", "xml_path": "ipcdo:UnifiedRegisterRecordsDetails", "required_engine_capability": "cross-instance equality", "notes": "Cross-record equality is not representable by current rules engine."}

PDF reread physical793–796: roles04=CANCEL and01=NEW. REQ21 external-resource comparison cannot be closed locally. REQ22 end>start in CANCEL and end<start NEW; REQ24 NEW TrademarkId=CANCEL TrademarkNewId. Exact owners from StructureDefinition require ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails dates and ipcdo:RegistrationCancellationDetails/ipcdo:ComplaintInvalidateProtectionTrademarkDetails/ipsdo:TrademarkNewId.


## Final repository verification

`git diff --check`: PASS. `graphify update .`: exit 0; code graph updated (6352 nodes, 14491 edges). No commit created. All six final gate runs passed.

Registry SHA256: `46aa4fa05258dba46c5b576a8fd1e633345387fcb7889ad91ca643aa53a32da2`. Matrix/result membership and 178 unique record IDs verified independently; 141 implemented + 37 explicitly unsupported.

`git status --short` (includes preserved concurrent/pre-existing files):

```text
 M P.MM.01_OP_26/tests/test_application_facade_pmm01.py
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.001.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.003.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.012.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.020.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.027.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.028.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.029.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.030.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.031.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.032.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.033.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.034.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.035.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.036.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.037.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.038.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.039.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.040.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.041.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.042.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.043.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.045.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.047.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.048.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.049.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.050.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.051.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.052.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.053.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.055.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.061.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.062.yaml
 M P.SP.02_OP_22/tests/test_msg001_structured_rules.py
 M P.SP.02_OP_22/tests/test_msg003_table37_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg012_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg020_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg020_repeatable_xml.py
 M P.SP.02_OP_22/tests/test_msg020_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg027_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg027_repeatable_xml.py
 M P.SP.02_OP_22/tests/test_msg027_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg028_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg028_repeatable_xml.py
 M P.SP.02_OP_22/tests/test_msg028_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg029_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg029_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg030_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg030_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg031_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg031_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg032_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg032_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg033_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg033_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg034_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg034_repeatable_xml.py
 M P.SP.02_OP_22/tests/test_msg034_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg035_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg035_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg036_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg036_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg037_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg037_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg038_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg038_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg039_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg039_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg040_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg040_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg041_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg041_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg042_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg042_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg043_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg045_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg045_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg047_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg048_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg048_repeatable_xml.py
 M P.SP.02_OP_22/tests/test_msg048_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg049_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg050_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg051_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg052_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg052_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg053_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg055_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg055_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg057_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg061_end_to_end.py
 M P.SP.02_OP_22/tests/test_msg061_safe_mapping.py
 M P.SP.02_OP_22/tests/test_msg062_safe_mapping.py
 M eaeu_xml/.DS_Store
 M eaeu_xml/src/eaeu_xml.egg-info/PKG-INFO
 M eaeu_xml/src/eaeu_xml.egg-info/SOURCES.txt
 M eaeu_xml/src/eaeu_xml/application/examples.py
 M eaeu_xml/src/eaeu_xml/application/facade.py
 M eaeu_xml/src/eaeu_xml/application/models.py
 M eaeu_xml/src/eaeu_xml/application/services.py
 M eaeu_xml/src/eaeu_xml/gui_qt/qml/pages/HomePage.qml
 M eaeu_xml/src/eaeu_xml/gui_qt/view_model.py
 M eaeu_xml/src/eaeu_xml/presentation/controller.py
 M eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py
 M eaeu_xml/src/eaeu_xml/process_packages/validator.py
 M eaeu_xml/tests/test_examples.py
 M eaeu_xml/tests/test_gui_qt_view_model.py
 M eaeu_xml/tests/test_structured_rules.py
?? FIELD_HELP_AUDIT.csv
?? FIX_NOW_CODE_BASELINE.md
?? FIX_NOW_CODE_FINAL_AUDIT.md
?? FIX_NOW_CODE_MATRIX.csv
?? FIX_NOW_CODE_RESULTS.csv
?? OP22_GAPS_REVIEWED.csv
?? P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py
?? P.SP.02_OP_22/tests/test_fix_now_code_msg052_xml.py
?? P.SP.02_OP_22/tests/test_fix_now_code_register_xml.py
?? UI_REQUIRED_DATA_AND_HELP_AUDIT.md
?? eaeu_xml/src/eaeu_xml/presentation/field_help.py
?? eaeu_xml/tests/test_field_help_audit.py
?? eaeu_xml/tests/test_required_form_data.py
?? eaeu_xml/tools/audit_field_help.py
```

`git diff --name-only` (tracked files; untracked task artifacts are above):

```text
P.MM.01_OP_26/tests/test_application_facade_pmm01.py
P.SP.02_OP_22/message_rules/P.SP.02.MSG.001.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.003.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.012.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.020.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.027.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.028.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.029.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.030.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.031.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.032.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.033.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.034.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.035.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.036.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.037.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.038.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.039.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.040.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.041.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.042.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.043.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.045.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.047.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.048.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.049.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.050.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.051.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.052.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.053.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.055.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.061.yaml
P.SP.02_OP_22/message_rules/P.SP.02.MSG.062.yaml
P.SP.02_OP_22/tests/test_msg001_structured_rules.py
P.SP.02_OP_22/tests/test_msg003_table37_safe_mapping.py
P.SP.02_OP_22/tests/test_msg012_safe_mapping.py
P.SP.02_OP_22/tests/test_msg020_end_to_end.py
P.SP.02_OP_22/tests/test_msg020_repeatable_xml.py
P.SP.02_OP_22/tests/test_msg020_safe_mapping.py
P.SP.02_OP_22/tests/test_msg027_end_to_end.py
P.SP.02_OP_22/tests/test_msg027_repeatable_xml.py
P.SP.02_OP_22/tests/test_msg027_safe_mapping.py
P.SP.02_OP_22/tests/test_msg028_end_to_end.py
P.SP.02_OP_22/tests/test_msg028_repeatable_xml.py
P.SP.02_OP_22/tests/test_msg028_safe_mapping.py
P.SP.02_OP_22/tests/test_msg029_end_to_end.py
P.SP.02_OP_22/tests/test_msg029_safe_mapping.py
P.SP.02_OP_22/tests/test_msg030_end_to_end.py
P.SP.02_OP_22/tests/test_msg030_safe_mapping.py
P.SP.02_OP_22/tests/test_msg031_end_to_end.py
P.SP.02_OP_22/tests/test_msg031_safe_mapping.py
P.SP.02_OP_22/tests/test_msg032_end_to_end.py
P.SP.02_OP_22/tests/test_msg032_safe_mapping.py
P.SP.02_OP_22/tests/test_msg033_end_to_end.py
P.SP.02_OP_22/tests/test_msg033_safe_mapping.py
P.SP.02_OP_22/tests/test_msg034_end_to_end.py
P.SP.02_OP_22/tests/test_msg034_repeatable_xml.py
P.SP.02_OP_22/tests/test_msg034_safe_mapping.py
P.SP.02_OP_22/tests/test_msg035_end_to_end.py
P.SP.02_OP_22/tests/test_msg035_safe_mapping.py
P.SP.02_OP_22/tests/test_msg036_end_to_end.py
P.SP.02_OP_22/tests/test_msg036_safe_mapping.py
P.SP.02_OP_22/tests/test_msg037_end_to_end.py
P.SP.02_OP_22/tests/test_msg037_safe_mapping.py
P.SP.02_OP_22/tests/test_msg038_end_to_end.py
P.SP.02_OP_22/tests/test_msg038_safe_mapping.py
P.SP.02_OP_22/tests/test_msg039_end_to_end.py
P.SP.02_OP_22/tests/test_msg039_safe_mapping.py
P.SP.02_OP_22/tests/test_msg040_end_to_end.py
P.SP.02_OP_22/tests/test_msg040_safe_mapping.py
P.SP.02_OP_22/tests/test_msg041_end_to_end.py
P.SP.02_OP_22/tests/test_msg041_safe_mapping.py
P.SP.02_OP_22/tests/test_msg042_end_to_end.py
P.SP.02_OP_22/tests/test_msg042_safe_mapping.py
P.SP.02_OP_22/tests/test_msg043_safe_mapping.py
P.SP.02_OP_22/tests/test_msg045_end_to_end.py
P.SP.02_OP_22/tests/test_msg045_safe_mapping.py
P.SP.02_OP_22/tests/test_msg047_safe_mapping.py
P.SP.02_OP_22/tests/test_msg048_end_to_end.py
P.SP.02_OP_22/tests/test_msg048_repeatable_xml.py
P.SP.02_OP_22/tests/test_msg048_safe_mapping.py
P.SP.02_OP_22/tests/test_msg049_safe_mapping.py
P.SP.02_OP_22/tests/test_msg050_safe_mapping.py
P.SP.02_OP_22/tests/test_msg051_safe_mapping.py
P.SP.02_OP_22/tests/test_msg052_end_to_end.py
P.SP.02_OP_22/tests/test_msg052_safe_mapping.py
P.SP.02_OP_22/tests/test_msg053_safe_mapping.py
P.SP.02_OP_22/tests/test_msg055_end_to_end.py
P.SP.02_OP_22/tests/test_msg055_safe_mapping.py
P.SP.02_OP_22/tests/test_msg057_end_to_end.py
P.SP.02_OP_22/tests/test_msg061_end_to_end.py
P.SP.02_OP_22/tests/test_msg061_safe_mapping.py
P.SP.02_OP_22/tests/test_msg062_safe_mapping.py
eaeu_xml/.DS_Store
eaeu_xml/src/eaeu_xml.egg-info/PKG-INFO
eaeu_xml/src/eaeu_xml.egg-info/SOURCES.txt
eaeu_xml/src/eaeu_xml/application/examples.py
eaeu_xml/src/eaeu_xml/application/facade.py
eaeu_xml/src/eaeu_xml/application/models.py
eaeu_xml/src/eaeu_xml/application/services.py
eaeu_xml/src/eaeu_xml/gui_qt/qml/pages/HomePage.qml
eaeu_xml/src/eaeu_xml/gui_qt/view_model.py
eaeu_xml/src/eaeu_xml/presentation/controller.py
eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py
eaeu_xml/src/eaeu_xml/process_packages/validator.py
eaeu_xml/tests/test_examples.py
eaeu_xml/tests/test_gui_qt_view_model.py
eaeu_xml/tests/test_structured_rules.py
```
