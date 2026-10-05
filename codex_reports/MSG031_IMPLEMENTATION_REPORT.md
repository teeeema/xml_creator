# MSG031 IMPLEMENTATION REPORT

STATUS = COMPLETE
VERDICT = READY

# ROOT_CAUSE

P.SP.02.MSG.031 had a declarative capture of 38 Table47/48/49 rows but no executable structured_rules. The normative model is R.010 with an exact ONE_OF between R.IP.SP.02.002 and R.IP.SP.02.007. Expanding Table48 REQ6-29 through original Table44 produces 61 normative requirements. The implementation therefore required branch-scoped executable rules, exact QName/owner verification, preservation of external/engine/source-conflict remainders, and reuse of the existing production ONE_OF mechanism.

# CHANGED_FILES

- P.SP.02_OP_22/message_rules/P.SP.02.MSG.031.yaml — Added 54 branch-scoped structured rule objects and complete 61-row mapping_audit.
- P.SP.02_OP_22/tests/test_msg031_safe_mapping.py — Normative classification, provenance, owner/QName, source-conflict, OR-semantics, and rule-identity tests.
- P.SP.02_OP_22/tests/test_msg031_repeatable_xml.py — Production-XML repeatable ownership, nested repeatables, QName collision, optional-branch, and same-parent signature tests.
- P.SP.02_OP_22/tests/test_msg031_rule_execution.py — Independent negative proof for every executable Table48/Table49 requirement code.
- P.SP.02_OP_22/tests/test_msg031_end_to_end.py — Two valid branch E2E pipelines, ONE_OF matrix, transaction context, branch isolation, and same-R010 MSG003/MSG031 isolation.
- codex_reports/MSG031_IMPLEMENTATION_REPORT.md — This service report; intentionally not staged or committed.

No shared production Python, MSG001-030 mapping/test, or MSG032+ file was changed by this batch.

# MSG031

- Message: P.SP.02.MSG.031 — сведения о регистрации (отказе в регистрации) ТЗ Союза.
- Outer structure verified in PDF/repository: R.010, root QName {urn:EEC:R:GenericEDocDetails:vY.Y.Y}GenericEDocDetails.
- Embedded selection: ONE_OF R.IP.SP.02.002 or R.IP.SP.02.007.
- Transaction context: P.SP.02.TRN.026, P.SP.02.PRC.005, P.SP.02.OPR.015 -> P.SP.02.OPR.016, initiating participant P.SP.02.ACT.001, responding participant P.SP.02.ACT.002, response P.SP.02.MSG.002.
- The task text used label R.IP.SP.02.010 in one place; the normative PDF and repository definition identify the container as R.010. Intentional placeholder versions were not investigated or changed.

# NORMATIVE_BASIS

CONFIRMED — independently reread /Users/tema/Documents/Work/Документы_xml/ОП_22.pdf: Table47 physical p.732, Table48 pp.733-735, Table49 pp.735-741, and original Table44 rows inherited by Table48 REQ6-29. Repository StructureDefinitions were used to verify exact paths/QNames/owners and evaluator capability.

# NORMATIVE_INVENTORY

Expanded requirements: 61.

| Table | REQ | Branch | Classification | Mapping status | Normative text | Provenance |
|---:|---:|---|---|---|---|---|
| 47 | 1 | R.010 | FULLY_MAPPABLE | INFRASTRUCTURE_EXECUTABLE | электронный документ (сведения) «Обобщенная структура электронного документа (сведений)» (R.010) должен включать в себя один экземпляр электронного документа (сведений) «Сведения о заявке, ходатайстве для прохождения процедур регистрации ТЗ Союза» (R.IP.SP.02.002) либо один экземпляр электронного документа (сведений) «Сведения о ТЗ Союза из Единого реестра ТЗ Союза» (R.IP.SP.02.007) | 22OP-RULE-P.SP.02.MSG.031-T47-1 p.732 Table 47 item 1 |
| 48 | 1 | R.IP.SP.02.002 | SAFE_PARTIAL | PARTIAL | реквизит «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) должен быть заполнен. В информационных ресурсах национального патентного ведомства, содержащих сведения о заявках на ТЗ Союза, должна содержаться запись, у которой реквизит «Код статуса» (csdo:StatusCode) равен значению «01» – «новая заявка на ТЗ Союза» или «02» – «заявка на ТЗ Союза изменена», реквизит «Конечная дата и время» (csdo:EndDateTime) не заполнен и в составе которой значение реквизита «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) совпадает со значением реквизита «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) в составе сообщения | 22OP-RULE-P.SP.02.MSG.031-T48-1 p.733 Table 48 item 1 |
| 48 | 2 | R.IP.SP.02.002 | SOURCE_CONFLICT | UNMAPPED | реквизит «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T48-2 p.733 Table 48 item 2 |
| 48 | 3 | R.IP.SP.02.002 | SAFE_PARTIAL | PARTIAL | при включении в классификатор видов документов, сведений и материалов вида документа «Решение об отказе в регистрации товарного знака, знака обслуживания Евразийского экономического союза», реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) должен быть заполнен и должен содержать кодовое обозначение указанного вида документа, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T48-3 p.733 Table 48 item 3 |
| 48 | 4 | R.IP.SP.02.002 | SAFE_PARTIAL | PARTIAL | при отсутствии в классификаторе видов документов, сведений и материалов вида документа «Решение об отказе в регистрации товарного знака, знака обслуживания Евразийского экономического союза», реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) не заполняется, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) должен быть заполнен, и его значение должно быть «Решение об отказе в регистрации товарного знака, знака обслуживания Евразийского экономического союза» | 22OP-RULE-P.SP.02.MSG.031-T48-4 p.733 Table 48 item 4 |
| 48 | 5 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Сведения о статусном состоянии» (ipcdo:IPEntityStatusDetails) реквизит «Дата» (csdo:EventDate) должен быть заполнен, значение реквизита «Код статуса» (csdo:StatusCode) должно соответствовать значению «20» – «отказ в регистрации ТЗ Союза», а атрибут «идентификатор справочника (классификатора)» (атрибут codeListId) в составе реквизита «Код статуса» (csdo:StatusCode) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T48-5 p.734 Table 48 item 5 |
| 48 | 6 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | реквизит «Дата подачи заявки (ходатайства)» (ipsdo:ApplicationReceiptDate) должен быть заполнен в соответствии с ISO 8601 | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-6 p.715 Table 44 item 6 |
| 48 | 7 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | если реквизит «Код страны» (csdo:UnifiedCountryCode) заполнен в составе любых реквизитов, то значение атрибута «идентификатор справочника (классификатора)» (атрибут codeListId) в его составе должно соответствовать значению «ВОИС ST.3» | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-7 p.715 Table 44 item 7 |
| 48 | 8 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | если реквизит «Адрес» (ccdo:SubjectAddressDetails) заполнен в составе любых реквизитов, то должны быть заполнены реквизиты «Код вида адреса» (csdo:AddressKindCode)», «Код страны» (csdo:UnifiedCountryCode), «Город» (csdo:CityName), «Улица» (csdo:StreetName) и «Номер дома» (csdo:BuildingNumberId) в его составе | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-8 p.715 Table 44 item 8 |
| 48 | 9 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) заполнен в составе любых реквизитов, то в его составе заполняются реквизиты «Код вида связи» (csdo:CommunicationChannelCode) и «Идентификатор канала связи» (csdo:CommunicationChannelId), а реквизит «Наименование вида связи» (csdo:CommunicationChannelName) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-9 p.716 Table 44 item 9 |
| 48 | 10 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) заполнен в составе любых реквизитов, то в его составе значение реквизита «Код вида связи» (csdo:CommunicationChannelCode) должно соответствовать одному из следующих значений: «TE», «EM» или «FX», в соответствии с перечнем видов средств (каналов) связи, утвержденным Решением Коллегии Комиссии от 6 декабря 2022 г. № 192 | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-10 p.716 Table 44 item 10 |
| 48 | 11 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Национальное патентное ведомство» (ipcdo:PatentAuthorityDetails) должен быть заполнен реквизит «Код страны» (csdo:UnifiedCountryCode) | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-11 p.716 Table 44 item 11 |
| 48 | 12 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Национальное патентное ведомство» (ipcdo:PatentAuthorityDetails) должен быть заполнен реквизит «Наименование уполномоченного органа» (csdo:AuthorityName) и должен быть заполнен реквизит «Адрес» (ccdo:SubjectAddressDetails), в составе которого значение реквизита «Код вида адреса» (csdo:AddressKindCode) должно соответствовать значению «2» – «фактический адрес (адрес места нахождения или места жительства)» | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-12 p.716 Table 44 item 12 |
| 48 | 13 | R.IP.SP.02.002 | AMBIGUOUS | UNMAPPED | значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) должно соответствовать значению «AP» – «заявитель» | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-13 p.716 Table 44 item 13 |
| 48 | 14 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | в электронном документе (сведениях) «Сведения о заявке, ходатайстве для прохождения процедур регистрации ТЗ Союза» (R.IP.SP.02.002) должен быть заполнен 1 экземпляр реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), в составе которого значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель» | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-14 p.716 Table 44 item 14 |
| 48 | 15 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должны быть заполнены реквизиты: «Код страны» (csdo:UnifiedCountryCode); «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName); «Адрес» (ccdo:SubjectAddressDetails); «Контактный реквизит» (ccdo:CommunicationDetails) | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-15 p.717 Table 44 item 15 |
| 48 | 16 | R.IP.SP.02.002 | ENGINE_UNSUPPORTED | UNMAPPED | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то значение атрибута «код вида представления наименования» (атрибут nameRepresentationKindCode) в составе реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName) должно соответствовать одному из следующих значений: «OR» – «сведения, представленные на исходном (оригинальном) языке»; «LA» – «транслитерация сведений на исходном (оригинальном) языке буквами латинского алфавита» | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-16 p.717 Table 44 item 16 |
| 48 | 17 | R.IP.SP.02.002 | ENGINE_UNSUPPORTED | UNMAPPED | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должен быть заполнен 1 экземпляр реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName), в составе которого значение атрибута «код вида представления наименования» (атрибут nameRepresentationKindCode) должно соответствовать значению «OR» – «сведения, представленные на исходном (оригинальном) языке» и атрибут «код языка» (атрибут languageCode) должен быть заполнен | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-17 p.717 Table 44 item 17 |
| 48 | 18 | R.IP.SP.02.002 | ENGINE_UNSUPPORTED | UNMAPPED | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель» и, если в составе реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName) значение атрибута «код языка» (атрибут languageCode) соответствует значению «RU», второй экземпляр реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-18 p.718 Table 44 item 18 |
| 48 | 19 | R.IP.SP.02.002 | ENGINE_UNSUPPORTED | UNMAPPED | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель» и если в составе реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName) значение атрибута «код языка» (атрибут languageCode) не соответствует значению «RU», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должен быть заполнен второй экземпляр реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName), в составе которого значение атрибута «код вида представления наименования» (атрибут nameRepresentationKindCode) должно соответствововать значению «LA» – «транслитерация сведений на исходном (оригинальном) языке буквами латинского алфавита» и атрибут «код языка» (атрибут languageCode) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-19 p.718 Table 44 item 19 |
| 48 | 20 | R.IP.SP.02.002 | ENGINE_UNSUPPORTED | UNMAPPED | если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) в составе реквизита «Адрес» (ccdo:SubjectAddressDetails) значение реквизита «Код вида адреса» (csdo:AddressKindCode) должно соответствовать значению «2» – «фактический адрес (адрес места нахождения или места жительства)» | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-20 p.718 Table 44 item 20 |
| 48 | 21 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | если в состав электронного документа (сведений) включен экземпляр реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), в составе которого значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «PA» – «представитель заявителя, являющийся патентным поверенным», то в составе такого экземпляра реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должны быть заполнены реквизиты: «Код страны» (csdo:UnifiedCountryCode); «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName); «Адрес» (ccdo:SubjectAddressDetails); «Контактный реквизит» (ccdo:CommunicationDetails); «Регистрационный номер патентного поверенного» (ipsdo:PatentAttorneyId) | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-21 p.719 Table 44 item 21 |
| 48 | 22 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | если в состав электронного документа (сведений) включен экземпляр реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), в составе которого значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «RE» – «представитель заявителя, не являющийся патентным поверенным», то в составе такого экземпляра реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должны быть заполнены реквизиты: «Код страны» (csdo:UnifiedCountryCode); «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName); «Адрес» (ccdo:SubjectAddressDetails); «Контактный реквизит» (ccdo:CommunicationDetails) | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-22 p.719 Table 44 item 22 |
| 48 | 23 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Адрес для переписки» (ipcdo:CorrespondenceAddressDetails) в составе реквизита «Адрес» (ccdo:SubjectAddressDetails) значение реквизита «Код вида адреса» (csdo:AddressKindCode) должно соответствовать значению «3» – «почтовый адрес (адрес для ведения переписки)» | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-23 p.719 Table 44 item 23 |
| 48 | 24 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Адрес для переписки» (ipcdo:CorrespondenceAddressDetails) в составе реквизита «Адрес» (ccdo:SubjectAddressDetails) значение реквизита «Код страны» (csdo:UnifiedCountryCode) должно соответствовать одному из следующих значений: «AM», «BY», «KZ», «KG» или «RU» | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-24 p.720 Table 44 item 24 |
| 48 | 25 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails) реквизит «Товарный знак Союза» (ipcdo:TrademarkDetails) должен быть заполнен, и в его составе должны быть заполнены реквизиты: «Описание товарного знака Союза» (ipcdo:TMDescriptionDetails); «Код вида товарного знака» (ipsdo:TrademarkKindCode); «Наименование вида товарного знака» (ipsdo:TrademarkKindName); «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-25 p.720 Table 44 item 25 |
| 48 | 26 | R.IP.SP.02.002 | ENGINE_UNSUPPORTED | UNMAPPED | в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails), в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида товарного знака» (ipsdo:TrademarkKindCode) или реквизита «Наименование вида товарного знака» (ipsdo:TrademarkKindName) должны соответствовать одному из следующих значений: «110» – «Словесный знак»; «120» – «Буквенный знак»; «130» – «Цифровой знак»; «140» – «Изобразительный знак»; «150» – «Объемный знак»; «160» – «Знак, представляющий собой цвет»; «170» – «Знак, представляющий собой сочетание цветов»; «180» – «Комбинированный знак» в соответствии со справочником основных характеристик товарного знака и знака обслуживания Евразийского экономического союза (по виду и приоритету), утвержденным Решением Коллегии Комиссии от 29 ноября 2022 г. № 184 | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-26 p.720 Table 44 item 26 |
| 48 | 27 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида товарного знака» (ipsdo:TrademarkKindCode) или реквизита «Наименование вида товарного знака» (ipsdo:TrademarkKindName) соответствует одному из приведённых значений: «140» – «Изобразительный знак»; «150» – «Объемный знак»; «160» – «Знак, представляющий собой цвет»; «170» – «Знак, представляющий собой сочетание цветов»; «180» – «Комбинированный знак», то реквизит «Изображение товарного знака» (ipsdo:TrademarkPicture) и реквизит «Описание цвета товарного знака» (ipsdo:TrademarkColourName) должны быть заполнены | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-27 p.721 Table 44 item 27 |
| 48 | 28 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | значение реквизита «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) должно соответствовать одному из следующих значений: «1» – «товарный знак является коллективным»; «0» – «товарный знак не является коллективным» | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-28 p.721 Table 44 item 28 |
| 48 | 29 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails) реквизит «Товар в соответствии с МКТУ» (ipcdo:GoodsBaseDetails) должен быть заполнен, и в его составе должны быть заполнены реквизиты: «Номер класса МКТУ» (ipsdo:GoodsClassCode); «Наименование класса МКТУ» (ipsdo:GoodsClassName); «Наименование товара (услуги)» (ipsdo:GoodsName) | 22OP-RULE-P.SP.02.MSG.031-T48-6-29 p.734 Table 48 item 6-29; 22OP-RULE-P.SP.02.MSG.028-T44-29 p.721 Table 44 item 29 |
| 48 | 30 | R.IP.SP.02.002 | SOURCE_CONFLICT | UNMAPPED | в составе реквизита «Товар в соответствии с МКТУ» (ipcdo:GoodsBaseDetails) реквизит «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId), реквизит «Описание основания для отказа в регистрации товарного знака Союза в отношении товара» (ipsdo:TrademarkRegRefusalReasonText), реквизит «Описание несоответствия» (ipsdo:InconsistencyText) должны быть заполнены | 22OP-RULE-P.SP.02.MSG.031-T48-30 p.734 Table 48 item 30 |
| 48 | 31 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | реквизит «Отказ в регистрации объекта интеллектуальной собственности» (ipcdo:RefusalDetails) должен быть заполнен | 22OP-RULE-P.SP.02.MSG.031-T48-31 p.734 Table 48 item 31 |
| 48 | 32 | R.IP.SP.02.002 | SOURCE_CONFLICT | UNMAPPED | в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails) реквизиты: «Национальная заявка на регистрацию товарного знака» (ipcdo:TrademarkNationalApplicationDetails), «Сведения об изменении заявителя» (ipcdo:ApplicantChangeDetails), «Сведения об обращении заинтересованного лица о несоответствии обозначения, заявленного на регистрацию в качестве товарного знака Союза, требованиям Договора о товарных знаках» (ipcdo:TrademarkClaimDetails), «Жалоба» (ipcdo:ComplaintDetails), «Текст решения о рассмотрении возражения заявителя» (ipsdo:DecisionOnComplaintText), «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails) не заполняются | 22OP-RULE-P.SP.02.MSG.031-T48-32 p.734 Table 48 item 32 |
| 48 | 33 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Технологические характеристики записи общего ресурса» (ccdo:ResourceItemStatusDetails) реквизит «Конечная дата и время» (csdo:EndDateTime) заполняется обязательно | 22OP-RULE-P.SP.02.MSG.031-T48-33 p.734 Table 48 item 33 |
| 48 | 34 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | реквизит «Сведения о подписании документа» (ipcdo:SignatureDetails) должен быть заполнен, и в его составе если реквизит «Сотрудник организации» (ipcdo:OfficerDetails) заполнен, то реквизит «ФИО» (ccdo:FullNameDetails), непосредственно подчиненный реквизиту «Сведения о подписании документа» (ipcdo:SignatureDetails), не заполняется | 22OP-RULE-P.SP.02.MSG.031-T48-34 p.735 Table 48 item 34 |
| 48 | 35 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | если в составе реквизита «Сведения о подписании документа» (ipcdo:SignatureDetails) реквизит «ФИО» (ccdo:FullNameDetails), непосредственно подчиненный реквизиту «Сведения о подписании документа» (ipcdo:SignatureDetails), заполнен, то реквизит «Сотрудник организации» (ipcdo:OfficerDetails) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T48-35 p.735 Table 48 item 35 |
| 48 | 36 | R.IP.SP.02.002 | FULLY_MAPPABLE | EXECUTABLE | если в составе реквизита «Сведения о подписании документа» (ipcdo:SignatureDetails) заполнен реквизит «Сотрудник организации» (ipcdo:OfficerDetails), в его составе должны быть заполнены реквизиты «Фамилия» (csdo:LastName), «Имя» (csdo:FirstName) и «Наименование должности» (csdo:PositionName), а реквизит «Контактный реквизит» (ccdo:CommunicationDetails) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T48-36 p.735 Table 48 item 36 |
| 49 | 1 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | реквизиты «Дата регистрации объекта интеллектуальной собственности» (ipsdo:RegistrationDate), «Дата истечения срока действия документа» (csdo:DocValidityDate) должны быть заполнены | 22OP-RULE-P.SP.02.MSG.031-T49-1 p.735 Table 49 item 1 |
| 49 | 2 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | реквизит «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) должен быть заполнен | 22OP-RULE-P.SP.02.MSG.031-T49-2 p.735 Table 49 item 2 |
| 49 | 3 | R.IP.SP.02.007 | SAFE_PARTIAL | PARTIAL | реквизит «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) должен быть заполнен. В информационных ресурсах национального патентного ведомства, содержащих сведения о ТЗ Союза, не должно содержаться записи, в составе которой значение реквизита «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) совпадает со значением реквизита «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) в представляемых сведениях | 22OP-RULE-P.SP.02.MSG.031-T49-3 p.736 Table 49 item 3 |
| 49 | 4 | R.IP.SP.02.007 | SAFE_PARTIAL | PARTIAL | при включении в классификатор видов документов, сведений и материалов значения, соответствующего одному из видов документа, приведённых ниже: «Решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении всех заявленных товаров и (или) услуг»; «Решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении части товаров и (или) услуг», реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) должен быть заполнен и должен содержать кодовое обозначение указанного вида документа, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T49-4 p.736 Table 49 item 4 |
| 49 | 5 | R.IP.SP.02.007 | SAFE_PARTIAL | PARTIAL | при отсутствии в классификаторе видов документов, сведений и материалов значения, соответствующего одному из видов документа, приведённых ниже: «Решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении всех заявленных товаров и (или) услуг»; «Решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении части товаров и (или) услуг», реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) не заполняется, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) должен быть заполнен, и его значение должно соответствовать одному из приведённых ниже: «Решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении всех заявленных товаров и (или) услуг»; «Решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении части товаров и (или) услуг» | 22OP-RULE-P.SP.02.MSG.031-T49-5 p.736 Table 49 item 5 |
| 49 | 6 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | если реквизит «Код страны» (csdo:UnifiedCountryCode) заполнен в составе любых реквизитов, в его составе значение атрибута «идентификатор справочника (классификатора)» (атрибут codeListId) должно соответствовать значению «ВОИС ST.3» | 22OP-RULE-P.SP.02.MSG.031-T49-6 p.737 Table 49 item 6 |
| 49 | 7 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | если реквизит «Адрес» (ccdo:SubjectAddressDetails) заполнен в составе любых реквизитов, в его составе должны быть заполнены реквизиты «Код вида адреса» (csdo:AddressKindCode)», «Код страны» (csdo:UnifiedCountryCode), «Город» (csdo:CityName), «Улица» (csdo:StreetName) и «Номер дома» (csdo:BuildingNumberId) | 22OP-RULE-P.SP.02.MSG.031-T49-7 p.737 Table 49 item 7 |
| 49 | 8 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) заполнен в составе любых реквизитов, в его составе заполняются реквизиты «Код вида связи» (csdo:CommunicationChannelCode) и «Идентификатор канала связи» (csdo:CommunicationChannelId), а реквизит «Наименование вида связи» (csdo:CommunicationChannelName) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T49-8 p.737 Table 49 item 8 |
| 49 | 9 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) заполнен в составе любых реквизитов, в его составе значение реквизита «Код вида связи» (csdo:CommunicationChannelCode) должно соответствовать одному из следующих значений: «TE», «EM» или «FX», в соответствии с перечнем видов средств (каналов) связи, утвержденным Решением Коллегии Комиссии от 6 декабря 2022 г. № 192 | 22OP-RULE-P.SP.02.MSG.031-T49-9 p.737 Table 49 item 9 |
| 49 | 10 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Национальное патентное ведомство» (ipcdo:PatentAuthorityDetails) должны быть заполнены реквизиты: «Код страны» (csdo:UnifiedCountryCode); «Наименование уполномоченного органа» (csdo:AuthorityName); «Краткое наименование уполномоченного органа» (csdo:AuthorityBriefName) | 22OP-RULE-P.SP.02.MSG.031-T49-10 p.737 Table 49 item 10 |
| 49 | 11 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | в электронном документе (сведениях) должен быть заполнен 1 экземпляр реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), в составе которого значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «RH» – «правообладатель» | 22OP-RULE-P.SP.02.MSG.031-T49-11 p.737 Table 49 item 11 |
| 49 | 12 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должны быть заполнены реквизиты: «Код страны» (csdo:UnifiedCountryCode); «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName); «Адрес» (ccdo:SubjectAddressDetails); «Контактный реквизит» (ccdo:CommunicationDetails) | 22OP-RULE-P.SP.02.MSG.031-T49-12 p.738 Table 49 item 12 |
| 49 | 13 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) в составе реквизита «Адрес» (ccdo:SubjectAddressDetails) значение реквизита «Код вида адреса» (csdo:AddressKindCode) должно соответствовать значению «2» – «фактический адрес (адрес места нахождения или места жительства)» | 22OP-RULE-P.SP.02.MSG.031-T49-13 p.738 Table 49 item 13 |
| 49 | 14 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) должны быть заполнены следующие реквизиты: «Изображение товарного знака» (ipsdo:TrademarkPicture); «Описание товарного знака Союза» (ipcdo:TMDescriptionDetails); «Наименование вида товарного знака» (ipsdo:TrademarkKindName); «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) | 22OP-RULE-P.SP.02.MSG.031-T49-14 p.738 Table 49 item 14 |
| 49 | 15 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Описание товарного знака Союза» (ipcdo:TMDescriptionDetails) должны быть заполнены следующие реквизиты: «Описание» (csdo:DescriptionText); «Описание элемента товарного знака Союза» (ipcdo:TMElementDetails), в составе которого должны быть заполнены следующие реквизиты: «Код изобразительного элемента товарного знака» (ipsdo:TrademarkCFECode); «Обозначение» (csdo:DesignationName); «Перевод словесного элемента обозначения» (ipsdo:TMLocalizedName); «Транслитерация словесного элемента обозначения» (ipsdo:TMTransliterationName) | 22OP-RULE-P.SP.02.MSG.031-T49-15 p.738 Table 49 item 15 |
| 49 | 16 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | реквизит «Товар в соответствии с МКТУ» (ipcdo:GoodsBaseDetails) должен быть заполнен, и в его составе должны быть заполнены реквизиты: «Номер класса МКТУ» (ipsdo:GoodsClassCode); «Наименование класса МКТУ» (ipsdo:GoodsClassName); «Наименование товара (услуги)» (ipsdo:GoodsName); «Признак возможности регистрации товарного знака Союза» (ipsdo:TrademarkDecisionIndicator); «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) | 22OP-RULE-P.SP.02.MSG.031-T49-16 p.739 Table 49 item 16 |
| 49 | 17 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Товар в соответствии с МКТУ» (ipcdo:GoodsBaseDetails) реквизиты: «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId); «Регистрационный номер НМПТ Союза» (ipsdo:ApellationOfOriginEAEUId); «Описание основания для отказа в регистрации товарного знака Союза в отношении товара» (ipsdo:TrademarkRegRefusalReasonText) не заполняются | 22OP-RULE-P.SP.02.MSG.031-T49-17 p.739 Table 49 item 17 |
| 49 | 18 | R.IP.SP.02.007 | ENGINE_UNSUPPORTED | UNMAPPED | если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) соответствует значению «1» – «товарный знак является коллективным», то должен быть заполнен хотя бы 1 экземпляр реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), в составе которого значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «UE» – «лицо, имеющее право использования коллективного знака Союза» | 22OP-RULE-P.SP.02.MSG.031-T49-18 p.739 Table 49 item 18 |
| 49 | 19 | R.IP.SP.02.007 | ENGINE_UNSUPPORTED | UNMAPPED | если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) соответствует значению «1» – «товарный знак является коллективным», то должен быть заполнен экземпляр реквизита «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails) в составе которого должен быть заполнен один из реквизитов «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) или «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) и их значения должны соответствовать коду или наименованию вида документа «Устав (положение) коллективного знака Евразийского экономического союза, содержащий наименование лица, уполномоченного на регистрацию коллективного знака Союза на свое имя, цель регистрации коллективного знака Союза, перечень субъектов, имеющих право на использование коллективного знака Союза, перечень и единые качественные или иные общие характеристики товаров, которые будут обозначаться коллективным знаком Союза, условия его использования, положения о порядке контроля за его использованием, положения об ответственности за нарушение его требований» | 22OP-RULE-P.SP.02.MSG.031-T49-19 p.740 Table 49 item 19 |
| 49 | 20 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Сведения о статусном состоянии» (ipcdo:IPEntityStatusDetails) реквизит «Дата» (csdo:EventDate) должен быть заполнен, значение реквизита «Код статуса» (csdo:StatusCode) должно соответствовать значению «01» – «ТЗ Союза зарегистрирован», а атрибут «идентификатор справочника (классификатора)» (атрибут codeListId) в составе реквизита «Код статуса» (csdo:StatusCode) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T49-20 p.740 Table 49 item 20 |
| 49 | 21 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | в составе реквизита «Технологические характеристики записи общего ресурса» (ccdo:ResourceItemStatusDetails) реквизит «Начальная дата и время» (csdo:StartDateTime) заполняется обязательно | 22OP-RULE-P.SP.02.MSG.031-T49-21 p.740 Table 49 item 21 |
| 49 | 22 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | реквизит «Сведения о подписании документа» (ipcdo:SignatureDetails) должен быть заполнен, и в его составе если реквизит «Сотрудник организации» (ipcdo:OfficerDetails) заполнен, то реквизит «ФИО» (ccdo:FullNameDetails), непосредственно подчиненный реквизиту «Сведения о подписании документа» (ipcdo:SignatureDetails), не заполняется | 22OP-RULE-P.SP.02.MSG.031-T49-22 p.740 Table 49 item 22 |
| 49 | 23 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | если в составе реквизита «Сведения о подписании документа» (ipcdo:SignatureDetails) реквизит «ФИО» (ccdo:FullNameDetails), непосредственно подчиненный реквизиту «Сведения о подписании документа» (ipcdo:SignatureDetails), заполнен, то реквизит «Сотрудник организации» (ipcdo:OfficerDetails) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T49-23 p.740 Table 49 item 23 |
| 49 | 24 | R.IP.SP.02.007 | FULLY_MAPPABLE | EXECUTABLE | если в составе реквизита «Сведения о подписании документа» (ipcdo:SignatureDetails) заполнен реквизит «Сотрудник организации» (ipcdo:OfficerDetails), в его составе должны быть заполнены реквизиты «Фамилия» (csdo:LastName), «Имя» (csdo:FirstName) и «Наименование должности» (csdo:PositionName), а реквизит «Контактный реквизит» (ccdo:CommunicationDetails) не заполняется | 22OP-RULE-P.SP.02.MSG.031-T49-24 p.741 Table 49 item 24 |

# TABLE47_R010

Table47 REQ1 requires R.010 to contain one instance of R.IP.SP.02.002 OR one instance of R.IP.SP.02.007. This is executed by existing embedded ONE_OF infrastructure. No fake pair of optional presence rules and no synthetic T47 structured rule were added.

# TABLE48_R002

R002 root: {urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails. Table48 has 29 structured-rule objects covering 26 executable requirement codes; inherited executable REQ6-29 rows carry dual Table48 + original Table44 provenance.

# TABLE49_R007

R007 root: {urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}TrademarkRegisterDetails. Table49 has 25 structured-rule objects covering 22 executable requirement codes.

# FULL_MAPPED

Fully mappable requirements: 43, including Table47 infrastructure-executable REQ1.
- Table47: 1.
- Table48: 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 31, 33, 34, 35, 36.
- Table49: 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24.

# PARTIAL_MAPPED

SAFE_PARTIAL requirements: 6.
- Table48 REQ1: TrademarkApplicationId is required. Remainder: external StatusCode in {01,02}, external EndDateTime absent, external TrademarkApplicationId equality. External dependency: national patent office information resource.
- Table48 REQ3: If direct IPDocKindCode is present, direct IPDocKindName is forbidden. Remainder: authoritative classifier-presence predicate, authoritative classifier code designation, required code when external branch applies. External dependency: classifier of document/material kinds.
- Table48 REQ4: If direct IPDocKindCode is absent, direct IPDocKindName equals: Решение об отказе в регистрации товарного знака, знака обслуживания Евразийского экономического союза Remainder: authoritative classifier-absence predicate. External dependency: classifier of document/material kinds.
- Table49 REQ3: TrademarkId is required. Remainder: external uniqueness/nonexistence lookup. External dependency: national patent office information resource.
- Table49 REQ4: If direct IPDocKindCode is present, direct IPDocKindName is forbidden. Remainder: authoritative classifier-presence predicate, authoritative classifier code designation, required code when external branch applies. External dependency: classifier of document/material kinds.
- Table49 REQ5: If direct IPDocKindCode is absent, direct IPDocKindName is required. Remainder: authoritative classifier-absence predicate, conditional membership in the two exact normative fallback names. External dependency: classifier of document/material kinds.

# UNMAPPED

Unmapped requirements: 12.
- Table48 REQ2 — SOURCE_CONFLICT: Table48 REQ2 names a direct TrademarkId, but R.IP.SP.02.002 has no exact direct TrademarkApplicationDetails/ipsdo:TrademarkId; TrademarkId exists under GoodsBaseDetails and must not be substituted.
- Table48 REQ13 — AMBIGUOUS: Original Table44 REQ13 states IPPartyKindCode=AP without an unambiguous repeated-owner/instance scope; global enforcement would conflict with PA/RE roles.
- Table48 REQ16 — ENGINE_UNSUPPORTED: Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values that the current evaluator cannot express exactly.
- Table48 REQ17 — ENGINE_UNSUPPORTED: Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values that the current evaluator cannot express exactly.
- Table48 REQ18 — ENGINE_UNSUPPORTED: Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values that the current evaluator cannot express exactly.
- Table48 REQ19 — ENGINE_UNSUPPORTED: Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values that the current evaluator cannot express exactly.
- Table48 REQ20 — ENGINE_UNSUPPORTED: Original Table44 requirement needs AP-scoped correlation/cardinality across nested repeated values that the current evaluator cannot express exactly.
- Table48 REQ26 — ENGINE_UNSUPPORTED: Original Table44 REQ26 is explicitly TrademarkKindCode OR TrademarkKindName matching an allowed kind; the evaluator cannot express the per-TrademarkDetails disjunction without strengthening OR to AND.
- Table48 REQ30 — SOURCE_CONFLICT: Table48 REQ30 assigns InconsistencyText to GoodsBaseDetails, while the StructureDefinition places ipsdo:InconsistencyText directly under TrademarkApplicationDetails.
- Table48 REQ32 — SOURCE_CONFLICT: Table48 REQ32 forbids direct ipsdo:DecisionOnComplaintText under TrademarkApplicationDetails, but that exact path/QName is absent from the StructureDefinition.
- Table49 REQ18 — ENGINE_UNSUPPORTED: Requires a conditional cross-collection existence check from TrademarkDetails.CollectiveMarkIndicator=1 to a UE IPPartyDetails instance.
- Table49 REQ19 — ENGINE_UNSUPPORTED: Requires a conditional cross-collection AccompanyingDocumentsDetails existence check plus exact per-document IPDocKindCode OR IPDocKindName value semantics.

# R010_ONE_OF

Production tests prove R002 only PASS; R007 only PASS; neither FAIL with EMBEDDED_STRUCTURE_CARDINALITY; both FAIL with EMBEDDED_STRUCTURE_CARDINALITY; right local name with wrong R002 namespace is rejected; right local name with wrong R007 namespace is rejected. Selected-branch evaluations contain only the selected Table48 or Table49 rule IDs.

# R002_REQ1_5

- REQ1 SAFE_PARTIAL: local TrademarkApplicationId presence executable; national-resource status/end/id correspondence remains external.
- REQ2 SOURCE_CONFLICT: no direct TrademarkApplicationDetails/ipsdo:TrademarkId; Goods-owned TrademarkId was not substituted.
- REQ3 SAFE_PARTIAL: if direct code exists, direct name forbidden; authoritative classifier membership/code remains external.
- REQ4 SAFE_PARTIAL: if code is absent, exact refusal-decision fallback name enforced; authoritative classifier absence remains external.
- REQ5 FULL: IPEntityStatusDetails EventDate required, StatusCode=20, StatusCode/@codeListId forbidden.

# R002_REQ6_12

FULL. ApplicationReceiptDate; under-application country-code list ID; each existing address required children; each existing communication required/forbidden children; channel TE/EM/FX; exact PatentAuthority country/authority/address-kind semantics.

# R002_REQ13

AMBIGUOUS and unmapped. Original Table44 gives IPPartyKindCode=AP without unambiguous repeated-owner instance scope. Global enforcement would conflict with explicit PA/RE roles.

# R002_REQ14_15

FULL. Exactly one semantic AP party selected by IPPartyKindCode=AP; required AP children are evaluated only inside that selected AP parent.

# R002_REQ16_20

ENGINE_UNSUPPORTED. These rows require AP-scoped correlation/cardinality across nested repeated IPSubjectName/address representation/language data that the current evaluator cannot express exactly. No approximation was added.

# R002_REQ21_25

FULL. PA and RE are role-filtered; correspondence address rules use exact optional owner; TrademarkDetails cardinality and required children are enforced.

# R002_REQ26_NORMATIVE_RECHECK

Original Table44 REQ26 was independently reread and is OR semantics: TrademarkKindCode OR TrademarkKindName must identify an allowed kind within the same TrademarkDetails. The evaluator cannot produce that exact per-parent OR-of-comparisons result without semantic strengthening. REQ26 remains ENGINE_UNSUPPORTED/unmapped. OR was not converted to AND.

# R002_REQ27_NORMATIVE_RECHECK

FULL. Within the same TrademarkDetails, if TrademarkKindCode OR TrademarkKindName denotes a visual kind, TrademarkPicture and TrademarkColourName are both required. condition.any remains scoped to that same parent.

# R002_REQ28_29

FULL. CollectiveMarkIndicator is limited to 1/0. GoodsBaseDetails must exist and each Goods parent requires exact ipsdo:GoodsClassCode, ipsdo:GoodsClassName, ipsdo:GoodsName. Production XML proves good+good PASS, good+bad FAIL, bad+good FAIL.

# R002_REQ30

SOURCE_CONFLICT and unmapped. Table48 assigns ipsdo:InconsistencyText to GoodsBaseDetails, while R.IP.SP.02.002 places the exact QName at ipcdo:TrademarkApplicationDetails/ipsdo:InconsistencyText, source field 2.13 p.876. Application-owned field was not substituted.

# R002_REQ31

FULL. Root ipcdo:RefusalDetails is required exactly once.

# R002_REQ32

SOURCE_CONFLICT and unmapped. Table48 includes direct ipsdo:DecisionOnComplaintText under TrademarkApplicationDetails, but that exact path/QName is absent from R002 StructureDefinition. Similar complaint/decree text fields under other owners were not substituted.

# R002_REQ33_36

FULL. Resource EndDateTime required; SignatureDetails required; Officer/direct FullName mutual exclusion is same-Signature; Officer exact owner is ipcdo:OfficerDetails and requires LastName, FirstName, PositionName while forbidding Officer CommunicationDetails.

# R007_REQ1_5

- REQ1-2 FULL: RegistrationDate+DocValidityDate and TrademarkApplicationId required.
- REQ3 SAFE_PARTIAL: local TrademarkId required; external uniqueness/nonexistence lookup remains external.
- REQ4 SAFE_PARTIAL: code-present branch safely forbids direct name; classifier membership/code is external.
- REQ5 SAFE_PARTIAL: code-absent branch safely requires direct name. Exact two-literal fallback membership and authoritative classifier absence remain unmapped because current evaluator has no conditional-IN assertion.

# R007_REQ6_17

FULL. Country code list IDs, addresses, communications, PatentAuthority, exactly one RH party, every-party required children/address-kind, TrademarkDetails, nested TMDescription/TMElement children, Goods cardinality/required children including exact ipsdo:GoodsClassCode, and forbidden Goods identifiers/reason text. Nested TMElement and Goods repeatables have production-XML order proofs.

# R007_REQ18_19

ENGINE_UNSUPPORTED and unmapped. REQ18 needs conditional cross-collection UE-party existence. REQ19 needs conditional cross-collection document existence plus exact per-document IPDocKindCode OR IPDocKindName matching. No approximation or OR-to-AND strengthening was introduced.

# R007_REQ20_24

FULL. IPEntityStatusDetails EventDate/StatusCode=01/codeListId-forbidden; Resource StartDateTime; required SignatureDetails; same-signature Officer/direct FullName mutual exclusion; exact Officer required/forbidden children.

# BRANCH_ISOLATION

All 54 structured-rule objects carry applies_to_structure. Table48 applies only to R.IP.SP.02.002; Table49 only to R.IP.SP.02.007. R002 E2E evaluates 29 T48 objects and zero T49; R007 E2E evaluates 25 T49 and zero T48.

# PROVENANCE

Table48 inherited REQ6-29 inventory entries and executable rules carry current Table48 REQ6-29 p.734 plus concrete original Table44 requirement/page/source ID. Direct rows carry direct confirmed source refs. No source_ref was fabricated.

# QNAME_COLLISION

Wrong-namespace R002-like/R007-like embedded roots are not recognized. Wrong-namespace GoodsClassCode does not enter normative extracted values and fails R002 REQ29. Table48 REQ2/30/32 remain source conflicts rather than matching same-local-name fields from another owner.

# REPEATABLE_XML

Production XML covers R002 Goods good+good/good+bad/bad+good, R002 repeatable SignatureDetails same-parent isolation, R007 nested TMElementDetails good+good/good+bad/bad+good, R007 Goods good+good/good+bad/bad+good, and R007 forbidden Goods fields per parent. Positional ownership is preserved; no scalar broadcast or cross-parent leakage was used.

# OPTIONAL_BRANCHES

Rules applying to each existing optional parent remain vacuous when that parent is absent. Tests cover optional R002 PatentAuthority/PA/RE/correspondence branches and optional R007 qname/parent branches. No synthetic existence requirement was added except where normative cardinality explicitly requires one.

# MESSAGE_ISOLATION

R.010 is also used by P.SP.02.MSG.003 and P.SP.02.MSG.059. P.SP.02.MSG.003 has executable rules, so the same embedded R002 payload was validated for MSG031 and MSG003; both produced non-empty disjoint evaluation sets containing only their requested message prefix. MSG031 rule identity is also disjoint from MSG029/MSG030/MSG032. Isolation is not inferred from an empty evaluation set.

# END_TO_END

- Scenario A: MSG031 R.010 + embedded R002: build -> serialize -> parse -> extract -> validate; exact outer/payload QName; extraction issues=0; ONE_OF PASS; 29 selected-branch evaluations PASS.
- Scenario B: MSG031 R.010 + embedded R007: build -> serialize -> parse -> extract -> validate; exact outer/payload QName; extraction issues=0; ONE_OF PASS; 25 selected-branch evaluations PASS.
Independent negative proof exists for every executable Table48 and Table49 requirement code in test_msg031_rule_execution.py; repeatable and QName-sensitive cases additionally use production XML.

# MSG031_TESTS

Final command: pytest -q P.SP.02_OP_22/tests/test_msg031_*.py

Result: 84 passed in 1.57s; 0 failed.
Component confirmations: safe mapping 14 passed; repeatable XML 14 passed; rule execution 48 passed; final end-to-end 8 passed.

# MSG030_REGRESSION

Command: pytest -q P.SP.02_OP_22/tests/test_msg030_*.py

Result: 119 passed in 2.87s; 0 failed.

# MSG029_REGRESSION

Command: pytest -q P.SP.02_OP_22/tests/test_msg029_*.py

Result: 84 passed in 2.03s; 0 failed.

# MSG028_REGRESSION

Command: pytest -q P.SP.02_OP_22/tests/test_msg028_*.py

Result: 113 passed in 3.12s; 0 failed.

# MSG027_REGRESSION

Command: pytest -q P.SP.02_OP_22/tests/test_msg027_*.py

Result: 96 passed in 2.39s; 0 failed.

# MSG020_024_REGRESSION

Command: pytest -q P.SP.02_OP_22/tests/test_msg02[0-4]_*.py

Result: 148 passed in 3.62s; 0 failed.

# PREVIOUS_REGRESSION

Explicit suites: MSG001, MSG003, MSG004, MSG005, MSG006-010, MSG011-014, MSG016-019.
Result: 595 passed in 21.93s; 0 failed.

# SHARED_REGRESSION

Command: pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_embedded_one_of.py eaeu_xml/tests/test_repeatable_xml_alignment.py
Result: 45 passed, 5 subtests passed in 0.17s; 0 failed.

# PSP02_TESTS

Final command after same-R010 isolation test: pytest -q P.SP.02_OP_22/tests
Result: 1252 passed in 37.30s; 0 failed. Baseline 1168 + 84 new MSG031 tests = 1252.

# EAEU_XML_TESTS

Command: pytest -q eaeu_xml/tests
Result: 265 passed, 43 skipped, 1042 subtests passed in 2.39s; 0 failed.

# ROOT_TESTS

Final command after all MSG031 test additions: pytest -q
Result: 1641 passed, 43 skipped, 1152 subtests passed in 46.45s; 0 failed. Baseline 1557 + 84 = 1641.

# PREEXISTING_CHANGES

Exact git status --short captured before MSG031 edit:

     M AGENTS.md
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.001.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.003.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.004.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.005.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.006.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.007.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.009.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.010.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.011.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.013.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.014.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.016.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.017.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.018.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.019.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.020.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.021.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.022.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.024.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.027.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.028.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.029.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.030.yaml
     M eaeu_xml/src/eaeu_xml/process_packages/body.py
     M eaeu_xml/src/eaeu_xml/process_packages/engine.py
     M eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py
     M eaeu_xml/src/eaeu_xml/process_packages/validator.py
     M eaeu_xml/tests/test_structured_rules.py
    ?? P.SP.02_OP_22/tests/test_msg001_structured_rules.py
    ?? P.SP.02_OP_22/tests/test_msg003_embedded_one_of.py
    ?? P.SP.02_OP_22/tests/test_msg003_repeatable_xml_alignment.py
    ?? P.SP.02_OP_22/tests/test_msg003_table36_full_rules.py
    ?? P.SP.02_OP_22/tests/test_msg003_table36_safe_partial_inherited.py
    ?? P.SP.02_OP_22/tests/test_msg003_table37_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg004_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg004_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg004_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg005_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg005_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg005_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg006_010_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg006_010_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg006_010_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg011_014_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg011_014_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg011_014_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg016_019_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg016_019_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg016_019_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg020_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg020_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg020_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg021_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg021_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg021_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg022_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg022_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg024_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg024_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg027_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg027_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg027_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg028_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg028_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg028_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg029_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg029_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg029_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg030_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg030_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg030_safe_mapping.py
    ?? codex_reports/
    ?? eaeu_xml/tests/test_embedded_one_of.py
    ?? eaeu_xml/tests/test_repeatable_xml_alignment.py

These changes were preserved. Protected baseline confirms no shared Python or MSG001-030 mapping changed during this batch.

# CURRENT_BATCH_CHANGES

- P.SP.02_OP_22/message_rules/P.SP.02.MSG.031.yaml
- P.SP.02_OP_22/tests/test_msg031_safe_mapping.py
- P.SP.02_OP_22/tests/test_msg031_repeatable_xml.py
- P.SP.02_OP_22/tests/test_msg031_rule_execution.py
- P.SP.02_OP_22/tests/test_msg031_end_to_end.py
- codex_reports/MSG031_IMPLEMENTATION_REPORT.md

MSG031 mapping diff stat relative to HEAD: 4246 insertions(+), 1 deletion(-). Four MSG031 test files are new/untracked. codex_reports was already an untracked service directory.
New tracked diff name relative to pre-edit snapshot: P.SP.02_OP_22/message_rules/P.SP.02.MSG.031.yaml.

# GIT_STATUS

Final git status --short:

     M AGENTS.md
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.001.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.003.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.004.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.005.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.006.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.007.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.009.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.010.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.011.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.013.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.014.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.016.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.017.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.018.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.019.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.020.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.021.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.022.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.024.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.027.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.028.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.029.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.030.yaml
     M P.SP.02_OP_22/message_rules/P.SP.02.MSG.031.yaml
     M eaeu_xml/src/eaeu_xml/process_packages/body.py
     M eaeu_xml/src/eaeu_xml/process_packages/engine.py
     M eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py
     M eaeu_xml/src/eaeu_xml/process_packages/validator.py
     M eaeu_xml/tests/test_structured_rules.py
    ?? P.SP.02_OP_22/tests/test_msg001_structured_rules.py
    ?? P.SP.02_OP_22/tests/test_msg003_embedded_one_of.py
    ?? P.SP.02_OP_22/tests/test_msg003_repeatable_xml_alignment.py
    ?? P.SP.02_OP_22/tests/test_msg003_table36_full_rules.py
    ?? P.SP.02_OP_22/tests/test_msg003_table36_safe_partial_inherited.py
    ?? P.SP.02_OP_22/tests/test_msg003_table37_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg004_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg004_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg004_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg005_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg005_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg005_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg006_010_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg006_010_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg006_010_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg011_014_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg011_014_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg011_014_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg016_019_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg016_019_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg016_019_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg020_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg020_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg020_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg021_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg021_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg021_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg022_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg022_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg024_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg024_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg027_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg027_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg027_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg028_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg028_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg028_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg029_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg029_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg029_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg030_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg030_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg030_safe_mapping.py
    ?? P.SP.02_OP_22/tests/test_msg031_end_to_end.py
    ?? P.SP.02_OP_22/tests/test_msg031_repeatable_xml.py
    ?? P.SP.02_OP_22/tests/test_msg031_rule_execution.py
    ?? P.SP.02_OP_22/tests/test_msg031_safe_mapping.py
    ?? codex_reports/
    ?? eaeu_xml/tests/test_embedded_one_of.py
    ?? eaeu_xml/tests/test_repeatable_xml_alignment.py

No git reset/clean/checkout/stash/add/commit was executed.

# GIT_DIFF_CHECK

Final git diff --check: PASS, no output.

# PROTECTED_FILES

Baseline /tmp/msg031_protected_before.json contains 29 protected entries: body.py, rules_engine.py, engine.py, validator.py, and mappings MSG001-030; MSG031 intentionally excluded. Final SHA-256 + mtime_ns comparison: 0 mismatches.

# DEFECTS_FOUND

- SOURCE_CONFLICT confirmed for Table48 REQ2, REQ30, REQ32; intentionally unmapped.
- Evaluator gaps remain for Table48 REQ16-20, REQ26 and Table49 REQ18-19; Table49 REQ5 also has an engine remainder for conditional membership in two exact literals.
- No shared production defect was required for the SAFE subset. Existing ONE_OF, branch applicability, same-parent for_each, conditions, filtered selection cardinality, and comparison primitives were sufficient for mapped fragments.

# REMAINING_REQUIREMENTS

- Table48 REQ1 — SAFE_PARTIAL: external StatusCode in {01,02}; external EndDateTime absent; external TrademarkApplicationId equality.
- Table48 REQ2 — SOURCE_CONFLICT: requirement left unmapped; no same-local-name/other-owner substitution.
- Table48 REQ3 — SAFE_PARTIAL: authoritative classifier-presence predicate; authoritative classifier code designation; required code when external branch applies.
- Table48 REQ4 — SAFE_PARTIAL: authoritative classifier-absence predicate.
- Table48 REQ13 — AMBIGUOUS: owner/instance semantics for the standalone AP value statement.
- Table48 REQ16 — ENGINE_UNSUPPORTED: exact normative semantics.
- Table48 REQ17 — ENGINE_UNSUPPORTED: exact normative semantics.
- Table48 REQ18 — ENGINE_UNSUPPORTED: exact normative semantics.
- Table48 REQ19 — ENGINE_UNSUPPORTED: exact normative semantics.
- Table48 REQ20 — ENGINE_UNSUPPORTED: exact normative semantics.
- Table48 REQ26 — ENGINE_UNSUPPORTED: exact normative semantics.
- Table48 REQ30 — SOURCE_CONFLICT: requirement left unmapped; no same-local-name/other-owner substitution.
- Table48 REQ32 — SOURCE_CONFLICT: requirement left unmapped; no same-local-name/other-owner substitution.
- Table49 REQ3 — SAFE_PARTIAL: external uniqueness/nonexistence lookup.
- Table49 REQ4 — SAFE_PARTIAL: authoritative classifier-presence predicate; authoritative classifier code designation; required code when external branch applies.
- Table49 REQ5 — SAFE_PARTIAL: authoritative classifier-absence predicate; conditional membership in the two exact normative fallback names.
- Table49 REQ18 — ENGINE_UNSUPPORTED: exact normative semantics.
- Table49 REQ19 — ENGINE_UNSUPPORTED: exact normative semantics.

These remainders do not block READY for the requested SAFE executable subset because they are explicitly classified instead of simulated.

# VERDICT

VERDICT = READY

All READY criteria are satisfied: independent normative reread; exact ONE_OF and branch isolation; QName/owner verification; dual inherited provenance; REQ26 OR preservation; source-conflict non-substitution; external semantics non-simulation; repeatable production-XML ownership; two valid E2E branches; green required regressions; git diff --check PASS; 29 protected files with 0 hash/mtime mismatches.
