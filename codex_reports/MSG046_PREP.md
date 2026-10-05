# MSG046 writer handoff

## STATUS

COMPLETE. Existing audit used as the classification authority; only executable R.IP.SP.02.007 paths were checked. No tests ran and no production or test file changed.

## NORMATIVE_CONTEXT

P.SP.02.MSG.046 — сведения о преобразовании аннулированной регистрации ТЗ Союза в национальную заявку. TRN.041 / PRC.023, request-response, OPR112 → OPR113, ACT001 → ACT002, response MSG002. Structure R.IP.SP.02.007 v1.0.0, root `{urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}TrademarkRegisterDetails`. Table 64, physical PDF pages 778–779; 9 captured and expanded requirements, no inheritance.

## INVENTORY

`CAPTURED_ROWS = 9`; `EXPANDED_REQUIREMENTS = 9`; `REQ_LIST = 1–9`.

## CLASSIFICATION

| Class | Requirements | Count |
|---|---|---:|
| FULLY_MAPPABLE | 4–9 | 6 |
| SAFE_PARTIAL | 1–3 | 3 |
| EXTERNAL / AMBIGUOUS / ENGINE_UNSUPPORTED / SOURCE_CONFLICT | — | 0 |

Arithmetic: **6 + 3 = 9**.

## EXECUTABLE_RULES

All rules iterate each `{ipcdo}UnifiedRegisterRecordsDetails` record (`1..*`).

- REQ1 | SAFE_PARTIAL | record direct `{ipsdo}IPDocKindCode` / `{ipsdo}IPDocKindName` | see Partial Rules.
- REQ2 | SAFE_PARTIAL | same direct owner | see Partial Rules.
- REQ3 | SAFE_PARTIAL | record direct `{ipsdo}TrademarkId` (`0..1`) | required.
- REQ4 | FULLY_MAPPABLE | record/`{ipcdo}TrademarkNationalApplicationDetails` (`0..1`) | container is normatively required; inside the **same container**, require `{csdo}UnifiedCountryCode`, `{ipsdo}NationalApplicationId`, and `{ipsdo}NationalApplicationReceiptDate` (each structurally `0..1`). A child under another owner cannot satisfy it.
- REQ5 | FULLY_MAPPABLE | record/`{ipcdo}IPEntityStatusDetails`/`{csdo}StatusCode` and `{csdo}EventDate` | EventDate required; StatusCode exactly `"06"`; `StatusCode/@codeListId` forbidden. The attribute is not an element.
- REQ6 | FULLY_MAPPABLE | record/`{ccdo}ResourceItemStatusDetails/{ccdo}ValidityPeriodDetails/{csdo}EndDateTime` | EndDateTime required. No StartDateTime requirement is introduced.
- REQ7 | FULLY_MAPPABLE | record/`{ipcdo}SignatureDetails` (`0..1`) | required; direct OfficerDetails present implies direct sibling FullNameDetails forbidden. **SAME_PARENT_REQUIRED**.
- REQ8 | FULLY_MAPPABLE | same SignatureDetails | direct FullNameDetails present implies direct OfficerDetails forbidden. **SAME_PARENT_REQUIRED**.
- REQ9 | FULLY_MAPPABLE | same SignatureDetails/OfficerDetails | Officer requires its FullNameDetails/LastName/FirstName and PositionName; its CommunicationDetails forbidden. **SAME_PARENT_REQUIRED**.

## PARTIAL_RULES

- REQ1 | SAFE_PARTIAL  
  **SAFE_FRAGMENT:** if the direct record IPDocKindCode is present, direct same-record IPDocKindName is forbidden.  
  **UNMAPPED_REMAINDER:** authoritative classifier presence and equality of IPDocKindCode to its code.
- REQ2 | SAFE_PARTIAL  
  **SAFE_FRAGMENT:** if direct record IPDocKindCode is absent, direct same-record IPDocKindName equals the Table 64 fallback literal: «Ходатайство о преобразовании аннулированной регистрации товарного знака, знака обслуживания Евразийского экономического союза в национальную заявку на регистрацию товарного знака, знака обслуживания».  
  **UNMAPPED_REMAINDER:** authoritative classifier absence predicate.
- REQ3 | SAFE_PARTIAL  
  **SAFE_FRAGMENT:** direct record TrademarkId is required.  
  **UNMAPPED_REMAINDER:** external national-resource record, StatusCode 04, populated external EndDateTime, and equality to the external record.

## UNMAPPED_RULES

No fully unmapped requirement. The classifier and external-resource portions remain explicitly unmapped inside REQ1–3.

## STRUCTURE_PATHS

Namespaces: `ipcdo={urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}`; `ipsdo={urn:EEC:M:IP:SimpleDataObjects:vZ.Z.Z}`; `ccdo={urn:EEC:M:ComplexDataObjects:vX.X.X}`; `csdo={urn:EEC:M:SimpleDataObjects:vX.X.X}`.

- Record direct fields include IPDocKindCode/Name, TrademarkId, and IPEntityStatusDetails; same local names under nested status and other branches are not valid substitutes.
- NationalApplicationDetails is a direct record child only. Its country, national identifier, and receipt date must share that owner.
- Status is the direct record IPEntityStatusDetails owner; EventDate and StatusCode must be below it.
- Resource status is record/`ccdo:ResourceItemStatusDetails`; its validity period is nested, not a global/root status.
- Signature rules use record/`ipcdo:SignatureDetails` and its direct OfficerDetails and direct FullNameDetails. Stakeholder/nested officers do not qualify.

## REPEATABLE_NOTES

Records are repeated. For every per-record rule: good+good passes; bad+good and good+bad fail. Evaluate signature mutual exclusion inside one SignatureDetails parent only; an Officer in one record/signature cannot affect a FullNameDetails in another.

## COLLISION_RISKS

- Repeated UnifiedRegisterRecordsDetails needs per-record context.
- Wrong IPEntityStatusDetails or root/resource status must not satisfy REQ5.
- NationalApplicationDetails children must not cross parent boundaries.
- `codeListId` is a StatusCode attribute.
- Direct signature OfficerDetails differs from stakeholder/nested officers.
- Exact namespace and QName are mandatory.

## TEST_MATRIX

- Valid MSG046 E2E: build → serialize → parse → production extract → validate.
- Negative proof each FULL.
- REQ1–3 negatives only for the listed safe fragment.
- REQ4: missing container and separately missing country, national identifier, and receipt date.
- REQ5: missing EventDate, wrong StatusCode, codeListId present, and wrong-owner collision.
- REQ6: missing EndDateTime.
- REQ7–9 same-parent and repeated-record good+good / bad+good / good+bad cases.
- MSG046 isolation.

## IMPLEMENTATION_NOTES

Implement the six FULL requirements and only the stated fragments for REQ1–3. Do not hard-code classifier lookup or external-resource status/equality. Preserve the structural optionality of NationalApplicationDetails while enforcing its MSG046 normative requiredness.

## READY_FOR_IMPLEMENTATION

YES.

