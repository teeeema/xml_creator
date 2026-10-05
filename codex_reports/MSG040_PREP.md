# MSG040 implementation preparation

## STATUS

COMPLETE. Preparation was read-only; no production or test file changed.

## NORMATIVE_CONTEXT

- **Message:** `P.SP.02.MSG.040` — «ходатайство о преобразовании заявки на ТЗ
  Союза в национальную заявку на регистрацию ТЗ».
- **Transaction:** `P.SP.02.TRN.035`; `P.SP.02.PRC.016`; request/response.
- **Operations / actors:** `P.SP.02.OPR.064` / `P.SP.02.ACT.001` (ведомство
  подачи) → `P.SP.02.OPR.065` / `P.SP.02.ACT.002` (национальное патентное
  ведомство). Response: `P.SP.02.MSG.002`.
- **Structure:** `R.IP.SP.02.002`, version `1.0.0`.
- **PDF reread:** Table 58, physical pp. 759–761; Table 44 inheritance REQ6–29
  reread on pp. 715–721; transaction context p. 665.

## INVENTORY

`CAPTURED_ROWS = 11`: 1–5, 6–29, 30–34.

`EXPANDED_REQUIREMENTS = 34`; `REQ_LIST = 1–34`. Each REQ6–29 has dual
provenance: Table 58 inheritance plus identically numbered Table 44 row.

## CLASSIFICATION

- **FULLY_MAPPABLE (24):** 1, 5–12, 14–15, 21–25, 27–34.
- **SAFE_PARTIAL (1):** 4.
- **EXTERNAL (2):** 2–3.
- **AMBIGUOUS (1):** 13.
- **ENGINE_UNSUPPORTED (6):** 16–20, 26.
- **SOURCE_CONFLICT (0).**

Arithmetic: `24 + 1 + 2 + 1 + 6 = 34`.

## EXECUTABLE_RULES

| REQ | Class | Owner/path | Rule semantics |
|---|---|---|---|
| 1 | FULL | root / `ipcdo:TrademarkApplicationDetails` | exact selection cardinality `1..1` |
| 5 | FULL | each direct `.../ipcdo:IPEntityStatusDetails` | container required; same `StatusCode == "30"`; its `@codeListId` forbidden |
| 6–12 | FULL | inherited Table 44 application owners | receipt date; country list ID; address/communication/authority requirements |
| 14–15 | FULL | `IPPartyDetails` filtered by same-parent `IPPartyKindCode == "AP"` | exactly one AP; required AP fields |
| 21–22 | FULL | each same filtered PA / RE party | respective required fields |
| 23–25 | FULL | correspondence-address and same `TrademarkDetails` owners | address kind/country; required trademark fields |
| 27–29 | FULL | same `TrademarkDetails`; application goods | same-parent image/colour conditional; indicator set; goods and child fields |
| 30 | FULL | each direct application `SignatureDetails` | at least one; if same-signature `OfficerDetails` exists, direct `FullNameDetails` forbidden |
| 31 | FULL | same signature | if direct `FullNameDetails` exists, direct `OfficerDetails` forbidden |
| 32 | FULL | each `OfficerDetails` directly under same signature | last name, first name, position required; officer communication forbidden |
| 33 | FULL | root `ccdo:ResourceItemStatusDetails` | `ValidityPeriodDetails/StartDateTime` required |
| 34 | FULL | same resource status | `ValidityPeriodDetails/EndDateTime` required |

## PARTIAL_RULES

`REQ4 | SAFE_PARTIAL | each TrademarkApplicationDetails/ipsdo:TrademarkApplicationId | required`.

**SAFE_FRAGMENT:** local application identifier presence.

**UNMAPPED_REMAINDER:** national-patent-office resource record, status `01|02`,
external absent end date, and cross-resource identifier equality.

## UNMAPPED_RULES

- `REQ2–3 | EXTERNAL`: branch choice and exact document-kind code/name depend
  on the classifier. Do not make either branch an unconditional local rule.
- `REQ13 | AMBIGUOUS`: no additional owner/instance invariant is explicit beyond
  REQ14’s AP selection.
- `REQ16–20 | ENGINE_UNSUPPORTED`: AP-conditioned language/name ordinal and
  cross-instance correlations are not expressible exactly.
- `REQ26 | ENGINE_UNSUPPORTED`: classifier correspondence uses code **OR** name;
  never change the disjunction to AND.

## STRUCTURE_PATHS

- Root `ipcdo:TrademarkApplicationDetails` is schema `1..*`, QName
  `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}TrademarkApplicationDetails`; Table
  58 restricts it to one.
- Direct `.../ipcdo:IPEntityStatusDetails` is schema `0..1`; its exact nested
  `csdo:StatusCode` is `1..1` and `codeListId` is that element’s attribute.
  REQ5 must require the container itself, not merely find a similarly named
  status under another owner.
- Direct signature owner is `.../ipcdo:SignatureDetails (0..*)`; its direct
  `ccdo:FullNameDetails (0..*)` and `ipcdo:OfficerDetails (0..*)` define
  REQ30–32. Stakeholder officers are a distinct path and must not satisfy them.
- Root `ccdo:ResourceItemStatusDetails` is `1..1`; validity period and both
  date fields are schema-optional. Table 58 makes Start and End required.
  `ccdo = urn:EEC:M:ComplexDataObjects:vX.X.X`; `csdo =
  urn:EEC:M:SimpleDataObjects:vX.X.X`.
- Inherited selectors retain Table 44 ownership; REQ27 condition and required
  fields are within the same `TrademarkDetails` instance.

## REPEATABLE_NOTES

- Signature and officer paths are repeatable. For REQ30–32 test
  `good+good → PASS`, `bad+good → FAIL`, `good+bad → FAIL`; branches must stay
  in the same `SignatureDetails` parent.
- REQ8–12, 15, 21–25 and 27–29 are per existing selected owners. Preserve
  sparse positional alignment across parties, addresses, communications,
  trademarks and goods. REQ27 requires same-parent code/name proof.
- Add wrong-owner and wrong-namespace collision cases for status and signature
  paths; unrelated officer/full-name elements must not satisfy a rule.

## TEST_MATRIX

1. Valid production E2E: build → serialize → parse → production extract →
   validate, with all mapped rules passing.
2. One negative proof per FULL; REQ4 tests only missing local identifier. Do
   not fabricate classifier tests for REQ2–3.
3. Same-signature and sparse repeatable matrices for REQ30–32; same-parent
   branch test for REQ27; owner/QName collision tests for REQ5 and signatures.
4. Message isolation: Table 58 IDs must not execute for another message sharing
   `R.IP.SP.02.002`.

## IMPLEMENTATION_NOTES

Writer should record 11 captured rows and 34 expanded entries, preserve dual
Table 58/Table 44 provenance for REQ6–29, and emit no executable rule for
EXTERNAL, AMBIGUOUS, or ENGINE_UNSUPPORTED entries. Table 58 specifically
requires status container/value `30`, direct signature rules, and both validity
dates; do not inherit these direct rules from another message.

## READY_FOR_IMPLEMENTATION

YES
