# Binary fields and minor GUI UX

Дата аудита: 2026-08-25. Нормативные структуры, MessageRules, FieldInputPolicy,
version profiles и XML serializer не изменялись.

## Итог

- уникальных binary field usages по 28 сообщениям: **53**;
- datatype: только `csdo:BinaryTextType`;
- structurally required: **0**, optional: **53**;
- file-picker coverage: **53/53**;
- boolean/indicator usages: **115**; GUI показывает `Да / Нет`, model хранит
  typed `bool`, XML остаётся `true / false`;
- MIME определяется `mimetypes` только для подсказки. Неизвестный MIME показан
  как «Тип не определён» и не выдумывается;
- соседний `@mediaTypeCode` остаётся отдельным редактируемым XML-реквизитом и
  автоматически из MIME не заполняется без явной нормативной связи.

## Binary audit

Все строки имеют `ui policy = GROUP + generic file picker`, attribute
`mediaTypeCode`, datatype `csdo:BinaryTextType`, `required = нет`, source ref
`SRC-PMM01-068`. Одинаковые пути сгруппированы без потери coverage.

| Message | Count | Field paths / parent groups |
|---|---:|---|
| MSG.001 | 7 | `DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/{DrugUsageInstructionDetails, DrugGeneralCharacteristicDetails, DrugPackageLayoutDetails, ExpertReportDetails, RiskManagementPlanDetails, QualityRegulatoryDocDetails}/PdfBinaryText`; `DrugRegistrationDetails/RegistrationDossierDocDetails/DocCopyBinaryText` |
| MSG.002 | 7 | те же семь путей структуры регистрации |
| MSG.003 | 7 | те же семь путей структуры регистрации |
| MSG.008 | 7 | те же семь путей структуры регистрации |
| MSG.011 | 7 | те же семь путей структуры регистрации |
| MSG.026 | 7 | те же семь путей структуры регистрации |
| MSG.012, MSG.016, MSG.017, MSG.019, MSG.020, MSG.021, MSG.022, MSG.027, MSG.028 | 1 каждый | `RegistrationDossierDocDetails/DocCopyBinaryText` |
| MSG.023, MSG.024 | 1 каждый | root `PdfBinaryText` with `@mediaTypeCode` |

## Реализация и draft strategy

Capability определяется только по datatype metadata, не по XML name, message
или parent. wx выбирает файл; generic application service читает bytes один раз,
получает presentation metadata и передаёт base64 lexical value существующему
Body pipeline. Путь, имя и MIME в XML не попадают, base64 в форме не показывается.
Порог 20 MiB является только предупреждением, а не нормативным maximum.

Draft v1 уже поддерживает строковые Body values, поэтому сохраняется сам base64
payload без изменения schema/version. Абсолютный путь не сохраняется; после
удаления исходного файла draft восстанавливается. Имя после восстановления —
«Вложение из черновика», размер вычисляется из payload, MIME неизвестен. JSON
может вырасти примерно на треть; attachment storage в рамках MVP не вводилось.

## Acceptance issues

- UAT-004 binary input: **FIXED**;
- UAT-005 boolean presentation: **FIXED**;
- UAT-003 transaction session recovery: **OPEN**, намеренно не затронут;
- UAT-006 numeric TextCtrl: **ACCEPTED**;
- UAT-007–UAT-009: **EXPECTED**;
- UAT-010 long captions: **ACCEPTED**, tooltip и `ⓘ` дают полный текст.
