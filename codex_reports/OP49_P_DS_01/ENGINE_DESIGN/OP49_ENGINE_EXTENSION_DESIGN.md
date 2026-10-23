# OP49 / P.DS.01 — Engine Extension Design

Generated: 2026-10-07. Scope: architecture/design audit only. Production code, process YAML, normative mappings and Knowledge Base were not modified.

## Executive result

The 23 capability-tagged rows were re-audited against the current working-tree engine, confirmed OP49 scope text and structure cardinalities.

- ENGINE_GAPS_REVIEWED: **23**
- CAN_USE_EXISTING_ENGINE: **2**
- TRUE_NEW_CAPABILITY_REQUIRED: **21**
- PREVIOUS_MONTH: **TRUE_NEW_CAPABILITY_REQUIRED**
- MAX: **EXISTING_CAPABILITY**
- ALL_EQUAL: **EXISTING_CAPABILITY**
- PREVIOUS_INSTANCE: **TRUE_NEW_CAPABILITY_REQUIRED**
- PER_INSTANCE_AGGREGATE: **TRUE_NEW_CAPABILITY_REQUIRED**

Two rows should be reclassified at engine-capability level after this review. This does not close their normative/source blockers.

## Evidence and current invariants

The current validator supports `aggregate_comparison`, `comparison`, `cross_instance_comparison`, `for_each` and static positional selectors. `aggregate_comparison` accepts only `SUM`/`VALUE` and is excluded from `FOR_EACH_ASSERTION_KINDS` (`eaeu_xml/src/eaeu_xml/process_packages/validator.py:12-21`, `:211-230`). The evaluator executes document-scope aggregates without an outer context (`rules_engine.py:132-141`, `:576-586`). `for_each` evaluates assertions with a `RuleContext`, and child cardinality already restricts descendants by the current parent index (`rules_engine.py:118-130`, `:565-574`).

Typed decimal comparison is already implemented in the evaluator (`rules_engine.py:589-603`), while package validation only permits `DATETIME` when `value_type` is present (`validator.py:162-163`). That is a grammar/validation gap, not a missing numeric comparator.

### A — previous calendar month

`OP49.P_DS_01.MSG_002.REQ.006` requires EventDate to be in the calendar month immediately after PreviousReportDate. Ordering two dates is insufficient: the engine must compare **calendar-month identity with an exact month offset**.

Recommended generic primitive: extend comparison semantics with a calendar-month type plus integer month offset. Conceptually:

```yaml
kind: comparison
left: EventDate
operator: EQ
right: PreviousReportDate
value_type: CALENDAR_MONTH
offset_months: 1
```

The exact YAML spelling can be chosen during implementation, but the invariant is fixed: normalize each operand to `(year, month)`, apply a signed month offset with year rollover, then compare. The helper should also back the relative selector in family C so month arithmetic has one owner.

### B — aggregates: two false-positive engine gaps

**ALL_EQUAL — MSG.005 REQ.003.** No new all-equal rule kind is necessary. Existing `for_each` + `comparison` can compare every report's modification-date field to the same field selected from `position: 1`. Equality to one member proves pairwise uniformity, and the choice of first member does not depend on normative ordering. Existing selected-operand behavior requires exactly one selected owner (`rules_engine.py:501-516`). The unresolved `ModificationDate` vs `ModificationDateTime` conflict remains a source blocker.

**MAX — MSG.006 REQ.008.** Table 14 item 2 states that requirements 3-36 apply to **each** `ChargedDistributedDutyReportDetails` (`raw_tables_13_14.md:782-787`). Within one report, the confirmed structure defines `ReportDate` with `max_occurs: 1` (`P.DS.01_OP_49/structures/R.FP.DS.01.001/1.0.0.yaml:481-489`). Therefore `MAX(ReportDate)` in that scope equals the sole `ReportDate`. Existing per-report `comparison GE` is sufficient. The `ModificationDate`/`ModificationDateTime` source conflict still prevents normative mapping today.

Result: **no MAX engine extension and no ALL_EQUAL engine extension are justified by these OP49 rows.**

### C — previous instance / positional

Table 13 item 41 defines the previous report by content: its `EventDate` is exactly one calendar month earlier (`raw_tables_13_14.md:567-583`). REQ.042-054 compare monetary values against that dynamically identified report. Static `position`, `where` constants, and current `cross_instance_comparison` cannot express a selector whose predicate depends on the current `RuleContext`. Treating the preceding XML position as the previous report would be normatively unsafe for unsorted input or a missing month.

Recommended generic primitive: a **context-relative selector** that can select sibling contexts by comparing a candidate field with a field in the current context plus a typed offset. Use it inside the already-supported `for_each` comparison operand so each current report can bind exactly one previous report. The selector must have deterministic cardinality semantics: zero matches means "no previous instance" (REQ.041 scope means REQ.042-054 do not apply); more than one match is invalid/FAIL because previous identity is ambiguous.

REQ.042-054 are monetary monotonic comparisons. Enable `DECIMAL` in validator `value_type` grammar; the evaluator already converts both sides to `Decimal`. Do not rely on lexical string `GE` (`"10" < "2"` lexically).

### D — repeated parent / per-instance aggregate

Six rules require local total-vs-sum checks inside each repeated report parent: MSG.005 REQ.023/029/036 and MSG.006 REQ.019/025/032. Existing document-scope `aggregate_comparison` can mix children belonging to different reports. The validator also rejects it inside `for_each` because it is absent from `FOR_EACH_ASSERTION_KINDS`.

Recommended generic primitive: **context-scoped aggregate comparison** by allowing `aggregate_comparison` as a `for_each` assertion. Aggregation must receive the outer `RuleContext` and restrict selected children to descendants whose index prefix belongs to that context, using the same ownership invariant already used by `_selected_child_count`. With no outer context, current document-scope aggregate behavior must stay unchanged.

This is smaller and more coherent than introducing an OP49-specific aggregate rule or encoding report indexes into YAML.

## Minimum engine extensions

1. **Calendar-month relation helper and grammar** — exact signed month offsets over typed date/date-time operands.
2. **Context-relative selector** — bind a sibling instance from current-context data, with zero/one/many semantics explicit; reuse the calendar-month helper.
3. **DECIMAL validator enablement** — allow `DECIMAL` where the evaluator already supports it; no new arithmetic comparator is needed.
4. **Context-scoped aggregate assertion** — permit `aggregate_comparison` inside `for_each` and scope aggregate selection to the current parent.

No dedicated `MAX` or `ALL_EQUAL` capability is required for the 23 OP49 rows.

## Cross-OP benefit

The scoped-aggregate design reuses an ownership model already used by repeated-child selection and parent scoping. OP23/MSG012 design material in this repository already relies on parent-scoped selectors and `for_each`, so making aggregation respect the same context is a generic engine improvement rather than an OP49 branch.

Calendar-month and context-relative selection are also generic for chronological repeated records. This audit found generic cross-OP potential but did **not** prove a specific non-OP49 normative requirement that can immediately be closed by those two extensions; that should be checked before claiming cross-OP closure.

## Regression risk

Overall risk: **MEDIUM-HIGH**. The highest risk is context-relative selection and scoped aggregation because both touch repeated-instance ownership. Required invariants are: no value leakage between repeated parents; document-scope behavior remains unchanged; positional selectors keep current semantics; duplicate relative matches fail deterministically; missing values are not fabricated; namespace/QName matching remains unchanged.

Calendar-month arithmetic is medium risk because edge cases are explicit and testable. DECIMAL validator enablement is low-to-medium risk because runtime conversion already exists, but it exposes that behavior to production package grammar and therefore needs invalid-number and lexical-vs-numeric regressions.

## Normative status

**CONFIRMED for requirement wording/scope from OP49 PDF-derived KB pages and package structure source_refs.** Engine design conclusions are implementation analysis, not normative facts. Exact imported Clark QNames remain unresolved without the official XSD payload, and the two `ModificationDate` rows retain their documented source conflict.

## Multi-agent execution note

The requested four-family subagent dispatch was attempted through Codex multi-agent tooling. The runtime returned `stream disconnected before completion: ChatGPT Web supports at most 5 simultaneous browser turns` for the parallel dispatch and again for a single-agent retry. No subagent result was used; the root audit completed the four families directly from repository evidence.
