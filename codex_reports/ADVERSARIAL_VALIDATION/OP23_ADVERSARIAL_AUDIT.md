# OP23 / P.SP.03 — Negative Validation QA

Scope: functional QA of the local validator against canonical requirements. No project implementation or tests were changed.

## Result

- Negative test cases recorded: 11
- EXPECTED_REJECT_AND_REJECTED: 10
- UNEXPECTED_ACCEPTANCE: 1
- CANNOT_TEST_MISSING_EVIDENCE: 0
- ENGINE_NOT_REACHED: 0
- RUNTIME_ERROR: 0

## Confirmed unexpected acceptance

Canonical requirement: `P.SP.03.MSG.001.REQ.010`.

Normative source: `ОП_23.pdf`, PDF page 342, Table 16 item 10.

Normative requirement: `csdo:DocId` inside `ipcdo:ApellationOfOriginApplicationDetails` must be filled.

Original valid XML condition: `csdo:DocId` contains a document identifier.

Modified test XML: the value was replaced by an empty `<csdo:DocId/>` element.

EXPECTED: REJECT.

ACTUAL: ACCEPT.

Rule expected to catch it: `P.SP.03.MSG.001.REQ.010`.

Why it escaped: the extracted path exists with value `None`, and the shared `presence REQUIRED` implementation tests dictionary-key membership only.

Severity: HIGH.

## Successful rejection controls

Selected real-XML tests confirmed rejection of:

- invalid `CommunicationChannelCode` outside `TE/EM/FX` (`P.SP.03.MSG.001.REQ.008`, p.342, Table 16 item 8);
- one application instead of two (`P.SP.03.MSG.003.REQ.001`, p.351, Table 17 item 1);
- cross-instance `DocId` mismatch under the same requirement;
- invalid/equal datetime ordering (`P.SP.03.MSG.003.REQ.003`, p.352, Table 17 item 3);
- duplicate attachment kind codes without a distinguishing document value (`P.SP.03.MSG.011.REQ.048`, p.255, Table 20 item 48);
- no identifier or more than one mutually exclusive identifier in `P.SP.03.MSG.025` (`REQ.002-.004`, p.288, Table 29);
- conditional required `PatentAttorneyId` missing when party kind is `PA` (`P.SP.03.MSG.009.REQ.025`);
- `DutyPaymentIndicator=true` with non-zero amount (`P.SP.03.MSG.024.REQ.021`, p.287);
- `DutyPaymentIndicator=false` with a non-positive amount (`P.SP.03.MSG.024.REQ.022`, p.287).

The selected OP23 run produced `59 passed, 571 deselected`; the dedicated `REQ.021` control produced `1 passed`.

## Traceability note

Canonical metadata for some requirements is stale relative to the current runtime. For example `P.SP.03.MSG.011.REQ.048` still reports `OPEN_PRODUCTION_MAPPING`, while current production rules and real-XML regression tests execute and reject the negative case. This audit did not edit KB metadata.

## OP23 verdict

The sampled structural, enum, equality, date, uniqueness, identifier exclusivity, and conditional rules behave correctly. The same empty-required-element defect found in OP22 remains reproducible in OP23.

