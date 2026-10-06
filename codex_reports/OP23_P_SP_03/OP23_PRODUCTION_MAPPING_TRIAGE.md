# OP23 / P.SP.03 — Production Mapping Triage

Этап: triage 627 GAP `OPEN_PRODUCTION_MAPPING`. Production code, rules engine, validator, tests, GUI, OP22 и FINAL_DELIVERY_* не изменялись.

## Source limitation

- Физический `ОП_23.pdf` в checkout отсутствует.
- OP23 XSD отсутствует.
- Официальные snapshots классификаторов отсутствуют.
- Использованы только captured `source_text/source_refs`, подтверждённые локальные `structures/*.yaml`, OP23 production metadata и фактически существующие capability общего rules engine.

## Итог

| Статус | Количество |
|---|---:|
| `READY_TO_IMPLEMENT` | 0 |
| `ALREADY_IMPLEMENTED_BUT_UNWIRED` | 608 |
| `ALREADY_IMPLEMENTED_AND_WIRED_BUT_UNPROVEN` | 0 |
| `NEEDS_SOURCE_REVERIFY` | 18 |
| `NEEDS_STRUCTURE` | 1 |
| `NEEDS_CLASSIFIER` | 0 |
| `NEEDS_EXTERNAL_REGISTRY` | 0 |
| **TOTAL** | **627** |

Арифметика: **PASS** — сумма triage-статусов равна 627.

## Ключевой вывод

Безопасный локальный implementation pool: **608** требований. Для них нормативное условие captured локально, нужные QName присутствуют в подтверждённых StructureDefinition, а требуемые примитивы общего rules engine уже существуют. OP23 mapping пока не подключён.

`NEEDS_SOURCE_REVERIFY`: **18** требований с конфликтом `ipcdo:IPStatusDetails` vs локальный `ipcdo:IPEntityStatusDetails`.
`NEEDS_STRUCTURE`: **1** требование — `P.SP.03.MSG.025.REQ.006`, где `csdo:DocBinaryText` отсутствует в локальной `R.IP.SP.03.007`.

Проверка ошибочной переклассификации external/classifier внутри 627: strong classifier/external dependency случаев не осталось; поэтому `NEEDS_CLASSIFIER=0`, `NEEDS_EXTERNAL_REGISTRY=0` в этом triage. Исходные 44 + 39 external GAP не изменялись.

## Engine capability evidence

Текущий rules engine содержит `presence`, `cardinality`, `fixed_value`, `selection_cardinality`, `conditional_presence`, `conditional_fixed_value`, `for_each`, selector `where`, ordinal `position`, recursive `all/any/not/count`, `comparison`, `cross_instance_comparison`, typed datetime comparison и aggregate comparison.

Targeted regression: `PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py eaeu_xml/tests/test_repeatable_xml_alignment.py` → **71 passed, 5 subtests passed**.

### Наиболее частые capability в 627 требованиях

| Capability | Требований |
|---|---:|
| `presence/cardinality` | 471 |
| `conditional_rule/where` | 348 |
| `fixed_value/comparison` | 237 |
| `selection_cardinality` | 213 |
| `disjunction/condition.any` | 184 |
| `for_each/qname_selector` | 73 |
| `cross_instance_comparison` | 56 |
| `typed_datetime_comparison` | 16 |
| `position/ordinal_selector` | 2 |
| `aggregate_comparison` | 1 |

## Safe implementation batches

Эти batches относятся только к `ALREADY_IMPLEMENTED_BUT_UNWIRED`; строки `NEEDS_*` в них не входят.

| Batch | Количество | Назначение |
|---|---:|---|
| `B1_SIMPLE_PRESENCE_AND_COMPARISON` | 162 | Простые presence/fixed value/comparison правила. |
| `B2_REPEATED_AND_CONDITIONAL` | 214 | Повторяемые контексты, `for_each`, `where`, условные правила и disjunction. |
| `B3_POSITIONAL_AND_CARDINALITY` | 159 | Ordinal/position и cardinality после отбора. |
| `B4_CROSS_INSTANCE_DATE_AGGREGATE` | 73 | Cross-instance equality/comparison, typed dates и aggregate comparison. |
| **TOTAL SAFE** | **608** | |

## Не реализовывать до reverify

- 18 требований: captured QName `ipcdo:IPStatusDetails` расходится с подтверждённым локальным QName `ipcdo:IPEntityStatusDetails`.
- 1 требование: `P.SP.03.MSG.025.REQ.006` ссылается на `csdo:DocBinaryText`, которого нет в локальной `R.IP.SP.03.007`; нужен XSD/повторная сверка структуры.

## Triage semantics

- `ALREADY_IMPLEMENTED_BUT_UNWIRED`: capability общего rules engine уже существует и протестирована; OP23 production rule отсутствует.
- `ALREADY_IMPLEMENTED_AND_WIRED_BUT_UNPROVEN`: не найдено — OP23 `structured_rules/correlation_rules/fixed_values/field_usage` пусты во всех 21 rule-файлах, а полного совпадения бизнес-требования с автоматически вызываемой структурной проверкой не доказано.
- `READY_TO_IMPLEMENT`: 0 — для безопасных строк более точен специальный статус `ALREADY_IMPLEMENTED_BUT_UNWIRED` по правилу задания.

## Files

- `OP23_PRODUCTION_MAPPING_TRIAGE.csv` — 627 строк, одна строка на один исходный production-mapping GAP.
- `OP23_PRODUCTION_MAPPING_TRIAGE.md` — сводка triage, capability и безопасные implementation batches.
