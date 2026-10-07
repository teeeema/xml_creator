---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 528
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

116 
 
Код 
требования 
Формулировка требования 
7 если реквизит «Адрес» (ccdo:SubjectAddressDetails) заполнен в составе 
любых реквизитов, в его составе должны быть заполнены реквизиты 
«Код вида адреса» (csdo:AddressKindCode)», «Код страны» 
(csdo:UnifiedCountryCode), «Город» (csdo:CityName), «Улица» 
(csdo:StreetName) и «Номер дома» (csdo:BuildingNumberId) 
8 если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) 
заполнен в составе любых реквизитов, в его составе заполняются 
реквизиты «Код вида связи» (csdo:CommunicationChannelCode)  
и «Идентификатор канала связи» (csdo:CommunicationChannelId), 
а реквизит «Наименование вида связи» 
(csdo:CommunicationChannelName) не заполняется 
9 если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) 
заполнен в составе любых реквизитов, в его составе значение реквизита 
«Код вида связи» (csdo:CommunicationChannelCode) должно 
соответствовать одному из следующих значений: «TE», «EM» или «FX», 
в соответствии с перечнем видов средств (каналов) связи, утвержденным 
Решением Коллегии Комиссии от 6 декабря 2022 г. № 192 
10 в составе реквизита «Национальное патентное ведомство» 
(ipcdo:PatentAuthorityDetails) должны быть заполнены реквизиты: 
«Код страны» (csdo:UnifiedCountryCode); 
«Наименование уполномоченного органа» (csdo:AuthorityName); 
«Краткое наименование уполномоченного органа» 
(csdo:AuthorityBriefName) 
11 в электронном документе (сведениях) должен быть заполнен 1 экземпляр 
реквизита «Участник отношений в сфере регистрации и использования 
прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), 
в составе которого значение реквизита «Код вида участника отношений  
в сфере регистрации и использования прав на объекты интеллектуальной 
собственности» (ipsdo:IPPartyKindCode) соответствует значению 
«RH» – «правообладатель» 
12 в составе реквизита «Участник отношений в сфере регистрации  
и использования прав на объекты интеллектуальной собственности» 
(ipcdo:IPPartyDetails) должны быть заполнены реквизиты: 
«Код страны» (csdo:UnifiedCountryCode); 
«Полное наименование субъекта c указанием вида представления 
сведений и кода языка» (ipsdo:IPSubjectName); 
«Адрес» (ccdo:SubjectAddressDetails); 
«Контактный реквизит» (ccdo:CommunicationDetails)
