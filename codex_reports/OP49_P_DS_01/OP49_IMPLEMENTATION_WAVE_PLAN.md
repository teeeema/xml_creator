# OP49 / P.DS.01 implementation wave plan

Generated: 2026-10-07. Scope: READ ONLY implementation triage. Production YAML, Knowledge Base and engine were not changed.

## Canonical baseline

- Requirements: **166** (MSG.001=35, MSG.002=38, MSG.003=0, MSG.004=2, MSG.005=54, MSG.006=37).
- Strict state: **0 IMPLEMENTED_CONFIRMED / 166 OPEN**.
- Current package: **111 business_rules**, **36 structured production rules**, therefore **130 requirements have no structured production mapping**.
- `ALREADY_PRODUCTION_MAPPED` means a structured rule object exists; it does **not** mean strict normative closure.
- Exact imported leaf Clark QNames remain unresolved without official XSD payloads. `MISSING_XSD/QNAME_ONLY` is used only where that is the primary blocker.

## Current engine audit

Inspected the current working-tree `rules_engine.py` and `validator.py`, including uncommitted changes. Current production grammar/evaluator supports:

- presence, fixed value, comparison and cardinality;
- selection cardinality;
- conditional presence/fixed value;
- `for_each` with logical conditions (`all` / `any` / `not`) and positional selectors;
- document-scope `aggregate_comparison` with `SUM` and single `VALUE`;
- `cross_instance_comparison` with static selectors;
- `group_distinctness`;
- external placeholders.

Current limits relevant to OP49:

- **previous calendar month**: no month arithmetic / relative-month selector;
- **MAX**: not supported (`aggregate_comparison` accepts only `SUM` / `VALUE`);
- **all-equal across repeated reports**: no direct primitive;
- **per-instance aggregates under repeated report parents**: not safely expressible; `aggregate_comparison` is document-scoped and is not a legal `for_each` assertion;
- **previous-instance / monotonic rules**: static cross-instance selectors cannot bind the sibling whose EventDate is current EventDate minus one month; validator also does not accept DECIMAL `value_type` even though evaluator contains DECIMAL conversion code;
- **workday**: needs an authoritative external working-day calendar/provider;
- **classifier/currency**: needs authoritative member-state country→currency data/version;
- **external information base**: needs external registry state/interface.

This changes the earlier re-audit capability split: six per-instance aggregate requirements move from B3/safe mapping to `ENGINE_GAP`:

- MSG.005 REQ.023, REQ.029, REQ.036;
- MSG.006 REQ.019, REQ.025, REQ.032.

## Primary triage (mutually exclusive, arithmetic = 166)

| Primary status | Count |
|---|---:|
| PRODUCTION_MAPPING_MISSING | 36 |
| ENGINE_GAP | 21 |
| CLASSIFIER_BLOCKED | 52 |
| EXTERNAL_REGISTRY_BLOCKED | 5 |
| SOURCE_CONFLICT | 35 |
| MISSING_XSD/QNAME_ONLY | 15 |
| NORMATIVE_AMBIGUITY | 0 |
| OTHER | 2 |
| **TOTAL** | **166** |

`SOURCE_CONFLICT` keeps precedence. Two source-conflict rows also have an engine capability gap, but remain primary `SOURCE_CONFLICT`.

## Mapping/readiness flags

- **ALREADY_PRODUCTION_MAPPED: 36** (MSG.001=34, MSG.004=2).
- **PRODUCTION_MAPPING_MISSING: 130** total rows without structured production rules.
- **SAFE_IMPLEMENTABLE_NOW / SAFE_MISSING_MAPPING: 36**: current engine can represent the rule and there is no stronger classifier/external/source/XSD-only/engine blocker.
- **BLOCKED_REQUIREMENTS: 130** under this triage (includes already-mapped rows that still lack strict normative closure).

## Engine batch map

| Batch | Count | Meaning |
|---|---:|---|
| B1 | 16 | simple presence/fixed/comparison |
| B2 | 57 | repeated/conditional/disjunction |
| B3 | 8 | positional/cardinality/document-scope aggregate or uniqueness |
| B4 | 62 | cross-instance/date/aggregate/external-context complexity that is representable in principle or externally blocked |
| ENGINE_GAP | 23 | not safely representable by current production grammar/evaluator |
| **TOTAL** | **166** | |

`ENGINE_GAP` capability count is **23**. Of these, **2** remain primary `SOURCE_CONFLICT`; therefore the mutually-exclusive primary `ENGINE_GAP` count is **21**.

## Safe implementation waves

The safe queue contains **36** rows:

1. **Wave 1 — B1: 6**. Direct presence/cardinality/comparison mappings. This is the next recommended OP49 wave because it has the smallest semantic surface and uses already-tested primitives.
2. **Wave 2 — B2: 25**. Repeated/conditional/disjunction mappings using existing selectors, conditions and `for_each`.
3. **Wave 3 — B3: 5**. Three MSG.002 document-scope SUM/VALUE aggregates plus duplicate-EventDate checks for MSG.005/MSG.006. The six repeated-parent aggregate rules are excluded and stay `ENGINE_GAP`.

**NEXT_SAFE_WAVE_SIZE: 6**.

## Source conflicts

No newer normative evidence was found in the current normative directory: `49_ОП.pdf` remains the OP49 primary PDF and there are still no XSD/XML schema payloads. The following three conflict patterns therefore remain unresolved and all **35 affected rows stay `SOURCE_CONFLICT`**:

- `CountryCode` vs `UnifiedCountryCode`;
- `ModificationDate` vs `ModificationDateTime`;
- `VerificationPro` vs `VerificationProDetails`.

No side was selected automatically.

## Verification performed

- Current engine tests: `74 passed, 5 subtests passed` (`test_structured_rules.py`, `test_repeatable_xml_alignment.py`, `test_required_presence_semantics.py`).
- OP49 package tests: `26 passed`.
- Canonical arithmetic: 166 unique rows; primary categories sum to 166; engine buckets sum to 166.
- Package inventory: 111 business rules / 36 structured rules.
- Source conflicts: 35.
- No official XSD/XML payloads found recursively in the primary normative directory.

## Next wave guardrails

Wave 1 may add only the six rows listed as `WAVE_1` in `OP49_SAFE_IMPLEMENTATION_QUEUE.csv`. Keep source-conflict rows untouched. Do not normalize conflicting QNames. Do not implement classifier, registry, workday, previous-month, MAX/all-equal or per-instance aggregate behavior until their blocker is resolved at the responsible layer.
