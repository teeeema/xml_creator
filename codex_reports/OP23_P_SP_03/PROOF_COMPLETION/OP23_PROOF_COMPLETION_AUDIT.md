# OP23 Proof Completion Audit

STATUS: **PARTIAL — closure plan complete; independent subagent execution blocked by runtime limits.**

## Scope

Audited the **142** rows with `current_verdict=MAPPED_TEST_PROOF_MISSING` from `OP23_EXISTING_RULES_NEEDING_PROOF.csv`. The same source file also contains two B1 semantic-partial rows (`MSG.023.REQ.019`, `MSG.024.REQ.019`); those are excluded from the 142 proof-completion count and reviewed separately in `OP23_B1_5MB_CAPABILITY_REVIEW.md`.

The audit does not treat a green package suite as requirement-level proof. Proof is accepted only when the live test exercises the current production `rule_id` through real XML extraction and the production validator, and explicitly observes PASS and the intended rule-specific failure.

## Root finding

The input proof report is stale relative to the live tests. **141/142** requirements already have current requirement-level positive, negative, and runtime/real-XML proof. Their missing artifact is the proof/report linkage, not a new test.

Exactly one requirement still has a substantive proof gap: **P.SP.03.MSG.013.REQ.001**. Its live production rules are `P.SP.03.MSG.013.REQ.001.cardinality;P.SP.03.MSG.013.REQ.001.resource_kind`, but no current requirement-specific test explicitly proves either rule.

## Evidence model

`P.SP.03_OP_23/tests/test_b1_production.py` validates documents by loading `EaeuXmlEngine`, extracting values with `body_provider._values_from_element(...)`, and calling `engine.validate_body(...)`. `_assert_rule_passes(...)` additionally requires a `PASS` evaluation for the exact `rule_id`; `_assert_rule_fails(...)` requires `STRUCTURED_RULE_FAILED` for the exact `rule_id`.

A read-only runtime probe wrapped only those two test helpers in memory and ran the unchanged test file. Result: **631 passed**. The trace recorded **459 exact-rule positive helper calls** and **427 exact-rule negative helper calls**. For 21 MSG.013/MSG.014 requirements the negative branch is written inline instead of via `_assert_rule_fails`; those tests mutate the real XML, call `_validate_document(...)`, and compare the issues to the exact single expected tuple `("STRUCTURED_RULE_FAILED", rule)`. They therefore count as direct negative runtime proof.

## Classification

- `POSITIVE_MISSING`: **1** canonical requirement (`P.SP.03.MSG.013.REQ.001`).
- `NEGATIVE_MISSING`: **1** canonical requirement (same requirement).
- `RUNTIME_MISSING`: **1** canonical requirement (same requirement; runtime proof closes together with the missing real-XML test).
- `SOURCE_LINK_MISSING`: **0**. All 142 source rows currently say `rule_source_ref_correct=YES`.
- `ONLY_REPORT_LINK_MISSING`: **141**.

Because the same one row lacks positive, negative, and explicit runtime proof, it is classified as `MULTIPLE_PROOF_MISSING`; it is not counted three times in the mutually exclusive summary.

## Minimal closure

For **141** requirements: do not add tests. Update/rebuild the proof matrix so each canonical requirement links to the existing pytest nodeid(s) listed in `OP23_PROOF_COMPLETION_PLAN.csv` and records the exact rule-level PASS/FAIL evidence.

For **P.SP.03.MSG.013.REQ.001**: add one compact parameterized real-XML regression test covering both current rule IDs. The positive document must contain exactly two register items with equal `ResourceItemKindCode`. Negative case 1 removes the second register item (`.cardinality`); negative case 2 changes the second `ResourceItemKindCode` (`.resource_kind`). Each negative case must assert `STRUCTURED_RULE_FAILED` for the exact rule ID. No production mapping change is needed.

A separate runtime matrix is not needed: the accepted tests already execute the XML parser/extractor and production validator. The one missing requirement should gain runtime proof as part of its new requirement-specific real-XML test.

## Multi-agent execution status

Four required read-only roles were dispatched through the available multi-agent mechanism (positive, negative, runtime/XML, B1 semantic review). All were terminated by the environment before producing findings with: `ChatGPT Web supports at most 5 simultaneous browser turns`. A second read-only CLI-agent route was attempted; Web-model runs hit the same concurrency limit, and the alternate model route was rejected with: `The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account.`

Therefore no subagent conclusion is represented as evidence in this report. The classification above is the root agent's direct read-only audit backed by the live test trace.

## Verification

Executed without modifying production/tests/KB:

- requirement-level trace run: `P.SP.03_OP_23/tests/test_b1_production.py` — **631 passed**; in-memory probe recorded exact `rule_id` positive/negative helper calls.
- full OP23 regression suite: `P.SP.03_OP_23/tests` — **634 passed, 27 subtests passed**. This full-suite result is regression context only and is not used as proof for any individual requirement.

## Final counts

```text
TOTAL_PROOF_MISSING: 142
ONLY_POSITIVE_MISSING: 0
ONLY_NEGATIVE_MISSING: 0
ONLY_RUNTIME_MISSING: 0
MULTIPLE_PROOF_MISSING: 1
LINK_ONLY_PROBLEM: 141

CAN_CLOSE_WITH_EXISTING_TESTS: 141
NEEDS_NEW_TEST: 1
NEEDS_RUNTIME_MATRIX: 0
```

## Requested final status

```text
STATUS: PARTIAL_MULTI_AGENT_RUNTIME_BLOCKED

TOTAL_PROOF_MISSING: 142

ONLY_POSITIVE_MISSING: 0
ONLY_NEGATIVE_MISSING: 0
ONLY_RUNTIME_MISSING: 0
MULTIPLE_PROOF_MISSING: 1
LINK_ONLY_PROBLEM: 141

CAN_CLOSE_WITH_EXISTING_TESTS: 141
NEEDS_NEW_TEST: 1
NEEDS_RUNTIME_MATRIX: 0

B1_5MB_ENGINE_CAPABILITY: MISSING_GENERIC_DECODED_BINARY_BYTE_LENGTH_PRIMITIVE
B1_5MB_IMPLEMENTATION_NEEDED: YES_GENERIC_ENGINE_PRIMITIVE_PLUS_RULE_MAPPING_AND_BOUNDARY_TESTS
B1_5MB_NORMATIVE_EVIDENCE: CONFIRMED_OP23_P286_TABLE27_ITEM19_AND_P287_TABLE28_INHERITANCE; EXACT_BYTE_MULTIPLIER_UNRESOLVED

PRODUCTION_CHANGED: 0
TESTS_CHANGED: 0
KB_CHANGED: 0
```
