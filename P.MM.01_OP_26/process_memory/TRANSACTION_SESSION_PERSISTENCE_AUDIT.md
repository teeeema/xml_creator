# Transaction session persistence audit

Дата: 2026-08-25. Статус: **ARCHITECTURE COMPLETE — MVP RESTORE NOT IMPLEMENTED**.

## Audit conclusion

Восстановление SOAP-корреляции после перезапуска архитектурно возможно, но
текущих данных недостаточно для безопасной реализации. Нынешний draft не
является доказательством существования транзакции: он хранит Body values и
контекст формы, а `session_metadata` содержит только `ProcedureID`,
`ConversationID` и явный `session_restorable: false`. Автоматически создавать
из этого `TransactionInstance` нельзя.

MVP остановлен после анализа. Причины:

1. application `TransactionSession` создаёт `TransactionInstance` без
   `TransactionDefinition` и не проводит GUI flow через `TransactionEngine`;
2. сохраняются не все `MessageRecord`, state, attempts, pattern, timestamps,
   direction/status, signals/faults и transition context;
3. `FaultFactory` вообще не добавляет record в transaction history;
4. P.MM.01 mutual-obligations и notification metadata не представлены в
   сохраняемом runtime state; `guaranteed_delivery` у ряда package entries
   nullable, что нельзя интерпретировать при restore;
5. Body correlation (`EDocId`/`EDocRefId`) не является частью generic session
   history и не должна выводиться из SOAP IDs;
6. нет нормативно подтверждённой политики, можно ли считать локально
   «сформированный», но не переданный XML совершившим transaction event.

До устранения этих границ сохраняется `SESSION_RESTART_REQUIRED`.

## Current session model

- `ProcedureInstance`: `procedure_code`, typed `ProcedureId`, optional parent.
- `TransactionInstance`: transaction code, `ConversationId`, procedure,
  `message_history`, `TransactionState`, optional `TransactionDefinition`,
  aggregate `retry_attempts`.
- `MessageRecord`: MessageID, typed Action, created_at, sequence, kind,
  RelatesTo, retry_of, attempt_number, optional transition_id.
- `MessageFactory`: всегда создаёт новый MessageID; initial требует пустую
  history; follow-up получает correlation source через `CorrelationService`.
- `CorrelationService`: без state machine берёт последний record; со state
  machine должен брать источник нормативно предыдущего этапа.
- `TransactionEngine`: отдельно управляет pattern state, signals, timeouts,
  completion/rollback и retry count.
- GUI/application session сейчас использует только `MessageFactory`, а не
  полноценный `TransactionEngine`; после generation состояние становится
  общим `ACTIVE`.

Следствие: текущая GUI-сессия достаточна для простого in-memory
request→response, но не является полной persistable state machine.

## What draft currently stores

`DraftDocument` version 1 хранит timestamps, process/TRN/MSG, process version,
structure/version, generation mode, Body values, notes и свободный
`session_metadata`. Запись атомарная, UTF-8 JSON, без pickle.

Текущий controller записывает в `session_metadata` только:

```json
{
  "conversation_id": "urn:uuid:...",
  "procedure_id": "urn:uuid:...",
  "session_restorable": false
}
```

MessageID, Action, history, state, pattern, attempt, request Body correlation и
package compatibility fingerprint отсутствуют. При load session сбрасывается,
а Facade возвращает `SESSION_RESTART_REQUIRED`.

## Draft data versus runtime state

Draft data: пользовательские Body values, выбранный process/TRN/MSG,
structure/profile metadata, generation mode и заметки. Эти данные можно
revalidate и открыть как новый документ.

Runtime transaction state: конкретный экземпляр procedure/transaction, IDs,
pattern state, complete ordered history, attempts, received/sent events,
correlation sources и timing evidence. Оно допустимо только после фактического
начала session и должно иметь отдельную версионированную модель.

## Required persistent state

Рекомендуемая portable модель `TransactionSessionSnapshot`:

- `session_snapshot_version` (независим от `draft_version`);
- `snapshot_id`, `created_at`, `updated_at`, `last_event_at`;
- process code/version и package compatibility fingerprint;
- procedure code и полный typed ProcedureID component chain;
- transaction code, pattern, guaranteed-delivery resolution, parameters;
- state и aggregate retry attempts;
- ConversationID;
- ordered history records:
  - message code (если APPLICATION), MessageID, serialized typed Action;
  - message kind и signal/fault subtype;
  - direction (`SENT`/`RECEIVED`) и lifecycle status;
  - created_at, sequence, transition id;
  - RelatesTo, retry_of, attempt number;
  - ProcedureID и ConversationID, записанные/проверенные для события;
- generic Body-correlation facts, например immutable document identifier facts
  с source message ID и semantic role, но без P.MM.01 field names;
- optional timeout observations/deadlines как runtime facts, не юридический
  вывод о просрочке.

Не сохранять Python objects, serializer/factory instances, GUI controls,
локальные paths, random generator state, XML как источник истины, secrets или
неподтверждённое «отправлено».

## Decision №5 correlation considerations

- Каждый новый message/retry получает новый MessageID. Старые MessageID после
  restore существуют только как immutable history/correlation targets.
- Initial не имеет RelatesTo и допустим только при пустой history.
- Follow-up RelatesTo ссылается на MessageID, полученный участником на
  нормативно предыдущем этапе, а не просто на последний JSON item.
- Retry получает новый MessageID, сохраняет Action, имеет `retry_of` исходной
  попытки и следующий attempt number. Aggregate attempts не обнуляются.
- ProcedureID может продолжаться после restart только при valid complete
  snapshot: restart приложения сам по себе не создаёт новую procedure.
- ConversationID принадлежит экземпляру транзакции и также может продолжаться
  только при valid snapshot. Open-as-new всегда создаёт новый ConversationID.
- SOAP `MessageID/RelatesTo` и Body `EDocId/EDocRefId` — независимые оси.

## Scenario matrix

| Scenario | Safe behaviour now | Future continue requirement |
|---|---|---|
| A. Draft до первого event | открыть Body как новый документ; session отсутствует | snapshot не нужен и старые IDs не создаются |
| B. Request сформирован | сейчас restart required | complete request record, event status, IDs, state и Body correlation |
| C. Response draft | сейчас restart required | request history + response Body draft; новый response MessageID только при generation |
| D. Notification | открыть как новый; не придумывать response | pattern state и RCV event/history, если notification реально начата |
| E. TRN.008/TRN.012 | restore запрещён | complete signals/application history, state, delivery policy, rollback state |
| F. Retry | restore запрещён | original/retry chain, attempts, state and timeout/fault trigger |

Важно: создание XML и фактическая отправка сейчас не различаются transport
receipt/status. Поэтому snapshot «request уже сформирован» нельзя автоматически
трактовать как удалённо начатую транзакцию.

## Safe to restore

- Body values и form context через существующую draft revalidation.
- Session только после отдельной проверки: supported snapshot version; exact
  process/TRN/pattern; compatible process package; valid state/history; unique
  IDs; consistent ProcedureID/ConversationID; valid Action and relationship
  graph; known correlation source; acceptable timeout status.
- Completed/cancelled/failed/rollback-required session можно открыть только для
  просмотра или как новый документ, если product policy отдельно не разрешает
  конкретное действие.

## Unsafe to restore

- snapshot отсутствует либо это только legacy `session_metadata`;
- неизвестная версия snapshot;
- process/TRN/pattern/guaranteed-delivery changed;
- duplicate MessageID, dangling/wrong RelatesTo, broken retry chain;
- inconsistent ProcedureID/ConversationID;
- невозможный state/history transition;
- process version mismatch для Continue;
- potentially expired session без подтверждения пользователя/runtime policy;
- response draft без доказуемого source request;
- сформированный XML, статус отправки которого неизвестен.

Результат: `SESSION_RESTORE_INVALID`; Body всё ещё можно предложить открыть как
новый после обычной draft validation.

## Open-as-new semantics

Body values сохраняются и повторно валидируются. Не переносятся session state,
history, ProcedureID, ConversationID, MessageID, RelatesTo, retry chain и SOAP
correlation. Создаётся новая procedure/transaction и каждый message получает
новый MessageID. Correlation Body fields нельзя автоматически переносить, если
они относятся к прежнему transaction event; для этого нужна отдельная generic
classification/migration policy.

UX: «Создан новый экземпляр транзакции. Идентификаторы предыдущей сессии не
используются.»

## Continue-session semantics

Continue — явный выбор пользователя, не side effect draft load. Перед выбором
показываются ProcedureID, ConversationID, process/TRN/pattern, state, last
message/event и snapshot time. После успешной строгой проверки Facade создаёт
runtime aggregate вокруг snapshot; новый message создаётся обычным factory и
получает новый MessageID.

## Version compatibility

- `draft_version` и `session_snapshot_version` независимы.
- Body/Structure mismatch обрабатывается существующей draft revalidation и не
  доказывает совместимость session.
- Continue требует exact process version/package semantic fingerprint в MVP.
  При mismatch — `SESSION_RESTORE_VERSION_MISMATCH`, только Open as new.
- Будущая migration должна быть явной version-to-version функцией с tests, а не
  permissive warning.

## Timeout considerations

Snapshot должен хранить UTC event timestamps и известные deadline facts.
Validator сравнивает их с текущими transaction parameters. Если deadline мог
истечь, статус `SESSION_RESTORE_STALE` и Continue блокируется или требует
отдельного подтверждённого runtime policy. Формулировка только техническая:
«Сохранённая транзакция могла выйти за нормативный срок»; юридический вывод не
делается. Scheduler/transport в этот этап не добавляется.

## Recommended architecture

Сравнение вариантов:

- A, optional snapshot внутри draft: удобен и атомарен, но смешивает жизненные
  циклы Body draft и runtime session и дублирует историю в каждом autosave.
- B, отдельный `*.eaeusession.json`: лучше разделяет ответственность, но требует
  atomic coordination двух файлов и понятного linking UX.
- C, draft → session id: чистое разделение, но требует локального session store,
  missing-reference handling и переносимости пары файлов.

Рекомендация: **B + optional immutable `snapshot_id` reference in draft**.
`TransactionSessionSnapshot` живёт отдельно; draft хранит только reference и
presentation summary. Экспорт portable bundle можно добавить позже. Legacy
`session_metadata` не повышается до snapshot.

Будущие generic компоненты:

- `TransactionSessionSnapshot` DTO;
- `SessionSnapshotValidator`;
- `SessionPersistenceService` с atomic JSON write;
- `SessionRestoreService`, единственный конструктор runtime aggregate;
- Facade: `inspect_draft_session`, `continue_session`, `open_draft_as_new`;
- GUI только показывает inspect result и передаёт явный choice.

## Validator test matrix

Обязательные tests перед feature: no-session draft; request→response;
response draft; notification; both mutual-obligation flows; rollback-required;
retry chain; duplicate MessageID; dangling/wrong RelatesTo; wrong ProcedureID;
wrong ConversationID; invalid state sequence; unsupported snapshot version;
process/pattern/version mismatch; stale timeout; missing session file; atomic
write; legacy draft compatibility; open-as-new regenerates all SOAP IDs.

## Final decision

`SAFE_TO_IMPLEMENT_AFTER_PREREQUISITES = YES`.

`SAFE_TO_RESTORE_FROM_CURRENT_DRAFTS = NO`.

Сначала application session должен использовать полный `TransactionDefinition`
и `TransactionEngine`, а history model должна однозначно фиксировать direction,
message code/subtype, faults и event status. Это persistence layer вокруг
Decision №5 core, а не изменение нормативного ядра.
