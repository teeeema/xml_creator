# OP23 / P.SP.03 — implementation snapshot (2026-10-06)

STATUS: **INCOMPLETE**. Из 608 безопасно локализованных требований 90 закрыты production wiring и positive/negative real XML; 518 остаются `NOT_PROCESSED`.

## Реализовано

Текущая последовательность MSG.022–MSG.024 добавила 43 canonical ID. Для диапазонного наследования использованы canonical ID из `OP23_FINAL_REQUIREMENTS.csv`, а source trace содержит одновременно локальную строку диапазона (`1-6` или `1-19`) и исходное унаследованное требование. Нумерация YAML business rows не использовалась как canonical numbering.

MSG.023.REQ.019 не закрыт частично: engine может проверить наличие binary/MIME, но пока нет доказанной проверки фактического размера ≤5 МБ. MSG.022/023/024 REQ.004/.005 также остаются открытыми из-за внешнего состояния справочника.

Для MSG.024 REQ.021/.022 в общем evaluator добавлен `DECIMAL` для числового сравнения сумм и поддержка `value_type` внутри condition. Это устраняет ошибочное строковое сравнение вроде `"0.00" > "0"`.

## Нормативная основа

CONFIRMED: `ОП_23.pdf`, P.SP.03 version 1.0.0, локальные confirmed `source_refs` и структуры R.IP.SP.03.*. QName/path и значения правил не выводились из отсутствующей XSD или классификаторов.

Открытые внешние/источниковые группы: CLASSIFIER **44**, EXTERNAL_REGISTRY **39**, SOURCE_CONFLICT **18**, MISSING_NORMATIVE_DATA **1**.

## Проверки

- Production real XML: **125 passed**.
- Весь OP23: **128 passed, 27 subtests passed**.
- Structured rules engine: **41 passed, 5 subtests passed**.
- Full repository suite: **NOT RUN** после этой пачки.

## Арифметика

`90 + 620 = 710`; `90 + 518 = 608`; `518 + 44 + 39 + 18 + 1 = 620` — **PASS**.
