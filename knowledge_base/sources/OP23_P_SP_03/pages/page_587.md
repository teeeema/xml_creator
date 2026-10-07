---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 587
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

12 
Код 
требования 
Формулировка требования 
5 если в составе экземпляра реквизита «Сведения записи Единого реестра 
НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails значение 
реквизита «Код вида записи общего информационного ресурса»  
(ipsdo:ResourceItemKindCode) соответствует значению «AN»– «сведения  
о национальном НМПТ» (далее – запись, содержащая сведения  
о национальном НМПТ), то в составе такого экземпляра реквизита 
«Сведения записи Единого реестра НМПТ Союза» 
(ipcdo:ApellationOfOriginRegisterItemDetails) не заполняется «Адрес  
для переписки» (ipcdo:CorrespondenceAddressDetails) 
6 в составе записи, содержащей сведения о национальном НМПТ,  
в составе реквизита «Сведения о национальной регистрации НМПТ» 
(ipcdo:ApellationOfOriginNationalRegistrationDetails) должны быть 
заполнены реквизиты: 
«Код страны» (csdo:UnifiedCountryCode); 
«Регистрационный номер НМПТ в национальном реестре НМПТ» 
(ipsdo:ApellationOfOriginNationalId); 
«Дата регистрации объекта интеллектуальной собственности»  
(ipsdo:RegistrationDate); 
«Наименование обозначения НМПТ» (ipsdo:ApellationOfOriginName); 
«Указание товара, в отношении которого осуществляется регистрация  
и (или) предоставление права использования НМПТ» 
(ipsdo:ApellationOfOriginGoodsText); 
«Описание особого свойства товара»  
(ipsdo:GoodsPropertiesDescriptionText); 
«Описание географического объекта или его границ» 
(ipsdo:GeographicRegionDescriptionText) 
7 в составе записи, содержащей сведения о национальном НМПТ,  
в составе реквизита «Сведения о национальной регистрации НМПТ» 
(ipcdo:ApellationOfOriginNationalRegistrationDetails) должен быть 
заполнен 1 экземпляр реквизита «Наименование обозначения НМПТ» 
(ipsdo:ApellationOfOriginName), в составе которого значение атрибута 
«код вида представления наименования» (атрибут nameRepresentation
KindCode) должно соответствовать значению «OR» – «сведения, 
представленные на исходном (оригинальном) языке» и атрибут «код 
языка» (атрибут languageCode) должен быть заполнен
