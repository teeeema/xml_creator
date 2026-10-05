# Финальный аудит P.MM.01 / ОП_26

- **Процесс**: P.MM.01 (Регистрация лекарственных средств)
- **Статус**: COMPLETE
- **Вердикт**: READY
- **Сообщений всего**: 28 (существующих: 28, нормативно отсутствующих: 0)

## Результаты тестовых наборов

| Набор | Результат |
|:---|:---|
| OP26 regression (`pytest P.MM.01_OP_26/tests`) | **87 passed, 83 subtests passed** |
| Engine & Validator regression | **40 passed, 5 subtests passed** |
| Full eaeu_xml suite | **291 passed, 43 skipped, 1052 subtests passed** |
| Package validation | **0 errors** |

## Распределение статусов

| Статус | Кол-во |
|:---|:---:|
| `PARTIAL_EXTERNAL` | 16 |
| `NO_SEPARATE_RULE_TABLE` | 12 |

## Агрегированные метрики требований

| Метрика | Значение |
|:---|:---:|
| Всего нормативных требований | **201** |
| FULLY_MAPPABLE | 165 |
| SAFE_PARTIAL | 0 |
| EXTERNAL | 36 |
| AMBIGUOUS | 0 |
| ENGINE_UNSUPPORTED | 0 |
| SOURCE_CONFLICT | 0 |
| **Исполняемых итого** | **165** |
| **Неразрешенных итого** | **36** |
| Записей в MISSING_DATA.csv | **36** |

## Сгенерированные артефакты

| Артефакт | Описание |
|:---|:---|
| `codex_reports/OP26_FINAL_AUDIT.md` | Этот документ — полный аудит P.MM.01 / ОП_26 |
| `codex_reports/OP26_FINAL_MESSAGE_MATRIX.csv` | Матрица сообщений (28 строк) |
| `codex_reports/OP26_MISSING_DATA.csv` | Все неразрешённые требования (36 строк) |
| `codex_reports/OP26_EXTERNAL_DOCUMENTATION_GAPS.md` | Документ внешних пробелов |

## QNAME COMPLETION AUDIT

Проверка полноты `xml_owner` / `xml_qname` / `xml_path` во всех 36 строках `OP26_MISSING_DATA.csv`.

### Итоговые счётчики

| Метрика | Значение |
| :--- | :---: |
| TOTAL_MISSING_DATA_ROWS | **36** |
| QNAME_RESOLVED | **36** |
| QNAME_NOT_APPLICABLE | **0** |
| QNAME_STILL_UNRESOLVED | **0** |
| OWNER_STILL_UNRESOLVED | **0** |
| PATH_STILL_UNRESOLVED | **0** |

**Необъяснённых unresolved: 0** ✓

## Детальный аудит сообщений

Всего в процессе 28 сообщений:
- 16 сообщений содержат отдельные таблицы требований (201 требование суммарно);
- 12 сообщений являются служебными квитанциями или уведомлениями без отдельных таблиц правил в Решении №68.

Все 87 тестов пакета проходят успешно.
