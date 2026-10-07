# REGULATOR QUESTIONS — OP26 / P.MM.01

Ниже вопросы сформулированы так, чтобы их можно было отправить владельцу нормативных/интеграционных данных без технических догадок.

## 1. Официальные XML-схемы и версии

1. Просим подтвердить конкретную опубликованную версию структуры R.006, которая в 26_ОП.pdf (PDF 309, таблица 2) обозначена как Y.Y.Y, и предоставить соответствующую официальную XML-схему (в источнике имя задано шаблоном EEC_R_ProcessingResultDetails_vY.Y.Y.xsd) вместе со всеми импортируемыми схемами. Просим также подтвердить concrete targetNamespace вместо urn:EEC:R:ProcessingResultDetails:vY.Y.Y.

2. Просим подтвердить конкретную опубликованную версию структуры R.007, которая в 26_ОП.pdf (PDF 314, таблица 5) обозначена как Y.Y.Y, и предоставить соответствующую официальную XML-схему (шаблон EEC_R_ResourceStatusDetails_vY.Y.Y.xsd) вместе со всеми импортируемыми схемами. Просим подтвердить concrete targetNamespace вместо urn:EEC:R:ResourceStatusDetails:vY.Y.Y.

3. Просим предоставить официальную XML-схему `EEC_R_HC_MM_01_DrugRegistrationDetails_v1.1.0.xsd` для структуры R.HC.MM.01.001 версии 1.1.0, указанную в 26_ОП.pdf (PDF 319, Table 8), вместе со всеми XSD, реально импортируемыми этой схемой, чтобы можно было проверить targetNamespace, xs:import/schemaLocation, типы и кардинальности.

4. Просим предоставить официальную XML-схему `EEC_R_HC_MM_01_DrugRegistrationExpertReportDetails_v1.1.0.xsd` для структуры R.HC.MM.01.002 версии 1.1.0, указанную в 26_ОП.pdf (PDF 413, Table 11), вместе со всеми XSD, реально импортируемыми этой схемой, чтобы можно было проверить targetNamespace, xs:import/schemaLocation, типы и кардинальности.

5. Просим предоставить официальную XML-схему `EEC_R_HC_MM_01_DrugRegistrationDocContentDetails_v1.1.0.xsd` для структуры R.HC.MM.01.003 версии 1.1.0, указанную в 26_ОП.pdf (PDF 422, Table 14), вместе со всеми XSD, реально импортируемыми этой схемой, чтобы можно было проверить targetNamespace, xs:import/schemaLocation, типы и кардинальности.

6. Просим предоставить официальную XML-схему `EEC_R_HC_MM_01_DrugRegistrationNumberRequestDetails_v1.1.0.xsd` для структуры R.HC.MM.01.004 версии 1.1.0, указанную в 26_ОП.pdf (PDF 433, Table 17), вместе со всеми XSD, реально импортируемыми этой схемой, чтобы можно было проверить targetNamespace, xs:import/schemaLocation, типы и кардинальности.

7. Просим предоставить официальную XML-схему `EEC_R_HC_MM_01_DrugApprovalApplicationDetails_v1.1.0.xsd` для структуры R.HC.MM.01.006 версии 1.1.0, указанную в 26_ОП.pdf (PDF 438, Table 20), вместе со всеми XSD, реально импортируемыми этой схемой, чтобы можно было проверить targetNamespace, xs:import/schemaLocation, типы и кардинальности.

8. Просим предоставить официальную XML-схему `EEC_R_HC_MM_01_DrugRegistrationStatusDetails_v1.0.0.xsd` для структуры R.HC.MM.01.007 версии 1.0.0, указанную в 26_ОП.pdf (PDF 450, Table 23), вместе со всеми XSD, реально импортируемыми этой схемой, чтобы можно было проверить targetNamespace, xs:import/schemaLocation, типы и кардинальности.

## 2. Базисная и healthcare-модель

9. В 26_ОП.pdf импортируемые пространства имен `urn:EEC:M:ComplexDataObjects:vX.X.X` (`ccdo`) и `urn:EEC:M:SimpleDataObjects:vX.X.X` (`csdo`) содержат placeholder X.X.X (например, PDF 309, таблица 3). Просим сообщить точную версию базисной модели данных, использованную при формировании XSD OP26, и предоставить официальный schema package этой версии.

10. В healthcare-структурах OP26 пространства имен `urn:EEC:M:HC:ComplexDataObjects:vX.X.X` (`hccdo`) и `urn:EEC:M:HC:SimpleDataObjects:vX.X.X` (`hcsdo`) также содержат X.X.X (PDF 319–320, таблица 9; аналогично таблицы 12/15/18/21/24). Просим сообщить точную версию модели данных предметной области «Здравоохранение» и официальный schema package этой версии.

## 3. P.CLS.019

11. 26_ОП.pdf, PDF 39, таблица 10 определяет P.CLS.019 как «классификатор стран мира» с кодами и наименованиями стран по ISO 3166-1. Просим предоставить официальный machine-readable payload P.CLS.019, применимый к данной редакции OP26, с идентификатором `P.CLS.019`, версией/редакцией, датой вступления в действие (effective date), полным набором кодов и наименований и, если ведётся, статусом/периодом действия кодов. Просим также указать официальный формат экспорта; текущий нормативный PDF конкретный XML/JSON/CSV-формат не задаёт.

## 4. Контракт единого реестра

12. Просим предоставить официальный контракт/API schema либо спецификацию официального offline snapshot единого реестра зарегистрированных лекарственных средств, применимый к P.MM.01, и подтвердить, как отличать `NOT FOUND` от недоступности/ошибки источника, как определяется активная запись (`EndDateTime`), какие исторические/временные данные доступны и как идентифицируются документы. Контракт нужен минимум для следующих нормативных lookup-правил:

| Requirement | PDF/table | Что нужно подтвердить в контракте | История |
|---|---|---|---|
| `OP26.P_MM_01.P.MM.01.MSG.001.REQ.011` | 209, Table 18 item 11 | ключ `ApplicationId + UnifiedCountryCode`; результат: No active matching record; active-state interpretation uses empty EndDateTime | NO |
| `OP26.P_MM_01.P.MM.01.MSG.001.REQ.014` | 210, Table 18 item 14 | ключ `DrugApplicationKindCode=02 + registration-certificate identity/details`; результат: Stored registration-certificate details must match incoming certificate data | NO |
| `OP26.P_MM_01.P.MM.01.MSG.001.REQ.015` | 210, Table 18 item 15 | ключ `DrugApplicationKindCode=03 + ApplicationChangeId / certificate-change details`; результат: Stored change/certificate details must match incoming data | NO |
| `OP26.P_MM_01.P.MM.01.MSG.001.REQ.028` | 212, Table 18 item 28 | ключ `ApplicationId`; результат: Matching active registry record must exist; EndDateTime empty | NO |
| `OP26.P_MM_01.P.MM.01.MSG.002.REQ.009` | 217, Table 19 item 9 | ключ `ApplicationId + RegistrationNumberId + UnifiedCountryCode + CountryKindCode`; результат: Matching active record; EndDateTime empty; stored StartDateTime < incoming StartDateTime | YES |
| `OP26.P_MM_01.P.MM.01.MSG.002.REQ.087 [source row; embedded in current REQ.050]` | 230–231, Table 19 item 87 | ключ `ApplicationId + UnifiedCountryCode + reference-state role`; результат: Matching registry data and PDF documents present in five named document groups | UNKNOWN |
| `OP26.P_MM_01.P.MM.01.MSG.003.REQ.007` | 232, Table 20 item 7 | ключ `ApplicationId + UnifiedCountryCode`; результат: Matching active record; EndDateTime empty; stored StartDateTime < exclusion StartDateTime | YES |
| `OP26.P_MM_01.P.MM.01.MSG.014.REQ.003` | 235, Table 22 item 3 | ключ `ApplicationId + UnifiedCountryCode`; результат: Matching record with ApplicationStatusCode=06 and reference-state country matching incoming country | NO |
| `OP26.P_MM_01.P.MM.01.MSG.025.REQ.003` | 236, Table 23 item 3 | ключ `ApplicationId and/or RegistrationNumberId`; результат: Matching registry record must exist | NO |
| `OP26.P_MM_01.P.MM.01.MSG.027.REQ.008` | 238, Table 24 item 8 | ключ `RegistrationNumberId + DrugRegistrationDocCode or DrugRegistrationFileCode`; результат: Matching stored document entry must exist | UNKNOWN |
| `OP26.P_MM_01.P.MM.01.MSG.028.REQ.005#SOURCE_ROW_5B` | 234, Table 21 item 5 (second occurrence) | ключ `RegistrationNumberId + ApplicationId`; результат: Matching registry record must exist | NO |

Для каждого lookup просим отдельно подтвердить поведение при отсутствии записи и при технической недоступности реестра; текущие таблицы требований задают бизнес-условие, но не транспортное/API-поведение.

## 5. Пять конфликтов источника

13. **OP26.P_MM_01.P.MM.01.MSG.002.REQ.022.** В 26_ОП.pdf PDF 219, Table 19 item 22: filling side: hcsdo:ChildJuvenileIndicator. В описании структуры на PDF 351, R.HC.MM.01.001 Table 10 fields *.2.3.2/*.2.3.3: structure side: separate hcsdo:ChildIndicator and hcsdo:JuvenileIndicator; ChildJuvenileIndicator absent. Confirm which field(s) the rule shall target: ChildIndicator, JuvenileIndicator, both, or a corrected field name; provide corrigendum/revised XSD if applicable.

14. **OP26.P_MM_01.P.MM.01.MSG.023.REQ.004.** В 26_ОП.pdf PDF 298, Table 21 item 4: filling side: DrugAttributeEnumText with AttributeKindCode or AttributeKindName. В описании структуры на PDF 415–421, R.HC.MM.01.002 Table 13: structure side: none of DrugAttributeEnumText/AttributeKindCode/AttributeKindName is declared. Confirm the authoritative target element/attributes, or provide corrected filling table / revised R.HC.MM.01.002 XSD.

15. **OP26.P_MM_01.P.MM.01.MSG.023.REQ.005.** В 26_ОП.pdf PDF 298, Table 21 item 5: filling side: AttributeKindCode/AttributeKindName inside DrugAttributeEnumText must denote “Номер документа основания”. В описании структуры на PDF 415–421, R.HC.MM.01.002 Table 13: structure side: referenced element/attributes absent. Confirm the intended field(s) that carry “Номер документа основания”, or provide corrected filling table / revised schema.

16. **OP26.P_MM_01.P.MM.01.MSG.024.REQ.006.** В 26_ОП.pdf PDF 300, Table 22 item 6: filling side: DrugAttributeEnumText requires AttributeKindCode or AttributeKindName. В описании структуры на PDF 415–421, R.HC.MM.01.002 Table 13: structure side: referenced element/attributes absent. Confirm the authoritative target element/attributes, or provide corrected filling table / revised schema.

17. **OP26.P_MM_01.P.MM.01.MSG.024.REQ.007.** В 26_ОП.pdf PDF 300, Table 22 item 7: filling side: AttributeKindName mandatory when AttributeKindCode is “другое”. В описании структуры на PDF 415–421, R.HC.MM.01.002 Table 13: structure side: DrugAttributeEnumText and the referenced attribute context are absent. Confirm where AttributeKindCode/AttributeKindName are defined for this message and whether a revised R.HC.MM.01.002 schema is authoritative.

## 6. Оборванный пункт 84

18. В `26_ОП.pdf`, PDF 230 / printed 229, Table 19, item 84 для `P.MM.01.MSG.002` текст заканчивается фразой «…PackageUpperLimitMeasure обязательны для заполнения и», после чего сразу начинается item 85. На следующей PDF-странице 231 продолжается уже item 87. Просим предоставить полную официальную формулировку item 84 либо реквизиты corrigendum/акта, исправляющего этот текст, и подтвердить, какая редакция является действующей.
