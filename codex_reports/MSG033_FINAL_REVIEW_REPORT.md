# MSG033 independent final review

## STATUS

COMPLETE

## VERDICT

READY

## EXECUTIVE_SUMMARY

Independent PDF reread, structure review, YAML review, production XML test review, isolation review, and required regressions confirm MSG033 as ready. No blocking defect was found. The implementation preserves Table44 REQ26 OR by leaving it unmapped, scopes REQ27 to the same TrademarkDetails parent, and keeps external/classifier and evaluator-limited requirements out of executable rules.

## INDEPENDENCE

The implementation reports were treated only as hypotheses. Normative source was reread directly from `ОП_22.pdf` using local PDFKit: Table51 pp.743–746; original Table44 REQ6–29 pp.714–721; transaction context for TRN.028. Repository captures, StructureDefinition, YAML, tests and evaluator were independently inspected.

## NORMATIVE_CONTEXT

`P.SP.02.MSG.033` is “сведения о результатах внутригосударственного обжалования решения по экспертизе”. Confirmed context: `TRN.028`, `PRC.007`, `OPR.025 -> OPR.026`, `ACT.002 -> ACT.001`, response `MSG.002`, structure `R.IP.SP.02.002` v1.0.0.

## STRUCTURE

Root QName: `{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails`. Direct `ipcdo:TrademarkApplicationDetails` is the message owner; all mapped descendants use exact namespace/path. Repeated descendants are evaluated per owning parent.

## EXPANDED_INVENTORY

Table51 has direct REQ1–5, inherited REQ6–29, and direct REQ30–37: **37** expanded requirements.

| Class | Requirements | Count |
|---|---|---:|
| FULLY_MAPPABLE | 1,2,6–12,14–15,21–25,27–37 | 27 |
| SAFE_PARTIAL | 3–5 | 3 |
| AMBIGUOUS | 13 | 1 |
| ENGINE_UNSUPPORTED | 16–20,26 | 6 |
| EXTERNAL | none primary | 0 |
| SOURCE_CONFLICT | none | 0 |

Arithmetic: 27 + 3 + 1 + 6 = 37.

## REQUIREMENT_REVIEW_MATRIX

| REQ | Normative meaning | Independent class | Implementation | Executable | Owner/QName | Test verdict |
|---:|---|---|---|---|---|---|
| 1 | exactly one application | FULL | FULL | yes | direct APP | CONFIRMED |
| 2 | APP status 10/20, no codeListId | FULL | FULL | yes | APP/status/StatusCode | CONFIRMED |
| 3–4 | classifier document code/name branches | PARTIAL | PARTIAL | safe local consequences | direct APP document fields | CONFIRMED |
| 5 | local ApplicationId plus filing-office record | PARTIAL | PARTIAL | local presence only | direct APP/ApplicationId | CONFIRMED |
| 6–12 | Table44 country/address/communication/authority | FULL | FULL | yes | exact per-owner paths | CONFIRMED |
| 13 | AP party scope | AMBIGUOUS | AMBIGUOUS | no | repeated IPPartyDetails | CONFIRMED |
| 14–15 | AP party fields | FULL | FULL | yes | filtered party parent | CONFIRMED |
| 16–20 | AP nested/cardinality/correlation | UNSUPPORTED | UNSUPPORTED | no | nested repeated paths | CONFIRMED |
| 21–25 | PA/RE/correspondence/trademark details | FULL | FULL | yes | exact scoped owners | CONFIRMED |
| 26 | trademark kind Code OR Name | UNSUPPORTED | UNSUPPORTED | no | same TrademarkDetails | CONFIRMED |
| 27–29 | visual kind consequence/indicator/goods | FULL | FULL | yes | same trademark/goods parent | CONFIRMED |
| 30 | TrademarkRegistrationCode required | FULL | FULL | yes | direct APP | CONFIRMED |
| 31–33 | signature branches | FULL | FULL | yes | same SignatureDetails/Officer | CONFIRMED |
| 34 | ApplicantComplainResponseDetails required | FULL | FULL | yes | direct APP | CONFIRMED |
| 35 | RefusalDetails forbidden | FULL | FULL | yes | direct APP | CONFIRMED |
| 36–37 | validity Start required/End forbidden | FULL | FULL | yes | ResourceItemStatusDetails/ValidityPeriodDetails | CONFIRMED |

## REQ1_5_REVIEW

REQ1 is exact 1..1 application cardinality. REQ2 uses StatusCode `IN [10,20]` and forbids `@codeListId` within the same APP status owner. REQ3’s code-present => name-forbidden and REQ4’s code-absent => exact fallback-name checks are necessary local consequences of the two classifier branches; they do not assert classifier membership. REQ5 maps only unconditionally required local ApplicationId and does not execute filing-office status/end/equality semantics.

## TABLE44_REVIEW

Table51 explicitly inherits Table44 REQ6–29, with dual source provenance in the mapping audit and structured rules. Original Table44 semantics were reread. Exact per-parent fields are mapped only where the DSL can preserve ownership.

## REQ13_REVIEW

CONFIRMED AMBIGUOUS. Table44 does not identify a safe repeated-party instance scope for the AP statement that would coexist with explicit PA/RE semantics. A global requirement would be invalid; no positional inference is permitted.

## REQ16_20_REVIEW

CONFIRMED ENGINE_UNSUPPORTED. These require exact AP-scoped nested repeated selection, conditional cardinality, ordinal/language semantics, or cross-collection correlation unavailable in the current DSL without approximation.

## REQ26_REVIEW

CONFIRMED. Original Table44 REQ26 is `TrademarkKindCode OR TrademarkKindName`, never AND. MSG033 emits no structured rule for REQ26. This avoids prohibited OR-to-AND strengthening.

## REQ27_REVIEW

CONFIRMED. The `for_each TrademarkDetails` rule uses same-parent `any` over kind code/name and requires Picture plus ColourName in that exact parent. Production tests cover good+good, bad+good, good+bad and both trigger alternatives; children from another trademark cannot satisfy the condition.

## REQ30_37_REVIEW

PDF confirms: REQ30 direct TrademarkRegistrationCode required; REQ31–33 exact signature pattern; REQ34 direct ApplicantComplainResponseDetails required; REQ35 direct RefusalDetails forbidden; REQ36 exact validity StartDateTime required; REQ37 corresponding EndDateTime forbidden. YAML targets match structure owners/QNames.

## SIGNATURE_REVIEW

Normative same-signature semantics and implementation match. Production XML proves Officer-only PASS, direct-FullName-only PASS, both branches in one signature FAIL, different valid branches across two signatures PASS, missing PositionName FAIL, and Officer CommunicationDetails FAIL. Nested Officer FullNameDetails is not confused with direct SignatureDetails FullNameDetails.

## QNAME_OWNER_REVIEW

Exact owners were verified for status/document fields, ApplicationId, authority, trademark kind/picture/colour, registration code, complaint response, refusal, signature/officer/full-name/communication, and validity dates. Tests prove wrong-namespace StatusCode and response fields fail, and nested complaint PatentAuthorityDetails does not satisfy direct authority rules.

## REPEATABLE_REVIEW

Production XML tests exercise SubjectAddressDetails, CommunicationDetails, AP/RE in both orders, TrademarkDetails, GoodsBaseDetails and SignatureDetails. Each relevant parent-local matrix includes good+good PASS, bad+good FAIL, good+bad FAIL. Shared sparse alignment tests remain green; no positional shifting or cross-parent leakage was observed.

## TEST_QUALITY_REVIEW

The E2E fixture uses `build -> serialize -> parse -> extract -> validate`, rather than injected flattened values. Every FULL requirement has an independent mutation and target rule-ID assertion; each PARTIAL local fragment has a negative proof; unmapped requirements are not presented as executable. No false-positive test mechanism was found.

## MESSAGE_ISOLATION_REVIEW

Confirmed: MSG031, MSG032, and MSG033 structured rule sets are non-empty and pairwise disjoint. MSG032 validates only MSG032 IDs and explicitly excludes MSG031/033; MSG033 validates only MSG033 IDs and excludes MSG031/032. The maintained MSG032 assertion now requires `rules033` to be non-empty while preserving all disjointness assertions.

## MSG033_TESTS

`73 passed in 1.92s`.

## MSG032_TESTS

`65 passed in 1.64s`.

## MSG031_TESTS

`84 passed in 1.70s`.

## PSP02_TESTS

`1390 passed in 45.15s`.

## EAEU_XML_TESTS

`265 passed, 43 skipped, 1042 subtests passed in 2.60s`.

## ROOT_TESTS

`1779 passed, 43 skipped, 1152 subtests passed in 65.44s`.

## DEFECTS

None.

## NON_BLOCKING_FINDINGS

None.

## GIT_STATE

`git diff --check` passed. The worktree contained pre-existing concurrent changes. This review added only the permitted report and did not modify implementation, tests, metadata, structures, classifiers, or sources.

## FINAL_VERDICT

READY.

Repository modifications: NONE.
