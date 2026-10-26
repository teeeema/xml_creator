# Решения по объединению и интеграции: ОП 22 (P.SP.02) и ОП 26 (P.MM.01)

## 1. Контекст и цели интеграции

Интеграция направлена на объединение функционала ОП 22 (восстановление карточек сведений о поле в GUI, 4 контрольных кода вида документа `07220`, `07320`, `07360`, `07365`, валидатор правил и классификатор `P.CLS.027`) с наработками этапов 1–3 ОП 26 (версия 1.3.0 в изолированном каталоге draft, строгий gate готовности `promotion_allowed: false`, сохранение активной версии 1.1.0, 41 сообщение и 518 тестов атомарных правил).

## 2. Анализ конфликтующих компонентов

### 2.1. Универсальный движок: `eaeu_xml/src/eaeu_xml/process_packages/body.py`

#### Исходная коллизия
1. **Требование ОП 22**:
   В сквозных тестах `test_msg004_end_to_end.py`, `test_msg005_end_to_end.py`, `test_msg027_end_to_end.py` и `test_msg001_structured_rules.py` проверяется утверждение `assert validation.is_complete`.
   В тестовом режиме (`GenerationMode.TEST`) структура ОП 22 содержит нормативные плейсхолдеры базовой версии модели `vX.X.X`, что порождает предупреждение `UNRESOLVED_NAMESPACE_VERSION` (`severity=WARNING`). При этом все 24 исполняемых структурных правила сообщения успешно проходят со статусом `RuleStatus.PASS`. Соответственно, ОП 22 ожидает, что `is_complete` вернёт `True`.

2. **Требование ОП 26**:
   В `test_v130_runtime.py` для 41 сообщения черновой версии 1.3.0 проверяется `self.assertFalse(validation.is_complete)`. Черновые структуры 1.3.0 не имеют официальных утверждённых XSD и namespace (`promotion_allowed: false`), поэтому их валидация не может считаться полной (`is_complete == False`).

3. **Архитектурное ограничение**:
   Тест `eaeu_xml/tests/test_process_packages.py::test_engine_has_no_specific_process_hardcode` запрещает наличие строк `"P.MM.01"` и `"R.007"` внутри `src/eaeu_xml`.
   Предыдущая попытка решить конфликт прямым сравнением `str(r.rule_id).startswith("P.MM.01")` нарушала этот инвариант.

#### Принятое семантическое решение
- В класс `BodyValidationResult` добавлено явное поле `complete: bool | None = None`.
- Свойство `is_complete` сначала проверяет `if self.complete is not None: return self.complete`.
- Метод `validate_body()` вычисляет признак полноты на основе **универсального контракта структуры**:
  ```python
  is_complete = not any(issue.severity == IssueSeverity.ERROR for issue in issues)
  if "DRAFT" in getattr(structure_definition, "status", ""):
      is_complete = False
  elif any(getattr(item, "status", None) not in {RuleStatus.PASS} for item in rule_evaluations):
      is_complete = False
  return BodyValidationResult(tuple(issues), rule_evaluations, complete=is_complete)
  ```
- **Почему это архитектурно корректно**:
  1. Черновые структуры ОП 26 v1.3.0 имеют статус `status: "DRAFT_MODEL_NAMESPACE_UNRESOLVED"`. Для них `is_complete` детерминированно равен `False`, выполняя инвариант блокировки незрелых черновиков.
  2. Утверждённые структуры (включая ОП 22 со статусом `"NEEDS_XSD"`) при успешном прохождении всех правил возвращают `is_complete == True`.
  3. В коде движка отсутствует какой-либо хардкод конкретных процессов (`"P.MM.01"`, `"P.SP.02"` и др.).
  4. Тест `test_engine_has_no_specific_process_hardcode` проходит со 100% успехом.

### 2.2. Уровень представления: `gui_qt/view_model.py` и `field_info.py`

#### Требования ОП 22
- Отображение карточки реквизита: название, описание, иерархия, тип данных, кратность, ограничения с человекочитаемыми пояснениями (`\d{5}` -> «Ровно 5 цифр»), источники и подсказки.
- Отображение контрольных кодов документов: MSG.001 (`07220`), MSG.004 (`07320`), MSG.005 (`07360`), MSG.027 (`07365`).

#### Решение
- В кодовой базе сохранены компоненты `build_field_details()` в `field_info.py` и расширенная модель `GuiViewModel`.
- Все 25 тестов интерфейса (`test_op22_visual_engine.py`, `test_presentation_text_sanitizer.py`, `test_gui_qt_view_model.py`, `test_examples.py`) выполняются со 100% успехом.
- Выбор сообщений ОП 26 (`P.MM.01.MSG.001` — 401 поле) и ОП 22 (`P.SP.02.MSG.001` — 256 полей) функционирует корректно.

### 2.3. Изоляция версий ОП 26: `versions/1.3.0/`

#### Решение
- Версия 1.3.0 сохранена в изолированной директории `P.MM.01_OP_26/versions/1.3.0/`.
- Файл `migration_status.json` сохраняет строгие флаги:
  - `"promotion_allowed": false`
  - `"status": "DRAFT_NOT_READY"`
  - `"active_version": "1.1.0"`
- Базовая активная версия ОП 26 остаётся 1.1.0. Все 104 теста `P.MM.01_OP_26/tests/` выполняются успешно.
