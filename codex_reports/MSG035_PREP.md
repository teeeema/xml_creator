# MSG035 implementation preparation

## STATUS

COMPLETE

## NORMATIVE_CONTEXT

- Message: `P.SP.02.MSG.035` — уведомление о необходимости представления документа о согласии.
- Transaction: `TRN.030`; procedure `PRC.011`; operations `OPR.044 -> OPR.045`; participants `ACT.002 -> ACT.001`; response `MSG.002`.
- Structure: `R.IP.SP.02.002` v1.0.0, root `{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails`.
- Table53, PDF pp.749–750. Transaction context p.654.

## INVENTORY

- Captured rows: **6** (`1,2,3,4,5,6–29`).
- Expanded requirements: **29** (`REQ1…REQ29`).
- REQ6–29 inherit original Table44 REQ6–29. Relevant original semantics were checked; Table44 REQ26 is Code **OR** Name and is not an AND rule.

## CLASSIFICATION

- FULLY_MAPPABLE (20): `1,4,5,6–12,14,15,21–25,27–29`.
- SAFE_PARTIAL (2): `2,3`.
- EXTERNAL: none primary.
- AMBIGUOUS (1): `13`.
- ENGINE_UNSUPPORTED (6): `16–20,26`.
- SOURCE_CONFLICT: none.

Arithmetic: 20 + 2 + 1 + 6 = 29.

## EXECUTABLE_RULES

| REQ | Class | Owner/path | Rule semantics |
|---:|---|---|---|
| 1 | FULL | `ipcdo:TrademarkApplicationDetails` | `selection_cardinality` 1..1 |
| 4 | FULL | `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime` | required per resource-status parent |
| 5 | FULL | same ancestor / `csdo:EndDateTime` | forbidden per resource-status parent |
| 6–12 | FULL | exact Table44 owners below APP | country codelist, address/communication, authority requirements; use QName/path-scoped `for_each` |
| 14–15 | FULL | filtered APP/IPPartyDetails and descendants | AP party/local mandatory fields; do not use index |
| 21–25 | FULL | PA/RE/correspondence/TrademarkDetails owners | exact Table44 presence/value rules |
| 27 | FULL | `APP/ipcdo:TrademarkDetails` | `for_each`; same-parent `any(kindCode, kindName)` -> Picture and ColourName required |
| 28 | FULL | same TrademarkDetails / CollectiveMarkIndicator | value `IN [0,1]` |
| 29 | FULL | `APP/ipcdo:GoodsBaseDetails` | required collection and per-goods required children |

`APP` is `ipcdo:TrademarkApplicationDetails`; its direct fields include `ipsdo:IPDocKindCode` and `ipsdo:TrademarkApplicationId`. APP repeats structurally, so all nested rules must preserve parent ownership even though REQ1 limits it to one valid instance.

## PARTIAL_RULES

| REQ | Safe fragment | Unmapped remainder |
|---:|---|---|
| 2 | direct APP `ipsdo:IPDocKindCode` required | authoritative classifier membership and code-to-literal correspondence for “Документальное подтверждение согласия правообладателей на регистрацию заявленного обозначения в качестве товарного знака (знака обслуживания) Евразийского экономического союза (письмо-согласие)” |
| 3 | direct APP `ipsdo:TrademarkApplicationId` required | filing-office record existence, status 01/02, absent external EndDateTime, external ID equality |

Do not infer classifier state from XML field presence. REQ2 must not invent a code value.

## UNMAPPED_RULES

- REQ13 `AMBIGUOUS`: AP instance scope is not safely separable from PA/RE instances without a normative discriminator beyond the Table44 wording.
- REQ16–20 `ENGINE_UNSUPPORTED`: AP-scoped nested repeated/cardinality/language/correlation semantics.
- REQ26 `ENGINE_UNSUPPORTED`: exact TrademarkKindCode **OR** TrademarkKindName semantics; no AND approximation.

## STRUCTURE_PATHS

- APP: `ipcdo:TrademarkApplicationDetails` (1..* root child).
- Document code: `APP/ipsdo:IPDocKindCode` (0..1).
- Application ID: `APP/ipsdo:TrademarkApplicationId` (1..1).
- Trademark: `APP/ipcdo:TrademarkDetails` (0..1); picture/colour repeat below it.
- Goods: `APP/ipcdo:GoodsBaseDetails` (0..*).
- Validity: `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime|EndDateTime`.
- Use exact namespaces from `R.IP.SP.02.002`; nested status/document `IPDocKindCode` must not satisfy REQ2.

## TEST_MATRIX

- Valid E2E: build → serialize → parse → extract → validate; one APP with required Table53/Table44 mapped subset.
- REQ1: zero and two APP fail.
- REQ2: missing direct APP code fails local fragment; wrong-namespace/nested code does not satisfy it.
- REQ3: missing direct ApplicationId fails; do not test external state locally.
- REQ4/5: missing Start and present End fail at exact validity owner.
- Every FULL inherited rule: one independent negative mutation and target rule-ID assertion.
- Per-parent: addresses, communications, party fields, REQ27 trademark branches, and goods use good+good / bad+good / good+bad.
- REQ27: test both kind-code and kind-name triggers; required children in a different TrademarkDetails parent must not cross-satisfy.
- QName collisions: nested/alternate-owner PatentAuthorityDetails, IPDocKindCode, and validity fields.
- Isolation: MSG033 and MSG034 use R002; assert requested MSG035 validation evaluates only MSG035-prefixed rules.

## IMPLEMENTATION_NOTES

Copy only reusable rule shapes from existing R002 messages; create MSG035-specific IDs/source provenance. Record Table53 direct source refs and dual provenance for each inherited REQ6–29. Do not change evaluator, classifiers, structure, or message metadata.

## READY_FOR_IMPLEMENTATION

YES.

Repository modifications: NONE.
