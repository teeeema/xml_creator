# OP23 / P.SP.03 — повторный аудит текущей реализации

Дата аудита: 2026-10-05. Этап: read-only re-audit после изменений общего rules engine, без исправления production code.

## Scope и источники

- OP: OP23; process: P.SP.03; version context: 1.0.0.
- Текущий package: `P.SP.03_OP_23/`.
- Нормативный документ `ОП_23.pdf` многократно указан в `source_refs`, с page/table/item, но физического PDF в текущем checkout **нет**. Поэтому номера страниц ниже являются сохраненными CONFIRMED metadata проекта и не были повторно визуально сверены с PDF в этом запуске.
- Локальные структуры: R.006/Y.Y.Y, R.IP.SP.03.001/1.0.0, .002/1.0.0, .003/1.0.0, .007/1.0.0.
- XSD OP23 в checkout не найден. Официальные classifier snapshots OP23 в checkout не найдены.
- Старые `codex_reports/OP23_*` использованы только для сравнения и для обнаружения прежних классификаций; inventory построен заново из текущих message rule tables.

## Главный результат

Текущие 21 таблица правил содержат 400 строк `business_rules`, но диапазоны требований разворачиваются в **710 canonical requirements**. Это подтверждается существующим тестом OP23, который ожидает coverage=710.

Во всех 21 rule-файлах OP23 сейчас `structured_rules=[]`, `correlation_rules=[]`, `fixed_values={}`, `field_usage={}`. Поэтому по строгим критериям этого аудита **IMPLEMENTED_CONFIRMED = 0**: нет requirement-specific production rule, вызова, positive/negative rejection proof и regression test для каждого требования.

## Итоговые счетчики

- OP23_TOTAL_REQUIREMENTS: **710**
- IMPLEMENTED_CONFIRMED: **0**
- OPEN_GAPS: **710**

### OPEN_BY_REASON
- OPEN_ENGINE: 0
- OPEN_PRODUCTION_MAPPING: 627
- OPEN_CLASSIFIER: 44
- OPEN_EXTERNAL_REGISTRY: 39
- OPEN_NORMATIVE_AMBIGUITY: 0
- OPEN_SOURCE_CONFLICT: 0
- OPEN_MISSING_STRUCTURE: 0
- OPEN_MISSING_NORMATIVE_DATA: 0
- OTHER_OPEN: 0

## Что произошло со старыми ENGINE GAP

Старый аудит содержал 36 `ENGINE_UNSUPPORTED`. Текущий `rules_engine.py` имеет positional `position`, conditional `where`, recursive `any/all/not`, `selection_cardinality`, count guards, typed datetime comparison и `cross_instance_comparison`; соответствующие tests присутствуют. Поэтому старый engine-level диагноз для этих 36 строк устарел.

Требования при этом **не закрыты**: OP23 production mapping их не использует. Они reclassified в `OPEN_PRODUCTION_MAPPING`. `STALE_GAPS_CLOSED_BY_CURRENT_IMPLEMENTATION = 0` на уровне требований; engine-причина исчезла, но requirement остается open.

## Сравнение со старым аудитом

- OLD_TOTAL_REQUIREMENTS: **400** (старый аудит считал строки business_rules, а не развёрнутые canonical REQ)
- NEW_TOTAL_REQUIREMENTS: **710**
- OLD_GAPS: **243**
- NEW_GAPS: **710**
- OLD_ENGINE_GAPS: **36**
- NEW_ENGINE_GAPS: **0**
- STALE_GAPS_CLOSED_BY_CURRENT_IMPLEMENTATION: **0**
- NEWLY_DISCOVERED_GAPS: **467** относительно старого row-based baseline.

Разница 467 состоит арифметически из 157 требований/строк, которые старый аудит называл executable, но которые не имеют текущего production mapping, и +310 canonical requirements, появившихся при корректном разворачивании диапазонов. Это сравнение не означает, что нормативный документ добавил 467 новых норм.

Старая единственная `AMBIGUOUS` строка MSG.023 REQ 13 не перенесена автоматически: сохраненный old reason говорит про scope `AP`, тогда как captured source_text текущего REQ 13 задаёт условие для `PA`/`RE` и допустимые страны. Текущие материалы не подтверждают два нормативных толкования; проблема остается production mapping.

## Проверка inventory

- PRC catalog: **12**.
- TRN catalog: **19**.
- MSG catalog: **27**, из них **21** с отдельными rule tables.
- Сумма canonical requirements по MSG: **710**.
- Сумма canonical requirements по TRN: **710**.
- Сумма canonical requirements по PRC: **710**.
- Duplicate canonical_requirement_id: **0**.
- Requirement одновременно IMPLEMENTED и OPEN: **0**.
- GAP без trace_source_refs: **0**.
- GAP без причины/plain_explanation: **0**.

## Тесты

- OP23: `PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.03_OP_23/tests` → **3 passed, 27 subtests passed**.
- Full regression: `PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q` → **3586 passed, 62348 subtests passed**.
- OP22 targeted regression: `PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests` → **3103 passed**.

## Арифметика

`710 = 0 + 710` — PASS.

PRC/TRN/MSG distribution sums all equal 710 — PASS. Canonical IDs unique — PASS.
