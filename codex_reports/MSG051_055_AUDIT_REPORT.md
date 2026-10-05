# P.SP.02.MSG.051–055 strict normative audit

## STATUS

COMPLETE

## VERDICT

READY_FOR_BATCH_MAPPING

## EXECUTIVE_SUMMARY

The normative PDF was independently reread locally through macOS PDFKit. Tables 49 and 69–73, their continuations, transaction contexts, structures, inherited rows, and all exact expanded counts were confirmed. Classifier and external predicates remain separate from local XML assertions. No OR was strengthened to AND.

## AUDIT_METHOD

Read-only PDFKit extraction from `ОП_22.pdf`: message list p.637; transaction contexts pp.692–700; original Table49 pp.735–740; Tables69–73 pp.790–804. Python PDF libraries `fitz`, `pypdf`, `PyPDF2`, and `pdfplumber` were unavailable; installed system PDFKit was available and read the source directly.

## EVALUATOR_CAPABILITY

Supported: presence/forbidden, selected cardinality, fixed values, conditions, `for_each`, exact QName/path and `qname + under`, filtering, attributes, nested repeats, and sparse alignment. Unsupported for this audit: classifier/external lookup, cross-resource equality, semantic-role correlation, typed date ordering, set difference/equality, conditional filtered cardinality, and generic sibling-QName OR cardinality.

## MSG051

### NORMATIVE_CONTEXT

Invalidity/termination of Union trademark protection. `TRN.046`, `PRC.028`, `OPR.151 -> OPR.152`, `ACT.002 -> ACT.001`, response `MSG.002` (pp.692–693).

### STRUCTURE

`R.IP.SP.02.007` v1.0.0; root `{urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}TrademarkRegisterDetails`; register records are repeated.

### TABLE

Table69 pp.790–792; captured 10; REQ6–19 inherit Table49 REQ6–19; expanded 23.

### REQUIREMENT_MATRIX

REQ1 partial: local TrademarkId required, filing-office resource/status/end/equality external. REQ2 full: exactly one record. REQ3–4 partial: classifier code/name branches, with two exact fallback literals; classifier state external. REQ5 full: required direct RegistrationCancellationDetails and its reason code/NationalPatentDecisionDetails. REQ6–17 full Table49 paths. REQ18–19 unsupported Table49 conditional collective-mark correlation/OR. REQ20–22 full same-SignatureDetails pattern. REQ23 full StartDateTime under ResourceItemStatusDetails/ValidityPeriodDetails.

### FULLY_MAPPABLE

2, 5–17, 20–23.

### SAFE_PARTIAL

1, 3, 4.

### EXTERNAL

None primary.

### SOURCE_CONFLICT

None.

### AMBIGUOUS

None.

### ENGINE_UNSUPPORTED

18–19.

### CRITICAL_SEMANTICS

REQ5 makes optional structural cancellation details normatively required. Signature rules are per SignatureDetails parent.

### QNAME_RISKS

Document kind, date, FullNameDetails, and CommunicationDetails recur under other owners.

### REPEATABLE_RISKS

All record rules execute per record; test good+good/bad+good/good+bad.

### OPTIONALITY

Cancellation and signature containers follow Table69, not structural optionality alone.

### FUTURE_TEST_PLAN

E2E; record 0/1/2; missing cancellation container/children; status/signature matrices; missing StartDateTime; QName collisions.

### IMPLEMENTATION_READINESS

READY_FOR_MAPPING.

## MSG052

### NORMATIVE_CONTEXT

Cancellation of Union trademark registration. `TRN.047`, `PRC.029`, `OPR.155 -> OPR.156`, `ACT.001 -> ACT.002`, response `MSG.002` (pp.694–695).

### STRUCTURE

`R.IP.SP.02.007` v1.0.0.

### TABLE

Table70 pp.793–797; captured 18; REQ6–19 inherit Table49; expanded 31.

### REQUIREMENT_MATRIX

REQ1 full 1..2 records. REQ2 full exactly one semantic cancellation record: status 04, EventDate, no codeListId. REQ3 unsupported: cancellation-goods condition requires second semantic new-registration record. REQ4 full status-01 new record. REQ5 partial: local cancellation-record TrademarkId; resource condition external. REQ6–17 full; REQ18–19 unsupported. REQ20 partial: new-record TrademarkId; uniqueness external. REQ21–22 unsupported external/cross-record typed date comparisons. REQ23 full cancellation details children. REQ24 unsupported cross-record TrademarkId/TrademarkNewId equality. REQ25–28 partial classifier branches scoped by role, with exact PDF literals. REQ29–31 full signature pattern.

### FULLY_MAPPABLE

1, 2, 4, 6–17, 23, 29–31.

### SAFE_PARTIAL

5, 20, 25–28.

### EXTERNAL

None primary.

### SOURCE_CONFLICT

None.

### AMBIGUOUS

None: roles are normatively distinguished by status/meaning, not index.

### ENGINE_UNSUPPORTED

3, 18, 19, 21, 22, 24.

### CRITICAL_SEMANTICS

Never map cancellation/new-registration roles to indexes. REQ28’s PDF fallback literal begins lowercase `решение`; retain its literal exactness.

### QNAME_RISKS

The two role records share QNames; status-scoped selectors are required.

### REPEATABLE_RISKS

Test both role orders and indicator-triggered second record.

### OPTIONALITY

Cancellation details are role-specific in REQ23.

### FUTURE_TEST_PLAN

1/2-record E2E, both orders, role-local classifier/details tests, no execution of unsupported date/equality semantics, QName collisions.

### IMPLEMENTATION_READINESS

READY_FOR_MAPPING.

## MSG053

### NORMATIVE_CONTEXT

Extension of exclusive-right term. `TRN.048`, `PRC.030`, `OPR.163 -> OPR.164`, `ACT.001 -> ACT.002`, response `MSG.002` (pp.696–697).

### STRUCTURE

`R.IP.SP.02.007` v1.0.0.

### TABLE

Table71 pp.798–801; captured 14; REQ6–19 inherit Table49; expanded 26.

### REQUIREMENT_MATRIX

REQ1 partial local TrademarkId/resource external. REQ2–3 full exact-one record/EndDateTime forbidden. REQ4–5 partial classifier consequences and exact fallback. REQ6–17 full, REQ18–19 unsupported. REQ20 full status 03/EventDate/no codeListId. REQ21–23 unsupported external validity-date set count/equality-except-one/maximum ordering. REQ24–26 full signature pattern.

### FULLY_MAPPABLE

2, 3, 6–17, 20, 24–26.

### SAFE_PARTIAL

1, 4, 5.

### EXTERNAL

None primary.

### SOURCE_CONFLICT

None.

### AMBIGUOUS

None.

### ENGINE_UNSUPPORTED

18, 19, 21–23.

### CRITICAL_SEMANTICS

REQ21–23 are external set semantics, never positional/scalar date comparisons.

### QNAME_RISKS

DocValidityDate is direct under the register record; other date fields cannot substitute.

### REPEATABLE_RISKS

Date collections require set semantics.

### OPTIONALITY

EndDateTime is normatively forbidden.

### FUTURE_TEST_PLAN

E2E; cardinality; forbidden end; status/classifier/signature negatives; Table49 matrices; prove date-set rules stay unmapped.

### IMPLEMENTATION_READINESS

READY_FOR_MAPPING.

## MSG054

### NORMATIVE_CONTEXT

Request for duty amount/payment details. `TRN.049`, `PRC.033`, `OPR.176 -> OPR.177`, `ACT.001 -> ACT.002`, responses `MSG.055` and `MSG.025` (pp.699–700).

### STRUCTURE

`R.IP.SP.03.003` v1.0.0; root `{urn:EEC:R:IP:SP:03:IPDutyDetails:v1.0.0}`.

### TABLE

Table72 pp.801–803; captured/expanded 7.

### REQUIREMENT_MATRIX

REQ1–3 full PatentAuthorityDetails country/name/address and AddressKindCode=2. REQ4–5 partial legal-action classifier code/name consequences; classifier state external. REQ6 full TrademarkApplicationId required. REQ7 full listed fields, including IPPaymentDetails, forbidden.

### FULLY_MAPPABLE

1–3, 6–7.

### SAFE_PARTIAL

4–5.

### EXTERNAL / SOURCE_CONFLICT / AMBIGUOUS / ENGINE_UNSUPPORTED

None primary.

### CRITICAL_SEMANTICS

REQ7 forbids IPPaymentDetails in the request.

### QNAME_RISKS

Use R003 owners only; do not reuse R007 paths.

### REPEATABLE_RISKS

No index-based semantics identified.

### OPTIONALITY

Structurally optional payment details are normatively forbidden.

### FUTURE_TEST_PLAN

E2E; each authority field/address kind; classifier branch tests; missing application ID; each forbidden field; wrong-owner collisions.

### IMPLEMENTATION_READINESS

READY_FOR_MAPPING.

## MSG055

### NORMATIVE_CONTEXT

Duty amount/payment details: response of TRN.049/PRC.033, `OPR.177`, `ACT.002 -> ACT.001` (pp.699–700).

### STRUCTURE

`R.IP.SP.03.003` v1.0.0.

### TABLE

Table73 pp.803–804; captured 4; REQ1–6 inherit Table72 REQ1–6; expanded 9.

### REQUIREMENT_MATRIX

REQ1–3,6 full from Table72; REQ4–5 partial classifier branches. REQ7 unsupported: IPPaymentDetails required and BankAccountDetails **OR** PaymentSystemAccountDetails must exist. REQ8 full forbids EventDateTime/IPPartyDetails/AccompanyingDocumentsDetails under payment. REQ9 full forbids TrademarkApplicationId/DocId/PaymentAmount/DutyPaymentIndicator.

### FULLY_MAPPABLE

1–3, 6, 8–9.

### SAFE_PARTIAL

4–5.

### EXTERNAL / SOURCE_CONFLICT / AMBIGUOUS

None primary.

### ENGINE_UNSUPPORTED

7.

### CRITICAL_SEMANTICS

REQ7 is inclusive OR: bank-only, payment-system-only, and both pass; neither fails. AND strengthening is prohibited.

### QNAME_RISKS

Account branches must be direct payment children.

### REPEATABLE_RISKS

No account position semantics.

### OPTIONALITY

PaymentDetails is normatively required despite structural optionality.

### FUTURE_TEST_PLAN

E2E; payment absent; bank-only/payment-system-only/both PASS; neither FAIL once exact support exists; REQ8/9 forbidden fields; inherited Table72 tests; MSG054/055 isolation.

### IMPLEMENTATION_READINESS

READY_FOR_MAPPING.

## CROSS_BATCH_SUMMARY

| MSG | Table | Structure | Expanded | FULL | PARTIAL | EXTERNAL | CONFLICT | AMBIGUOUS | UNSUPPORTED | Readiness |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 051 | 69 | R.IP.SP.02.007 | 23 | 18 | 3 | 0 | 0 | 0 | 2 | READY |
| 052 | 70 | R.IP.SP.02.007 | 31 | 19 | 6 | 0 | 0 | 0 | 6 | READY |
| 053 | 71 | R.IP.SP.02.007 | 26 | 18 | 3 | 0 | 0 | 0 | 5 | READY |
| 054 | 72 | R.IP.SP.03.003 | 7 | 5 | 2 | 0 | 0 | 0 | 0 | READY |
| 055 | 73 | R.IP.SP.03.003 | 9 | 6 | 2 | 0 | 0 | 0 | 1 | READY |

Each row sums to its expanded count.

## ISOLATION_MATRIX

MSG051–053 share R007/QNames: MSG051 termination, MSG052 semantic cancellation/new-record roles, MSG053 forbidden end and external validity-date sets. MSG054/055 share R003 and are request/response: MSG054 forbids payment details while MSG055 requires them. All rules must be message-scoped.

## SOURCE_CONFLICT_REGISTER

NONE. PDF and exact repository paths for executable fragments agree. Placeholders were excluded.

## COMMON_ENGINE_LIMITATIONS

MSG051–053 REQ18–19: collective-mark conditional cross-collection/document OR. MSG052 REQ3,21,22,24: semantic-role conditional cardinality, equality, date ordering. MSG053 REQ21–23: external validity-date set operations. MSG055 REQ7: sibling-QName OR; requiring both accounts is prohibited.

## FUTURE_PRODUCTION_XML_STRATEGY

Source-derived E2E fixtures; independent negative proof for each full rule; 0/1/2 cardinality; good+good/bad+good/good+bad per-parent cases; both MSG052 role orders; optional PASS/FAIL by normative row; wrong QName/owner collision cases; assert unsupported/external rules remain unmapped.

## IMPLEMENTATION_ORDER

MSG054 then MSG055 for R003 request/response isolation and account OR; MSG051 then MSG053 for ordinary R007/status/date fixture; MSG052 last for semantic roles and cross-record risk.

## CONCURRENT_CHANGES_IGNORED

Concurrent MSG033 work was excluded.

## REPOSITORY_STATE

Pre-existing dirty worktree preserved. Only this permitted report changed.

## FINAL_VERDICT

READY_FOR_BATCH_MAPPING.

Repository modifications: NONE.
