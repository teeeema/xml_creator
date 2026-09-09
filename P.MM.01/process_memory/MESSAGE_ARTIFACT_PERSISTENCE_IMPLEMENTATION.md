# Message artifact persistence implementation

Дата: 2026-08-25.

## Architecture

`TransactionSessionSnapshot` v1 остаётся самостоятельным SOAP runtime contract.
Historical Body не добавлен в его history. Новый `TransactionSessionBundle` v1
атомарно сохраняет два разных компонента: snapshot и immutable
`PersistedMessageArtifact` records. Bundle имеет собственную версию и не меняет
версию snapshot.

Artifact связан с history только по `message_id_ref` как technical reference,
а не business identifier. Он хранит transaction/message code, attempt number,
canonical JSON Body payload и SHA-256 integrity digest. Payload — snapshot
значений конкретного successfully materialized/generated application attempt;
он не является ссылкой на editable GUI draft.

## Persistence and validation

Один `*.eaeusession.json` bundle пишется через temporary file → flush → fsync →
`os.replace`. Поэтому операция Save Session является единым safe contract и не
может сообщить об успешном snapshot save без artifact set. Validator отвергает
unknown bundle/artifact versions, malformed JSON/payload, SHA mismatch,
duplicate references, unknown history reference, transaction/message/attempt
mismatch. Старый plain snapshot остаётся readable, но без artifacts.

## Body codec and immutability

Payload codec losslessly round-trips primitives, bool, lists, nested mappings,
attributes-by-path, base64 BinaryText values и `ANY_XML` Element. `payload_json`
canonicalized; mutation исходного GUI dict после generation не меняет artifact.
Local path/filename binary input не сохраняется — только actual base64 Body value.
Large binary may legitimately duplicate payload across retry artifacts; отдельная
deduplication не добавлялась.

## Body correlation

Generic resolver видит только source-traced `CORRELATION/PREVIOUS_BODY` policy
из external ProcessPackage. P.MM.01 policy for target `EDocHeader/EDocRefId`
declares `correlation_source_path: EDocHeader/EDocId`. Resolver ищет это значение
только в immutable historical artifacts; он никогда не использует MessageID,
RelatesTo, ProcedureID или ConversationID. Missing payload/source returns typed
`BODY_CORRELATION_UNRESOLVED`; silent autofill отсутствует.

## Retry

`TransactionSession.retry_with_payload(message_id)` — application API. Он
проверяет original runtime attempt и artifact, builds Body through existing
provider, затем использует existing RetryService and MessageFactory to create a
fresh header. New MessageID, retry_of, attempt chain and Decision №5 context
принадлежат runtime; Body семантически равен original artifact. Raw historical
XML не повторно отправляется. Missing/corrupt artifact blocks retry and never
uses current GUI form.

## Restore / legacy / GUI

Lifecycle open распознаёт bundle, restores existing snapshot through unchanged
restore service и присоединяет validated artifacts only after RESTORABLE result.
Plain legacy snapshot is still restorable for SOAP-only operations but has no
artifact payload capability. Legacy `*.eaeudraft.json` remains Body-only and
cannot restore SOAP session. Open-as-new remains fresh lifecycle semantics and
does not inherit historical artifacts.

Signals/Faults/notifications remain their existing typed branches; no false
application Body artifact is manufactured for them. Incoming RECEIVED artifact
ingestion/transport model is still out of scope.

## Verification

- Baseline: 268 tests / 892 subtests.
- Final: 273 tests / 905 subtests.
- New artifact-focused tests: 5 tests / 13 subtests.
- Covered: Body round-trip/immutability; binary/base64; nested/list/bool/XML;
  bundle integrity; EDocId→EDocRefId after fresh restart; retry XML after restart;
  missing/corrupt artifact blocking; real macOS wx bundle restore response XML.

## Status

MESSAGE_ARTIFACT_PERSISTENCE_IMPLEMENTED = YES

HISTORICAL_BODY_ROUNDTRIP_PROVEN = YES

EDOC_CORRELATION_AFTER_RESTART_PROVEN = YES

PAYLOAD_BACKED_RETRY_IMPLEMENTED = YES

RETRY_BODY_AFTER_RESTART_PROVEN = YES

BINARY_RETRY_PAYLOAD_PROVEN = YES

SESSION_ARTIFACT_CONSISTENCY_PROVEN = YES

LEGACY_DRAFT_SESSION_RESTORE = FORBIDDEN
