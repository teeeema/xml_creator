# Unified transaction lifecycle and runtime restore

Дата: 2026-08-25.

## Status

`SESSION_RUNTIME_RESTORE_IMPLEMENTED = YES`

`RUNTIME_ROUNDTRIP_PROVEN = YES`

`STATE_REPLAY_PROVEN = YES`

`CORRELATION_REVALIDATION_PROVEN = YES`

`SAFE_TO_ENABLE_GUI_CONTINUE = YES`

`LEGACY_DRAFT_SESSION_RESTORE = FORBIDDEN`

Значение `SAFE_TO_ENABLE_GUI_CONTINUE = YES` относится только к будущему GUI,
который выдаёт session исключительно при `SessionRestoreStatus.RESTORABLE`.
Timing/mismatch/unsupported direction и любые validation issues Continue
блокируют. Сам GUI на этом этапе не изменён.

## Architecture

Добавлены два application-layer компонента:

- `TransactionSessionLifecycleService`: явно разделяет `create_new()` и
  `restore_existing()`;
- `TransactionSessionRestoreService`: выполняет двухфазный restore и никогда не
  возвращает candidate session до final acceptance.

`create_new()` создаёт новые ProcedureID/ConversationID; MessageID создаётся
обычным factory при новом attempt. `restore_existing()` не генерирует и не
переписывает ни одного historical ID.

## Restore pipeline

1. Snapshot schema/identifier/history validator.
2. Lookup текущего ProcessPackage по process code.
3. Exact process-version check.
4. Transaction definition compatibility: procedure, pattern,
   guaranteed-delivery value, timeouts и retry count.
5. Message membership и current package Action comparison.
6. Candidate reconstruction с исходными ProcedureID, ConversationID,
   MessageID, timestamps, Actions и links.
7. Replay через существующий `TransactionStateMachine`, `TransactionEngine` и
   `RetryValidator`.
8. `TransactionValidator`/`CorrelationValidator` на candidate aggregate.
9. Exact replayed-state comparison.
10. Runtime → snapshot equality check.
11. Только после всех проверок создаётся accepted `TransactionSession`.

## Restore result statuses

Typed `SessionRestoreStatus` включает:

- `RESTORABLE`;
- `SNAPSHOT_INVALID`;
- `PROCESS_NOT_FOUND`, `PROCESS_VERSION_MISMATCH`;
- `TRANSACTION_NOT_FOUND`, `TRANSACTION_DEFINITION_MISMATCH`;
- `MESSAGE_DEFINITION_MISMATCH`, `ACTION_INVALID`, `DIRECTION_INVALID`;
- `CORRELATION_INVALID`, `RETRY_INVALID`, `SIGNAL_INVALID`, `FAULT_INVALID`;
- `STATE_INVALID`;
- `TIMING_REVALIDATION_REQUIRED`.

`SessionRestoreResult.session` существует только для `RESTORABLE`.
`continue_ready` вычисляется из status/session, а не из JSON.

## Unified runtime lifecycle

New sessions теперь получают текущую core `TransactionDefinition` и используют
`TransactionEngine` для state transitions:

- initial application → pattern-specific initial waiting/completed state;
- response → existing receive-response transition;
- retry → existing RetryService;
- signal → SignalFactory + state-machine signal transition;
- fault → FaultFactory + failed transition.

Application session хранит presentation/runtime evidence, которого нет в
`MessageRecord`: direction, message code, signal/fault subtype и RelatesAction.
Эти данные попадают в snapshot и восстанавливаются без default/fake history.

Текущий desktop runtime моделирует локально создаваемые events и сохраняет
direction `SENT`. Snapshot с `RECEIVED` блокируется `DIRECTION_INVALID`, пока не
будет добавлена отдельная actor/transport ingestion model. Это fail-closed
ограничение, а не best-effort restore.

## State replay

Replay начинается с NEW:

- первый APPLICATION обязан быть initiating message текущей transaction;
- pattern state вычисляется current state machine;
- retry не заменяет predecessor, проходит RetryValidator и сохраняет state;
- response допустим только из разрешённого state и коррелирует с последним
  application attempt соответствующего этапа;
- RCV/PRS/ERR остаются SIGNAL и проходят signal transitions;
- fault остаётся TECHNICAL_FAULT и переводит candidate в FAILED;
- рассчитанный state обязан совпасть со snapshot state.

Snapshot state не является доверенным входом.

## Correlation and IDs

Restore сохраняет точно:

- ProcedureID и ConversationID;
- все historical MessageID;
- Action, RelatesTo, retry_of, attempts и timestamps;
- signal/fault type и Fault RelatesAction.

Следующий новый response/retry/signal/fault получает новый MessageID через
существующие IdentifierService/Factory. TRN.004 test доказывает новый response
MessageID, RelatesTo исходного request и прежние ProcedureID/ConversationID.

EDocId/EDocRefId не входят в snapshot/runtime SOAP graph.

## Timing

Waiting snapshot, у которого timeout window потенциально истёк или не доказан,
возвращает `TIMING_REVALIDATION_REQUIRED`, `session=None` и
`continue_ready=false`. Юридический вывод о просрочке не делается.

## Backward compatibility

- snapshot schema остаётся v1;
- legacy draft остаётся Body draft;
- legacy `session_metadata` не конвертируется;
- `SESSION_RESTART_REQUIRED` сохранён;
- Open as new и GUI dialogs не реализованы;
- StructureDefinition, MessageRules, profiles, Body schema, Decision №5 core и
  XML serializer не менялись.

## Tests

Новый restore module проверяет:

- simple restore и exact snapshot→runtime→snapshot invariant;
- TRN.004 restart, next response IDs/correlation;
- retry attempt 3 после restore;
- notification restore без fake response;
- TRN.008 RCV history restore и следующий PRS transition;
- новый Fault после restore с core RelatesTo/RelatesAction;
- process version и missing transaction;
- unknown transaction message и direction mismatch;
- state replay mismatch и semantic RelatesTo mismatch;
- invalid retry predecessor;
- incompatible signal/fault history;
- stale timing;
- legacy draft rejection;
- create-new versus restore-existing ID semantics.

## Changed files

- `application/session_restore.py`;
- `application/session_snapshot.py`;
- `application/facade.py`;
- `application/__init__.py`;
- `tests/test_session_restore.py`;
- `tests/test_session_snapshot.py`;
- engine/process memory and this report.

## Intentionally not implemented

- GUI Continue/Open as new;
- automatic opening of session files;
- automatic restore from drafts;
- process-version migration;
- timeout legal policy;
- transport/MQ received-event ingestion;
- Body-value migration or SOAP/business-ID mixing.
