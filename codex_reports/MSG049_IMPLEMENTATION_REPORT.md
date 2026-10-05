# MSG049 Implementation Report

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.049.yaml` — implemented approved Table 67 structured mappings and mapping audit.
- `P.SP.02_OP_22/tests/test_msg049_safe_mapping.py` — verifies inventory, classifications, exact executable set, QName/owner shapes, partial/unmapped requirements, signatures, and the normative REQ20 gap.
- `P.SP.02_OP_22/tests/test_msg049_repeatable_xml.py` — verifies per-parent alignment, owner isolation, document-kind branches, inherited rules, and signature isolation.
- `P.SP.02_OP_22/tests/test_msg049_end_to_end.py` — verifies production build -> serialize -> parse -> extract -> validate and message isolation.
- `codex_reports/MSG049_IMPLEMENTATION_REPORT.md` — this report.

## IMPLEMENTATION
MSG049 implements exactly the approved executable requirement codes:
`{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,21,22,23,24,25}`.

REQ1, REQ21 and REQ22 remain partial executable mappings. REQ18 and REQ19 have no executable mappings. REQ20 was not created or classified.

REQ3 requires `StartDateTime` under the governed record's `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails`. REQ4 forbids `EndDateTime` in the same owner. REQ5 requires `StatusCode == "03"`, requires `EventDate`, and forbids `StatusCode/@codeListId`.

REQ6–17 reuse the established Table 49 executable mappings with dual Table67 + Table49 provenance. REQ22 preserves the exact approved fallback literal. REQ23–25 preserve same-parent signature/officer semantics.

## MAPPING_COUNTS
- captured = 11
- expanded = 24
- REQ_LIST = 1..19,21..25
- FULL = 19
- SAFE_PARTIAL = 3
- EXTERNAL = 0
- AMBIGUOUS = 0
- ENGINE_UNSUPPORTED = 2
- SOURCE_CONFLICT = 0
- executable requirement codes = 22
- structured-rule object count = 25

## PARTIAL_REMAINDERS
- REQ1: external national-resource lookup/status/equality semantics remain outside local XML validation.
- REQ21: classifier membership/code validity remains external.
- REQ22: classifier absence predicate remains external.

## UNMAPPED_REQUIREMENTS
`{18,19}`.

Both remain `ENGINE_UNSUPPORTED` and have no executable structured mappings.

## NORMATIVE_GAP_REQ20
REQ20 = NORMATIVELY_ABSENT.

The normative inventory is exactly `{1..19,21,22,23,24,25}`. No REQ20 rule, audit entry, classification, executable mapping, or unmapped entry was created.

## OWNER_QNAME_SAFETY
- TrademarkId is direct under the governed `ipcdo:UnifiedRegisterRecordsDetails`.
- REQ3/4 use `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails`.
- REQ5 uses the distinct `ipcdo:IPEntityStatusDetails` owner.
- document-kind fields are direct same-record fields.
- StatusCode `codeListId` is validated as an attribute.
- signature branches use direct same-parent `OfficerDetails` / `FullNameDetails`.
- REQ25 targets officers owned by the same SignatureDetails path.

## NORMATIVE_BASIS
CONFIRMED — approved MSG049 writer handoff; Table 67 direct requirements and inherited Table 49 requirements already captured in the repository audit. No new normative audit was performed.

## MSG049_TESTS
Command:
`PYTHONDONTWRITEBYTECODE=1 pytest -q P.SP.02_OP_22/tests/test_msg049_*.py -p no:cacheprovider`

Result:
`21 passed in 1.54s`.

Production E2E covers valid MSG049, record cardinality, TrademarkId, StartDateTime required, EndDateTime forbidden, StatusCode 03, EventDate, forbidden codeListId, exact REQ22 fallback, inherited Table49 behavior, signatures, and message isolation.

## OPTIONAL_FULL_REGRESSION
NOT RUN — explicitly not required while MSG048 is being modified concurrently.

## CONCURRENT_CHANGES
The repository already contained many modified/untracked files, including shared infrastructure and parallel work. Those changes were treated as foreign and were not reverted or edited for MSG049.

## GIT_DIFF_CHECK
CLEAN — `git diff --check` produced no output.

## REMAINING_ISSUES
None.
