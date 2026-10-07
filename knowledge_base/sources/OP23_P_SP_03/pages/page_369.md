---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 369
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

80 
 
Код 
требования 
Формулировка требования 
32 если в составе электронного документа (сведений) заполнен экземпляр 
реквизита «Сведения записи Единого реестра НМПТ Союза» 
(ipcdo:ApellationOfOriginRegisterItemDetails), содержащий сведения 
о праве использования НМПТ Союза, или если в составе электронного 
документа (сведений) заполнен экземпляр реквизита «Сведения записи 
Единого реестра НМПТ Союза» 
(ipcdo:ApellationOfOriginRegisterItemDetails), содержащий сведения 
о предоставленном на основании национального свидетельства праве 
использования НМПТ Союза, в составе реквизита «Адрес 
для переписки» (ipcdo:CorrespondenceAddressDetails) в составе реквизита 
«Адрес» (ccdo:SubjectAddressDetails) значение реквизита «Код вида 
адреса» (csdo:AddressKindCode) должно соответствовать значению 
«3» – «почтовый адрес (адрес для ведения переписки)», а значение 
реквизита «Код страны» (csdo:UnifiedCountryCode) должно 
соответствовать одному из следующих значений: «AM», «BY», «KZ», 
«KG» или «RU» 
33 если в составе электронного документа (сведений) заполнен экземпляр 
реквизита «Сведения записи Единого реестра НМПТ Союза» 
(ipcdo:ApellationOfOriginRegisterItemDetails), содержащий сведения 
о предоставленном на основании национального свидетельства праве 
использования НМПТ Союза, то в составе такого экземпляра реквизита 
«Сведения записи Единого реестра НМПТ Союза» 
(ipcdo:ApellationOfOriginRegisterItemDetails) должны быть заполнены 
от 1 до 5 экземпляров реквизита «Сведения о национальной регистрации 
НМПТ» (ipcdo:ApellationOfOriginNationalRegistrationDetails), 
в составе которых: 
реквизит «Код страны» (csdo:UnifiedCountryCode) заполнен и уникален  
в рамках таких экземпляров реквизита «Сведения о национальной 
регистрации НМПТ» 
(ipcdo:ApellationOfOriginNationalRegistrationDetails); 
заполнены реквизиты «Регистрационный номер НМПТ в национальном 
реестре НМПТ» (ipsdo:ApellationOfOriginNationalId) и «Сведения о праве 
использования (исключительном праве)» (ipcdo:IPRightDetails),  
а остальные реквизиты в составе реквизита «Сведения о национальной 
регистрации НМПТ» (ipcdo:ApellationOfOriginNationalRegistrationDetails) 
не заполняются
