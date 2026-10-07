# OP49 / P.DS.01 — WORKING STATE (живой журнал сессии)

## ЭТАП 1-2 (завершены): package + normative source discovery

- Package найден: `/Users/tema/Documents/Work/xml_creator/P.DS.01_OP_49/` (единственный, второй не создаем).
- PRIMARY_NORMATIVE_DIRECTORY: `/Users/tema/Documents/Work/Документы_xml`.
- Нормативный источник: `49_ОП.pdf` (206 PDF-страниц) — «Правила информационного взаимодействия … общего процесса "Обеспечение обмена сведениями о суммах зачисленных и распределенных ввозных таможенных пошлин…"».
- Решение КЕЭК: номер/дата в утвержденном PDF-шаблоне ПУСТЫЕ («от ___ 20__ г. № ___») — действующая редакция Правил, номер решения в тексте отсутствует (не выдумывать).
- Текст извлечен pdfminer.six → `/tmp/op49/49_op.txt` (300 567 символов). Страница в source_refs = PDF-страница (extracted), подтверждено по TRN.001 (стр. 67, таблица 4) и TRN.004 (стр. 71, таблица 6).

### Подтверждено из PDF (extracted pages = source pages)

- Процесс: **P.DS.01, версия 1.0.0** (стр. 4, п. 6 Основных сведений).
- Участники ACT: P.ACT.001 Комиссия; P.DS.01.ACT.001 уполномоченный орган-отправитель; P.DS.01.ACT.002 уполномоченный орган-получатель (стр. 5-6, таблица 1).
- Процедуры PRC.001-007 (стр. 9-10, таблица 2).
- Операции OPR.001-021 (стр. 15-52, таблицы 6-32).
- Транзакции (описания, шаблон запрос/ответ):
  - TRN.001 стр. 67 (таблица 4), TRN.002 стр. 69 (таблица 5), TRN.004 стр. 71 (таблица 6), TRN.006 стр. 73 (таблица 7), TRN.007 стр. 75 (таблица 8);
  - TRN.003 стр. 119 (таблица 4), TRN.005 стр. 121 (таблица 5).
- Сообщения: перечень стр. 65-66 (таблица 3): MSG.001-006, MSG.003 = уведомление об успешной обработке (R.006), у остальных структура R.FP.DS.01.001; MSG.004 = протокол оперативной сверки (R.FP.DS.01.003).
- MSG.001 «информация за отчетный день»: структура R.FP.DS.01.001, транзакция TRN.001 (инициирующее), ответ MSG.003; root QName `urn:EEC:R:FP:DS:01:ChargedDistributedReport:v1.0.0` / `ChargedDistributedReport` (стр. 151, таблица 5); таблица правил 10 (стр. 79-84).
- Таблицы требований: MSG.001 → таблица 10 (стр. 79-84); MSG.002 → таблица 11 (стр. 85-92); MSG.004 → таблица 12 (стр. 91-92); MSG.005 → таблица 13 (стр. 92-102); MSG.006 → таблица 14 (стр. 103-104).
- Структуры: R.006 (Y.Y.Y), R.FP.DS.01.001 (1.0.0, стр. 151, таблица 5, XSD `EEC_R_FP_DS_01_ChargedDistributedReport_v1.0.0.xsd`), R.FP.DS.01.003 (1.0.0, VerificationProtocol, XSD `EEC_R_FP_DS_01_VerificationProtocol_v1.0.0.xsd`).
- Архитектурная особенность R.*: у P.DS.01 НЕТ структуры с префиксом R.* кроме самих нормативных структур (R.006, R.FP.DS.01.001, R.FP.DS.01.003). «Запрос без R.*» подтвержден: тело запроса = структура R.FP.DS.01.001, искусственные R.* структуры НЕ создаем.
- XSD-файлов (реальных .xsd) в PRIMARY_NORMATIVE_DIRECTORY НЕ найдено (проверен весь `Документы_xml/**`, включая XML/ГИС_ДТС — там только ГИС ДТС материалы, не относящиеся к P.DS.01). Структуры заданы таблицами PDF (таблицы 4, 7, 8) — локально восстановлены в structures/. Отдельные классификаторы для OP49 в каталоге отсутствуют (упоминаются: классификатор валют КЕЭК № 11, классификатор результатов обработки — нет файлов).

### Текущее состояние package (production)

- messages.yaml: 6 сообщений, статусы HAS_SEPARATE_RULE_TABLE (5) / NO_SEPARATE_RULE_TABLE (MSG.003).
- message_rules: MSG.001 — 34 business rules, из них 20 EXECUTABLE со structured_rules (kind: cardinality, selection_cardinality, conditional_presence, aggregate_comparison, comparison, presence FORBIDDEN) + 14 external (1 EXTERNAL_CONTEXT_REQUIRED R004, 13 EXTERNAL_REFERENCE_REQUIRED — валютные правила).
- MSG.002 — 38 rules, structured_rules ОТСУТСТВУЮТ (0). MSG.005 — 23 rules, 0 structured. MSG.006 — 14 rules, 0 structured. MSG.004 — 2 rules + 2 structured (FINAL_READY).
- Все правила имеют source_refs (Таблица 10-14, CONFIRMED).
- Тесты OP49: 26 passed (базлайн, py3.13 + pytest 9.1.1).
- Параллельные сессии: OP22 (GUI, 3103 tests passed), OP23 (production rules, правит shared rules_engine.py: presence + _contexts_for_path), OP26 (3 pre-existing failures в их GUI-тестах). НЕ ТРОГАТЬ.
- Shared engine: только что изменен OP23 (git diff подтвержден). Для OP49 engine READ-ONLY.

### Ключевые слоты правил MSG.002 (аналог MSG.001, таблица 11)

- R001: единственный ChargedDistributedDutyReportDetails (cardinality 1..1).
- R002: ровно один ChargedDistributedDutyDetails с DailyInfoIndicator=1.
- R003: ровно один ChargedDistributedDutyDetails с DailyInfoIndicator=0 (месяц нарастающим итогом!) — в отличие от MSG.001.
- R004: дубликат в информационной базе (external).
- R005: наличие предыдущей записи (external).
- R006: EventDate в месяце, следующем за месяцем PreviousReportDate (external context — рабочий календарь не нужен, но сравнение месяцев — вне текущих движковых возможностей; кандидат OPEN_ENGINE или typed month comparison).
- R007: ReportDate > EventDate (comparison GT — executable).
- R008: ModificationDate не заполняется (presence FORBIDDEN — executable).
- R016-R031: блочные требования Distributable/Transfer/StopTransfer (selection_cardinality, conditional_presence, aggregate — executable, зеркально MSG.001 R014-R031).
- R032-R038: валютные правила (external reference).

### Бейслайн тестов (до изменений)

- OP49: 26 passed. OP23+OP26: 3 failed (pre-existing, OP26 GUI), 124 passed. OP22: 3103 passed. eaeu_xml: NOT RUN пока.

## ЭТАП 3: normative scope recovery — ЗАВЕРШЕН (159 требований)

### Нормативный baseline (подтверждено по таблицам 10-14 PDF)

- MSG.001 → Таблица 10 (PDF стр. 79-84): **34** items (в пакете 34 — полное покрытие).
- MSG.002 → Таблица 11 (PDF стр. 85-92): **38** items (в пакете 38 — полное покрытие).
- MSG.004 → Таблица 12 (PDF стр. 91-92): **2** items (в пакете 2 — полное покрытие).
- MSG.005 → Таблица 13 (PDF стр. 92-102): **54** items (в пакете только 23; items 24-54 ОТСУТСТВОВАЛИ).
- MSG.006 → Таблица 14 (PDF стр. 103-107): **31** items (в пакете только 14; items 15-31 ОТСУТСТВОВАЛИ).
- **TOTAL = 34+38+2+54+31 = 159** (пакет покрывал 111). Knowledge Base: `knowledge_base/sources/OP49_P_DS_01/pages/` (KB FIRST, оригинальный PDF — source of truth).
- PDF page != printed page (PDF 93 = printed 40; смещение ~53). Код требования ≠ printed page.

### Вердикт по MSG.005 item 7 (Таблица 13, PDF стр. 94)

Полный текст item 7: «в сложном реквизите "Сведения из отчета…" (ds01cdo:ChargedDistributedDutyReportDetails) должен присутствовать только один экземпляр реквизита "Информация о суммах…" (ds01cdo:ChargedDistributedDutyDetails), имеющий реквизит "Признак ежедневных сведений" (ds01sdo:DailyInfoIndicator) со значением "0" для передачи сведений за отчетный месяц нарастающим итогом».
→ = for_each(report details) + selection_cardinality(DailyInfoIndicator=false, min1 max1). Исполнимо (B2/B3). Подтверждено из PDF стр. 94.

### Карта item→rule для новых items (использовать при реализации, не выводить заново)

- MSG.002 (одиночный отчет гарантирован R001): R001-R003 cardinality/sel_card (исполнимо); R004,R005 OPEN_EXTERNAL_REGISTRY (информационная база); R006 OPEN_ENGINE (месяц, следующий за); R007 comparison GT (исполнимо); R008 presence FORBIDDEN ModificationDateTime (исполнимо); R009-R015,R021,R027,R028,R035-R038 OPEN_CLASSIFIER (валюты); R016-R020 Distributable-блок (исполнимо); R022-R026 Transfer-блок (исполнимо); R029-R033 StopTransfer-блок (исполнимо); R034 проверка текста при атомизации.
- MSG.005 (мультиэкземплярное, scope per instance задан item 5): items 1,4,8,9 OPEN_EXTERNAL_REGISTRY; 2 OPEN_ENGINE (дубликаты EventDate); 3 OPEN_ENGINE (равенство ModificationDate по экземплярам); 5 scope-directive (OTHER_OPEN); 6,7 for_each+selection_cardinality (исполнимо); 8? см. 4; 10 for_each+presence REQUIRED ModificationDateTime (исполнимо); 11 for_each+comparison GT DATETIME (исполнимо); 12-18,24,30,31,37,38,39,40 OPEN_CLASSIFIER; 19 (sel_card=1),20 (sel_card=0 min1),21,22 (cond_pres),25-28 (Transfer),32-35 (StopTransfer) исполнимо; 23,29,36 OPEN_ENGINE (агрегаты per instance); 41 scope-directive (OTHER_OPEN); 42-54 OPEN_ENGINE (монотонность по месяцам между экземплярами). Item 8 = OPEN_EXTERNAL_REGISTRY (информационная база), item 9 = OPEN_EXTERNAL_REGISTRY (равенство значениям из базы).
- MSG.006 (мультиэкземплярное, scope per instance item 2): 1 OPEN_ENGINE (дубликаты); 2 scope-directive (OTHER_OPEN); 3 sel_card DailyInfoIndicator=false max0 document-level (исполнимо); 4 for_each+sel_card=1 1..1 (исполнимо); 5 OPEN_EXTERNAL_REGISTRY (рабочий день); 6 for_each+comparison GT DATETIME (исполнимо); 7 for_each+presence REQUIRED (исполнимо); 8 for_each+comparison GE DATETIME (исполнимо; «максимального» = собственное значение при per-instance scope, пометить интерпретацию); 9-15,20,26,27 OPEN_CLASSIFIER; 19,25 OPEN_ENGINE (per-instance агрегаты); 16-18,21-24,28-31 исполнимо (for_each/cond_pres/sel_card).

### Классификация причин (для FINAL)

OPEN_ENGINE; OPEN_CLASSIFIER (валюты КЕЭК № 11 — файла нет); OPEN_EXTERNAL_REGISTRY (информационная база/рабочий день); OTHER_OPEN (scope directives items MSG.005 №5, №41; MSG.006 №2).

## СЛЕДУЮЩИЕ ШАГИ (этап 4+)

1. Атомизация 159 requirements (canonical_requirement_id OP49.P_DS_01.<MSG>.REQ.<NNN>) → REAUDIT CSV в codex_reports/OP49_P_DS_01/.
2. REAUDIT отчеты: requirements.csv, gaps.csv, message_matrix.csv, transaction_matrix.csv, audit.md.
3. Safe batch map (B1-B4), затем реализация structured_rules (только yamls пакета OP49).
4. Positive/negative XML tests через production validate_body.
5. Regression: OP49, OP22, OP23, OP26, eaeu_xml.
6. FINAL snapshot.

## СЛЕДУЮЩИЕ ШАГИ (этап 3+)

1. Ре-аудит: атомизация всех 159 требований (34+38+2+54+31) с canonical_requirement_id OP49.P_DS_01.<MSG>.REQ.<NNN>.
2. Отчеты re-audit в codex_reports/OP49_P_DS_01/ (requirements.csv, gaps.csv, message_matrix.csv, transaction_matrix.csv, audit.md).
3. Safe batch map: реализация structured_rules для MSG.002 (зеркало MSG.001), MSG.005, MSG.006 — там где источники однозначны.
4. Positive/negative XML tests через production validate_body.
5. Regression: OP49, OP22, OP23, OP26, eaeu_xml.
6. FINAL snapshot.
