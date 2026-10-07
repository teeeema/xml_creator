# WAVE 2 — OP23 B1 regression results

## WAVE 2 focused

Shared generator root-cause checks:

```text
2 passed in 0.08s
```

Covered:

- complex `condition.any` `NE null` can materialize a complex branch and required descendants;
- unconditional cardinality still adds only the minimum `[None]` structural instance.

MSG.022 focused after removing the old payment/account helper fallback:

```text
14 passed, 619 deselected in 1.92s
```

The generated MSG.022 baseline contains `ipcdo:IPPaymentDetails`, a `ccdo:BankAccountDetails` branch, and its required bank descendants before `build_body()`. `build_body()` succeeds without message-specific payment injection.

Package generation check:

```text
1 passed, 2 deselected, 27 subtests passed in 1.81s
```

## OP23 B1

Final rerun after removing the helper fallback:

```text
631 passed in 103.71s
```

Historical WAVE 2 baseline before the MSG.022 fix:

```text
617 passed, 14 failed
```

Unexpected B1 rejections therefore changed from **14 → 0**.

## Full OP23

```text
634 passed, 27 subtests passed in 106.13s
```

## Shared engine/application tests

```text
398 passed, 62250 subtests passed in 10.48s
```

## WAVE 1 original negative QA cases

```text
6 passed in 0.76s
```

Covered the same six WAVE 1 acceptance regressions: OP22 empty REQUIRED, OP23 empty REQUIRED, OP26 empty REQUIRED StartDateTime, two OP26 TEST-placeholder cases, and GUI stale snapshot validation.

## WAVE 1 focused regression

```text
12 passed in 0.99s
```

Includes shared REQUIRED semantics, OP22/OP23 negative checks, OP26 normative test-data/negative checks, GUI current-snapshot validation, and the shared repeated-child context regression.

## GUI

```text
22 passed in 0.74s
```

## OP22

```text
3110 passed in 115.05s
```

## OP26

```text
93 passed, 83 subtests passed in 8.03s
```

## Safety

- Validator weakened: **NO**.
- Production message-specific hardcode: **NO**.
- Shared generator/application infrastructure changed: **YES**.
- GUI changed by WAVE 2: **NO**.
- Knowledge Base changed by WAVE 2: **NO**.
- Existing uncommitted/parallel work was preserved.

## git diff --check

Global repository check reports one pre-existing unrelated whitespace warning:

```text
eaeu_xml/tests/test_structured_rules.py:889: new blank line at EOF.
```

No WAVE 2 production/test/report file introduces a new trailing-whitespace error. The unrelated file was not modified solely to make this check green.

## Graphify

`graphify update .` completed after the final code changes:

```text
39125 nodes, 49008 edges, 5175 communities
```

`graph.json` and `GRAPH_REPORT.md` were rebuilt. `graph.html` remains stale because the aggregated graph has 5175 nodes, above the configured 5000-node visualization limit. This is the known pre-existing visualization limitation and does not affect the code graph data used by Graphify queries.

## Full repository suite

`NOT RUN`. The complete affected verification set was run instead: shared engine/application, full OP23, full OP23 B1, OP22, OP26, GUI, and WAVE 1 focused/original regressions.
