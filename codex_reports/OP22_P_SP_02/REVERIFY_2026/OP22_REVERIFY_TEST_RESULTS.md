# OP22 / P.SP.02 — REVERIFY 2026 test results

Date: 2026-10-14  
Scope: OP22 / P.SP.02 only

## Fresh runtime proof

The fresh 111 transaction/message runtime matrix executes Test Data and Required Data through serialization → parse → extract → validate.

- PASS: 102
- FAIL: 9
- Historical 111/111 matrix is stale and is not used as current proof.

### Current runtime failures

| Message | Test error | Required error |
|---|---|---|
| P.SP.02.MSG.001 | BodyValidationError:Body содержит 12 issue(s). | BodyValidationError:Body содержит 12 issue(s). |
| P.SP.02.MSG.003 | postvalidate:EMBEDDED_STRUCTURE_CARDINALITY,MIN_OCCURS | postvalidate:EMBEDDED_STRUCTURE_CARDINALITY,MIN_OCCURS |
| P.SP.02.MSG.017 |  | BodyValidationError:Body содержит 1 issue(s). |
| P.SP.02.MSG.020 | BodyValidationError:Body содержит 4 issue(s). | BodyValidationError:Body содержит 4 issue(s). |
| P.SP.02.MSG.021 | postvalidate:STRUCTURED_RULE_FAILED | postvalidate:STRUCTURED_RULE_FAILED |
| P.SP.02.MSG.031 | postvalidate:EMBEDDED_STRUCTURE_CARDINALITY,MIN_OCCURS | postvalidate:EMBEDDED_STRUCTURE_CARDINALITY,MIN_OCCURS |
| P.SP.02.MSG.052 | BodyValidationError:Body содержит 4 issue(s). | BodyValidationError:Body содержит 4 issue(s). |
| P.SP.02.MSG.057 | postvalidate:STRUCTURED_RULE_FAILED | postvalidate:STRUCTURED_RULE_FAILED |
| P.SP.02.MSG.059 | postvalidate:EMBEDDED_STRUCTURE_CARDINALITY,MIN_OCCURS | postvalidate:EMBEDDED_STRUCTURE_CARDINALITY,MIN_OCCURS |


These failures are why 24 historical `FULL_TRACE` requirement rows were downgraded from strict `DONE` to `FIX_MAPPING_OR_PROOF`.

## Pytest verification

- Focused P.CLS.027 + MSG001 policy: `17 passed in 1.53s`.
- Proof-completion pair: `1319 passed in 1.11s`.
- Full OP22 regression: `4446 passed in 116.90s`.
- Initial `eaeu_xml/tests`: `1 failed, 417 passed, 63519 subtests passed`; the only failure was a stale OP22-specific GUI assertion still expecting the old word `Условно` for `IPDocKindCode`.
- Targeted stale-assertion regression after update: `1 passed in 0.37s`.
- Final `eaeu_xml/tests`: `418 passed, 63519 subtests passed in 10.87s`.

## Graph refresh

`graphify update .` completed successfully. It rebuilt `graph.json` and `GRAPH_REPORT.md`. `graph.html` was left stale because the aggregated view has 5229 nodes and exceeds the configured 5000-node visualization limit; this does not affect the code graph data used by Graphify.

## Verification boundary

Green pytest suites are not treated as normative proof by themselves. Requirement status is based on the source-first six-dimension gate: exact normative source, production mapping, positive proof, negative proof, runtime proof, and real XML/body serialization proof where applicable.
