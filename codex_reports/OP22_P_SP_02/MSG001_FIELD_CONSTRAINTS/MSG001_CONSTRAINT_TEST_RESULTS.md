# Результаты проверки

## Targeted suite

Команда:

`python3.13 -m pytest -q eaeu_xml/tests/test_gui_qt_view_model.py`

Результат:

`22 passed in 0.74s`

Проверено:

- `IPDocKindCode`: исходный `\d{5}` + разрешённое пояснение `Ровно 5 цифр`;
- `IPDocKindName`: 1 / 500 символов;
- `StatusCode`: 1 / 3 символа;
- `StatusCode/@codeListId`: 1 / 20 символов;
- `ApplicationReceiptDate`: ISO 8601;
- GROUP/container без явного ограничения: секция скрыта;
- сложный `TrademarkApplicationId` regex сохраняется без придуманного пояснения;
- Unicode noncharacter sanitation сохраняется только в presentation text;
- GROUP selection сохраняется;
- `ScrollView`, `Text.Wrap`, `Text.PlainText` сохраняются;
- `P.SP.02.MSG.002` остаётся на legacy-поведении;
- старые debug markers не попадают в карточку.

## Final checks

- `git diff --check` — PASS.
- `graphify update .` — PASS: `graph.json` и `GRAPH_REPORT.md` обновлены; HTML-визуализация оставлена прежней, потому что агрегированный граф содержит 5184 узла при лимите визуализации 5000.
- `python3.13 -m pytest -q eaeu_xml/tests/test_validation_page_qml.py` — `2 passed in 0.83s`; `Main.qml` успешно загружается через `QQmlApplicationEngine`.

Попытка запустить оба GUI test-файла одной командой в одном Python-процессе завершилась `Fatal Python error: Aborted` в `gui_qt/fonts.py`. Причина воспроизводится из существующего test lifecycle: `test_gui_qt_view_model.py` создаёт `QCoreApplication`, после чего `test_validation_page_qml.py` получает этот экземпляр через `QGuiApplication.instance()` и обращается к `QFontDatabase` без настоящего `QGuiApplication`. Это отдельная проблема изоляции тестов; по отдельности оба набора проходят. В рамках текущего scope она не исправлялась.
