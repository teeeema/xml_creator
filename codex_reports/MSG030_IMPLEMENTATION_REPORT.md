STATUS = COMPLETE

# ROOT_CAUSE

P.SP.02.MSG.030 already had the declarative Table 46 capture, but it did not have the verified SAFE executable subset required for runtime validation. The task therefore required an independent normative reread of Table 46 and inherited Table 44 REQ6–29, exact StructureDefinition ownership/QName checks, and conservative mapping of only semantics expressible by the current evaluator without strengthening, cross-parent leakage, or external-data simulation.

No shared engine defect was required. Existing evaluator capabilities (selection_cardinality with where, for_each with where, conditional presence/fixed value, comparison IN, and all/any/not conditions) were sufficient for the selected MSG030 rules.

# CHANGED_FILES

Current batch implementation/test scope:

- P.SP.02_OP_22/message_rules/P.SP.02.MSG.030.yaml
  - added 36 structured rule objects;
  - added complete mapping_audit for expanded REQ1–40;
  - retained unsupported/ambiguous/external portions as partial or unmapped instead of approximating them.
- P.SP.02_OP_22/tests/test_msg030_safe_mapping.py
  - new MSG030-only mapping/provenance/isolation tests.
- P.SP.02_OP_22/tests/test_msg030_repeatable_xml.py
  - new MSG030-only production-XML extraction/repeatability/ownership/QName tests.
- P.SP.02_OP_22/tests/test_msg030_end_to_end.py
  - new MSG030-only build → serialize → parse → extract → validate tests and independent invalid proofs.
- codex_reports/MSG030_IMPLEMENTATION_REPORT.md
  - this service report; intentionally not added to git.

No existing MSG001–029 test file and no shared production Python file was changed in this batch.

# MSG030

Confirmed context:

- message: P.SP.02.MSG.030
- name: доводы и замечания по результатам экспертизы
- structure: R.IP.SP.02.002 v1.0.0
- normative table: Table 46, physical PDF pp. 728–731
- transaction: P.SP.02.TRN.025
- procedure: P.SP.02.PRC.004
- operations: P.SP.02.OPR.011 → P.SP.02.OPR.012
- sender: P.SP.02.ACT.001
- receiver: P.SP.02.ACT.002
- response: P.SP.02.MSG.002
- Table46 REQ6–29 inherits Table44 REQ6–29.
- executable structured rule objects: 36
- unique mapped requirement codes: 33

# FULL_MAPPED

30 requirements:

1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40

# PARTIAL_MAPPED

3 requirements:

- REQ2 — SAFE_PARTIAL. Local branch is executable: if direct ipsdo:IPDocKindCode is present, direct ipsdo:IPDocKindName is forbidden. Authoritative classifier membership is external.
- REQ3 — SAFE_PARTIAL. If direct code is absent, direct ipsdo:IPDocKindName must equal the exact single Table46 fallback name. Authoritative classifier-absence semantics remain external.
- REQ4 — SAFE_PARTIAL. Direct ipsdo:TrademarkApplicationId is required. National-patent-office resource lookup, StatusCode=02, external EndDateTime absence, and external ID correspondence remain external.

# UNMAPPED

7 requirements:

- REQ13 — AMBIGUOUS / stored as UNMAPPED: standalone AP statement has no safe repeated-owner/instance semantics; a global AP rule would contradict valid PA/RE records.
- REQ16 — ENGINE_UNSUPPORTED / stored as UNMAPPED: AP-scoped correlation to repeated IPSubjectName representation attributes.
- REQ17 — ENGINE_UNSUPPORTED / stored as UNMAPPED: per-AP filtered cardinality over repeated names plus representation/language attributes.
- REQ18 — ENGINE_UNSUPPORTED / stored as UNMAPPED: AP-scoped languageCode=RU second-instance semantics.
- REQ19 — ENGINE_UNSUPPORTED / stored as UNMAPPED: AP-scoped languageCode!=RU second-instance LA semantics.
- REQ20 — ENGINE_UNSUPPORTED / stored as UNMAPPED: AP-role correlation with nested repeated SubjectAddressDetails.
- REQ26 — ENGINE_UNSUPPORTED / stored as UNMAPPED: exact per-TrademarkDetails disjunctive Code OR Name value comparison is not expressible without strengthening the norm.

No source conflict was identified for MSG030 (mapping_audit.source_conflicts = []).

# REQ1_APPLICATION_CARDINALITY

FULL.

Table46 requires exactly one direct ipcdo:TrademarkApplicationDetails.

Implemented as selection_cardinality on ipcdo:TrademarkApplicationDetails with min_occurs=1 and max_occurs=1. Production E2E invalid proofs cover both zero and two instances.

# REQ2_3_DOCUMENT_KIND

REQ2 = PARTIAL.

Exact safe fragment:

- scope: direct ipcdo:TrademarkApplicationDetails;
- if direct ipsdo:IPDocKindCode is present;
- direct ipsdo:IPDocKindName is forbidden.

Classifier-presence membership remains external.

REQ3 = PARTIAL.

If direct ipsdo:IPDocKindCode is absent, direct ipsdo:IPDocKindName must equal:

Доводы и замечания заявителя в связи с уведомлением о результатах экспертизы заявки на товарный знак, знак обслуживания Евразийского экономического союза в отношении всех или части заявленных товаров

Classifier-absence determination remains external.

Production XML collision coverage proves that a wrong-namespace IPDocKindCode does not switch the REQ2/REQ3 branch and that a nested document IPDocKindName cannot satisfy the direct application field.

# REQ4_EXTERNAL_ID

PARTIAL.

Direct application ipsdo:TrademarkApplicationId presence is executable and mapped.

Not simulated:

- national patent office information-resource lookup;
- external StatusCode = 02;
- external EndDateTime absence;
- external TrademarkApplicationId equality with the message value.

Wrong-namespace direct application ID fails the mapped local fragment.

# REQ5_REGISTRATION_CODE

FULL.

Exact direct application owner/QName:

ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkRegistrationCode

Required and restricted to 02 or 03.

Production XML invalid proof uses value 01. Wrong-namespace direct registration code also fails.

# REQ6_12_CORE

FULL, independently confirmed against inherited Table44.

- REQ6: direct ApplicationReceiptDate required.
- REQ7: selected exact csdo:UnifiedCountryCode/@codeListId = "ВОИС ST.3".
- REQ8: each selected ccdo:SubjectAddressDetails requires the mapped address children.
- REQ9: each selected ccdo:CommunicationDetails requires ChannelCode + ChannelId and forbids ChannelName.
- REQ10: ChannelCode IN {TE, EM, FX}.
- REQ11: each direct ipcdo:PatentAuthorityDetails requires UnifiedCountryCode.
- REQ12: each direct PatentAuthorityDetails requires AuthorityName + SubjectAddressDetails, with nested AddressKindCode fixed to 2.

# REQ13_AMBIGUOUS

UNMAPPED / AMBIGUOUS.

Original Table44 states an AP value but does not provide safe owner/instance semantics for applying that statement across repeated IPPartyDetails. A global IPPartyKindCode=AP rule would reject normative PA/RE instances required by other requirements.

No executable approximation was added.

# REQ14_15_AP

FULL.

AP selection is semantic and discriminator-based: IPPartyKindCode = AP. No positional/index assumption is used.

- REQ14: AP cardinality implemented with filtered selection_cardinality.
- REQ15: required children evaluated only inside selected AP records.

Production XML tests cover:

- AP, PA, RE
- PA, AP, RE
- RE, PA, AP
- RE, AP, PA

Targeted bad AP fails AP semantics without leaking to PA/RE.

# REQ16_20_ENGINE_GAPS

UNMAPPED / ENGINE_UNSUPPORTED.

No approximations were introduced.

Remaining exact semantics require combinations of:

- nested repeatable descendants under selected AP;
- filtered child cardinality;
- representation/language correlation;
- ordinal first/second-instance semantics;
- nested repeated address correlation.

The current evaluator does not express those requirements exactly while preserving parent alignment.

# REQ21_PA

FULL.

Each actually existing semantic PA (IPPartyKindCode = PA) is validated in its own parent context, including PatentAttorneyId as required by the inherited Table44 rule.

PA absence does not create synthetic existence. Targeted bad PA and role-order tests pass/fail only PA semantics.

# REQ22_RE

FULL.

Each actually existing semantic RE (IPPartyKindCode = RE) is validated in its own parent context.

RE absence does not create synthetic existence. Targeted bad RE and role-order tests show no cross-parent leakage.

# REQ23_24_CORRESPONDENCE

FULL.

Rules are scoped only to existing correspondence-address branch.

- REQ23: AddressKindCode = 3.
- REQ24: UnifiedCountryCode IN {AM, BY, KZ, KG, RU}.

Correspondence absence is valid; no synthetic branch existence was introduced.

# REQ25_TRADEMARK

FULL.

ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkDetails is required.

Mapped required children are the independently rechecked inherited Table44 fields:

- ipcdo:TMDescriptionDetails
- ipsdo:TrademarkKindCode
- ipsdo:TrademarkKindName
- ipsdo:CollectiveMarkIndicator

# REQ26_NORMATIVE_RECHECK

UNMAPPED / ENGINE_UNSUPPORTED.

Critical independent reread of original Table44 physical p.720 confirmed the operator is:

TrademarkKindCode OR TrademarkKindName

One of the two must match the normative kinds.

Conclusion:

- normative semantics are OR;
- they must not be strengthened to Code AND Name;
- no non-normative pair-consistency requirement may be added;
- current evaluator cannot assert the exact per-TrademarkDetails disjunctive value comparison as one normative result without strengthening.

Therefore REQ26 remains intentionally unmapped.

# REQ27_NORMATIVE_RECHECK

FULL.

Independent reread of original Table44 physical p.721 confirmed:

- condition is TrademarkKindCode OR TrademarkKindName;
- the matching values are the listed normative kinds corresponding to codes 140/150/160/170/180;
- consequence requires both TrademarkPicture and TrademarkColourName;
- trigger and consequences belong to the same ipcdo:TrademarkDetails parent.

The evaluator can express this exactly using same-parent for_each plus an any condition.

Production XML tests prove Code and Name independently trigger the requirement, missing picture/colour fails, and wrong-namespace colour cannot satisfy the exact QName.

# REQ28_COLLECTIVE

FULL.

Within each selected TrademarkDetails:

CollectiveMarkIndicator IN {"1", "0"}

Invalid value 2 is independently proven to fail.

# REQ29_GOODS

FULL.

GoodsBaseDetails is required.

Every existing Goods parent requires:

- GoodsClassCode
- GoodsClassName
- GoodsName

Production XML tests cover:

- good + good PASS;
- good + bad FAIL;
- bad + good FAIL;
- 3-parent sparse missing child at each position;
- wrong-namespace required Goods children do not satisfy exact QName.

Parent alignment is preserved.

# REQ30_DECISION_GOODS

FULL.

Independent Table46 reread confirmed unconditional semantics: at least one ipcdo:GoodsBaseDetails must have direct ipsdo:TrademarkDecisionIndicator = "0".

Implemented exactly as filtered selection_cardinality:

- collection: direct GoodsBaseDetails under the application;
- where TrademarkDecisionIndicator == "0";
- min_occurs = 1;
- no maximum.

Production XML tests cover decision sequences 0, 1+0, 0+1, 1+1, and wrong-namespace decision indicator. Only exact decision-0 Goods count.

# REQ31_DECISION_FIELDS

FULL.

For every Goods parent where direct TrademarkDecisionIndicator = "0":

- direct TrademarkApplicationId required;
- direct TrademarkRegRefusalReasonText required.

Implemented with for_each + where, preserving same-Goods ownership.

Production XML tests cover:

- good decision0 + good decision0 PASS;
- good + bad FAIL;
- bad + good FAIL;
- decision1 fields cannot satisfy missing fields in a different decision0 parent;
- wrong-namespace application ID/refusal reason do not satisfy exact fields.

# REQ32_DOCUMENTS

FULL.

Table46 reread confirmed child requirements for each existing ipcdo:AccompanyingDocumentsDetails; it does not require synthetic document-parent existence.

Every existing document requires exactly the mapped six children:

- ipsdo:IPDocKindName
- csdo:DocId
- csdo:DocCreationDate
- csdo:DescriptionText
- csdo:PageQuantity
- csdo:DocBinaryText

No MSG029 document semantics were copied mechanically.

Production XML tests cover each required child independently, good/bad and bad/good parent order, two complete documents, and wrong-namespace DocBinaryText.

Documents absent → no REQ32 child-only failure.

# REQ33_CONSENT

FULL.

Exact direct application field:

ipsdo:ConsentToDataProcessingIndicator

Required and restricted to 1 or 0.

Production tests show nested same-local-name data cannot satisfy the direct owner and wrong-namespace direct data cannot satisfy the QName.

# REQ34_36_SIGNATURE

FULL.

Exact signature owner:

ipcdo:TrademarkApplicationDetails/ipcdo:SignatureDetails

Direct alternative:

SignatureDetails/ccdo:FullNameDetails

Officer alternative:

SignatureDetails/ipcdo:OfficerDetails

REQ34:

- at least one SignatureDetails;
- within each signature, Officer present ⇒ direct FullNameDetails forbidden.

REQ35:

- within each signature, direct FullNameDetails present ⇒ OfficerDetails forbidden.

REQ36:

for each exact OfficerDetails:

- FullNameDetails/LastName required;
- FullNameDetails/FirstName required;
- PositionName required;
- Officer CommunicationDetails forbidden.

Production XML tests cover direct/officer variants, two signatures in both orders, illegal both-branches-in-one-parent, missing each Officer child, forbidden Officer communication, wrong-namespace Officer, and wrong-namespace SignatureDetails.

No cross-parent escape is possible.

# REQ37_ARGUMENT

FULL.

Direct application ipcdo:ArgumentDetails is required with minimum cardinality one.

The valid E2E fixture also supplies StructureDefinition-required Argument children DescriptionText and EventDate.

Wrong-namespace ArgumentDetails does not satisfy the rule.

# REQ38_REFUSAL

FULL.

Exact root-level ipcdo:RefusalDetails is forbidden.

Production E2E independently proves root refusal fails. A nested same-QName RefusalDetails under the application does not trigger the root-level rule, proving owner isolation.

# REQ39_START_DATE

FULL.

For each existing exact ccdo:ResourceItemStatusDetails:

ccdo:ValidityPeriodDetails/csdo:StartDateTime is required.

No external-equality remainder was found in the rechecked Table46 row.

# REQ40_END_DATE

FULL.

For each existing exact ccdo:ResourceItemStatusDetails:

ccdo:ValidityPeriodDetails/csdo:EndDateTime is forbidden.

Independent E2E invalid proof adds EndDateTime and observes the MSG030 REQ40 rule failure.

# PROVENANCE

All executable inherited REQ6–29 rules carry dual provenance.

CURRENT_PROVENANCE:

- Table46
- physical p.729
- inherited item/range 6-29
- source id 22OP-RULE-P.SP.02.MSG.030-T46-6-29

ORIGINAL_PROVENANCE:

- the concrete Table44 requirement item;
- its concrete Table44 page/source reference.

REQ26, although unmapped, also records both the Table46 inherited reference and original Table44 REQ26 p.720 reference in mapping_audit.

Direct Table46 requirements retain their own Table46 source refs.

# PARTY_ROLE_ORDER

Production XML tests executed semantic order permutations:

- AP, PA, RE
- PA, AP, RE
- RE, PA, AP
- RE, AP, PA

All required AP/PA/RE mapped semantics pass independent of order.

Targeted invalid cases:

- bad AP;
- bad PA;
- bad RE.

Each fails its corresponding role rule without cross-parent leakage.

# QNAME_COLLISION

StructureDefinition paths were audited before mapping.

Production extraction tests additionally prove exact QName/owner behavior for representative and critical MSG030 fields, including:

- direct application TrademarkApplicationId;
- direct TrademarkRegistrationCode;
- direct IPDocKindCode branch;
- direct/nested IPDocKindName;
- direct/nested ConsentToDataProcessingIndicator;
- TrademarkColourName;
- all three required Goods fields;
- TrademarkDecisionIndicator;
- decision0 Goods TrademarkApplicationId;
- decision0 Goods TrademarkRegRefusalReasonText;
- document DocBinaryText;
- SignatureDetails;
- OfficerDetails;
- ArgumentDetails;
- root-vs-nested RefusalDetails.

Wrong namespace or wrong owner does not silently satisfy the exact mapped target.

# REPEATABLE_XML

Critical repeated structures exercised through real XML serialization/parsing/extraction:

- IPPartyDetails
- TrademarkDetails
- GoodsBaseDetails
- AccompanyingDocumentsDetails
- SignatureDetails

Coverage includes good+good, good+bad, bad+good, multi-parent order, sparse child positions, discriminator filtering, and same-parent conditional ownership.

No manually flattened-only proof is used for the critical ownership assertions.

# OPTIONAL_BRANCHES

Verified:

- PA absent → no PA child-only failure.
- RE absent → no RE child-only failure.
- correspondence absent → no correspondence child-only failure.
- accompanying documents absent → no REQ32 child-only failure.
- Officer absent → REQ36 Officer-child assertions inactive.

No synthetic existence rule was added for optional branches.

# MESSAGE_ISOLATION

Same extracted R.IP.SP.02.002 values are validated under:

- P.SP.02.MSG.027
- P.SP.02.MSG.028
- P.SP.02.MSG.029
- P.SP.02.MSG.030

Isolation proof requires:

- non-empty evaluations for all four;
- every rule ID has the requested message prefix;
- pairwise rule-ID sets are disjoint.

No isolation check relies on MSG030 having no rules.

No stale existing MSG027/028/029 isolation assertion failed in the final regression.

# END_TO_END

Valid MSG030 pipeline executed:

build
→ serialize
→ parse
→ extract
→ validate

Final valid E2E assertions:

- exact R.IP.SP.02.002 root QName;
- extraction issues = 0;
- validation valid and complete;
- 36 structured rule evaluations;
- every evaluation PASS;
- unique evaluated mapped requirements equal the 33 mapped REQ codes;
- TRN.025 context matches MSG030, MSG002 response, OPR.011→OPR.012, ACT.001→ACT.002.

Every executable requirement has an independent production-XML invalid proof. Composite requirements can have multiple rule objects, and tests assert normative behavior rather than only IDs.

# MSG030_TESTS

Final command:

pytest -q P.SP.02_OP_22/tests/test_msg030_*.py

Result:

119 passed in 2.79s

0 failed.

# MSG029_REGRESSION

Final command:

pytest -q P.SP.02_OP_22/tests/test_msg029_*.py

Result:

84 passed in 1.98s

0 failed.

# MSG028_REGRESSION

Final command:

pytest -q P.SP.02_OP_22/tests/test_msg028_*.py

Result:

113 passed in 2.96s

0 failed.

# MSG027_REGRESSION

Final command:

pytest -q P.SP.02_OP_22/tests/test_msg027_*.py

Result:

96 passed in 2.30s

0 failed.

# MSG020_024_REGRESSION

Final command:

pytest -q P.SP.02_OP_22/tests/test_msg02[0-4]_*.py

Result:

148 passed in 3.42s

0 failed.

# PREVIOUS_REGRESSION

Final command covered previously implemented message suites:

- MSG001
- MSG003
- MSG004
- MSG005
- MSG006–010
- MSG011–014
- MSG016–019

Result:

595 passed in 21.04s

0 failed.

# SHARED_REGRESSION

Final command:

pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_embedded_one_of.py eaeu_xml/tests/test_repeatable_xml_alignment.py

Result:

45 passed, 5 subtests passed in 0.17s

0 failed.

# PSP02_TESTS

Final command:

pytest -q P.SP.02_OP_22/tests

Result:

1168 passed in 33.85s

0 failed.

Previous control point was 1049 passed; increase is the 119 new MSG030 tests.

# EAEU_XML_TESTS

Final command:

pytest -q eaeu_xml/tests

Result:

265 passed, 43 skipped, 1042 subtests passed in 2.27s

0 failed.

# ROOT_TESTS

Final command:

pytest -q

Result:

1557 passed, 43 skipped, 1152 subtests passed in 42.22s

0 failed.

Previous root control point:

1438 passed, 43 skipped, 1152 subtests passed

Net increase:

+119 passed

This exactly matches the final MSG030-only test count.

# PREEXISTING_CHANGES

The repository was already dirty before the MSG030 batch. Observed preexisting modified files included:

- AGENTS.md
- MSG mappings for previously completed batches:
  MSG001, MSG003, MSG004, MSG005, MSG006, MSG007, MSG009, MSG010, MSG011, MSG013, MSG014, MSG016, MSG017, MSG018, MSG019, MSG020, MSG021, MSG022, MSG024, MSG027, MSG028, MSG029
- shared files already dirty from prior completed work:
  - eaeu_xml/src/eaeu_xml/process_packages/body.py
  - eaeu_xml/src/eaeu_xml/process_packages/engine.py
  - eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py
  - eaeu_xml/src/eaeu_xml/process_packages/validator.py
- eaeu_xml/tests/test_structured_rules.py
- numerous untracked test files for previous MSG001–029 batches;
- prior untracked eaeu_xml/tests/test_embedded_one_of.py;
- prior untracked eaeu_xml/tests/test_repeatable_xml_alignment.py;
- codex_reports/ was already an untracked service-report directory.

Those changes were preserved. No reset/clean/checkout/stash/add/commit was performed.

# CURRENT_BATCH_CHANGES

Only allowed MSG030 implementation/test/report files were created or changed by this batch:

- P.SP.02_OP_22/message_rules/P.SP.02.MSG.030.yaml
- P.SP.02_OP_22/tests/test_msg030_safe_mapping.py
- P.SP.02_OP_22/tests/test_msg030_repeatable_xml.py
- P.SP.02_OP_22/tests/test_msg030_end_to_end.py
- codex_reports/MSG030_IMPLEMENTATION_REPORT.md

Relative to HEAD, MSG030 YAML diff stat at final check:

2810 insertions(+), 1 deletion(-)

The three MSG030 test files and report are untracked, as expected.

# GIT_STATUS

Final git status remains dirty because it contains the preexisting completed batches plus this MSG030 batch.

Current MSG030 entries are:

- M P.SP.02_OP_22/message_rules/P.SP.02.MSG.030.yaml
- ?? P.SP.02_OP_22/tests/test_msg030_end_to_end.py
- ?? P.SP.02_OP_22/tests/test_msg030_repeatable_xml.py
- ?? P.SP.02_OP_22/tests/test_msg030_safe_mapping.py
- ?? codex_reports/ (service directory also contains prior reports)

All other dirty entries observed in final status were present before this MSG030 batch and were not modified by this batch.

No git staging or commit operation was performed.

# GIT_DIFF_CHECK

Final command:

git diff --check

Result:

PASS.

No output; exit code 0.

# PROTECTED_FILES

Baseline:

/tmp/msg030_protected_before.json

Protected set:

- shared body.py
- shared rules_engine.py
- shared engine.py
- shared validator.py
- all existing MSG001–029 mappings

Total protected entries:

28

Final SHA-256 + exact mtime_ns comparison:

entries=28
mismatches=0

Therefore all protected shared production Python files and all protected MSG001–029 mappings are unchanged from the pre-MSG030 protected baseline.

MSG030 is intentionally not part of that baseline because it is the current target.

# DEFECTS_FOUND

No remaining MSG030 production defect or unexpected regression was found inside the allowed scope.

During construction of the valid E2E fixture, the first build correctly exposed three StructureDefinition-level missing fields in the test fixture:

- SignatureDetails/csdo:DocCreationDate
- ArgumentDetails/csdo:DescriptionText
- ArgumentDetails/csdo:EventDate

The fixture was corrected. No production code or normative mapping outside MSG030 was changed for this.

No stale existing isolation test failed after the final implementation.

Intentional placeholders X.X.X / Y.Y.Y / Z.Z.Z were not investigated, changed, reported as defects, or treated as blockers.

# REMAINING_REQUIREMENTS

The SAFE executable subset intentionally does not claim full execution of all normative semantics.

PARTIAL remainders:

- REQ2 — authoritative classifier-presence predicate and classifier designation.
- REQ3 — authoritative classifier-absence predicate.
- REQ4 — national patent office external resource lookup/status/end-date/ID correspondence.

UNMAPPED remainders:

- REQ13 — ambiguous repeated owner/instance semantics.
- REQ16–20 — current evaluator cannot exactly express the required nested/filtered/ordinal AP correlations.
- REQ26 — current evaluator cannot exactly express normative per-TrademarkDetails Code OR Name value matching without strengthening OR to AND or adding non-normative pair consistency.

These are explicitly recorded in mapping_audit. They are not silently approximated.

# VERDICT

VERDICT = READY

Reasons:

1. Every implemented executable rule has normative source provenance.
2. Exact owner/QName paths used by mapped rules were audited against R.IP.SP.02.002.
3. Inherited executable REQ6–29 carry current Table46 plus original Table44 provenance.
4. REQ26 remains OR and was not strengthened to AND.
5. REQ27 was independently reread and implemented with same-parent OR trigger semantics.
6. REQ30 is exact filtered cardinality supported by the current evaluator.
7. REQ31 preserves same-Goods ownership.
8. REQ32 does not create synthetic document existence.
9. REQ34–36 preserve same-signature semantics.
10. Critical repeatable ownership is proven through production XML extraction.
11. AP/PA/RE are selected by discriminator, not position.
12. External/classifier semantics are not simulated.
13. 28/28 protected files are unchanged by SHA-256 and mtime_ns.
14. MSG030 E2E is green with 36 PASS evaluations and zero extraction issues.
15. Final package and root regressions have zero failures.
16. git diff --check passes.

STATUS = COMPLETE
