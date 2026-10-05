# Финальный аудит P.MM.06 / ОП_32

- **Процесс**: P.MM.06 (Регистрация медицинских изделий)
- **Статус**: COMPLETE
- **Вердикт**: READY
- **Сообщений всего**: 24 (существующих: 24, нормативно отсутствующих: 0)

## Результаты тестовых наборов

| Набор | Результат |
|:---|:---|
| OP32 regression (`pytest P.MM.06_OP_32/tests`) | **8 passed** |
| Engine & Validator regression | **40 passed, 5 subtests passed** |
| Full eaeu_xml suite | **291 passed, 43 skipped, 1052 subtests passed** |
| Package validation | **0 errors** |

## Распределение статусов

| Статус | Кол-во |
|:---|:---:|
| `PARTIAL_EXTERNAL` | 14 |
| `NO_SEPARATE_RULE_TABLE` | 10 |

## Агрегированные метрики требований

| Метрика | Значение |
|:---|:---:|
| Всего нормативных требований | **178** |
| FULLY_MAPPABLE | 108 |
| SAFE_PARTIAL | 0 |
| EXTERNAL | 35 |
| AMBIGUOUS | 0 |
| ENGINE_UNSUPPORTED | 35 |
| SOURCE_CONFLICT | 0 |
| **Исполняемых итого** | **108** |
| **Неразрешенных итого** | **70** |
| Записей в MISSING_DATA.csv | **70** |

## Сгенерированные артефакты

| Артефакт | Описание |
|:---|:---|
| `codex_reports/OP32_FINAL_AUDIT.md` | Этот документ — полный аудит P.MM.06 / ОП_32 |
| `codex_reports/OP32_FINAL_MESSAGE_MATRIX.csv` | Матрица сообщений (24 строки) |
| `codex_reports/OP32_MISSING_DATA.csv` | Все неразрешённые требования (70 строк) |
| `codex_reports/OP32_EXTERNAL_DOCUMENTATION_GAPS.md` | Документ внешних пробелов |

## QNAME COMPLETION AUDIT

Проверка полноты `xml_owner` / `xml_qname` / `xml_path` во всех 70 строках `OP32_MISSING_DATA.csv`.

### Итоговые счётчики

| Метрика | Значение |
| :--- | :---: |
| TOTAL_MISSING_DATA_ROWS | **70** |
| QNAME_RESOLVED | **70** |
| QNAME_NOT_APPLICABLE | **0** |
| QNAME_STILL_UNRESOLVED | **0** |
| OWNER_STILL_UNRESOLVED | **0** |
| PATH_STILL_UNRESOLVED | **0** |

**Необъяснённых unresolved: 0** ✓

## Детальный аудит сообщений

Всего в процессе 24 сообщения:
- 14 сообщений содержат отдельные таблицы требований (168 требований суммарно);
- 10 сообщений являются служебными квитанциями или уведомлениями без отдельных таблиц правил в Решении №92.

Все тесты пакета проходят успешно (8 passed).
