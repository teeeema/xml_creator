# Этап 3 — фактическая проверка

Завершение: 26.10.2026. Python 3.13; pytest; Qt/PySide6 в отдельном offscreen процессе. Данные NSI получены 23.10.2026 и остаются датированными снимками этой даты, не заявлением об актуальности навсегда.

## Последние прогоны

```sh
PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q \
 P.MM.01_OP_26/tests/test_v130_stage3.py \
 P.MM.01_OP_26/tests/test_v130_runtime.py \
 eaeu_xml/tests/test_xml_value_context.py \
 eaeu_xml/tests/test_op26_v130_source_catalog.py \
 --junitxml=codex_reports/OP26_P_MM_01/V130_STAGE3/verification/focused.xml
```

**12 failed, 33 passed, 1219 subtests passed**, 1.89 s. `verification/final_snapshot/focused.log/xml`. Каждый из 518 compiled atoms проверяется положительным значением и отрицательной мутацией фактического XML через существующий provider; отдельно проверены 41 roundtrip, неверные UUID/dateTime/QName/order/cardinality, conditional activation, repeated contexts, classifier lookup и readiness gate. Это внутренний компонентный TEST proof, не official XSD или application E2E новой редакции.

```sh
PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q \
 --ignore=eaeu_xml/tests/test_validation_page_qml.py \
 --ignore=eaeu_xml/tests/test_gui_qt_view_model.py \
 --junitxml=codex_reports/OP26_P_MM_01/V130_STAGE3/verification/regression.xml
```

**31 failed, 725 passed, 2417 subtests passed**, 33.08 s. `verification/final_snapshot/regression.log/xml`. Собраны все доступные backend-тесты корня, включая новые параллельные тесты OP22 и shared presentation. Это **FAIL**, не общий PASS. Нельзя утверждать отсутствие всех регрессий или относить все отказы к одному автору без независимой изоляции изменений.

Оставшиеся группы отказов: примеры/placeholder значения; отсутствующий generate_required_data и sanitization stale draft; проекция REQUIRED/FIXED policy в формы OP23/legacy OP26; ожидание is_complete=true при предупреждениях unresolved namespace. Последняя группа не является основанием ослаблять нормативную полноту ради зелёного теста. Полный перечень testcase/message: `verification/regression_failure_inventory.json`; GAP `REGRESSION-SHARED-TREE`.

```sh
PYTHONPATH=eaeu_xml/src QT_QPA_PLATFORM=offscreen python3.13 -m pytest -q \
 eaeu_xml/tests/test_validation_page_qml.py \
 eaeu_xml/tests/test_gui_qt_view_model.py \
 --junitxml=codex_reports/OP26_P_MM_01/V130_STAGE3/verification/qt.xml
```

**14 passed**, 1.20 s. `verification/final_snapshot/qt.log/xml`. Проверено отображение 1.1.0 и недоступной 1.3.0 без смены engine/catalog. Объединённый Qt/backend процесс не повторялся: прежний baseline имел Qt abort; отдельный успех не доказывает устранения причины совместного abort.

## Регрессии, найденные при завершении

`verification/completion_baseline.log`: **12 failed, 33 passed, 1219 subtests passed** до исправления is_complete. В существующем dirty body.py была снята проверка issues; сообщения без специальных business rules считались complete при unresolved namespace. Попытка восстановить conservative completeness guard была перезаписана параллельной работой. Семантика флага требует согласования; assertions не ослаблялись. Последний зафиксированный focused-прогон содержит 12 SUBFAILED по этому ожиданию. Совместимый `_values_from_element`, добавленный параллельно, сохранён.

`verification/cardinality_reproduction.json`: реально исполненный код исходного HEAD принимал Groups=[None] при minOccurs=1, хотя узел не сериализовался; новый код отклоняет MIN_OCCURS. Тесты различают отсутствующий list slot, пустой список, явный пустой элемент и контейнер. Это изменение некорректных входов общего движка, а не декларация полного сохранения всех прежних ошибок поведения.

Промежуточные логи rules_initial/second/third/fourth/fifth, classifiers_initial/second, additional_local и parallel_transient сохранены. Во время этапа появились параллельные shared model/form/policy/rules изменения и новые OP22 тесты. Зафиксированы временные ошибки порядка dataclass полей, signature pattern и shadowing contexts; совместимость field_constraint восстановлена без удаления новых ветвей. Прежние 433-pass прогоны относятся к меньшему/другому состоянию дерева и не заменяют итоговый FAIL 13/731.

## Артефакты и границы

- `verification/xml/`, `xml_results.json`: по одному synthetic TEST и invalid UUID XML для 41 MSG, SHA-256 и diagnostics. is_complete записан фактически; unresolved diagnostics не считаются normative completeness; STRICT отказ; invalid XML отклонён.
- `test_v130_stage3.py`: полнота 8 официальных snapshots, raw page hashes/count/unique IDs, positive/negative membership, invalid snapshot rejection, nested uniqueness/positional scope, source Unicode preservation, draft metadata isolation.
- `verification/final_audit.json`: 481/710/47/41 CSV accounted; 167 прежних constraints сохранены; 286 исходных контрольных файлов проверены, 284 неизменны, два ожидаемых изменения — именно v130 test harness. Legacy нормативные каталоги и отчёты этапов 1/2 не переписаны.
- `verification/gui_editions.png`: фактически отрендеренная Qt information page; offscreen preview не является ручной production-сессией.
- Official XSD, полный нормативный Level A, новая application/session correlation/E2E — **NOT_EXECUTED / NOT_PROVEN**.

Условие закрытия общей регрессии: согласовать shared APIs/политики и тестовые ожидания с источниками, доказать причины отказов, затем получить полный свежий прогон без failed/errors на зафиксированном состоянии дерева. Тесты не отключались ради PASS.

Снимки выполненных прогонов заморожены в final_snapshot с manifest/hash. Позднейшие изменения общего движка не превращают этот FAIL в PASS. Аудит итоговых CSV/источников проверяет учёт и происхождение, но не исправность всего дерева.
