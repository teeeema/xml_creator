# MSG037 implementation preparation

## STATUS

COMPLETE.  This is a read-only preparation; no production or test file was
changed.

## NORMATIVE_CONTEXT

- **Message:** `P.SP.02.MSG.037` — «сведения о признании заявки на ТЗ Союза
  отозванной по причине непоступления документа о согласии».
- **Transaction:** `P.SP.02.TRN.032`; `P.SP.02.PRC.013`; request/response.
- **Operations / actors:** `P.SP.02.OPR.050` / `P.SP.02.ACT.001` (ведомство
  подачи) → `P.SP.02.OPR.051` / `P.SP.02.ACT.002` (национальное патентное
  ведомство).  Response: `P.SP.02.MSG.002`.
- **Structure:** `R.IP.SP.02.002`, version `1.0.0`.
- **Normative source reread:** Table 55, physical pp. 752–754; inheritance is
  Table 44 REQ6–29 (physical pp. 715–721).  Transaction context is confirmed
  by the PDF on pp. 658–659.

## INVENTORY

`CAPTURED_ROWS = 8`: 1, 2, 3, 4, 5, 6–29, 30, 31.

`EXPANDED_REQUIREMENTS = 31`.

`REQ_LIST = 1–31`; REQ6–29 each have dual provenance: Table 55 inheritance
plus the identically numbered original Table 44 row.

## CLASSIFICATION

- **FULLY_MAPPABLE (21):** 1, 5, 6–12, 14–15, 21–25, 27–31.
- **SAFE_PARTIAL (1):** 4.
- **EXTERNAL (2):** 2–3.
- **AMBIGUOUS (1):** 13.
- **ENGINE_UNSUPPORTED (6):** 16–20, 26.
- **SOURCE_CONFLICT (0).**

The arithmetic is `21 + 1 + 2 + 1 + 6 = 31`.

## EXECUTABLE_RULES

| REQ | Class | Owner/path | Rule semantics |
|---|---|---|---|
| 1 | FULL | root / `ipcdo:TrademarkApplicationDetails` | exact selection cardinality `1..1` |
| 5 | FULL | `TrademarkApplicationDetails/IPEntityStatusDetails` | `StatusCode == "31"`; its local `@codeListId` forbidden |
| 6 | FULL | each `TrademarkApplicationDetails` | `ApplicationReceiptDate` required |
| 7 | FULL | each populated `csdo:UnifiedCountryCode` under application | `@codeListId == "ВОИС ST.3"` |
| 8 | FULL | each `ccdo:SubjectAddressDetails` under application | five child fields required |
| 9 | FULL | each `ccdo:CommunicationDetails` under application | two child fields required; `CommunicationChannelName` forbidden |
| 10 | FULL | same `CommunicationDetails` | `CommunicationChannelCode ∈ {TE, EM, FX}` |
| 11 | FULL | each `PatentAuthorityDetails` | `UnifiedCountryCode` required |
| 12 | FULL | same authority / same address | authority name and address required; address kind `== "2"` |
| 14 | FULL | application `IPPartyDetails` filtered by `IPPartyKindCode == "AP"` | exact cardinality `1..1` |
| 15 | FULL | each same filtered AP party | country, subject name, address, communication required |
| 21 | FULL | each PA party | country, subject name, address, communication, patent-attorney ID required |
| 22 | FULL | each RE party | country, subject name, address, communication required |
| 23 | FULL | each correspondence address | address kind `== "3"` |
| 24 | FULL | same correspondence address | country in `{AM,BY,KZ,KG,RU}` |
| 25 | FULL | each application trademark | at least one; description, kind code/name, collective indicator required |
| 27 | FULL | each same `TrademarkDetails` | if same-parent kind code **or** name is 140–180, picture and colour name required |
| 28 | FULL | each same `TrademarkDetails` | collective indicator in `{0,1}` |
| 29 | FULL | each application goods item | at least one; class code/name and goods name required |
| 30 | FULL | each root `ResourceItemStatusDetails` | `ValidityPeriodDetails/StartDateTime` required |
| 31 | FULL | same resource status | `ValidityPeriodDetails/EndDateTime` required |

## PARTIAL_RULES

`REQ4 | SAFE_PARTIAL | each TrademarkApplicationDetails/ipsdo:TrademarkApplicationId | required`.

**SAFE_FRAGMENT:** local application identifier presence.

**UNMAPPED_REMAINDER:** national patent-office resource record existence,
status `01|02`, absent external end time, and equality with the message
identifier.

## UNMAPPED_RULES

- `REQ2–3 | EXTERNAL`: both branches are selected solely by presence/absence
  of a classifier entry.  Do not turn either branch into an unconditional local
  code/name rule or simulate the classifier.
- `REQ13 | AMBIGUOUS`: Table 44 states the AP code requirement without a
  sufficiently explicit owner/instance scope for a second executable invariant
  beside REQ14’s exactly-one AP selection.
- `REQ16–20 | ENGINE_UNSUPPORTED`: AP-conditioned repeated-name ordinal and
  language/attribute correlation semantics require cross-instance or nested
  filtered cardinality that the evaluator cannot state exactly.
- `REQ26 | ENGINE_UNSUPPORTED`: same `TrademarkDetails` requires code **OR**
  name classifier correspondence.  Do not convert this OR to AND.

## STRUCTURE_PATHS

Use exact QNames, never local-name fallback:

- `ipcdo:TrademarkApplicationDetails` —
  `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}TrademarkApplicationDetails`, root,
  schema `1..*`; Table 55 narrows it to exactly one.
- `.../ipsdo:IPDocKindCode`, `.../ipsdo:IPDocKindName`,
  `.../ipsdo:TrademarkApplicationId` —
  `{urn:EEC:M:IP:SimpleDataObjects:vZ.Z.Z}`; direct application children.
- `.../ipcdo:IPEntityStatusDetails/csdo:StatusCode` — exact nested owner;
  `StatusCode` is `{urn:EEC:M:SimpleDataObjects:vX.X.X}StatusCode`; its
  `codeListId` is its attribute, not an element with the same local name.
- `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/{Start,End}DateTime`
  — root resource owner; `ccdo` namespace is
  `urn:EEC:M:ComplexDataObjects:vX.X.X`, `csdo` namespace is
  `urn:EEC:M:SimpleDataObjects:vX.X.X`.  Schema makes period and dates optional;
  REQ30–31 make both dates mandatory for this message.

Inherited paths must retain the Table 44 owners shown in the executable table;
in particular REQ27 is scoped to the same `TrademarkDetails` instance.

## REPEATABLE_NOTES

- `TrademarkApplicationDetails` is schema-repeatable but REQ1 fixes one;
  still use cardinality, never scalar broadcast.
- REQ8–12, 15, 21–25, and 27–29 operate per selected existing owner.  For
  repeatable `IPPartyDetails`, addresses, communications, trademarks and goods,
  preserve sparse positional alignment and same-parent filtering.
- REQ27 needs `good+good → PASS`, `bad+good → FAIL`, and `good+bad → FAIL`.
  The same matrix is useful for REQ15, 21, 22, 25 and 29 where their selected
  collection is repeated.  Test exact QName/owner collisions for nested status,
  address and communication fields.

## TEST_MATRIX

1. Valid production path: build → serialize → parse → production extract →
   validate; verify every mapped rule passes.
2. One negative test per FULL rule; REQ2–3 receive no fabricated classifier
   tests, and REQ4 tests only missing local identifier.
3. Owner/QName collision negatives for REQ5 status and for inherited nested
   address/communication selectors.
4. Per-parent sparse-alignment tests only for the repeatable rules named above;
   include REQ27 same-parent branches.
5. Message-isolation test: MSG037 rules and source IDs must not execute for
   another `R.IP.SP.02.002` message.

## IMPLEMENTATION_NOTES

Writer should create a Table 55 mapping audit with eight captured rows and 31
expanded entries, dual Table 55/Table 44 provenance for REQ6–29, and no rule
object for EXTERNAL, AMBIGUOUS, or ENGINE_UNSUPPORTED entries.  REQ31 is
**required**, unlike neighbouring messages whose table may forbid end time.

## READY_FOR_IMPLEMENTATION

YES
