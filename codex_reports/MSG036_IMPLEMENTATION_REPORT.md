# MSG036 implementation report

## Scope

Implemented only `P.SP.02.MSG.036` in `R.IP.SP.02.002` from the independently
read Table 54 (ОП_22.pdf, pages 750–751).  No MSG035 file was changed.

## Mapping

- Table 54 REQ1 is an exact one-instance `TrademarkApplicationDetails` rule.
- REQ2 and REQ3 are marked `SAFE_PARTIAL`: local presence of
  `IPDocKindCode` and `TrademarkApplicationId` is executable; classifier
  correspondence and the national patent-office resource remain external.
- REQ4 requires one or more direct `AccompanyingDocumentsDetails` and all six
  required children per direct document instance.
- REQ5 forbids root `RefusalDetails` by exact QName cardinality.
- REQ6–29 retain dual Table 54/Table 44 source provenance and their existing
  local executable semantics.
- REQ30 requires, and REQ31 forbids, the respective validity-period date per
  `ResourceItemStatusDetails` owner.

The complete 31-requirement inventory has counts: FULLY_MAPPABLE 22,
SAFE_PARTIAL 2, AMBIGUOUS 1, ENGINE_UNSUPPORTED 6, EXTERNAL 0,
SOURCE_CONFLICT 0.  The arithmetic is 31/31.  Unsupported or ambiguous
requirements have no executable rule.

## Verification

`PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests/test_msg036_*.py -p no:cacheprovider`

`8 passed in 0.24s`

The tests cover safe mapping classification, direct-document repeatability
with `[good, good]`, `[missing, good]`, and `[good, missing]`, exact QName
ownership, and build → serialize → parse → extract → rebuild semantic
roundtrip validation.

`PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests -p no:cacheprovider`

`1461 passed in 45.27s`

`git diff --check` completed without output.

## Repository state

The worktree contained concurrent pre-existing changes.  This task changed
only the MSG036 mapping and its three MSG036 tests, plus this report.

VERDICT: READY
