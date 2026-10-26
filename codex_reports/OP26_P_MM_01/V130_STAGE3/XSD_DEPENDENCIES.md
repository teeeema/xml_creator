# Официальные XSD, модели и источники данных — этап 3

Вердикт: **Недостаточно данных** для официальной XSD-валидации. Самостоятельные XSD-аналоги не создавались.

Семь source-table деревьев не перестраивались. Пять отраслевых root URI/versions 1.3.0 остаются подтверждёнными таблицами 140/77. R.006/R.007 содержат Y.Y.Y; базисные/отраслевые imports — X.X.X/Z.Z.Z. Не получено нормативного основания заменить эти параметры эффективной версией. 591 effective model QName остаётся неизвестным, 119 source interpretations сохранены; новых QName closure — 0.

| Структура | Root / версия из источника | Зависимости / статус |
|---|---|---|
| R.006 | ProcessingResultDetails / Y.Y.Y | базисная модель X.X.X; официальный XSD не получен |
| R.007 | ResourceStatusDetails / Y.Y.Y | базисная модель X.X.X; официальный XSD не получен |
| R.HC.MM.01.001 | DrugRegistrationDetails / 1.3.0 | ccdo/csdo X.X.X, hccdo/hcsdo Z.Z.Z |
| R.HC.MM.01.003 | DrugRegistrationDocContentDetails / 1.3.0 | те же символические imports |
| R.HC.MM.01.004 | DrugRegistrationNumberRequestDetails / 1.3.0 | те же символические imports |
| R.HC.MM.01.006 | DrugApprovalApplicationRegistrationDossierDetails / 1.3.0 | те же символические imports |
| R.HC.MM.01.007 | DrugRegistrationStatusDetails / 1.3.0 | те же символические imports |

Полные URI, source refs, raw/normalized field names: `QNAME_RESOLUTION.csv`; исходные определения: `P.MM.01_OP_26/versions/1.3.0/structures/source_inventory.json`. Источники 140/77 и SHA-256 сохранены в неизменённом V130_COMPLETION/sources; ссылки и имена схем подробно перечислены в Stage2/XSD_SOURCE_AUDIT.md. Отдельная schema payload не найдена, поэтому её SHA-256/version/dependency closure — UNKNOWN, а не значение, выведенное из имени файла.

## Фактический поиск

- Официальные домены: точные DrugRegistrationDetails / 1.3.0, P.MM.01 и модели; совместимого загруженного XSD не получено.
- `https://rseds.eaeunion.org/ru`, `https://eomi.eaeunion.org/`: web-fetch timeout; Python urllib — unexpected TLS EOF; системный curl — exit 35 SSL_ERROR_SYSCALL. Даты/ошибки: `verification/network_attempts.json`, `xsd_curl_attempts.json`. Результаты прежних HTTP/HTTPS альтернатив сохранены отдельно в Stage2 и не выдаются за новый успешный запрос.
- `https://nsi.eaeunion.org/portal/info`: web открывает пустую HTML/SPA оболочку. Python urllib не доверял цепочке сертификатов, но системный curl с обычной проверкой сертификатов получил официальный сайт и API. Проверка TLS не отключалась. Ошибка одного клиента не объявляется недоступностью NSI в целом.
- Официальная [страница справочников в сфере лекарственных средств](https://eec.eaeunion.org/en/comission/department/deptexreg/formirovanie-obshchikh-rynkov/edinye-reestry-i-informatsionnye-bazy-dannykh/detalizirovannye-svedeniya.php) дала альтернативные portal.eaeunion.org ссылки. Проверены ATC, регистрационное досье, структурные элементы и лекарственные формы: 404 либо timeout. Старая ссылка не подменена неофициальным набором.

## Найденный официальный NSI канал

`https://nsi.eaeunion.org/portal/api/registries/get-by-code-n-date?code=2021&date=2026-10-23` и read-only POST `.../dictionaries/2021/get-list-data[-total]`. Аналогичные endpoint paths извлечены из официального опубликованного JS bundle, сохранённого в verification/nsi_index.js. Использованы только явно напечатанные в каталоге ES NSI codes, без угадывания ID по похожему названию.

22 паспорта получены с versionId, effective dates и publication status. Для 8 наборов подтверждены полные страницы, server count, уникальные record IDs, actual status и literal data.Code; все raw responses и SHA-256 сохранены: `sources/nsi_acquisition.json`, `sources/nsi/`. Дата снимка — 2026-10-23. Это датированные снимки, а не обещание актуальности навсегда. Literal authorityStatus паспорта сохранён как notAvailable без выдуманной интерпретации этого служебного флага; publication_status=published и payload actual проверены отдельно.

Полные наборы: 2021, 1041, 1016, 2044, 2045, 1019, 2046, 1030. Локальные индексы 8 snapshot JSON не являются XSD. Четыре набора (2055, 1066, 1020, 1018) имеют нестандартные/множественные code columns и не активированы через догадку. Ещё 10 паспортов доступны, но data endpoint вернул 502; у 25 из 47 ссылок нет явного NSI binding. Точные результаты каждой ссылки — `CLASSIFIER_STATUS.csv`.

Закрытие XSD GAP требует официального совместимого набора со всеми import/include, effective URI, схемами типов/compositor/xs:any/processContents, происхождением/датой/хэшами и положительной/отрицательной официальной валидацией. До этого уровень B — NOT_EXECUTED; частичные внутренние проверки уровня A не превращаются в нормативный XSD PASS.
