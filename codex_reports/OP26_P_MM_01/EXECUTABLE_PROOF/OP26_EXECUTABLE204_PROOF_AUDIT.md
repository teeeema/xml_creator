# OP26 EXECUTABLE 204 PROOF RECONCILIATION

Date: 2026-10-13  
Process: `P.MM.01` / OP26  
Mode: READ/TEST wave; production rules, engine and Knowledge Base unchanged.

## Inventory

- Canonical total: **239**.
- Executable canonical target: **204**.
- Current production rule entries behind those 204 requirements: **252**.
- Confirmed blocked requirements: **35**.
- Executable/blocker overlap: **0**.
- Reconciled union: **239**.

## Requirement-level proof result

- Production mapping: **204/204 linked**.
- Source linkage: **204/204 CONFIRMED** in current production `source_refs`.
- Positive proof: **204/204 canonical requirements**, covering **252/252 production rule entries**.
- Negative proof: **204/204 canonical requirements**, covering **252/252 production rule entries**.
- Runtime rule evaluation: **204/204 PASS** through `EaeuXmlEngine.validate_body(..., mode=TEST)` using the existing OP26 transaction fixture.
- Real XML/body proof: **113/204 PASS**.
- Real XML/body proof missing: **91/204** because the whole message is blocked before serialization by already-known message-level normative/classifier issues.

Strict verdict counts:

- `FULL_PROOF`: **113**.
- `PROOF_LINK_ONLY`: **0**.
- `NEW_NEGATIVE_TEST_REQUIRED`: **0**.
- `NEW_POSITIVE_TEST_REQUIRED`: **0**.
- `RUNTIME_PROOF_MISSING`: **91**.
- `SEMANTIC_REVIEW_REQUIRED`: **0** within the executable-204 queue.

`FULL_PROOF` here means requirement-level executable proof in the current TEST/runtime path: production mapping + confirmed source link + deterministic positive/negative evaluator proof + engine runtime PASS + serialized body XML. It does **not** claim package-wide XSD/model-version closure. Concrete XSD bytes/imported model versions remain unresolved at package level for all affected messages.

## Real XML gaps

- `P.MM.01.MSG.002`: **78** executable canonical requirements. Current validation includes `NORMATIVE_CONFLICT-001` and `CLASSIFIER_DATASET_NOT_AVAILABLE`.
- `P.MM.01.MSG.023`: **7** executable canonical requirements. Current validation includes `NORMATIVE_CONFLICT-002`, `NORMATIVE_CONFLICT-003` and `CLASSIFIER_DATASET_NOT_AVAILABLE`.
- `P.MM.01.MSG.024`: **6** executable canonical requirements. Current validation includes `NORMATIVE_CONFLICT-004`, `NORMATIVE_CONFLICT-005` and `CLASSIFIER_DATASET_NOT_AVAILABLE`.

The 91 rows are not failed executable rules: every target rule evaluates `PASS` at runtime. They remain open only for the real-XML serialization leg because `build_body()` correctly refuses a message that still contains unrelated blocking issues.

## Blocked 35 confirmation

- Classifier membership: **11**.
- External registry: **11**.
- Source/structure conflict: **9**.
- Other: **4** = 1 truncated normative requirement + 3 unknown semantic `другое` codes.
- Blocked requirements present in executable rules: **0**.
- Blocked requirements present in executable proof matrix: **0**.
- New implementable queue: **0**.

## Proof implementation

`P.MM.01_OP_26/tests/test_executable204_proof.py` adds only deterministic proof/regression tests. It does not change production YAML or the shared engine.

The proof test:

1. reconciles `204 executable + 35 blocked = 239 canonical` with zero overlap;
2. exercises every one of the 252 production rule entries with a positive and a deliberately failing negative vector;
3. confirms every rule carries `CONFIRMED` source refs;
4. executes every canonical rule through `EaeuXmlEngine.validate_body()` on the existing OP26 fixture;
5. serializes and reparses body XML where current message-level validation permits it;
6. asserts the known real-XML gap explicitly for MSG.002/023/024 instead of bypassing their blockers.

Existing proofs for empty REQUIRED values, invalid `DrugApplicationKindCode=TEST`, invalid `CountryKindCode=TEST`, and the MSG.023/024 runtime6 fixture remain in their existing tests and were not duplicated as production behavior.

## Verification

- Focused executable proof: `PYTHONPATH=eaeu_xml/src pytest -q P.MM.01_OP_26/tests/test_executable204_proof.py` -> **661 passed**.
- Full OP26: `PYTHONPATH=eaeu_xml/src pytest -q P.MM.01_OP_26/tests` -> **853 passed, 83 subtests passed**.
- `git diff --check`: **PASS**.

## Change boundaries

- Production YAML changed by this wave: **0**.
- Shared engine changed by this wave: **0**.
- Knowledge Base changed by this wave: **0**.
- Other OP packages changed by this wave: **0**.

## Next action

Do not add more executable-proof tests for the current 204. The remaining proof gap is the real-XML leg for 91 executable requirements in MSG.002/023/024 and requires resolution of the existing normative/classifier blockers. The separate 35 blocked requirements remain outside the executable queue until new official evidence is available.
