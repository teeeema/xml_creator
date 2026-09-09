# Пользовательская приёмка GUI P.MM.01

Дата: 2026-08-25. Проверка выполнена локально на macOS через реальный wxPython 4.3.1 без изменения Decision №5, StructureDefinition, MessageRules, FieldInputPolicy, version profiles или XML serializer.

## Итог сценариев

| Сценарий | Результат | Marker |
|---|---|---|
| TRN.004, MSG.005 → MSG.006 | PASS | `WX_TRN004_ACCEPTANCE_OK` |
| TRN.005, MSG.007 → MSG.008 / MSG.009 | PASS | `WX_TRN005_ACCEPTANCE_OK` |
| TRN.011 notification, MSG.017 | PASS | `WX_NOTIFICATION_ACCEPTANCE_OK` |
| TRN.008 mutual obligations, MSG.019 → MSG.020 / MSG.018 | PASS | `WX_MUTUAL_OBLIGATIONS_ACCEPTANCE_OK` |
| Большая форма MSG.001 | PASS | `WX_MSG001_LARGE_FORM_ACCEPTANCE_OK` |

## Issues

| ID | Scenario | TRN | MSG | Field | Category | Severity | Description | Expected | Actual | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| UAT-001 | Control type / enum | generic | fixture | allowed-values field | GUI bug / data loss | HIGH | Обычный `wx.Choice` обрабатывался как boolean. | Выбранный enum сохраняется и восстанавливается. | Значение превращалось в `None`, draft restore не выбирал пункт. | FIXED |
| UAT-002 | Control type / arbitrary XML | multiple | multiple | `AnyDetails/*` | GUI bug | HIGH | TextCtrl возвращал строку для `ANY_XML`. | Корректный XML передаётся как XML Element и проходит существующую validation. | Любой ручной ввод получал `DATATYPE_INVALID`. | FIXED |
| UAT-003 | Draft response continuation | TRN.004/TRN.008 | responses | transaction session | usability issue | MEDIUM | Draft хранит session metadata, но session намеренно не восстанавливается. | Пользователь понимает, что для ответа надо заново начать/сформировать исходное сообщение. | Load выдаёт `SESSION_RESTART_REQUIRED`; автоматическое продолжение correlation невозможно. | OPEN — requires separate session-restoration design |
| UAT-004 | Binary document input | several | several | `DocCopyBinaryText` | usability issue | MEDIUM | Бинарное содержимое было представлено обычным text control. | Пользователь выбирает файл; путь/base64 скрыты, draft автономен. | Generic file picker покрывает 53/53 usages. | FIXED |
| UAT-005 | Boolean input | several | several | `bdt:IndicatorType` | usability issue | LOW | Choice показывал технические `true/false`. | Понятные пользователю Да/Нет при сохранении XML semantics. | GUI показывает Да/Нет, model/XML сохраняют bool/true/false. | FIXED |
| UAT-006 | Numeric input | several | several | quantity/integer | usability issue | LOW | Используется TextCtrl. | Понятная ошибка при неверном числе; большой диапазон не ограничивается SpinCtrl. | Validation корректна, но нет input mask. | ACCEPTED |
| UAT-007 | Classifier fallback | TRN.005 | MSG.007 | classifier fields | expected behaviour | LOW | Dataset отсутствует. | GUI предупреждает, что произвольная строка не подтверждена классификатором. | Маркер «Классификатор», tooltip и validation warning присутствуют. | EXPECTED |
| UAT-008 | Version placeholder | TRN.004/TRN.005 | MSG.005/MSG.009 | structure namespace | normative blocker | LOW | Реальная версия отсутствует. | TEST XML содержит Y.Y.Y/X.X.X и предупреждение; STRICT блокируется. | Поведение соответствует модели. | EXPECTED |
| UAT-009 | Normative conflicts | TRN.002 and others | MSG.002/023/024 | source rules | normative blocker | LOW | Подтверждённые конфликты нельзя обходить. | GUI объясняет blocker без traceback. | Сообщения блокируются отдельно, остальные сценарии работают. | EXPECTED |
| UAT-010 | Long selector captions | all | all | process/TRN/MSG selectors | cosmetic | COSMETIC | Длинные подписи сокращаются многоточием. | Полный текст доступен без потери контекста. | Полный текст доступен через tooltip и `ⓘ`. | ACCEPTED |

Severity summary: BLOCKER 0; HIGH 2 fixed; MEDIUM 1 fixed и 1 open; LOW 1 fixed, 1 accepted, 3 expected; COSMETIC 1 accepted. Открыт только UAT-003 (MEDIUM); остальные исправлены или являются ожидаемым/приемлемым поведением.

## TRN.004

- EDocId редактируется; IdentifierService generator и повторная ручная правка работают.
- EDocDateTime поддерживает manual, System, UTC и IANA picker.
- Preview, clipboard и saved XML побайтно используют одну строку.
- Ответ имеет новый Body EDocId и SOAP MessageID; EDocRefId/RelatesTo коррелируют с request; ProcedureID и ConversationID сохраняются.
- MSG.006 UpdateDateTime остаётся EXTERNAL_SYSTEM без кнопки «Сейчас».

## TRN.005

- classifier fallback явно помечен как непроверенный без dataset;
- required filter, validation и XML работают;
- MSG.008 и MSG.009 формируются только после исходного MSG.007;
- MSG.009 сохраняет TEST placeholders, correlation не нарушается.

## Notification и mutual obligations

- TRN.011 содержит только initiating MSG.017, обычный response UI отсутствует, RelatesTo не создаётся.
- TRN.008 показывает обе response branches. MSG.020 и MSG.018 проверены в отдельных transaction instances; обе сохраняют ConversationID и связываются с MessageID исходного MSG.019.
- После загрузки draft session не восстанавливается автоматически; это явно сообщается пользователю (UAT-003).

## Большая форма MSG.001

- форма иерархическая, группы сворачиваются; это не плоский список;
- ALL 401, REQUIRED 168, USER_FIELDS 399; значения не теряются при filter/search;
- repeatable groups, field help, Guide, test data и draft roundtrip работают.

## Control type audit

| Control mapping | Usages | Result |
|---|---:|---|
| string/text → TextCtrl | 1150 | PASS |
| boolean/indicator → Choice | 115 | PASS, Да/Нет; UAT-005 FIXED |
| integer/quantity → TextCtrl + validation | 8 | PASS, UAT-006 |
| DATE → editable text + Today + calendar | 173 | PASS |
| DATETIME → editable text + Now/timezone | 53 | PASS |
| hidden/unresolved temporal | 7 | EXPECTED |
| identifier/business ID → TextCtrl | 436 | PASS; UUID helper only on explicit EDocId capability |
| classifier → editable TEST fallback + warning | 354 | PASS |
| attribute → scalar control | 108 | PASS |
| ANY_XML → TextCtrl parsed to XML Element | 17 | FIXED |
| complex group | 539 | PASS |
| enum with allowed values → Choice | fixture coverage | FIXED |

## Performance

Measured in the real wx smoke, seconds:

| Operation | Time |
|---|---:|
| MSG.001 form build | 0.1113 |
| Required filter | 0.0831 |
| User-fields filter | 0.1291 |
| Search | 0.0522 |
| Guide open | 0.1841 |
| Draft load | 0.0253 |
| Validation | 0.0009 |

No visible freezes were observed. Window layout, scrolling, persistent bottom actions and resize behaviour remained functional during the smoke.
