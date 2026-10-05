# MSG039 implementation preparation

## STATUS

COMPLETE. Preparation was read-only; no production or test file changed.

## NORMATIVE_CONTEXT

- **Message:** `P.SP.02.MSG.039` — «уведомление о прекращении
  делопроизводства по заявке на ТЗ Союза».
- **Transaction:** `P.SP.02.TRN.034`; `P.SP.02.PRC.015`; request/response.
- **Operations / actors:** `P.SP.02.OPR.061` / `P.SP.02.ACT.001` (ведомство
  подачи) → `P.SP.02.OPR.062` / `P.SP.02.ACT.002` (национальное патентное
  ведомство). Response: `P.SP.02.MSG.002`.
- **Structure:** `R.IP.SP.02.002`, version `1.0.0`.
- **PDF reread:** Table 57, physical pp. 757–759; Table 44 inheritance REQ6–29
  reread on pp. 715–721; transaction context pp. 662–663.

## INVENTORY

`CAPTURED_ROWS = 8`: 1, 2, 3, 4, 5, 6–29, 30, 31.

`EXPANDED_REQUIREMENTS = 31`; `REQ_LIST = 1–31`. Each REQ6–29 has dual
provenance: Table 57 inheritance plus identically numbered Table 44 row.

## CLASSIFICATION

- **FULLY_MAPPABLE (21):** 1, 5–12, 14–15, 21–25, 27–31.
- **SAFE_PARTIAL (1):** 4.
- **EXTERNAL (2):** 2–3.
- **AMBIGUOUS (1):** 13.
- **ENGINE_UNSUPPORTED (6):** 16–20, 26.
- **SOURCE_CONFLICT (0).**

Arithmetic: `21 + 1 + 2 + 1 + 6 = 31`.

## EXECUTABLE_RULES

| REQ | Class | Owner/path | Rule semantics |
|---|---|---|---|
| 1 | FULL | root / `ipcdo:TrademarkApplicationDetails` | exact selection cardinality `1..1` |
| 5 | FULL | `TrademarkApplicationDetails/IPEntityStatusDetails` | `StatusCode == "21"`; same `StatusCode/@codeListId` forbidden |
| 6 | FULL | each `TrademarkApplicationDetails` | `ApplicationReceiptDate` required |
| 7 | FULL | each populated application `UnifiedCountryCode` | `@codeListId == "ВОИС ST.3"` |
| 8 | FULL | each application `SubjectAddressDetails` | five child fields required |
| 9–10 | FULL | each application `CommunicationDetails` | fields required/name forbidden; code in `{TE,EM,FX}` |
| 11–12 | FULL | each `PatentAuthorityDetails` / same address | country required; authority name and address required, kind `== "2"` |
| 14–15 | FULL | `IPPartyDetails` filtered by same-parent `IPPartyKindCode == "AP"` | exactly one AP; required AP fields |
| 21–22 | FULL | each same filtered PA / RE party | respective required fields |
| 23–25 | FULL | correspondence-address and same `TrademarkDetails` owners | address kind/country; required trademark fields |
| 27–29 | FULL | same `TrademarkDetails`; application goods | same-parent image/colour conditional; indicator set; goods and child fields |
| 30 | FULL | root `ResourceItemStatusDetails` | `ValidityPeriodDetails/StartDateTime` required |
| 31 | FULL | same resource status | `ValidityPeriodDetails/EndDateTime` required |

## PARTIAL_RULES

`REQ4 | SAFE_PARTIAL | each TrademarkApplicationDetails/ipsdo:TrademarkApplicationId | required`.

**SAFE_FRAGMENT:** local application identifier presence.

**UNMAPPED_REMAINDER:** national-patent-office resource record, status `01|02`,
external absent end date, and cross-resource identifier equality.

## UNMAPPED_RULES

- `REQ2–3 | EXTERNAL`: branch selection relies completely on a document-kind
  classifier. Do not synthesize a classifier predicate or unconditional
  code/name rule.
- `REQ13 | AMBIGUOUS`: no second owner/instance invariant is explicit beyond
  REQ14’s AP selection.
- `REQ16–20 | ENGINE_UNSUPPORTED`: AP-conditioned language/name ordinal and
  cross-instance semantics cannot be expressed exactly.
- `REQ26 | ENGINE_UNSUPPORTED`: classifier correspondence by code **OR** name;
  never convert OR to AND.

## STRUCTURE_PATHS

- Root `ipcdo:TrademarkApplicationDetails` is schema `1..*`, QName
  `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}TrademarkApplicationDetails`; Table
  57 narrows it to exactly one.
- `IPDocKindCode`, `IPDocKindName`, and `TrademarkApplicationId` are direct
  `ipsdo` children; code/name are optional in the schema, identifier is `1..1`.
- `.../ipcdo:IPEntityStatusDetails` is an optional direct application child;
  its `csdo:StatusCode` is `1..1`, and `codeListId` is that exact element’s
  attribute. A status value from another owner cannot satisfy REQ5.
- Root `ccdo:ResourceItemStatusDetails` is `1..1`, but its validity period and
  Start/End children are schema-optional. Table 57 makes both dates required.
  Namespaces: `ccdo = urn:EEC:M:ComplexDataObjects:vX.X.X`,
  `csdo = urn:EEC:M:SimpleDataObjects:vX.X.X`.
- Inherited paths retain their Table 44 owner. REQ27 condition and required
  picture/colour are in the same `TrademarkDetails` instance.

## REPEATABLE_NOTES

- `TrademarkApplicationDetails` is schema-repeatable but REQ1 fixes one; use
  cardinality, never scalar broadcast.
- REQ8–12, 15, 21–25 and 27–29 operate per existing selected owner. Preserve
  sparse alignment across repeated parties, addresses, communications,
  trademarks and goods.
- For REQ15, 21, 22, 25, 27 and 29 require `good+good → PASS`,
  `bad+good → FAIL`, `good+bad → FAIL`. REQ27 additionally needs same-parent
  code/name condition proof. Test exact-QName/owner collisions for status,
  address and communication fields.

## TEST_MATRIX

1. Valid production E2E: build → serialize → parse → production extract →
   validate; every mapped rule passes.
2. One negative proof per FULL requirement; REQ4 tests only a missing local
   identifier. Do not fabricate classifier scenarios for REQ2–3.
3. Per-parent sparse-alignment and same-parent tests only for repeatable rules
   named above; wrong-owner/wrong-namespace collisions for REQ5 and inherited
   nested selectors.
4. Message isolation: Table 57 rule IDs must not evaluate for another message
   using `R.IP.SP.02.002`.

## IMPLEMENTATION_NOTES

Writer should produce eight captured rows and 31 expanded entries, preserve
Table 57/Table 44 dual provenance for REQ6–29, and emit no executable rule for
EXTERNAL, AMBIGUOUS, or ENGINE_UNSUPPORTED entries. Table 57 differs from
MSG037 in the exact local status (`21`, not `31`) and nevertheless requires
`EndDateTime`.

## READY_FOR_IMPLEMENTATION

YES
