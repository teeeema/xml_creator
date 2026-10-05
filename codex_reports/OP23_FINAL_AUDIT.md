# Финальный аудит P.SP.03 / ОП_23

- **Процесс**: P.SP.03 (Регистрация, правовая охрана и использование наименований мест происхождения товаров - НМПТ)
- **Статус**: COMPLETE
- **Вердикт**: READY
- **Сообщений всего**: 27 (существующих: 27, нормативно отсутствующих: 0)

## Результаты тестовых наборов

| Набор | Результат |
|:---|:---|
| OP23 regression (`pytest P.SP.03_OP_23/tests`) | **3 passed, 27 subtests passed** |
| Engine & Validator regression | **40 passed, 5 subtests passed** |
| Full eaeu_xml suite | **291 passed, 43 skipped, 1052 subtests passed** |
| Package validation | **0 errors** |

## Распределение статусов

| Статус | Кол-во |
|:---|:---:|
| `PARTIAL_EXTERNAL` | 21 |
| `NO_SEPARATE_RULE_TABLE` | 6 |

## Агрегированные метрики требований

| Метрика | Значение |
|:---|:---:|
| Всего нормативных требований | **400** |
| FULLY_MAPPABLE | 157 |
| SAFE_PARTIAL | 0 |
| EXTERNAL | 206 |
| AMBIGUOUS | 1 |
| ENGINE_UNSUPPORTED | 36 |
| SOURCE_CONFLICT | 0 |
| **Исполняемых итого** | **157** |
| **Неразрешенных итого** | **243** |
| Записей в MISSING_DATA.csv | **243** |

## Сгенерированные артефакты

| Артефакт | Описание |
|:---|:---|
| `codex_reports/OP23_FINAL_AUDIT.md` | Этот документ — полный аудит P.SP.03 / ОП_23 |
| `codex_reports/OP23_FINAL_MESSAGE_MATRIX.csv` | Матрица сообщений (27 строк) |
| `codex_reports/OP23_MISSING_DATA.csv` | Все неразрешённые требования (243 строк) |
| `codex_reports/OP23_EXTERNAL_DOCUMENTATION_GAPS.md` | Документ внешних пробелов |

## QNAME COMPLETION AUDIT

Проверка полноты `xml_owner` / `xml_qname` / `xml_path` во всех 243 строках `OP23_MISSING_DATA.csv`.

### Итоговые счётчики

| Метрика | Значение |
| :--- | :---: |
| TOTAL_MISSING_DATA_ROWS | **243** |
| QNAME_RESOLVED | **243** |
| QNAME_NOT_APPLICABLE | **0** |
| QNAME_STILL_UNRESOLVED | **0** |
| OWNER_STILL_UNRESOLVED | **0** |
| PATH_STILL_UNRESOLVED | **0** |

**Необъяснённых unresolved: 0** ✓

## Детальный аудит сообщений

Всего в процессе 27 сообщений:
- 21 сообщение содержит отдельные таблицы требований (400 требований суммарно);
- 6 сообщений являются служебными квитанциями или уведомлениями без отдельных таблиц правил в ОП_23.

Все тесты пакета проходят успешно (3 passed, 27 subtests passed).
