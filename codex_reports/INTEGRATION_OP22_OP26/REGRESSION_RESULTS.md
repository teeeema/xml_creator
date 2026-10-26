# Результаты регрессионного тестирования: Интеграция ОП 22 и ОП 26

## 1. Сводная таблица результатов

| Тестовый набор | До интеграции (Baseline) | После интеграции | Статус | Примечание |
|---|---|---|---|---|
| **P.SP.02 (ОП 22)** | 306 passed / 0 failed | **306 passed / 0 failed** | **100% PASS** | Полная сохранность восстановленной функциональности |
| **P.MM.01 (ОП 26)** | 104 passed / 0 failed | **104 passed / 0 failed** | **100% PASS** | Все 41 MSG, 518 атомов и тесты v1.3.0 проходят |
| **GUI & Presentation** | 25 passed / 0 failed | **25 passed / 0 failed** | **100% PASS** | `GuiViewModel`, карточки полей, санитизация текста |
| **Engine Contract (`body.py`)** | 1 FAILED (`test_engine_has_no_specific_process_hardcode`) | **1 PASSED** | **FIXED** | Устранён специфичный хардкод `P.MM.01` в ядре |
| **Общий репозиторный сьют** | 727 passed / 17 failed | **714 passed / 16 failed** (16 skipped) | **Улучшение: -1 failure** | Все 16 оставшихся падений — пре-существующие в базовой ветке |

## 2. Детализация прогонов

### 2.1. ОП 22 (P.SP.02_OP_22/tests/)
- **Команда**: `PYTHONPATH=eaeu_xml/src python3 -m pytest P.SP.02_OP_22/tests/`
- **Результат**: 306 passed in 13.92s (100%)
- **Покрытие**:
  - `test_msg001_effective_field_policy.py`: 12 passed
  - `test_msg001_structured_rules.py`: 46 passed
  - `test_msg004_classifier_policy.py`: 7 passed
  - `test_msg004_end_to_end.py`: 2 passed
  - `test_msg004_repeatable_xml.py`: 27 passed
  - `test_msg004_safe_mapping.py`: 22 passed
  - `test_msg005_end_to_end.py`: 3 passed
  - `test_msg005_repeatable_xml.py`: 31 passed
  - `test_msg005_safe_mapping.py`: 37 passed
  - `test_msg027_end_to_end.py`: 29 passed
  - `test_msg027_repeatable_xml.py`: 57 passed
  - `test_msg027_safe_mapping.py`: 14 passed
  - `test_pcls027_classifier.py`: 6 passed
  - `test_psp02_catalog.py`: 13 passed

### 2.2. ОП 26 (P.MM.01_OP_26/tests/)
- **Команда**: `PYTHONPATH=eaeu_xml/src:P.MM.01_OP_26/tests python3 -m pytest P.MM.01_OP_26/tests/`
- **Результат**: 104 passed in 7.42s (100%)
- **Покрытие**:
  - `test_all_transactions_e2e.py`: 7 passed
  - `test_application_facade_pmm01.py`: 20 passed
  - `test_drafts_pmm01.py`: 4 passed
  - `test_end_to_end_transactions.py`: 4 passed
  - `test_gui_controller_pmm01.py`: 17 passed
  - `test_message_artifact_persistence.py`: 5 passed
  - `test_pmm01_catalog.py`: 21 passed
  - `test_restored_session_xml_e2e.py`: 9 passed
  - `test_v130_runtime.py`: 9 passed
  - `test_v130_stage3.py`: 8 passed

### 2.3. GUI и отображение (eaeu_xml/tests/)
- **Команда**: `QT_QPA_PLATFORM=offscreen PYTHONPATH=eaeu_xml/src python3 -m pytest eaeu_xml/tests/test_op22_visual_engine.py eaeu_xml/tests/test_presentation_text_sanitizer.py eaeu_xml/tests/test_gui_qt_view_model.py eaeu_xml/tests/test_examples.py`
- **Результат**: 25 passed in 3.65s (100%)

### 2.4. Полный репозиторный сьют (746 тестов)
- **Команда**: `PYTHONPATH=eaeu_xml/src:P.MM.01_OP_26/tests python3 -m pytest --ignore=eaeu_xml/tests/test_production_window.py --ignore=eaeu_xml/tests/test_validation_page_qml.py`
- **Результат**: 714 passed, 16 failed, 16 skipped in 29.90s
- **Анализ 16 непройденных тестов**:
  - 11 падений в `P.DS.01_OP_49` (давний дефект маппинга генератора данных DS.01, существовавший до начала работ)
  - 1 падение в `eaeu_xml/tests/test_application_facade.py` (`test_ds01_test_data_satisfies_executable_structured_rules`, связано с DS.01)
  - 4 падения в `eaeu_xml/tests/test_structured_rule_form_policy.py` (тесты для P.SP.03 и активной версии P.MM.01 1.1.0, где структурные правила ещё не перенесены в каталоги)
  - **Ни одного регрессионного сбоя относительно исходного состояния.**
