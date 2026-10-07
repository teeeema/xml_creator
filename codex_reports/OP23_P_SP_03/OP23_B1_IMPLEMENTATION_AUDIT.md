# OP23 B1 — WAVE 2 final audit 2026-10-07

## STATUS

`B1_SIMPLE_PRESENCE_AND_COMPARISON` is deterministically reproduced as exactly **162** canonical requirements. All **162/162** have current production structured-rule wiring and requirement-specific real-XML coverage. `OP23_B1_IMPLEMENTATION_RESULTS.csv` contains **162 CLOSED_CONFIRMED, 0 NOT_PROCESSED**.

## MAPPING

The safe batch map contains 608 unique candidates:

- B1: 162
- B2: 214
- B3: 159
- B4: 73

The remaining 102 of 710 canonical OP23 requirements remain outside the safe batches: 44 classifier, 39 external registry, 18 source conflict, 1 missing normative data. No blocked item was moved into B1 to match the expected count.

## MSG.022

MSG.022 contributes six B1 canonical requirements: REQ.001, REQ.002, REQ.006, REQ.007, REQ.008 and REQ.009.

Before the fix the B1 suite reproduced **617 passed, 14 failed**. All 14 failures occurred while constructing the positive MSG.022 baseline, before the intended negative mutation.

The root cause was shared generator behavior. REQ.007 requires `ipcdo:IPPaymentDetails` and at least one account complex group. A `for_each` `condition.any` with `ccdo:BankAccountDetails NE null` or `ccdo:PaymentSystemAccountDetails NE null` could not previously choose and materialize a complex branch with its required descendants.

The generator now materializes one structurally present complex alternative and its required children. Structural presence is tracked separately from generic cardinality selection, preserving the established cardinality representation. The old MSG.022 helper payment/account fallback was removed, and the focused MSG.022 suite still passes **14/14**.

Trace for the affected normative requirement:

OP23 → P.SP.03.PRC.008 → P.SP.03.TRN.017 → P.SP.03.MSG.022 → REQ.007 → R.IP.SP.03.003 → `ipcdo:IPPaymentDetails` → `ccdo:BankAccountDetails` / `ccdo:PaymentSystemAccountDetails`.

Confirmed source: `ОП_23.pdf`, version context `P.SP.03 1.0.0`, Table 26, PDF page 283, item 7 (`CONFIRMED_PDF` in the current KB).

## VERIFICATION

- Shared generator root-cause regressions: **2 passed**.
- MSG.022 focused: **14 passed**.
- OP23 B1: **631 passed**.
- Full OP23: **634 passed, 27 subtests passed**.
- Shared engine/application tests: **398 passed, 62250 subtests passed**.
- WAVE 1 original six: **6 passed**.
- WAVE 1 focused: **12 passed**.
- GUI: **22 passed**.
- OP22: **3110 passed**.
- OP26: **93 passed, 83 subtests passed**.

## SAFETY

- Validator weakened: **NO**.
- Production message-specific hardcode added: **NO**.
- Shared generator/application layer changed: **YES**.
- GUI changed by WAVE 2: **NO**.
- Knowledge Base changed by WAVE 2: **NO**.
