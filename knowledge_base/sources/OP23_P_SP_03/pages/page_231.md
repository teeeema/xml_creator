---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 231
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

65 
 
Код 
требования 
Формулировка требования 
(ipcdo:ApellationOfOriginDetails) должен быть заполнен, и в его составе 
должны быть заполнены реквизиты: 
«Регистрационный номер НМПТ Союза» 
(ipsdo:ApellationOfOriginEAEUId); 
«Наименование обозначения НМПТ» (ipsdo:ApellationOfOriginName; 
«Указание товара, в отношении которого осуществляется регистрация  
и (или) предоставление права использования НМПТ» 
(ipsdo:ApellationOfOriginGoodsText); 
«Описание особого свойства товара» 
(ipsdo:GoodsPropertiesDescriptionText); 
«Описание географического объекта или его границ» 
(ipsdo:GeographicRegionDescriptionText) 
40 в составе реквизита «НМПТ Союза» (ipcdo:ApellationOfOriginDetails) 
реквизиты «Код страны» (csdo:UnifiedCountryCode), «Дата регистрации 
объекта интеллектуальной собственности» (ipsdo:RegistrationDate)  
и «Дата опубликования сведений об объекте интеллектуальной 
собственности» (ipsdo:PublicationDate) не заполняются 
41 реквизит «Сведения о национальной регистрации НМПТ» 
(ipcdo:ApellationOfOriginNationalRegistrationDetails) не заполняется 
42 реквизит «Признак согласия на обработку представленных сведений» 
(ipsdo:ConsentToDataProcessingIndicator)) должен быть заполнен 
43 реквизит «Сведения о подписании документа» (ipcdo:SignatureDetails) 
должен быть заполнен, и в его составе если реквизит «Сотрудник 
организации» (ipcdo:OfficerDetails) заполнен, то реквизит «ФИО» 
(ccdo:FullNameDetails), непосредственно подчиненный реквизиту 
«Сведения о подписании документа» (ipcdo:SignatureDetails),  
не заполняется 
44 если в составе реквизита «Сведения о подписании документа» 
(ipcdo:SignatureDetails) реквизит «ФИО» (ccdo:FullNameDetails), 
непосредственно подчиненный реквизиту «Сведения о подписании 
документа» (ipcdo:SignatureDetails), заполнен, то реквизит «Сотрудник 
организации» (ipcdo:OfficerDetails) не заполняется 
45 в составе электронного документа (сведений) должен быть заполнен 1 
или несколько экземпляров реквизита «Прилагаемый документ» 
(ipcdo:AccompanyingDocumentsDetails)
