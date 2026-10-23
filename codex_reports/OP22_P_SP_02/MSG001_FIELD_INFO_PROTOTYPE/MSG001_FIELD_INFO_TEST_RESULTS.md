# P.SP.02.MSG.001 — результаты проверки прототипа «Сведения о поле»

## Область проверки

Трассировка: **ОП №22 → P.SP.02 → P.SP.02.TRN.001 → P.SP.02.MSG.001 → R.IP.SP.02.002**.

## Выполненные проверки

### GUI/ViewModel

Команда:

```text
python3.13 -m pytest -q eaeu_xml/tests/test_gui_qt_view_model.py
```

Результат после исправления имени группового контейнера:

```text
22 passed in 0.64s
```

Первый запуск выявил одну регрессию прототипа: общий `FieldView.display_name` удалял не только технический QName-суффикс, но и семантические скобки «(ходатайство, жалоба)». Исправление сделано локально в прототипе; повторный запуск — PASS.

### OP22 catalog + application facade smoke

Команда:

```text
python3.13 -m pytest -q P.SP.02_OP_22/tests/test_psp02_catalog.py eaeu_xml/tests/test_application_facade.py
```

Результат:

```text
22 passed in 0.17s
```

### Проверки завершения

Команда:

```text
git diff --check
```

Результат: **PASS**, вывод отсутствует.

Проверка соответствия GUI-полей каноническим `presentation_fields` структуры `R.IP.SP.02.002`:

```text
GUI_FIELDS=404
STRUCTURE_PRESENTATION_FIELDS=404
MISSING_STRUCTURE_METADATA=0
UNREADABLE_CORE_METADATA=0
PROTOTYPE_ENABLED=YES
```

Команда:

```text
graphify update .
```

Результат: **PASS**, exit code 0. Обновлены `graphify-out/graph.json` и `graphify-out/GRAPH_REPORT.md`; итоговый граф содержит 39745 узлов, 50025 рёбер и 5207 сообществ. `graph.html` генератор оставил прежним, потому что агрегированное представление содержит 5207 узлов при лимите визуализации 5000.

Дополнительная попытка запустить те же тесты через системный `python3` (Python 3.12) не дошла до тестов: в этом интерпретаторе отсутствует модуль `pytest`. После проверки окружения тесты повторены через `python3.13`, где `pytest 9.1.1` установлен; результаты выше являются актуальными успешными результатами.

## Граница доказательства

Полный test suite в рамках этой задачи не запускался. Проверка покрывает целевой GUI/ViewModel, сохранение legacy-поведения для `P.SP.02.MSG.002`, OP22 catalog и application facade smoke.
