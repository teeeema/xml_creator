# OP23 TRACEABILITY AUDIT

REQUIREMENTS_CHECKED: 710
FULL_TRACE: 310
PARTIAL_TRACE: 400
BROKEN_TRACE: 0

Метод: canonical inventory берётся из `knowledge_base/requirements`; source document hashes сверены с оригиналами в `/Users/tema/Documents/Work/Документы_xml`; current production linkage строится из текущих `message_rules/*.yaml`; requirement-specific test evidence берётся только когда есть явная positive+negative связь с этим requirement. Общий зелёный suite сам по себе не считается индивидуальным доказательством требования. Для inherited OP22 источник считается корректным, если сохранены current/leaf provenance; различие страницы текущего диапазона и semantic leaf не считается ошибкой само по себе.

Runtime `NOT_APPLICABLE` не использовался: все 2520 строки являются XML/business validation constraints с runtime-семантикой после выполнения нормативных/внешних prerequisites.

## Current findings

- Current structured-rule objects: **598**; canonical requirements with current structured-rule linkage: **474**.
- **310** requirements have current structured rules plus positive and negative real-XML proof through `P.SP.03_OP_23/tests/test_b1_production.py` and are FULL_TRACE.
- **400** remain PARTIAL_TRACE: their canonical source/structure linkage exists, but individual production/test closure is absent. Historical `OP23_REAUDIT_AUDIT.md` is stale because it predates the current structured-rule population.

## Broken trace examples

- None confirmed.

## Verification

- Original PDF SHA256 values match `knowledge_base/02_SOURCE_REGISTRY.md`.
- Current process regression run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests P.SP.03_OP_23/tests P.MM.01_OP_26/tests -p no:cacheprovider` → **3829 passed, 110 subtests passed, 0 failed**.
- Production and KB were not modified by this audit.
