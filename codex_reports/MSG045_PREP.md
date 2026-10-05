# MSG045 implementation preparation

## STATUS

COMPLETE. Read-only specification based on the local OP_22 PDF read with PDFKit. No production or test file changed; no tests were run.

## NORMATIVE_CONTEXT

PDF-confirmed: **P.SP.02.MSG.045** — «Сведения о внесении изменений в заявку на ТЗ Союза»; structure **R.IP.SP.02.002 v1.0.0**; Table **63**, physical PDF pages **773–777**.

Transaction context is **P.SP.02.TRN.040**, procedure **P.SP.02.PRC.022**, request/response, **OPR104 → OPR105**, **ACT001 → ACT002**, request MSG045 and response **P.SP.02.MSG.002**. The navigation checkpoint is confirmed. Table 63 inherits REQ6–29 from **Table 44** with identical numbering; relevant source rows are on physical PDF pages **715–721**.

## INVENTORY

`CAPTURED_ROWS = 12`: 1–5, 6–29, 30–35.

`EXPANDED_REQUIREMENTS = 35`; `REQ_LIST = 1–35`.

Each REQ6–29 has dual provenance: Table 63 REQ6–29 plus the matching Table 44 row. Table 63 applies them to one application instance and has no role-specific application qualification.

## CLASSIFICATION

| Class | Requirements | Count |
|---|---|---:|
| FULLY_MAPPABLE | 1, 3, 6–12, 14–15, 21–25, 27–29, 31–35 | 24 |
| SAFE_PARTIAL | — | 0 |
| EXTERNAL | 2, 4–5 | 3 |
| AMBIGUOUS | 13 | 1 |
| ENGINE_UNSUPPORTED | 16–20, 26, 30 | 7 |
| SOURCE_CONFLICT | — | 0 |

Arithmetic: **24 + 0 + 3 + 1 + 7 + 0 = 35**.

## EXECUTABLE_RULES

Namespace ownership is exact: `ipcdo={urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}`, `ipsdo={urn:EEC:M:IP:SimpleDataObjects:vZ.Z.Z}`, `ccdo={urn:EEC:M:ComplexDataObjects:vX.X.X}`, `csdo={urn:EEC:M:SimpleDataObjects:vX.X.X}`.

- REQ1 | FULLY_MAPPABLE | root `{ipcdo}TrademarkApplicationDetails` | exact cardinality **1..1**.
- REQ3 | FULLY_MAPPABLE | root `{ccdo}ResourceItemStatusDetails/{ccdo}ValidityPeriodDetails/{csdo}EndDateTime` | EndDateTime forbidden.
- REQ6–12 | FULLY_MAPPABLE | Table 44, exact application descendants | receipt date required; present country code requires `@codeListId="ВОИС ST.3"`; address/communication completeness and forbidden-name semantics; PatentAuthority country and authority/address rules.
- REQ14–15 | FULLY_MAPPABLE | application/`{ipcdo}IPPartyDetails`, filtered by same-parent `{ipsdo}IPPartyKindCode="AP"` | exactly one AP, then required AP fields.
- REQ21–22 | FULLY_MAPPABLE | same `IPPartyDetails`, filtered by `PA` or `RE` | required fields belong to that selected party.
- REQ23–25 | FULLY_MAPPABLE | correspondence-address and `{ipcdo}TrademarkDetails` descendants of the application | fixed address kind/country set and required trademark container/children.
- REQ27 | FULLY_MAPPABLE | same `TrademarkDetails` | when KindCode **or** KindName is 140/150/160/170/180, TrademarkPicture and TrademarkColourName are required. **SAME_PARENT_REQUIRED**.
- REQ28–29 | FULLY_MAPPABLE | same trademark/application | CollectiveMarkIndicator is `"0"` or `"1"`; each GoodsBaseDetails has required class code/name and goods name.
- REQ31 | FULLY_MAPPABLE | application/`{ipcdo}IPEntityStatusDetails` | required; same-owner StatusCode `"02"`; StatusCode `@codeListId` forbidden.
- REQ32 | FULLY_MAPPABLE | same application status owner | EventDate, DocId, IPDocReceiptDate, and DescriptionText required. DescriptionText is repeatable but at least one is required.
- REQ33 | FULLY_MAPPABLE | application/`{ipcdo}SignatureDetails` | at least one signature; direct OfficerDetails present implies direct sibling FullNameDetails forbidden. **SAME_PARENT_REQUIRED**.
- REQ34 | FULLY_MAPPABLE | same SignatureDetails | direct FullNameDetails present implies direct OfficerDetails forbidden. **SAME_PARENT_REQUIRED**.
- REQ35 | FULLY_MAPPABLE | same signature/OfficerDetails | Officer requires its FullNameDetails/LastName/FirstName and PositionName; its CommunicationDetails forbidden. **SAME_PARENT_REQUIRED**.

## PARTIAL_RULES

None. Rules with authoritative classifier or external-resource predicates remain non-executable rather than inferring their predicate from message fields.

## UNMAPPED_RULES

- REQ2 | EXTERNAL | external national-patent-office resource must contain an active record with StatusCode 01 or 02, no EndDateTime, and a matching triple of application identifier, status, and StartDateTime.
- REQ4–5 | EXTERNAL | classifier lookup decides the code-versus-name branch for four enumerated amendment document kinds; REQ5 additionally requires the appropriate exact document-kind name.
- REQ13 | AMBIGUOUS | Table 44 globally says IPPartyKindCode is AP, whereas REQ21–22 expressly recognize PA and RE party instances. Its scope cannot safely be made global.
- REQ16–20 | ENGINE_UNSUPPORTED | filtered/nested cardinality and correlation over repeated names and addresses, including “second instance” semantics. Do not use ordinal selection.
- REQ26 | ENGINE_UNSUPPORTED | TrademarkKindCode **or** TrademarkKindName must be in the normative set; it must not become AND.
- REQ30 | ENGINE_UNSUPPORTED | conditional cross-collection correlation: application document kind/name plus an AS successor party requires at least one AccompanyingDocumentsDetails with another required document kind/name. This needs correlation/filtering across distinct collections and code-or-name semantics.

## STRUCTURE_PATHS

- `{ipcdo}TrademarkApplicationDetails`: structural `1..*` root collection, narrowed by REQ1 to one; direct `{ipsdo}IPDocKindCode` and `IPDocKindName` are each `0..1`.
- Application status: `TrademarkApplicationDetails/{ipcdo}IPEntityStatusDetails` `0..1`; its `{csdo}StatusCode` `1..1`, `StatusCode/@codeListId` is an attribute `0..1`, and EventDate/DocId/IPDocReceiptDate are `0..1`; DescriptionText is `0..*`.
- Resource status is a distinct root `{ccdo}ResourceItemStatusDetails` `1..1`, with optional ValidityPeriodDetails and `{csdo}EndDateTime` `0..1`.
- Signature paths are application/`{ipcdo}SignatureDetails` `0..*`, with direct `{ipcdo}OfficerDetails` and direct `{ccdo}FullNameDetails` sibling collections. Officer FullNameDetails owns LastName/FirstName; PositionName is direct OfficerDetails child.
- REQ30’s non-executable paths are application direct IPDocKindCode/Name, application/IPPartyDetails/IPPartyKindCode, and application/AccompanyingDocumentsDetails/IPDocKindCode/Name. They must retain their distinct owners.
- Exact QName plus complete ancestor path is required; local-name matching does not satisfy a rule.

## ROLE_DISCRIMINATORS

Not applicable. Table 63 requires exactly one TrademarkApplicationDetails and contains no prior/new/first/second semantic application role. No positional mapping is authorized or needed.

## REPEATABLE_NOTES

Apply ordinary repeatable rules per structural parent: good+good passes; bad+good and good+bad fail when that collection is selected. REQ27 and REQ33–35 require same-parent evaluation. There is no repeated-application semantic-role test.

## COLLISION_RISKS

- Direct versus nested IPDocKindCode/Name, including IPEntityStatusDetails and AccompanyingDocumentsDetails.
- Application TrademarkApplicationId versus same local name under GoodsBaseDetails.
- Application entity status versus root ResourceItemStatusDetails.
- Status `codeListId` is an attribute, not an element.
- Direct signature OfficerDetails/FullNameDetails versus nested officer name and stakeholder officer paths.
- QName/namespace or owner mismatch must not satisfy any rule.

## TEST_MATRIX

Writer should add only:

- Valid MSG045 production E2E: build → serialize → parse → production extract → validate.
- One negative proof per FULL requirement, including resource EndDateTime, status code/attribute, and all required status descendants.
- Same-parent signature negatives for REQ33–35 and same-TrademarkDetails trigger/required-field negatives for REQ27.
- QName/owner collision tests only for direct/nested document kinds, status owners, identifiers, and signature names.
- Per-parent repeatable tests for structurally selectable collections; no positional application test.
- MSG045 isolation from other messages.

## IMPLEMENTATION_NOTES

Implement only the 24 FULL requirements. Retain REQ2/4/5 as external and REQ13/16–20/26/30 as non-executable with the stated reasons. Do not add classifier/resource lookup, ordinal roles, cross-collection correlation, or replacement AND logic for normative OR.

## READY_FOR_IMPLEMENTATION

YES. The executable subset is normatively confirmed and its non-executable boundaries are explicit.

