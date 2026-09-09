# GUI transaction session controls implementation

Дата: 2026-08-25.

## Scope and changed layers

Добавлены GUI-операции «Открыть сессию», «Продолжить сессию», «Открыть как
новую», «Сохранить сессию» и компактная панель сведений. GUI использует только
`EaeuXmlApplication`, typed restore result и восстановленный application
`TransactionSession`. Decision №5 core, TransactionEngine, snapshot schema,
validator/restore semantics, ProcessPackage, Body/XML и нормативные данные не
изменялись.

Application boundary получил минимальные методы открытия и сохранения session.
`SessionPersistenceService.load_candidate()` выполняет только строгий JSON/schema
decode, после чего candidate обязательно передаётся lifecycle restore. Это
позволяет GUI показать реальный typed semantic status, не создавая runtime из
JSON и не понижая строгость проверки.

## Open Session flow

1. wx file dialog принимает только `*.eaeusession.json`.
2. Facade вызывает `TransactionSessionLifecycleService.open_existing()`.
3. Storage декодирует schema candidate.
4. Lifecycle вызывает существующий `restore_existing()` и полный restore service.
5. GUI получает `SessionOpenResult` с typed `SessionRestoreResult`.
6. Восстановленный session остаётся pending до явного Continue.

Malformed/schema-invalid input возвращает `SNAPSHOT_INVALID`; session не
создаётся, текущее приложение остаётся работоспособным. Semantic failures
сохраняют свои enum statuses: version/timing/state/correlation/message/action,
retry/signal/fault/direction и missing definitions.

## Continue rule and runtime ownership

Кнопка Continue включается только по `SessionOpenResult.continue_ready`, который
делегирует существующему правилу `status is RESTORABLE and session is not None`.
JSON flags не читаются. После Continue controller использует именно
`restore.session`, помечает UI context как `SessionMode.RESTORED` и не создаёт
новую session. Повторное формирование initiating message в RESTORED context
возвращает `INITIAL_ALREADY_GENERATED`, исключая случайный `create_new()`.

ProcedureID, ConversationID, historical MessageID/Action/RelatesTo, attempts,
retry/signal/fault history и current state принадлежат runtime. GUI не создаёт и
не исправляет correlation. Следующий message attempt проходит обычный runtime и
получает новый MessageID.

## Typed status presentation

Покрыты все существующие `SessionRestoreStatus`: `RESTORABLE`,
`SNAPSHOT_INVALID`, `PROCESS_NOT_FOUND`, `PROCESS_VERSION_MISMATCH`,
`TRANSACTION_NOT_FOUND`, `TRANSACTION_DEFINITION_MISMATCH`,
`MESSAGE_DEFINITION_MISMATCH`, `ACTION_INVALID`, `DIRECTION_INVALID`,
`CORRELATION_INVALID`, `RETRY_INVALID`, `SIGNAL_INVALID`, `FAULT_INVALID`,
`STATE_INVALID`, `TIMING_REVALIDATION_REQUIRED`. Основная строка человекочитаема;
process/version/transaction/IDs/state/history/attempts и issues доступны в info.

Version mismatch и timing revalidation всегда блокируют Continue. Timing text
не утверждает, что сессия юридически истекла. `RECEIVED` не переписывается в
`SENT`; существующее ограничение actor/transport model отображается через
`DIRECTION_INVALID`.

## Open as new and Body draft separation

Session snapshot намеренно не содержит Body values. Поэтому fake coupling не
добавлен. «Открыть как новую» явно просит выбрать `*.eaeudraft.json`, загружает
его существующим draft API и вызывает обычный lifecycle `create_new()`. Body
values сохраняются; ProcedureID и ConversationID новые; history/attempts/retry/
signals/faults/state старой session не переносятся.

Legacy draft остаётся Body-only: его можно открыть обычным способом или как
новую транзакцию, но попытка открыть его как session даёт `SNAPSHOT_INVALID` и
Continue недоступен. `LEGACY_DRAFT_SESSION_RESTORE = FORBIDDEN` сохранён.

## Save Session and dirty state

Save Session доступен только при активном application `TransactionSession` и
вызывает facade/session `save_snapshot()`; GUI не сериализует JSON. Open Session
и Open as new используют существующее подтверждение dirty draft. Draft и
session имеют разные dialogs, extensions, menu items и labels.

## Responsive layout

Session info входит в существующую responsive data tab. Action controls находятся
в `wx.WrapSizer`, status text повторно Wrap-ится, минимум остаётся `700x560`.
Проверены `1200x800`, `900x650`, `700x560`, `1100x760`; clipping отсутствует.

## Tests and smoke

- Исходный подтверждённый baseline: 253 tests / 861 subtests.
- Final unified run: 259 tests / 887 subtests — PASS.
- Engine non-GUI: 172 — PASS.
- P.MM.01 non-GUI: 56 — PASS.
- Combined GUI: 31 — PASS.
- Session snapshot + restore focused: 26 — PASS.
- Compile/import checks — PASS.
- Real macOS wx: save → restart/new Frame → open → RESTORABLE → Continue →
  response — PASS.
- Invalid snapshot и four-size resize внутри real Frame — PASS.

Главный acceptance доказал: response B MessageID отличается от request A;
`B.RelatesTo == A`; ProcedureID и ConversationID не изменились; historical A и
history сохранены; restored state принят application layer.

## Final status

GUI_SESSION_OPEN_IMPLEMENTED = YES

GUI_SESSION_CONTINUE_IMPLEMENTED = YES

GUI_OPEN_AS_NEW_IMPLEMENTED = YES

GUI_SESSION_SAVE_IMPLEMENTED = YES

CONTINUE_ONLY_FOR_RESTORABLE = YES

GUI_DOES_NOT_IMPLEMENT_CORRELATION = YES

LEGACY_DRAFT_SESSION_RESTORE = FORBIDDEN

PROCESS_VERSION_MISMATCH_BLOCKS_CONTINUE = YES

TIMING_REVALIDATION_BLOCKS_CONTINUE = YES

GUI_SESSION_CONTROLS_RESIZE_SAFE = YES

WX_SESSION_SMOKE = PASS

MACOS_SESSION_SMOKE = PASS

SAFE_TO_USE_GUI_SESSION_CONTINUE = YES
