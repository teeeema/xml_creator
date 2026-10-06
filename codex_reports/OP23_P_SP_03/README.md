# OP23_P_SP_03 audit workspace

- OP: **OP23**
- process: **P.SP.03**
- назначение: изолированное хранение результатов повторного аудита OP23; отчеты других ОП и общие FINAL_DELIVERY-файлы сюда не входят.
- дата/этап: **2026-10-05, re-audit current repository baseline after shared rules-engine improvements; production code unchanged**.

## Нормативные источники

- `ОП_23.pdf`, P.SP.03 version context 1.0.0 — referenced by current CONFIRMED `source_refs` with pages/tables/items, but the PDF file is absent from the current checkout, so visual page verification was not possible in this run.
- Local structure definitions: `P.SP.03_OP_23/structures/` (R.006; R.IP.SP.03.001/.002/.003/.007).
- OP23 XSD: **not found locally**.
- Official OP23 classifier snapshots: **not found locally**.
- Current source_refs/message rules/catalog YAML under `P.SP.03_OP_23/`.

## Файлы

- `OP23_REAUDIT_GAPS.csv` — одна строка на каждый открытый canonical requirement/GAP, с причиной, простым объяснением, источником, трассировкой и критерием закрытия.
- `OP23_REAUDIT_REQUIREMENTS.csv` — полный canonical inventory требований, включая статус каждого требования.
- `OP23_REAUDIT_MESSAGE_MATRIX.csv` — матрица 27 сообщений и распределение 710 требований.
- `OP23_REAUDIT_TRANSACTION_MATRIX.csv` — матрица 19 транзакций и их требования.
- `OP23_REAUDIT_AUDIT.md` — развернутый итог аудита, сравнение со старым baseline и проверки.
- `README.md` — индекс этой папки.

## Итоги

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

## Тесты

- OP23: **3 passed, 27 subtests passed**.
- Full regression: **3586 passed, 62348 subtests passed**.
- OP22 targeted: **3103 passed** (`PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests`).

## Проверки

- ARITHMETIC_CHECK: **PASS** (`710 = 0 + 710`; PRC/TRN/MSG sums = 710).
- TRACEABILITY_CHECK: **PASS** (0 GAP без `trace_source_refs`).
- DUPLICATE_CHECK: **PASS** (0 duplicate canonical_requirement_id).
- SOURCE_REVERIFY: **LIMITED** — `ОП_23.pdf` отсутствует физически в checkout; source page/table values взяты из текущих CONFIRMED source_refs.
