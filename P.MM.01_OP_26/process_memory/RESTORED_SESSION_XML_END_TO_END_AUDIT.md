# Restored session XML end-to-end audit

Дата: 2026-08-25.

## Executive conclusion

Цепочка fresh application restart → typed restore → runtime response → final
SOAP/XML доказана для Header, Action, namespaces, history и serializer. Однако
полный production status не установлен: snapshot v1 намеренно не хранит Body,
а P.MM.01 response требует correlation `EDocRefId <- request EDocId`; кроме того,
application retry API создаёт runtime record, но не имеет payload-backed retry
SOAP/XML generation. Эти ограничения не обходились и production schema/core не
менялись.

## Architecture path

`MainFrame` → `GuiController.generate_xml()` → `EaeuXmlApplication` lifecycle →
typed `SessionOpenResult` → restored `TransactionSession` → `TransactionEngine` /
`MessageFactory` → validated message/context → `XmlSerializer` → parsed XML.

Snapshot никогда не передаётся serializer. GUI не создаёт MessageID,
ProcedureID, ConversationID, RelatesTo/RelatesAction или Action. Serializer
только переносит готовые typed header/body values в XML и не создаёт session,
не выполняет state transition и не решает retry semantics.

## XML normalization

Integration tests используют `xml.etree.ElementTree`: сравнивают expanded
namespace names, структуру Header/Body, атрибуты и semantic text values. Raw XML
и случайные UUID независимых sessions не сравниваются побайтово. Production
serializer ради тестов не изменялся.

## Main TRN.004 acceptance

Созданы Facade/MainFrame A, request A и snapshot; ссылки на A удалены. Затем
созданы новые Facade/MainFrame B, выполнены Open → RESTORABLE → Continue →
response B → final XML parsing.

Доказано:

- `B.MessageID != A.MessageID`;
- XML MessageID равен runtime B MessageID;
- runtime/XML RelatesTo равен A MessageID;
- XML ProcedureID и ConversationID равны original snapshot values;
- XML Action parsed как P.MM.01 / 1.1.0 / PRC.007 / TRN.004 / MSG.006;
- historical A остался первым record, history содержит A и B;
- Body root — `ResourceStatusDetails` в R.007 namespace;
- SOAP/WSA/Interaction и Body namespace URI сохранены;
- EDocId/EDocRefId не подставляются из SOAP identifiers.

## Continuous vs restored

| Invariant | Continuous | Restored | Result |
|---|---|---|---|
| Новый response MessageID | yes | yes | equivalent rule |
| RelatesTo own request | yes | yes | equivalent rule |
| Header element shape | typed factory | typed factory | equal |
| Action | response MSG.006 | response MSG.006 | equal |
| To / ReplyTo rules | current package | current package | equal |
| Procedure/Conversation | own session | preserved session | correct semantics |
| Body structure with identical supplied values | R.007 | R.007 | equal |
| Namespace URIs | current resolution | current resolution | equal |

## Audited event invariants

- Response: final application XML and correlation — PASS.
- Retry: attempts 1/2 survive restore and attempt 3 is appended with a fresh
  MessageID and correct retry_of/attempt number — PASS at runtime. Retry XML —
  BLOCKED because no high-level payload-backed retry XML API exists.
- Signal: TRN.008 RCV survives; next PRS signal serializes after restore with
  fresh MessageID, correct RelatesTo, preserved ProcedureID/ConversationID and
  `WAITING_RESPONSE` state — PASS.
- Fault: post-restore Decision №5 FaultFactory output serializes with fresh
  MessageID, RelatesTo A, `int:RelatesAction == A.Action`, preserved IDs and
  SOAP Fault Body — PASS.
- Notification: initiating XML has no artificial RelatesTo; after restore the
  allowed RCV signal relates to the notification and completes the transaction;
  no fake request/response is introduced — PASS.
- Controlled response validation failure does not change history or snapshot — PASS.

## Body persistence conclusion

For TRN.004 the next SOAP Header needs only restored runtime history. The next
P.MM.01 Body, however, needs the previous request `EDocId` to populate response
`EDocRefId`. `TransactionSession.request_body_values` is in-memory only;
snapshot v1 deliberately excludes Body and a restored session initializes it as
empty. Generated response test data does not contain `EDocRefId`. Correct Body
can be produced only when the caller separately supplies
`body_correlations={EDocRefId: request EDocId}`; current GUI restart flow has no
safe source for that value.

PREVIOUS_BODY_REQUIRED_FOR_CONTINUATION = YES

BODY_PERSISTENCE_SUFFICIENT = NO

No fake snapshot↔draft linkage was added. Open-as-new remains correct: a Body
draft is explicitly loaded, a fresh lifecycle session gets new ProcedureID,
ConversationID and MessageID, with no old RelatesTo/history. Legacy draft remains
Body-only and cannot Continue an old SOAP session.

## Invalid restore

SNAPSHOT_INVALID, PROCESS_VERSION_MISMATCH, TIMING_REVALIDATION_REQUIRED and
STATE_INVALID return continue_ready false. Controller Continue raises and a
response Generate in a fresh context returns `INITIAL_MESSAGE_REQUIRED`; there
is no fallback create_new. Existing correlation-invalid coverage follows the
same typed rule.

## Identity separation

SOAP correlation fields are emitted only from typed Header. Body EDoc fields
come only from Body values/building. Source audit found no GUI/controller UUID,
manual RelatesTo, snapshot→serializer shortcut, or process-specific branch.
Tests assert EDoc values are not copied from SOAP MessageID, RelatesTo,
ProcedureID or ConversationID. The missing EDocRef correlation is an absence of
Body state, not substitution with SOAP correlation.

## XSD status

Generated documents pass existing application Body validation, XML
well-formedness and typed Decision №5 construction/validation. Physical official
XSD for placeholder R.007 remains unavailable; no XSD was invented.

XSD_VALIDATION = NOT_AVAILABLE

## Found defects / blockers

1. `RESTORED_BODY_CORRELATION_UNAVAILABLE`: snapshot v1 excludes the request
   `EDocId`; restored GUI cannot automatically supply response `EDocRefId`.
   Affected boundary: separate Body draft/session persistence design. No fix in
   this audit because changing snapshot schema or introducing implicit coupling
   was explicitly out of scope.
2. `RETRY_XML_PAYLOAD_UNAVAILABLE`: retry runtime history is correct, but
   `TransactionSession.retry()` returns only a MessageRecord and snapshot has no
   Body payload for final retry XML. Affected boundary: application retry payload
   reconstruction. No artificial test-side envelope construction was added.

No defect was found in restored response Header/XML, signal/fault serialization,
serializer ownership or typed restore gating.

## Verification

- Baseline: 259 tests / 887 subtests — PASS.
- Final: 268 tests / 892 subtests — PASS.
- New: 9 tests / 5 subtests.
- Engine non-GUI: 172 — PASS; Engine GUI: 13 — PASS.
- P.MM.01 non-GUI: 65 — PASS; P.MM.01 GUI: 18 — PASS.
- Snapshot/restore focused: 26 — PASS.
- XML integration focused: 9 — PASS.
- Real wx fresh MainFrame restart→restore→response XML parsing — PASS.
- Compile/import, process-hardcode scan and four-size wx resize — PASS.

## Final statuses

RESTORED_SESSION_XML_GENERATION_PROVEN = YES

CONTINUOUS_VS_RESTORED_XML_SEMANTICS_EQUIVALENT = YES

PROCEDURE_ID_PRESERVED_IN_FINAL_XML = YES

CONVERSATION_ID_PRESERVED_IN_FINAL_XML = YES

NEW_MESSAGE_ID_AFTER_RESTORE_PROVEN = YES

RELATES_TO_AFTER_RESTORE_PROVEN = YES

ACTION_AFTER_RESTORE_PROVEN = YES

RETRY_XML_AFTER_RESTORE_PROVEN = NO

SIGNAL_XML_AFTER_RESTORE_PROVEN = YES

FAULT_XML_AFTER_RESTORE_PROVEN = YES

NOTIFICATION_XML_SEMANTICS_PRESERVED = YES

BODY_SOAP_IDENTIFIER_SEPARATION_PROVEN = YES

INVALID_RESTORE_CANNOT_GENERATE_CONTINUATION_XML = YES

GUI_RESTORE_TO_XML_END_TO_END_PROVEN = YES

SESSION_PERSISTENCE_END_TO_END_PROVEN = NO

SAFE_FOR_PRODUCTION_SESSION_CONTINUATION = NO
