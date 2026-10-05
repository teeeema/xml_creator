# MSG041 IMPLEMENTATION REPORT

## STATUS

COMPLETE

## VERDICT

READY

## CHANGED_FILES

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.041.yaml` — added executable structured rules and complete mapping audit for P.SP.02.MSG.041.
- `P.SP.02_OP_22/tests/test_msg041_safe_mapping.py` — validates inventory, classification, executable/unmapped sets, provenance, rule ownership, critical fixed values, and MSG041/MSG042 isolation.
- `P.SP.02_OP_22/tests/test_msg041_repeatable_xml.py` — validates cardinality, direct-owner status semantics, REQ27 same-parent behavior, REQ30 repeatability, validity ownership, signature mutual exclusion, and officer fields.
- `P.SP.02_OP_22/tests/test_msg041_end_to_end.py` — validates production build → serialize → parse → extraction → validation, transaction metadata, MSG041-specific negative proofs, inherited executable negative proofs, wrong-owner behavior, and message isolation.
- `codex_reports/MSG041_IMPLEMENTATION_REPORT.md` — this report.

## IMPLEMENTATION

Implemented only the approved MSG041 subset from `codex_reports/MSG041_PREP.md`.

Key executable behavior:

- REQ1: exactly one direct `ipcdo:TrademarkApplicationDetails`.
- REQ4: safe partial direct `ipsdo:TrademarkApplicationId` presence only.
- REQ5: direct application status owner required; `csdo:StatusCode == "02"`; `StatusCode/@codeListId` forbidden.
- REQ6–12, REQ14–15, REQ21–25, REQ27–29: inherited Table 44 executable subset with Table 59 + Table 44 provenance.
- REQ30: same-`TrademarkDetails` `ipsdo:CollectiveMarkIndicator == "0"`.
- REQ31: same resource-status validity `StartDateTime` required.
- REQ32: same resource-status validity `EndDateTime` forbidden.
- REQ33–35: signature presence/mutual exclusion and direct signature-owned officer requirements with same-parent scoping.
- REQ26 remains unmapped; no OR-as-AND approximation was introduced.

No shared Python, StructureDefinitions, classifiers, source_refs, process metadata, or MSG042 files were modified by this task.

## MAPPING_COUNTS

- captured = 12
- expanded = 35
- FULL = 25
- SAFE_PARTIAL = 1
- EXTERNAL = 2
- AMBIGUOUS = 1
- ENGINE_UNSUPPORTED = 6
- SOURCE_CONFLICT = 0
- executable codes = 26
- structured-rule object count = 29

Arithmetic:

`25 + 1 + 2 + 1 + 6 = 35`

Executable requirement codes:

`1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35`

## UNMAPPED_REQUIREMENTS

Exact unmapped set:

`2, 3, 13, 16, 17, 18, 19, 20, 26`

- REQ2–3: EXTERNAL.
- REQ13: AMBIGUOUS.
- REQ16–20: ENGINE_UNSUPPORTED.
- REQ26: ENGINE_UNSUPPORTED exact TrademarkKindCode OR TrademarkKindName semantics.

## NORMATIVE_BASIS

CONFIRMED — implementation authority: `codex_reports/MSG041_PREP.md`.

The PREP confirms Table 59, inherited Table 44 REQ6–29, message P.SP.02.MSG.041, transaction P.SP.02.TRN.036, procedure P.SP.02.PRC.018, operations P.SP.02.OPR.072 → P.SP.02.OPR.073, actors P.SP.02.ACT.001 → P.SP.02.ACT.002, response P.SP.02.MSG.002, structure R.IP.SP.02.002, StatusCode `"02"`, CollectiveMarkIndicator `"0"`, Start required, End forbidden, and signature REQ33–35 semantics.

No new normative audit was performed.

## MSG041_TESTS

Command:

`PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests/test_msg041_*.py -p no:cacheprovider`

Result:

`55 passed in 1.89s`

Coverage includes:

- exact inventory/arithmetic and unmapped set;
- REQ1 0/1/2 cardinality;
- REQ4 missing direct ApplicationId;
- REQ5 missing/wrong/listed/wrong-owner status;
- negative proof for every inherited executable requirement;
- REQ26 absence from executable mappings;
- REQ27 same-parent proof;
- REQ30 `0` pass / `1` fail / missing fail / wrong-owner fail / repeated-owner matrix;
- REQ31 missing and wrong-owner StartDateTime;
- REQ32 governed-owner EndDateTime forbidden;
- REQ33–35 same-signature mutual exclusion, required officer fields, forbidden CommunicationDetails, and same-parent scoping;
- production build → serialize → parse → extract → validate;
- MSG041/MSG042 rule isolation.

## OPTIONAL_FULL_REGRESSION

NOT RUN.

Per task instructions, full OP22 regression was not required while MSG042 is being modified concurrently.

## CONCURRENT_CHANGES

Concurrent MSG042 changes were detected in:

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.042.yaml`
- `P.SP.02_OP_22/tests/test_msg042_safe_mapping.py`
- `P.SP.02_OP_22/tests/test_msg042_repeatable_xml.py`
- `P.SP.02_OP_22/tests/test_msg042_end_to_end.py`

They were treated as foreign concurrent work and were not modified by this task.

## GIT_DIFF_CHECK

Command:

`git diff --check`

Result:

PASS — no whitespace errors reported.

Diff inspection was limited to the allowed MSG041 files. Critical facts rechecked from the resulting rule file:

- StatusCode fixed value = `"02"`
- CollectiveMarkIndicator fixed value = `"0"`
- executable codes exactly match the approved 26-code set
- REQ26 has no executable rule

## REMAINING_ISSUES

None.
