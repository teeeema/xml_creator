# End-to-end transaction verification

Verified through the generic ProcessPackage and Decision No. 5 APIs. No
transaction-specific code was added to the engine.

| Transaction | PRC | Request | Success response | Alternative response | Result |
|---|---|---|---|---|---|
| P.MM.01.TRN.004 | P.MM.01.PRC.007 | MSG.005 / R.007 | MSG.006 / R.007 | - | Catalog and Action verified; Body/SOAP blocked by `UNRESOLVED_STRUCTURE_VERSION` |
| P.MM.01.TRN.005 | P.MM.01.PRC.008 | MSG.007 / R.HC.MM.01.007 v1.0.0 | MSG.008 / R.HC.MM.01.001 v1.1.0 | MSG.009 / R.006 | Request/success SOAP verified; alternative blocked by `UNRESOLVED_STRUCTURE_VERSION` |
| P.MM.01.TRN.006 | P.MM.01.PRC.009 | MSG.010 / R.HC.MM.01.007 v1.0.0 | MSG.011 / R.HC.MM.01.001 v1.1.0 | MSG.009 / R.006 | Request/success SOAP verified; alternative blocked by `UNRESOLVED_STRUCTURE_VERSION` |

Resolved branches verify Body validation, MessageRules application, ordered
Body serialization, Decision No. 5 Header and SOAP serialization, namespaces,
Action, MessageID, ProcedureID, ConversationID and XML well-formedness.
Responses have a new MessageID, preserve ProcedureID and ConversationID, and
set SOAP `RelatesTo` to the request MessageID. Body `EDocRefId` references the
request `EDocId` independently and is not used as SOAP correlation.

Reference artifacts: four SOAP XML files and three blocked reports under
`examples/p_mm_01/`. Blocked reports contain message, structure, null active
version, blocking status and message/structure source references.

Baseline: 80 tests. Final: 63 engine + 21 package = 84 tests. Import and compile
checks pass. Package remains `BODY_MODEL_CONFIRMED_WITH_EXTERNAL_CONFLICTS` and
is not production-ready.
