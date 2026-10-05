# MSG044 implementation preparation

## STATUS

COMPLETE. This is a read-only implementation specification. The local PDF was read with PDFKit; no production or test file was changed and no tests were run.

## NORMATIVE_CONTEXT

PDF-confirmed: **P.SP.02.MSG.044** — «Сведения о признании заявки на ТЗ Союза отозванной по ходатайству заявителя»; structure **R.IP.SP.02.002 v1.0.0**; Table **62**, physical PDF pages **770–772**. Table 62 has one `ipcdo:TrademarkApplicationDetails`.

Transaction context is **P.SP.02.TRN.039**, procedure **P.SP.02.PRC.021**, request/response, **OPR096 → OPR097**, **ACT001 → ACT002**, request MSG044 and response **P.SP.02.MSG.002**. The PDF checkpoint is confirmed. Table 62 inherits REQ6–29 from **Table 44** with identical numbering; the source rows are on physical PDF pages **715–721**.

## INVENTORY

`CAPTURED_ROWS = 11`: 1–5, 6–29, 30–34.

`EXPANDED_REQUIREMENTS = 34`; `REQ_LIST = 1–34`.

REQ6–29 each have dual provenance: Table 62 REQ6–29 plus the identically numbered Table 44 row. Table 62 applies them to its single application instance; there is no role-specific repeated-application qualification.

## CLASSIFICATION

| Class | Requirements | Count |
|---|---|---:|
| FULLY_MAPPABLE | 1, 5–12, 14–15, 21–25, 27–30, 33–34 | 24 |
| SAFE_PARTIAL | — | 0 |
| EXTERNAL | 2–4 | 3 |
| AMBIGUOUS | 13 | 1 |
| ENGINE_UNSUPPORTED | 16–20, 26 | 6 |
| SOURCE_CONFLICT | — | 0 |

Arithmetic: **24 + 0 + 3 + 1 + 6 + 0 = 34**.

## EXECUTABLE_RULES

All paths below belong to the R.IP.SP.02.002 namespace set: `ipcdo={urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}`, `ipsdo={urn:EEC:M:IP:SimpleDataObjects:vZ.Z.Z}`, `ccdo={urn:EEC:M:ComplexDataObjects:vX.X.X}`, `csdo={urn:EEC:M:SimpleDataObjects:vX.X.X}`.

- REQ1 | FULLY_MAPPABLE | root `{ipcdo}TrademarkApplicationDetails` | exact cardinality **1..1**.
- REQ5 | FULLY_MAPPABLE | application/`{ipcdo}IPEntityStatusDetails` | required; same-owner `{csdo}StatusCode = "30"`; its `@codeListId` forbidden; `{csdo}EventDate` required.
- REQ6–12 | FULLY_MAPPABLE | Table 44, per single application and its exact descendants | receipt date required; any present country-code has `@codeListId="ВОИС ST.3"`; address and communication completeness/forbidden-name rules; PatentAuthority country and authority/address rules.
- REQ14–15 | FULLY_MAPPABLE | application/`{ipcdo}IPPartyDetails` filtered by same-parent `{ipsdo}IPPartyKindCode="AP"` | exactly one AP and required AP fields.
- REQ21–22 | FULLY_MAPPABLE | same `IPPartyDetails`, filtered respectively by `PA` and `RE` | required fields are checked in that same party.
- REQ23–25 | FULLY_MAPPABLE | application correspondence address and `{ipcdo}TrademarkDetails` | fixed address kind/country set; required trademark container and prescribed children.
- REQ27 | FULLY_MAPPABLE | same `TrademarkDetails` | if KindCode **or** KindName is one of 140/150/160/170/180, its `TrademarkPicture` and `TrademarkColourName` are required. **SAME_PARENT_REQUIRED**.
- REQ28–29 | FULLY_MAPPABLE | same trademark/application | CollectiveMarkIndicator is `"0"` or `"1"`; every GoodsBaseDetails has the listed three required fields.
- REQ30 | FULLY_MAPPABLE | application/`{ipcdo}SignatureDetails` | at least one signature; if its direct `OfficerDetails` is present, direct sibling `ccdo:FullNameDetails` is forbidden. **SAME_PARENT_REQUIRED**.
- REQ31 | FULLY_MAPPABLE | same `SignatureDetails` | direct FullNameDetails present implies direct OfficerDetails forbidden. **SAME_PARENT_REQUIRED**.
- REQ32 | FULLY_MAPPABLE | same signature/`OfficerDetails` | Officer implies its FullNameDetails/LastName/FirstName and PositionName required, its CommunicationDetails forbidden. These are the direct signature officer paths, not stakeholder officers. **SAME_PARENT_REQUIRED**.
- REQ33 | FULLY_MAPPABLE | `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime` | required.
- REQ34 | FULLY_MAPPABLE | same status/validity owner | `csdo:EndDateTime` required.

## PARTIAL_RULES

None. Classifier/resource-dependent requirements are retained as EXTERNAL rather than treating a proxy condition as the normative classifier result.

## UNMAPPED_RULES

- REQ2–3 | EXTERNAL | classifier lookup determines whether the code path or exact fallback literal is required; lookup is not simulated.
- REQ4 | EXTERNAL | TrademarkApplicationId presence is structural, but the normative rule also requires a matching active external patent-office resource with StatusCode 01 or 02 and no EndDateTime. The whole requirement remains external.
- REQ13 | AMBIGUOUS | Table 44 says IPPartyKindCode must be AP without an explicit instance scope, while REQ21–22 expressly recognize PA and RE instances. Do not turn the sentence into a global AP-only assertion.
- REQ16–20 | ENGINE_UNSUPPORTED | filtered/nested cardinality and correlation over repeated IPSubjectName/address structures, including the “second instance” semantics; no ordinal or cross-collection simulation.
- REQ26 | ENGINE_UNSUPPORTED | Code **OR** Name belongs to the prescribed trademark-kind set. It must not be implemented as AND.

## STRUCTURE_PATHS

- `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}TrademarkApplicationDetails`: 1..*, root repeated structural owner; MSG044 REQ1 narrows it to one.
- Direct application children: `{ipsdo}IPDocKindCode` and `{ipsdo}IPDocKindName` (each 0..1), `{ipsdo}TrademarkApplicationId` (1..1), `{ipcdo}IPEntityStatusDetails` (0..1), and `{ipcdo}SignatureDetails` (0..*).
- Status owner: `IPEntityStatusDetails/{csdo}StatusCode` (1..1), `StatusCode/@codeListId` (attribute, 0..1), and `{csdo}EventDate` (0..1).
- Signature owner: `SignatureDetails/{ipcdo}OfficerDetails` and direct `SignatureDetails/{ccdo}FullNameDetails` are distinct sibling collections. Officer FullNameDetails contains LastName/FirstName; PositionName is a direct OfficerDetails child.
- Resource status is a separate root owner: `{ccdo}ResourceItemStatusDetails` (1..1) / `ValidityPeriodDetails` (0..1) / StartDateTime and EndDateTime (both 0..1). Required Table 62 values require container creation only when their descendants exist.
- QName and full ancestor paths are required; local-name matching is insufficient.

## ROLE_DISCRIMINATORS

Not applicable to MSG044. PDF Table 62 requires exactly **one** TrademarkApplicationDetails, and it contains no “prior/new/first/second” application role. No structural role discriminator is needed or sought. This differs from MSG043.

## REPEATABLE_NOTES

Ordinary repeated descendants use their structural parent context. Per-parent negative proofs apply where a selector iterates such a collection. No positional repeated-application rule is authorized. For REQ27 and REQ30–32, evaluation must remain inside the same TrademarkDetails or SignatureDetails parent respectively.

## COLLISION_RISKS

- Direct `IPDocKindCode` versus same-named nested status/accompanying-document fields.
- Direct application `TrademarkApplicationId` versus GoodsBaseDetails child of the same local name.
- `codeListId` is an attribute of StatusCode.
- Direct SignatureDetails FullNameDetails versus OfficerDetails/FullNameDetails and stakeholder officer paths.
- Separate root ResourceItemStatusDetails must not be confused with application status.
- QName/namespace and ancestor ownership must be exact.

## TEST_MATRIX

Writer should add only these tests:

- Valid MSG044 production E2E: build → serialize → parse → production extract → validate.
- Negative proof for each FULL rule, including exact cardinality, status code/attribute/event date, required/forbidden resource dates, and signature same-parent branches.
- Table 44 FULL rules: per-owner presence/fixed-set tests; REQ27 both trigger alternatives with picture/colour absence under the same TrademarkDetails.
- QName/owner collision tests for direct versus nested IPDocKindCode, TrademarkApplicationId, and signature/officer name paths.
- Repeatable tests only for structurally selectable descendants; no first/second application test.
- Message-isolation regression for MSG044.

## IMPLEMENTATION_NOTES

Use only the 24 FULL requirements. Preserve REQ2–4 as external and surface REQ13/16–20/26 as unmapped with their classifications. Do not introduce classifier access, external-resource access, ordinal logic, or cross-collection correlation. Table 62 confirms `EndDateTime` is **required** for MSG044 REQ34; do not copy MSG043's forbidden-date behavior.

## READY_FOR_IMPLEMENTATION

YES. A writer can implement the conservative executable subset while preserving the listed non-executable requirements and their reasons.

