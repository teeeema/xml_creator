# P.SP.02.MSG.046–050 normative audit

## STATUS

COMPLETE

## VERDICT

READY_FOR_BATCH_MAPPING

## EXECUTIVE_SUMMARY

All five messages, their transactions, structures, rule tables, direct rows and Table 49 inheritance were identified. They share `R.IP.SP.02.007` v1.0.0 but have distinct status, transformation, and terminal-date semantics; future rules must always be message-scoped. No source conflict that blocks a safe mapping batch was identified. Classifier, external-resource, and evaluator-limited portions are explicitly separated below.

## AUDIT_METHOD

Read-only review of the normative rule captures and source references for Tables 64–68, original Table 49 REQ6–19, transaction/message metadata, and `R.IP.SP.02.007`. Evaluator capability was determined from `rules_engine.py`, `validator.py`, and existing shared alignment tests. No placeholders were investigated. No implementation, YAML, tests, source refs, or metadata were changed.

## EVALUATOR_CAPABILITY

Supported: required/forbidden presence, scalar and selected cardinality, fixed values, `IN`/`NOT_IN`, `all`/`any`/`not`, conditional presence/value, `for_each`, exact path/QName selection including `qname + under`, `where`, nested repeated descendants, sparse positional alignment, and attributes.

Unsupported or unsafe for this batch: classifier lookup, external-resource lookup, cross-instance/resource equality, conditional filtered cardinality over another repeated collection, cross-collection correlation, ordinal semantics, and exact classifier-dependent OR branches where code/name membership must be correlated.

## MSG046

### NORMATIVE_CONTEXT

`P.SP.02.MSG.046`: сведения о преобразовании аннулированной регистрации ТЗ Союза в национальную заявку на регистрацию ТЗ. `TRN.041`, `PRC.023`, `OPR.112 -> OPR.113`, `ACT.001 -> ACT.002`, response `MSG.002`. Transaction context p.680; message list p.636.

### STRUCTURE

`R.IP.SP.02.007` v1.0.0, root `{urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}TrademarkRegisterDetails`. `UnifiedRegisterRecordsDetails` is repeated (1..*). Direct NationalApplicationDetails is optional 0..1; SignatureDetails is optional 0..1 per record; ResourceItemStatusDetails validity dates are nested per record.

### TABLE

Table 64, pp.778–779. Captured rows 9; expanded count 9; no inherited range.

### REQUIREMENT_MATRIX

| REQ | Meaning / owner | Classification | Mapping recommendation |
|---|---|---|---|
| 1–2 | direct record document-kind classifier branches | SAFE_PARTIAL | local code-present/name-forbidden and code-absent/exact fallback only; keep classifier predicate external |
| 3 | direct `ipsdo:TrademarkId` plus national-resource status/end/equality | SAFE_PARTIAL | require local TrademarkId; do not simulate external record |
| 4 | direct `TrademarkNationalApplicationDetails`: country, national ID, receipt date | FULLY_MAPPABLE | require container and listed children at exact owner |
| 5 | record status EventDate, StatusCode=06, StatusCode/@codeListId forbidden | FULLY_MAPPABLE | per record |
| 6 | record validity EndDateTime required | FULLY_MAPPABLE | exact nested owner |
| 7–9 | SignatureDetails, direct FullName vs Officer exclusion, Officer children/communication forbidden | FULLY_MAPPABLE | per same SignatureDetails parent; use QName+under to avoid descendant collision |

### CRITICAL_SEMANTICS

REQ4 requires the NationalApplicationDetails branch despite its structural optionality. REQ7–9 are same-signature-parent rules: an Officer under one signature cannot forbid a direct FullName under another record.

### QNAME_RISKS

`IPDocKindCode`, `EventDate`, `FullNameDetails`, and `CommunicationDetails` recur below other owners. Direct path/QName ownership is mandatory.

### REPEATABLE_RISKS

All record rules require per-`UnifiedRegisterRecordsDetails` execution. Test good+good, bad+good, and good+bad for status, national application, end date, and signatures.

### FUTURE_TEST_PLAN

Valid E2E; missing each REQ4 child; status 06/date/codeListId matrix; EndDateTime absent; both signature branches and mixed signatures across two records; wrong-owner and wrong-namespace collisions.

### IMPLEMENTATION_READINESS

READY_FOR_MAPPING

## MSG047

### NORMATIVE_CONTEXT

`P.SP.02.MSG.047`: сведения о преобразовании коллективного знака Союза в ТЗ Союза. `TRN.042`, `PRC.024`, `OPR.120 -> OPR.121`, `ACT.001 -> ACT.002`, response `MSG.002`. Transaction context p.683; message list p.636.

### STRUCTURE

Same `R.IP.SP.02.007` root and repeated record owner.

### TABLE

Table 65, pp.780–782. Captured rows 12; REQ6–19 inherit original Table 49 REQ6–19; expanded count 25.

### REQUIREMENT_MATRIX

| REQ | Meaning / owner | Classification |
|---|---|---|
| 1 | local TrademarkId plus external active-resource correspondence | SAFE_PARTIAL |
| 2 | exactly one register record | FULLY_MAPPABLE |
| 3 | record status date, code 03, no codeListId | FULLY_MAPPABLE |
| 4–5 | classifier branches for transformation request | SAFE_PARTIAL |
| 6–17 | inherited Table 49 universal country/address/communication, authority, RH party, trademark and goods requirements | FULLY_MAPPABLE |
| 18–19 | inherited collective-mark UE-party and charter-document conditional existence/correlation | ENGINE_UNSUPPORTED |
| 20 | existing TransformationDetails requires kind name, object ID, EventDate | FULLY_MAPPABLE |
| 21 | record CollectiveMarkIndicator=0 | FULLY_MAPPABLE |
| 22 | record EndDateTime forbidden | FULLY_MAPPABLE |
| 23–25 | signature pattern | FULLY_MAPPABLE |

### CRITICAL_SEMANTICS

REQ20 applies per existing TransformationDetails (0..*): absence is vacuous unless a different normative row requires the container. REQ18–19 are conditional repeated/cross-collection semantics and must not be approximated by array position.

### QNAME_RISKS

Transformation EventDate is distinct from status EventDate. Direct document-kind fields are distinct from status/document descendants.

### REPEATABLE_RISKS

Use two records and two TransformationDetails for every per-parent assertion; test RH party by role in both orders.

### FUTURE_TEST_PLAN

E2E; REQ2 zero/two records; status 03; indicator 0; EndDateTime present; each transformation child; signature matrix; Table49 address/communication/party/trademark/goods matrices; explicitly assert REQ18–19 remain unmapped.

### IMPLEMENTATION_READINESS

READY_FOR_MAPPING

## MSG048

### NORMATIVE_CONTEXT

`P.SP.02.MSG.048`: сведения о преобразовании ТЗ Союза в коллективный знак Союза. `TRN.043`, `PRC.025`, `OPR.128 -> OPR.129`, `ACT.001 -> ACT.002`, response `MSG.002`. Transaction context p.685; message list p.637.

### STRUCTURE

Same `R.IP.SP.02.007` root and repeated record owner.

### TABLE

Table 66, pp.783–784. Captured rows 12; REQ6–19 inherit Table 49 REQ6–19; expanded count 25.

### REQUIREMENT_MATRIX

REQ1 SAFE_PARTIAL (local TrademarkId only; resource state external); REQ2–3 FULLY_MAPPABLE; REQ4–5 SAFE_PARTIAL classifier branches; REQ6–17 FULLY_MAPPABLE inherited Table 49; REQ18–19 ENGINE_UNSUPPORTED inherited conditional correlation; REQ20 FULLY_MAPPABLE TransformationDetails children; REQ21 FULLY_MAPPABLE `CollectiveMarkIndicator=1`; REQ22 FULLY_MAPPABLE EndDateTime forbidden; REQ23–25 FULLY_MAPPABLE signature pattern.

### CRITICAL_SEMANTICS

This message is not MSG047 with a substituted indicator: its classifier literals describe the reverse transformation and REQ21 requires `1`, not `0`. Keep message rule IDs and fallback literal isolated.

### QNAME_RISKS

Same as MSG047, especially `EventDate` under status versus TransformationDetails and document-kind local-name collisions.

### REPEATABLE_RISKS

Same per-record/per-transformation risks as MSG047; conditional collective-mark requirements must remain unmapped rather than use record index.

### FUTURE_TEST_PLAN

MSG047 plan with reverse transformation literals and indicator=1, including explicit negative cross-message isolation against MSG047.

### IMPLEMENTATION_READINESS

READY_FOR_MAPPING

## MSG049

### NORMATIVE_CONTEXT

`P.SP.02.MSG.049`: сведения о внесении изменений в сведения Единого реестра ТЗ Союза. `TRN.044`, `PRC.026`, `OPR.136 -> OPR.137`, `ACT.001 -> ACT.002`, response `MSG.002`. Transaction context p.687; message list p.637.

### STRUCTURE

Same `R.IP.SP.02.007` root and repeated record owner.

### TABLE

Table 67, pp.785–787. Captured rows 11; REQ6–19 inherit Table 49 REQ6–19; expanded count 24 (there is no REQ20).

### REQUIREMENT_MATRIX

REQ1 SAFE_PARTIAL (local TrademarkId); REQ2–5 FULLY_MAPPABLE (one record; StartDateTime required; EndDateTime forbidden; status date/code=03/no codeListId); REQ6–17 FULLY_MAPPABLE inherited Table49; REQ18–19 ENGINE_UNSUPPORTED; REQ21–22 SAFE_PARTIAL classifier branches for the amendment statement; REQ23–25 FULLY_MAPPABLE signature pattern.

### CRITICAL_SEMANTICS

REQ3/4 target the record validity dates, not merely a similarly named status or registration date. The missing REQ20 is normative table numbering, not a synthetic omission.

### QNAME_RISKS

StartDateTime/EndDateTime must resolve via `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails`, not another date branch.

### REPEATABLE_RISKS

Though REQ2 requires one record, future negative tests must prove zero and two record failures. Table49 per-parent branches still need two-parent fixture coverage.

### FUTURE_TEST_PLAN

E2E; cardinality zero/two; Start missing; End present; status codeListId; classifier branch/fallback tests without classifier simulation; signature and inherited Table49 matrices.

### IMPLEMENTATION_READINESS

READY_FOR_MAPPING

## MSG050

### NORMATIVE_CONTEXT

`P.SP.02.MSG.050`: сведения об отказе от исключительного права на ТЗ Союза. `TRN.045`, `PRC.027`, `OPR.144 -> OPR.145`, `ACT.001 -> ACT.002`, response `MSG.002`. Transaction context p.690; message list p.637.

### STRUCTURE

Same `R.IP.SP.02.007` root and repeated record owner.

### TABLE

Table 68, pp.788–789. Captured rows 10; REQ6–19 inherit Table 49 REQ6–19; expanded count 23.

### REQUIREMENT_MATRIX

REQ1 SAFE_PARTIAL (local TrademarkId; national-resource correspondence external); REQ2–3 FULLY_MAPPABLE (one record, EndDateTime required); REQ4–5 SAFE_PARTIAL classifier branches; REQ6–17 FULLY_MAPPABLE inherited Table49; REQ18–19 ENGINE_UNSUPPORTED; REQ20 FULLY_MAPPABLE status date/code=05/no codeListId; REQ21–23 FULLY_MAPPABLE signature pattern.

### CRITICAL_SEMANTICS

MSG050 requires EndDateTime, the opposite of MSG047–049. This is a high isolation risk. Do not reuse a shared message-local fixed rule without message scoping.

### QNAME_RISKS

Same direct status/validity/signature ownership distinctions as the other R007 messages.

### REPEATABLE_RISKS

EndDateTime required must be tested per record despite exact-one record requirement; inherited requirements require their own repeatable fixtures.

### FUTURE_TEST_PLAN

E2E; zero/two record cardinality; End missing; status 05; classifier fallback; full signature matrix; Table49 matrices; MSG050 vs MSG047–049 terminal-date isolation.

### IMPLEMENTATION_READINESS

READY_FOR_MAPPING

## CROSS_BATCH_SUMMARY

| MSG | Table | Structure | Expanded | FULL | PARTIAL | EXTERNAL | CONFLICT | AMBIGUOUS | UNSUPPORTED | Readiness |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 046 | 64 | R.IP.SP.02.007 | 9 | 6 | 3 | 0 | 0 | 0 | 0 | READY_FOR_MAPPING |
| 047 | 65 | R.IP.SP.02.007 | 25 | 20 | 3 | 0 | 0 | 0 | 2 | READY_FOR_MAPPING |
| 048 | 66 | R.IP.SP.02.007 | 25 | 20 | 3 | 0 | 0 | 0 | 2 | READY_FOR_MAPPING |
| 049 | 67 | R.IP.SP.02.007 | 24 | 19 | 3 | 0 | 0 | 0 | 2 | READY_FOR_MAPPING |
| 050 | 68 | R.IP.SP.02.007 | 23 | 18 | 3 | 0 | 0 | 0 | 2 | READY_FOR_MAPPING |

Each row sums to its expanded count.

## ISOLATION_MATRIX

All pairs share R.IP.SP.02.007 and therefore exact QName overlap.

| Pair | Potential conflict | Differentiator |
|---|---|---|
| 046/047 | status and terminal date | 06/end required vs 03/end forbidden |
| 046/048 | status and terminal date | 06/end required vs 03/end forbidden, indicator=1 |
| 046/049 | status and terminal date | 06/end required vs 03/start required/end forbidden |
| 046/050 | terminal date | 06 vs 05; both end required |
| 047/048 | reverse transformation | indicator 0 vs 1 and distinct classifier literal |
| 047/049 | same status 03 | transformation branch vs amendment classifier/start date |
| 047/050 | terminal/status | end forbidden/03 vs end required/05 |
| 048/049 | status/terminal | transformation indicator 1 vs amendment start/end |
| 048/050 | terminal/status | end forbidden/03 vs end required/05 |
| 049/050 | terminal date | end forbidden/03 vs end required/05 |

## SOURCE_CONFLICT_REGISTER

No blocking source conflict identified. Table 67’s absent REQ20 is a table-numbering fact; do not synthesize it. The shared X.X.X/Y.Y.Y/Z.Z.Z placeholders were intentionally excluded.

## COMMON_ENGINE_LIMITATIONS

Table 49 REQ18–19 require conditional existence and role/document correlation across repeated collections. The current evaluator cannot express them exactly. Leave them unmapped unless evaluator capability changes; do not replace them with global cardinality, first-item, or Code-and-Name AND rules.

## FUTURE_PRODUCTION_XML_STRATEGY

For each message create one valid build→serialize→parse→extract→validate fixture. For every FULL rule add an independent mutation. For every per-parent branch use good+good, bad+good, good+bad. Verify both semantic-role orders where roles exist. Add wrong namespace, wrong owner, direct-versus-nested same-local-name, and optional-container tests. Test absent optional TransformationDetails as PASS; test required NationalApplicationDetails in MSG046 as FAIL when absent.

## IMPLEMENTATION_ORDER

Implement MSG046 first to establish R007 record/status/validity/signature fixture without Table49 inheritance. Then MSG047 and MSG048 together, sharing the Table49 fixture while proving reverse-transformation isolation. Implement MSG049 next for start/end date variation and its deliberate gap at REQ20. Implement MSG050 last because it reuses Table49 but reverses the terminal-date rule and needs explicit isolation from MSG047–049. This order maximizes fixture reuse without mixing message-specific rules.

## CONCURRENT_CHANGES_IGNORED

Concurrent MSG033 work was ignored and was not read as a normative baseline or reported as a defect.

## REPOSITORY_STATE

The worktree was already dirty before this audit. No production or test file was modified by this audit. The only output is this report.

## FINAL_VERDICT

READY_FOR_BATCH_MAPPING

Repository modifications: NONE.
