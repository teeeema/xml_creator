# XSD and model source audit — 2026-10-23

Вердикт: **Недостаточно данных** для официальной XSD-валидации. Уровень B: NOT_EXECUTED. Тайм-аут/TLS-ошибка не доказывают отсутствие публикации.

Стратегия: повторно открыть официальные карточки решений 140/77 и искать точные имена схем/структур версии 1.3.0; проверить официальные реестры схем и моделей по HTTP/HTTPS; сверить сохранённые официальные приложения и явные imports. Сохранённые PDF/Word — нормативные таблицы, не XSD. Нового официального XSD, архива схем или набора модельных зависимостей не получено.

| Адрес | Назначение | Фактический результат | Доказательство |
|---|---|---|---|
| https://docs.eaeunion.org/documents/446/10427/ | 140/2025 | Повторное web-открытие недоступно; сохранённый PDF/Word доступен локально | V130_COMPLETION/sources |
| https://docs.eaeunion.org/documents/463/10765/ | 77/2026 | Повторное web-открытие недоступно; сохранённый PDF/Word доступен локально | V130_COMPLETION/sources |
| https://rseds.eaeunion.org/ | Реестр электронных документов и сведений | curl SSL_ERROR_SYSCALL | verification/rseds_https.txt |
| http://rseds.eaeunion.org/ | Альтернативный протокол реестра | curl Empty reply | verification/rseds_http.txt |
| https://eomi.eaeunion.org/ | Модели данных | curl SSL_ERROR_SYSCALL | verification/eomi_https.txt |
| http://eomi.eaeunion.org/ | Альтернативный протокол моделей | curl Empty reply | verification/eomi_http.txt |
| https://eec.eaeunion.org/upload/iblock/aad/K_1026.pdf | Официальный документ архитектуры | Web-поиск указал официальные rseds/eomi; не является публикацией схем версии 1.3.0 | Primary-source discovery only |

Поиск точных имён схем в официальных доменах не дал загруженного артефакта. Поисковая выдача/карточка без полезной нагрузки не считаются схемой. Хэш недоступного ресурса: N/A, а не выдуманное значение.

## Имеющиеся нормативные артефакты

| Файл | Происхождение/редакция | SHA-256 |
|---|---|---|
| decision_122.pdf | official attachment archived in Stage 1; 140/2025 or 77/2026 by filename | 80e830f82d3c39a2a7a8cf307f413a66c9b61ff7cb54495d3a2fb4b496c9f858 |
| decision_140.pdf | official attachment archived in Stage 1; 140/2025 or 77/2026 by filename | c09bfbe18badeeed967ed51dc00b9b1bd6ff849e7b1843df491bcee48fe3b62c |
| decision_140_word.zip | official attachment archived in Stage 1; 140/2025 or 77/2026 by filename | 100c060e65423aea704d981ba678bf4266a15483a1914362623e349f5ed71d02 |
| decision_77.pdf | official attachment archived in Stage 1; 140/2025 or 77/2026 by filename | e19fef72b499a9afe53b51cc8b26bee0d51dc3609bfd8fb9aed13fb665c48800 |
| decision_77_word.zip | official attachment archived in Stage 1; 140/2025 or 77/2026 by filename | a2be40e33b6cb8d907a5b4a5731fe98f71b38959579c5ff6227e1efc1cd96310 |

## Структуры и зависимости

| Структура | Версия источника | Root URI | Имя XSD из источника (не загруженный файл) | Imports |
|---|---|---|---|---|
| R.006 | Y.Y.Y | urn:EEC:R:ProcessingResultDetails:vY.Y.Y | EEC_R_ProcessingResultDetails_vY.Y.Y.xsd | urn:‌EEC:‌M:‌Complex‌Data‌Objects:v‌X.‌X.‌X; urn:‌EEC:‌M:‌Simple‌Data‌Objects:v‌X.‌X.‌X |
| R.007 | Y.Y.Y | urn:EEC:R:ResourceStatusDetails:vY.Y.Y | EEC_R_ResourceStatusDetails_vY.Y.Y.xsd | urn:‌EEC:‌M:‌Complex‌Data‌Objects:v‌X.‌X.‌X; urn:‌EEC:‌M:‌Simple‌Data‌Objects:v‌X.‌X.‌X |
| R.HC.MM.01.001 | 1.3.0 | urn:EEC:R:HC:MM:01:DrugRegistrationDetails:v1.3.0 | EEC_R_HC_MM_01_DrugRegistrationDetails_v1.3.0.xsd | urn:‌EEC:‌M:‌Complex‌Data‌Objects:v‌X.‌X.‌X; urn:‌EEC:‌M:‌HC:‌Complex‌Data‌Objects:v‌Z.‌Z.‌Z; urn:‌EEC:‌M:‌HC:‌Simple‌Data‌Objects:v‌Z.‌Z.‌Z; urn:‌EEC:‌M:‌Simple‌Data‌Objects:v‌X.‌X.‌X |
| R.HC.MM.01.003 | 1.3.0 | urn:EEC:R:HC:MM:01:DrugRegistrationDocContentDetails:v1.3.0 | EEC_R_HC_MM_01_DrugRegistrationDocContentDetails_v1.3.0.xsd | urn:‌EEC:‌M:‌Complex‌Data‌Objects:v‌X.‌X.‌X; urn:‌EEC:‌M:‌HC:‌Complex‌Data‌Objects:v‌Z.‌Z.‌Z; urn:‌EEC:‌M:‌HC:‌Simple‌Data‌Objects:v‌Z.‌Z.‌Z; urn:‌EEC:‌M:‌Simple‌Data‌Objects:v‌X.‌X.‌X |
| R.HC.MM.01.004 | 1.3.0 | urn:EEC:R:HC:MM:01:DrugRegistrationNumberRequestDetails:v1.3.0 | EEC_R_HC_MM_01_DrugRegistrationNumberRequestDetails_v1.3.0.xsd | urn:‌EEC:‌M:‌Complex‌Data‌Objects:v‌X.‌X.‌X; urn:‌EEC:‌M:‌HC:‌Complex‌Data‌Objects:v‌Z.‌Z.‌Z; urn:‌EEC:‌M:‌HC:‌Simple‌Data‌Objects:v‌Z.‌Z.‌Z; urn:‌EEC:‌M:‌Simple‌Data‌Objects:v‌X.‌X.‌X |
| R.HC.MM.01.006 | 1.3.0 | urn:EEC:R:HC:MM:01:DrugApprovalApplicationRegistrationDossierDetails:v1.3.0 | EEC_R_HC_MM_01_DrugApprovalApplicationRegistrationDossierDetails_v1.3.0.xsd | urn:‌EEC:‌M:‌Complex‌Data‌Objects:v‌X.‌X.‌X; urn:‌EEC:‌M:‌HC:‌Complex‌Data‌Objects:v‌Z.‌Z.‌Z; urn:‌EEC:‌M:‌HC:‌Simple‌Data‌Objects:v‌Z.‌Z.‌Z; urn:‌EEC:‌M:‌Simple‌Data‌Objects:v‌X.‌X.‌X |
| R.HC.MM.01.007 | 1.3.0 | urn:EEC:R:HC:MM:01:DrugRegistrationStatusDetails:v1.3.0 | EEC_R_HC_MM_01_DrugRegistrationStatusDetails_v1.3.0.xsd | urn:‌EEC:‌M:‌Complex‌Data‌Objects:v‌X.‌X.‌X; urn:‌EEC:‌M:‌HC:‌Complex‌Data‌Objects:v‌Z.‌Z.‌Z; urn:‌EEC:‌M:‌HC:‌Simple‌Data‌Objects:v‌Z.‌Z.‌Z; urn:‌EEC:‌M:‌Simple‌Data‌Objects:v‌X.‌X.‌X |

X.X.X/Z.Z.Z — буквальные параметры базисной/отраслевой модели; Y.Y.Y — версия R.006/R.007. Их нельзя подменять 1.3.0. Пять отраслевых root URI подтверждены источниками; 591 QName вложенных элементов не имеет подтверждённого effective URI. 117 атрибутов unqualified и 2 arbitrary XML имеют подтверждённую интерпретацию токена/дерева (119), без доказательства полноты типов/XSD. `xs:any` реализован как исходный произвольный XML без синтетической обёртки; processContents/namespace/compositor требуют официальной схемы.

Уровень A: семь деревьев, 710 строк, явные facets, кратность и 167 локальных предикатов исполняются через существующий Body provider. XML тестов содержит буквальные unresolved URI и не пригоден как production-образец. Уровень A целиком не закрыт: 333 исходные строки требований не завершены. Уровень B требует авторитетного совместимого набора XSD, import/include closure, версии, дат, происхождения и SHA-256 каждого файла.
