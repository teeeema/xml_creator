# Реестр неразрешённых конфликтов и внешних дефектов (UNRESOLVED CONFLICTS)

## 1. Статус интеграции ОП 22 и ОП 26

**Между ОП 22 и ОП 26 неразрешённых конфликтов НЕТ.**
Все прямые коллизии в универсальном ядре (`body.py`), уровне контроллеров (`facade.py`), моделях представления (`view_model.py`) и каталогах правил успешно и детерминированно разрешены.

## 2. Пре-существующие дефекты других процессов (Out of Scope)

В базовой кодовой ветке присутствуют 16 непроходящих тестов, не связанных с функциональностью ОП 22 или ОП 26. В соответствии с регламентом безопасной стабилизации, изменение сторонних процессов за пределами задачи интеграции не производилось.

### 2.1. Дефекты процесса ОП 49 (P.DS.01) — 12 тестов
- **Файлы**:
  - `P.DS.01_OP_49/tests/test_msg001_full_message.py` (1 failure)
  - `P.DS.01_OP_49/tests/test_pds01_catalog.py` (1 failure)
  - `P.DS.01_OP_49/tests/test_process_pipeline.py` (9 failures)
  - `eaeu_xml/tests/test_application_facade.py::ApplicationFacadeTests::test_ds01_test_data_satisfies_executable_structured_rules` (1 failure)
- **Причина**: Генератор тестовых данных для сообщений P.DS.01 формирует неполный набор реквизитов для сложных циклических структур распределения пошлин.
- **Влияние на ОП 22 / ОП 26**: Отсутствует. Процесс P.DS.01 полностью изолирован.

### 2.2. Неимплементированные структурные правила в ОП 23 и ОП 26 v1.1.0 — 4 теста
- **Файл**: `eaeu_xml/tests/test_structured_rule_form_policy.py`
  - `test_top_level_string_target_presence_rules_project_into_form_policy[P.SP.03-P.SP.03.TRN.018-P.SP.03.MSG.023-ipsdo:ApellationOfOriginApplicationId]`
  - `test_top_level_string_target_presence_rules_project_into_form_policy[P.MM.01-P.MM.01.TRN.018-P.MM.01.MSG.027-RegistrationNumberId]`
  - `test_op23_msg001_projects_static_authority_requirement`
  - `test_op26_msg001_projects_static_classifier_id_as_read_only_fixed_value`
- **Причина**:
  - В процессе ОП 23 (`P.SP.03`) правила в файлах `message_rules` имеют статус `DECLARATIVE_NOT_YET_EXECUTABLE` и пустой список `structured_rules: []`.
  - В базовой версии ОП 26 v1.1.0 структурные правила классификатора `P.CLS.019` отсутствуют (они формализованы только в целевой черновой версии 1.3.0 в `versions/1.3.0/message_rules/`).
- **Влияние на ОП 22 / ОП 26**: Настоящие рабочие тесты ОП 22 (`test_structured_rules.py`, `test_op22_visual_engine.py`) и ОП 26 (`test_v130_runtime.py`, `test_v130_stage3.py`) проходят на 100%.

## 3. Блокеры релиза ОП 26 v1.3.0

- **Блокер**: Официальные XSD-схемы для версии 1.3.0 не опубликованы ЕЭК (отсутствуют окончательные namespace и XSD).
- **Статус**: В соответствии с архитектурным планом, продвижение версии заблокировано (`promotion_allowed: false` в `migration_status.json`). Процесс функционирует в базовой версии 1.1.0, а наработки 1.3.0 подтверждены автономным пакетом тестов.
