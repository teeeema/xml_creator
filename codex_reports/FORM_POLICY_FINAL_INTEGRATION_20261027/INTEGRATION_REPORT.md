# Финальная интеграция FORM_POLICY — 27 октября 2026

## Вердикт: SUCCESS — локальная интеграция завершена

Применён только согласованный MINIMAL_INTEGRATION.patch: 10 файлов, 406 additions / 11 deletions. SHA-256 `2be8992f5e6033073c661a0cb3a578e2474b696908d2bc7d9ebed49ee336b14b` совпал с обоими отчётами. Перед записью повторно проверены все 963 baseline hashes, HEAD и git apply --check --whitespace=error-all. Все 9 существующих целей совпадали с before manifest; десятая отсутствовала. Семантического расхождения базы нет. Чужие dirty prerequisites были согласованной частью базы, не пересекаются с патчем и сохранены побайтно.

HEAD до/после: `9864e456a443921f4cc99025260ff5a1122b9009`; ветка `feature/op26-v1.3.0`. Существующее расхождение с origin (2 локальных / 1 удалённый commit) не менялось. main и backup-ветки не изменялись. Commit/push/pull/merge/rebase/reset/restore/clean/stash не выполнялись.

## Резервная копия и обратимость

Внешняя уникальная директория: `/Users/tema/Documents/Work/FORM_POLICY_INTEGRATION_BACKUP_20261027_112444_8227f302`. Содержит originals всех 963 git-visible baseline файлов, включая чужие untracked, SHA256 manifest, status/porcelain, binary diff и cached diff, HEAD/branch/refs/log и копию патча. Новая цель теста до интеграции отсутствовала. Исходные материалы не перезаписывались, ничего не удалялось.

При будущей регрессии предлагается только отдельная обратная дельта данной интеграции после повторной проверки пересечений; никакой автоматический откат или замена целых файлов не выполнялись. Чужие resolver/services, untracked tests и reports должны остаться сохранными.

## Четыре исправления

1. ОП23 MSG.023: REQUIRED для ApellationOfOriginApplicationId, заполненность scalar и реальная XML positive/negative проверка (табл27 → табл25).
2. ОП23 MSG.001: обязательные UnifiedCountryCode/AuthorityName только внутри присутствующего PatentAuthorityDetails; независимые повторяющиеся контексты; отсутствующий optional parent допустим.
3. ОП26 MSG.027 1.1.0: structured presence RegistrationNumberId дополняет прежний field_usage и отклоняет None/empty/whitespace.
4. ОП26 MSG.001 1.1.0: country-only FIXED codeListId=P.CLS.019 в 11 путях, READ_ONLY projection и отрицательная проверка 2021. Идентификатор классификатора не отождествлён с literal без основания: PDF213/R34 прямо требует «кодовое обозначение» из VII, а PDF39/табл10 задаёт P.CLS.019. Это отдельно проверено read-only reviewer по первичному PDF.

Две узкие правки body provider: передача существующей structure metadata для scalar/container presence и распознавание объявленного RELATIVE по точному QName. Не введён второй валидатор или local-name обход. field_usage и structured presence могут давать перекрывающиеся missing-key diagnostics; дедупликация диагностик не заявляется. Дублированных structured rule IDs нет.

## Пять разрешённых конфликтов тестов

- priority_field_examples_are_safe_and_origin_traced: точный country path получает нормативный FIXED_VALUE вместо instructional placeholder.
- large_message_form_filters_preserve_counts_hierarchy_and_performance: 401/297 manual и filters 401/145/387; проверено точное множество 11 country attributes, все 401 visible и hierarchy/performance guards сохранены.
- ui_policy_keeps_normative_source_separate_and_forms_usable: unresolved source metadata отделена от доказанного effective FIXED; остальные поля остаются USER_INPUT.
- every_branch_is_typed_and_expected_counts_are_stable: assertions 37/3/3 сохранены; helper учитывает FIXED только для выбранных synthetic полей.
- artifacts_cover_matrix_and_are_machine_readable: точное множество artifacts и assertions сохранены; изменён только synthetic INITIATING_001, response XML сохранены.

Skip/xfail или ослабления assertions ради PASS не добавлялись. Исходный structured form policy module не изменён.

## Свежие проверки в основном дереве

Python 3.13, PYTHONDONTWRITEBYTECODE=1, pytest -q -p no:cacheprovider, PYTHONPATH=eaeu_xml/src. GUI: QT_QPA_PLATFORM=offscreen, отдельный процесс на модуль.

| Набор | Результат |
|---|---|
| Сначала targeted: structured form policy + reconciled rules + legacy facade + E2E | 62 passed, 69 subtests |
| Полный backend: 58 модулей | 722 passed, 2450 subtests, 0 failed |
| GUI/Presentation: 9 модулей отдельно | 74 passed, 0 failed |

Все 67 верхнеуровневых test_*.py шести каталогов обнаружены и выполнены; пропущенных модулей нет. Мультимножества JUnit (classname, name, outcome) полностью совпали с подготовленными final backend/GUI и transfer focused: нет пропавших, новых либо изменивших результат test IDs. Backend имеет 722 testcase occurrences, но 700 уникальных classname/name из-за повторных идентификаторов; сравнение выполнено с multiplicity, не только по числам. Наборы focused не суммируются с backend.

ОП22: protected contract, карточки/описания/regex, 07220/07320/07360/07365, P.CLS.027, XML и drafts покрыты свежим backend/GUI. Все baseline файлы ОП22 сохранены побайтно.
ОП49: full message/pipeline/generator и TestDataGenerator safety PASS; align_sample_attributes в чужом services не изменён, пользовательские значения не санитизируются патчем. Все baseline файлы ОП49 сохранены.
Также PASS: ОП23/26/32, Application Facade, XML serialization/extraction/validation, version selection, readiness и stage3 component tests. GUI Cocoa/SIGABRT не воспроизведён при изолированном offscreen запуске. Это не ручной smoke-test нативного оконного режима.

## Нормативные версии и оставшиеся блокировки

1.1.0 остаётся default; действующее версионирование и E2E совместимы. Каталог 1.3.0 побайтно неизменён: отдельный literal 2021, DRAFT_NOT_READY, promotion_allowed=false и запрет production activation сохранены. Артефакты этапов 1–3 не перезаписывались, их тесты входят в прогон.
Официальный effective model QName/XSD payload по-прежнему не получен; 591 QName не разрешён по подготовленным source reports. XML proofs — TEST/runtime, НЕ official XSD validation. Релиз/promotion 1.3.0 остаётся SOURCE_BLOCKED.

## Git, сохранность и ограничения

Новых регрессий в выполненных наборах не выявлено. Все 10 after SHA совпадают с проверенным candidate. Финальная сверка остальных 954 baseline файлов: ни одного изменения. Чужие message_field_policy/services и оба untracked protected/safety tests сохранены. AGENTS не менялись. project_memory/ в корне и eaeu_xml отсутствует; новые нормативные или архитектурные решения вне патча не вводились, memory документы не создавались.
Graphify AST update выполнен успешно, локальные ignored generated graph артефакты обновлены; LLM label refresh не запускался. Кроме разрешённого патча добавлен только этот отдельный evidence/report комплект. Рабочее дерево намеренно dirty, индекс не изменялся; полный status приведён отдельно.

## SHA-256 всех целей до/после

| Файл | До | После |
|---|---|---|
| [P.MM.01_OP_26/examples/all_transactions/TRN.001/INITIATING_001.xml](</Users/tema/Documents/Work/xml_creator/P.MM.01_OP_26/examples/all_transactions/TRN.001/INITIATING_001.xml>) | `c089106f357c2ce95d9a6e5cce8fafe5db1f0b112c8da836e3366eec6594bd97` | `fcf620af15427278a1173f876aaab474dcc60c6345a5eec2c205101f0cdb5591` |
| [P.MM.01_OP_26/message_rules/P.MM.01.MSG.001.yaml](</Users/tema/Documents/Work/xml_creator/P.MM.01_OP_26/message_rules/P.MM.01.MSG.001.yaml>) | `2adc85bba0fe5b40e4735b0ea74dd11a995cc23e71848109c4844302d0ed3019` | `9a6b7056260f3fd4a4f7ff01d127e57f91016a32736a2d69abea2d673213f8b6` |
| [P.MM.01_OP_26/message_rules/P.MM.01.MSG.027.yaml](</Users/tema/Documents/Work/xml_creator/P.MM.01_OP_26/message_rules/P.MM.01.MSG.027.yaml>) | `37393fbe817ac3a8716d75bb7b2d0f4201d105122a0126b48d4424d90ceffe40` | `f1df859568defa8e0c2d98ffb44022f5f37440b7a3159d4323056453442ebcf7` |
| [P.MM.01_OP_26/tests/all_transactions_matrix.py](</Users/tema/Documents/Work/xml_creator/P.MM.01_OP_26/tests/all_transactions_matrix.py>) | `0318cf6f287c173d4ba7195d98950e91e1a66261a81484873570d3f481a746ad` | `29139bfe7281b993dca8f537a8e752a4677b943596b76c7c58a1417f69aa6d7c` |
| [P.MM.01_OP_26/tests/test_all_transactions_e2e.py](</Users/tema/Documents/Work/xml_creator/P.MM.01_OP_26/tests/test_all_transactions_e2e.py>) | `64d7818e3102f518f74b84f67aebb5da352ef725b28dabd00ec23cae8fd4f1d8` | `46ba87ab545c95bbc7398fff13206ccf2f771508e51dda54f5fa87a37207785f` |
| [P.MM.01_OP_26/tests/test_application_facade_pmm01.py](</Users/tema/Documents/Work/xml_creator/P.MM.01_OP_26/tests/test_application_facade_pmm01.py>) | `a563792db2e4360efe0e31c874eaf4e6ed51af1d79cebc7bd1f1fe348ac3fb30` | `23ebeb9c051a1f54cab50e76f76244c725270910e8804c0c1a2242a6bc589bcd` |
| [P.SP.03_OP_23/message_rules/P.SP.03.MSG.001.yaml](</Users/tema/Documents/Work/xml_creator/P.SP.03_OP_23/message_rules/P.SP.03.MSG.001.yaml>) | `db0e9c4fef2960992fbdb0fae2e8c1c0f97304bd18551065cd14b24c75d6575c` | `727b96cf478fda7a9b4a0601b039960e6ce9ec56bddcfb04988b8efbea108f17` |
| [P.SP.03_OP_23/message_rules/P.SP.03.MSG.023.yaml](</Users/tema/Documents/Work/xml_creator/P.SP.03_OP_23/message_rules/P.SP.03.MSG.023.yaml>) | `36d0780f8b0e6f6e94e2d2989e23788480f8a0916ca8fea5393fa439478f6ee8` | `177bd554950565600e97ede3100e144884dba393e17a729c76ee04683dfde29a` |
| [eaeu_xml/src/eaeu_xml/process_packages/body.py](</Users/tema/Documents/Work/xml_creator/eaeu_xml/src/eaeu_xml/process_packages/body.py>) | `63c9a4524bed30621c4ee2b135d1ee7e2b637018c1c1f2a7c8f6e46315f2bd97` | `6e37fe016bfbf8f8c43f1d2e81f4709ad366c46705f91fe0a3b360ea3705ddd8` |
| [eaeu_xml/tests/test_reconciled_normative_rules.py](</Users/tema/Documents/Work/xml_creator/eaeu_xml/tests/test_reconciled_normative_rules.py>) | `ABSENT` | `fc9c08ce17d459e9907259d7c4ef88f08d10b5fd9aa8bb7304a46bc8ec7c04a1` |

## Доказательства

- [PRECHECK.json](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/PRECHECK.json>)
- [HASHES_BEFORE_AFTER.json](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/HASHES_BEFORE_AFTER.json>)
- [TEST_ID_COMPARISON.json](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/TEST_ID_COMPARISON.json>)
- [backend.log](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/backend.log>)
- [backend_runs.json](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/backend_runs.json>)
- [gui_runs.json](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/gui_runs.json>)
- [focused.log](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/focused.log>)
- [GIT_BEFORE.txt](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/GIT_BEFORE.txt>)
- [GIT_AFTER.txt](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/GIT_AFTER.txt>)
- [FOREIGN_CHANGES.patch](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/FOREIGN_CHANGES.patch>)
- [GIT_DIFF_AFTER.patch](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/GIT_DIFF_AFTER.patch>)
- [graphify_update.log](</Users/tema/Documents/Work/xml_creator/codex_reports/FORM_POLICY_FINAL_INTEGRATION_20261027/graphify_update.log>)
