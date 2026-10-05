# FIX_NOW_CODE baseline

## Environment and source registry

The requested `/Users/tema/Documents/Работа/xml_creator` directory does not exist on this host. The active checkout is `/Users/tema/Documents/Work/xml_creator`.

At the initial checkpoint the reviewed registry was unavailable, so the tracked `codex_reports/FINAL_DELIVERY_GAPS.csv` was used only as a provisional candidate list. On continuation the user supplied `/Users/tema/Downloads/OP22_GAPS_REVIEWED.csv`; an identical copy is now at the repository root. The authoritative matrix is generated exclusively from `op == OP22` and `review_status == FIX_NOW_CODE`: 178 rows; capability counts 60/54/35/26/2/1. The provisional registry is not used for closure. Since the reviewed CSV has no gap_id, IDs identify the original CSV record ordinal (header included), not physical lines when a record contains newlines.

## Test baseline

Command: `PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q -p no:cacheprovider`

- BASELINE_TOTAL: 2806 collected tests, plus 1162 reported subtests
- BASELINE_PASSED: 2806 tests; 1162 subtests
- BASELINE_FAILED: 0
- BASELINE_ERRORS: 0
- Existing failures/errors: none

## Rule engine architecture

`eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py` evaluates structured rule dictionaries against flattened XML values. `RuleContext` carries the exact path, repeated-instance indexes, and fields for each selected parent. `_select_contexts` supports collection/QName selection, parent-scoped selection, and a `where` predicate. `selection_cardinality` counts the selected contexts after the predicate. `evaluate_condition` supports recursive `all`, `any`, and `not`; `cross_instance_comparison` selects semantically identified records and compares their fields. The package validator checks rule syntax and operators; the body provider extracts production XML values while preserving repeated-parent alignment.

The existing evaluator lacks an explicit ordinal selector and typed ISO date comparator. Current support for the other four capability labels must be checked against each normative rule rather than inferred from the label alone.

Pre-existing worktree changes before this task: `eaeu_xml/.DS_Store`, `eaeu_xml/src/eaeu_xml.egg-info/PKG-INFO`, and `eaeu_xml/src/eaeu_xml.egg-info/SOURCES.txt`. They were left untouched.
