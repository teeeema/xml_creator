# OP32 / P.MM.06 — missing operations evidence

Baseline date: 2026-10-06. This is evidence only; `P.MM.06_OP_32/**` was not modified.

## P.MM.06.OPR.007

- Official name: **Проверка возможности опубликования сведений в едином реестре**.
- Normative evidence: `32_ОП.pdf`, p.28 point 48; p.29 Table 14; pp.31–32 Table 18.
- Procedure: `P.MM.06.PRC.002` — Представление в Комиссию сведений о регистрации медицинского изделия.
- Executor: Комиссия.
- Role: after `P.MM.06.OPR.005`, the Commission checks whether received registration information may be published under the applicable procedure.
- Direct TRN/MSG binding: **none** in the current transaction catalog. It is an internal Commission operation following processing of data delivered through `P.MM.06.TRN.002` (`MSG.002` → `MSG.004`).
- Current package: absent from `operations.yaml`; no transaction references it.
- Runtime impact: current transaction execution can still load because no transaction points to OPR.007, but the process operation catalog is normatively incomplete.
- Required future fix: add the operation with exact normative metadata in a separate production task, then update the package test that currently asserts OPR.007 is absent.
- Closure criterion: loader exposes OPR.007, metadata matches Table 18, process/package validation passes, and existing transaction behavior remains unchanged.

## P.MM.06.OPR.008

- Official name: **Опубликование сведений о регистрации медицинского изделия**.
- Normative evidence: `32_ОП.pdf`, p.28 point 49; p.29 Table 14; p.32 Table 19.
- Procedure: `P.MM.06.PRC.002`.
- Executor: Комиссия.
- Role: when OPR.007 establishes that publication is permitted, the Commission publishes the registration information in the unified register on the Union portal.
- Direct TRN/MSG binding: **none** in the current transaction catalog; it is an internal follow-up operation after OPR.007.
- Current package: absent from `operations.yaml`; no transaction references it.
- Runtime impact: same as OPR.007 — no immediate transaction lookup failure, but the normative operation inventory is incomplete.
- Required future fix: add OPR.008 in a separate production task and revise the catalog test that currently expects both operations to be absent.
- Closure criterion: loader exposes OPR.008, metadata matches Table 19, process/package validation passes, and no transaction behavior regresses.
