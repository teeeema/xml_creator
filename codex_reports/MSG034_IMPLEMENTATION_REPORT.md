# MSG034_IMPLEMENTATION_REPORT

## STATUS

STATUS = COMPLETE

## VERDICT

VERDICT = READY

## ROOT_CAUSE

P.SP.02.MSG.034 had the normative Table 52 rows captured as declarative `business_rules`, but had no executable `structured_rules` and no complete 37-requirement `mapping_audit`. The implementation task was therefore to translate only the normatively safe subset into the existing evaluator without changing shared Python or strengthening unsupported semantics.

## CHANGED_FILES

Current batch implementation/test scope:

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.034.yaml` — added 33 unique executable rule IDs and complete mapping audit for 37 expanded requirements.
- `P.SP.02_OP_22/tests/test_msg034_safe_mapping.py` — mapping/provenance/StructureDefinition/isolation contract tests.
- `P.SP.02_OP_22/tests/test_msg034_repeatable_xml.py` — production extraction, repeatable-parent alignment, same-parent and QName-owner tests.
- `P.SP.02_OP_22/tests/test_msg034_end_to_end.py` — build -> serialize -> parse -> production extract -> validate tests and negative proofs.
- `codex_reports/MSG034_IMPLEMENTATION_REPORT.md` — this service report; intentionally not added to git.

No shared production Python, MSG001–033 mapping/test, StructureDefinition, classifier, process metadata, P.MM.01, or MSG035+ file was changed by this batch.

## MSG034

Message: `P.SP.02.MSG.034` — «доказательство приобретения обозначением различительной способности».

Final mapping state:

- business/declarative rows retained: 14;
- expanded normative requirements: 37;
- executable structured rules: 33;
- unique structured rule IDs: 33;
- executable requirement codes: 30 (27 FULL + 3 SAFE_PARTIAL);
- intentionally unmapped requirement codes: 7 (REQ13, REQ16–20, REQ26).

## NORMATIVE_BASIS

CONFIRMED from `/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf` using the independently reread normative text:

- message list physical p.635;
- procedure P.SP.02.PRC.010 physical pp.143–147;
- operations P.SP.02.OPR.037 and P.SP.02.OPR.038 physical pp.149–150;
- transaction P.SP.02.TRN.029 physical pp.651–653;
- Table 52 physical pp.746–748;
- original inherited Table 44 physical pp.714–723;
- repository StructureDefinition `R.IP.SP.02.002` v1.0.0 cross-checked against the confirmed message structure.

No normative behavior was inferred from a neighboring message without rereading the original source.

## TRANSACTION_CONTEXT

CONFIRMED context:

- transaction: `P.SP.02.TRN.029`;
- procedure: `P.SP.02.PRC.010`;
- initiating operation: `P.SP.02.OPR.037`;
- responding operation: `P.SP.02.OPR.038`;
- initiating participant: `P.SP.02.ACT.001`;
- responding participant: `P.SP.02.ACT.002`;
- initiating message: `P.SP.02.MSG.034`;
- response message: `P.SP.02.MSG.002`.

The end-to-end test also verifies these exact repository transaction fields and the generated application action suffix.

## STRUCTURE

CONFIRMED structure: `R.IP.SP.02.002`, version `1.0.0`.

Root QName: `{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails`.

Critical exact owners verified in StructureDefinition:

- `ipcdo:TrademarkApplicationDetails` id 2, min 1, max `*`;
- direct `.../ipcdo:AccompanyingDocumentsDetails` id 2.16, min 0, max `*`;
- nested proof document `.../ipcdo:NamingAbilityProofDetails/ipcdo:ProofDocTextDetails/ipcdo:AccompanyingDocumentsDetails` id 2.26.3.1, min 0, max 1;
- `.../ipcdo:NamingAbilityProofDetails` id 2.26, min 0, max `*`;
- `.../ipcdo:SignatureDetails` id 2.18, min 0, max `*`;
- exact signature `OfficerDetails` id 2.18.2, distinct from the separate OfficerDetails owner under TrademarkClaimDetails;
- root-level `ipcdo:RefusalDetails` id 3, min 0, max 1;
- root-level `ccdo:ResourceItemStatusDetails` id 4;
- `ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime` id 4.1.1;
- `ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime` id 4.1.2.

## RULE_TABLE

Table 52 contains 14 captured rows for MSG034: `1, 2, 3, 4, 5, 6-29, 30, 31, 32, 33, 34, 35, 36, 37`.

Row `6-29` explicitly inherits the corresponding requirement numbers from original Table 44. It was expanded into 24 independent audit entries, giving exactly 37 requirements overall.

## NORMATIVE_INVENTORY

| REQ | Primary classification | Mapping status | Provenance | Source refs |
|---:|---|---|---|---|
| 1 | FULLY_MAPPABLE | EXECUTABLE | DIRECT | T52 p.746 item 1 |
| 2 | SAFE_PARTIAL | PARTIAL_EXECUTABLE | DIRECT | T52 p.746 item 2 |
| 3 | SAFE_PARTIAL | PARTIAL_EXECUTABLE | DIRECT | T52 p.747 item 3 |
| 4 | SAFE_PARTIAL | PARTIAL_EXECUTABLE | DIRECT | T52 p.747 item 4 |
| 5 | FULLY_MAPPABLE | EXECUTABLE | DIRECT | T52 p.747 item 5 |
| 6 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.715 item 6 |
| 7 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.715 item 7 |
| 8 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.715 item 8 |
| 9 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.716 item 9 |
| 10 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.716 item 10 |
| 11 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.716 item 11 |
| 12 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.716 item 12 |
| 13 | AMBIGUOUS | UNMAPPED | INHERITED | T52 p.747 item 6-29; T44 p.716 item 13 |
| 14 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.716 item 14 |
| 15 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.717 item 15 |
| 16 | ENGINE_UNSUPPORTED | UNMAPPED | INHERITED | T52 p.747 item 6-29; T44 p.717 item 16 |
| 17 | ENGINE_UNSUPPORTED | UNMAPPED | INHERITED | T52 p.747 item 6-29; T44 p.717 item 17 |
| 18 | ENGINE_UNSUPPORTED | UNMAPPED | INHERITED | T52 p.747 item 6-29; T44 p.718 item 18 |
| 19 | ENGINE_UNSUPPORTED | UNMAPPED | INHERITED | T52 p.747 item 6-29; T44 p.718 item 19 |
| 20 | ENGINE_UNSUPPORTED | UNMAPPED | INHERITED | T52 p.747 item 6-29; T44 p.718 item 20 |
| 21 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.719 item 21 |
| 22 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.719 item 22 |
| 23 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.719 item 23 |
| 24 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.720 item 24 |
| 25 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.720 item 25 |
| 26 | ENGINE_UNSUPPORTED | UNMAPPED | INHERITED | T52 p.747 item 6-29; T44 p.720 item 26 |
| 27 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.721 item 27 |
| 28 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.721 item 28 |
| 29 | FULLY_MAPPABLE | EXECUTABLE | INHERITED | T52 p.747 item 6-29; T44 p.721 item 29 |
| 30 | FULLY_MAPPABLE | EXECUTABLE | DIRECT | T52 p.748 item 30 |
| 31 | FULLY_MAPPABLE | EXECUTABLE | DIRECT | T52 p.748 item 31 |
| 32 | FULLY_MAPPABLE | EXECUTABLE | DIRECT | T52 p.748 item 32 |
| 33 | FULLY_MAPPABLE | EXECUTABLE | DIRECT | T52 p.748 item 33 |
| 34 | FULLY_MAPPABLE | EXECUTABLE | DIRECT | T52 p.748 item 34 |
| 35 | FULLY_MAPPABLE | EXECUTABLE | DIRECT | T52 p.748 item 35 |
| 36 | FULLY_MAPPABLE | EXECUTABLE | DIRECT | T52 p.748 item 36 |
| 37 | FULLY_MAPPABLE | EXECUTABLE | DIRECT | T52 p.748 item 37 |

## CLASSIFICATION_COUNTS

Final arithmetic from `mapping_audit.classification_counts`:

- FULLY_MAPPABLE = 27;
- SAFE_PARTIAL = 3;
- AMBIGUOUS = 1;
- ENGINE_UNSUPPORTED = 6;
- EXTERNAL = 0 primary classifications;
- SOURCE_CONFLICT = 0;
- total = 37.

The audit also stores the established project-style `summary` as exact requirement-code lists for each classification.

## FULL_MAPPED

FULLY_MAPPABLE codes:

`1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37`.

Key direct MSG034 mappings:

- REQ1: exactly one TrademarkApplicationDetails via selection cardinality.
- REQ5: every existing exact-QName AccompanyingDocumentsDetails must contain IPDocKindCode, DocId, DocCreationDate, DescriptionText, PageQuantity, DocBinaryText; the container itself remains optional.
- REQ30: at least one NamingAbilityProofDetails using selection cardinality on the exact child path.
- REQ31: five exact direct application children forbidden.
- REQ32: root RefusalDetails cardinality 0.
- REQ33: exact ValidityPeriodDetails/StartDateTime required.
- REQ34: exact ValidityPeriodDetails/EndDateTime forbidden.
- REQ35: SignatureDetails required, and OfficerDetails in a specific signature forbids direct sibling FullNameDetails in that same signature.
- REQ36: direct FullNameDetails in a specific signature forbids OfficerDetails in that same signature.
- REQ37: each signature-owned OfficerDetails requires nested LastName, FirstName, PositionName and forbids CommunicationDetails.

Inherited FULL mappings preserve the independently rechecked Table 44 semantics for REQ6–12, REQ14–15, REQ21–25, REQ27–29.

## PARTIAL_MAPPED

### REQ2 — SAFE_PARTIAL

SAFE_FRAGMENT: If `TrademarkApplicationDetails/ipsdo:IPDocKindCode` is present, same-parent `ipsdo:IPDocKindName` is forbidden.

UNMAPPED_REMAINDER:

- authoritative classifier-presence predicate;
- authoritative classifier lookup;
- equality of IPDocKindCode to the authoritative classifier code.

Reason: classifier availability and the authoritative code are external to the current evaluator.

### REQ3 — SAFE_PARTIAL

SAFE_FRAGMENT: If `TrademarkApplicationDetails/ipsdo:IPDocKindCode` is absent, same-parent `ipsdo:IPDocKindName` must equal exactly `Документ, содержащий доказательства в подтверждение приобретения заявленным обозначением различительной способности`.

UNMAPPED_REMAINDER:

- authoritative classifier-absence predicate.

Reason: the local fallback condition is necessary and exact; authoritative classifier absence is external.

### REQ4 — SAFE_PARTIAL

SAFE_FRAGMENT: `TrademarkApplicationDetails/ipsdo:TrademarkApplicationId` is required.

UNMAPPED_REMAINDER:

- external record existence;
- external StatusCode in `{01,02}`;
- external EndDateTime absence;
- external TrademarkApplicationId equality with the message value.

Reason: these remaining checks require the national patent-office application information resource and are not simulated locally.

## EXTERNAL

No requirement has `EXTERNAL` as its primary classification. External dependencies remain explicitly recorded only as the unmapped remainder of SAFE_PARTIAL REQ2, REQ3 and REQ4.

## AMBIGUOUS

REQ13 — AMBIGUOUS / UNMAPPED.

WHY NOT EXECUTABLE: the standalone Table 44 statement sets `IPPartyKindCode = AP` but does not identify a safe repeated `IPPartyDetails` owner/instance scope. Later requirements explicitly address PA and RE roles. A global AP assertion would strengthen/contradict the normative repeated-role model, so no executable rule was created.

## ENGINE_UNSUPPORTED

REQ16 — ENGINE_UNSUPPORTED / UNMAPPED. WHY: exact semantics depend on filtering the repeated IPPartyDetails to AP and then asserting a value constraint in the correlated repeated IPSubjectName context. Current evaluator lacks the required nested repeated correlation/filter semantics.

REQ17 — ENGINE_UNSUPPORTED / UNMAPPED. WHY: exact semantics require AP-scoped cardinality of a filtered IPSubjectName instance (`nameRepresentationKindCode=OR`) together with languageCode in that same nested instance. Current evaluator cannot express this exact filtered nested cardinality/correlation.

REQ18 — ENGINE_UNSUPPORTED / UNMAPPED. WHY: the rule refers to absence of the second IPSubjectName conditional on AP and languageCode=RU, requiring per-parent ordinal/repeated correlation unsupported by the evaluator.

REQ19 — ENGINE_UNSUPPORTED / UNMAPPED. WHY: the rule requires a second IPSubjectName only for the non-RU branch, with `nameRepresentationKindCode=LA` and languageCode absent in that second correlated instance. Exact ordinal/correlation semantics are unavailable.

REQ20 — ENGINE_UNSUPPORTED / UNMAPPED. WHY: the exact condition is AP-scoped and nested under the corresponding repeated party/address instance. It was not approximated by a global address-kind assertion because the current evaluator cannot safely preserve the required filtered AP correlation for this inherited condition.

REQ26 — ENGINE_UNSUPPORTED / UNMAPPED. WHY: Table 44 states that `TrademarkKindCode OR TrademarkKindName` must correspond to the allowed 110–180 code/name set in the same TrademarkDetails. The current evaluator has logical conditions for conditional rules but no standalone per-TrademarkDetails disjunctive value-membership assertion that expresses this requirement without strengthening OR into AND or depending on another requirement.

## SOURCE_CONFLICT

None. No MSG034 requirement was classified SOURCE_CONFLICT after the StructureDefinition owner/QName review.

## INHERITED_REQUIREMENTS

Every REQ6–29 audit entry has dual provenance: the Table 52 inheritance row and the exact original Table 44 row/page.

- REQ6: Table 52 p.747 item 6-29 + original Table 44 p.715 item 6.
- REQ7: Table 52 p.747 item 6-29 + original Table 44 p.715 item 7.
- REQ8: Table 52 p.747 item 6-29 + original Table 44 p.715 item 8.
- REQ9: Table 52 p.747 item 6-29 + original Table 44 p.716 item 9.
- REQ10: Table 52 p.747 item 6-29 + original Table 44 p.716 item 10.
- REQ11: Table 52 p.747 item 6-29 + original Table 44 p.716 item 11.
- REQ12: Table 52 p.747 item 6-29 + original Table 44 p.716 item 12.
- REQ13: Table 52 p.747 item 6-29 + original Table 44 p.716 item 13.
- REQ14: Table 52 p.747 item 6-29 + original Table 44 p.716 item 14.
- REQ15: Table 52 p.747 item 6-29 + original Table 44 p.717 item 15.
- REQ16: Table 52 p.747 item 6-29 + original Table 44 p.717 item 16.
- REQ17: Table 52 p.747 item 6-29 + original Table 44 p.717 item 17.
- REQ18: Table 52 p.747 item 6-29 + original Table 44 p.718 item 18.
- REQ19: Table 52 p.747 item 6-29 + original Table 44 p.718 item 19.
- REQ20: Table 52 p.747 item 6-29 + original Table 44 p.718 item 20.
- REQ21: Table 52 p.747 item 6-29 + original Table 44 p.719 item 21.
- REQ22: Table 52 p.747 item 6-29 + original Table 44 p.719 item 22.
- REQ23: Table 52 p.747 item 6-29 + original Table 44 p.719 item 23.
- REQ24: Table 52 p.747 item 6-29 + original Table 44 p.720 item 24.
- REQ25: Table 52 p.747 item 6-29 + original Table 44 p.720 item 25.
- REQ26: Table 52 p.747 item 6-29 + original Table 44 p.720 item 26.
- REQ27: Table 52 p.747 item 6-29 + original Table 44 p.721 item 27.
- REQ28: Table 52 p.747 item 6-29 + original Table 44 p.721 item 28.
- REQ29: Table 52 p.747 item 6-29 + original Table 44 p.721 item 29.

The executable rules for inherited FULL requirements carry the same dual provenance. REQ13, REQ16–20 and REQ26 retain dual provenance even though they remain unmapped.

## OR_AND_RECHECK

REQ26 was reread directly in original Table 44. Its `TrademarkKindCode OR TrademarkKindName` semantics were preserved by leaving the requirement ENGINE_UNSUPPORTED; no AND strengthening was introduced.

REQ27 was also reread directly. It is executable because the evaluator can express a same-`TrademarkDetails` `any` condition over TrademarkKindCode / TrademarkKindName for graphical/colour kinds 140–180 and require TrademarkPicture plus TrademarkColourName in that same parent context. Production XML tests exercise this rule independently.

## QNAME_OWNER_REVIEW

Exact QName/owner review found and preserved these distinctions:

- root `ipcdo:RefusalDetails` is not an application child;
- StartDateTime/EndDateTime are nested under `ResourceItemStatusDetails/ValidityPeriodDetails`;
- SignatureDetails is under TrademarkApplicationDetails;
- signature-owned OfficerDetails is scoped with exact `under`/collection ownership and is not confused with TrademarkClaimDetails/.../OfficerDetails;
- direct SignatureDetails/ccdo:FullNameDetails is distinct from OfficerDetails/ccdo:FullNameDetails;
- AccompanyingDocumentsDetails exists at both a direct application owner and a nested proof-document owner, and REQ5 deliberately targets the exact QName for every existing instance;
- wrong-namespace elements with the same local name are ignored by the exact QName selector/extractor tests.

## REPEATABLE_SEMANTICS

Production XML repeatability tests serialize/parse/extract real XML rather than only testing manually flattened dictionaries.

Covered cases include:

- direct AccompanyingDocumentsDetails good+good => PASS;
- bad+good and good+bad => FAIL;
- extracted missing child alignment explicitly preserves `[None, value]` and `[value, None]` rather than collapsing positions;
- repeated OfficerDetails good+good => PASS;
- bad+good and good+bad => FAIL with aligned PositionName values;
- multiple SignatureDetails preserve same-parent branch semantics with no cross-parent leakage;
- nested/direct AccompanyingDocumentsDetails are both selected by exact QName;
- wrong-owner and wrong-namespace collisions do not leak into MSG034 rules.

## OPTIONAL_BRANCHES

REQ5 preserves optional-container semantics: when both optional AccompanyingDocumentsDetails locations are absent, the rule is vacuously PASS and does not make the container mandatory.

REQ2/REQ3 preserve only safe local classifier branches; classifier presence/absence itself remains external.

REQ35/REQ36 preserve mutually exclusive signature branches per SignatureDetails without requiring one presentation style beyond the normative signature-presence requirement.

## SIGNATURE_SEMANTICS

REQ35–37 are scoped to exact SignatureDetails parents:

- at least one SignatureDetails is required;
- OfficerDetails and direct FullNameDetails cannot coexist within the same SignatureDetails;
- a direct FullNameDetails in one signature does not conflict with an OfficerDetails in another signature;
- each signature-owned OfficerDetails is independently validated for nested FirstName, LastName, PositionName and forbidden CommunicationDetails;
- an OfficerDetails under TrademarkClaimDetails is outside the REQ37 selector and cannot satisfy or fail the signature rule.

## PROVENANCE

Direct MSG034 requirements use confirmed Table 52 source refs with exact page/item metadata. Inherited REQ6–29 use both Table 52 item `6-29` on p.747 and the corresponding original Table 44 source ref. `mapping_audit` stores one primary classification for every REQ1–37, exact target paths, owner, repeatability note, provenance kind, reason and any external/engine remainder.

## MESSAGE_ISOLATION

Isolation proof is executable and message-code based:

- MSG032, MSG033 and MSG034 all use `R.IP.SP.02.002`, all have non-empty structured rule sets, and their rule-id sets are disjoint;
- validating the same extracted R.IP.SP.02.002 values for each requested message executes only that requested message's rule IDs;
- MSG034 execution contains only `P.SP.02.MSG.034.*` IDs and is disjoint from MSG032/MSG033 IDs;
- MSG031 was checked during review and uses `R.010`, not R.IP.SP.02.002, so it is not treated as a same-structure execution peer. Rule identity remains message-prefixed.

No stale `assert not rules034` isolation pattern was introduced.

## END_TO_END

The MSG034 end-to-end suite uses the production path:

`EaeuXmlEngine.build_body` -> `BodyPayload.serialize_xml_element` -> XML serialize -> XML parse -> `StructuredProcessBodyProvider._values_from_element` -> `validate_body`.

The valid document proves root QName, extraction, 33 PASS evaluations, transaction/action context and message isolation. Every FULL requirement has an independent negative production-XML proof; every SAFE_PARTIAL requirement has a negative proof only for its executable safe fragment.

## MSG034_TESTS

Final command:

`pytest -q P.SP.02_OP_22/tests/test_msg034_*.py`

Result: `63 passed in 1.87s`.

Additional focused check during finalization: `18 passed in 0.30s` for the valid pipeline, first repeatable case and full safe-mapping contract. Catalog loader check: `13 passed in 0.14s`.

## NEIGHBOR_REGRESSIONS

Executed after MSG034 implementation:

- `pytest -q P.SP.02_OP_22/tests/test_msg033_*.py` -> `73 passed in 2.05s`;
- `pytest -q P.SP.02_OP_22/tests/test_msg032_*.py` -> `65 passed in 1.81s`;
- `pytest -q P.SP.02_OP_22/tests/test_msg031_*.py` -> `84 passed in 1.70s`;
- `pytest -q P.SP.02_OP_22/tests/test_msg030_*.py` -> `119 passed in 3.29s`.

All match their supplied pre-MSG034 baselines.

## PSP02_TESTS

Final dedicated command on the final audit schema:

`pytest -q P.SP.02_OP_22/tests`

Result: `1453 passed in 49.86s`.

This is exactly 63 tests above the supplied pre-MSG034 baseline of 1390 passed.

## EAEU_XML_TESTS

Command:

`pytest -q eaeu_xml/tests`

Result: `265 passed, 43 skipped, 1042 subtests passed in 2.52s`.

No shared eaeu_xml source/test file was changed by this batch.

## ROOT_TESTS

Final root command on the final implementation state:

`pytest -q`

Result: `1842 passed, 43 skipped, 1152 subtests passed in 55.73s`.

This is 63 tests above the supplied pre-MSG034 root baseline of 1779 passed, with the same skip/subtest counts.

## PREEXISTING_CHANGES

The repository was dirty before this batch. The following `git status --short` baseline was captured before MSG034 edits and is treated as pre-existing work:

```text
 M AGENTS.md
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.001.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.003.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.004.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.005.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.006.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.007.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.009.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.010.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.011.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.013.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.014.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.016.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.017.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.018.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.019.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.020.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.021.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.022.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.024.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.027.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.028.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.029.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.030.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.031.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.032.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.033.yaml
 M eaeu_xml/src/eaeu_xml/process_packages/body.py
 M eaeu_xml/src/eaeu_xml/process_packages/engine.py
 M eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py
 M eaeu_xml/src/eaeu_xml/process_packages/validator.py
 M eaeu_xml/tests/test_structured_rules.py
?? P.SP.02_OP_22/tests/test_msg001_structured_rules.py
?? P.SP.02_OP_22/tests/test_msg003_embedded_one_of.py
?? P.SP.02_OP_22/tests/test_msg003_repeatable_xml_alignment.py
?? P.SP.02_OP_22/tests/test_msg003_table36_full_rules.py
?? P.SP.02_OP_22/tests/test_msg003_table36_safe_partial_inherited.py
?? P.SP.02_OP_22/tests/test_msg003_table37_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg004_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg004_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg004_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg005_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg005_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg005_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg006_010_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg006_010_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg006_010_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg011_014_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg011_014_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg011_014_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg016_019_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg016_019_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg016_019_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg020_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg020_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg020_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg021_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg021_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg021_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg022_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg022_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg024_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg024_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg027_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg027_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg027_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg028_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg028_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg028_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg029_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg029_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg029_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg030_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg030_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg030_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg031_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg031_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg031_rule_execution.py
?? P.SP.02_OP_22/tests/test_msg031_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg032_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg032_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg032_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg033_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg033_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg033_safe_mapping.py
?? codex_reports/
?? eaeu_xml/tests/test_embedded_one_of.py
?? eaeu_xml/tests/test_repeatable_xml_alignment.py
```

These files were not reset, cleaned, stashed, checked out, committed or otherwise rewritten by this batch unless they are explicitly listed under CURRENT_BATCH_CHANGES (none of the baseline entries are implementation-scope changes for MSG034).

## CURRENT_BATCH_CHANGES

Implementation/test delta relative to the captured pre-batch status:

```text
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.034.yaml
?? P.SP.02_OP_22/tests/test_msg034_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg034_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg034_safe_mapping.py
```

Additionally created/updated as explicitly allowed service output:

`codex_reports/MSG034_IMPLEMENTATION_REPORT.md`

The report directory itself was already present as an untracked pre-existing directory, so top-level `git status --short` reports it as `?? codex_reports/` both before and after this batch.

## PROTECTED_FILES

Protected baseline: `/tmp/msg034_protected_before.json`.

Final comparison:

- protected files: 36;
- missing: 0;
- SHA-256/mtime_ns mismatches: 0.

Therefore all protected MSG001–033/shared/StructureDefinition/test files remained byte-for-byte and mtime unchanged during the MSG034 batch.

## GIT_STATUS

Final captured `git status --short` (before writing this report; the already-untracked `codex_reports/` directory makes the status representation unchanged by this report file):

```text
 M AGENTS.md
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.001.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.003.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.004.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.005.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.006.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.007.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.009.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.010.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.011.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.013.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.014.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.016.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.017.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.018.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.019.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.020.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.021.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.022.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.024.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.027.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.028.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.029.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.030.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.031.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.032.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.033.yaml
 M P.SP.02_OP_22/message_rules/P.SP.02.MSG.034.yaml
 M eaeu_xml/src/eaeu_xml/process_packages/body.py
 M eaeu_xml/src/eaeu_xml/process_packages/engine.py
 M eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py
 M eaeu_xml/src/eaeu_xml/process_packages/validator.py
 M eaeu_xml/tests/test_structured_rules.py
?? P.SP.02_OP_22/tests/test_msg001_structured_rules.py
?? P.SP.02_OP_22/tests/test_msg003_embedded_one_of.py
?? P.SP.02_OP_22/tests/test_msg003_repeatable_xml_alignment.py
?? P.SP.02_OP_22/tests/test_msg003_table36_full_rules.py
?? P.SP.02_OP_22/tests/test_msg003_table36_safe_partial_inherited.py
?? P.SP.02_OP_22/tests/test_msg003_table37_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg004_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg004_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg004_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg005_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg005_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg005_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg006_010_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg006_010_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg006_010_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg011_014_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg011_014_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg011_014_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg016_019_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg016_019_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg016_019_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg020_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg020_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg020_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg021_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg021_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg021_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg022_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg022_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg024_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg024_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg027_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg027_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg027_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg028_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg028_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg028_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg029_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg029_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg029_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg030_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg030_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg030_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg031_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg031_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg031_rule_execution.py
?? P.SP.02_OP_22/tests/test_msg031_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg032_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg032_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg032_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg033_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg033_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg033_safe_mapping.py
?? P.SP.02_OP_22/tests/test_msg034_end_to_end.py
?? P.SP.02_OP_22/tests/test_msg034_repeatable_xml.py
?? P.SP.02_OP_22/tests/test_msg034_safe_mapping.py
?? codex_reports/
?? eaeu_xml/tests/test_embedded_one_of.py
?? eaeu_xml/tests/test_repeatable_xml_alignment.py
```

The only new implementation/test status delta versus the pre-batch baseline is the MSG034 YAML plus the three new MSG034 test files shown in CURRENT_BATCH_CHANGES.

## GIT_DIFF_CHECK

Final `git diff --check` = PASS, no output.

No git add/commit/reset/clean/checkout/stash operation was performed.

## DEFECTS_FOUND

No blocking production defect remains.

Two batch-local issues were found and corrected during implementation:

1. Initial REQ30/REQ35 mandatory-container checks used a parent-context presence assertion that sees repeatable container placeholders before serialization. They were replaced, within MSG034 mapping only, by exact `selection_cardinality` rules, matching the established evaluator pattern and StructureDefinition repeatability.
2. An initial isolation test attempted same-R002 execution for MSG031. Repository metadata confirmed MSG031 uses `R.010`; the test was corrected to use the actual same-structure peers MSG032/MSG033/MSG034.

These corrections required no shared engine change.

## REMAINING_REQUIREMENTS

Intentionally non-executable requirements remain documented rather than approximated:

- REQ13 — AMBIGUOUS owner/instance semantics for the standalone AP value statement.
- REQ16 — ENGINE_UNSUPPORTED AP-scoped nested repeat/filter correlation.
- REQ17 — ENGINE_UNSUPPORTED filtered nested cardinality/correlation.
- REQ18 — ENGINE_UNSUPPORTED second-instance/ordinal correlation for RU branch.
- REQ19 — ENGINE_UNSUPPORTED conditional second-instance/ordinal correlation for non-RU branch.
- REQ20 — ENGINE_UNSUPPORTED exact AP-scoped address correlation.
- REQ26 — ENGINE_UNSUPPORTED exact same-parent `TrademarkKindCode OR TrademarkKindName` allowed-value assertion; deliberately not strengthened to AND.

SAFE_PARTIAL external remainders also remain for REQ2–4 exactly as listed in PARTIAL_MAPPED. Resolving these would require classifier/external-resource capabilities or evaluator extensions outside the authorized MSG034 scope.

## FINAL_VERDICT

STATUS = COMPLETE

VERDICT = READY

Basis: complete 37-requirement audit; conservative classification; 27 FULL + 3 safe partial requirements executable without approximation; all required production/repeatable/isolation tests green; neighbor regressions green; P.SP.02 suite green; shared eaeu_xml suite green; final root suite green; 36 protected files unchanged; `git diff --check` PASS; no out-of-scope stale test remains.
