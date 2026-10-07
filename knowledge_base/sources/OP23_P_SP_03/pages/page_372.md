---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 372
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

83 
 
Код 
требования 
Формулировка требования 
38 если реквизит «Описание особого свойства товара» 
(ipsdo:GoodsPropertiesDescriptionText) заполнен, атрибут «код вида 
свойства» (атрибут featureKindCode) и атрибут «наименование 
описываемого свойства» (атрибут featureName) в его составе 
не заполняются в составе любых реквизитов 
39 в составе любых экземпляров реквизита «Сведения записи Единого 
реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails) 
в составе реквизита «Национальное патентное ведомство» 
(ipcdo:PatentAuthorityDetails) должны быть заполнены реквизиты: 
«Код страны» (csdo:UnifiedCountryCode); 
«Наименование уполномоченного органа» (csdo:AuthorityName); 
«Адрес» (ccdo:SubjectAddressDetails), в составе которого значение 
реквизита «Код вида адреса» (csdo:AddressKindCode) должно 
соответствовать значению «2» – «фактический адрес (адрес места 
нахождения или места жительства)» 
40 если реквизит «Адрес» (ccdo:SubjectAddressDetails) заполнен в составе 
любых реквизитов, в его составе должны быть заполнены реквизиты 
«Код вида адреса» (csdo:AddressKindCode)», «Код страны» 
(csdo:UnifiedCountryCode), «Город» (csdo:CityName), «Улица» 
(csdo:StreetName) и «Номер дома» (csdo:BuildingNumberId) 
41 если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) 
заполнен в составе любых реквизитов, в его составе заполняются 
реквизиты «Код вида связи» (csdo:CommunicationChannelCode)  
и «Идентификатор канала связи» (csdo:CommunicationChannelId), 
а реквизит «Наименование вида связи» 
(csdo:CommunicationChannelName) не заполняется 
42 если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) 
заполнен в составе любых реквизитов, в его составе значение реквизита 
«Код вида связи» (csdo:CommunicationChannelCode) должно 
соответствовать одному из следующих значений: «TE», «EM» или «FX» 
в соответствии с перечнем видов средств (каналов) связи, утвержденным 
Решением Коллегии Комиссии от 6 декабря 2022 г. № 192 
43 если реквизит «Код страны» (csdo:UnifiedCountryCode) заполнен 
в составе любых реквизитов, в его составе значение атрибута 
«идентификатор справочника (классификатора)» (атрибут codeListId) 
должно соответствовать значению «ВОИС ST.3» 
44 в составе любых экземпляров реквизита «Сведения записи Единого 
реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails) 
реквизит «Прилагаемый документ» 
(ipcdo:AccompanyingDocumentsDetails) не заполняется
