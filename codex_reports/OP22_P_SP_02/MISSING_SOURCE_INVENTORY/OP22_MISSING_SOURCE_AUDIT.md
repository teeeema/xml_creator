# OP22 / P.SP.02 — аудит отсутствующих нормативных источников

## Статус

- Основной источник: `/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf`.
- SHA-256: `99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3`.
- Страниц: **1035**.
- KB extraction: `knowledge_base/sources/OP22_P_SP_02/FULL.md`, `COMPLETE`.
- Canonical requirements: **1609**.
- Blocked requirements: **85**.
- SOURCE_CONFLICT: **7**.
- Inventory artifacts: **77**.
- Missing or unresolved (всё, кроме `PRESENT_COMPLETE`): **72**.

## Методика

Проверен весь извлечённый текст OP22 и текущие OP22-отчёты. Упоминание в Markdown/YAML/report не считается наличием официального normative payload.

Локальная доступность проверялась по `/Users/tema/Documents/Work/Документы_xml`, `knowledge_base/**`, `P.SP.02_OP_22/**` и `codex_reports/OP22_P_SP_02/**`. Проектные YAML структуры — `METADATA_ONLY`; official XSD учитываются отдельно как `XSD_MISSING`.

## Семантика статусов

- `PRESENT_COMPLETE` — нормативный файл/содержимое реально присутствует локально.
- `PRESENT_PARTIAL` — часть содержания доступна, но отдельный/полный artifact отсутствует.
- `METADATA_ONLY` — есть проектные метаданные, но нет official payload.
- `PAYLOAD_MISSING` — artifact известен, но official code list/reference payload отсутствует.
- `XSD_MISSING` — официальный XSD отсутствует.
- `MODEL_VERSION_MISSING` / `VERSION_UNRESOLVED` — точная versioned модель/редакция не установлена.
- `REGISTRY_CONTRACT_MISSING` — ресурс назван, но точный технический контракт не идентифицирован.
- `SOURCE_CONFLICT_NEEDS_DOCUMENT` — конфликт нельзя разрешать без дополнительного официального источника.

## Реконсиляция 85 blockers

Из 66 исторических `CLASSIFIER` строк: 57 относятся к `P.CLS.027`, 3 — к `P.P.SP.02.CLS.001`, 1 — к `P.P.SP.03.CLS.001`, 4 фактически зависят от внешних информационных ресурсов, а `P.SP.02.MSG.038:56:2` оставлен `UNRESOLVED`.

Подтверждённые stale provenance исправлены только в новых отчётах: `MSG.028:44:32 -> p.722`, `MSG.029:45:32 -> p.726`, `MSG.031:48:2 -> p.733`, `MSG.038:56:2 -> p.754`, `MSG.038:56:3 -> p.755`. Исходные отчёты не изменялись.

Exact known artifact mapping: **68/85**; unresolved artifact identity/contract/source: **17/85**.

## Дополнительные зависимости, подтверждённые полным проходом

При повторном полном проходе по `FULL.md` выявлены ещё 4 source dependencies, которые не были отдельными строками исходного 73-artifact inventory:

- `UNRESOLVED:NATIONAL_TAXPAYER_ID_RULES` — правила значения `TaxpayerId`, принятые в стране регистрации налогоплательщика; OP22: стр. 854, 889, 917, 949, 1014. Это отдельная зависимость от реестра налогоплательщиков и его технического контракта.
- `UNRESOLVED:APPLICANT_CHANGE_REASON_LIST` — перечень причин для `ipsdo:ApplicantChangeBasisCode`; OP22: стр. 885. Точный нормативный идентификатор/редакция перечня не названы.
- `UNRESOLVED:NATIONAL_BUDGET_CLASSIFICATION_RULES` — национальные правила формирования `PaymentBudgetCode`; OP22: стр. 1003. Номер национального акта не указан и не выводится предположительно.
- `UNRESOLVED:BANK_ID_METHOD_SOURCE` — источник значений `schemeId` для идентификации банка; OP22: стр. 1009. OP22 описывает атрибут, но governing справочник/акт не называет.

Проверка ссылки на «перечень видов средств (каналов) связи» новой строки не добавила: эта зависимость уже учтена как `P.CLS.008` и Решение Коллегии ЕЭК № 192 от 06.12.2022.

## Ограничения

- Web search не выполнялся.
- Версии `X.X.X` / `Z.Z.Z` не угадывались.
- `UNRESOLVED:` — внутренний ключ inventory, а не нормативный код ЕЭК.
- Для 7 SOURCE_CONFLICT требований сторона конфликта не выбиралась.
- `affected_requirements_count` отражает текущие 85 blockers, а не все места использования artifact во всех 1609 requirements.

## Итог по availability

- `DOCUMENT_MISSING`: **20**
- `EXTERNAL_RESOURCE_ONLY`: **7**
- `METADATA_ONLY`: **6**
- `MODEL_VERSION_MISSING`: **4**
- `PAYLOAD_MISSING`: **9**
- `PRESENT_COMPLETE`: **5**
- `PRESENT_PARTIAL`: **1**
- `REGISTRY_CONTRACT_MISSING`: **5**
- `SOURCE_CONFLICT_NEEDS_DOCUMENT`: **2**
- `VERSION_UNRESOLVED`: **12**
- `XSD_MISSING`: **6**

## Файлы

- `OP22_ALL_REFERENCED_ARTIFACTS.csv` — полный дедуплицированный inventory.
- `OP22_MISSING_DOCUMENTS.csv` — неполные/отсутствующие artifacts.
- `OP22_BLOCKED85_TO_MISSING_SOURCE.csv` — связь каждого из 85 blockers с source artifact.
- `OP22_SOURCE_CONFLICTS.csv` — 7 конфликтов с обеими сторонами и документом для разрешения.
- `OP22_DOCUMENTS_TO_FIND.md` — приоритетный список следующего поиска.
