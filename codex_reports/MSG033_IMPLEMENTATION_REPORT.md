# P.SP.02.MSG.033 IMPLEMENTATION REPORT

## STATUS

STATUS = COMPLETE

## VERDICT

VERDICT = NOT_READY

Implementation of the normative-safe executable subset for P.SP.02.MSG.033 is complete within the authorized scope. MSG033-only tests are green and all 31 protected files are unchanged. The repository-wide acceptance gate is not fully green because one older MSG032 test contains a stale assertion that MSG033 has no structured rules, and an unrelated P.MM.01 performance-threshold test also fails outside this batch scope.

## ROOT_CAUSE

P.SP.02.MSG.033 had Table 51 captured only as declarative `business_rules`; it had no executable `structured_rules` and no expanded per-requirement `mapping_audit`. As a result, the validator had no message-specific executable enforcement for the safe local subset of Table 51.

The implementation required an independent reread of Table 51 pp. 743-746, inherited Table 44 REQ6-29 pp. 714-723, the R.IP.SP.02.002 StructureDefinition, and current evaluator semantics. Requirements that cannot be represented exactly or require external normative data were deliberately left partial or unmapped rather than approximated.

## CHANGED_FILES

Current batch implementation/test scope:

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.033.yaml`
- `P.SP.02_OP_22/tests/test_msg033_safe_mapping.py`
- `P.SP.02_OP_22/tests/test_msg033_repeatable_xml.py`
- `P.SP.02_OP_22/tests/test_msg033_end_to_end.py`

Authorized service output:

- `codex_reports/MSG033_IMPLEMENTATION_REPORT.md`

No shared production Python, MSG001-032 mapping, older message test, StructureDefinition, classifier, process metadata, or MSG034+ mapping was changed in this batch.

## MSG033

Confirmed message context:

- message: `P.SP.02.MSG.033`
- name: `сведения о результатах внутригосударственного обжалования решения по экспертизе`
- structure: `R.IP.SP.02.002`, version `1.0.0`
- root QName: `{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails`
- normative table: Table 51, physical PDF pp. 743-746
- expanded requirement inventory: 37 requirements
- transaction: `P.SP.02.TRN.028`
- procedure: `P.SP.02.PRC.007`
- initiating operation: `P.SP.02.OPR.025`
- responding operation: `P.SP.02.OPR.026`
- initiating participant: `P.SP.02.ACT.002` (national patent office)
- responding participant: `P.SP.02.ACT.001` (filing office)
- response message: `P.SP.02.MSG.002`

The final mapping contains 33 structured rule entries covering 30 requirement codes.

## NORMATIVE_BASIS

CONFIRMED for the source text used in this batch:

- ОП_22.pdf Table 51, pp. 743-746, for MSG033-specific requirements.
- ОП_22.pdf Table 44, pp. 714-723, for inherited REQ6-29.
- ОП_22.pdf procedure/operation material around pp. 115-120 for PRC.007 and OPR.025/026.
- ОП_22.pdf transaction description pp. 649-651 for TRN.028 and MSG033 -> MSG002.
- R.IP.SP.02.002 StructureDefinition table source beginning at p. 840 for exact owner/QName paths.

Where the normative requirement depends on an external classifier/resource or requires evaluator semantics not currently available, the mapping records that limitation explicitly instead of treating it as confirmed executable behavior.

## NORMATIVE_INVENTORY

Primary classification is complete and mutually exclusive for all 37 expanded requirements:

- FULLY_MAPPABLE: 1, 2, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37
- SAFE_PARTIAL: 3, 4, 5
- AMBIGUOUS: 13
- ENGINE_UNSUPPORTED: 16, 17, 18, 19, 20, 26
- EXTERNAL: none as a primary classification
- SOURCE_CONFLICT: none

The executable requirement-code set is therefore 1-12 excluding none in that range, 14-15, 21-25, 27-37, plus safe local fragments for 3-5; REQ13, REQ16-20, and REQ26 have no executable approximation.

## FULL_MAPPED

Fully mapped requirements:

- REQ1: exactly one `ipcdo:TrademarkApplicationDetails`.
- REQ2: same application context `csdo:StatusCode IN {10,20}` and `StatusCode/@codeListId` absent.
- REQ6-12: inherited Table 44 exact safe rules for application receipt, country classifier attribute, addresses, communications, communication channel, and direct patent-authority details.
- REQ14-15: inherited AP role cardinality and AP-local required children using filtered same-parent context.
- REQ21-24: inherited PA/RE and correspondence rules with exact owners.
- REQ25: inherited TrademarkDetails presence and required local children.
- REQ27: inherited same-TrademarkDetails Code OR Name trigger requiring picture and colour.
- REQ28-29: inherited collective-mark and GoodsBaseDetails rules.
- REQ30: `ipsdo:TrademarkRegistrationCode` required under each application.
- REQ31-33: exact same-SignatureDetails / OfficerDetails semantics.
- REQ34: exact application-owned `ipcdo:ApplicantComplainResponseDetails` required.
- REQ35: root `ipcdo:RefusalDetails` forbidden.
- REQ36-37: exact ResourceItemStatusDetails / ValidityPeriodDetails start required and end forbidden.

## PARTIAL_MAPPED

REQ3-5 are SAFE_PARTIAL only:

- REQ3 executable fragment: if application `ipsdo:IPDocKindCode` is present, application `ipsdo:IPDocKindName` is forbidden. Unmapped: authoritative classifier-presence predicate, classifier lookup, and equality to the authoritative classifier code.
- REQ4 executable fragment: if application `ipsdo:IPDocKindCode` is absent, `ipsdo:IPDocKindName` must equal the exact fallback document-kind text from Table 51. Unmapped: authoritative classifier-absence predicate.
- REQ5 executable fragment: application `ipsdo:TrademarkApplicationId` is required. Unmapped: external filing-office record existence, external StatusCode=02, external EndDateTime absence, and external ID correspondence.

## UNMAPPED

- REQ13 = AMBIGUOUS. Original Table 44 states AP for `IPPartyKindCode` without an exact repeated-instance scope; globally forcing every party to AP would conflict with REQ21/22 PA/RE semantics.
- REQ16-20 = ENGINE_UNSUPPORTED. They require exact AP-filtered nested repeated correlation/cardinality semantics that the current evaluator cannot express without risking cross-parent leakage or strengthening.
- REQ26 = ENGINE_UNSUPPORTED. The normative requirement is a same-parent `TrademarkKindCode OR TrademarkKindName` disjunction. No AND approximation was introduced.
- External remainders of REQ3-5 remain intentionally non-executable.

## REQ1_5

REQ1 is exact selection cardinality 1..1 on `ipcdo:TrademarkApplicationDetails`.

REQ2 is fully executable in each application context using the exact nested owner path `ipcdo:IPEntityStatusDetails/csdo:StatusCode`; accepted values are exactly `10` and `20`, and the exact `csdo:StatusCode/@codeListId` attribute is forbidden.

REQ3/4 preserve the classifier-dependent split only as safe necessary local implications. The exact fallback text is:

`Заключение национального патентного ведомства по результатам экспертизы заявленного обозначения о возможности (невозможности) регистрации товарного знака, знака обслуживания Евразийского экономического союза`

REQ5 maps only the independently mandatory message-local TrademarkApplicationId; no external resource state was fabricated.

## REQ6_29

Table 51 explicitly inherits Table 44 REQ6-29. Each mapping-audit row for 6-29 carries dual provenance:

1. Table 51 inheritance source `22OP-RULE-P.SP.02.MSG.033-T51-6-29`, p. 745.
2. The exact original Table 44 requirement source row/page.

Executable inherited subset: REQ6-12, 14-15, 21-25, 27-29.

Unmapped inherited subset: REQ13, REQ16-20, REQ26.

## REQ26_NORMATIVE_RECHECK

Original Table 44 p. 720 was reread independently. REQ26 requires `TrademarkKindCode OR TrademarkKindName` to correspond to an allowed trademark kind. The OR is normative. Mapping both fields as independently required/validated would strengthen OR into AND and is therefore prohibited.

Classification: ENGINE_UNSUPPORTED / UNMAPPED.

No structured rule was created for REQ26.

## REQ27_NORMATIVE_RECHECK

Original Table 44 p. 721 was reread independently. REQ27 identifies graphical/colour trademark kinds by `TrademarkKindCode OR TrademarkKindName`; if either trigger matches in a given TrademarkDetails parent, `TrademarkPicture` and `TrademarkColourName` must be present in that same parent.

The current evaluator can express this exactly with `for_each` on `ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkDetails` and an `any` condition containing the Code and Name alternatives. Repeatable XML tests prove the required children cannot be cross-satisfied by another parent context.

Classification: FULLY_MAPPABLE.

## REQ30_PLUS

- REQ30: required `ipsdo:TrademarkRegistrationCode` under the application.
- REQ31: at least one SignatureDetails; within each SignatureDetails, OfficerDetails present => direct sibling FullNameDetails forbidden.
- REQ32: within each SignatureDetails, direct FullNameDetails present => OfficerDetails forbidden.
- REQ33: for each exact OfficerDetails below SignatureDetails, require nested FullNameDetails/LastName, FullNameDetails/FirstName, PositionName; forbid OfficerDetails/CommunicationDetails.
- REQ34: required application-owned ApplicantComplainResponseDetails.
- REQ35: root RefusalDetails forbidden.
- REQ36: ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime required.
- REQ37: ResourceItemStatusDetails/ValidityPeriodDetails/EndDateTime forbidden.

All exact target owners/QNames were verified against R.IP.SP.02.002 before mapping.

## PROVENANCE

MSG033-specific rules use Table 51 source_refs with exact requirement item/page.

Inherited REQ6-29 retain both the Table 51 inheritance reference and the original Table 44 requirement reference. The mapping audit records one primary classification for every expanded requirement and explicit `safe_fragment`, `unmapped_remainder`, `external_dependency`, or `engine_gap` where applicable.

No source_ref was invented for an unsupported semantic claim.

## QNAME_COLLISION

New tests verify exact owner/namespace behavior, including:

- wrong-namespace `StatusCode` does not satisfy REQ2;
- wrong-namespace `ApplicantComplainResponseDetails` does not satisfy REQ34;
- direct SignatureDetails/FullNameDetails is distinguished from OfficerDetails/FullNameDetails;
- a nested ComplaintDetails/PatentAuthorityDetails does not satisfy or trigger rules for direct application PatentAuthorityDetails.

## REPEATABLE_XML

Tests use real XML elements serialized and reparsed through production extraction rather than manually flattened values only.

Covered repeatable/alignment cases include:

- repeatable party SubjectAddressDetails with a missing child in either parent;
- repeatable CommunicationDetails with a missing child in either parent;
- AP filtering with AP before/after another role;
- REQ27 same-parent trademark trigger/required children;
- repeatable GoodsBaseDetails;
- multiple SignatureDetails parents using different allowed signature branches.

## OPTIONAL_BRANCHES

Signature matrix verified:

- OfficerDetails-only branch: PASS.
- direct SignatureDetails/FullNameDetails-only branch: PASS.
- two SignatureDetails parents, one using OfficerDetails and one direct FullNameDetails: PASS.
- both branches in the same SignatureDetails: FAIL as required by REQ31/32.
- OfficerDetails missing PositionName: FAIL REQ33.
- OfficerDetails containing CommunicationDetails: FAIL REQ33.

Optional classifier branches in REQ3/4 are only mapped to necessary local implications; classifier existence itself remains external.

## MESSAGE_ISOLATION

MSG033 tests prove that rule IDs for MSG031 R.IP.SP.02.002, MSG032, and MSG033 are all non-empty and pairwise disjoint. Actual MSG033 validation executes exactly the defined MSG033 rule-id set and all executed IDs use the `P.SP.02.MSG.033.` prefix.

The older MSG032 isolation test also passes all its real isolation assertions: MSG032 executions contain only MSG032 IDs, and MSG031/032/033 rule-id sets are disjoint. Its final stale assertion `assert not rules033` is the only reason that old test now fails.

## END_TO_END

The MSG033 E2E test performs:

build -> serialize -> parse -> production extract -> validate.

The valid production XML fixture validates successfully with 33 rule evaluations, all PASS. It confirms the exact root QName, status 10 branch, exact fallback document name, TrademarkRegistrationCode, ApplicantComplainResponseDetails, SignatureDetails, absence of root RefusalDetails, resource validity start, and TRN.028 routing metadata.

Every FULLY_MAPPABLE requirement has an independent negative production-XML proof; every SAFE_PARTIAL requirement has a negative proof for its executable local fragment.

## MSG033_TESTS

Command:

`pytest -q P.SP.02_OP_22/tests/test_msg033_*.py`

Result:

`73 passed in 2.00s`

No MSG033-only failures remain.

## REGRESSIONS

Required neighboring suites actually executed:

- `pytest -q P.SP.02_OP_22/tests/test_msg032_*.py` -> `1 failed, 64 passed in 1.73s`
  - exact fail: `P.SP.02_OP_22/tests/test_msg032_end_to_end.py::test_requested_msg032_validation_contains_no_msg031_or_msg033_rule_ids`
  - stale assertion: `assert not rules033`
  - no old file was modified because current strict scope forbids MSG032 test changes.
- `pytest -q P.SP.02_OP_22/tests/test_msg031_*.py` -> `84 passed in 1.74s`
- `pytest -q P.SP.02_OP_22/tests/test_msg030_*.py` -> `119 passed in 3.13s`
- `pytest -q P.SP.02_OP_22/tests/test_msg029_*.py` -> `84 passed in 2.20s`
- `pytest -q P.SP.02_OP_22/tests/test_msg028_*.py` -> `113 passed in 3.50s`
- `pytest -q P.SP.02_OP_22/tests/test_msg027_*.py` -> `96 passed in 2.62s`
- `pytest -q P.SP.02_OP_22/tests/test_msg02[0-4]_*.py` -> `148 passed in 4.12s`

## PSP02_TESTS

Command:

`pytest -q P.SP.02_OP_22/tests`

Result:

`1 failed, 1389 passed in 95.97s`

Only failure is the same stale MSG032 assertion described above.

## EAEU_XML_TESTS

Command:

`pytest -q eaeu_xml/tests`

Result:

`265 passed, 43 skipped, 1042 subtests passed in 13.06s`

Status: PASS.

## ROOT_TESTS

Command:

`pytest -q`

Result:

`2 failed, 1777 passed, 43 skipped, 1152 subtests passed in 115.85s`

Failures:

1. `P.SP.02_OP_22/tests/test_msg032_end_to_end.py::test_requested_msg032_validation_contains_no_msg031_or_msg033_rule_ids`
   - stale `assert not rules033` after MSG033 legitimately gained structured rules.
2. `P.MM.01_OP_26/tests/test_application_facade_pmm01.py::Pmm01ApplicationFacadeTests::test_large_message_form_filters_preserve_counts_hierarchy_and_performance`
   - measured 100 filter operations at `1.0105820840108208s`, threshold `< 1.0s`.
   - exact isolated rerun also failed at `1.0357432079908904s`.
   - unrelated to MSG033 and outside authorized scope; no change was made.

The pre-MSG033 root baseline was `1706 passed, 43 skipped, 1152 subtests passed, 0 failed`. The new MSG033 tests account for 73 additional passing tests. The two current root failures are the stale older MSG032 assertion and the unrelated P.MM.01 timing gate above.

## PREEXISTING_CHANGES

Repository was dirty before this batch. The baseline status was captured in `/tmp/msg033_status_before.txt` and diff names in `/tmp/msg033_diff_names_before.txt` before MSG033 edits.

All modified MSG001-032 mappings, shared production Python, existing shared tests, earlier untracked message tests, `AGENTS.md`, and pre-existing `codex_reports/` status entries shown in that baseline are PREEXISTING and were preserved.

No destructive git operation was used.

## CURRENT_BATCH_CHANGES

Status delta relative to `/tmp/msg033_status_before.txt` contains exactly:

- modified `P.SP.02_OP_22/message_rules/P.SP.02.MSG.033.yaml`
- new `P.SP.02_OP_22/tests/test_msg033_safe_mapping.py`
- new `P.SP.02_OP_22/tests/test_msg033_repeatable_xml.py`
- new `P.SP.02_OP_22/tests/test_msg033_end_to_end.py`

The report file is an authorized service artifact under the already-present untracked `codex_reports/` directory.

No other status line was introduced by this batch.

## GIT_STATUS

Final `git status --short` remains dirty because of pre-existing completed batches plus the four current MSG033 implementation/test paths and the report directory. The exact status was captured at `/tmp/msg033_status_after.txt`.

The before/after status diff shows only the MSG033 mapping and three new MSG033 tests as new implementation/test status lines.

## GIT_DIFF_CHECK

Command:

`git diff --check`

Result: PASS, exit code 0, no output.

## PROTECTED_FILES

Baseline: `/tmp/msg033_protected_before.json`

Protected files: 31.

Final SHA-256 + `mtime_ns` comparison:

- protected count: 31
- mismatches: 0

Therefore all protected MSG001-032 mappings and shared production files in the baseline remained byte-for-byte and timestamp unchanged during this batch.

## DEFECTS_FOUND

1. STALE OUT-OF-SCOPE TEST:
   `P.SP.02_OP_22/tests/test_msg032_end_to_end.py::test_requested_msg032_validation_contains_no_msg031_or_msg033_rule_ids`
   ends with `assert not rules033`. That was valid before MSG033 implementation and is now obsolete. The preceding isolation assertions still prove disjoint message rule sets. Strict scope forbids editing this test in the current batch.

2. UNRELATED OUT-OF-SCOPE PERFORMANCE FAILURE:
   `P.MM.01_OP_26/tests/test_application_facade_pmm01.py::Pmm01ApplicationFacadeTests::test_large_message_form_filters_preserve_counts_hierarchy_and_performance`
   exceeds a strict `<1.0s` timing threshold in both root and isolated execution. No MSG033 code path or allowed file owns this behavior.

No MSG033 source conflict was found for Table 51-specific target paths.

## REMAINING_REQUIREMENTS

Normative/evaluator limitations intentionally remaining:

- REQ3: authoritative classifier-present predicate/code lookup.
- REQ4: authoritative classifier-absence predicate.
- REQ5: filing-office resource existence/status/end-date/ID correspondence.
- REQ13: ambiguous repeated-party scope in original Table 44.
- REQ16-20: exact nested repeated filtered correlation/cardinality evaluator support.
- REQ26: exact same-parent Code OR Name membership requirement without OR-to-AND strengthening.

Regression maintenance remaining outside this batch scope:

- update the stale MSG032 isolation test to expect non-empty, disjoint MSG033 rules rather than `assert not rules033`;
- investigate the unrelated P.MM.01 performance threshold separately.

## VERDICT

VERDICT = NOT_READY

MSG033 implementation itself is complete and its dedicated suite is green, provenance/protection checks pass, and no protected file changed. Repository-wide readiness cannot be declared because the mandated regression gates are not fully green and the failures are outside the current authorized edit scope.
