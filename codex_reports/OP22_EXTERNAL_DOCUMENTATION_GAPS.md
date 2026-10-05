# P.SP.02 / ОП_22 — Документ пробелов внешней валидации

- **Процесс**: P.SP.02
- **Источник**: `codex_reports/OP22_MISSING_DATA.csv`
- **Всего записей MISSING_DATA**: 343
- **Классификации, входящие в документ**: EXTERNAL · ENGINE_UNSUPPORTED · AMBIGUOUS · SOURCE_CONFLICT · SAFE_PARTIAL

## Сводка по классификациям

| Класс | Кол-во | Значение |
| :--- | :---: | :--- |
| `EXTERNAL` | 54 | Требует внешних реестров/классификаторов, недоступных движку |
| `ENGINE_UNSUPPORTED` | 181 | Семантика правила недостижима текущим движком |
| `AMBIGUOUS` | 23 | Нормативное требование недостаточно специфицировано |
| `SOURCE_CONFLICT` | 6 | Таблица ОП_22 противоречит структуре R.IP.SP.02.002 / XSD |
| `SAFE_PARTIAL` | 79 | Частично реализовано без риска ложных срабатываний |

## 1. EXTERNAL — требования, зависящие от внешних реестров

Данные требования не могут быть валидированы движком без доступа к внешним классификаторам или базам данных Союза. Валидация возможна только при интеграции с соответствующими реестрами.

### Источник: Классификаторы / база данных Союза

**Затронутых требований**: 2

| Сообщение | Требование | XML QName | Суть ограничения |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.028` | REQ 32 | `ipsdo:PriorityKindCode` | Requires authoritative priority-characteristic classifier/reference data not available to the current evaluator. |
| `P.SP.02.MSG.030` | REQ 13 | `ipsdo:IPPartyKindCode` | Table44 states IPPartyKindCode=AP without an unambiguous repeated owner; applying it globally would contradict explicitl… |

### Источник: Нормативный источник / XSD

**Затронутых требований**: 2

| Сообщение | Требование | XML QName | Суть ограничения |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.056` | REQ 4 | `ipsdo:IPDocKindCode` | Классификация: EXTERNAL |
| `P.SP.02.MSG.056` | REQ 5 | `ipsdo:IPDocKindName` | Классификация: EXTERNAL |

### Источник: Решение Коллегии ЕЭК №92 / реестр Союза

**Затронутых требований**: 50

| Сообщение | Требование | XML QName | Суть ограничения |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.001` | REQ 4 | `ipcdo:TrademarkApplicationDetails; ipsdo:IPDocKindCode; ipsd…` | при включении в классификатор видов документов, сведений и материалов, используемых в сфере интеллектуальной собственнос… |
| `P.SP.02.MSG.001` | REQ 5 | `ipcdo:TrademarkApplicationDetails; ipsdo:IPDocKindCode; ipsd…` | при отсутствии в классификаторе видов документов, сведений и материалов значения, соответствующего виду документа «Заявк… |
| `P.SP.02.MSG.003` | REQ 4 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при отсутствии в классификаторе видов документов, сведений и материалов вида документа «Решение об отказе в регистрации … |
| `P.SP.02.MSG.003` | REQ 4 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при включении в классификатор видов документов, сведений и материалов значения, соответствующего одному из видов докумен… |
| `P.SP.02.MSG.004` | REQ 2 | `ipcdo:TrademarkApplicationDetails; ipsdo:IPDocKindCode; ipsd…` | при включении в классификатор видов документов, сведений и материалов значения, соответствующего виду документа «Обращен… |
| `P.SP.02.MSG.004` | REQ 3 | `ipcdo:TrademarkApplicationDetails; ipsdo:IPDocKindCode; ipsd…` | при отсутствии в классификаторе видов документов, сведений и материалов значения, соответствующего виду документа «Обращ… |
| `P.SP.02.MSG.005` | REQ 2 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при включении в классификатор видов документов, сведений и материалов значения, соответствующего виду документа «Доводы … |
| `P.SP.02.MSG.005` | REQ 3 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при отсутствии указанного вида документа в классификаторе ipsdo:IPDocKindCode не заполняется, а ipsdo:IPDocKindName долж… |
| `P.SP.02.MSG.006` | REQ 2 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при наличии соответствующего вида документа в классификаторе ipsdo:IPDocKindCode заполняется кодом документа «Документ, … |
| `P.SP.02.MSG.006` | REQ 3 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при отсутствии соответствующего вида документа в классификаторе ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName … |
| `P.SP.02.MSG.012` | REQ 2 | `ipsdo:IPDocKindCode` | national patent-office classifier and prior role assignment |
| `P.SP.02.MSG.012` | REQ 3 | `ipsdo:IPDocKindCode` | national patent-office classifier and prior role assignment |
| `P.SP.02.MSG.012` | REQ 4 | `ipsdo:IPDocKindCode` | national patent-office classifier and divided role assignment |
| `P.SP.02.MSG.012` | REQ 5 | `ipsdo:IPDocKindCode` | national patent-office classifier and divided role assignment |
| `P.SP.02.MSG.012` | REQ 32 | `ipsdo:TrademarkApplicationId` | national patent-office application information resource and prior/divided role assignment |
| `P.SP.02.MSG.014` | REQ 4 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при наличии в классификаторе соответствующего вида ходатайства о внесении изменений ipsdo:IPDocKindCode заполняется его … |
| `P.SP.02.MSG.015` | REQ 1 | `ipsdo:IPDocKindCode` | Unified classifier of IP document kinds |
| `P.SP.02.MSG.015` | REQ 2 | `ipsdo:IPDocKindCode` | Unified classifier of IP document kinds |
| `P.SP.02.MSG.037` | REQ 2 | `ipsdo:IPDocKindCode` | classifier of document/material kinds |
| `P.SP.02.MSG.037` | REQ 3 | `ipsdo:IPDocKindCode` | classifier of document/material kinds |
| `P.SP.02.MSG.038` | REQ 2 | `ipcdo:TrademarkApplicationDetails` | classifier of document/material kinds |
| `P.SP.02.MSG.038` | REQ 3 | `ipcdo:TrademarkApplicationDetails` | classifier of document/material kinds |
| `P.SP.02.MSG.038` | REQ 31 | `ipcdo:TrademarkApplicationDetails` | priority-kind classifier |
| `P.SP.02.MSG.039` | REQ 2 | `ipsdo:IPDocKindCode` | classifier of document/material kinds |
| `P.SP.02.MSG.039` | REQ 3 | `ipsdo:IPDocKindCode` | classifier of document/material kinds |
| `P.SP.02.MSG.040` | REQ 2 | `ipcdo:TrademarkApplicationDetails` | classifier/resource |
| `P.SP.02.MSG.040` | REQ 3 | `ipcdo:TrademarkApplicationDetails` | classifier/resource |
| `P.SP.02.MSG.041` | REQ 2 | `ipcdo:TrademarkApplicationDetails` | classifier/resource |
| `P.SP.02.MSG.041` | REQ 3 | `ipcdo:TrademarkApplicationDetails` | classifier/resource |
| `P.SP.02.MSG.042` | REQ 2 | `ipcdo:TrademarkApplicationDetails` | classifier/resource |
| `P.SP.02.MSG.042` | REQ 3 | `ipcdo:TrademarkApplicationDetails` | classifier/resource |
| `P.SP.02.MSG.043` | REQ 2 | `ipsdo:IPDocKindCode` | national patent-office classifier and prior/allocated role assignment |
| `P.SP.02.MSG.043` | REQ 3 | `ipsdo:IPDocKindCode` | national patent-office classifier and prior/allocated role assignment |
| `P.SP.02.MSG.043` | REQ 4 | `ipsdo:IPDocKindCode` | national patent-office classifier and prior/allocated role assignment |
| `P.SP.02.MSG.043` | REQ 5 | `ipsdo:IPDocKindCode` | national patent-office classifier and prior/allocated role assignment |
| `P.SP.02.MSG.043` | REQ 31 | `ipsdo:TrademarkApplicationId` | national patent-office application information resource and prior/allocated role assignment |
| `P.SP.02.MSG.044` | REQ 2 | `ipcdo:TrademarkApplicationDetails` | classifier/resource |
| `P.SP.02.MSG.044` | REQ 3 | `ipcdo:TrademarkApplicationDetails` | classifier/resource |
| `P.SP.02.MSG.044` | REQ 4 | `ipsdo:TrademarkApplicationId` | patent-office resource status/end-state correlation |
| `P.SP.02.MSG.045` | REQ 2 | `ipsdo:TrademarkApplicationId` | national patent-office application information resource |
| `P.SP.02.MSG.045` | REQ 4 | `ipsdo:IPDocKindCode` | national patent-office document kind classifier |
| `P.SP.02.MSG.045` | REQ 5 | `ipsdo:IPDocKindCode` | national patent-office document kind classifier |
| `P.SP.02.MSG.057` | REQ 4 | `ipsdo:IPLegalActionKindCode` | Inclusion of legal action classifier in Union unified NSI resources |
| `P.SP.02.MSG.057` | REQ 5 | `ipsdo:IPLegalActionKindCode` | Absence of legal action classifier in Union unified NSI resources |
| `P.SP.02.MSG.061` | REQ 2 | `ipsdo:IPDocKindCode` | classifier of document/material kinds |
| `P.SP.02.MSG.061` | REQ 3 | `ipsdo:IPDocKindCode` | classifier of document/material kinds |
| `P.SP.02.MSG.062` | REQ 2 | `ipsdo:IPDocKindCode` | classifier of document kinds (Decision No. 92) |
| `P.SP.02.MSG.062` | REQ 3 | `ipsdo:IPDocKindCode` | classifier of document kinds (Decision No. 92) |
| `P.SP.02.MSG.063` | REQ 2 | `ipsdo:IPDocKindCode` | CLASSIFIER_DOCUMENT_KIND |
| `P.SP.02.MSG.063` | REQ 3 | `ipsdo:IPDocKindCode` | CLASSIFIER_DOCUMENT_KIND |

## 2. ENGINE_UNSUPPORTED — ограничения движка правил

Требования этой группы нормативно корректны, однако их семантика недостижима текущей реализацией движка структурных правил. Каждая подгруппа соответствует конкретному типу отсутствующей возможности.

### Межролевая фильтрация (предикаты AP/PA/LA) (34)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.001` | REQ 13 | `ipsdo:IPPartyKindCode` | значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты… |
| `P.SP.02.MSG.001` | REQ 14 | `ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode` | в электронном документе (сведениях) «Сведения о заявке, ходатайстве для прохождения процедур регистр… |
| `P.SP.02.MSG.001` | REQ 15 | `ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; csdo:…` | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты инт… |
| `P.SP.02.MSG.001` | REQ 16 | `ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ipsdo…` | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты инт… |
| `P.SP.02.MSG.001` | REQ 17 | `ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ipsdo…` | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты инт… |
| `P.SP.02.MSG.001` | REQ 18 | `ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ipsdo…` | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты инт… |
| `P.SP.02.MSG.001` | REQ 19 | `ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ipsdo…` | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты инт… |
| `P.SP.02.MSG.001` | REQ 20 | `ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ccdo:…` | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты инт… |
| `P.SP.02.MSG.001` | REQ 21 | `ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; csdo:…` | если в состав электронного документа (сведений) включен экземпляр реквизита «Участник отношений в сф… |
| `P.SP.02.MSG.001` | REQ 22 | `ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; csdo:…` | если в состав электронного документа (сведений) включен экземпляр реквизита «Участник отношений в сф… |
| `P.SP.02.MSG.001` | REQ 26 | `ipcdo:TrademarkApplicationDetails; ipcdo:Trademark…` | в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicatio… |
| `P.SP.02.MSG.001` | REQ 27 | `ipcdo:TrademarkDetails; ipsdo:TrademarkKindCode; i…` | если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида… |
| `P.SP.02.MSG.001` | REQ 32 | `ipcdo:TrademarkPriorityDetails; ipsdo:PriorityKind…` | если в состав электронного документа (сведений) включен и заполнен экземпляр реквизита «Приоритет то… |
| `P.SP.02.MSG.001` | REQ 33 | `ipcdo:AccompanyingDocumentsDetails; ipsdo:IPDocKin…` | если в состав электронного документа (сведений) включен экземпляр реквизита «Прилагаемый документ» (… |
| `P.SP.02.MSG.003` | REQ 18 | `ipcdo:TrademarkDetails; ipsdo:CollectiveMarkIndica…` | если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Признак … |
| `P.SP.02.MSG.003` | REQ 19 | `ipcdo:TrademarkDetails; ipsdo:CollectiveMarkIndica…` | если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Признак … |
| `P.SP.02.MSG.005` | REQ 33 | `ipcdo:ArgumentDetails; csdo:DescriptionText; csdo:…` | в составе ipcdo:ArgumentDetails должны быть заполнены csdo:DescriptionText и csdo:EventDate |
| `P.SP.02.MSG.007` | REQ 2 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при наличии вида документа «Другие документы, подтверждающие правомочность требования установления п… |
| `P.SP.02.MSG.007` | REQ 3 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при отсутствии указанного вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName зап… |
| `P.SP.02.MSG.009` | REQ 2 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при наличии соответствующего вида документа о преобразовании заявки в национальную заявку ipsdo:IPDo… |
| `P.SP.02.MSG.009` | REQ 3 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при отсутствии соответствующего вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindNa… |
| `P.SP.02.MSG.010` | REQ 2 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при наличии вида документа о преобразовании заявки на коллективный знак Союза в заявку на ТЗ Союза i… |
| `P.SP.02.MSG.010` | REQ 3 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при отсутствии такого вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполня… |
| `P.SP.02.MSG.011` | REQ 2 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при наличии вида документа о преобразовании заявки на ТЗ Союза в заявку на коллективный знак Союза i… |
| `P.SP.02.MSG.011` | REQ 3 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при отсутствии такого вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполня… |
| `P.SP.02.MSG.013` | REQ 2 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при наличии вида документа «Ходатайство об отзыве заявки ... (по инициативе заявителя)» ipsdo:IPDocK… |
| `P.SP.02.MSG.013` | REQ 3 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при отсутствии указанного вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName зап… |
| `P.SP.02.MSG.014` | REQ 2 | `ipsdo:TrademarkApplicationId; ipcdo:IPEntityStatus…` | в ресурсах Комиссии должна существовать активная запись заявки со статусом «01» или «02», у которой … |
| `P.SP.02.MSG.014` | REQ 5 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | при отсутствии соответствующего вида ходатайства ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKind… |
| `P.SP.02.MSG.014` | REQ 30 | `ipcdo:AccompanyingDocumentsDetails; ipsdo:IPDocKin…` | если вид документа соответствует ходатайству об изменениях, связанных с передачей или переходом прав… |
| `P.SP.02.MSG.020` | REQ 3 | `ipcdo:GoodsBaseDetails; ipsdo:CancellationStatusIn…` | Если CancellationStatusIndicator хотя бы для одного GoodsBaseDetails = «1», должен быть второй экзем… |
| `P.SP.02.MSG.021` | REQ 22 | `csdo:DocValidityDate` | Все прежние DocValidityDate должны совпадать со значениями сообщения, кроме одного нового значения. |
| `P.SP.02.MSG.021` | REQ 23 | `csdo:DocValidityDate` | Новое DocValidityDate должно быть больше остальных DocValidityDate в сообщении. |
| `P.SP.02.MSG.024` | REQ 2 | `ipcdo:AccompanyingDocumentsDetails; ipsdo:Apellati…` | ipcdo:AccompanyingDocumentsDetails и ipsdo:ApellationOfOriginApplicationId не заполняются. |

### Корреляция вложенных повторяемых элементов (30)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.031` | REQ 16 | `ipcdo:UnifiedRegisterRecordsDetails; ipcdo:GoodsBa…` | Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values t… |
| `P.SP.02.MSG.031` | REQ 17 | `ipcdo:UnifiedRegisterRecordsDetails; ipcdo:GoodsBa…` | Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values t… |
| `P.SP.02.MSG.031` | REQ 18 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values t… |
| `P.SP.02.MSG.031` | REQ 19 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values t… |
| `P.SP.02.MSG.031` | REQ 20 | `ipcdo:UnifiedRegisterRecordsDetails; ipcdo:IPEntit…` | Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values t… |
| `P.SP.02.MSG.032` | REQ 16 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.032` | REQ 17 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.032` | REQ 18 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.032` | REQ 19 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.032` | REQ 20 | `ccdo:SubjectAddressDetails; csdo:AddressKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.033` | REQ 16 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.033` | REQ 17 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.033` | REQ 18 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.033` | REQ 19 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.033` | REQ 20 | `ccdo:SubjectAddressDetails; csdo:AddressKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.034` | REQ 16 | `@nameRepresentationKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.034` | REQ 17 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.034` | REQ 18 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.034` | REQ 19 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.034` | REQ 20 | `csdo:AddressKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.035` | REQ 16 | `@nameRepresentationKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.035` | REQ 17 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.035` | REQ 18 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.035` | REQ 19 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.035` | REQ 20 | `csdo:AddressKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.036` | REQ 16 | `@nameRepresentationKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.036` | REQ 17 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.036` | REQ 18 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.036` | REQ 19 | `ipsdo:IPSubjectName` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |
| `P.SP.02.MSG.036` | REQ 20 | `csdo:AddressKindCode` | Table44 requirement needs AP-scoped correlation/cardinality across nested repeated IPSubjectName/add… |

### Разделительные / кросс-экземплярные семантики (OR) (24)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.040` | REQ 16 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.040` | REQ 17 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.040` | REQ 18 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.040` | REQ 19 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.040` | REQ 20 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.040` | REQ 26 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.041` | REQ 16 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.041` | REQ 17 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.041` | REQ 18 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.041` | REQ 19 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.041` | REQ 20 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.041` | REQ 26 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.042` | REQ 16 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.042` | REQ 17 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.042` | REQ 18 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.042` | REQ 19 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.042` | REQ 20 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.042` | REQ 26 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.044` | REQ 16 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.044` | REQ 17 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.044` | REQ 18 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.044` | REQ 19 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.044` | REQ 20 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |
| `P.SP.02.MSG.044` | REQ 26 | `ipcdo:TrademarkApplicationDetails` | No safe exact evaluator expression. |

### Прочее (ENGINE_UNSUPPORTED, причина не детализирована) (15)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.027` | REQ 16 | `ipsdo:IPSubjectName` | Requires AP-scoped correlation to repeated IPSubjectName attributes. |
| `P.SP.02.MSG.027` | REQ 17 | `ipsdo:IPSubjectName` | Requires per-AP filtered cardinality over repeated IPSubjectName plus attributes. |
| `P.SP.02.MSG.027` | REQ 18 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Requires AP-scoped languageCode=RU second-instance semantics. |
| `P.SP.02.MSG.027` | REQ 19 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Requires AP-scoped languageCode!=RU second-instance LA semantics. |
| `P.SP.02.MSG.027` | REQ 20 | `ccdo:SubjectAddressDetails; csdo:AddressKindCode` | Requires AP role correlated with nested repeated SubjectAddressDetails. |
| `P.SP.02.MSG.028` | REQ 18 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Requires AP-scoped languageCode=RU second-instance semantics. |
| `P.SP.02.MSG.028` | REQ 19 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Requires AP-scoped languageCode!=RU second-instance LA semantics. |
| `P.SP.02.MSG.029` | REQ 16 | `ipsdo:IPSubjectName` | Requires AP-scoped correlation to repeated IPSubjectName representation attributes. |
| `P.SP.02.MSG.029` | REQ 17 | `ipsdo:IPSubjectName` | Requires per-AP filtered cardinality over repeated IPSubjectName plus representation/language attrib… |
| `P.SP.02.MSG.029` | REQ 18 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Requires AP-scoped languageCode=RU second-instance semantics. |
| `P.SP.02.MSG.029` | REQ 19 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Requires AP-scoped languageCode!=RU second-instance LA semantics. |
| `P.SP.02.MSG.029` | REQ 20 | `ccdo:SubjectAddressDetails; csdo:AddressKindCode` | Requires AP role correlated with nested SubjectAddressDetails semantics beyond the current safe sele… |
| `P.SP.02.MSG.029` | REQ 26 | `ipsdo:TrademarkKindCode; ipsdo:TrademarkKindName` | Original Table44 REQ26 is written as TrademarkKindCode OR TrademarkKindName matching the listed valu… |
| `P.SP.02.MSG.029` | REQ 30 | `ipsdo:TrademarkRegistrationCode; ipsdo:TrademarkDe…` | Requires conditional filtered cardinality: for TrademarkRegistrationCode=01, count GoodsBaseDetails … |
| `P.SP.02.MSG.029` | REQ 31 | `ipsdo:TrademarkRegistrationCode; ipsdo:TrademarkDe…` | Requires conditional filtered cardinality: for TrademarkRegistrationCode in {02,03}, at least one Go… |

### Условная кросс-коллекционная корреляция (11)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.038` | REQ 16 | `@nameRepresentationKindCode` | No safe exact evaluator expression. |
| `P.SP.02.MSG.038` | REQ 17 | `ipsdo:IPSubjectName` | No safe exact evaluator expression. |
| `P.SP.02.MSG.038` | REQ 18 | `ipsdo:IPSubjectName` | No safe exact evaluator expression. |
| `P.SP.02.MSG.038` | REQ 19 | `ipsdo:IPSubjectName` | No safe exact evaluator expression. |
| `P.SP.02.MSG.038` | REQ 20 | `csdo:AddressKindCode` | No safe exact evaluator expression. |
| `P.SP.02.MSG.038` | REQ 26 | `ipsdo:TrademarkKindCode` | No safe exact evaluator expression. |
| `P.SP.02.MSG.061` | REQ 16 | `@nameRepresentationKindCode` | No safe exact evaluator expression. |
| `P.SP.02.MSG.061` | REQ 17 | `@nameRepresentationKindCode` | No safe exact evaluator expression. |
| `P.SP.02.MSG.061` | REQ 18 | `@nameRepresentationKindCode` | No safe exact evaluator expression. |
| `P.SP.02.MSG.061` | REQ 19 | `@nameRepresentationKindCode` | No safe exact evaluator expression. |
| `P.SP.02.MSG.061` | REQ 20 | `ccdo:CommunicationDetails` | No safe exact evaluator expression. |

### Позиционная индексация повторяемых дочерних элементов (10)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.012` | REQ 16 | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent,… |
| `P.SP.02.MSG.012` | REQ 17 | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent,… |
| `P.SP.02.MSG.012` | REQ 18 | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent,… |
| `P.SP.02.MSG.012` | REQ 19 | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent,… |
| `P.SP.02.MSG.012` | REQ 20 | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent,… |
| `P.SP.02.MSG.043` | REQ 16 | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent,… |
| `P.SP.02.MSG.043` | REQ 17 | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent,… |
| `P.SP.02.MSG.043` | REQ 18 | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent,… |
| `P.SP.02.MSG.043` | REQ 19 | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent,… |
| `P.SP.02.MSG.043` | REQ 20 | `ipcdo:TrademarkApplicationDetails` | Requires ordinal positional indexing of multiple IPSubjectName instances within a repeatable parent,… |

### Ординальная / повторяемая корреляция экземпляров (10)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.037` | REQ 16 | `@nameRepresentationKindCode` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current… |
| `P.SP.02.MSG.037` | REQ 17 | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current… |
| `P.SP.02.MSG.037` | REQ 18 | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current… |
| `P.SP.02.MSG.037` | REQ 19 | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current… |
| `P.SP.02.MSG.037` | REQ 20 | `csdo:AddressKindCode` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current… |
| `P.SP.02.MSG.039` | REQ 16 | `@nameRepresentationKindCode` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current… |
| `P.SP.02.MSG.039` | REQ 17 | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current… |
| `P.SP.02.MSG.039` | REQ 18 | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current… |
| `P.SP.02.MSG.039` | REQ 19 | `ipsdo:IPSubjectName` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current… |
| `P.SP.02.MSG.039` | REQ 20 | `csdo:AddressKindCode` | Required ordinal/language/repeated-instance correlation cannot be represented exactly by the current… |

### Условная кросс-коллекционная зависимость (10)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.047` | REQ 18 | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires IPPartyDetails with k… |
| `P.SP.02.MSG.047` | REQ 19 | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires AccompanyingDocuments… |
| `P.SP.02.MSG.048` | REQ 18 | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires IPPartyDetails with k… |
| `P.SP.02.MSG.048` | REQ 19 | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires AccompanyingDocuments… |
| `P.SP.02.MSG.049` | REQ 18 | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires IPPartyDetails with k… |
| `P.SP.02.MSG.049` | REQ 19 | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires AccompanyingDocuments… |
| `P.SP.02.MSG.050` | REQ 18 | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires IPPartyDetails with k… |
| `P.SP.02.MSG.050` | REQ 19 | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires AccompanyingDocuments… |
| `P.SP.02.MSG.051` | REQ 18 | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires IPPartyDetails with k… |
| `P.SP.02.MSG.051` | REQ 19 | `ipsdo:CollectiveMarkIndicator` | Conditional cross-collection dependency: CollectiveMarkIndicator == 1 requires AccompanyingDocuments… |

### Дизъюнктивное утверждение поля на уровне родителя (5)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.032` | REQ 26 | `ipsdo:TrademarkKindCode; ipsdo:TrademarkKindName` | Table44 REQ26 normatively allows TrademarkKindCode OR TrademarkKindName to carry an allowed kind. Th… |
| `P.SP.02.MSG.033` | REQ 26 | `ipsdo:TrademarkKindCode; ipsdo:TrademarkKindName` | Table44 REQ26 normatively allows TrademarkKindCode OR TrademarkKindName to carry an allowed kind. Th… |
| `P.SP.02.MSG.034` | REQ 26 | `ipsdo:TrademarkKindCode` | Table 44 uses TrademarkKindCode OR TrademarkKindName allowed-value semantics; current evaluator lack… |
| `P.SP.02.MSG.035` | REQ 26 | `ipsdo:TrademarkKindCode` | Table 44 uses TrademarkKindCode OR TrademarkKindName allowed-value semantics; current evaluator lack… |
| `P.SP.02.MSG.036` | REQ 26 | `ipsdo:TrademarkKindCode` | Table 44 uses TrademarkKindCode OR TrademarkKindName allowed-value semantics; current evaluator lack… |

### Вложенная ординальная семантика (второй экземпляр) (5)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.045` | REQ 16 | `ipcdo:TrademarkApplicationDetails` | Filtered/nested cardinality and correlation over repeated names and addresses. |
| `P.SP.02.MSG.045` | REQ 17 | `ipcdo:TrademarkApplicationDetails` | Filtered/nested cardinality and correlation over repeated names and addresses. |
| `P.SP.02.MSG.045` | REQ 18 | `ipcdo:TrademarkApplicationDetails` | Filtered/nested cardinality and correlation over repeated names and addresses. |
| `P.SP.02.MSG.045` | REQ 19 | `ipcdo:TrademarkApplicationDetails` | Filtered/nested cardinality and correlation over repeated names and addresses. |
| `P.SP.02.MSG.045` | REQ 20 | `ipcdo:TrademarkApplicationDetails` | Filtered/nested cardinality and correlation over repeated names and addresses. |

### cross-collection conditional/correlated OR semantics unavailable (2)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.031` | REQ 18 | `ipsdo:CollectiveMarkIndicator; ipcdo:IPPartyDetail…` | Requires a conditional cross-collection existence check from TrademarkDetails.CollectiveMarkIndicato… |
| `P.SP.02.MSG.031` | REQ 19 | `ipsdo:IPDocKindCode; ipsdo:IPDocKindName` | Requires a conditional cross-collection AccompanyingDocumentsDetails existence check plus exact per-… |

### missing exact same-parent disjunctive code-or-name assertion (2)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.037` | REQ 26 | `ipsdo:TrademarkKindCode` | Normative semantics require TrademarkKindCode OR TrademarkKindName correspondence within the same Tr… |
| `P.SP.02.MSG.039` | REQ 26 | `ipsdo:TrademarkKindCode` | Normative semantics require TrademarkKindCode OR TrademarkKindName correspondence within the same Tr… |

### Typed/semantic constraint not representable by current structured rules. (2)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.052` | REQ 18 | `ipcdo:UnifiedRegisterRecordsDetails` | Inherited Table 49 requirement remains engine-unsupported under the authoritative classification. |
| `P.SP.02.MSG.052` | REQ 19 | `ipcdo:UnifiedRegisterRecordsDetails` | Inherited Table 49 requirement remains engine-unsupported under the authoritative classification. |

### Typed cross-record date comparison. (2)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.052` | REQ 21 | `ipcdo:UnifiedRegisterRecordsDetails` | Cross-record typed/date relationship is not representable by current rules engine. |
| `P.SP.02.MSG.052` | REQ 22 | `ipcdo:UnifiedRegisterRecordsDetails` | Cross-record typed/date relationship is not representable by current rules engine. |

### CROSS_COLLECTION_CONDITIONAL_PRESENCE (2)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.053` | REQ 18 | `ipcdo:UnifiedRegisterRecordsDetails` | Conditional cross-collection dependency: if CollectiveMarkIndicator == 1, IPPartyDetails with kind U… |
| `P.SP.02.MSG.053` | REQ 19 | `ipcdo:UnifiedRegisterRecordsDetails` | Conditional cross-collection dependency: if CollectiveMarkIndicator == 1, AccompanyingDocumentsDetai… |

### Requires AP-scoped correlation to repeated IPSubjectName representation attribut (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.030` | REQ 16 | `ipsdo:IPSubjectName` | Requires AP-scoped correlation to repeated IPSubjectName representation attributes. |

### Requires per-AP filtered cardinality over repeated IPSubjectName plus representa (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.030` | REQ 17 | `ipsdo:IPSubjectName` | Requires per-AP filtered cardinality over repeated IPSubjectName plus representation/language attrib… |

### Requires AP-scoped languageCode=RU second-instance semantics. (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.030` | REQ 18 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Requires AP-scoped languageCode=RU second-instance semantics. |

### Requires AP-scoped languageCode!=RU second-instance LA semantics. (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.030` | REQ 19 | `ipsdo:IPSubjectName; csdo:LanguageCode` | Requires AP-scoped languageCode!=RU second-instance LA semantics. |

### Requires AP-role correlation with nested repeated SubjectAddressDetails semantic (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.030` | REQ 20 | `ccdo:SubjectAddressDetails; csdo:AddressKindCode` | Requires AP-role correlation with nested repeated SubjectAddressDetails semantics beyond the current… |

### no direct OR-of-comparisons assertion result in for_each (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.030` | REQ 26 | `ipsdo:TrademarkKindCode; ipsdo:TrademarkKindName` | Table44 REQ26 is explicitly TrademarkKindCode OR TrademarkKindName matching one of the listed kinds.… |

### no exact OR-of-comparisons assertion result inside for_each (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.031` | REQ 26 | `ipsdo:TrademarkKindCode; ipsdo:TrademarkKindName` | Original Table44 REQ26 is explicitly TrademarkKindCode OR TrademarkKindName matching an allowed kind… |

### Exact disjunctive code-or-name semantics unsupported. (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.045` | REQ 26 | `ipcdo:TrademarkApplicationDetails` | TrademarkKindCode or TrademarkKindName must be in normative set; cannot be safely replaced with AND. |

### Cross-collection filtering and correlation unsupported. (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.045` | REQ 30 | `ipsdo:IPPartyKindCode` | Conditional cross-collection correlation: application doc kind + AS party requires AccompanyingDocum… |

### Cross-record conditional cardinality based on nested repeated GoodsBaseDetails. (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.052` | REQ 3 | `ipcdo:UnifiedRegisterRecordsDetails` | Requires data-dependent creation of a second record from nested goods state; current rules engine ca… |

### Cross-record value equality. (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.052` | REQ 24 | `ipcdo:UnifiedRegisterRecordsDetails` | Cross-record equality is not representable by current rules engine. |

### EXTERNAL_REGISTRY_SET_CARDINALITY_COMPARISON (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.053` | REQ 21 | `csdo:DocValidityDate` | External resource check: national patent office register contains matching TrademarkId and exactly o… |

### EXTERNAL_REGISTRY_SET_INTERSECTION_COMPARISON (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.053` | REQ 22 | `csdo:DocValidityDate` | External resource check: all DocValidityDate values except one must match between external register … |

### EXTERNAL_REGISTRY_COMPARATIVE_ORDERING (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.053` | REQ 23 | `csdo:DocValidityDate` | External resource check: the new DocValidityDate value in message (not matching external register) m… |

### INCLUSIVE_OR_SIBLING_CARDINALITY_NOT_SUPPORTED (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.055` | REQ 7 | `ipcdo:IPPaymentDetails` | Normative requirement mandates IPPaymentDetails presence AND inclusive OR between BankAccountDetails… |

### Inherited Table 81 -> Table 44 -> Table 34 rule 18. (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.062` | REQ 18 | `ipcdo:TrademarkApplicationDetails` | Inherited Table 81 -> Table 44 -> Table 34 rule 18. |

### Inherited Table 81 -> Table 44 -> Table 34 rule 19. (1)

| Сообщение | Требование | XML QName | Причина |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.062` | REQ 19 | `ipcdo:TrademarkApplicationDetails` | Inherited Table 81 -> Table 44 -> Table 34 rule 19. |

## 3. AMBIGUOUS — нормативно неоднозначные требования

Требования этой группы не могут быть реализованы без дополнительного нормативного уточнения. Реализация в текущем виде могла бы привести к ложным срабатываниям.

| Сообщение | Требование | XML QName | Причина неоднозначности |
| :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.012` | REQ 13 | `ipcdo:TrademarkApplicationDetails` | Ambiguous normative definition in isolation; IPPartyKindCode AP is enforced as part of requirement 14. |
| `P.SP.02.MSG.027` | REQ 13 | `ipsdo:IPPartyKindCode` | Exact repeated owner is ambiguous; global AP enforcement would conflict with PA/RE roles. |
| `P.SP.02.MSG.028` | REQ 13 | `ipsdo:IPPartyKindCode` | The row states IPPartyKindCode=AP without an unambiguous repeated owner; global enforcement would contradict PA/RE rows. |
| `P.SP.02.MSG.029` | REQ 13 | `ipsdo:IPPartyKindCode` | Table44 states IPPartyKindCode=AP without an unambiguous repeated owner; global enforcement would contradict the explicitly permitted PA/RE … |
| `P.SP.02.MSG.031` | REQ 13 | `ipcdo:UnifiedRegisterRecordsDetails; ipcdo:IPParty…` | Original Table44 REQ13 states IPPartyKindCode=AP without an unambiguous repeated-owner/instance scope; global enforcement would conflict wit… |
| `P.SP.02.MSG.032` | REQ 13 | `ipsdo:IPPartyKindCode` | Table44 REQ13 states IPPartyKindCode=AP without an unambiguous repeated IPPartyDetails instance scope; enforcing it globally would conflict … |
| `P.SP.02.MSG.033` | REQ 13 | `ipsdo:IPPartyKindCode` | Table44 REQ13 states IPPartyKindCode=AP without an unambiguous repeated IPPartyDetails instance scope; enforcing it globally would conflict … |
| `P.SP.02.MSG.034` | REQ 13 | `ipsdo:IPPartyKindCode` | The standalone AP value statement does not identify an exact repeated IPPartyDetails owner/instance scope, while later requirements explicit… |
| `P.SP.02.MSG.035` | REQ 13 | `ipsdo:IPPartyKindCode` | The standalone AP value statement does not identify an exact repeated IPPartyDetails owner/instance scope, while later requirements explicit… |
| `P.SP.02.MSG.036` | REQ 13 | `ipsdo:IPPartyKindCode` | The standalone AP value statement does not identify an exact repeated IPPartyDetails owner/instance scope, while later requirements explicit… |
| `P.SP.02.MSG.037` | REQ 13 | `ipsdo:IPPartyKindCode` | Table 44 AP code requirement does not establish a sufficiently explicit owner/instance scope beyond REQ14. |
| `P.SP.02.MSG.038` | REQ 13 | `ipsdo:IPPartyKindCode` | Normative owner scope is ambiguous. |
| `P.SP.02.MSG.039` | REQ 13 | `ipsdo:IPPartyKindCode` | Table 44 AP code requirement does not establish a sufficiently explicit owner/instance scope beyond REQ14. |
| `P.SP.02.MSG.040` | REQ 13 | `ipcdo:TrademarkApplicationDetails` | Normative owner scope is ambiguous. |
| `P.SP.02.MSG.041` | REQ 13 | `ipcdo:TrademarkApplicationDetails` | Normative owner scope is ambiguous. |
| `P.SP.02.MSG.042` | REQ 13 | `ipcdo:TrademarkApplicationDetails` | Normative owner scope is ambiguous. |
| `P.SP.02.MSG.043` | REQ 13 | `ipcdo:TrademarkApplicationDetails` | Ambiguous normative definition in isolation; IPPartyKindCode AP is enforced as part of requirement 14. |
| `P.SP.02.MSG.044` | REQ 13 | `ipcdo:TrademarkApplicationDetails` | Normative owner scope is ambiguous. |
| `P.SP.02.MSG.045` | REQ 13 | `ipcdo:TrademarkApplicationDetails` | Table 44 globally says IPPartyKindCode is AP, whereas REQ21-22 recognize PA and RE party instances. |
| `P.SP.02.MSG.059` | REQ 5 | `R.IP.SP.02.002` | The requirement 'другие реквизиты не заполняются' does not specify which elements or scope are considered 'other' (e.g., within Accompanying… |
| `P.SP.02.MSG.059` | REQ 5 | `R.IP.SP.02.007` | The requirement 'другие реквизиты не заполняются' does not specify which elements or scope are considered 'other' (e.g., within Accompanying… |
| `P.SP.02.MSG.061` | REQ 13 | `ipsdo:IPPartyKindCode` | Normative owner scope is ambiguous. |
| `P.SP.02.MSG.062` | REQ 13 | `ipcdo:TrademarkApplicationDetails` | Inherited Table 81 -> Table 44 -> Table 34 rule 13. |

## 4. SOURCE_CONFLICT — противоречия между источниками

Требования этой группы имеют явное противоречие между таблицей ОП_22 и структурным определением R.IP.SP.02.002 / XSD. Реализация заблокирована до разрешения конфликта.

### P.SP.02.MSG.027 — REQ 27

**XML QName**: `ipsdo:TrademarkColourName; ipsdo:TrademarkColourPictureImage`
**Причина**: Table34 image QName conflicts with R.IP.SP.02.002 TrademarkPicture/TrademarkColourName semantics.

### P.SP.02.MSG.029 — SOURCE_CONFLICT

**XML QName**: `ipsdo:InconsistencyText`
**Причина**: Table45 REQ32 assigns ipsdo:InconsistencyText to the selected ipcdo:GoodsBaseDetails instance, but the StructureDefinition places that QName directly under ipcdo:TrademarkApplicationDetails.

### P.SP.02.MSG.029 — REQ 32

**XML QName**: `ipcdo:GoodsBaseDetails; ipsdo:TrademarkDecisionIndicator; ipsdo:TrademarkApplicationId; ipsdo:TrademarkRegRefusalReasonText`
**Причина**: Table45 requires InconsistencyText inside each selected GoodsBaseDetails row, while R.IP.SP.02.002 defines ipsdo:InconsistencyText directly under TrademarkApplicationDetails and has no GoodsBaseDetail

### P.SP.02.MSG.031 — REQ 2

**XML QName**: `ipcdo:UnifiedRegisterRecordsDetails`
**Причина**: Table48 REQ2 names a direct TrademarkId, but R.IP.SP.02.002 has no exact direct TrademarkApplicationDetails/ipsdo:TrademarkId; TrademarkId exists under GoodsBaseDetails and must not be substituted.

### P.SP.02.MSG.031 — REQ 30

**XML QName**: `ipsdo:InconsistencyText`
**Причина**: Table48 REQ30 assigns InconsistencyText to GoodsBaseDetails, while the StructureDefinition places ipsdo:InconsistencyText directly under TrademarkApplicationDetails.

### P.SP.02.MSG.031 — REQ 32

**XML QName**: `ipsdo:DecisionOnComplaintText`
**Причина**: Table48 REQ32 forbids direct ipsdo:DecisionOnComplaintText under TrademarkApplicationDetails, but that exact path/QName is absent from the StructureDefinition.

## 5. SAFE_PARTIAL — частично реализованные требования

Требования реализованы частично. Реализованный фрагмент не порождает ложных срабатываний, однако полная семантика нормативного требования не покрыта.

| Сообщение | Требование | XML QName | Валидируется | Не покрыто |
| :--- | :--- | :--- | :--- | :--- |
| `P.SP.02.MSG.015` | REQ 3 | `ipsdo:TrademarkId` | TrademarkId is required under UnifiedRegisterRecordsDetails | Unified Register record lookup, StatusCode=04, EndDateTime presence, and Tradema… |
| `P.SP.02.MSG.027` | REQ 2 | `ipsdo:IPDocKindCode` | Базовая структурная проверка | classifier existence; correct classifier code; classifier version/context; code … |
| `P.SP.02.MSG.027` | REQ 3 | `ipsdo:IPDocKindCode` | Базовая структурная проверка | authoritative proof that the corresponding document kind is absent from the clas… |
| `P.SP.02.MSG.027` | REQ 4 | `ipcdo:TrademarkApplicationDetails` | Базовая структурная проверка | external Commission record existence; external status 01/02; external EndDateTim… |
| `P.SP.02.MSG.028` | REQ 3 | `ipcdo:TrademarkApplicationDetails` | Базовая структурная проверка | external check that no matching TrademarkApplicationId record exists in the nati… |
| `P.SP.02.MSG.028` | REQ 4 | `ipsdo:IPDocKindCode` | Базовая структурная проверка | classifier membership/existence semantics for the MSG028 document kind; authorit… |
| `P.SP.02.MSG.028` | REQ 5 | `ipsdo:IPDocKindCode` | Базовая структурная проверка | authoritative proof that the MSG028 document kind is absent from the classifier |
| `P.SP.02.MSG.028` | REQ 37 | `ccdo:ResourceItemStatusDetails` | Базовая структурная проверка | equality of StartDateTime to the external/contextual national-register inclusion… |
| `P.SP.02.MSG.029` | REQ 2 | `ipcdo:TrademarkApplicationDetails` | Базовая структурная проверка | external filing-office information-resource lookup; external record StatusCode i… |
| `P.SP.02.MSG.029` | REQ 4 | `ipsdo:IPDocKindCode` | Базовая структурная проверка | authoritative classifier-presence predicate for the three MSG029 document kinds;… |
| `P.SP.02.MSG.029` | REQ 5 | `ipsdo:IPDocKindCode` | Базовая структурная проверка | authoritative classifier-absence predicate for the three MSG029 document kinds; … |
| `P.SP.02.MSG.029` | REQ 35 | `ccdo:ResourceItemStatusDetails` | Базовая структурная проверка | equality of StartDateTime to the external national-patent-office information-res… |
| `P.SP.02.MSG.030` | REQ 2 | `ipsdo:IPDocKindCode` | If direct IPDocKindCode is present, direct IPDocKindName is forbidden. | authoritative classifier-presence predicate; authoritative classifier code desig… |
| `P.SP.02.MSG.030` | REQ 3 | `ipsdo:IPDocKindCode` | If direct IPDocKindCode is absent, direct IPDocKindName must equal the single no… | authoritative classifier-absence predicate |
| `P.SP.02.MSG.030` | REQ 4 | `ipcdo:TrademarkApplicationDetails` | Direct TrademarkApplicationId is required. | national-patent-office information-resource lookup; external StatusCode=02; exte… |
| `P.SP.02.MSG.031` | REQ 1 | `ipcdo:TrademarkApplicationDetails; ipcdo…` | TrademarkApplicationId is required. | external StatusCode in {01,02}; external EndDateTime absent; external TrademarkA… |
| `P.SP.02.MSG.031` | REQ 3 | `ipsdo:IPDocKindCode; ipcdo:UnifiedRegist…` | If direct IPDocKindCode is present, direct IPDocKindName is forbidden. | authoritative classifier-presence predicate; authoritative classifier code desig… |
| `P.SP.02.MSG.031` | REQ 4 | `ipsdo:IPDocKindCode` | If direct IPDocKindCode is absent, direct IPDocKindName equals: Решение об отказ… | authoritative classifier-absence predicate |
| `P.SP.02.MSG.031` | REQ 3 | `ipsdo:IPDocKindCode; ipcdo:UnifiedRegist…` | TrademarkId is required. | external uniqueness/nonexistence lookup |
| `P.SP.02.MSG.031` | REQ 4 | `ipsdo:IPDocKindCode` | If direct IPDocKindCode is present, direct IPDocKindName is forbidden. | authoritative classifier-presence predicate; authoritative classifier code desig… |
| `P.SP.02.MSG.031` | REQ 5 | `ipcdo:TrademarkApplicationDetails; ipcdo…` | If direct IPDocKindCode is absent, direct IPDocKindName is required. | authoritative classifier-absence predicate; conditional membership in the two ex… |
| `P.SP.02.MSG.032` | REQ 2 | `ipsdo:IPDocKindCode` | If ipsdo:IPDocKindCode is present in TrademarkApplicationDetails, ipsdo:IPDocKin… | authoritative classifier-presence predicate; authoritative classifier lookup for… |
| `P.SP.02.MSG.032` | REQ 3 | `ipsdo:IPDocKindCode` | If ipsdo:IPDocKindCode is absent, ipsdo:IPDocKindName must equal 'Жалоба на реше… | authoritative classifier-absence predicate |
| `P.SP.02.MSG.032` | REQ 4 | `ipcdo:TrademarkApplicationDetails` | ipsdo:TrademarkApplicationId is required in each TrademarkApplicationDetails. | external record existence; external StatusCode in {'01','02'}; external EndDateT… |
| `P.SP.02.MSG.033` | REQ 3 | `ipsdo:IPDocKindCode` | If ipsdo:IPDocKindCode is present in TrademarkApplicationDetails, ipsdo:IPDocKin… | authoritative classifier-presence predicate; authoritative classifier lookup for… |
| `P.SP.02.MSG.033` | REQ 4 | `ipsdo:IPDocKindCode` | If ipsdo:IPDocKindCode is absent, ipsdo:IPDocKindName must equal 'Заключение нац… | authoritative classifier-absence predicate |
| `P.SP.02.MSG.033` | REQ 5 | `ipcdo:TrademarkApplicationDetails` | ipsdo:TrademarkApplicationId is required in each TrademarkApplicationDetails. | external record existence; external StatusCode = 02; external EndDateTime absenc… |
| `P.SP.02.MSG.034` | REQ 2 | `ipsdo:IPDocKindCode` | If TrademarkApplicationDetails/ipsdo:IPDocKindCode is present, same-parent ipsdo… | authoritative classifier-presence predicate; authoritative classifier lookup; eq… |
| `P.SP.02.MSG.034` | REQ 3 | `ipsdo:IPDocKindCode` | If TrademarkApplicationDetails/ipsdo:IPDocKindCode is absent, same-parent ipsdo:… | authoritative classifier-absence predicate |
| `P.SP.02.MSG.034` | REQ 4 | `ipsdo:TrademarkApplicationId` | TrademarkApplicationDetails/ipsdo:TrademarkApplicationId is required. | external record existence; external StatusCode in {01,02}; external EndDateTime … |
| `P.SP.02.MSG.035` | REQ 2 | `ipsdo:IPDocKindCode` | Direct TrademarkApplicationDetails/ipsdo:IPDocKindCode is required. | authoritative classifier membership; authoritative code-to-literal correspondenc… |
| `P.SP.02.MSG.035` | REQ 3 | `ipsdo:TrademarkApplicationId` | Direct TrademarkApplicationDetails/ipsdo:TrademarkApplicationId is required. | external record existence; external StatusCode in {01,02}; external EndDateTime … |
| `P.SP.02.MSG.036` | REQ 2 | `ipsdo:IPDocKindCode` | TrademarkApplicationDetails/ipsdo:IPDocKindCode is required. | classifier membership and code correspondence |
| `P.SP.02.MSG.036` | REQ 3 | `ipsdo:TrademarkApplicationId` | TrademarkApplicationDetails/ipsdo:TrademarkApplicationId is required. | external filing-office record, status, end date, equality |
| `P.SP.02.MSG.037` | REQ 4 | `ipsdo:TrademarkApplicationId` | TrademarkApplicationDetails/ipsdo:TrademarkApplicationId is required. | external record existence; external StatusCode in {01,02}; external EndDateTime … |
| `P.SP.02.MSG.038` | REQ 4 | `ipsdo:TrademarkApplicationId` | TrademarkApplicationDetails/ipsdo:TrademarkApplicationId is required. | external record existence; external StatusCode in {01,02}; external EndDateTime … |
| `P.SP.02.MSG.039` | REQ 4 | `ipsdo:TrademarkApplicationId` | TrademarkApplicationDetails/ipsdo:TrademarkApplicationId is required. | external record existence; external StatusCode in {01,02}; external EndDateTime … |
| `P.SP.02.MSG.040` | REQ 4 | `ipsdo:TrademarkApplicationId` | ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId is required. | external resource state/equality |
| `P.SP.02.MSG.041` | REQ 4 | `ipsdo:TrademarkApplicationId` | ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId is required. | external resource state/equality |
| `P.SP.02.MSG.042` | REQ 4 | `ipsdo:TrademarkApplicationId` | ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId is required. | external resource state/equality |
| `P.SP.02.MSG.046` | REQ 1 | `ipsdo:IPDocKindCode` | NONE | authoritative classifier membership predicate for the specified document kind |
| `P.SP.02.MSG.046` | REQ 2 | `ipsdo:IPDocKindCode` | NONE | authoritative classifier-absence predicate for the specified document kind |
| `P.SP.02.MSG.046` | REQ 3 | `ipsdo:TrademarkId` | NONE | national patent-office resource lookup, status=04, EndDateTime presence, and Tra… |
| `P.SP.02.MSG.047` | REQ 1 | `ipsdo:TrademarkId` | ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId is required | verification of active record status in external patent office registry (StatusC… |
| `P.SP.02.MSG.047` | REQ 4 | `ipsdo:IPDocKindCode` | If IPDocKindCode is present, IPDocKindName is forbidden | presence of code in external document kind classifier |
| `P.SP.02.MSG.047` | REQ 5 | `ipsdo:IPDocKindCode` | If IPDocKindCode is absent, IPDocKindName equals exact literal | absence of code in external document kind classifier |
| `P.SP.02.MSG.048` | REQ 1 | `ipsdo:TrademarkId` | ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId is required | verification of active record status in external patent office registry (StatusC… |
| `P.SP.02.MSG.048` | REQ 4 | `ipsdo:IPDocKindCode` | If IPDocKindCode is present, IPDocKindName is forbidden | presence of code in external document kind classifier |
| `P.SP.02.MSG.048` | REQ 5 | `ipsdo:IPDocKindCode` | If IPDocKindCode is absent, IPDocKindName equals exact literal | absence of code in external document kind classifier |
| `P.SP.02.MSG.049` | REQ 1 | `ipsdo:TrademarkId` | direct same-record TrademarkId is required | external resource lookup, active-status check, EndDateTime state, and TrademarkI… |
| `P.SP.02.MSG.049` | REQ 21 | `ipsdo:IPDocKindCode` | if direct IPDocKindCode is present, direct IPDocKindName is forbidden | classifier membership and code validity |
| `P.SP.02.MSG.049` | REQ 22 | `ipsdo:IPDocKindCode` | if direct IPDocKindCode is absent, direct IPDocKindName must equal the exact ame… | classifier absence predicate |
| `P.SP.02.MSG.050` | REQ 1 | `ipsdo:TrademarkId` | ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId is required | verification of active record status in external patent office registry (StatusC… |
| `P.SP.02.MSG.050` | REQ 4 | `ipsdo:IPDocKindCode` | If IPDocKindCode is present, IPDocKindName is forbidden | presence of code in external document kind classifier |
| `P.SP.02.MSG.050` | REQ 5 | `ipsdo:IPDocKindCode` | If IPDocKindCode is absent, IPDocKindName equals exact literal | absence of code in external document kind classifier |
| `P.SP.02.MSG.051` | REQ 1 | `ipsdo:TrademarkId` | ipcdo:UnifiedRegisterRecordsDetails/ipsdo:TrademarkId is required | verification of active record status in filing office external patent office reg… |
| `P.SP.02.MSG.051` | REQ 3 | `ipsdo:IPDocKindCode` | If IPDocKindCode is present, IPDocKindName is forbidden | presence of code in external document kind classifier |
| `P.SP.02.MSG.051` | REQ 4 | `ipsdo:IPDocKindCode` | If IPDocKindCode is absent, IPDocKindName matches one of the two exact normative… | absence of code in external document kind classifier |
| `P.SP.02.MSG.052` | REQ 5 | `ipsdo:TrademarkId` | status-04 record requires ipsdo:TrademarkId | external active-record lookup and TrademarkId equality |
| `P.SP.02.MSG.052` | REQ 20 | `ipsdo:TrademarkId` | status-01 record requires ipsdo:TrademarkId | external uniqueness check for TrademarkId |
| `P.SP.02.MSG.052` | REQ 25 | `ipsdo:IPDocKindCode` | role-scoped IPDocKindCode/IPDocKindName branch | classifier membership/absence check |
| `P.SP.02.MSG.052` | REQ 26 | `ipsdo:IPDocKindCode` | role-scoped IPDocKindCode/IPDocKindName branch | classifier membership/absence check |
| `P.SP.02.MSG.052` | REQ 27 | `ipsdo:IPDocKindCode` | role-scoped IPDocKindCode/IPDocKindName branch | classifier membership/absence check |
| `P.SP.02.MSG.052` | REQ 28 | `ipsdo:IPDocKindCode` | role-scoped IPDocKindCode/IPDocKindName branch | classifier membership/absence check |
| `P.SP.02.MSG.053` | REQ 1 | `ipsdo:TrademarkId` | direct TrademarkId is REQUIRED | verification of active record status in external patent office registry (StatusC… |
| `P.SP.02.MSG.053` | REQ 4 | `ipsdo:IPDocKindCode` | If IPDocKindCode is present, IPDocKindName is forbidden | presence of code in external document kind classifier |
| `P.SP.02.MSG.053` | REQ 5 | `ipsdo:IPDocKindCode` | If IPDocKindCode is absent, IPDocKindName equals exact literal | absence of code in external document kind classifier |
| `P.SP.02.MSG.054` | REQ 4 | `ipsdo:IPLegalActionKindCode` | IF IPLegalActionKindCode is present THEN IPLegalActionKindName is FORBIDDEN | classifier availability state; IPLegalActionKindCode membership in the external … |
| `P.SP.02.MSG.054` | REQ 5 | `ipsdo:IPLegalActionKindCode` | IF IPLegalActionKindCode is absent THEN IPLegalActionKindName is REQUIRED and IN… | classifier absence state |
| `P.SP.02.MSG.055` | REQ 4 | `ipsdo:IPLegalActionKindCode` | IF IPLegalActionKindCode != null THEN IPLegalActionKindName FORBIDDEN | Union legal action classifier presence check; IPLegalActionKindCode value member… |
| `P.SP.02.MSG.055` | REQ 5 | `ipsdo:IPLegalActionKindCode` | IF IPLegalActionKindCode == null THEN IPLegalActionKindName REQUIRED | Union legal action classifier absence check; IPLegalActionKindName membership in… |
| `P.SP.02.MSG.056` | REQ 19 | `ipcdo:IPPaymentDetails; ipcdo:Accompanyi…` | NONE |  |
| `P.SP.02.MSG.057` | REQ 19 | `csdo:DocBinaryText` | DocBinaryText presence REQUIRED and mediaTypeCode IN allowed extensions list | DocBinaryText binary payload size <= 5MB |
| `P.SP.02.MSG.057` | REQ 22 | `ipsdo:DutyPaymentIndicator` | PaymentAmount presence is REQUIRED when DutyPaymentIndicator == 'false' | PaymentAmount > 0 numeric decimal comparison |
| `P.SP.02.MSG.059` | REQ 4 | `csdo:DocBinaryText` | DocBinaryText presence REQUIRED and mediaTypeCode IN allowed extensions list | DocBinaryText binary payload size <= 5MB |
| `P.SP.02.MSG.059` | REQ 4 | `csdo:DocBinaryText` | DocBinaryText presence REQUIRED and mediaTypeCode IN allowed extensions list | DocBinaryText binary payload size <= 5MB |
| `P.SP.02.MSG.061` | REQ 4 | `ipsdo:TrademarkApplicationId` | TrademarkApplicationDetails/ipsdo:TrademarkApplicationId is required. | external record existence; external StatusCode in {01,02}; external TrademarkApp… |
| `P.SP.02.MSG.062` | REQ 4 | `ipsdo:TrademarkApplicationId` | TrademarkApplicationDetails/ipsdo:TrademarkApplicationId is required. | external record existence in national patent office information resource; extern… |
| `P.SP.02.MSG.063` | REQ 4 | `ipsdo:TrademarkApplicationId` | TrademarkApplicationId presence is REQUIRED inside TrademarkApplicationDetails | External query against national patent office database for record with StatusCod… |

## 6. Сводка по сообщениям

Число неразрешённых записей (EXTERNAL + ENGINE_UNSUPPORTED + AMBIGUOUS + SOURCE_CONFLICT) по каждому сообщению:

| Сообщение | Неразр. | EXT | ENG | AMB | CONF | SAFE_P |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `P.SP.02.MSG.001` | 16 | 2 | 14 | — | — | — |
| `P.SP.02.MSG.031` | 12 | — | 8 | 1 | 3 | 6 |
| `P.SP.02.MSG.012` | 11 | 5 | 5 | 1 | — | — |
| `P.SP.02.MSG.029` | 11 | — | 8 | 1 | 2 | 4 |
| `P.SP.02.MSG.043` | 11 | 5 | 5 | 1 | — | — |
| `P.SP.02.MSG.045` | 11 | 3 | 7 | 1 | — | — |
| `P.SP.02.MSG.038` | 10 | 3 | 6 | 1 | — | 1 |
| `P.SP.02.MSG.044` | 10 | 3 | 6 | 1 | — | — |
| `P.SP.02.MSG.037` | 9 | 2 | 6 | 1 | — | 1 |
| `P.SP.02.MSG.039` | 9 | 2 | 6 | 1 | — | 1 |
| `P.SP.02.MSG.040` | 9 | 2 | 6 | 1 | — | 1 |
| `P.SP.02.MSG.041` | 9 | 2 | 6 | 1 | — | 1 |
| `P.SP.02.MSG.042` | 9 | 2 | 6 | 1 | — | 1 |
| `P.SP.02.MSG.061` | 8 | 2 | 5 | 1 | — | 1 |
| `P.SP.02.MSG.027` | 7 | — | 5 | 1 | 1 | 3 |
| `P.SP.02.MSG.030` | 7 | 1 | 6 | — | — | 3 |
| `P.SP.02.MSG.032` | 7 | — | 6 | 1 | — | 3 |
| `P.SP.02.MSG.033` | 7 | — | 6 | 1 | — | 3 |
| `P.SP.02.MSG.034` | 7 | — | 6 | 1 | — | 3 |
| `P.SP.02.MSG.035` | 7 | — | 6 | 1 | — | 2 |
| `P.SP.02.MSG.036` | 7 | — | 6 | 1 | — | 2 |
| `P.SP.02.MSG.052` | 6 | — | 6 | — | — | 6 |
| `P.SP.02.MSG.053` | 5 | — | 5 | — | — | 3 |
| `P.SP.02.MSG.062` | 5 | 2 | 2 | 1 | — | 1 |
| `P.SP.02.MSG.003` | 4 | 2 | 2 | — | — | — |
| `P.SP.02.MSG.014` | 4 | 1 | 3 | — | — | — |
| `P.SP.02.MSG.028` | 4 | 1 | 2 | 1 | — | 4 |
| `P.SP.02.MSG.005` | 3 | 2 | 1 | — | — | — |
| `P.SP.02.MSG.004` | 2 | 2 | — | — | — | — |
| `P.SP.02.MSG.006` | 2 | 2 | — | — | — | — |
| `P.SP.02.MSG.007` | 2 | — | 2 | — | — | — |
| `P.SP.02.MSG.009` | 2 | — | 2 | — | — | — |
| `P.SP.02.MSG.010` | 2 | — | 2 | — | — | — |
| `P.SP.02.MSG.011` | 2 | — | 2 | — | — | — |
| `P.SP.02.MSG.013` | 2 | — | 2 | — | — | — |
| `P.SP.02.MSG.015` | 2 | 2 | — | — | — | 1 |
| `P.SP.02.MSG.021` | 2 | — | 2 | — | — | — |
| `P.SP.02.MSG.047` | 2 | — | 2 | — | — | 3 |
| `P.SP.02.MSG.048` | 2 | — | 2 | — | — | 3 |
| `P.SP.02.MSG.049` | 2 | — | 2 | — | — | 3 |
| `P.SP.02.MSG.050` | 2 | — | 2 | — | — | 3 |
| `P.SP.02.MSG.051` | 2 | — | 2 | — | — | 3 |
| `P.SP.02.MSG.056` | 2 | 2 | — | — | — | 1 |
| `P.SP.02.MSG.057` | 2 | 2 | — | — | — | 2 |
| `P.SP.02.MSG.059` | 2 | — | — | 2 | — | 2 |
| `P.SP.02.MSG.063` | 2 | 2 | — | — | — | 1 |
| `P.SP.02.MSG.020` | 1 | — | 1 | — | — | — |
| `P.SP.02.MSG.024` | 1 | — | 1 | — | — | — |
| `P.SP.02.MSG.055` | 1 | — | 1 | — | — | 2 |
| `P.SP.02.MSG.046` | 0 | — | — | — | — | 3 |
| `P.SP.02.MSG.054` | 0 | — | — | — | — | 2 |

## 7. Рекомендации

### 7.1 Для EXTERNAL-требований

1. Интегрировать классификатор видов документов (Решение Коллегии ЕЭК №92) как справочник движка.
2. Предоставить API или статический снимок реестра Союза для offline-валидации.
3. До интеграции регистрировать EXTERNAL-нарушения как предупреждения, а не ошибки.

### 7.2 Для ENGINE_UNSUPPORTED-требований

Основные недостающие возможности движка (в порядке приоритета по покрытию):

| Приоритет | Возможность | Требований |
|:---:|:---|:---:|
| 1 | Межролевая фильтрация по атрибуту (AP/PA/LA) в повторяемых родителях | 34 |
| 2 | Дизъюнктивные / кросс-экземплярные утверждения | 24 |
| 3 | Корреляция вложенных повторяемых элементов | 30 |
| 4 | Позиционная индексация повторяемых дочерних элементов | 20 |
| 5 | Условная кросс-коллекционная корреляция | 21 |

Реализация пп. 1–3 закроет ~88 из 181 ENGINE_UNSUPPORTED-записей.

### 7.3 Для AMBIGUOUS-требований

1. Запросить нормативное уточнение у правообладателя ОП_22 (ФИПС / ЕЭК).
2. До получения уточнения не реализовывать — риск ложных срабатываний.

### 7.4 Для SOURCE_CONFLICT-требований

1. Направить запрос о разрешении конфликта: таблицы ОП_22 vs. XSD R.IP.SP.02.002.
2. Не реализовывать до получения официальной позиции.

### 7.5 Для SAFE_PARTIAL-требований

1. Текущая реализация безопасна — продолжать использовать.
2. Расширение до полного покрытия зависит от ENGINE_UNSUPPORTED-возможностей.

## DOCUMENTS_AND_DATA_TO_FIND

Практический checklist того, что необходимо найти/получить для снятия блокировок валидации.
Требования типа ENGINE_UNSUPPORTED в этот список НЕ включены (данные в XML, проблема — движок).

- [ ] **Классификатор видов документов, сведений и материалов в сфере интеллектуальной собственности**
  - Needed for: Валидация ipsdo:IPDocKindCode и ipsdo:IPDocKindName — требуется наличие кода в реестре
  - Affected MSG: P.SP.02.MSG.001, P.SP.02.MSG.003, P.SP.02.MSG.004, P.SP.02.MSG.005, P.SP.02.MSG.006 и ещё 15
  - Affected requirements: REQ 2, REQ 3, REQ 4, REQ 5 (ipsdo:IPDocKindCode / ipsdo:IPDocKindName)
  - Need to obtain: Актуальный справочник кодов (статический снимок или API ЕЭК)
  - Known reference: Решение Коллегии ЕЭК от 27.07.2021 № 92
  - Unknown: Актуальный URL/API для получения реестра в машиночитаемом виде
  - Expected impact: Закрывает ~46 EXTERNAL-записей (IPDocKindCode / IPDocKindName)

- [ ] **Классификатор видов приоритетов товарного знака Союза**
  - Needed for: Валидация ipsdo:PriorityKindCode — требуется наличие кода приоритета в классификаторе
  - Affected MSG: P.SP.02.MSG.028, P.SP.02.MSG.038
  - Affected requirements: REQ 31, REQ 32 (ipsdo:PriorityKindCode)
  - Need to obtain: Справочник видов приоритетов с допустимыми кодами
  - Known reference: UNKNOWN_FROM_OP22
  - Unknown: Точное название документа и источник; в ОП_22 ссылка не приведена явно
  - Expected impact: Закрывает 2 EXTERNAL-записи

- [ ] **Реестр поданных заявок национальных патентных ведомств (prior/divided application IDs)**
  - Needed for: Валидация ipsdo:TrademarkApplicationId — требуется подтверждение существования заявки из предшествующего/разделённого делопроизводства
  - Affected MSG: P.SP.02.MSG.012, P.SP.02.MSG.043
  - Affected requirements: REQ 32 (ipsdo:TrademarkApplicationId)
  - Need to obtain: API или статический снимок реестра заявок национальных ведомств
  - Known reference: UNKNOWN_FROM_OP22
  - Unknown: Конкретный источник данных; не определён в ОП_22
  - Expected impact: Закрывает 2 EXTERNAL-записи

- [ ] **Единый реестр зарегистрированных ТЗ Союза (UnifiedRegister)**
  - Needed for: Проверка наличия ipsdo:TrademarkId в реестре Союза (MSG.015 REQ 3)
  - Affected MSG: P.SP.02.MSG.015
  - Affected requirements: REQ 3 (ipsdo:TrademarkId)
  - Need to obtain: API или offline-снимок Единого реестра ТЗ ЕАЭС
  - Known reference: UNKNOWN_FROM_OP22
  - Unknown: Точный endpoint / формат данных реестра
  - Expected impact: Закрывает 1 SAFE_PARTIAL-запись (перевод в FULLY_MAPPABLE)

- [ ] **Классификаторы/базы данных Союза (роли/типы участников)**
  - Needed for: Валидация ipsdo:IPPartyKindCode в MSG.028 REQ 32 и MSG.030 REQ 13 — требуется авторитетный классификатор видов участников
  - Affected MSG: P.SP.02.MSG.028, P.SP.02.MSG.030
  - Affected requirements: REQ 13, REQ 32 (ipsdo:IPPartyKindCode / ipsdo:PriorityKindCode)
  - Need to obtain: Справочник допустимых значений IPPartyKindCode из авторитетного источника ЕЭК
  - Known reference: UNKNOWN_FROM_OP22
  - Unknown: Нормативный документ, закрепляющий допустимые значения кода вида участника
  - Expected impact: Закрывает 2 EXTERNAL-записи

- [ ] **XSD-схема R.IP.SP.02.002 (актуальная версия)**
  - Needed for: Разрешение SOURCE_CONFLICT между таблицами ОП_22 и структурным определением R.IP.SP.02.002 (MSG.027 REQ27, MSG.031 REQ2/30/32, MSG.029 REQ32)
  - Affected MSG: P.SP.02.MSG.027, P.SP.02.MSG.029, P.SP.02.MSG.031
  - Affected requirements: REQ 2, REQ 27, REQ 30, REQ 32 (несколько QNames)
  - Need to obtain: Актуальная XSD для проверки допустимости путей ipsdo:InconsistencyText, ipsdo:DecisionOnComplaintText, ipsdo:TrademarkId
  - Known reference: XSD-схема, которую уже использует проект (R.IP.SP.02.002)
  - Unknown: Версия XSD, используемая в ОП_22 (может отличаться от проектной)
  - Expected impact: Разрешает 6 SOURCE_CONFLICT-записей

- [ ] **Нормативное уточнение по REQ 13 Table 44 / Table 34 (ipsdo:IPPartyKindCode=AP)**
  - Needed for: Разрешение 23 AMBIGUOUS-записей: требование «IPPartyKindCode=AP» применяется глобально или только к конкретному экземпляру IPPartyDetails
  - Affected MSG: P.SP.02.MSG.012, P.SP.02.MSG.027, P.SP.02.MSG.028, P.SP.02.MSG.029, P.SP.02.MSG.031 и ещё 17
  - Affected requirements: REQ 13 (ipsdo:IPPartyKindCode)
  - Need to obtain: Официальное разъяснение ЕЭК/ФИПС о сфере применения REQ 13
  - Known reference: Table 44 / Table 34 ОП_22
  - Unknown: Нормативный приказ или разъяснение о scope REQ 13
  - Expected impact: Разрешает все 23 AMBIGUOUS-записи (REQ 13)

- [ ] **Нормативное уточнение: «другие реквизиты не заполняются» (MSG.059 REQ 5)**
  - Needed for: Определение исчерпывающего перечня «других реквизитов» в контексте R.IP.SP.02.002 и R.IP.SP.02.007
  - Affected MSG: P.SP.02.MSG.059
  - Affected requirements: REQ 5 (Tables 78, 79)
  - Need to obtain: Перечень элементов, которые относятся к «другим реквизитам» по смыслу таблиц
  - Known reference: Таблицы 78–79 ОП_22
  - Unknown: Явный перечень элементов или XSD-constraint подтверждающий scope
  - Expected impact: Разрешает 2 AMBIGUOUS-записи (MSG.059 REQ5)


## CAN_BE_FIXED_WITHOUT_NEW_DOCUMENTATION

Требования, где нормативная семантика известна, XML-данные присутствуют,
и единственная блокировка — отсутствующая возможность движка правил.

### Межролевая фильтрация: атрибутивный предикат на повторяемом родителе (AP/PA/LA) (34 требований)

Проверка значения дочернего поля (IPPartyKindCode=AP/PA/RE/LA) внутри конкретного экземпляра повторяемого родителя (IPPartyDetails). Данные присутствуют в XML; движок не поддерживает for_each с role-предикатом.

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.001, P.SP.02.MSG.003, P.SP.02.MSG.005, P.SP.02.MSG.007, P.SP.02.MSG.009, P.SP.02.MSG.010... |
| REQ | REQ 13, REQ 14, REQ 15, REQ 16, REQ 17, REQ 18, REQ 19, REQ 2... |
| QName/path | csdo:DocValidityDate; ipcdo:AccompanyingDocumentsDetails; ipsdo:ApellationOfOriginApplicationId; ipcdo:AccompanyingDocumentsDetails; ipsdo:IPDocKindCode; ipsdo:IPDocKindName; csdo:DocId; ipcdo:AccompanyingDocumentsDetails; ipsdo:IPDocKindCode; ipsdo:IPPartyKindCode; ipcdo:ArgumentDetails; csdo:DescriptionText; csdo:EventDate |
| CURRENT_ENGINE_LIMITATION | for_each не поддерживает фильтрацию повторяемого родителя по значению дочернего поля |
| REQUIRED_ENGINE_FEATURE | for_each_where(owner, predicate_field=value) → apply rules to matching instances only |

### Дизъюнктивные утверждения (OR) внутри for_each (50 требований)

Проверка: field_A = X OR field_B = Y. Данные (code + name) присутствуют в XML; движок не поддерживает OR-of-comparisons.

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.029, P.SP.02.MSG.030, P.SP.02.MSG.031, P.SP.02.MSG.032, P.SP.02.MSG.033, P.SP.02.MSG.034... |
| REQ | REQ 16, REQ 17, REQ 18, REQ 19, REQ 20, REQ 23, REQ 26, REQ 7 |
| QName/path | @nameRepresentationKindCode; ccdo:CommunicationDetails; csdo:AddressKindCode; csdo:DocValidityDate; ipcdo:IPPaymentDetails |
| CURRENT_ENGINE_LIMITATION | Нет OR-композиции результатов сравнений внутри for_each |
| REQUIRED_ENGINE_FEATURE | assert: value_of(A) == X OR value_of(B) == Y |

### Корреляция вложенных повторяемых элементов (nested repeated correlation) (34 требований)

Проверка совпадения атрибута вложенного повторяемого элемента с атрибутом родительского повторяемого элемента (AP-роль + IPSubjectName). Данные в XML; движок не поддерживает вложенную корреляцию.

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.027, P.SP.02.MSG.029, P.SP.02.MSG.030, P.SP.02.MSG.031, P.SP.02.MSG.032, P.SP.02.MSG.033... |
| REQ | REQ 16, REQ 17, REQ 18, REQ 19, REQ 20, REQ 3 |
| QName/path | @nameRepresentationKindCode; ccdo:SubjectAddressDetails; csdo:AddressKindCode; csdo:AddressKindCode; ipcdo:UnifiedRegisterRecordsDetails; ipcdo:UnifiedRegisterRecordsDetails; ipcdo:GoodsBaseDetails |
| CURRENT_ENGINE_LIMITATION | Нет семантики "для каждого AP-родителя проверить вложенный IPSubjectName с languageCode=RU" |
| REQUIRED_ENGINE_FEATURE | nested for_each_where с cross-parent correlation |

### Позиционная индексация повторяемых дочерних элементов (ordinal indexing) (25 требований)

Проверка значения второго (N-го) экземпляра повторяемого дочернего элемента. Данные в XML; движок не поддерживает позиционный доступ к N-му экземпляру.

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.012, P.SP.02.MSG.037, P.SP.02.MSG.039, P.SP.02.MSG.043, P.SP.02.MSG.045 |
| REQ | REQ 16, REQ 17, REQ 18, REQ 19, REQ 20 |
| QName/path | @nameRepresentationKindCode; csdo:AddressKindCode; ipcdo:TrademarkApplicationDetails; ipsdo:IPSubjectName |
| CURRENT_ENGINE_LIMITATION | Нет ordinal/positional indexing: item[N] для повторяемых дочерних |
| REQUIRED_ENGINE_FEATURE | nth_instance(element, N) или skip_first / second_instance семантика |

### Условная кросс-коллекционная корреляция (cross-collection conditional) (26 требований)

Условное правило, зависящее от значения поля в одной коллекции и применяемое к другой коллекции (например, количество GoodsBaseDetails зависит от TrademarkRegistrationCode). Данные в XML; движок не поддерживает cross-collection conditions.

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.031, P.SP.02.MSG.038, P.SP.02.MSG.045, P.SP.02.MSG.047, P.SP.02.MSG.048, P.SP.02.MSG.049... |
| REQ | REQ 16, REQ 17, REQ 18, REQ 19, REQ 20, REQ 26, REQ 30 |
| QName/path | @nameRepresentationKindCode; ccdo:CommunicationDetails; csdo:AddressKindCode; ipcdo:UnifiedRegisterRecordsDetails; ipsdo:CollectiveMarkIndicator |
| CURRENT_ENGINE_LIMITATION | Нет семантики: if collection_A.field = X then assert collection_B.count >= N |
| REQUIRED_ENGINE_FEATURE | cross_collection_conditional_cardinality(source, predicate, target, cardinality) |


## AMBIGUOUS_NORMATIVE_QUESTIONS

Конкретные вопросы для нормативного уточнения.
Без ответа на эти вопросы реализация невозможна (риск ложных срабатываний).

### Вопрос 1: P.SP.02.MSG.012 – P.SP.02.MSG.062 (22 сообщения) — REQ 13

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.012 – P.SP.02.MSG.062 (22 сообщения) |
| REQ | REQ 13 |
| Source | Table 44 / Table 34 / таблицы 45–81 ОП_22 |
| QName/path | `ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode` |
| Interpretation A | REQ 13 означает, что В ЛЮБОМ экземпляре ipcdo:IPPartyDetails значение ipsdo:IPPartyKindCode ДОЛЖНО равняться «AP» (глобальное ограничение) |
| Interpretation B | REQ 13 означает, что ХОТЯ БЫ ОДИН экземпляр ipcdo:IPPartyDetails должен иметь IPPartyKindCode=«AP» (требование наличия роли «заявитель»), при этом другие экземпляры (PA, RE, LA) допустимы |
| **Exact question** | Следует ли REQ 13 понимать как «все IPPartyDetails должны иметь IPPartyKindCode=AP» или как «должен существовать хотя бы один IPPartyDetails с IPPartyKindCode=AP»? Если второе — каков допустимый набор прочих ролей в одном документе? |

### Вопрос 2: P.SP.02.MSG.059 — REQ 5 (Tables 78 и 79)

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.059 |
| REQ | REQ 5 (Tables 78 и 79) |
| Source | Таблицы 78, 79 ОП_22 (R.IP.SP.02.002 и R.IP.SP.02.007) |
| QName/path | `R.IP.SP.02.002 (полная структура), R.IP.SP.02.007` |
| Interpretation A | «Другие реквизиты не заполняются» означает, что ВСЕ элементы структуры R.IP.SP.02.002/007, не упомянутые в таблице, должны отсутствовать или быть пустыми (строгое exclusion) |
| Interpretation B | «Другие реквизиты не заполняются» означает только рекомендацию не заполнять опциональные поля, не является валидируемым ограничением |
| **Exact question** | Какие конкретно XML-элементы попадают под «другие реквизиты»? Является ли это правило валидируемым (должно быть проверено движком) или только документационным? Если валидируемым — требуется исчерпывающий список допустимых/запрещённых элементов. |


## SOURCE_CONFLICT_ANALYSIS

Детальный анализ противоречий между источниками.
Победитель не выбирается — требуется авторитетное разрешение.

### P.SP.02.MSG.027 — REQ 27

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.027 |
| REQ | REQ 27 |
| QName/path | `ipsdo:TrademarkPictureName / ipcdo:TrademarkDetails/ipcdo:TrademarkColourName` |
| Source A | Table 57 ОП_22 (таблица правил MSG.027): QName для изображения — одно значение |
| Source B | R.IP.SP.02.002 XSD: TrademarkPicture и TrademarkColourName находятся в ipcdo:TrademarkDetails, путь к ним не совпадает с указанным в таблице |
| Exact contradiction | Table 57 REQ 27 использует QName для поля изображения, который не совпадает с фактическим расположением ipcdo:TrademarkColourName в структуре R.IP.SP.02.002 |
| Authoritative resolution needed | Авторитетное подтверждение: какой QName и путь нормативно корректен для поля «цветовое наименование ТЗ» в R.IP.SP.02.002 — из таблицы ОП_22 или из XSD? |

### P.SP.02.MSG.029 — SOURCE_CONFLICT / REQ 32

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.029 |
| REQ | SOURCE_CONFLICT / REQ 32 |
| QName/path | `ipsdo:InconsistencyText внутри ipcdo:GoodsBaseDetails` |
| Source A | Table 45 ОП_22 REQ 32: ipsdo:InconsistencyText назначен выбранному экземпляру ipcdo:GoodsBaseDetails |
| Source B | R.IP.SP.02.002 XSD/StructureDefinition: ipsdo:InconsistencyText не является дочерним элементом ipcdo:GoodsBaseDetails в структуре |
| Exact contradiction | Table 45 предписывает заполнять ipsdo:InconsistencyText внутри GoodsBaseDetails, тогда как XSD/StructureDefinition не определяет такого дочернего пути |
| Authoritative resolution needed | Подтверждение: допускает ли актуальная XSD R.IP.SP.02.002 элемент ipsdo:InconsistencyText как дочерний для ipcdo:GoodsBaseDetails? Если нет — исправление таблицы ОП_22. |

### P.SP.02.MSG.031 — REQ 2

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.031 |
| REQ | REQ 2 |
| QName/path | `ipsdo:TrademarkId / ipcdo:TrademarkApplicationDetails` |
| Source A | Table 48 ОП_22 REQ 2: прямой ipsdo:TrademarkId под TrademarkApplicationDetails |
| Source B | R.IP.SP.02.002 XSD: прямой дочерний ipsdo:TrademarkId под TrademarkApplicationDetails в структуре отсутствует |
| Exact contradiction | Table 48 именует прямой TrademarkId, которого нет как прямого дочернего элемента TrademarkApplicationDetails в XSD |
| Authoritative resolution needed | Актуальная XSD должна подтвердить или опровергнуть наличие прямого ipsdo:TrademarkId под ipcdo:TrademarkApplicationDetails. |

### P.SP.02.MSG.031 — REQ 30

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.031 |
| REQ | REQ 30 |
| QName/path | `ipsdo:InconsistencyText внутри ipcdo:GoodsBaseDetails` |
| Source A | Table 48 ОП_22 REQ 30: ipsdo:InconsistencyText назначается GoodsBaseDetails |
| Source B | R.IP.SP.02.002 XSD/StructureDefinition: ipsdo:InconsistencyText отсутствует как дочерний для GoodsBaseDetails |
| Exact contradiction | Аналогично MSG.029 REQ 32: Table 48 предписывает GoodsBaseDetails/ipsdo:InconsistencyText, что не подтверждается XSD. |
| Authoritative resolution needed | Та же что и для MSG.029 REQ 32 — подтверждение актуальной XSD. |

### P.SP.02.MSG.031 — REQ 32

| Поле | Значение |
| :--- | :--- |
| MSG | P.SP.02.MSG.031 |
| REQ | REQ 32 |
| QName/path | `ipsdo:DecisionOnComplaintText под ipcdo:TrademarkApplicationDetails` |
| Source A | Table 48 ОП_22 REQ 32: запрещает прямой ipsdo:DecisionOnComplaintText под TrademarkApplicationDetails |
| Source B | R.IP.SP.02.002 XSD/StructureDefinition: ipsdo:DecisionOnComplaintText присутствует по этому пути в структуре |
| Exact contradiction | Table 48 явно запрещает элемент, который XSD допускает как валидный |
| Authoritative resolution needed | Должна ли валидация запрещать этот элемент (следуя Table 48) или допускать (следуя XSD)? |
