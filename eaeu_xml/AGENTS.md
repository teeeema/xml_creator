# Правила работы с новым проектом eaeu_xml

1. `./15kr0005.doc` — READ ONLY; не изменять, не перемещать и не переименовывать.
2. Перед изменением нормативной логики проверить Решение №5.
3. Старый проект `xml_creator` не является нормативным источником или архитектурной основой.
4. Перед разработкой прочитать все файлы `project_memory/`.
5. После значимого изменения обновить `CURRENT_STATE.md` и `CHANGELOG.md`.
6. Новое архитектурное решение фиксировать в `DECISIONS.md`.
7. Новое нормативное правило фиксировать в `DECISION_5_RULES.md` и `source_rules.yaml`.
8. Пробел или конфликт фиксировать в `UNRESOLVED_RULES.md`.
9. Нельзя реализовывать правило только потому, что оно кажется логичным или присутствует лишь в XML-примере.

Главный принцип: нормативное правило → source reference → модель → код → тест.

## Graphify navigation

Use Graphify as the primary repository-navigation mechanism.

Before broad grep/search or opening many source files:

1. Query `graphify-out/graph.json` through Graphify.
2. Prefer:
   - `graphify query`
   - `graphify explain`
   - `graphify path`
   - `graphify affected`
3. Use Graphify to identify the minimal relevant source set.
4. Open only the files required to verify or modify the implementation.
5. Fall back to grep/ripgrep only when Graphify cannot answer the question.
6. Before changing a central model or API, run `graphify affected`.
7. After meaningful code changes, update the Graphify graph.
8. Never treat Graphify output as the source of truth for normative XML/process data; verify actual source/config files before changing behavior.

Goal: minimize repository-wide scanning and unnecessary context usage.
