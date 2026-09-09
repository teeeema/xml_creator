# P.MM.01 conditional rules report

Generated: 2026-08-25

## Summary

- total conditional usages: 133
- machine-evaluable: 0
- unresolved: 133
- compilation policy: only explicit structured `conditional_rule` metadata with source traceability

The current P.MM.01 MessageRules contain textual condition descriptions and referenced fields, but no explicit `source_field_path + operator + expected value + effect` metadata. No NLP or XML-name inference was performed; therefore no real P.MM.01 field is dynamically hidden, enabled or required.

## By message

| MSG | Conditional usages | Machine-evaluable | Unresolved |
|---|---:|---:|---:|
| P.MM.01.MSG.001 | 17 | 0 | 17 |
| P.MM.01.MSG.002 | 85 | 0 | 85 |
| P.MM.01.MSG.007 | 1 | 0 | 1 |
| P.MM.01.MSG.010 | 1 | 0 | 1 |
| P.MM.01.MSG.019 | 6 | 0 | 6 |
| P.MM.01.MSG.020 | 4 | 0 | 4 |
| P.MM.01.MSG.021 | 8 | 0 | 8 |
| P.MM.01.MSG.023 | 3 | 0 | 3 |
| P.MM.01.MSG.024 | 3 | 0 | 3 |
| P.MM.01.MSG.025 | 1 | 0 | 1 |
| P.MM.01.MSG.027 | 1 | 0 | 1 |
| P.MM.01.MSG.028 | 3 | 0 | 3 |

## Condition type distribution

- none (0 compiled rules)

## Effect distribution

- none (0 compiled rules)

## Safety conclusion

All 133 usages remain visible and annotated as conditional. Their current evaluation is `UNKNOWN`. Known normative conflicts in MSG.002, MSG.023 and MSG.024 retain priority and were not reinterpreted.
