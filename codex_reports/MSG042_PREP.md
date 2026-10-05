# MSG042 implementation preparation

## STATUS

COMPLETE. The prior checkpoint was independently confirmed from the PDF; no
production or test file changed.

## NORMATIVE_CONTEXT

- **Message:** `P.SP.02.MSG.042` — «сведения о преобразовании заявки на ТЗ
  Союза в заявку на коллективный знак Союза».
- **Transaction:** `P.SP.02.TRN.037`; `P.SP.02.PRC.019`; request/response.
- **Operations / actors:** `P.SP.02.OPR.080` / `P.SP.02.ACT.001` (ведомство
  подачи) → `P.SP.02.OPR.081` / `P.SP.02.ACT.002` (национальное патентное
  ведомство). Response: `P.SP.02.MSG.002`.
- **Structure:** `R.IP.SP.02.002`, version `1.0.0`.
- **PDF reread:** Table 60, physical pp. 764–766; Table 44 inheritance REQ6–29
  reread on pp. 715–721. No checkpoint discrepancy found.

## INVENTORY

`CAPTURED_ROWS = 12`: 1–5, 6–29, 30–35.

`EXPANDED_REQUIREMENTS = 35`; `REQ_LIST = 1–35`. Table 60 explicitly inherits
Table 44 REQ6–29 with matching numbering, so each carries dual provenance.

## CLASSIFICATION

- **FULLY_MAPPABLE (25):** 1, 5–12, 14–15, 21–25, 27–35.
- **SAFE_PARTIAL (1):** 4.
- **EXTERNAL (2):** 2–3.
- **AMBIGUOUS (1):** 13.
- **ENGINE_UNSUPPORTED (6):** 16–20, 26.
- **SOURCE_CONFLICT (0).**

Arithmetic: `25 + 1 + 2 + 1 + 6 = 35`.

## EXECUTABLE_RULES

| REQ | Class | Owner/path | Rule semantics |
|---|---|---|---|
| 1 | FULL | root / `ipcdo:TrademarkApplicationDetails` | exact selection cardinality `1..1` |
| 5 | FULL | each direct `.../ipcdo:IPEntityStatusDetails` | container required; same `StatusCode == "02"`; its `@codeListId` forbidden |
| 6–12 | FULL | inherited Table 44 application owners | receipt date; country list ID; address/communication/authority requirements |
| 14–15 | FULL | `IPPartyDetails` filtered by same-parent `IPPartyKindCode == "AP"` | exactly one AP; required AP fields |
| 21–22 | FULL | each same filtered PA / RE party | respective required fields |
| 23–25 | FULL | correspondence-address and same `TrademarkDetails` owners | address kind/country; required trademark fields |
| 27–29 | FULL | same `TrademarkDetails`; application goods | same-parent image/colour conditional; indicator set; goods and child fields |
| 30 | FULL | same `TrademarkDetails/ipsdo:CollectiveMarkIndicator` | fixed value `"1"` |
| 31 | FULL | root `ccdo:ResourceItemStatusDetails` | `ValidityPeriodDetails/StartDateTime` required |
| 32 | FULL | same resource status | `ValidityPeriodDetails/EndDateTime` forbidden |
| 33 | FULL | each direct application `SignatureDetails` | at least one; if same-signature `OfficerDetails` exists, direct `FullNameDetails` forbidden |
| 34 | FULL | same signature | if direct `FullNameDetails` exists, direct `OfficerDetails` forbidden |
| 35 | FULL | each `OfficerDetails` directly under same signature | last name, first name, position required; officer communication forbidden |

## PARTIAL_RULES

`REQ4 | SAFE_PARTIAL | each TrademarkApplicationDetails/ipsdo:TrademarkApplicationId | required`.

**SAFE_FRAGMENT:** local application identifier presence.

**UNMAPPED_REMAINDER:** national-patent-office resource record, status `01|02`,
external absent end date, and cross-resource identifier equality.

## UNMAPPED_RULES

- `REQ2–3 | EXTERNAL`: the document-kind classifier selects the branch and
  supplies the code/name semantics. Do not simulate it or make a branch
  unconditional.
- `REQ13 | AMBIGUOUS`: no additional owner/instance invariant is explicit
  beyond REQ14’s AP selection.
- `REQ16–20 | ENGINE_UNSUPPORTED`: AP-conditioned name language/ordinal and
  cross-instance semantics cannot be stated exactly by the evaluator.
- `REQ26 | ENGINE_UNSUPPORTED`: classifier correspondence is code **OR** name;
  never alter this to AND.

## STRUCTURE_PATHS

- Root `ipcdo:TrademarkApplicationDetails` is schema `1..*`, QName
  `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}TrademarkApplicationDetails`; Table
  60 narrows it to one.
- Direct `.../ipcdo:IPEntityStatusDetails` is `0..1`; its exact nested
  `csdo:StatusCode` is `1..1`, and `codeListId` is that element’s attribute.
  A status from another owner cannot satisfy REQ5.
- `.../ipcdo:TrademarkDetails/ipsdo:CollectiveMarkIndicator` is `1..1` in the
  same trademark owner; REQ30 fixes it to `1`.
- Direct `SignatureDetails` is `0..*`; direct signature `FullNameDetails` and
  `OfficerDetails` define REQ33–35. Stakeholder-owned officers/full names are
  distinct paths.
- Root `ccdo:ResourceItemStatusDetails` is `1..1`; validity dates are
  schema-optional. Table 60 makes Start required and End forbidden.
  `ccdo = urn:EEC:M:ComplexDataObjects:vX.X.X`; `csdo =
  urn:EEC:M:SimpleDataObjects:vX.X.X`.

## REPEATABLE_NOTES

- REQ33–35 use repeatable signatures/officers and require
  `good+good → PASS`, `bad+good → FAIL`, `good+bad → FAIL`, with
  **SAME_PARENT_REQUIRED**.
- REQ8–12, 15, 21–25 and 27–29 remain per selected owner; preserve sparse
  alignment. REQ27’s trigger and picture/colour fields belong to the same
  `TrademarkDetails` parent.

## COLLISION_RISKS

- `StatusCode`/`codeListId`: required nested status owner and attribute, not a
  same-local-name element elsewhere.
- `CollectiveMarkIndicator`: direct child of the target trademark only.
- Signature direct `OfficerDetails`/`FullNameDetails` differ from stakeholder
  paths; repeated sibling leakage changes branch results.
- Wrong namespaces must not select any of the above paths.

## TEST_MATRIX

1. Valid production E2E: build → serialize → parse → production extract →
   validate, with every mapped rule passing.
2. One negative proof per FULL; REQ4 only tests missing local identifier. Do
   not fabricate classifier cases for REQ2–3.
3. Owner/QName collision tests for REQ5, REQ30 and REQ33–35; signature sparse
   alignment/same-parent matrix; same-parent REQ27 test.
4. Isolation proof with MSG041: `CollectiveMarkIndicator = 1` passes only
   MSG042 and `0` passes only MSG041; their Table IDs must remain isolated.

## IMPLEMENTATION_NOTES

Writer should record 12 captured rows and 35 expanded entries, preserve dual
Table 60/Table 44 provenance for REQ6–29, and emit no rule for EXTERNAL,
AMBIGUOUS or ENGINE_UNSUPPORTED entries. PDF confirms the reverse direction of
MSG041 and the critical non-shared literal: MSG042 requires indicator `1`,
whereas MSG041 requires `0`.

## READY_FOR_IMPLEMENTATION

YES
