# MSG047 writer handoff

## STATUS

COMPLETE. Existing MSG046–050 audit is the classification authority. Only executable R.IP.SP.02.007 paths were checked. No tests or production files changed.

## NORMATIVE_CONTEXT

P.SP.02.MSG.047 — преобразование коллективного знака Союза в товарный знак Союза. TRN.042 / PRC.024, request-response, OPR120 → OPR121, ACT001 → ACT002, response MSG002. Structure R.IP.SP.02.007 v1.0.0; root `{urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}TrademarkRegisterDetails`. Table 65, physical pages 780–782. REQ6–19 inherit Table 49 REQ6–19.

## INVENTORY

`CAPTURED_ROWS = 12`; `EXPANDED_REQUIREMENTS = 25`; `REQ_LIST = 1–25`.

REQ6–19 retain dual provenance: Table 65 REQ6–19 plus the identically numbered Table 49 row.

## CLASSIFICATION

| Class | Requirements | Count |
|---|---|---:|
| FULLY_MAPPABLE | 2–3, 6–17, 20–25 | 20 |
| SAFE_PARTIAL | 1, 4–5 | 3 |
| ENGINE_UNSUPPORTED | 18–19 | 2 |
| EXTERNAL / AMBIGUOUS / SOURCE_CONFLICT | — | 0 |

Arithmetic: **20 + 3 + 2 = 25**.

## EXECUTABLE_RULES

All record-scoped rules execute per `{ipcdo}UnifiedRegisterRecordsDetails` (`1..*`).

- REQ1 | SAFE_PARTIAL | record direct `{ipsdo}TrademarkId` | see Partial Rules.
- REQ2 | FULLY_MAPPABLE | root record collection | MSG047-specific exact cardinality **1..1**.
- REQ3 | FULLY_MAPPABLE | record/`{ipcdo}IPEntityStatusDetails` | its EventDate required; its StatusCode exactly `"03"`; its `StatusCode/@codeListId` forbidden.
- REQ4–5 | SAFE_PARTIAL | direct record `{ipsdo}IPDocKindCode` and `IPDocKindName` | see Partial Rules.
- REQ6–17 | FULLY_MAPPABLE | Table 49 inherited rules under the same record | universal country/address/communication, authority, RH party, trademark, and goods rules. Preserve Table 65 + matching Table 49 provenance and all established same-parent filters.
- REQ18–19 | ENGINE_UNSUPPORTED | Table 49 inherited | no executable mapping.
- REQ20 | FULLY_MAPPABLE | record/`{ipcdo}TransformationDetails` (`0..*`) | for each existing container, require its `{ipsdo}TransformationKindName`, `{ipsdo}IPObjectId`, and `{csdo}EventDate`. **CONTAINER_EXISTENCE_NOT_INTRODUCED**.
- REQ21 | FULLY_MAPPABLE | record/`{ipcdo}TrademarkDetails/{ipsdo}CollectiveMarkIndicator` | fixed `"0"`.
- REQ22 | FULLY_MAPPABLE | record/`{ccdo}ResourceItemStatusDetails/{ccdo}ValidityPeriodDetails/{csdo}EndDateTime` | forbidden. No StartDateTime requirement.
- REQ23 | FULLY_MAPPABLE | record/`{ipcdo}SignatureDetails` | required; direct OfficerDetails present implies direct sibling FullNameDetails forbidden. **SAME_PARENT_REQUIRED**.
- REQ24 | FULLY_MAPPABLE | same SignatureDetails | direct FullNameDetails present implies direct OfficerDetails forbidden. **SAME_PARENT_REQUIRED**.
- REQ25 | FULLY_MAPPABLE | same signature/OfficerDetails | Officer requires its FullNameDetails/LastName/FirstName and PositionName; its CommunicationDetails forbidden. **SAME_PARENT_REQUIRED**.

## PARTIAL_RULES

- REQ1 | SAFE_PARTIAL  
  **SAFE_FRAGMENT:** direct record TrademarkId required.  
  **UNMAPPED_REMAINDER:** external national resource, active-status predicate (01 or 03), no external EndDateTime, and identifier equality.
- REQ4 | SAFE_PARTIAL  
  **SAFE_FRAGMENT:** if direct record IPDocKindCode is present, direct same-record IPDocKindName is forbidden.  
  **UNMAPPED_REMAINDER:** classifier presence and equality to its authoritative code.
- REQ5 | SAFE_PARTIAL  
  **SAFE_FRAGMENT:** if direct record IPDocKindCode is absent, direct same-record IPDocKindName equals «Ходатайство о преобразовании коллективного знака Евразийского экономического союза в товарный знак, знак обслуживания Евразийского экономического союза».  
  **UNMAPPED_REMAINDER:** classifier absence predicate.

## UNMAPPED_RULES

- REQ18–19 | ENGINE_UNSUPPORTED | Table 49 collective-mark UE-party and charter-document conditional existence/correlation across repeated collections. Do not approximate it by position, global cardinality, or Code-and-Name AND logic.

## STRUCTURE_PATHS

Namespaces: `ipcdo={urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}`; `ipsdo={urn:EEC:M:IP:SimpleDataObjects:vZ.Z.Z}`; `ccdo={urn:EEC:M:ComplexDataObjects:vX.X.X}`; `csdo={urn:EEC:M:SimpleDataObjects:vX.X.X}`.

- Record: `{ipcdo}UnifiedRegisterRecordsDetails`, `1..*`; its direct TrademarkId is `0..1`.
- Status: record/`{ipcdo}IPEntityStatusDetails` `0..1`; StatusCode `1..1`, EventDate `0..1`, and `@codeListId` is an attribute `0..1`.
- TransformationDetails is direct record child `0..*`; its three REQ20 children are each `0..1`.
- TrademarkDetails is direct record child `0..1`; CollectiveMarkIndicator is its direct child `1..1`.
- Resource status is direct record child `1..1`; ValidityPeriodDetails is `0..1`; EndDateTime is `0..1`.
- SignatureDetails is direct record child `0..1`. Its direct OfficerDetails and direct FullNameDetails are distinct paths; Officer FullNameDetails owns LastName/FirstName, and PositionName is direct under Officer.
- Exact QName and ancestor ownership are mandatory. Status EventDate, Transformation EventDate, and other same-local-name fields cannot substitute for one another.

## REPEATABLE_NOTES

Per-record rules must retain record context: good+good passes; bad+good and good+bad fail. REQ20 is per existing TransformationDetails, not cross-container. Signature checks remain within one SignatureDetails parent. No role or positional mapping is permitted.

## COLLISION_RISKS

- Repeated register records.
- Status owner versus resource status and TransformationDetails EventDate.
- Direct document-kind fields versus descendant document-kind fields.
- CollectiveMarkIndicator under the wrong TrademarkDetails.
- Signature OfficerDetails versus stakeholder/nested officers; direct FullNameDetails versus Officer FullNameDetails.
- `codeListId` attribute versus element and wrong namespace.

## TEST_MATRIX

- Inventory: 12 captured rows, 25 expanded, classification arithmetic, dual provenance REQ6–19, MSG047-specific IDs.
- Valid E2E: build → serialize → parse → production extract → validate.
- REQ1: negative only for local TrademarkId fragment.
- REQ2: zero records fail; one passes; two fail.
- REQ3: missing EventDate, non-03 StatusCode, codeListId present, and wrong-owner status each fail.
- REQ4–5: test only the listed safe fragments, never classifier lookup.
- REQ6–17: negative proof per executable inherited requirement.
- REQ18–19: assert no executable mapping.
- REQ20: each missing child fails when its TransformationDetails exists; absent container passes.
- REQ21: 0 passes, 1 fails; retain future MSG048 isolation note for its expected reverse literal.
- REQ22: EndDateTime absent passes; present fails.
- REQ23–25: same-parent and repeated-record good+good / bad+good / good+bad.
- Message isolation: rules scoped only to MSG047.

## IMPLEMENTATION_NOTES

Implement the 20 FULL requirements plus only the stated safe fragments. Do not add classifier or external-resource lookup, cross-collection correlation, positional selection, or a mandatory TransformationDetails container. Do not copy MSG046's required EndDateTime or MSG048's expected indicator literal.

## READY_FOR_IMPLEMENTATION

YES.

