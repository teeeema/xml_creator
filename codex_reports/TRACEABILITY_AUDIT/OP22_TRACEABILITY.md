# OP22 TRACEABILITY AUDIT

REQUIREMENTS_CHECKED: 1609
FULL_TRACE: 141
PARTIAL_TRACE: 1467
BROKEN_TRACE: 1

Метод: canonical inventory берётся из `knowledge_base/requirements`; source document hashes сверены с оригиналами в `/Users/tema/Documents/Work/Документы_xml`; current production linkage строится из текущих `message_rules/*.yaml`; requirement-specific test evidence берётся только когда есть явная positive+negative связь с этим requirement. Общий зелёный suite сам по себе не считается индивидуальным доказательством требования. Для inherited OP22 источник считается корректным, если сохранены current/leaf provenance; различие страницы текущего диапазона и semantic leaf не считается ошибкой само по себе.

Runtime `NOT_APPLICABLE` не использовался: все 2520 строки являются XML/business validation constraints с runtime-семантикой после выполнения нормативных/внешних prerequisites.

## Current findings

- Current structured-rule objects: **1643**; canonical requirements with a current structured-rule linkage: **1159**.
- Requirement-specific positive+negative proof is recorded for **142** canonical rows, but one row has a wrong table link, leaving **141 FULL_TRACE**.
- Confirmed broken row: `P.SP.02.MSG.031:49:19`. Its canonical source is Table 49 item 19 / page 740, but positive, negative and runtime test references point to parameter `...MSG.031-48`, i.e. Table 48 requirement 19. The actual Table 49 requirement remains unmapped in structured rules.
- The remaining partial rows are mostly current executable/structural coverage without individual positive+negative certification, or open classifier/external/source/mapping gaps. This follows the current KB and the explicit caveat in `codex_reports/FINAL_DELIVERY_AUDIT.md` that non-FIX implemented rows were not individually positive/negative certified.

## Broken trace examples

- `P.SP.02.MSG.031:49:19` — WRONG_TEST_LINK: Requirement-specific proof references a different OP22 table/requirement identity: [('positive', [('19', 'P.SP.02.MSG.031', '48'), ('19', 'P.SP.02.MSG.031', '48')]), ('negative', [('19', 'P.SP.02.MSG.031', '48'), ('19', 'P.SP.02.MSG.031', '48')]), ('runtime', [('19', 'P.SP.02.MSG.031', '48'), ('19', 'P.SP.02.MSG.031', '48'), ('19', 'P.SP.02.MSG.031', '48'), ('19', 'P.SP.02.MSG.031', '48')])] | Missing/incomplete: CURRENT_PRODUCTION_RULE_LINK; POSITIVE_TEST; NEGATIVE_TEST; RUNTIME_PROOF

## Verification

- Original PDF SHA256 values match `knowledge_base/02_SOURCE_REGISTRY.md`.
- Current process regression run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q P.SP.02_OP_22/tests P.SP.03_OP_23/tests P.MM.01_OP_26/tests -p no:cacheprovider` → **3829 passed, 110 subtests passed, 0 failed**.
- Production and KB were not modified by this audit.
