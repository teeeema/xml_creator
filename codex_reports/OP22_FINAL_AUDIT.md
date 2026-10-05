# Финальный аудит P.SP.02 / ОП_22

- **Процесс**: P.SP.02
- **Статус**: COMPLETE
- **Вердикт**: READY
- **Сообщений всего**: 63 (существующих: 61, нормативно отсутствующих: 2)

## Результаты тестовых наборов

| Набор | Результат |
|:---|:---|
| OP22 regression (`pytest P.SP.02_OP_22/tests`) | **2348 passed** |
| Engine & Validator regression | **40 passed, 5 subtests passed** |
| Full eaeu_xml suite | **291 passed, 43 skipped, 1052 subtests passed** |
| Package validation | **0 errors** |

## Распределение статусов

| Статус | Кол-во |
|:---|:---:|
| `FINAL_READY` | 6 |
| `PARTIAL_EXTERNAL` | 39 |
| `PARTIAL_ENGINE_UNSUPPORTED` | 8 |
| `PARTIAL_AMBIGUOUS` | 1 |
| `SOURCE_CONFLICT` | 3 |
| `NO_SEPARATE_RULE_TABLE` | 4 |
| `NORMATIVELY_ABSENT` | 2 |

## Агрегированные метрики требований

| Метрика | Значение |
|:---|:---:|
| Всего нормативных требований | **1557** |
| FULLY_MAPPABLE | 1214 |
| SAFE_PARTIAL | 79 |
| EXTERNAL | 54 |
| AMBIGUOUS | 23 |
| ENGINE_UNSUPPORTED | 181 |
| SOURCE_CONFLICT | 6 |
| **Исполняемых итого** | **1293** |
| **Неразрешенных итого** | **264** |
| Записей в MISSING_DATA.csv | **343** |

## Сгенерированные артефакты

| Артефакт | Описание |
|:---|:---|
| `codex_reports/OP22_FINAL_AUDIT.md` | Этот документ — полный аудит P.SP.02 / ОП_22 |
| `codex_reports/OP22_FINAL_MESSAGE_MATRIX.csv` | Матрица сообщений (63 строки) |
| `codex_reports/OP22_MISSING_DATA.csv` | Все неразрешённые требования (343 строки) |
| `codex_reports/OP22_EXTERNAL_DOCUMENTATION_GAPS.md` | Документ пробелов: EXTERNAL / ENGINE_UNSUPPORTED / AMBIGUOUS / SOURCE_CONFLICT / SAFE_PARTIAL |

## QNAME COMPLETION AUDIT

Проверка полноты `xml_owner` / `xml_qname` / `xml_path` во всех 343 строках `OP22_MISSING_DATA.csv`.

### Итоговые счётчики

| Метрика | Значение |
| :--- | :---: |
| TOTAL_MISSING_DATA_ROWS | **343** |
| QNAME_RESOLVED | **341** |
| QNAME_NOT_APPLICABLE | **2** |
| QNAME_STILL_UNRESOLVED | **0** |
| OWNER_STILL_UNRESOLVED | **0** |
| PATH_STILL_UNRESOLVED | **0** |

**Необъяснённых unresolved: 0** ✓

### Методология по классам

| Класс | xml_owner / xml_qname / xml_path | missing_data | missing_engine_capability |
| :--- | :--- | :--- | :--- |
| `EXTERNAL` | Точный QName поля | Нормативный текст условия | N/A |
| `ENGINE_UNSUPPORTED` | Точный QName поля | `NONE` (данные в XML) | Описание отсутствующей возможности |
| `AMBIGUOUS` | QName спорного поля | Нормативный текст | N/A |
| `SOURCE_CONFLICT` | QName конфликтующего поля | Описание конфликта | N/A |
| `SAFE_PARTIAL` | QName частично покрытого поля | Описание непокрытой части | N/A |

### NOT_APPLICABLE строки (2)

`P.SP.02.MSG.059 REQ 5` (Tables 78, 79): `xml_owner = xml_qname = xml_path = NOT_APPLICABLE`.
Требование «другие реквизиты не заполняются» не относится к конкретному XML-полю,
а к объёму структуры документа целиком. `reason` объясняет неоднозначность.

### Изменения, внесённые при аудите

| Тип изменения | Кол-во строк |
| :--- | :---: |
| `ENGINE_UNSUPPORTED` → `missing_data = NONE` (данные в XML, проблема в движке) | 181 |
| `ENGINE_UNSUPPORTED` → заполнен `missing_engine_capability` (был NONE) | 15 |
| `AMBIGUOUS` → исправлен QName (был идентификатор структуры, а не поля) | 10 |
| `AMBIGUOUS` → `NOT_APPLICABLE` (структурное требование без конкретного поля) | 2 |

## Детальный аудит сообщений

### P.SP.02.MSG.001: сведения о заявке на ТЗ Союза для опубликования

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.001` | **Процедура**: `P.SP.02.PRC.001` | **Операция**: `P.SP.02.OPR.001`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 34
- **Тесты**: PASS (44 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 39 | 23 | 0 | 2 | 0 | 14 | 0 | 23 | 16 |

**Записей в MISSING_DATA** (16):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 4 | `EXTERNAL` | N/A | при включении в классификатор видов документов, сведений и материалов, используемых в сфере интеллектуальной собственнос |
| REQ 5 | `EXTERNAL` | N/A | при отсутствии в классификаторе видов документов, сведений и материалов значения, соответствующего виду документа «Заявк |
| REQ 13 | `ENGINE_UNSUPPORTED` | N/A | значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной со |
| REQ 14 | `ENGINE_UNSUPPORTED` | N/A | в электронном документе (сведениях) «Сведения о заявке, ходатайстве для прохождения процедур регистрации ТЗ Союза» (R.IP |
| REQ 15 | `ENGINE_UNSUPPORTED` | N/A | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собств |
| REQ 16 | `ENGINE_UNSUPPORTED` | N/A | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собств |
| REQ 17 | `ENGINE_UNSUPPORTED` | N/A | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собств |
| REQ 18 | `ENGINE_UNSUPPORTED` | N/A | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собств |
| REQ 19 | `ENGINE_UNSUPPORTED` | N/A | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собств |
| REQ 20 | `ENGINE_UNSUPPORTED` | N/A | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собств |
| REQ 21 | `ENGINE_UNSUPPORTED` | N/A | если в состав электронного документа (сведений) включен экземпляр реквизита «Участник отношений в сфере регистрации и ис |
| REQ 22 | `ENGINE_UNSUPPORTED` | N/A | если в состав электронного документа (сведений) включен экземпляр реквизита «Участник отношений в сфере регистрации и ис |
| REQ 26 | `ENGINE_UNSUPPORTED` | N/A | в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails), в составе |
| REQ 27 | `ENGINE_UNSUPPORTED` | N/A | если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида товарного знака» (i |
| REQ 32 | `ENGINE_UNSUPPORTED` | N/A | если в состав электронного документа (сведений) включен и заполнен экземпляр реквизита «Приоритет товарного знака Союза» |
| REQ 33 | `ENGINE_UNSUPPORTED` | N/A | если в состав электронного документа (сведений) включен экземпляр реквизита «Прилагаемый документ» (ipcdo:AccompanyingDo |

### P.SP.02.MSG.002: уведомление о приеме и обработке сведений

- **Статус**: `NO_SEPARATE_RULE_TABLE`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.054` | **Процедура**: `P.SP.02.PRC.034` | **Операция**: `P.SP.02.OPR.199`
- **Направление**: RESPONSE | **Структура**: `R.006`
- **Таблица ОП_22**: NO_SEPARATE_RULE_TABLE
- **Тесты**: PASS (catalog only, 0 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.003: сведения о регистрации (отказе в регистрации) ТЗ Союза для опубликования

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.002` | **Процедура**: `P.SP.02.PRC.005` | **Операция**: `P.SP.02.OPR.018`
- **Направление**: REQUEST | **Структура**: `R.010`
- **Таблица ОП_22**: Table 35/36/37
- **Тесты**: PASS (76 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 33 | 29 | 0 | 2 | 0 | 2 | 0 | 29 | 4 |

**Записей в MISSING_DATA** (4):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 4 | `EXTERNAL` | N/A | при отсутствии в классификаторе видов документов, сведений и материалов вида документа «Решение об отказе в регистрации  |
| REQ 4 | `EXTERNAL` | N/A | при включении в классификатор видов документов, сведений и материалов значения, соответствующего одному из видов докумен |
| REQ 18 | `ENGINE_UNSUPPORTED` | N/A | если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Признак коллективного знака» |
| REQ 19 | `ENGINE_UNSUPPORTED` | N/A | если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Признак коллективного знака» |

### P.SP.02.MSG.004: обращение заинтересованного лица для опубликования

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.003` | **Процедура**: `P.SP.02.PRC.008` | **Операция**: `P.SP.02.OPR.028`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 38
- **Тесты**: PASS (51 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 31 | 29 | 0 | 2 | 0 | 0 | 0 | 29 | 2 |

**Записей в MISSING_DATA** (2):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | N/A | при включении в классификатор видов документов, сведений и материалов значения, соответствующего виду документа «Обращен |
| REQ 3 | `EXTERNAL` | N/A | при отсутствии в классификаторе видов документов, сведений и материалов значения, соответствующего виду документа «Обращ |

### P.SP.02.MSG.005: доводы заявителя в отношении обращения заинтересованного лица для опубликования

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.004` | **Процедура**: `P.SP.02.PRC.009` | **Операция**: `P.SP.02.OPR.032`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 39
- **Тесты**: PASS (69 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 31 | 28 | 0 | 2 | 0 | 1 | 0 | 28 | 3 |

**Записей в MISSING_DATA** (3):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | N/A | при включении в классификатор видов документов, сведений и материалов значения, соответствующего виду документа «Доводы  |
| REQ 3 | `EXTERNAL` | N/A | при отсутствии указанного вида документа в классификаторе ipsdo:IPDocKindCode не заполняется, а ipsdo:IPDocKindName долж |
| REQ 33 | `ENGINE_UNSUPPORTED` | N/A | в составе ipcdo:ArgumentDetails должны быть заполнены csdo:DescriptionText и csdo:EventDate |

### P.SP.02.MSG.006: доказательства приобретения обозначением различительной способности для опубликования

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.005` | **Процедура**: `P.SP.02.PRC.010` | **Операция**: `P.SP.02.OPR.040`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 40
- **Тесты**: PASS (211 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 29 | 27 | 0 | 2 | 0 | 0 | 0 | 27 | 2 |

**Записей в MISSING_DATA** (2):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | N/A | при наличии соответствующего вида документа в классификаторе ipsdo:IPDocKindCode заполняется кодом документа «Документ,  |
| REQ 3 | `EXTERNAL` | N/A | при отсутствии соответствующего вида документа в классификаторе ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName  |

### P.SP.02.MSG.007: сведения о документах, подтверждающих испрашиваемый приоритет ТЗ Союза для опубликования

- **Статус**: `PARTIAL_ENGINE_UNSUPPORTED`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.006` | **Процедура**: `P.SP.02.PRC.014` | **Операция**: `P.SP.02.OPR.057`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 41
- **Тесты**: PASS (211 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 28 | 26 | 0 | 0 | 0 | 2 | 0 | 26 | 2 |

**Записей в MISSING_DATA** (2):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `ENGINE_UNSUPPORTED` | N/A | при наличии вида документа «Другие документы, подтверждающие правомочность требования установления приоритета более ранн |
| REQ 3 | `ENGINE_UNSUPPORTED` | N/A | при отсутствии указанного вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется указанным н |

### P.SP.02.MSG.008: NORMATIVELY_ABSENT

- **Статус**: `NORMATIVELY_ABSENT`
- **Существование**: NO
- **Транзакция**: `None` | **Процедура**: `None` | **Операция**: `None`
- **Направление**: None | **Структура**: `None`
- **Таблица ОП_22**: NORMATIVELY_ABSENT
- **Тесты**: N/A

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.009: cведения о преобразовании заявки на ТЗ Союза в национальную заявку на регистрацию ТЗ для опубликования

- **Статус**: `PARTIAL_ENGINE_UNSUPPORTED`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.007` | **Процедура**: `P.SP.02.PRC.017` | **Операция**: `P.SP.02.OPR.067`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 42
- **Тесты**: PASS (211 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 26 | 24 | 0 | 0 | 0 | 2 | 0 | 24 | 2 |

**Записей в MISSING_DATA** (2):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `ENGINE_UNSUPPORTED` | N/A | при наличии соответствующего вида документа о преобразовании заявки в национальную заявку ipsdo:IPDocKindCode заполняетс |
| REQ 3 | `ENGINE_UNSUPPORTED` | N/A | при отсутствии соответствующего вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется норма |

### P.SP.02.MSG.010: сведения о преобразовании заявки на коллективный знак Союза в заявку на ТЗ Союза для опубликования

- **Статус**: `PARTIAL_ENGINE_UNSUPPORTED`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.008` | **Процедура**: `P.SP.02.PRC.018` | **Операция**: `P.SP.02.OPR.075`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 43
- **Тесты**: PASS (211 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 26 | 24 | 0 | 0 | 0 | 2 | 0 | 24 | 2 |

**Записей в MISSING_DATA** (2):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `ENGINE_UNSUPPORTED` | N/A | при наличии вида документа о преобразовании заявки на коллективный знак Союза в заявку на ТЗ Союза ipsdo:IPDocKindCode з |
| REQ 3 | `ENGINE_UNSUPPORTED` | N/A | при отсутствии такого вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется нормативным наи |

### P.SP.02.MSG.011: сведения о преобразовании заявки на ТЗ Союза в заявку на коллективный знак Союза для опубликования

- **Статус**: `PARTIAL_ENGINE_UNSUPPORTED`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.009` | **Процедура**: `P.SP.02.PRC.019` | **Операция**: `P.SP.02.OPR.083`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 44
- **Тесты**: PASS (70 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 26 | 24 | 0 | 0 | 0 | 2 | 0 | 24 | 2 |

**Записей в MISSING_DATA** (2):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `ENGINE_UNSUPPORTED` | N/A | при наличии вида документа о преобразовании заявки на ТЗ Союза в заявку на коллективный знак Союза ipsdo:IPDocKindCode з |
| REQ 3 | `ENGINE_UNSUPPORTED` | N/A | при отсутствии такого вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется нормативным наи |

### P.SP.02.MSG.012: сведения о выделении заявки на ТЗ Союза из ранее поданной заявки на ТЗ Союза для опубликования

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.010` | **Процедура**: `P.SP.02.PRC.020` | **Операция**: `P.SP.02.OPR.091`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 45
- **Тесты**: PASS (98 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 34 | 23 | 0 | 5 | 1 | 5 | 0 | 23 | 11 |

**Записей в MISSING_DATA** (11):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Document-kind classifier and prior role selection are external. |
| REQ 3 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Document-kind classifier absence check and prior role selection are external. |
| REQ 4 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Document-kind classifier and divided role selection are external. |
| REQ 5 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Document-kind classifier absence check and divided role selection are external. |
| REQ 13 | `AMBIGUOUS` | `ipcdo:TrademarkApplicationDetails` | Ambiguous normative definition in isolation; IPPartyKindCode AP is enforced as part of requirement 14. |
| REQ 16 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent, which is unsupporte |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent, which is unsupporte |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent, which is unsupporte |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent, which is unsupporte |
| REQ 20 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent, which is unsupporte |
| REQ 32 | `EXTERNAL` | `ipsdo:TrademarkApplicationId` | Both role-specific resource existence/absence checks are external and require identifying the two instances. |

### P.SP.02.MSG.013: cведения о признании заявки на ТЗ Союза отозванной по ходатайству заявителя для опубликования

- **Статус**: `PARTIAL_ENGINE_UNSUPPORTED`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.011` | **Процедура**: `P.SP.02.PRC.021` | **Операция**: `P.SP.02.OPR.099`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 46
- **Тесты**: PASS (70 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 26 | 24 | 0 | 0 | 0 | 2 | 0 | 24 | 2 |

**Записей в MISSING_DATA** (2):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `ENGINE_UNSUPPORTED` | N/A | при наличии вида документа «Ходатайство об отзыве заявки ... (по инициативе заявителя)» ipsdo:IPDocKindCode заполняется  |
| REQ 3 | `ENGINE_UNSUPPORTED` | N/A | при отсутствии указанного вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется нормативным |

### P.SP.02.MSG.014: сведения о внесении изменений в заявку на ТЗ Союза для опубликования

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.012` | **Процедура**: `P.SP.02.PRC.022` | **Операция**: `P.SP.02.OPR.107`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 47
- **Тесты**: PASS (70 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 26 | 22 | 0 | 1 | 0 | 3 | 0 | 22 | 4 |

**Записей в MISSING_DATA** (4):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `ENGINE_UNSUPPORTED` | N/A | в ресурсах Комиссии должна существовать активная запись заявки со статусом «01» или «02», у которой совокупность Tradema |
| REQ 4 | `EXTERNAL` | N/A | при наличии в классификаторе соответствующего вида ходатайства о внесении изменений ipsdo:IPDocKindCode заполняется его  |
| REQ 5 | `ENGINE_UNSUPPORTED` | N/A | при отсутствии соответствующего вида ходатайства ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется соо |
| REQ 30 | `ENGINE_UNSUPPORTED` | N/A | если вид документа соответствует ходатайству об изменениях, связанных с передачей или переходом права на заявку, и IPPar |

### P.SP.02.MSG.015: сведения о преобразовании аннулированной регистрации ТЗ Союза в национальную заявку на регистрацию ТЗ для опубликования

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.013` | **Процедура**: `P.SP.02.PRC.023` | **Операция**: `P.SP.02.OPR.115`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 48
- **Тесты**: PASS (21 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 6 | 3 | 1 | 2 | 0 | 0 | 0 | 4 | 2 |

**Записей в MISSING_DATA** (3):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 1 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Requires external lookup in unified classifier resource for IP document kind presence. Non-executable. |
| REQ 2 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Requires external lookup verifying absence of document kind in unified classifier resource. Non-executable. |
| REQ 3 | `SAFE_PARTIAL` | `ipsdo:TrademarkId` | Local predicate mapped: TrademarkId is required in each record. External lookup of canceled status 04 in registry remain |

### P.SP.02.MSG.016: сведения о преобразовании коллективного знака Союза в ТЗ Союза для опубликования

- **Статус**: `FINAL_READY`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.014` | **Процедура**: `P.SP.02.PRC.024` | **Операция**: `P.SP.02.OPR.123`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 49
- **Тесты**: PASS (74 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 21 | 21 | 0 | 0 | 0 | 0 | 0 | 21 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.017: сведения о преобразовании ТЗ Союза в коллективный знак Союза для опубликования

- **Статус**: `FINAL_READY`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.015` | **Процедура**: `P.SP.02.PRC.025` | **Операция**: `P.SP.02.OPR.131`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 50
- **Тесты**: PASS (74 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 23 | 23 | 0 | 0 | 0 | 0 | 0 | 23 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.018: сведения о внесении изменений в сведения Единого реестра ТЗ Союза для опубликования

- **Статус**: `FINAL_READY`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.016` | **Процедура**: `P.SP.02.PRC.026` | **Операция**: `P.SP.02.OPR.139`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 51
- **Тесты**: PASS (74 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 22 | 22 | 0 | 0 | 0 | 0 | 0 | 22 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.019: сведения об отказе от исключительного права на ТЗ Союза для опубликования

- **Статус**: `FINAL_READY`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.017` | **Процедура**: `P.SP.02.PRC.027` | **Операция**: `P.SP.02.OPR.147`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 52
- **Тесты**: PASS (74 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 21 | 21 | 0 | 0 | 0 | 0 | 0 | 21 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.020: сведения об аннулировании регистрации ТЗ Союза для опубликования

- **Статус**: `PARTIAL_ENGINE_UNSUPPORTED`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.018` | **Процедура**: `P.SP.02.PRC.029` | **Операция**: `P.SP.02.OPR.158`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 53
- **Тесты**: PASS (64 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 29 | 28 | 0 | 0 | 0 | 1 | 0 | 28 | 1 |

**Записей в MISSING_DATA** (1):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 3 | `ENGINE_UNSUPPORTED` | N/A | Если CancellationStatusIndicator хотя бы для одного GoodsBaseDetails = «1», должен быть второй экземпляр с регистрацией  |

### P.SP.02.MSG.021: сведения о продлении срока действия исключительного права на ТЗ Союза для опубликования

- **Статус**: `PARTIAL_ENGINE_UNSUPPORTED`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.019` | **Процедура**: `P.SP.02.PRC.030` | **Операция**: `P.SP.02.OPR.166`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 54
- **Тесты**: PASS (54 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 21 | 19 | 0 | 0 | 0 | 2 | 0 | 19 | 2 |

**Записей в MISSING_DATA** (2):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 22 | `ENGINE_UNSUPPORTED` | N/A | Все прежние DocValidityDate должны совпадать со значениями сообщения, кроме одного нового значения. |
| REQ 23 | `ENGINE_UNSUPPORTED` | N/A | Новое DocValidityDate должно быть больше остальных DocValidityDate в сообщении. |

### P.SP.02.MSG.022: запрос информации о дате и времени обновления Единого реестра ТЗ Союза

- **Статус**: `FINAL_READY`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.020` | **Процедура**: `P.SP.02.PRC.031` | **Операция**: `P.SP.02.OPR.170`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.008`
- **Таблица ОП_22**: Table 55
- **Тесты**: PASS (14 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.023: информация о дате и времени обновления Единого реестра ТЗ Союза

- **Статус**: `NO_SEPARATE_RULE_TABLE`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.020` | **Процедура**: `P.SP.02.PRC.031` | **Операция**: `P.SP.02.OPR.171`
- **Направление**: RESPONSE | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: NO_SEPARATE_RULE_TABLE
- **Тесты**: PASS (catalog only, 0 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.024: запрос изменений сведений Единого реестра ТЗ Союза

- **Статус**: `PARTIAL_ENGINE_UNSUPPORTED`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.021` | **Процедура**: `P.SP.02.PRC.032` | **Операция**: `P.SP.02.OPR.173`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.008`
- **Таблица ОП_22**: Table 56
- **Тесты**: PASS (16 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 3 | 2 | 0 | 0 | 0 | 1 | 0 | 2 | 1 |

**Записей в MISSING_DATA** (1):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `ENGINE_UNSUPPORTED` | N/A | ipcdo:AccompanyingDocumentsDetails и ipsdo:ApellationOfOriginApplicationId не заполняются. |

### P.SP.02.MSG.025: уведомление об отсутствии сведений

- **Статус**: `NO_SEPARATE_RULE_TABLE`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.051` | **Процедура**: `P.SP.02.PRC.036` | **Операция**: `P.SP.02.OPR.187`
- **Направление**: RESPONSE | **Структура**: `R.006`
- **Таблица ОП_22**: NO_SEPARATE_RULE_TABLE
- **Тесты**: PASS (catalog only, 0 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.026: изменения сведений Единого реестра ТЗ Союза

- **Статус**: `NO_SEPARATE_RULE_TABLE`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.021` | **Процедура**: `P.SP.02.PRC.032` | **Операция**: `P.SP.02.OPR.174`
- **Направление**: RESPONSE | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: NO_SEPARATE_RULE_TABLE
- **Тесты**: PASS (catalog only, 0 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.027: сведения о признании заявки на ТЗ Союза отозванной по причине неуплаты пошлин для опубликования

- **Статус**: `SOURCE_CONFLICT`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.022` | **Процедура**: `P.SP.02.PRC.034` | **Операция**: `P.SP.02.OPR.179`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 57
- **Тесты**: PASS (96 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 42 | 32 | 3 | 0 | 1 | 5 | 1 | 35 | 7 |

**Записей в MISSING_DATA** (10):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 3 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 13 | `AMBIGUOUS` | N/A | Exact repeated owner is ambiguous; global AP enforcement would conflict with PA/RE roles. |
| REQ 16 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-scoped correlation to repeated IPSubjectName attributes. |
| REQ 17 | `ENGINE_UNSUPPORTED` | N/A | Requires per-AP filtered cardinality over repeated IPSubjectName plus attributes. |
| REQ 18 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-scoped languageCode=RU second-instance semantics. |
| REQ 19 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-scoped languageCode!=RU second-instance LA semantics. |
| REQ 20 | `ENGINE_UNSUPPORTED` | N/A | Requires AP role correlated with nested repeated SubjectAddressDetails. |
| REQ 27 | `SOURCE_CONFLICT` | N/A | Table34 image QName conflicts with R.IP.SP.02.002 TrademarkPicture/TrademarkColourName semantics. |

### P.SP.02.MSG.028: сведения о заявке на ТЗ Союза для экспертизы

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.023` | **Процедура**: `P.SP.02.PRC.002` | **Операция**: `P.SP.02.OPR.005`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 44
- **Тесты**: PASS (119 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 49 | 41 | 4 | 1 | 1 | 2 | 0 | 45 | 4 |

**Записей в MISSING_DATA** (8):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 3 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 5 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 37 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 13 | `AMBIGUOUS` | N/A | The row states IPPartyKindCode=AP without an unambiguous repeated owner; global enforcement would contradict PA/RE rows. |
| REQ 18 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-scoped languageCode=RU second-instance semantics. |
| REQ 19 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-scoped languageCode!=RU second-instance LA semantics. |
| REQ 32 | `EXTERNAL` | N/A | Requires authoritative priority-characteristic classifier/reference data not available to the current evaluator. |

### P.SP.02.MSG.029: заключение (решение) о результатах экспертизы

- **Статус**: `SOURCE_CONFLICT`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.024` | **Процедура**: `P.SP.02.PRC.003` | **Операция**: `P.SP.02.OPR.008`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 45
- **Тесты**: PASS (84 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 43 | 28 | 4 | 0 | 1 | 8 | 2 | 32 | 11 |

**Записей в MISSING_DATA** (15):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| SOURCE_CONFLICT | `SOURCE_CONFLICT` | N/A | Table45 REQ32 assigns ipsdo:InconsistencyText to the selected ipcdo:GoodsBaseDetails instance, but the StructureDefiniti |
| REQ 2 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 5 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 35 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 13 | `AMBIGUOUS` | N/A | Table44 states IPPartyKindCode=AP without an unambiguous repeated owner; global enforcement would contradict the explici |
| REQ 16 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-scoped correlation to repeated IPSubjectName representation attributes. |
| REQ 17 | `ENGINE_UNSUPPORTED` | N/A | Requires per-AP filtered cardinality over repeated IPSubjectName plus representation/language attributes. |
| REQ 18 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-scoped languageCode=RU second-instance semantics. |
| REQ 19 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-scoped languageCode!=RU second-instance LA semantics. |
| REQ 20 | `ENGINE_UNSUPPORTED` | N/A | Requires AP role correlated with nested SubjectAddressDetails semantics beyond the current safe selector model. |
| REQ 26 | `ENGINE_UNSUPPORTED` | N/A | Original Table44 REQ26 is written as TrademarkKindCode OR TrademarkKindName matching the listed values. The current eval |
| REQ 30 | `ENGINE_UNSUPPORTED` | N/A | Requires conditional filtered cardinality: for TrademarkRegistrationCode=01, count GoodsBaseDetails with TrademarkDecisi |
| REQ 31 | `ENGINE_UNSUPPORTED` | N/A | Requires conditional filtered cardinality: for TrademarkRegistrationCode in {02,03}, at least one GoodsBaseDetails with  |
| REQ 32 | `SOURCE_CONFLICT` | N/A | Table45 requires InconsistencyText inside each selected GoodsBaseDetails row, while R.IP.SP.02.002 defines ipsdo:Inconsi |

### P.SP.02.MSG.030: доводы и замечания по результатам экспертизы

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.025` | **Процедура**: `P.SP.02.PRC.004` | **Операция**: `P.SP.02.OPR.011`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 46
- **Тесты**: PASS (119 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 40 | 30 | 3 | 1 | 0 | 6 | 0 | 33 | 7 |

**Записей в MISSING_DATA** (10):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | Exact branch depends on authoritative classifier membership, which is external to the current values. |
| REQ 3 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | Exact branch depends on authoritative classifier absence, which is external to the current values. |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | Local TrademarkApplicationId presence is executable; the required national-patent-office resource lookup and corresponde |
| REQ 13 | `EXTERNAL` | N/A | Table44 states IPPartyKindCode=AP without an unambiguous repeated owner; applying it globally would contradict explicitl |
| REQ 16 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-scoped correlation to repeated IPSubjectName representation attributes. |
| REQ 17 | `ENGINE_UNSUPPORTED` | N/A | Requires per-AP filtered cardinality over repeated IPSubjectName plus representation/language attributes. |
| REQ 18 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-scoped languageCode=RU second-instance semantics. |
| REQ 19 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-scoped languageCode!=RU second-instance LA semantics. |
| REQ 20 | `ENGINE_UNSUPPORTED` | N/A | Requires AP-role correlation with nested repeated SubjectAddressDetails semantics beyond the current safe selector model |
| REQ 26 | `ENGINE_UNSUPPORTED` | N/A | Table44 REQ26 is explicitly TrademarkKindCode OR TrademarkKindName matching one of the listed kinds. The current evaluat |

### P.SP.02.MSG.031: сведения о регистрации (отказе в регистрации) ТЗ Союза

- **Статус**: `SOURCE_CONFLICT`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.026` | **Процедура**: `P.SP.02.PRC.005` | **Операция**: `P.SP.02.OPR.015`
- **Направление**: REQUEST | **Структура**: `R.010`
- **Таблица ОП_22**: Table 47/48/49
- **Тесты**: PASS (84 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 61 | 43 | 6 | 0 | 1 | 8 | 3 | 49 | 12 |

**Записей в MISSING_DATA** (18):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 1 | `SAFE_PARTIAL` | N/A | Local TrademarkApplicationId presence is executable; national-resource correspondence is external. |
| REQ 2 | `SOURCE_CONFLICT` | N/A | Table48 REQ2 names a direct TrademarkId, but R.IP.SP.02.002 has no exact direct TrademarkApplicationDetails/ipsdo:Tradem |
| REQ 3 | `SAFE_PARTIAL` | N/A | Classifier membership and code designation are external; local mutual-exclusion fragment is safe. |
| REQ 4 | `SAFE_PARTIAL` | N/A | Classifier absence is external; exact single fallback name is locally enforceable when code is absent. |
| REQ 13 | `AMBIGUOUS` | N/A | Original Table44 REQ13 states IPPartyKindCode=AP without an unambiguous repeated-owner/instance scope; global enforcemen |
| REQ 16 | `ENGINE_UNSUPPORTED` | N/A | Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values that the current eval |
| REQ 17 | `ENGINE_UNSUPPORTED` | N/A | Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values that the current eval |
| REQ 18 | `ENGINE_UNSUPPORTED` | N/A | Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values that the current eval |
| REQ 19 | `ENGINE_UNSUPPORTED` | N/A | Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values that the current eval |
| REQ 20 | `ENGINE_UNSUPPORTED` | N/A | Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values that the current eval |
| REQ 26 | `ENGINE_UNSUPPORTED` | N/A | Original Table44 REQ26 is explicitly TrademarkKindCode OR TrademarkKindName matching an allowed kind; the evaluator cann |
| REQ 30 | `SOURCE_CONFLICT` | N/A | Table48 REQ30 assigns InconsistencyText to GoodsBaseDetails, while the StructureDefinition places ipsdo:InconsistencyTex |
| REQ 32 | `SOURCE_CONFLICT` | N/A | Table48 REQ32 forbids direct ipsdo:DecisionOnComplaintText under TrademarkApplicationDetails, but that exact path/QName  |
| REQ 3 | `SAFE_PARTIAL` | N/A | Local TrademarkId presence is executable; uniqueness/nonexistence lookup is external. |
| REQ 4 | `SAFE_PARTIAL` | N/A | Classifier membership/code designation are external; local mutual-exclusion fragment is safe. |
| REQ 5 | `SAFE_PARTIAL` | N/A | Classifier absence is external and the evaluator cannot conditionally compare IPDocKindName against either of two exact  |
| REQ 18 | `ENGINE_UNSUPPORTED` | N/A | Requires a conditional cross-collection existence check from TrademarkDetails.CollectiveMarkIndicator=1 to a UE IPPartyD |
| REQ 19 | `ENGINE_UNSUPPORTED` | N/A | Requires a conditional cross-collection AccompanyingDocumentsDetails existence check plus exact per-document IPDocKindCo |

### P.SP.02.MSG.032: уведомление о поступившей жалобе на решение по экспертизе

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.027` | **Процедура**: `P.SP.02.PRC.006` | **Операция**: `P.SP.02.OPR.022`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 50
- **Тесты**: PASS (65 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 32 | 22 | 3 | 0 | 1 | 6 | 0 | 25 | 7 |

**Записей в MISSING_DATA** (10):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `SAFE_PARTIAL` | N/A | Classifier availability and authoritative complaint-kind code are external; the local implication code-present => name f |
| REQ 3 | `SAFE_PARTIAL` | N/A | Classifier absence is external; the local implication code-absent => exact fallback name is a necessary condition of eve |
| REQ 4 | `SAFE_PARTIAL` | N/A | Local TrademarkApplicationId presence is independently required; resource status, EndDateTime state, and ID corresponden |
| REQ 13 | `AMBIGUOUS` | N/A | Table44 REQ13 states IPPartyKindCode=AP without an unambiguous repeated IPPartyDetails instance scope; enforcing it glob |
| REQ 16 | `ENGINE_UNSUPPORTED` | N/A | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 17 | `ENGINE_UNSUPPORTED` | N/A | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 18 | `ENGINE_UNSUPPORTED` | N/A | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 19 | `ENGINE_UNSUPPORTED` | N/A | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 20 | `ENGINE_UNSUPPORTED` | N/A | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 26 | `ENGINE_UNSUPPORTED` | N/A | Table44 REQ26 normatively allows TrademarkKindCode OR TrademarkKindName to carry an allowed kind. The evaluator cannot e |

### P.SP.02.MSG.033: сведения о результатах внутригосударственного обжалования решения по экспертизе

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.028` | **Процедура**: `P.SP.02.PRC.007` | **Операция**: `P.SP.02.OPR.025`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 51
- **Тесты**: PASS (73 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 37 | 27 | 3 | 0 | 1 | 6 | 0 | 30 | 7 |

**Записей в MISSING_DATA** (10):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 3 | `SAFE_PARTIAL` | N/A | Classifier availability and the authoritative document-kind code are external; code-present => name forbidden is a neces |
| REQ 4 | `SAFE_PARTIAL` | N/A | Classifier absence is external; code-absent => exact fallback name is a necessary local condition of every valid classif |
| REQ 5 | `SAFE_PARTIAL` | N/A | Local TrademarkApplicationId presence is independently required; record existence, resource status/end-date state, and I |
| REQ 13 | `AMBIGUOUS` | N/A | Table44 REQ13 states IPPartyKindCode=AP without an unambiguous repeated IPPartyDetails instance scope; enforcing it glob |
| REQ 16 | `ENGINE_UNSUPPORTED` | N/A | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 17 | `ENGINE_UNSUPPORTED` | N/A | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 18 | `ENGINE_UNSUPPORTED` | N/A | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 19 | `ENGINE_UNSUPPORTED` | N/A | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 20 | `ENGINE_UNSUPPORTED` | N/A | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 26 | `ENGINE_UNSUPPORTED` | N/A | Table44 REQ26 normatively allows TrademarkKindCode OR TrademarkKindName to carry an allowed kind. The evaluator cannot e |

### P.SP.02.MSG.034: доказательство приобретения обозначением различительной способности

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.029` | **Процедура**: `P.SP.02.PRC.010` | **Операция**: `P.SP.02.OPR.037`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 52
- **Тесты**: PASS (63 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 37 | 27 | 3 | 0 | 1 | 6 | 0 | 30 | 7 |

**Записей в MISSING_DATA** (10):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | Classifier presence and authoritative code lookup are external; code-present => same-parent name forbidden is a necessar |
| REQ 3 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | Classifier absence is external; code-absent => exact normative fallback name is a necessary local consequence. |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | TrademarkApplicationId presence is independently required locally; record status, EndDateTime state and ID correspondenc |
| REQ 13 | `AMBIGUOUS` | `ipsdo:IPPartyKindCode` | The standalone AP value statement does not identify an exact repeated IPPartyDetails owner/instance scope, while later r |
| REQ 16 | `ENGINE_UNSUPPORTED` | `@nameRepresentationKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 20 | `ENGINE_UNSUPPORTED` | `csdo:AddressKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 26 | `ENGINE_UNSUPPORTED` | `ipsdo:TrademarkKindCode` | Table 44 uses TrademarkKindCode OR TrademarkKindName allowed-value semantics; current evaluator lacks a standalone per-T |

### P.SP.02.MSG.035: уведомление о необходимости представления документа о согласии

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.030` | **Процедура**: `P.SP.02.PRC.011` | **Операция**: `P.SP.02.OPR.044`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 53
- **Тесты**: PASS (46 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 29 | 20 | 2 | 0 | 1 | 6 | 0 | 22 | 7 |

**Записей в MISSING_DATA** (9):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | Authoritative classifier membership and code-to-literal correspondence are external; direct application-level IPDocKindC |
| REQ 3 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | External filing-office record state and identifier correspondence are not locally executable; direct application-level T |
| REQ 13 | `AMBIGUOUS` | `ipsdo:IPPartyKindCode` | The standalone AP value statement does not identify an exact repeated IPPartyDetails owner/instance scope, while later r |
| REQ 16 | `ENGINE_UNSUPPORTED` | `@nameRepresentationKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 20 | `ENGINE_UNSUPPORTED` | `csdo:AddressKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 26 | `ENGINE_UNSUPPORTED` | `ipsdo:TrademarkKindCode` | Table 44 uses TrademarkKindCode OR TrademarkKindName allowed-value semantics; current evaluator lacks a standalone per-T |

### P.SP.02.MSG.036: документ о согласии

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.031` | **Процедура**: `P.SP.02.PRC.012` | **Операция**: `P.SP.02.OPR.047`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 54
- **Тесты**: PASS (8 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 31 | 22 | 2 | 0 | 1 | 6 | 0 | 24 | 7 |

**Записей в MISSING_DATA** (9):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | Classifier correspondence is external; local IPDocKindCode presence is the safe executable fragment. |
| REQ 3 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | National patent-office record status and identifier correspondence are external; local TrademarkApplicationId presence i |
| REQ 13 | `AMBIGUOUS` | `ipsdo:IPPartyKindCode` | The standalone AP value statement does not identify an exact repeated IPPartyDetails owner/instance scope, while later r |
| REQ 16 | `ENGINE_UNSUPPORTED` | `@nameRepresentationKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 20 | `ENGINE_UNSUPPORTED` | `csdo:AddressKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/address values that the |
| REQ 26 | `ENGINE_UNSUPPORTED` | `ipsdo:TrademarkKindCode` | Table 44 uses TrademarkKindCode OR TrademarkKindName allowed-value semantics; current evaluator lacks a standalone per-T |

### P.SP.02.MSG.037: сведения о признании заявки на ТЗ Союза отозванной по причине непоступления документа о согласии

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.032` | **Процедура**: `P.SP.02.PRC.013` | **Операция**: `P.SP.02.OPR.050`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 55
- **Тесты**: PASS (58 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 31 | 21 | 1 | 2 | 1 | 6 | 0 | 22 | 9 |

**Записей в MISSING_DATA** (10):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipsdo:IPDocKindCode` | The branch depends on authoritative classifier presence/absence and lookup; no local executable rule is safe. |
| REQ 3 | `EXTERNAL` | `ipsdo:IPDocKindCode` | The branch depends on authoritative classifier presence/absence and lookup; no local executable rule is safe. |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | Local TrademarkApplicationId presence is independently required; resource/status/equality semantics are external. |
| REQ 13 | `AMBIGUOUS` | `ipsdo:IPPartyKindCode` | Table 44 AP code requirement does not establish a sufficiently explicit owner/instance scope beyond REQ14. |
| REQ 16 | `ENGINE_UNSUPPORTED` | `@nameRepresentationKindCode` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current evaluator. |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current evaluator. |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current evaluator. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current evaluator. |
| REQ 20 | `ENGINE_UNSUPPORTED` | `csdo:AddressKindCode` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current evaluator. |
| REQ 26 | `ENGINE_UNSUPPORTED` | `ipsdo:TrademarkKindCode` | Normative semantics require TrademarkKindCode OR TrademarkKindName correspondence within the same TrademarkDetails; AND  |

### P.SP.02.MSG.038: сведения о документах, подтверждающих испрашиваемый приоритет ТЗ Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.033` | **Процедура**: `P.SP.02.PRC.014` | **Операция**: `P.SP.02.OPR.054`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 56
- **Тесты**: PASS (6 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 37 | 26 | 1 | 3 | 1 | 6 | 0 | 27 | 10 |

**Записей в MISSING_DATA** (11):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipcdo:TrademarkApplicationDetails` | External classifier/resource semantics are not executable. |
| REQ 3 | `EXTERNAL` | `ipcdo:TrademarkApplicationDetails` | External classifier/resource semantics are not executable. |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | Local identifier presence is executable; external resource state/equality is not. |
| REQ 13 | `AMBIGUOUS` | `ipsdo:IPPartyKindCode` | Normative owner scope is ambiguous. |
| REQ 16 | `ENGINE_UNSUPPORTED` | `@nameRepresentationKindCode` | No safe exact evaluator expression. |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | No safe exact evaluator expression. |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | No safe exact evaluator expression. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | No safe exact evaluator expression. |
| REQ 20 | `ENGINE_UNSUPPORTED` | `csdo:AddressKindCode` | No safe exact evaluator expression. |
| REQ 26 | `ENGINE_UNSUPPORTED` | `ipsdo:TrademarkKindCode` | No safe exact evaluator expression. |
| REQ 31 | `EXTERNAL` | `ipcdo:TrademarkApplicationDetails` | External classifier/resource semantics are not executable. |

### P.SP.02.MSG.039: уведомление о прекращении делопроизводства по заявке на ТЗ Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.034` | **Процедура**: `P.SP.02.PRC.015` | **Операция**: `P.SP.02.OPR.061`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 57
- **Тесты**: PASS (60 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 31 | 21 | 1 | 2 | 1 | 6 | 0 | 22 | 9 |

**Записей в MISSING_DATA** (10):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipsdo:IPDocKindCode` | The branch depends on authoritative classifier presence/absence and lookup; no local executable rule is safe. |
| REQ 3 | `EXTERNAL` | `ipsdo:IPDocKindCode` | The branch depends on authoritative classifier presence/absence and lookup; no local executable rule is safe. |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | Local TrademarkApplicationId presence is independently required; resource/status/equality semantics are external. |
| REQ 13 | `AMBIGUOUS` | `ipsdo:IPPartyKindCode` | Table 44 AP code requirement does not establish a sufficiently explicit owner/instance scope beyond REQ14. |
| REQ 16 | `ENGINE_UNSUPPORTED` | `@nameRepresentationKindCode` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current evaluator. |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current evaluator. |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current evaluator. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current evaluator. |
| REQ 20 | `ENGINE_UNSUPPORTED` | `csdo:AddressKindCode` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current evaluator. |
| REQ 26 | `ENGINE_UNSUPPORTED` | `ipsdo:TrademarkKindCode` | Normative semantics require TrademarkKindCode OR TrademarkKindName correspondence within the same TrademarkDetails; AND  |

### P.SP.02.MSG.040: ходатайство о преобразовании заявки на ТЗ Союза в национальную заявку на регистрацию ТЗ

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.035` | **Процедура**: `P.SP.02.PRC.016` | **Операция**: `P.SP.02.OPR.064`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 58
- **Тесты**: PASS (9 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 34 | 24 | 1 | 2 | 1 | 6 | 0 | 25 | 9 |

**Записей в MISSING_DATA** (10):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipcdo:TrademarkApplicationDetails` | External classifier/resource semantics are not executable. |
| REQ 3 | `EXTERNAL` | `ipcdo:TrademarkApplicationDetails` | External classifier/resource semantics are not executable. |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | Local identifier presence is executable; external resource state/equality is not. |
| REQ 13 | `AMBIGUOUS` | `ipcdo:TrademarkApplicationDetails` | Normative owner scope is ambiguous. |
| REQ 16 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 20 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 26 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |

### P.SP.02.MSG.041: сведения о преобразовании заявки на коллективный знак Союза в заявку на ТЗ Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.036` | **Процедура**: `P.SP.02.PRC.018` | **Операция**: `P.SP.02.OPR.072`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 59
- **Тесты**: PASS (55 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 35 | 25 | 1 | 2 | 1 | 6 | 0 | 26 | 9 |

**Записей в MISSING_DATA** (10):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipcdo:TrademarkApplicationDetails` | External classifier/resource semantics are not executable. |
| REQ 3 | `EXTERNAL` | `ipcdo:TrademarkApplicationDetails` | External classifier/resource semantics are not executable. |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | Local identifier presence is executable; external resource state/equality is not. |
| REQ 13 | `AMBIGUOUS` | `ipcdo:TrademarkApplicationDetails` | Normative owner scope is ambiguous. |
| REQ 16 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 20 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 26 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |

### P.SP.02.MSG.042: сведения о преобразовании заявки на ТЗ Союза в заявку на коллективный знак Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.037` | **Процедура**: `P.SP.02.PRC.019` | **Операция**: `P.SP.02.OPR.080`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 60
- **Тесты**: PASS (16 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 35 | 25 | 1 | 2 | 1 | 6 | 0 | 26 | 9 |

**Записей в MISSING_DATA** (10):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipcdo:TrademarkApplicationDetails` | External classifier/resource semantics are not executable. |
| REQ 3 | `EXTERNAL` | `ipcdo:TrademarkApplicationDetails` | External classifier/resource semantics are not executable. |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | Local identifier presence is executable; external resource state/equality is not. |
| REQ 13 | `AMBIGUOUS` | `ipcdo:TrademarkApplicationDetails` | Normative owner scope is ambiguous. |
| REQ 16 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 20 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 26 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |

### P.SP.02.MSG.043: сведения о выделении заявки на ТЗ Союза из ранее поданной заявки на ТЗ Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.038` | **Процедура**: `P.SP.02.PRC.020` | **Операция**: `P.SP.02.OPR.088`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 61
- **Тесты**: PASS (33 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 37 | 26 | 0 | 5 | 1 | 5 | 0 | 26 | 11 |

**Записей в MISSING_DATA** (11):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Document-kind classifier and prior/allocated role selection are external. |
| REQ 3 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Document-kind classifier and prior/allocated role selection are external. |
| REQ 4 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Document-kind classifier and prior/allocated role selection are external. |
| REQ 5 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Document-kind classifier and prior/allocated role selection are external. |
| REQ 13 | `AMBIGUOUS` | `ipcdo:TrademarkApplicationDetails` | Ambiguous normative definition in isolation; IPPartyKindCode AP is enforced as part of requirement 14. |
| REQ 16 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent, which is unsupporte |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent, which is unsupporte |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent, which is unsupporte |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent, which is unsupporte |
| REQ 20 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent, which is unsupporte |
| REQ 31 | `EXTERNAL` | `ipsdo:TrademarkApplicationId` | Both role-specific resource existence/absence checks are external and require identifying the two instances. |

### P.SP.02.MSG.044: сведения о признании заявки на ТЗ Союза отозванной по ходатайству заявителя

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.039` | **Процедура**: `P.SP.02.PRC.021` | **Операция**: `P.SP.02.OPR.096`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 62
- **Тесты**: PASS (45 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 34 | 24 | 0 | 3 | 1 | 6 | 0 | 24 | 10 |

**Записей в MISSING_DATA** (10):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipcdo:TrademarkApplicationDetails` | External classifier/resource semantics are not executable. |
| REQ 3 | `EXTERNAL` | `ipcdo:TrademarkApplicationDetails` | External classifier/resource semantics are not executable. |
| REQ 4 | `EXTERNAL` | `ipsdo:TrademarkApplicationId` | External patent-office resource semantics are required; REQ4 remains completely unmapped. |
| REQ 13 | `AMBIGUOUS` | `ipcdo:TrademarkApplicationDetails` | Normative owner scope is ambiguous. |
| REQ 16 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 20 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| REQ 26 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |

### P.SP.02.MSG.045: сведения о внесении изменений в заявку на ТЗ Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.040` | **Процедура**: `P.SP.02.PRC.022` | **Операция**: `P.SP.02.OPR.104`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 63
- **Тесты**: PASS (27 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 35 | 24 | 0 | 3 | 1 | 7 | 0 | 24 | 11 |

**Записей в MISSING_DATA** (11):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipsdo:TrademarkApplicationId` | Requires external national patent-office resource check matching application id, status, and start date. |
| REQ 4 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Classifier lookup decides IPDocKindCode vs IPDocKindName presence for amendment document kinds. |
| REQ 5 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Classifier absence fallback requires specific IPDocKindName for amendment document kinds. |
| REQ 13 | `AMBIGUOUS` | `ipcdo:TrademarkApplicationDetails` | Table 44 globally says IPPartyKindCode is AP, whereas REQ21-22 recognize PA and RE party instances. |
| REQ 16 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Filtered/nested cardinality and correlation over repeated names and addresses. |
| REQ 17 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Filtered/nested cardinality and correlation over repeated names and addresses. |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Filtered/nested cardinality and correlation over repeated names and addresses. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Filtered/nested cardinality and correlation over repeated names and addresses. |
| REQ 20 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Filtered/nested cardinality and correlation over repeated names and addresses. |
| REQ 26 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | TrademarkKindCode or TrademarkKindName must be in normative set; cannot be safely replaced with AND. |
| REQ 30 | `ENGINE_UNSUPPORTED` | `ipsdo:IPPartyKindCode` | Conditional cross-collection correlation: application doc kind + AS party requires AccompanyingDocumentsDetails with mat |

### P.SP.02.MSG.046: сведения о преобразовании аннулированной регистрации ТЗ Союза в национальную заявку на регистрацию ТЗ

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.041` | **Процедура**: `P.SP.02.PRC.023` | **Операция**: `P.SP.02.OPR.112`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 64
- **Тесты**: PASS (26 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 9 | 6 | 3 | 0 | 0 | 0 | 0 | 9 | 0 |

**Записей в MISSING_DATA** (3):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 1 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 2 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` |  |
| REQ 3 | `SAFE_PARTIAL` | `ipsdo:TrademarkId` |  |

### P.SP.02.MSG.047: сведения о преобразовании коллективного знака Союза в ТЗ Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.042` | **Процедура**: `P.SP.02.PRC.024` | **Операция**: `P.SP.02.OPR.120`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 65
- **Тесты**: PASS (33 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 25 | 20 | 3 | 0 | 0 | 2 | 0 | 23 | 2 |

**Записей в MISSING_DATA** (5):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 1 | `SAFE_PARTIAL` | `ipsdo:TrademarkId` | Governed register record TrademarkId is required locally; verification of active registration status and equality in ext |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | If IPDocKindCode is present, IPDocKindName is forbidden; classifier membership is safe partial remainder. |
| REQ 5 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | If IPDocKindCode is absent, IPDocKindName must equal exact normative string; classifier absence is safe partial remainde |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires IPPartyDetails with kind UE. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires AccompanyingDocumentsDetails with charter |

### P.SP.02.MSG.048: сведения о преобразовании ТЗ Союза в коллективный знак Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.043` | **Процедура**: `P.SP.02.PRC.025` | **Операция**: `P.SP.02.OPR.128`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 66
- **Тесты**: PASS (33 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 25 | 20 | 3 | 0 | 0 | 2 | 0 | 23 | 2 |

**Записей в MISSING_DATA** (5):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 1 | `SAFE_PARTIAL` | `ipsdo:TrademarkId` | Governed register record TrademarkId is required locally; verification of active registration status and equality in ext |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | If IPDocKindCode is present, IPDocKindName is forbidden; classifier membership is safe partial remainder. |
| REQ 5 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | If IPDocKindCode is absent, IPDocKindName must equal exact normative string; classifier absence is safe partial remainde |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires IPPartyDetails with kind UE. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires AccompanyingDocumentsDetails with charter |

### P.SP.02.MSG.049: сведения о внесении изменений в сведения Единого реестра ТЗ Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.044` | **Процедура**: `P.SP.02.PRC.026` | **Операция**: `P.SP.02.OPR.136`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 67
- **Тесты**: PASS (21 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 24 | 19 | 3 | 0 | 0 | 2 | 0 | 22 | 2 |

**Записей в MISSING_DATA** (5):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 1 | `SAFE_PARTIAL` | `ipsdo:TrademarkId` | Local TrademarkId presence is executable; external resource status and equality checks remain outside local XML validati |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires IPPartyDetails with kind UE. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires AccompanyingDocumentsDetails with charter |
| REQ 21 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | When direct same-record IPDocKindCode is present, direct IPDocKindName is forbidden; classifier validity remains externa |
| REQ 22 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | When direct same-record IPDocKindCode is absent, direct IPDocKindName must equal the exact normative fallback literal; c |

### P.SP.02.MSG.050: сведения об отказе от исключительного права на ТЗ Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.045` | **Процедура**: `P.SP.02.PRC.027` | **Операция**: `P.SP.02.OPR.144`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 68
- **Тесты**: PASS (27 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 23 | 18 | 3 | 0 | 0 | 2 | 0 | 21 | 2 |

**Записей в MISSING_DATA** (5):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 1 | `SAFE_PARTIAL` | `ipsdo:TrademarkId` | Governed register record TrademarkId is required locally; verification of active registration status and equality in ext |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | If IPDocKindCode is present, IPDocKindName is forbidden; classifier membership is safe partial remainder. |
| REQ 5 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | If IPDocKindCode is absent, IPDocKindName must equal exact normative string; classifier absence is safe partial remainde |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires IPPartyDetails with kind UE. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires AccompanyingDocumentsDetails with charter |

### P.SP.02.MSG.051: сведения о признании предоставления правовой охраны ТЗ Союза недействительным (о прекращении правовой охраны)

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.046` | **Процедура**: `P.SP.02.PRC.028` | **Операция**: `P.SP.02.OPR.151`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 69
- **Тесты**: PASS (27 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 23 | 18 | 3 | 0 | 0 | 2 | 0 | 21 | 2 |

**Записей в MISSING_DATA** (5):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 1 | `SAFE_PARTIAL` | `ipsdo:TrademarkId` | Governed register record TrademarkId is required locally; verification of active registration status and equality in fil |
| REQ 3 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | If IPDocKindCode is present, IPDocKindName is forbidden; classifier membership is safe partial remainder. |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | If IPDocKindCode is absent, IPDocKindName must equal one of two exact normative strings; classifier absence is safe part |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires IPPartyDetails with kind UE. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires AccompanyingDocumentsDetails with charter |

### P.SP.02.MSG.052: сведения об аннулировании регистрации ТЗ Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.047` | **Процедура**: `P.SP.02.PRC.029` | **Операция**: `P.SP.02.OPR.155`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 70
- **Тесты**: PASS (22 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 31 | 19 | 6 | 0 | 0 | 6 | 0 | 25 | 6 |

**Записей в MISSING_DATA** (12):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 3 | `ENGINE_UNSUPPORTED` | `ipcdo:UnifiedRegisterRecordsDetails` | Requires data-dependent creation of a second record from nested goods state; current rules engine cannot express this cr |
| REQ 5 | `SAFE_PARTIAL` | `ipsdo:TrademarkId` | Cancellation-record TrademarkId is enforceable locally; matching active external-registry record remains external. |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipcdo:UnifiedRegisterRecordsDetails` | Inherited Table 49 requirement remains engine-unsupported under the authoritative classification. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipcdo:UnifiedRegisterRecordsDetails` | Inherited Table 49 requirement remains engine-unsupported under the authoritative classification. |
| REQ 20 | `SAFE_PARTIAL` | `ipsdo:TrademarkId` | New-registration TrademarkId is enforceable locally; external uniqueness check remains external. |
| REQ 21 | `ENGINE_UNSUPPORTED` | `ipcdo:UnifiedRegisterRecordsDetails` | Cross-record typed/date relationship is not representable by current rules engine. |
| REQ 22 | `ENGINE_UNSUPPORTED` | `ipcdo:UnifiedRegisterRecordsDetails` | Cross-record typed/date relationship is not representable by current rules engine. |
| REQ 24 | `ENGINE_UNSUPPORTED` | `ipcdo:UnifiedRegisterRecordsDetails` | Cross-record equality is not representable by current rules engine. |
| REQ 25 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | status-04 cancellation document-kind local branch is enforceable; classifier membership/absence remains external. |
| REQ 26 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | status-04 cancellation document-kind local branch is enforceable; classifier membership/absence remains external. |
| REQ 27 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | status-01 new-registration document-kind local branch is enforceable; classifier membership/absence remains external. |
| REQ 28 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | status-01 new-registration document-kind local branch is enforceable; classifier membership/absence remains external. |

### P.SP.02.MSG.053: сведения о продлении срока действия исключительного права на ТЗ Союза

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.048` | **Процедура**: `P.SP.02.PRC.030` | **Операция**: `P.SP.02.OPR.163`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.007`
- **Таблица ОП_22**: Table 71
- **Тесты**: PASS (26 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 26 | 18 | 3 | 0 | 0 | 5 | 0 | 21 | 5 |

**Записей в MISSING_DATA** (8):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 1 | `SAFE_PARTIAL` | `ipsdo:TrademarkId` | TrademarkId is required locally; external registry active status (StatusCode in 01, 03; EndDateTime empty; matching Trad |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | If IPDocKindCode is present, IPDocKindName is forbidden; classifier membership is safe partial remainder. |
| REQ 5 | `SAFE_PARTIAL` | `ipsdo:IPDocKindCode` | If IPDocKindCode is absent, IPDocKindName must equal exact normative string; classifier absence is safe partial remainde |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipcdo:UnifiedRegisterRecordsDetails` | Conditional cross-collection dependency: if CollectiveMarkIndicator == 1, IPPartyDetails with kind UE required. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipcdo:UnifiedRegisterRecordsDetails` | Conditional cross-collection dependency: if CollectiveMarkIndicator == 1, AccompanyingDocumentsDetails with charter docu |
| REQ 21 | `ENGINE_UNSUPPORTED` | `csdo:DocValidityDate` | External resource check: national patent office register contains matching TrademarkId and exactly one fewer DocValidity |
| REQ 22 | `ENGINE_UNSUPPORTED` | `csdo:DocValidityDate` | External resource check: all DocValidityDate values except one must match between external register and message. |
| REQ 23 | `ENGINE_UNSUPPORTED` | `csdo:DocValidityDate` | External resource check: the new DocValidityDate value in message (not matching external register) must be strictly grea |

### P.SP.02.MSG.054: запрос сведений о сумме и платежных реквизитах для уплаты пошлины

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.049` | **Процедура**: `P.SP.02.PRC.033` | **Операция**: `P.SP.02.OPR.176`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.03.003`
- **Таблица ОП_22**: Table 72
- **Тесты**: PASS (11 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 7 | 5 | 2 | 0 | 0 | 0 | 0 | 7 | 0 |

**Записей в MISSING_DATA** (2):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:IPLegalActionKindCode` | The locally observable code-present branch is executable; classifier availability and code membership require the extern |
| REQ 5 | `SAFE_PARTIAL` | `ipsdo:IPLegalActionKindCode` | The locally observable code-absent branch is executable, including required name and membership in the four Table 72 lit |

### P.SP.02.MSG.055: сведения о сумме и платежных реквизитах для уплаты пошлины

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.049` | **Процедура**: `P.SP.02.PRC.033` | **Операция**: `P.SP.02.OPR.177`
- **Направление**: RESPONSE | **Структура**: `R.IP.SP.03.003`
- **Таблица ОП_22**: Table 73
- **Тесты**: PASS (31 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 9 | 6 | 2 | 0 | 0 | 1 | 0 | 8 | 1 |

**Записей в MISSING_DATA** (3):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:IPLegalActionKindCode` | Local conditional predicate mapped: if IPLegalActionKindCode is present, IPLegalActionKindName is forbidden. External cl |
| REQ 5 | `SAFE_PARTIAL` | `ipsdo:IPLegalActionKindCode` | Local conditional predicate mapped: if IPLegalActionKindCode is absent, IPLegalActionKindName is required. External clas |
| REQ 7 | `ENGINE_UNSUPPORTED` | `ipcdo:IPPaymentDetails` | Normative requirement mandates IPPaymentDetails presence AND inclusive OR between BankAccountDetails and PaymentSystemAc |

### P.SP.02.MSG.056: запрос сведений о подтверждении уплаты пошлины

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.050` | **Процедура**: `P.SP.02.PRC.035` | **Операция**: `P.SP.02.OPR.183`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.03.003`
- **Таблица ОП_22**: Table 74
- **Тесты**: PASS (4 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 20 | 17 | 1 | 2 | 0 | 0 | 0 | 18 | 2 |

**Записей в MISSING_DATA** (3):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 19 | `SAFE_PARTIAL` | N/A |  |
| REQ 4 | `EXTERNAL` | N/A |  |
| REQ 5 | `EXTERNAL` | N/A |  |

### P.SP.02.MSG.057: сведения о подтверждении уплаты пошлины

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.050` | **Процедура**: `P.SP.02.PRC.035` | **Операция**: `P.SP.02.OPR.184`
- **Направление**: RESPONSE | **Структура**: `R.IP.SP.03.003`
- **Таблица ОП_22**: Table 75
- **Тесты**: PASS (41 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 22 | 18 | 2 | 2 | 0 | 0 | 0 | 20 | 2 |

**Записей в MISSING_DATA** (4):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 4 | `EXTERNAL` | `ipsdo:IPLegalActionKindCode` | External dependency: applies upon inclusion of legal action classifier in Union unified NSI resources. |
| REQ 5 | `EXTERNAL` | `ipsdo:IPLegalActionKindCode` | External dependency: applies upon absence of legal action classifier in Union unified NSI resources. |
| REQ 19 | `SAFE_PARTIAL` | `csdo:DocBinaryText` | DocBinaryText is required and mediaTypeCode attribute must be one of allowed extensions. Payload size <= 5MB is unmapped |
| REQ 22 | `SAFE_PARTIAL` | `ipsdo:DutyPaymentIndicator` | If DutyPaymentIndicator is 'false', PaymentAmount must be present. Numeric constraint PaymentAmount > 0 is unmapped due  |

### P.SP.02.MSG.058: запрос материалов и документов, используемых в ходе регистрации или иных процедур, связанных с ТЗ Союза

- **Статус**: `FINAL_READY`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.051` | **Процедура**: `P.SP.02.PRC.036` | **Операция**: `P.SP.02.OPR.186`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.008`
- **Таблица ОП_22**: Table 76
- **Тесты**: PASS (3 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 7 | 7 | 0 | 0 | 0 | 0 | 0 | 7 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.059: материалы и документы, используемые в ходе регистрации или иных процедур, связанных с ТЗ Союза

- **Статус**: `PARTIAL_AMBIGUOUS`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.051` | **Процедура**: `P.SP.02.PRC.036` | **Операция**: `P.SP.02.OPR.187`
- **Направление**: RESPONSE | **Структура**: `R.010`
- **Таблица ОП_22**: Table 77/78/79
- **Тесты**: PASS (82 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 11 | 7 | 2 | 0 | 2 | 0 | 0 | 9 | 2 |

**Записей в MISSING_DATA** (4):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 4 | `SAFE_PARTIAL` | `csdo:DocBinaryText` | Within each AccompanyingDocumentsDetails instance, DocBinaryText is required and mediaTypeCode attribute must be one of  |
| REQ 5 | `AMBIGUOUS` | `R.IP.SP.02.002` | The requirement 'другие реквизиты не заполняются' does not specify which elements or scope are considered 'other' (e.g., |
| REQ 4 | `SAFE_PARTIAL` | `csdo:DocBinaryText` | Within each AccompanyingDocumentsDetails instance, DocBinaryText is required and mediaTypeCode attribute must be one of  |
| REQ 5 | `AMBIGUOUS` | `R.IP.SP.02.007` | The requirement 'другие реквизиты не заполняются' does not specify which elements or scope are considered 'other' (e.g., |

### P.SP.02.MSG.060: NORMATIVELY_ABSENT

- **Статус**: `NORMATIVELY_ABSENT`
- **Существование**: NO
- **Транзакция**: `None` | **Процедура**: `None` | **Операция**: `None`
- **Направление**: None | **Структура**: `None`
- **Таблица ОП_22**: NORMATIVELY_ABSENT
- **Тесты**: N/A

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Нет записей в MISSING_DATA (полностью покрыто или нормативно отсутствует).

### P.SP.02.MSG.061: обращение заинтересованного лица

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.052` | **Процедура**: `P.SP.02.PRC.008` | **Операция**: `P.SP.02.OPR.190`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 80
- **Тесты**: PASS (36 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 40 | 31 | 1 | 2 | 1 | 5 | 0 | 32 | 8 |

**Записей в MISSING_DATA** (9):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipsdo:IPDocKindCode` | External classifier/resource semantics are not executable. |
| REQ 3 | `EXTERNAL` | `ipsdo:IPDocKindCode` | External classifier/resource semantics are not executable. |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | Local identifier presence is executable; external national patent office resource state/equality is not. |
| REQ 13 | `AMBIGUOUS` | `ipsdo:IPPartyKindCode` | Normative owner scope is ambiguous. |
| REQ 16 | `ENGINE_UNSUPPORTED` | `@nameRepresentationKindCode` | No safe exact evaluator expression. |
| REQ 17 | `ENGINE_UNSUPPORTED` | `@nameRepresentationKindCode` | No safe exact evaluator expression. |
| REQ 18 | `ENGINE_UNSUPPORTED` | `@nameRepresentationKindCode` | No safe exact evaluator expression. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `@nameRepresentationKindCode` | No safe exact evaluator expression. |
| REQ 20 | `ENGINE_UNSUPPORTED` | `ccdo:CommunicationDetails` | No safe exact evaluator expression. |

### P.SP.02.MSG.062: доводы заявителя в отношении обращения заинтересованного лица

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.053` | **Процедура**: `P.SP.02.PRC.009` | **Операция**: `P.SP.02.OPR.194`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 81
- **Тесты**: PASS (37 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 39 | 33 | 1 | 2 | 1 | 2 | 0 | 34 | 5 |

**Записей в MISSING_DATA** (6):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Classifier inclusion condition is external. |
| REQ 3 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Classifier absence condition is external. |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | Local identifier presence is executable; external national patent office resource state/equality is not. |
| REQ 13 | `AMBIGUOUS` | `ipcdo:TrademarkApplicationDetails` | Inherited Table 81 -> Table 44 -> Table 34 rule 13. |
| REQ 18 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Inherited Table 81 -> Table 44 -> Table 34 rule 18. |
| REQ 19 | `ENGINE_UNSUPPORTED` | `ipcdo:TrademarkApplicationDetails` | Inherited Table 81 -> Table 44 -> Table 34 rule 19. |

### P.SP.02.MSG.063: сведения о признании заявки на ТЗ Союза отозванной по причине неуплаты пошлин

- **Статус**: `PARTIAL_EXTERNAL`
- **Существование**: YES
- **Транзакция**: `P.SP.02.TRN.054` | **Процедура**: `P.SP.02.PRC.034` | **Операция**: `P.SP.02.OPR.198`
- **Направление**: REQUEST | **Структура**: `R.IP.SP.02.002`
- **Таблица ОП_22**: Table 82
- **Тесты**: PASS (17 tests)

| Всего | FULL | PART | EXT | AMB | ENG | CONF | Exec | Unmap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 4 | 1 | 1 | 2 | 0 | 0 | 0 | 2 | 2 |

**Записей в MISSING_DATA** (3):

| Требование | Класс | XML QName | Причина |
|:---|:---|:---|:---|
| REQ 2 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Normative condition depends on whether the classifier includes a code value for document kind 'Уведомление о признании з |
| REQ 3 | `EXTERNAL` | `ipsdo:IPDocKindCode` | Normative condition depends on whether the classifier lacks a code value for document kind 'Уведомление о признании заяв |
| REQ 4 | `SAFE_PARTIAL` | `ipsdo:TrademarkApplicationId` | Presence of TrademarkApplicationId inside TrademarkApplicationDetails is required and safe to map locally. The remainder |

