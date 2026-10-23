# P.SP.02.MSG.001 — GUI / validator comparison

## Coverage

- Table 34 business requirements: **39**.
- Requirements with at least one executable structured rule: **34/39**.
- Requirements without an executable structured rule: **5** — P.SP.02.MSG.001.REQ.004, P.SP.02.MSG.001.REQ.005, P.SP.02.MSG.001.REQ.013, P.SP.02.MSG.001.REQ.027, P.SP.02.MSG.001.REQ.032.
- Requirements whose existing structured mapping is explicitly `PARTIAL`: **3** — P.SP.02.MSG.001.REQ.003, P.SP.02.MSG.001.REQ.030, P.SP.02.MSG.001.REQ.038.
- Combined validator coverage gaps requiring external/source follow-up: **8**.

## Consistency result

The prototype does not change shared rules-engine semantics. For fields governed by existing executable rules, the GUI policy is applied before validation/generation: forbidden inputs are dropped, fixed values are forced, required fields are marked, and conditional fields remain conditional. No post-implementation contradiction was identified between an executable MSG.001 structured rule and the effective GUI policy.

The remaining items are validator/source coverage gaps rather than GUI-versus-validator contradictions. The five requirements without executable structured rules are intentionally represented as conditional/source-dependent policy where appropriate. The three partial mappings keep their external or source-structure limitation explicit.

## Known gaps

1. REQ.003 — required application id is executable, but uniqueness against Commission resources is an external check.
2. REQ.004 / REQ.005 — Decision No. 92 classifier branch is unresolved; no fake code/name branch is selected.
3. REQ.013 — AP/PA/RE instance-specific semantics conflict with a single flat path; no global AP fixed value is forced.
4. REQ.027 — colour/description requirement retains the source conflict.
5. REQ.030 — confirmed forbidden GoodsBaseDetails fields are enforced; `InconsistencyText` has a source/structure path conflict and is not globally forbidden at another path.
6. REQ.032 — Decision No. 184 classifier dependency remains unresolved.
7. REQ.038 — StartDateTime is required, but equality with the national-register timestamp is external and remains outside the local validator.

No shared rules-engine behavior was modified.
