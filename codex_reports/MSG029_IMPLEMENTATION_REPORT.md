# MSG029_IMPLEMENTATION_REPORT

STATUS = COMPLETE

ROOT_CAUSE
P.SP.02.MSG.029 already contained the Table 45 business-rule capture, but had no executable structured_rules for the locally enforceable subset. The work therefore required translating only source-confirmed, evaluator-safe requirements into structured rules while leaving external-data, ambiguous, engine-unsupported, and source-conflicting semantics explicitly unmapped.

CHANGED_FILES
- P.SP.02_OP_22/message_rules/P.SP.02.MSG.029.yaml
  - Added 32 structured rule objects covering 29 requirement codes.
  - Added mapping_audit with SAFE_PARTIAL, AMBIGUOUS, ENGINE_UNSUPPORTED, and SOURCE_CONFLICT provenance.
- P.SP.02_OP_22/tests/test_msg029_safe_mapping.py
  - New MSG029 mapping/provenance/QName/message-isolation tests.
- P.SP.02_OP_22/tests/test_msg029_repeatable_xml.py
  - New production-XML repeatable-parent and same-parent tests.
- P.SP.02_OP_22/tests/test_msg029_end_to_end.py
  - New MSG029 build/serialize/parse/extract/validate and message-isolation coverage.
- codex_reports/MSG029_IMPLEMENTATION_REPORT.md
  - Service report required by the user; intentionally not added to git.

MSG029
- Structure: R.IP.SP.02.002 v1.0.0.
- Context: P.SP.02.TRN.024, initiating P.SP.02.MSG.029, response P.SP.02.MSG.002, OPR.008 -> OPR.009, ACT.002 -> ACT.001.
- Source: ОП_22.pdf, Table 45 physical pp.724-728.
- Inherited requirements: Table45 REQ6-29 explicitly correspond to Table44 REQ6-29.
- structured_rules: 32 rule objects.
- Executable/partial requirement codes covered: 29.
- Composite requirements 25, 29 and 37 are represented by two rule objects each under the same normative requirement id.
- YAML status remains CONFIRMED.

FULL_MAPPED
25 requirement codes:
1, 3, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 33, 34, 36, 37, 38, 39.

PARTIAL_MAPPED
4 SAFE_PARTIAL requirement codes:
- 2: local TrademarkApplicationId presence is executable; external filing-office resource lookup/status/end-date/id equality remains external.
- 4: locally safe branch forbids IPDocKindName when IPDocKindCode is present; authoritative classifier membership/code lookup remains external.
- 5: locally safe branch requires IPDocKindName when IPDocKindCode is absent; classifier absence and conditional membership in the three Table45 document names remain unsupported by the current evaluator.
- 35: StartDateTime presence is executable; equality to the external national-resource inclusion timestamp remains external.

UNMAPPED
10 requirement codes:
- 13: AMBIGUOUS.
- 16, 17, 18, 19, 20: ENGINE_UNSUPPORTED.
- 26: ENGINE_UNSUPPORTED.
- 30, 31: ENGINE_UNSUPPORTED.
- 32: SOURCE_CONFLICT.

REQ1_APPLICATION_CARDINALITY
FULL_MAPPED.
Exactly one ipcdo:TrademarkApplicationDetails is required by selection_cardinality min=1 max=1.
Source: Table45 REQ1, physical p.724.

REQ2_EXTERNAL_ID
SAFE_PARTIAL.
Executable part: ipsdo:TrademarkApplicationId is required inside each TrademarkApplicationDetails.
Unmapped external remainder:
- filing-office information-resource lookup;
- external StatusCode in {01,02};
- external EndDateTime absent;
- external TrademarkApplicationId equality to message value.
Source: Table45 REQ2, physical p.724.

REQ3_REGISTRATION_CODE
FULL_MAPPED.
Direct ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkRegistrationCode is required.
Source: Table45 REQ3, physical p.724.

REQ4_5_DOCUMENT_KIND
SAFE_PARTIAL.
Table45 p.725 names three possible MSG029 document kinds.
REQ4 safe local branch:
- when direct IPDocKindCode is present, direct IPDocKindName is forbidden.
Remaining external semantics are authoritative classifier presence and the classifier code designation.
REQ5 safe local branch:
- when direct IPDocKindCode is absent, direct IPDocKindName is required.
The rule does not invent a single fallback literal and does not strengthen the source. Classifier absence and conditional membership in the three normative names remain unmapped.

REQ6_12_CORE
FULL_MAPPED from Table45 inheritance plus original Table44 rows.
- REQ6: ApplicationReceiptDate required.
- REQ7: every UnifiedCountryCode under the application uses @codeListId = "ВОИС ST.3".
- REQ8: every SubjectAddressDetails under the application requires AddressKindCode, UnifiedCountryCode, CityName, StreetName, BuildingNumberId.
- REQ9: every CommunicationDetails requires CommunicationChannelCode and CommunicationChannelId and forbids CommunicationChannelName.
- REQ10: CommunicationChannelCode is one of TE, EM, FX.
- REQ11: PatentAuthorityDetails requires UnifiedCountryCode.
- REQ12: PatentAuthorityDetails requires AuthorityName and SubjectAddressDetails with AddressKindCode = 2.

REQ13_AMBIGUOUS
UNMAPPED / AMBIGUOUS.
Original Table44 REQ13 states IPPartyKindCode=AP without an unambiguous repeated owner. Enforcing AP globally across repeated IPPartyDetails would conflict with the explicitly permitted PA and RE roles in REQ21 and REQ22. No speculative global rule was added.

REQ14_15_AP
FULL_MAPPED.
Role-filtered selectors target only IPPartyDetails where IPPartyKindCode=AP.
- REQ14 enforces exactly one AP party.
- REQ15 enforces the AP-required local fields.
Repeatable tests verify party ordering does not affect the result and values do not leak between parents.

REQ16_20_ENGINE_GAPS
UNMAPPED / ENGINE_UNSUPPORTED.
- REQ16: AP-scoped correlation to repeated IPSubjectName representation attributes.
- REQ17: per-AP filtered cardinality over repeated IPSubjectName with representation/language attributes.
- REQ18: AP-scoped languageCode=RU second-instance semantics.
- REQ19: AP-scoped languageCode!=RU second-instance LA semantics.
- REQ20: AP role correlated with nested SubjectAddressDetails semantics beyond the current safe selector model.
No approximations were added.

REQ21_PA
FULL_MAPPED.
Role-filtered IPPartyDetails selector uses IPPartyKindCode=PA and preserves same-parent semantics.

REQ22_RE
FULL_MAPPED.
Role-filtered IPPartyDetails selector uses IPPartyKindCode=RE and preserves same-parent semantics.

REQ23_24_CORRESPONDENCE
FULL_MAPPED.
Correspondence address/contact requirements are mapped to the exact application-owned correspondence branch. No values are borrowed from another owner.

REQ25_TRADEMARK
FULL_MAPPED.
Trademark requirements are applied to exact ipcdo:TrademarkDetails owners. Composite normative semantics are represented by two structured-rule objects for the same requirement id where needed.

REQ26_NORMATIVE_RECHECK
UNMAPPED / ENGINE_UNSUPPORTED.
Original Table44 was reread directly from the prepared PDF material. Table44 REQ26 on physical p.720 requires the value of either:
- ipsdo:TrademarkKindCode
OR
- ipsdo:TrademarkKindName
to correspond to one of the listed trademark kinds 110-180.
This is a genuine OR requirement. The current evaluator has no direct disjunctive comparison assertion scoped to each repeated TrademarkDetails parent. Requiring both code and name, or adding pair-consistency, would strengthen the normative text. Therefore REQ26 remains ENGINE_UNSUPPORTED.

REQ27_NORMATIVE_RECHECK
FULL_MAPPED.
Original Table44 REQ27 on physical p.721 was reread directly.
Condition within the same ipcdo:TrademarkDetails:
TrademarkKindCode OR TrademarkKindName corresponds to one of:
140, 150, 160, 170, 180 / their listed names.
Consequence within that same TrademarkDetails:
- ipsdo:TrademarkPicture required;
- ipsdo:TrademarkColourName required.
The mapping uses the exact TrademarkDetails owner and same-parent condition. Wrong-namespace TrademarkColourName does not satisfy the rule.

REQ28_COLLECTIVE
FULL_MAPPED.
ipsdo:CollectiveMarkIndicator must be one of {1,0}.
Source: inherited Table44 REQ28.

REQ29_GOODS
FULL_MAPPED.
GoodsBaseDetails is required, and each actual GoodsBaseDetails instance requires:
- ipsdo:GoodsClassCode;
- ipsdo:GoodsClassName;
- ipsdo:GoodsName.
Production-XML repeatable tests preserve per-goods-instance ownership.

REQ30_ENGINE_GAP
UNMAPPED / ENGINE_UNSUPPORTED.
Table45 REQ30, physical p.726:
if TrademarkRegistrationCode=01, the count of GoodsBaseDetails with TrademarkDecisionIndicator=0 must be zero.
This is conditional filtered cardinality. The current evaluator cannot express it exactly without approximation, so no rule was added.

REQ31_ENGINE_GAP
UNMAPPED / ENGINE_UNSUPPORTED.
Table45 REQ31, physical p.726:
if TrademarkRegistrationCode in {02,03}, at least one GoodsBaseDetails with TrademarkDecisionIndicator=0 must exist.
This is conditional filtered cardinality. The current evaluator cannot express it exactly without approximation, so no rule was added.

REQ32_SOURCE_CONFLICT
UNMAPPED / SOURCE_CONFLICT.
Table45 REQ32, physical p.726, places ipsdo:InconsistencyText inside the selected GoodsBaseDetails row when TrademarkDecisionIndicator=0.
Exact R.IP.SP.02.002 StructureDefinition audit shows:
- GoodsBaseDetails/ipsdo:TrademarkApplicationId exists;
- GoodsBaseDetails/ipsdo:TrademarkRegRefusalReasonText exists;
- GoodsBaseDetails/ipsdo:InconsistencyText does NOT exist;
- ipcdo:TrademarkApplicationDetails/ipsdo:InconsistencyText exists directly under the application.
No application-level or similarly named field was substituted for the missing GoodsBaseDetails child.
Recorded structure provenance: source_id 22OP-R.IP.SP.02.002-2.13, ОП_22.pdf p.876, table 10, item 2.13.

REQ33_DOCUMENTS
FULL_MAPPED.
Exact StructureDefinition owner:
ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails.
Per each document:
- IPDocKindCode OR IPDocKindName is enforced exactly by two same-context conditional_presence assertions:
  - if Code is absent -> Name required;
  - if Name is absent -> Code required.
This accepts code-only, name-only, and both; rejects neither. It does not turn OR into AND and does not leak values across document parents.
Independent necessary children are required in the same document context:
DocName, DocId, DocCreationDate, DocValidityDate, DescriptionText, PageQuantity.
Production-XML tests include mixed code/name documents and missing-child cases.

REQ34_REFUSAL
FULL_MAPPED.
ipcdo:RefusalDetails is forbidden by selection_cardinality max=0.
StructureDefinition confirms RefusalDetails is root-level for R.IP.SP.02.002.
Source: Table45 REQ34, physical p.727.

REQ35_START_DATE
SAFE_PARTIAL.
ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime is required.
Equality to the external national-patent-office information-resource inclusion timestamp remains outside the evaluator and is recorded as unmapped remainder.

REQ36_END_DATE
FULL_MAPPED.
ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime is forbidden.
Source: Table45 REQ36, physical p.727.

REQ37_39_SIGNATURE
FULL_MAPPED with same-parent semantics.
Exact StructureDefinition paths:
- ipcdo:TrademarkApplicationDetails/ipcdo:SignatureDetails
- .../ipcdo:OfficerDetails
- .../ipcdo:SignatureDetails/ccdo:FullNameDetails
- .../ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName
- .../ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName
- .../ipcdo:OfficerDetails/csdo:PositionName
- .../ipcdo:OfficerDetails/ccdo:CommunicationDetails
REQ37:
- SignatureDetails required;
- when OfficerDetails exists in a signature, the direct SignatureDetails/ccdo:FullNameDetails is forbidden in that same signature.
REQ38:
- when direct SignatureDetails/ccdo:FullNameDetails exists, OfficerDetails is forbidden in that same signature.
REQ39:
- exact selector qname ipcdo:OfficerDetails under the SignatureDetails path;
- LastName, FirstName, PositionName required;
- CommunicationDetails forbidden.
Repeatable XML tests verify sparse/multiple signatures cannot satisfy each other.

PROVENANCE
CONFIRMED.
- Table45 pp.724-728 is the current MSG029 source.
- For executable inherited REQ6-29, each rule carries both:
  1. Table45 provenance item 6-29, p.725; and
  2. the original Table44 requirement-specific source_ref/page/item.
A final scripted audit found no executable inherited REQ6-29 rule lacking both references.
REQ32 additionally records the conflicting StructureDefinition source reference.

PARTY_ROLE_ORDER
Verified.
Role filtering is by IPPartyKindCode value, not position.
Production-XML repeatable tests verify missing data in one AP/PA/RE parent is not satisfied by another parent and party ordering is irrelevant.

QNAME_COLLISION
Verified.
MSG029-only production-XML tests cover:
- wrong-namespace ipsdo:TrademarkColourName;
- wrong-namespace ipcdo:OfficerDetails;
- wrong-owner document-kind fields that must not satisfy the direct application document-kind rule.
StructureDefinition audit also confirmed exact owners for GoodsBaseDetails, AccompanyingDocumentsDetails, SignatureDetails and OfficerDetails.

REPEATABLE_XML
Command:
pytest -q P.SP.02_OP_22/tests/test_msg029_repeatable_xml.py
Result:
33 passed in 0.87s.
Tests build namespaced production-shaped XML, parse it through the production extraction path, and validate repeated party, goods, document, trademark and signature parent alignment.

OPTIONAL_BRANCHES
Verified in MSG029-only tests.
Optional documents/signature alternatives are exercised with both presence and absence cases. OR branches for REQ33 are tested per document. Signature direct-name/officer alternatives are tested within the same signature parent.

MESSAGE_ISOLATION
Verified.
New MSG029 tests validate that rule evaluations are scoped to the requested message code and every executed rule id has the requested message prefix.
The existing MSG028 regression contains a stale expectation that MSG029 has no rule evaluations; that expectation is now obsolete because MSG029 intentionally has structured_rules.

END_TO_END
Command:
pytest -q P.SP.02_OP_22/tests/test_msg029_end_to_end.py
Result:
32 passed in 1.15s.
Coverage includes the normal production pipeline for R.IP.SP.02.002 and failure mutations for mapped requirements, plus requested-message rule isolation.

MSG029_TESTS
Commands/results:
- pytest -q P.SP.02_OP_22/tests/test_msg029_safe_mapping.py
  - 19 passed in 0.12s.
- pytest -q P.SP.02_OP_22/tests/test_msg029_repeatable_xml.py
  - 33 passed in 0.87s.
- pytest -q P.SP.02_OP_22/tests/test_msg029_end_to_end.py
  - 32 passed in 1.15s.
- pytest -q P.SP.02_OP_22/tests/test_msg029_*.py
  - 84 passed in 1.90s.

MSG028_REGRESSION
Command:
pytest -q P.SP.02_OP_22/tests/test_msg028_*.py
Result:
1 failed, 112 passed in 2.93s.
Only failure:
P.SP.02_OP_22/tests/test_msg028_end_to_end.py::test_same_r002_values_execute_only_rules_for_requested_message_code
Stale assertion:
assert not result029.rule_evaluations
That assertion was valid only before MSG029 had structured_rules. It was intentionally not changed because the hard scope forbids editing existing MSG028 tests.

MSG027_REGRESSION
Command:
pytest -q P.SP.02_OP_22/tests/test_msg027_*.py
Result:
96 passed in 2.24s.

MSG020_024_REGRESSION
Command:
pytest -q P.SP.02_OP_22/tests/test_msg02[0-4]_*.py
Result:
148 passed in 3.31s.

PREVIOUS_REGRESSION
Command:
pytest -q P.SP.02_OP_22/tests/test_msg00*.py P.SP.02_OP_22/tests/test_msg01*.py
Result:
595 passed in 20.29s.

SHARED_REGRESSION
Command:
pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_embedded_one_of.py eaeu_xml/tests/test_repeatable_xml_alignment.py
Result:
45 passed, 5 subtests passed in 0.17s.

PSP02_TESTS
Command:
pytest -q P.SP.02_OP_22/tests
Result:
1 failed, 1048 passed in 30.54s.
The sole failure is the same out-of-scope stale MSG028 assertion described above.

PROCESS_TESTS
Command:
pytest -q eaeu_xml/tests/test_process_packages.py
Result:
34 passed in 0.21s.

Additional eaeu_xml regression:
Command:
pytest -q eaeu_xml/tests
Result:
265 passed, 43 skipped, 1042 subtests passed in 2.29s.

ROOT_TESTS
Command:
pytest -q
Result:
1 failed, 1437 passed, 43 skipped, 1152 subtests passed in 39.12s.
The sole failure is the same stale MSG028 assertion. No additional failure appeared.
Historical user-provided pre-batch baseline:
1354 passed, 43 skipped, 1152 subtests passed, 0 failed.

PREEXISTING_CHANGES
The repository was already dirty before the MSG029 batch.
Pre-existing tracked modifications include AGENTS.md, multiple P.SP.02 message-rule YAMLs for earlier messages, shared process-package Python files, and eaeu_xml/tests/test_structured_rules.py.
Pre-existing untracked files include the earlier MSG001-MSG028 test batches and shared regression tests.
These files were not reset or rewritten during this MSG029 batch.

CURRENT_BATCH_CHANGES
Implementation/test scope:
- P.SP.02_OP_22/message_rules/P.SP.02.MSG.029.yaml
- P.SP.02_OP_22/tests/test_msg029_safe_mapping.py
- P.SP.02_OP_22/tests/test_msg029_repeatable_xml.py
- P.SP.02_OP_22/tests/test_msg029_end_to_end.py
Allowed service report:
- codex_reports/MSG029_IMPLEMENTATION_REPORT.md
No shared production Python, MSG001-028, MSG030, or existing other-message tests were modified by this batch.

GIT_STATUS
Branch: pyside6-gui.
Working tree remains dirty because of pre-existing changes plus this MSG029 batch.
MSG029.yaml is tracked-modified.
The three MSG029 test files are untracked new files.
codex_reports/ is untracked as required.
No git add, commit, reset, clean, or history rewrite was performed.

GIT_DIFF_CHECK
Command:
git diff --check
Result:
PASS, no output.

PROTECTED_FILES
Original protected-baseline capture was confirmed from Codex session history:
- capture timestamp: 2026-09-25T06:48:02.883Z
- captured count: 28 files
- protected set: 4 shared production files plus existing P.SP.02.MSG.001-028 and MSG030 rule YAMLs included by the original capture command; MSG029 was excluded as intended.

The temporary file /tmp/msg029_protected_before.json is no longer present, so a literal before-vs-after SHA-256 comparison cannot be honestly reproduced and is NOT claimed as completed.

Current SHA-256 values for the same 28 protected paths were captured to:
/tmp/msg029_protected_after.json

Independent scope evidence:
- protected_count = 28
- mtime_after_capture_count = 0
Every one of the 28 protected files has a filesystem mtime at or before the confirmed baseline-capture timestamp. This supports that none of the protected files was written after baseline capture during the MSG029 batch.
The task-specific changed files are outside that protected set.
No protected-file modification was made in this batch.

DEFECTS_FOUND
1. SOURCE_CONFLICT in normative inputs for REQ32:
   Table45 requires GoodsBaseDetails/ipsdo:InconsistencyText, while R.IP.SP.02.002 defines ipsdo:InconsistencyText directly under TrademarkApplicationDetails.
2. Existing stale MSG028 regression expectation:
   P.SP.02_OP_22/tests/test_msg028_end_to_end.py::test_same_r002_values_execute_only_rules_for_requested_message_code
   contains assert not result029.rule_evaluations, which is obsolete after MSG029 gains structured_rules.
3. Evidence limitation only:
   the temporary protected baseline JSON was lost, so exact hash equality cannot be asserted. Current hashes plus mtime/scope evidence were recorded instead.
No defect was found in the implemented MSG029 SAFE executable subset after the final targeted and regression runs.

REMAINING_REQUIREMENTS
SAFE_PARTIAL remainders:
- REQ2 external resource lookup/status/end-date/id-equality semantics.
- REQ4 authoritative classifier-presence/code semantics.
- REQ5 authoritative classifier-absence and conditional three-name membership.
- REQ35 external StartDateTime equality.

Unmapped:
- REQ13 AMBIGUOUS.
- REQ16-20 ENGINE_UNSUPPORTED.
- REQ26 ENGINE_UNSUPPORTED because exact per-TrademarkDetails Code OR Name comparison cannot be expressed without strengthening.
- REQ30-31 ENGINE_UNSUPPORTED conditional filtered cardinality.
- REQ32 SOURCE_CONFLICT.

These are intentionally not approximated.

NORMATIVE_BASIS
CONFIRMED for the implemented subset:
- ОП_22.pdf Table45, physical pp.724-728.
- Original Table44 rows 6-29, physical pp.715-721, where inherited by Table45.
- R.IP.SP.02.002 v1.0.0 exact StructureDefinition paths.
UNKNOWN/BLOCKED_BY_SOURCE is not silently converted to executable behavior. Unsupported evaluator semantics remain explicitly classified.

VERDICT
READY for the defined SAFE executable subset of P.SP.02.MSG.029.
The MSG029 implementation and all MSG029-only tests are green.
The only suite-wide failure is the explicitly anticipated, out-of-scope stale MSG028 assertion.
The remaining unmapped/partial requirements are documented rather than approximated.

STATUS = COMPLETE
VERDICT = READY

