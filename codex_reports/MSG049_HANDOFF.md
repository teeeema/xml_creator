# MSG049 writer handoff

## STATUS

COMPLETE. Existing MSG046–050 audit is the classification authority. Only Table 67 wording and executable R.IP.SP.02.007 paths were checked. No tests or production files changed.

## NORMATIVE_CONTEXT

P.SP.02.MSG.049 — внесение изменений в сведения Единого реестра ТЗ Союза. TRN.044 / PRC.026, request-response, OPR136 → OPR137, ACT001 → ACT002, response MSG002. Structure R.IP.SP.02.007 v1.0.0; root `{urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}TrademarkRegisterDetails`. Table 67, physical pages 785–787. REQ6–19 inherit Table 49 REQ6–19.

## INVENTORY

`CAPTURED_ROWS = 11`; `EXPANDED_REQUIREMENTS = 24`.

`REQ_LIST = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25`.

REQ6–19 retain dual provenance: Table 67 REQ6–19 plus the matching Table 49 row.

## CLASSIFICATION

| Class | Requirements | Count |
|---|---|---:|
| FULLY_MAPPABLE | 2–17, 23–25 | 19 |
| SAFE_PARTIAL | 1, 21–22 | 3 |
| ENGINE_UNSUPPORTED | 18–19 | 2 |
| EXTERNAL / AMBIGUOUS / SOURCE_CONFLICT | — | 0 |

Arithmetic: **19 + 3 + 2 = 24**.

## EXECUTABLE_RULES

All record-scoped rules execute per `{ipcdo}UnifiedRegisterRecordsDetails` (`1..*`).

- REQ1 | SAFE_PARTIAL | direct record `{ipsdo}TrademarkId` | see Partial Rules.
- REQ2 | FULLY_MAPPABLE | root record collection | MSG049-specific exact cardinality **1..1**.
- REQ3 | FULLY_MAPPABLE | record/`{ccdo}ResourceItemStatusDetails/{ccdo}ValidityPeriodDetails/{csdo}StartDateTime` | required.
- REQ4 | FULLY_MAPPABLE | same record validity owner/`{csdo}EndDateTime` | forbidden.
- REQ5 | FULLY_MAPPABLE | record/`{ipcdo}IPEntityStatusDetails` | its EventDate required; its StatusCode exactly `"03"`; its `StatusCode/@codeListId` forbidden.
- REQ6–17 | FULLY_MAPPABLE | Table 49 inherited rules under the same record | universal country/address/communication, authority, RH party, trademark, and goods rules. Preserve Table 67 and matching Table 49 provenance.
- REQ18–19 | ENGINE_UNSUPPORTED | inherited Table 49 | no executable mapping.
- REQ21–22 | SAFE_PARTIAL | direct record IPDocKindCode/IPDocKindName | see Partial Rules.
- REQ23 | FULLY_MAPPABLE | record/`{ipcdo}SignatureDetails` | required; direct OfficerDetails present implies direct sibling FullNameDetails forbidden. **SAME_PARENT_REQUIRED**.
- REQ24 | FULLY_MAPPABLE | same SignatureDetails | direct FullNameDetails present implies direct OfficerDetails forbidden. **SAME_PARENT_REQUIRED**.
- REQ25 | FULLY_MAPPABLE | same signature/OfficerDetails | Officer requires its FullNameDetails/LastName/FirstName and PositionName; its CommunicationDetails forbidden. **SAME_PARENT_REQUIRED**.

## PARTIAL_RULES

- REQ1 | SAFE_PARTIAL  
  **SAFE_FRAGMENT:** direct record TrademarkId required.  
  **UNMAPPED_REMAINDER:** external national resource, active-status predicate (01 or 03), no external EndDateTime, and identifier equality.
- REQ21 | SAFE_PARTIAL  
  **SAFE_FRAGMENT:** if direct record IPDocKindCode is present, direct same-record IPDocKindName is forbidden.  
  **UNMAPPED_REMAINDER:** classifier presence and equality to its authoritative code.
- REQ22 | SAFE_PARTIAL  
  **SAFE_FRAGMENT:** if direct record IPDocKindCode is absent, direct same-record IPDocKindName equals exactly «Заявление о внесении изменений в сведения Единого реестра товарных знаков, знаков обслуживания Евразийского экономического союза».  
  **UNMAPPED_REMAINDER:** classifier absence predicate.

## UNMAPPED_RULES

- REQ18–19 | ENGINE_UNSUPPORTED | Table 49 collective-mark UE-party and charter-document conditional existence/correlation across repeated collections. Do not approximate with position, global cardinality, cross-collection matching, or Code-and-Name AND.

## NORMATIVELY_ABSENT_REQUIREMENTS

**REQ20 = NORMATIVELY_ABSENT.** Table 67 contains no REQ20. The numbering intentionally jumps from REQ19 to REQ21. Do not create a rule, classification, mapping-audit placeholder, or test that treats REQ20 as captured.

## STRUCTURE_PATHS

Namespaces: `ipcdo={urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}`; `ipsdo={urn:EEC:M:IP:SimpleDataObjects:vZ.Z.Z}`; `ccdo={urn:EEC:M:ComplexDataObjects:vX.X.X}`; `csdo={urn:EEC:M:SimpleDataObjects:vX.X.X}`.

- Record: `{ipcdo}UnifiedRegisterRecordsDetails` `1..*`; direct TrademarkId/IPDocKindCode/IPDocKindName are `0..1`.
- Resource status: direct record ResourceItemStatusDetails `1..1`; ValidityPeriodDetails `0..1`; StartDateTime and EndDateTime each `0..1`. Other date branches cannot satisfy REQ3–4.
- Entity status: direct record IPEntityStatusDetails `0..1`; StatusCode `1..1`, EventDate `0..1`, and `@codeListId` is an attribute `0..1`.
- SignatureDetails is direct record child `0..1`. Direct OfficerDetails and direct FullNameDetails are distinct; Officer FullNameDetails owns LastName/FirstName, and PositionName is direct under Officer.
- Exact QName and full ancestor ownership are mandatory.

## REPEATABLE_NOTES

Record requirements are local to one record: good+good passes; bad+good and good+bad fail where repeatability is relevant. Signature conditions remain within one SignatureDetails parent. REQ2 still requires exactly one record; use two-record fixtures only for negative cardinality and inherited per-parent proofs.

## COLLISION_RISKS

- Repeated register records.
- Resource status versus entity status.
- StartDateTime/EndDateTime under an incorrect owner.
- Entity-status EventDate versus other EventDate fields.
- Direct document-kind fields versus descendant fields.
- Signature OfficerDetails versus stakeholder/nested officers; direct signature FullNameDetails versus Officer FullNameDetails.
- `codeListId` attribute versus element and wrong namespace.

## TEST_MATRIX

- Inventory: 11 captured rows, exact 24-code list, REQ20 absent, arithmetic, mapped/unmapped sets, dual Table 67/Table 49 provenance, MSG049 IDs.
- Valid E2E: build → serialize → parse → production extract → validate.
- REQ1: negative only for local TrademarkId fragment.
- REQ2: zero records fail; one passes; two fail.
- REQ3: missing or wrong-owner StartDateTime fails.
- REQ4: EndDateTime absent passes; present fails.
- REQ5: missing EventDate, non-03 StatusCode, codeListId present, and wrong-owner status fail.
- REQ6–17: negative proof per executable inherited requirement.
- REQ18–19: assert no executable mapping.
- REQ20: assert normatively absent, without any classification.
- REQ21–22: safe-fragment tests only; REQ22 uses the exact Table 67 literal.
- REQ23–25: same-parent signature proofs.
- Repeated-record good+good / bad+good / good+bad where applicable.
- Message isolation: MSG049 rules only; do not reuse MSG047/048 transformation rules.

## IMPLEMENTATION_NOTES

Implement 19 FULL requirements and the three stated safe fragments. Do not add classifier or external-resource lookup, cross-collection correlation, positional selection, or synthetic REQ20. MSG049 requires StartDateTime and forbids EndDateTime; preserve that message-specific pair.

## READY_FOR_IMPLEMENTATION

YES.

