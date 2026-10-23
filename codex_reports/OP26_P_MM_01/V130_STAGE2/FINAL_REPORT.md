# ОП 26 / P.MM.01 1.3.0 — этап 2

Дата: 2026-10-23. Итог: **Частично подтверждено**. Реализованы частичные исполняемые структуры и правила; полная нормативная готовность не достигнута. `DRAFT_NOT_READY`, `promotion_allowed=false`, `active_in_application=false` сохранены.

## Доказанный результат

| Показатель | Результат |
|---|---|
| Каталоги | 28 PRC, 84 OPR, 28 TRN, 41 MSG, 8 участников |
| Расхождение 34/41 | Первый регламент 34, второй 13, общих 6: объединение 41 |
| Структуры | 7 частичных исполняемых деревьев; **0 полностью завершённых** |
| Реквизиты | Все 710 строк сопоставлены без пропусков, orphan parents и duplicate paths |
| Подтверждение реквизитов | 119 source interpretations VERIFIED: 117 unqualified attributes + 2 arbitrary XML; 591 NEEDS_EXTERNAL_SOURCE по effective model namespace |
| Требования | 481 исходная строка сохранена; всего нормативных атомов UNKNOWN |
| Исполняемые ограничения | 167 локальных предикатов: 63 REQUIRED, 87 FORBIDDEN, 6 FIXED, 6 ENUM, 5 AT_LEAST_ONE |
| Покрытие строк | 148 IMPLEMENTED (30.77%), 2 PARTIAL, 87 SOURCE_BLOCKED, 244 NOT_IMPLEMENTED |
| Внутренний XML | 41 TEST Body serialize/parse/extract/revalidate успешно; **0 полностью проверенных нормативных Level A MSG** |
| Официальный XSD | **0 MSG**, NOT_EXECUTED |
| Полный production engine E2E | **0 MSG**, загрузка новой редакции блокируется |
| Классификаторы | 47 ссылок, 0 новых подтверждённых официальных датасетов |
| Фокусные тесты | 16 passed / 515 subtests passed |
| Регрессия core/application/OP26/22/23/32/49 | 424 passed / 1667 subtests passed |
| Qt отдельно | 13 passed; объединённый запуск NOT_RERUN |
| Legacy/Stage1 сохранность | 151 контрольный файл без изменений |

**Подтверждено:** состав MSG в доступной редакции 140/77, каталожные ссылки, исходная иерархия 710 строк и фактические компонентные тесты. **Опровергнуто:** 34 как полный список MSG обоих регламентов; 481 как количество реализованных атомарных правил; готовность новой редакции из одного успешного roundtrip. **Частично подтверждено:** исполняемая Level A реализация. **Недостаточно данных:** эффективные версии моделей/официальные XSD, датасеты/внешние состояния и полнота последующей истории изменений.

## ROOT_CAUSE

Предыдущий этап импортировал нормативные таблицы и каталоги, но не построил исполняемые поля/предикаты. Кроме того, общий Body provider терял позицию отсутствующего дочернего значения при flatten списков объектов, не обеспечивал согласованную обработку вложенных repeated axes, допускал scalar broadcast и не давал проверки обратного exact-QName извлечения. TestDataGenerator воспринимал простой элемент с одними атрибутами как пустую группу. Невыполненные правила могли не влиять на признак полноты. Отдельная самопроверка обнаружила, что `FORBIDDEN` принимал явный None, хотя сериализация создаёт пустой элемент.

Другая часть недостающего поведения обусловлена не дефектом Python, а незавершённой интерпретацией 244 локальных строк и отсутствующими нормативными/внешними зависимостями. Эти две причины явно разделены; все GAP нельзя приписать недоступности серверов.

## CHANGED_FILES

Полный перечень файлов, изменённых/добавленных этапом 2: [changed_files.txt](changed_files.txt). Полный Git dirty inventory, включая ранее существовавшую работу: [verification/working_tree_files.txt](verification/working_tree_files.txt); точный статус [verification/git_status.txt](verification/git_status.txt). Эти списки различаются намеренно: каталоги PRC/OPR/TRN/ACT, version gate и Stage1 sources уже были dirty до этапа 2.

Изменения этапа 2:

- `P.MM.01_OP_26/versions/1.3.0/tools/compile_structures.py`, семь `structures/*/*.yaml`: детерминированная компиляция сохранённого source_inventory, без повторного импорта и выдуманных effective URI.
- `tools/compile_rules.py`, 33 `message_rules/*.yaml`: derived executable sections с полной трассировкой; исходные business_rules не заменены.
- `eaeu_xml/src/eaeu_xml/process_packages/value_context.py`, `body.py`, `rules_engine.py`: общие родительские контексты, корректные отсутствующие слоты, типы/кратность, точные QName/order при извлечении, incomplete diagnostics и локальные предикаты. Нет `if message_code == ...`.
- `loader.py`: используется прежний canonical parser rules через выделенный `load_rules`, без обхода production readiness.
- `application/services.py`: корректные synthetic simple-content/attribute samples.
- `P.MM.01_OP_26/tests/test_v130_runtime.py`, `v130_runtime_support.py`, `eaeu_xml/tests/test_xml_value_context.py`: реальные компонентные XML positive/negative доказательства. `test_op26_v130_source_catalog.py` сохраняет проверку source integrity при появлении derived rules.
- Три OP49 test fixture builders: форма repeated attributes исправлена без ослабления assertions; нормативные каталоги других ОП не изменены.
- README/passport/CURRENT_STATE/CHANGELOG и отдельные отчёты этапа 2; AST graph обновлён.

## IMPLEMENTATION

### Инвентаризация MSG и связь каталогов

[MSG_INVENTORY_VERIFICATION.md](MSG_INVENTORY_VERIFICATION.md) содержит OLD_1_1_0 → NORMATIVE_1_3_0 → IMPLEMENTED_1_3_0, официальные названия, структуры/версии, PRC/TRN/OPR и дословные роли отправителя/получателя. Независимо прочитаны страницы PDF, а не повторён только импортированный счётчик. Таблица 5 первого регламента (PDF 259–262; Word table_index=130) содержит 34 MSG, таблица 6 второго (381–382; table_index=183) — 13. Дополнительные уникальные семь — .012/.016/.017/.021/.022/.023/.024; общих шесть — .004/.009/.019/.020/.030/.031. Ошибочного объединения разных версий не обнаружено; объединены два регламента одного процесса.

Старый каталог содержит 28 MSG: 27 совпадающих кодов, MSG.003 отсутствует в новых полных перечнях, 14 новых кодов. Совпадение кода не доказывает сохранение прежнего содержания. Официальная история всех возможных последующих поправок после 77 не закрыта и отмечена отдельным GAP; 41 относится к фактически проверенной нормативной базе 140/77.

### Семь деревьев и 710 строк

Дерево восстановлено по позициям ячеек/отступам сохранённой официальной Word-таблицы, включая обозначения `*.n`. Fnnnn — внутренние стабильные номера строк, не нормативные ID. Путь движка root-relative, полный Body path приведён отдельно. QName не выводится из русского названия. Родители и порядок проверены машинно; атрибуты сохранены как атрибуты, arbitrary XML — без выдуманной обёртки. Все строки учтены в [STRUCTURE_FIELD_AUDIT.csv](STRUCTURE_FIELD_AUDIT.csv) и [QNAME_NAMESPACE_AUDIT.csv](QNAME_NAMESPACE_AUDIT.csv).

Пять отраслевых root namespace/версий 1.3.0 указаны источником. R.006/R.007 содержат Y.Y.Y; imports базисной/отраслевой моделей X.X.X/Z.Z.Z. Поэтому 591 эффективный expanded QName вложенных элементов не подтверждён. 119 VERIFIED означает подтверждение интерпретации исходного токена/дерева, а не полноту XSD/типов/бизнес-проверок. Типы/facets берутся только из явного текста. Режим TEST допускает символические URI с предупреждением, STRICT отклоняет. В PDF page locator таблицы не выдаётся за страницу каждой строки: exact Word table_index/row сохранены, row-specific PDF page отдельно не проверена.

Порядок исходной таблицы реализован и проверен, но официальный compositor `sequence/choice/all`, ограничения xs:any/processContents и полная семантика импортированных типов остаются SOURCE_BLOCKED до получения XSD.

### Исполняемые требования

Компилятор распознаёт только замкнутый набор однозначных конструкций источника. Сохраняет MSG, исходный нормативный номер требования (в контексте таблицы), source_row_id, stable atomic ID, пути/предков, условия, diagnostic/error code и source refs. SOURCE_ROW и суффикс A+hash — внутренние ключи, не нормативные REQ. Наследуемые диапазоны MSG.002 (3–87 таблицы 26) и MSG.035 (2–69 таблицы 47) разрешены в правильном регламенте; первичная и наследуемая ссылки сохранены. Составные/неоднозначные фразы не урезаются до удобной части.

167 ограничений включают повторное применение наследуемых локальных предикатов, а не 167 независимых нормативных атомов. CONDITIONAL_REQUIRED реализован условием на сопоставленный QName в том же parent context; обязательность StreetName применяется ко всем соответствующим адресам. AT_LEAST_ONE учитывает XML/binary alternatives; FIXED атрибута pdf проверяется внутри present parent. Остальные классы исследованы: PATTERN/LENGTH и явные numeric facets принадлежат существующей проверке полей; CARDINALITY поддержан структурным валидатором/локальным evaluator, но отдельного compiled атома этого класса в текущих 167 нет. DATE_COMPARISON, сложные CROSS_FIELD/MUTUAL_EXCLUSION/REFERENCE_INTEGRITY/CROSS_MESSAGE и внешние classifier/registry predicates не объявлены реализованными, если строка не может быть однозначно связана и доказана. Для них остаются non-PASS DEFERRED-маркеры.

[BUSINESS_RULES_COVERAGE.csv](BUSINESS_RULES_COVERAGE.csv) учитывает все 481 строки: 148 полностью покрыты локальными предикатами, 2 частично (наследуемые диапазоны), 87 с внешним контекстом, 244 требуют дальнейшей интерпретации/реализации. Не завершены **333 строки**, из них 331 пока не имеют compiled локального предиката. 87 SOURCE_BLOCKED — классификация явно внешнего содержания, а не заявление, что все его локальные части исследованы исчерпывающе.

### Генерация и интеграция

Использован существующий StructuredProcessBodyProvider, canonical loader structures/rules и StructuredRuleEvaluator. В тестовом harness соединены реальные MSG→Structure→Fields→Rules→Body; каталожные PRC/TRN/OPR связи проверены. Нормальный ProcessPackageLoader/EaeuXmlEngine не активирует draft. Это компонентная проверка, не обход gate для пользовательской генерации. SOAP/Decision5 транспорт и адреса/Action не переопределялись; production new-edition correlation/prior-message integrity остаются неисполненными.

Отсутствующие значения сохраняют позиции в repeated parent axes; пользовательский scalar не транслируется на несколько родителей. Явная пустая группа сохраняется, отсутствующая не создаётся. Извлечение сравнивает expanded QName, неизвестные элементы/атрибуты и неправильный порядок отклоняются. `is_complete` не становится true при предупреждениях/неисполненных правилах. TEST `is_valid=true` не равно нормативной полноте. Синтетические тестовые значения не являются официальным датасетом/образцом.

## NORMATIVE_BASIS

**CONFIRMED в границах доступных таблиц:** [Решение 140 от 24.12.2025](https://docs.eaeunion.org/documents/446/10427/) и [Решение 77 от 29.06.2026](https://docs.eaeunion.org/documents/463/10765/); архивированные PDF/Word, исходные SHA-256 и exact source_refs находятся в неизменённом `V130_COMPLETION/sources/`. Это редакция приложений к Решению 122, не самостоятельная придуманная спецификация.

Проверена поправка 77: исключены **P.MM.01.CLS.009/.010**, добавлены **P.MM.01.CLS.028/.029**; 47 ссылок классифицированы в [CLASSIFIER_DEPENDENCIES.csv](CLASSIFIER_DEPENDENCIES.csv). Биндинг к полям делается по буквальному CLS/явному ЕС НСИ коду; неразрешённые связи не угадываются по похожему названию. Дата/версия датасета UNKNOWN; локальный lookup SOURCE_BLOCKED.

**UNKNOWN / BLOCKED_BY_SOURCE:** effective model versions, официальный XSD closure, datasets, externally stateful rules и полный последующий amendment history. [XSD_SOURCE_AUDIT.md](XSD_SOURCE_AUDIT.md) содержит адреса/повторные HTTP/HTTPS попытки и хэши имеющихся источников. TLS/empty reply официальных rseds/eomi не доказывают отсутствия схемы. Уровень A не называется XSD-валидацией уровня B.

## VERIFICATION

Финальные команды/артефакты: [REGRESSION_RESULTS.md](REGRESSION_RESULTS.md), [MESSAGE_TEST_MATRIX.csv](MESSAGE_TEST_MATRIX.csv), [verification/xml_results.json](verification/xml_results.json). 41 синтетический TEST roundtrip принят внутренним компонентом с incomplete diagnostics; 41 отрицательный UUID XML отклонён; каждый из 167 предикатов имеет positive и actual XML negative mutation test. Проверены context/empty/namespace/order/type/cardinality boundaries. Все положительные XML сохраняются с буквальными unresolved URI и не предназначены для внешнего обмена.

Фокус: **16/515**; выбранная полная регрессия core/application/пяти ОП: **424/1667**; Qt отдельно: **13**. Два Qt-файла исключены из backend-прогона; combined Qt NOT_RERUN, зафиксированная на этапе 1 авария не объявляется устранённой. Manual GUI новой редакции и официальный XSD не запускались. Нельзя суммировать пересекающиеся focused/regression как независимые тесты.

Повторная компиляция 40 файлов идентична. 151 legacy/Stage1 файл сохранён по хэшу; это доказательство содержимого выбранных файлов, не математическое доказательство неизменности любого поведения shared code. Общая обработка некорректного scalar broadcast и позиционных данных намеренно исправлена для всех процессов; существующие позитивные legacy generation/correlation/registry tests прошли. Нормативные каталоги 1.1.0 не изменены, 28 MSG и default/explicit selection сохранены.

Git: рабочая ветка `feature/op26-v1.3.0`, HEAD `da0af7459edae6aa8da6b56de585afb8c658002e`. Working tree dirty, включая сохранённую Stage1 работу и новые файлы. Remote main и backup остаются `0c9b8c03cbf9f03cfc6be5c53e043e571d124038`, feature remote — `da0af745...`. Commit/push/reset/restore/clean/rebase не выполнялись. Graphify обновлён AST-only; semantic labels не перегенерировались через API.

## REMAINING_ISSUES

[GAP_REGISTER.csv](GAP_REGISTER.csv) содержит 980 контекстных записей в заданном формате: 591 unresolved QName row + 333 незавершённые requirement rows + 47 datasets + 7 schema closures + amendment-history + application E2E. Это **не число независимых атомарных требований**: одна модельная зависимость блокирует много полей, inherited gaps могут перекрываться.

Для окончательной активации нужны:

1. Авторитетный совместимый XSD/model set: effective URI/версии, все imports/includes, provenance/date/hash, compositor/type/xs:any semantics; закрытие всех 710 реквизитов.
2. Официальные версии/данные 47 CLS и точные привязки, positive/negative lookup; внешние реестры/предыдущие сообщения или подтверждённые контракты/снимки для stateful требований.
3. Завершение 244 локально не реализованных строк, 2 partial ranges и локальных/внешних частей 87 SOURCE_BLOCKED; полное атомарное разложение 481 строк и доказательство каждого применимого predicate.
4. Проверенные input/UI policies и полный existing-engine путь PRC/TRN/MSG/Body/transport/correlation для всех применимых сообщений; отсутствие смешения версий.
5. Официальный XSD positive/negative набор, полная Level A и E2E/GUI регрессия, отдельное разрешение на promotion. До этого readiness false и default 1.1.0 сохраняются.

Работа этапа 2 дала исполняемую основу и проверяемую трассировку, но не завершила полную нормативную реализацию. Ни недоступность внешних источников, ни количество успешных тестов не скрывают оставшуюся локальную работу.
