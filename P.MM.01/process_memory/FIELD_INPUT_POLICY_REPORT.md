# FIELD INPUT POLICY REPORT

Дата аудита: 2026-08-24. Область: все 28 MSG процесса P.MM.01.

## Метод

Единицей подсчёта является использование реквизита в MSG-контексте, а не уникальная строка StructureDefinition. Resolver использует ключ `(message_code, field_path)`. Приоритет: нормативный конфликт сообщения → fixed value → явно заданная policy → classifier metadata → structural container → условие MessageRule → `UNRESOLVED_INPUT_POLICY`. Выводов из XML-имени поля нет.

## Итоговые метрики

| Policy | Count |
|---|---:|
| Total field usages | 2960 |
| USER_INPUT | 0 |
| USER_SELECT | 0 |
| CLASSIFIER | 356 |
| AUTO_GENERATED | 28 |
| AUTO_FIXED | 56 |
| AUTO_DATETIME | 0 |
| CORRELATION | 11 |
| EXTERNAL_SYSTEM | 1 |
| INTEGRATION_PLATFORM | 0 |
| CONDITIONAL | 133 |
| UNRESOLVED_INPUT_POLICY | 1831 |
| STRUCTURAL_CONTAINER | 544 |

Нулевое число `USER_INPUT` — намеренный результат консервативного аудита: существующие структуры и правила описывают состав/ограничения данных, но для обычных бизнес-реквизитов не подтверждают, что значение вводит именно оператор GUI. Такие поля не были произвольно переведены в ручной ввод.

## По сообщениям

Столбцы: Total, Visible, Manual, Select, Automatic, Classifier, Conditional, External, Unresolved.

| MSG | Total | Visible | Manual | Select | Automatic | Classifier | Conditional | External | Unresolved |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P.MM.01.MSG.001 | 405 | 401 | 0 | 0 | 3 | 52 | 17 | 0 | 255 |
| P.MM.01.MSG.002 | 405 | 403 | 0 | 0 | 3 | 52 | 85 | 0 | 187 |
| P.MM.01.MSG.003 | 405 | 405 | 0 | 0 | 3 | 52 | 0 | 0 | 272 |
| P.MM.01.MSG.004 | 10 | 10 | 0 | 0 | 4 | 1 | 0 | 0 | 4 |
| P.MM.01.MSG.005 | 11 | 11 | 0 | 0 | 3 | 1 | 0 | 0 | 6 |
| P.MM.01.MSG.006 | 11 | 11 | 0 | 0 | 4 | 1 | 0 | 1 | 4 |
| P.MM.01.MSG.007 | 14 | 14 | 0 | 0 | 3 | 2 | 1 | 0 | 7 |
| P.MM.01.MSG.008 | 405 | 405 | 0 | 0 | 4 | 52 | 0 | 0 | 271 |
| P.MM.01.MSG.009 | 10 | 10 | 0 | 0 | 4 | 1 | 0 | 0 | 4 |
| P.MM.01.MSG.010 | 14 | 14 | 0 | 0 | 3 | 2 | 1 | 0 | 7 |
| P.MM.01.MSG.011 | 405 | 405 | 0 | 0 | 4 | 52 | 0 | 0 | 271 |
| P.MM.01.MSG.012 | 39 | 38 | 0 | 0 | 3 | 3 | 0 | 0 | 27 |
| P.MM.01.MSG.013 | 11 | 11 | 0 | 0 | 4 | 1 | 0 | 0 | 5 |
| P.MM.01.MSG.014 | 11 | 10 | 0 | 0 | 3 | 1 | 0 | 0 | 6 |
| P.MM.01.MSG.015 | 11 | 11 | 0 | 0 | 4 | 1 | 0 | 0 | 5 |
| P.MM.01.MSG.016 | 42 | 42 | 0 | 0 | 3 | 3 | 0 | 0 | 29 |
| P.MM.01.MSG.017 | 42 | 42 | 0 | 0 | 3 | 3 | 0 | 0 | 29 |
| P.MM.01.MSG.018 | 10 | 10 | 0 | 0 | 4 | 1 | 0 | 0 | 4 |
| P.MM.01.MSG.019 | 39 | 38 | 0 | 0 | 3 | 3 | 6 | 0 | 21 |
| P.MM.01.MSG.020 | 39 | 39 | 0 | 0 | 4 | 3 | 4 | 0 | 22 |
| P.MM.01.MSG.021 | 39 | 39 | 0 | 0 | 3 | 3 | 8 | 0 | 19 |
| P.MM.01.MSG.022 | 42 | 42 | 0 | 0 | 3 | 3 | 0 | 0 | 29 |
| P.MM.01.MSG.023 | 23 | 23 | 0 | 0 | 3 | 2 | 3 | 0 | 11 |
| P.MM.01.MSG.024 | 23 | 23 | 0 | 0 | 3 | 2 | 3 | 0 | 11 |
| P.MM.01.MSG.025 | 11 | 11 | 0 | 0 | 3 | 1 | 1 | 0 | 5 |
| P.MM.01.MSG.026 | 405 | 405 | 0 | 0 | 4 | 52 | 0 | 0 | 271 |
| P.MM.01.MSG.027 | 39 | 39 | 0 | 0 | 3 | 3 | 1 | 0 | 26 |
| P.MM.01.MSG.028 | 39 | 39 | 0 | 0 | 4 | 3 | 3 | 0 | 23 |

`Automatic` объединяет AUTO_GENERATED, AUTO_FIXED, AUTO_DATETIME, CORRELATION и INTEGRATION_PLATFORM. Structural containers учитываются только в Total/Visible.

## Поля, которые действительно должен заполнить пользователь

Для всех MSG подтверждённых `USER_INPUT`/`USER_SELECT` полей сейчас нет. Поэтому таблицы ручных полей и TOP-20 пусты. Это не означает, что бизнес-данные не требуются: 1831 usages имеют `UNRESOLVED_INPUT_POLICY` и требуют отдельного подтверждения источника значения.

## Проверенные общие реквизиты

| Field | MSG context | Policy | Value source |
|---|---|---|---|
| EDocHeader/InfEnvelopeCode | все 28 MSG | AUTO_FIXED | MESSAGE_METADATA |
| EDocHeader/EDocCode | все 28 MSG | AUTO_FIXED | MESSAGE_METADATA |
| EDocHeader/EDocId | все 28 MSG | AUTO_GENERATED | GENERATED_UUID |
| EDocHeader/EDocRefId | 11 response MSG | CORRELATION | PREVIOUS_BODY |
| EDocHeader/EDocRefId | прочие 17 MSG | UNRESOLVED_INPUT_POLICY | UNKNOWN |
| EDocHeader/EDocDateTime | все 28 MSG | UNRESOLVED_INPUT_POLICY | UNKNOWN |
| UpdateDateTime | MSG.006 | EXTERNAL_SYSTEM | EXTERNAL_INFORMATION_SYSTEM |
| UpdateDateTime | прочие контексты | UNRESOLVED_INPUT_POLICY | UNKNOWN |

`UpdateDateTime` не классифицирован как AUTO_DATETIME. SOAP `MessageID/RelatesTo` не смешиваются с Body `EDocId/EDocRefId`. Для MSG.002, MSG.023 и MSG.024 статус `NORMATIVE_CONFLICT` остаётся приоритетным.
