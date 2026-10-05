# MSG052 Implementation Report

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.052.yaml` — implemented structured rules and completed mapping audit for P.SP.02.MSG.052.
- `P.SP.02_OP_22/tests/test_msg052_safe_mapping.py` — verifies authoritative mapping classification, provenance, owner/QName targets, and unmapped requirements.
- `P.SP.02_OP_22/tests/test_msg052_repeatable_xml.py` — verifies role-scoped, order-independent repeatable-record behavior and same-parent semantics.
- `P.SP.02_OP_22/tests/test_msg052_end_to_end.py` — verifies build/serialize/parse/extract/validate roundtrip, negative cases, and message isolation.
- `codex_reports/MSG052_IMPLEMENTATION_REPORT.md` — this report.

## IMPLEMENTATION
P.SP.02.MSG.052 now contains executable structured rules for the authoritative FULLY_MAPPABLE and SAFE_PARTIAL requirements while leaving ENGINE_UNSUPPORTED requirements unmapped.

Role ownership is selected by same-record `StatusCode` semantics:
- cancellation record: `StatusCode == "04"`;
- new-registration record: `StatusCode == "01"`.

No positional record binding is used.

REQ23 was corrected to the actual R.IP.SP.02.007 ownership path:
`RegistrationCancellationDetails/ComplaintInvalidateProtectionTrademarkDetails`, with both cancellation decision codes evaluated inside that same status-04 record.

Inherited Table 49 rules REQ6-17 retain dual provenance from Table 70 and Table 49. REQ29-31 enforce signature presence, mutually exclusive officer/direct-name branches, and officer-name/position requirements within the same signature parent.

## MAPPING_COUNTS
- Captured source rows: 18
- Expanded requirements: 31
- FULLY_MAPPABLE: 19
- SAFE_PARTIAL: 6
- ENGINE_UNSUPPORTED: 6
- EXTERNAL: 0
- AMBIGUOUS: 0
- SOURCE_CONFLICT: 0

FULLY_MAPPABLE:
`{1,2,4,6,7,8,9,10,11,12,13,14,15,16,17,23,29,30,31}`

SAFE_PARTIAL:
`{5,20,25,26,27,28}`

ENGINE_UNSUPPORTED:
`{3,18,19,21,22,24}`

## PARTIAL_REMAINDERS
- REQ5: cancellation-role TrademarkId presence is enforced; the remaining external semantic portion is retained as non-executable.
- REQ20: new-registration-role TrademarkId presence is enforced; cross-record uniqueness remains external.
- REQ25-28: role-scoped document-kind branch logic is executable; classifier-dependent validation remains external.
- REQ26 fallback literal is exact and case-sensitive:
  `Решение об аннулировании регистрации товарного знака, знака обслуживания Евразийского экономического союза`
- REQ28 fallback literal is exact and case-sensitive:
  `решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении всех заявленных товаров и (или) услуг.`

## UNMAPPED_REQUIREMENTS
REQ3, REQ18, REQ19, REQ21, REQ22, and REQ24 remain UNMAPPED because the current rule engine cannot safely express the required semantics without changing shared infrastructure.

No speculative workaround was added.

## SEMANTIC_ROLE_SAFETY
Cancellation and new-registration behavior is bound by status value within each `UnifiedRegisterRecordsDetails` record. Tests cover both record orders and verify that data from one role does not satisfy requirements for the other role.

No `[0]`, `[1]`, first/second, or ordinal record assumptions are used.

## OWNER_QNAME_SAFETY
REQ23 uses the confirmed nested owner:
`ipcdo:RegistrationCancellationDetails/ipcdo:ComplaintInvalidateProtectionTrademarkDetails`.

The required cancellation code paths are:
- `.../ipsdo:CancellationRegistrationTrademarkCode`
- `.../ipsdo:SolutionCancellationRegistrationTrademarkCode`

Signature rules preserve the distinct ownership of:
- `ipcdo:OfficerDetails/ccdo:FullNameDetails`
- direct `ipcdo:SignatureDetails/ccdo:FullNameDetails`

## NORMATIVE_BASIS
CONFIRMED.

Primary normative source references are the existing P.SP.02 MSG052 Table 70 references in `ОП_22.pdf`, together with inherited Table 49 provenance for REQ6-19 and the existing R.IP.SP.02.007 structure definition/source references.

The implementation does not invent missing normative behavior and does not reclassify the supplied authoritative mapping.

## MSG052_TESTS
Executed:

`PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests/test_msg052_*.py -p no:cacheprovider`

Result:

`22 passed in 1.29s`

Also executed:

`python3 -m json.tool P.SP.02_OP_22/message_rules/P.SP.02.MSG.052.yaml >/dev/null`

Result: PASS.

## OPTIONAL_FULL_REGRESSION
NOT RUN.

The task is strict-scope MSG052 implementation, and the targeted suite covers the changed rule file plus safe-mapping, repeatable XML, end-to-end roundtrip, negative proofs, and message isolation. No shared infrastructure was changed by this task.

## CONCURRENT_CHANGES
The repository contains many pre-existing/concurrent modified and untracked files outside MSG052 scope. They were left untouched.

This task did not modify MSG051, shared XML infrastructure, or unrelated process/message files.

## GIT_DIFF_CHECK
Executed scoped `git diff --check` for the five allowed paths.

Result: PASS.

## REMAINING_ISSUES
None.
