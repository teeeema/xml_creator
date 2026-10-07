# OP23 / P.SP.03 — индекс отчётов

Дата: 2026-10-06. Этап: продолжающаяся реализация безопасных требований OP23; **этап ещё не завершён**. Отчёты OP22, OP26 и общие `FINAL_DELIVERY_*` здесь не изменялись.

Нормативная основа: `/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf` (P.SP.03, версия 1.0.0), локальные `P.SP.03_OP_23/message_rules/`, `structures/` и `source_refs`. OP23 XSD, официальный snapshot классификаторов и внешние реестры не найдены. 18 QName-конфликтов и MSG.025.REQ.006 не разрешались предположением.

## Текущий снимок

- OP23_TOTAL_REQUIREMENTS: **710**; IMPLEMENTED_CONFIRMED: **90**; OPEN_GAPS: **620**.
- SAFE_TOTAL: **608**; закрыто с production wiring и positive/negative real XML: **90**; ещё не обработано: **518**.
- Batch: B1 **63/162**, B2 **14/214**, B3 **10/159**, B4 **3/73**.
- OPEN_BY_REASON: ENGINE **0**, PRODUCTION_MAPPING **518**, CLASSIFIER **44**, EXTERNAL_REGISTRY **39**, SOURCE_CONFLICT **18**, MISSING_NORMATIVE_DATA **1**; остальные **0**.
- Арифметика: **PASS** (`90 + 620 = 710`; `90 + 518 = 608`; `518 + 44 + 39 + 18 + 1 = 620`).
- Статус: **INCOMPLETE**. 518 safe ID остаются `NOT_PROCESSED`, а не выданы за доказанные blockers.

## Последняя реализованная последовательность

- MSG.022: закрыты REQ.001/.002/.003/.006/.007/.008/.009. REQ.004/.005 оставлены внешними, поскольку зависят от наличия справочника.
- MSG.023: закрыты 17 требований: REQ.001/.002/.003/.006–.018/.020. REQ.004/.005 зависят от справочника; REQ.019 не закрыт из-за недоказанной проверки ограничения бинарного документа 5 МБ.
- MSG.024: закрыты унаследованные REQ.001/.002/.003/.006–.018 и локальные REQ.020–.022. Для денежных сравнений добавлена общая typed `DECIMAL` semantics; `0.00` корректно считается нулём.

## Тесты на текущем снимке

- `P.SP.03_OP_23/tests/test_b1_production.py`: **125 passed**.
- Весь OP23: **128 passed, 27 subtests passed**.
- Общий structured rules engine: **41 passed, 5 subtests passed**.
- Полный repository suite после этой пачки: **NOT RUN**; широкий gate будет повторён перед финальным закрытием safe-реестра.

## Файлы

- `OP23_REAUDIT_*`, `OP23_PRODUCTION_MAPPING_TRIAGE.*`, `OP23_SOURCE_REVERIFY.*` — исторические этапы; не перезаписывались.
- `OP23_SAFE_IMPLEMENTATION_BATCH_MAP.csv` и `OP23_B1_IMPLEMENTATION_RESULTS.csv` … `OP23_B4_IMPLEMENTATION_RESULTS.csv` — актуальный план и построчные результаты 608 safe ID.
- `OP23_FINAL_REQUIREMENTS.csv` — текущие 710 статусов; `OP23_FINAL_GAPS.csv` — 620 открытых требований.
- `OP23_FINAL_MESSAGE_MATRIX.csv`, `OP23_FINAL_TRANSACTION_MATRIX.csv`, `OP23_FINAL_IMPLEMENTATION_AUDIT.md` — агрегаты и проверенный текущий снимок.
