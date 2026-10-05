# MSG043 implementation preparation

## STATUS

COMPLETE. The PDF establishes an ordinal two-application message shape. No production or test file changed.

## NORMATIVE_CONTEXT

- **Message:** `P.SP.02.MSG.043` — «сведения о выделении заявки на ТЗ Союза из ранее поданной заявки на ТЗ Союза».
- **Transaction:** `P.SP.02.TRN.038`; `P.SP.02.PRC.020`; request/response.
- **Operations / actors:** `P.SP.02.OPR.088` / `P.SP.02.ACT.001` (ведомство подачи) → `P.SP.02.OPR.089` / `P.SP.02.ACT.002` (национальное патентное ведомство). Response: `P.SP.02.MSG.002`.
- **Structure:** `R.IP.SP.02.002`, version `1.0.0`.
- **PDF reread:** Table 61, physical pp. 767–770; Table 44 inheritance REQ6–29 reread on pp. 715–721. No checkpoint discrepancy found.

## INVENTORY

`CAPTURED_ROWS = 14`: 1–5, 6–29, 30–37.

`EXPANDED_REQUIREMENTS = 37`; `REQ_LIST = 1–37`. Table 61 inherits Table 44 REQ6–29 only for the **allocated application** (выделенная заявка), with matching numbering and dual provenance.

## CLASSIFICATION

- **FULLY_MAPPABLE (6):** 1, 33–37.
- **SAFE_PARTIAL (0).**
- **EXTERNAL (5):** 2–5, 31.
- **AMBIGUOUS (0).**
- **ENGINE_UNSUPPORTED (26):** 6–30, 32.
- **SOURCE_CONFLICT (0).**

Arithmetic: `6 + 5 + 26 = 37`.

## EXECUTABLE_RULES

| REQ | Class | Owner/path | Rule semantics |
|---|---|---|---|
| 1 | FULL | root / `ipcdo:TrademarkApplicationDetails` | exact selection cardinality `2..2` |
| 33 | FULL | root `ccdo:ResourceItemStatusDetails` | `ValidityPeriodDetails/StartDateTime` required |
| 34 | FULL | same resource status | `ValidityPeriodDetails/EndDateTime` forbidden |
| 35 | FULL | each direct application `SignatureDetails` | at least one signature; if same-signature direct `OfficerDetails` exists, direct `FullNameDetails` forbidden |
| 36 | FULL | same signature | if direct `FullNameDetails` exists, direct `OfficerDetails` forbidden |
| 37 | FULL | each `OfficerDetails` directly under same signature | last name, first name, position required; officer communication forbidden |

## PARTIAL_RULES

None. No role-scoped local fragment is safe without a normative, machine-readable discriminator of the prior and allocated applications.

## UNMAPPED_RULES

- `REQ2–5 | EXTERNAL`: each is selected by a document-kind classifier and by the prior/allocated role. Do not synthesize the classifier or assign roles by element index.
- `REQ6–29 | ENGINE_UNSUPPORTED`: Table 44 semantics apply only to the allocated application. `R.IP.SP.02.002` has two identical repeatable `TrademarkApplicationDetails` siblings and Table 61 provides no element, QName, attribute, or value selector that identifies that role. Applying these rules to both instances would be a normative change; selecting `[1]` would simulate forbidden ordinal semantics. This includes Table 44 REQ26’s code **OR** name and REQ27’s same-trademark condition.
- `REQ30 | ENGINE_UNSUPPORTED`: `SourceTrademarkApplicationId` is required for the allocated application and must equal the prior application’s ID. Both role selection and cross-instance equality are unsupported.
- `REQ31 | EXTERNAL`: both role-specific resource existence/absence checks are external and require identifying the two instances.
- `REQ32 | ENGINE_UNSUPPORTED`: status containers and fixed codes differ by prior (`02`, no codeListId) versus allocated (`01`) application; there is no safe role selector.

## STRUCTURE_PATHS

- Root `ipcdo:TrademarkApplicationDetails` is schema `1..*`, QName `{urn:EEC:M:IP:ComplexDataObjects:vZ.Z.Z}TrademarkApplicationDetails`; Table 61 narrows it to exactly two but does not label either instance.
- `.../ipsdo:SourceTrademarkApplicationId` is a direct application child, schema `0..1`; it describes the source application but does not furnish an executable, normative selector for the two Table 61 roles without enforcing the very cross-instance relation in REQ30.
- Direct `IPEntityStatusDetails/StatusCode/@codeListId` exists beneath each application, so status values cannot be assigned to prior/allocated roles by owner alone.
- Root resource dates and direct signature paths are role-independent and executable. Signatures are `0..*`; direct signature `FullNameDetails` and `OfficerDetails` are distinct from stakeholder-owned paths.

## REPEATABLE_NOTES

- The two application slots are **not** a generic sparse-alignment case. Their semantic roles are ordinally described but structurally unlabelled; `first/second` mapping is forbidden. No role-specific repeatable test may be written until a normative discriminator or engine capability exists.
- REQ35–37 remain repeatable signature/officer rules. Require `good+good → PASS`, `bad+good → FAIL`, `good+bad → FAIL`, with **SAME_PARENT_REQUIRED**.

## COLLISION_RISKS

- Two sibling applications expose the same QName/path. Positional leakage or scalar broadcast would silently misassign prior versus allocated semantics.
- `TrademarkApplicationId`, `StatusCode`, and `IPDocKindCode` occur in both application instances; direct-vs-nested same local names do not identify roles.
- Direct signature officer/full-name paths differ from stakeholder paths; wrong namespace and repeated sibling leakage must not satisfy REQ35–37.

## TEST_MATRIX

1. Valid production E2E for the six executable rules: build → serialize → parse → production extract → validate.
2. Negative tests for REQ1, REQ33–37; signature same-parent and sparse alignment matrix; direct-signature versus stakeholder owner collision.
3. Message isolation: MSG043’s cardinality and root resource/signature rules do not execute for another `R.IP.SP.02.002` message.
4. Do not add tests that assume first/second application role mapping. Future role-specific tests require a confirmed discriminator and implementation.

## IMPLEMENTATION_NOTES

Writer should record 14 captured rows and 37 expanded entries, including dual Table 61/Table 44 provenance for REQ6–29. The mapping must intentionally leave REQ2–32 unmapped except the global root/signature rules above. This is not a missing implementation: Table 61’s prior/allocated semantics cannot be safely bound to identical repeated XML instances under the stated engine constraints.

## READY_FOR_IMPLEMENTATION

YES
