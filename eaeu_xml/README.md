# eaeu_xml

Независимый универсальный движок XML/SOAP ЕАЭС по Решению Коллегии ЕЭК №5.

Реализованы namespaces, логические адреса, технологические идентификаторы, Action, Header policy, Integration, сигналы, SOAP Fault, корреляция, шесть шаблонов транзакций и XML serialization с интерфейсом Body. Нормативный источник хранится локально в `./15kr0005.doc`.

Конкретные общие процессы подключаются как внешние нормативные `ProcessPackage`. Движок не знает заранее, какие процессы существуют, и никогда не сканирует родительские каталоги. Путь всегда передаёт вызывающий код:

```python
from pathlib import Path
from eaeu_xml import EaeuXmlEngine

engine = EaeuXmlEngine.load_process(Path("/path/to/process-package"))
transaction = engine.get_transaction("P.XX.01.TRN.001")
message = engine.get_message("P.XX.01.MSG.001")
structure = engine.get_structure(message.message_code)
action = engine.build_application_action(transaction.transaction_code, message.message_code)
```

Manifests имеют расширение `.yaml` и используют JSON-compatible YAML 1.2, поэтому движок остаётся без сторонней runtime-зависимости от YAML-парсера.

Проект не зависит от соседнего старого приложения. P.MM.01-specific данные, GUI, БД и реальный transport не входят в ядро.

Запуск тестов:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Требуется только Python 3.11+; core runtime-зависимостей от сторонних пакетов нет.

## GUI

wxPython устанавливается как необязательная зависимость и не требуется для
движка или application facade:

```bash
pip install -e ".[gui]"
```

Запуск с явным корнем внешних процессов:

```bash
python -m eaeu_xml.gui /path/to/processes-root
```

или после editable installation:

```bash
eaeu-xml-gui /path/to/processes-root
```

Если путь не передан, GUI предложит выбрать каталог. Затем нужно выбрать общий
процесс, транзакцию и сообщение, заполнить форму вручную или тестовыми данными,
выполнить проверку, сформировать XML и при необходимости сохранить его.

Основное окно разделено на вкладки «Заполнение данных» и «XML». У каждого поля
есть пример, tooltip и окно `ⓘ` с datatype, XML QName/path, cardinality,
описанием, classifier/fixed/source metadata. В обычных заголовках показываются
человекочитаемые названия; технические QName остаются в справке. Корень
процессов, TEST/STRICT validation mode и seed доступны через «Настройки…».

Typed statuses отображаются как отдельные success, warning и blocked-состояния
с объяснением и следующим действием. Окно «Проблемы процесса» получает через
facade агрегированные unresolved-version, normative-conflict, external
classifier/source issues и не читает package manifests напрямую.

Если конкретная версия структуры или импортированной модели не определена, TEST
mode сохраняет нормативные `Y.Y.Y`/`X.X.X` прямо в namespaces и помечает
результат `VERSION_PLACEHOLDER_TEST`. Такие токены никогда не заменяются на
предполагаемые версии; STRICT mode блокирует формирование до подтверждённой
конфигурации.

GUI является только presentation layer: он использует `EaeuXmlApplication`,
не читает YAML, не реализует правила Решения №5 и не сериализует XML.

### Черновики

«Файл → Сохранить черновик» сохраняет введённые значения и контекст сообщения
в локальный JSON-файл `*.eaeudraft.json`. Черновик не является XML и не
содержит копию нормативных определений. Запись выполняется атомарно; после
открытия значения повторно сопоставляются с актуальной формой и проходят
текущую проверку. Несопоставленные поля сохраняются в исходном документе и
показываются как предупреждение.

Автосохранение включено по умолчанию с задержкой 3 секунды. Каталог и задержка
задаются в «Настройки…»; стандартный каталог — `~/EAEU_XML_Drafts`. После
аварийного завершения GUI предлагает восстановить autosave. Черновики разрешены
и для заблокированных сообщений, но не снимают блокировку формирования XML.
