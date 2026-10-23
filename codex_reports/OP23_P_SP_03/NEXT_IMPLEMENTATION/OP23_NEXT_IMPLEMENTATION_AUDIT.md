# OP23 / P.SP.03 — Next Implementation Audit

## Status

- TARGET_QUEUE: **126**
- REVERIFIED_SAFE: **27**
- IMPLEMENTED: **27 canonical requirements / 42 structured subrules**
- CLOSED_POSITIVE_NEGATIVE_RUNTIME: **27**
- RECLASSIFIED_BLOCKED: **99**
- FAILED: **0**
- MAPPED_BEFORE: **474**
- MAPPED_AFTER: **501**
- BLOCKED_BEFORE_KNOWN: **110**
- NEW_BLOCKERS_FOUND: **99**
- BLOCKED_AFTER: **209**
- B1_PARTIAL_5MB_STATUS: **PARTIAL_UNRESOLVED — unchanged; MSG.023/024 REQ.019 5MB semantics not invented**
- SHARED_ENGINE_CHANGED: **0**
- GUI_CHANGED: **0**
- KB_CHANGED: **0**

## Normative basis

CONFIRMED. Every implemented rule carries the target message source refs from ОП_23.pdf. No source_ref was fabricated. The queue was reverified against the KB-first evidence and the original OP23 source where needed.

The implementation boundary changed during reverification: rows that require semantic identification of named IP document kinds cannot be closed without the authoritative Decision No. 92 classifier payload/version and code→name mapping. Two date-ordering rows require typed DATE support. MSG.004/011 REQ.007 require conditional cross-instance evaluation. MSG.004/011 REQ.034 additionally needs order-independent set equivalence.

MSG.015.REQ.007 was moved from the provisional blocked set into SAFE after final source review: MSG.015 requires exactly two register items (table 24, p.279), and inherited MSG.011.REQ.007 (table 20, p.239) requires both EAEU IDs to be present/equal; therefore unconditional cross-instance equality is valid for MSG.015.

## Implemented canonical requirements

- **P.SP.03.MSG.004**: 001, 002, 003, 036, 037
- **P.SP.03.MSG.006**: 023, 042
- **P.SP.03.MSG.007**: 023
- **P.SP.03.MSG.008**: 023
- **P.SP.03.MSG.011**: 001, 002, 003, 036, 037
- **P.SP.03.MSG.014**: 001, 003, 004, 006, 007, 015, 023, 036
- **P.SP.03.MSG.015**: 001, 003, 007, 035, 036

## Reclassified blockers

- **BLOCKED_CLASSIFIER_AND_SET_EQUIVALENCE**: 2
- **BLOCKED_CLASSIFIER_NO_AUTHORITATIVE_CODE_NAME_MAPPING**: 93
- **ENGINE_CAPABILITY_GAP_CONDITIONAL_CROSS_INSTANCE**: 2
- **ENGINE_CAPABILITY_GAP_DATE**: 2

Per-requirement evidence and reasons are in `OP23_RECLASSIFIED_BLOCKED.csv`. No blocked requirement was approximated in production rules.

## Runtime proof

- `python3.13 -m pytest P.SP.03_OP_23/tests/test_next_implementation.py -q` → **42 passed in 7.48s**.
- `python3.13 -m pytest P.SP.03_OP_23/tests/test_psp03_package.py -q` → **3 passed, 27 subtests passed in 2.49s**.
- `python3.13 -m pytest P.SP.03_OP_23/tests -q` → **676 passed, 27 subtests passed in 132.73s**.
- `python3.13 -m pytest eaeu_xml/tests/test_structured_rules.py -q` → **49 passed, 5 subtests passed in 0.11s** (shared engine unchanged).

Exact rule IDs and pytest nodeids for the 42 positive+negative real-XML proofs are in `OP23_NEXT_RUNTIME_PROOF.csv`.

## Remaining issues

1. Obtain the authoritative Decision No. 92 classifier payload/version/code→name mapping before implementing classifier-dependent rows.
2. Add shared-engine typed DATE comparison in a separate authorized wave before closing MSG.007.REQ.036 and MSG.014.REQ.039.
3. Add conditional cross-instance support before closing MSG.004/011 REQ.007.
4. Establish order-independent set-equivalence support/evidence before closing MSG.004/011 REQ.034.
5. Resolve the pre-existing B1 5MB semantics for MSG.023/024 REQ.019 separately.
