# MSG038 implementation preparation

## STATUS

COMPLETE.  Preparation was read-only; no production or test file changed.

## NORMATIVE_CONTEXT

- **Message:** `P.SP.02.MSG.038` — «сведения о документах, подтверждающих
  испрашиваемый приоритет ТЗ Союза».
- **Transaction:** `P.SP.02.TRN.033`; `P.SP.02.PRC.014`; request/response.
- **Operations / actors:** `P.SP.02.OPR.054` / `P.SP.02.ACT.001` (ведомство
  подачи) → `P.SP.02.OPR.055` / `P.SP.02.ACT.002` (национальное патентное
  ведомство). Response: `P.SP.02.MSG.002`.
- **Structure:** `R.IP.SP.02.002`, version `1.0.0`.
- **PDF reread:** Table 56, physical pp. 754–756; Table 44 inheritance REQ6–29
  reread on pp. 715–721; transaction pp. 660–661.

## INVENTORY

`CAPTURED_ROWS = 14`: 1–5, 6–29, 30–37.

`EXPANDED_REQUIREMENTS = 37`; `REQ_LIST = 1–37`.  Each REQ6–29 has dual
provenance: Table 56 inheritance plus identically numbered Table 44 row.

## CLASSIFICATION

- **FULLY_MAPPABLE (26):** 1, 5–12, 14–15, 21–25, 27–30, 32–37.
- **SAFE_PARTIAL (1):** 4.
- **EXTERNAL (3):** 2–3, 31.
- **AMBIGUOUS (1):** 13.
- **ENGINE_UNSUPPORTED (6):** 16–20, 26.
- **SOURCE_CONFLICT (0).**

Arithmetic: `26 + 1 + 3 + 1 + 6 = 37`.

## EXECUTABLE_RULES

| REQ | Class | Owner/path | Rule semantics |
|---|---|---|---|
| 1 | FULL | root / `ipcdo:TrademarkApplicationDetails` | exact selection cardinality `1..1` |
| 5 | FULL | each `TrademarkApplicationDetails/TrademarkPriorityDetails` | at least one priority |
| 6–12 | FULL | inherited Table 44 application owners | receipt date; country list ID; address/communication/authority requirements |
| 14–15 | FULL | `IPPartyDetails` filtered by same-parent `IPPartyKindCode == "AP"` | exactly one AP; required AP fields |
| 21–22 | FULL | each same filtered PA / RE party | respective required fields |
| 23–25 | FULL | correspondence-address and same `TrademarkDetails` owners | address kind/country; required trademark fields |
| 27–29 | FULL | same `TrademarkDetails`; application goods | same-parent image/colour conditional; indicator set; goods and child fields |
| 30 | FULL | each `TrademarkPriorityDetails` | `PriorityKindCode`, `PriorityDate`, `UnifiedCountryCode` required |
| 32 | FULL | every exact-QName `ipcdo:AccompanyingDocumentsDetails` | if present, `DocName`, `DocId`, `DocCreationDate`, `DescriptionText`, `PageQuantity` required per document |
| 33 | FULL | root `ccdo:ResourceItemStatusDetails` | `ValidityPeriodDetails/StartDateTime` required |
| 34 | FULL | same resource status | `ValidityPeriodDetails/EndDateTime` forbidden |
| 35 | FULL | each direct application `SignatureDetails` | at least one signature; if same-signature direct `OfficerDetails` exists, direct `FullNameDetails` forbidden |
| 36 | FULL | same signature | if direct `FullNameDetails` exists, direct `OfficerDetails` forbidden |
| 37 | FULL | each `OfficerDetails` directly under same signature | last name, first name, position required; officer communication forbidden |

## PARTIAL_RULES

`REQ4 | SAFE_PARTIAL | each TrademarkApplicationDetails/ipsdo:TrademarkApplicationId | required`.

**SAFE_FRAGMENT:** local `TrademarkApplicationId` presence.

**UNMAPPED_REMAINDER:** national-patent-office resource record, status `01|02`,
external absent end date, and cross-resource identifier equality.

## UNMAPPED_RULES

- `REQ2–3 | EXTERNAL`: their branches depend wholly on the document-kind
  classifier. Do not create unconditional code/name rules or a synthetic
  classifier predicate.
- `REQ13 | AMBIGUOUS`: no second owner/instance invariant is sufficiently
  explicit beyond REQ14’s AP selection.
- `REQ16–20 | ENGINE_UNSUPPORTED`: AP-conditioned language/name ordinal and
  cross-instance correlations cannot be expressed exactly.
- `REQ26 | ENGINE_UNSUPPORTED`: classifier correspondence by code **OR** name;
  never convert OR to AND.
- `REQ31 | EXTERNAL`: priority-kind classifier lookup is not local evaluator
  data; do not hard-code an unconfirmed code set.

## STRUCTURE_PATHS

- `ipcdo:TrademarkApplicationDetails` is root-level, schema `1..*`, QName
  `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}TrademarkApplicationDetails`; REQ1
  narrows this to one.
- `.../ipcdo:TrademarkPriorityDetails` is `0..*`; its direct children are
  `ipsdo:PriorityKindCode (0..1)`, `ipsdo:PriorityDate (1..1)`, and
  `csdo:UnifiedCountryCode (0..1)`. REQ30 is per priority owner.
- Direct accompanying documents are `0..*`, but the same exact
  `ipcdo:AccompanyingDocumentsDetails` QName also occurs under proof text.
  REQ32 says “included in the electronic document”, so select every exact QName
  occurrence and check its own children, not one hard-coded ancestor path.
- Signature paths are direct application children:
  `.../ipcdo:SignatureDetails (0..*)`, its direct
  `ccdo:FullNameDetails (0..*)`, and direct `ipcdo:OfficerDetails (0..*)`.
  Stakeholder `OfficerDetails` is a different owner and must not satisfy REQ35–37.
- Root `ccdo:ResourceItemStatusDetails` is `1..1`; its validity container and
  Start/End dates are schema-optional. Table 56 makes start required and end
  forbidden. Namespaces: `ccdo = urn:EEC:M:ComplexDataObjects:vX.X.X`,
  `csdo = urn:EEC:M:SimpleDataObjects:vX.X.X`.

## REPEATABLE_NOTES

- REQ30 and REQ32 are per repeated priority/document. Require
  `good+good → PASS`, `bad+good → FAIL`, `good+bad → FAIL`, preserving sparse
  positional alignment.
- Apply the same matrix to repeated signatures/officers for REQ35–37. The
  condition is per **same SignatureDetails**; no value may leak to another
  signature.
- REQ27 is per same `TrademarkDetails`; test code/name condition and required
  picture/colour in that same parent. Exact-QName collision tests are needed for
  documents and signature officer/full-name paths.

## TEST_MATRIX

1. Valid production E2E: build → serialize → parse → production extract →
   validate, with all mapped rules passing.
2. One negative proof per FULL requirement; REQ4 only tests its local required
   fragment. No fabricated classifier tests for REQ2–3 or REQ31.
3. Repeated priority, document, signature and officer alignment matrices above;
   direct and nested `AccompanyingDocumentsDetails` must each be covered.
4. Same-signature branch tests for REQ35–37 and same-trademark branch tests for
   REQ27; wrong-owner and wrong-namespace collision cases.
5. Message isolation: Table 56 rule IDs must not evaluate for another message
   sharing `R.IP.SP.02.002`.

## IMPLEMENTATION_NOTES

Writer should record 14 captured rows and 37 expanded entries, use dual
Table 56/Table 44 source provenance for REQ6–29, and emit no executable rule
for EXTERNAL, AMBIGUOUS, or ENGINE_UNSUPPORTED rows.  Preserve the Table 56
distinctions: REQ34 forbids end time; REQ35–37 govern signature branches; and
REQ32 has five fields (no `DocBinaryText`).

## READY_FOR_IMPLEMENTATION

YES
