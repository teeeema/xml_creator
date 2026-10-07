# Canonical KB Scope 2894 Migration

## Baseline

- Schema version: `1.0`
- Superseded known scope: **2849**.
- Previous Schema v1 canonical entities: **2690** (OP49 was not materialized).
- New canonical scope: **2894** atomic requirements.
- Canonical entity delta: **+204** = OP26 **+38** + OP49 **+166**.

## New scope

| OP | Canonical requirements |
|---|---:|
| OP22 | 1609 |
| OP23 | 710 |
| OP26 | 239 |
| OP32 | 170 |
| OP49 | 166 |
| **TOTAL** | **2894** |

## Identity rule for duplicate source numbering

Normative source numbering remains source metadata. For OP26 MSG.028 the two distinct Table 21 rows both remain source item `5`; canonical identity uses `source_occurrence` and a deterministic canonical disambiguator. No synthetic normative item number is introduced.

## Validation

- Status: **PASS**
- Duplicate canonical IDs: **0**
- Missing requirement files: **0**
- Broken canonical relations: **0**
- Broken internal links: **0**
- Stale sources: **0**
- Reproducibility: **PASS**
