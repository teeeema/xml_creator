# Transaction session snapshot v1 implementation

Дата: 2026-08-25.

`SESSION_SNAPSHOT_V1_IMPLEMENTED = YES`

`SAFE_TO_ENABLE_GUI_CONTINUE = NO`

`LEGACY_DRAFT_SESSION_RESTORE = FORBIDDEN`

## Scope

Реализован отдельный generic persistence layer `*.eaeusession.json`. Он не
встроен в `DraftDocument`, не восстанавливает `TransactionSession` и не меняет
GUI. Legacy draft остаётся Body draft и продолжает выдавать
`SESSION_RESTART_REQUIRED` при наличии старого `session_metadata`.

## Changed files

- `eaeu_xml/application/session_snapshot.py` — DTO, serializer/deserializer,
  validator и atomic storage;
- `eaeu_xml/application/facade.py` — явные `create_snapshot()` и
  `save_snapshot()` hooks у runtime session;
- `eaeu_xml/application/__init__.py` — public API exports;
- `eaeu_xml/tests/test_session_snapshot.py` — snapshot/corruption/correlation
  regression suite;
- engine/process project memory и этот отчёт.

StructureDefinition, MessageRules, profiles, Body schema, Decision №5 core,
XML serializer и wx code не менялись.

## Snapshot schema v1

Top-level:

- `session_snapshot_version = 1`;
- created/updated UTC timestamps;
- process code/version;
- transaction/procedure codes, pattern, guaranteed-delivery resolution and
  transaction parameters;
- typed ProcedureID and ConversationID strings;
- current TransactionState and aggregate retry attempts;
- complete ordered history available in the runtime aggregate.

History record:

- sequence, message code for APPLICATION, direction;
- serialized typed Action, MessageID, RelatesTo and optional RelatesAction;
- UTC timestamp, attempt number and retry_of;
- message kind, signal/fault subtype and transition id;
- per-event ProcedureID/ConversationID evidence.

Body values and business identifiers such as EDocId/EDocRefId are deliberately
absent. Они остаются в Body draft/document model и не являются SOAP correlation.

## Serialization and atomic storage

`SessionPersistenceService` пишет deterministic readable UTF-8 JSON с
`sort_keys=True`. Алгоритм: temporary file в target directory → write → flush →
`fsync` → `os.replace`. При ошибке replace прежний target остаётся неизменным,
temporary удаляется в `finally`.

Load запрещает malformed JSON, non-object root, неизвестную schema version,
missing/unknown fields, неверные history/parameter types и любой snapshot,
который не проходит строгий validator. Silent repair отсутствует.

## Validator

`continue_ready` вычисляется, а не читается из JSON. Проверяются:

- supported snapshot version и обязательный context;
- exact process version при переданном current version;
- typed ProcedureID, ConversationID, MessageID и TransactionState;
- known transaction pattern;
- ordered nonempty history для started state и empty history для NEW;
- direction `SENT/RECEIVED`, UTC timestamp, attempt shape;
- уникальность MessageID;
- backward-only RelatesTo/retry_of graph;
- ApplicationAction components против snapshot context/message code;
- SignalAction против Action source APPLICATION message;
- FaultAction, RelatesTo и RelatesAction против source record;
- retry action/message identity и monotonic attempt number;
- per-record ProcedureID/ConversationID consistency;
- existing `CorrelationValidator` для core history invariants.

Process-version mismatch возвращает `PROCESS_VERSION_MISMATCH` и
`continue_ready = false`, но файл остаётся читаемым без current-version check.

Waiting state с истёкшим либо недоказуемым timing window получает warning
`TIMING_REVALIDATION_REQUIRED`; validator не делает юридический вывод о
просрочке и не считает snapshot continue-ready.

## Lifecycle hooks

`TransactionSession.create_snapshot()` фиксирует только реально существующие
runtime records. `save_snapshot(path)` применяет validator и atomic storage.
Hooks можно вызвать для NEW session или после generated application attempts.

Автоматический autosave на каждом event намеренно не добавлен: текущий GUI
runtime не проводит notification/mutual-obligations/retry/fault lifecycle через
единую application state machine. Signal/fault/retry snapshot coverage доказана
на существующих Decision №5 aggregates отдельно. Fake events/history не
создаются.

## Tests

Добавлены проверки:

- TransactionSession → snapshot → JSON → snapshot round-trip;
- TRN.004 MSG.005 → MSG.006: оба MessageID, response RelatesTo, Actions,
  ProcedureID, ConversationID и history;
- retry attempt 1/2, новый MessageID и retry_of;
- notification без искусственного response;
- signal history и state-compatible correlation;
- fault RelatesTo/RelatesAction;
- malformed JSON, unknown version и broken schema;
- missing history, broken RelatesTo/retry_of, duplicate MessageID;
- invalid direction/Action/state/per-message IDs;
- process-version mismatch и stale timing;
- atomic replace failure preserves old snapshot;
- legacy draft остаётся non-restorable.

## Intentionally not implemented

- GUI Continue/Open as new dialogs;
- snapshot → runtime aggregate restore service;
- automatic snapshot save policy;
- conversion legacy draft/session_metadata to snapshot;
- inferred sent/received transport status;
- invented signal/fault history;
- changes to Decision №5 core or XML generation.

`SAFE_TO_ENABLE_GUI_CONTINUE = NO`, потому что для GUI требуется следующий
отдельный этап: единый application lifecycle поверх `TransactionEngine`, явные
transport/event statuses и restore service, который повторно валидирует snapshot
против текущего package. Сам snapshot v1 уже является строгой безопасной
основой для этого этапа.
