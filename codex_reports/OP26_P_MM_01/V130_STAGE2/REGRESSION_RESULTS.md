# Stage 2 — фактически выполненная проверка

Дата: 2026-10-23. Ветка `feature/op26-v1.3.0`, HEAD `da0af7459edae6aa8da6b56de585afb8c658002e`. Результаты Stage 1 не включены в новые счётчики.

## Финальные прогоны

```sh
PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q \
  P.MM.01_OP_26/tests/test_v130_runtime.py \
  eaeu_xml/tests/test_xml_value_context.py \
  --junitxml=codex_reports/OP26_P_MM_01/V130_STAGE2/verification/focused.xml
```

**16 passed, 515 subtests passed** (`verification/focused.log`, `focused.xml`). Проверены дерево всех 710 строк, 41 TEST Body roundtrip, положительные/отрицательные случаи для всех 167 compiled constraints, реальные XML-мутации, missing EDocId, неверные UUID/dateTime/header cardinality, QName/order, binary/arbitrary XML alternatives, условная обязательность, пустые/отсутствующие поля, вложенные повторения и атрибуты. Есть проверка сохранения блокировки actual engine 1.3.0.

```sh
PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q \
  eaeu_xml/tests P.MM.01_OP_26/tests P.SP.02_OP_22/tests \
  P.SP.03_OP_23/tests P.MM.06_OP_32/tests P.DS.01_OP_49/tests \
  --ignore=eaeu_xml/tests/test_validation_page_qml.py \
  --ignore=eaeu_xml/tests/test_gui_qt_view_model.py \
  --junitxml=codex_reports/OP26_P_MM_01/V130_STAGE2/verification/regression.xml
```

**424 passed, 1667 subtests passed**, 10.76 s (`verification/regression.log`, `regression.xml`). Это полный прогон указанной области core/application/OP26/22/23/32/49 без двух Qt-файлов, а не утверждение о запуске каждого теста всего репозитория. Включены фактические legacy engine/registry/default/explicit version, исходные каталоги и защита от смешения/активации версий.

```sh
PYTHONPATH=eaeu_xml/src QT_QPA_PLATFORM=offscreen python3.13 -m pytest -q \
  eaeu_xml/tests/test_validation_page_qml.py \
  eaeu_xml/tests/test_gui_qt_view_model.py \
  --junitxml=codex_reports/OP26_P_MM_01/V130_STAGE2/verification/qt.xml
```

**13 passed**, 0.70 s (`verification/qt.log`, `qt.xml`). Combined GUI+backend: **NOT_RERUN**; Stage 1 зафиксировал аварийное завершение Qt в объединённом baseline-запуске. Этот дефект окружения/жизненного цикла Qt не объявляется исправленным отдельным успешным прогоном. Отдельный GUI manual/live session: NOT_EXECUTED; новая редакция не активирована.

После обновления README/passport отдельно перепроверены source integrity/version selection: **25 passed, 19 subtests passed** (`verification/readiness_final.log`); это новый запуск Stage 2, не копия результата Stage 1.

## Дополнительные доказательства

- `verification/pre_fix_reproduction.json`: прежний код из HEAD сворачивал `[{},{Name:later}]` в child `[later]`; исправленный сохраняет `[null,later]` и обе parent-позиции.
- `verification/compiler_determinism.json`: повторены оба компилятора, все 40 файлов структур/правил имеют идентичные хэши.
- `verification/preservation_result.json`: 151 контрольный файл (legacy OP26 и Stage 1) не изменён относительно снимка начала Stage 2.
- `verification/pdf_message_inventory.json`: независимая сверка страниц PDF — 34/13/6/41; SHA-256 PDF сохранён.
- `verification/xml_results.json` и `verification/xml/`: 41 синтетический положительный TEST Body и 41 XML с неверным UUID, хэши и диагностика. Все положительные имеют `is_complete=false`, STRICT отказ; все отрицательные отклонены. Это не официальные примеры и не XSD PASS.
- `verification/stage2_counts.json`: счётчики получены из фактических каталогов; нет пропущенных строк в 710/481/47/41 CSV.
- `verification/graphify_update.log`: выполнен `graphify update .`, AST-only, без LLM/API; финальный размер указан в логе. Семантические community labels не обновлялись через LLM.
- `verification/final_git_state.json`, `git_status.txt`, `working_tree_files.txt`: состояние dirty worktree и refs; commit/push не выполнялись.
- `git diff --check`: завершён с кодом 0. Изменения общих модулей и fixtures просмотрены; исходный dirty diff этапа 1 сохранён отдельно.

## Найденные и устранённые ошибки при проверке

Промежуточные неуспешные логи сохранены, не выдаются за финальный успех: `body_initial.log`, `v130_initial.log`, `conditional_initial.log`, `expanded_rules_initial.log`, `related.log`, `related2.log`.

Исправлены потеря missing slots при flatten, нарушение родительских осей вложенных списков, scalar broadcast, смешение простого значения с группой из-за одних атрибутов, неверная форма синтетических attribute samples, допуск явно пустого элемента `FORBIDDEN`, отсутствие roundtrip-проверки exact QName/order и ложная полнота при deferred rules. Ошибки синтетических regex/conditional fixtures также устранены.

Три OP49 positive fixture builders теперь явно формируют attribute arrays в форме repeated parents через TestDataGenerator; прежнее скалярное значение полагалось на недопустимое broadcasting. Assertions/negative expectations не ослаблялись; нормативные файлы OP49 не менялись. Исходная Stage 1 проверка `structured_rules == []` заменена проверкой трассировки derived rules к сохранённым исходным строкам, поскольку Stage 2 именно добавляет исполняемые правила. Проверка 481 строк, 47 CLS, hashes и readiness сохранена.

## Не выполнено

Официальная XSD-валидация (нет подтверждённого набора), полный normative Level A (333 строки не завершены), новый production engine E2E/корреляция и реальные внешние справочники/реестры — **NOT_EXECUTED / SOURCE_BLOCKED**. Крупное число успешных unit/subtests не закрывает эти условия.
