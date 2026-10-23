# CONTROL_VERIFICATION — independent CASE 3–4 evidence

Date: 2026-10-21. Workspace: `/Users/tema/Documents/Work/xml_creator`.
The original PDFs and the local Knowledge Base were read before runtime
probing. The checks below use the actual application facade, package validator,
serializer, XML parser and structured-rule evaluator. This agent did not edit
the shared control CSV/report or production normative mapping files.

## CV-03: OP22 / P.SP.02.TRN.022 / P.SP.02.MSG.027 / Table 57 REQ.2–3

**Result: FAIL; source is available.** Decision No. 92, physical PDF p. 15,
updated by No. 148, physical PDF p. 4, has `P.CLS.027` code `07365` for the
notification of a withdrawn trademark application. Table 57 of `ОП_22.pdf`,
physical PDF pp. 578–579, requires Code on the classifier-present branch and
omits Name. The local snapshot already includes `07365`.

Real `get_form()` returns `IPDocKindCode` and `IPDocKindName` as editable fields,
with `fixed_value=None`, `effective_message_policy=None`; effective resolver
returns no entry for either field. Existing conditional
`P.SP.02.MSG.027.T57.REQ.2` rejects Code+Name but checks presence of Code,
not equality with `07365`. Existing `T57.REQ.3` incorrectly leaves the old
no-code/Name-only path valid even though the classifier is now populated.

After build→serialize→parse→extract→validate:

| Scenario | Observed Code / Name | Actual validity | Normative result |
|---|---|---|---|
| positive | `07365` / absent | valid | valid |
| wrong_code | `99999` / absent | **valid** | invalid, `T57.REQ.2` |
| code_and_name | `07365` / present | invalid, `T57.REQ.2` | invalid |
| missing_code | absent / absent | invalid, `T57.REQ.3` | invalid |
| legacy_fallback | absent / full fallback name | **valid** | invalid in current classifier revision |

## CV-04: OP22 / P.SP.02.TRN.003 / P.SP.02.MSG.004 / Table 38 REQ.2–3

**Result: FAIL; proposed `STILL_EXTERNAL` classification is disproven.**
The authoritative Decision No. 92, physical PDF p. 13, amended by No. 148,
physical PDF p. 3, contains **`07320`**, corresponding to the interested
party's objection under Article 8. Table 38 (`ОП_22.pdf`, physical PDF
pp. 532–533) consequently uses classifier-present `REQ.2`. The local
`P.CLS.027` snapshot *omits* `07320`; snapshot omission is not absence from
the authoritative classifier.

Real `get_form()` leaves Code/Name user-editable and has no fixed, forbidden
or effective resolver policy. Neither `REQ.2` nor `REQ.3` is executable in the
current structured-rule set. Build→serialize→parse→extract→validate succeeds
for Code=`07320`/Name absent, but also incorrectly succeeds for Code=`99999`,
Code+Name, both fields missing, and the previous fixture with neither field.

## Tests and actual XML

`PYTHONPATH=eaeu_xml/src python3.13 codex_reports/OP22_P_SP_02/CONTROL_VERIFICATION/runtime_evidence/op22_branch_runtime.py`

- All **10 actual XML files** (`op22_branch_CASE3_*.xml`,
  `op22_branch_CASE4_*.xml`) were serialized and reparsed; no extraction errors
  occurred in the recorded scenarios. See
  `op22_branch_CASE3_CASE4_baseline.json` for actual rule IDs/status and hashes.
- `PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q codex_reports/OP22_P_SP_02/CONTROL_VERIFICATION/runtime_evidence/op22_branch_test.py --tb=short`:
  **4 passed, 6 failed**, as expected from confirmed normative discrepancies.
- Existing positive fixture checks for MSG.027 and MSG.004:
  **2 passed in 0.19s**. Their green state demonstrates the missing negative
  coverage, not normative correctness.
- `python3.13 -m py_compile` for the two evidence Python files: passed.
- `git diff --check`: passed (working tree is dirty from parallel work).
- Sources, original PDF page numbers, checksum and extracted textual snippets:
  `op22_branch_source_trace.json`.

## Minimal correction supported by sources

Update only OP22 classifier snapshot (`07320`), MSG.027/MSG.004 message-field
policies and corresponding structured validator rules to enforce `07365`/
`07320` FIXED Code and FORBIDDEN Name, respectively. The earlier fallback
branch must not validate in the current classifier revision. Align the two
message-specific fixtures with the effective classifier before rerunning the
focused acceptance tests and nearby OP22 regression.

**This independent evidence pass did not change production code; both cases
remain FAIL until the documented acceptance tests pass after correction.**
