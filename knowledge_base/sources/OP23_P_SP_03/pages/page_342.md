---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 342
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

53 
 
Код 
требования 
Формулировка требования 
8 если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) 
заполнен в составе любых реквизитов, в его составе значение реквизита 
«Код вида связи» (csdo:CommunicationChannelCode) должно 
соответствовать одному из следующих значений: «TE», «EM» или «FX» 
в соответствии с перечнем видов средств (каналов) связи, утвержденным 
Решением Коллегии Комиссии от 6 декабря 2022 г. № 192 
9 если реквизит «Код страны» (csdo:UnifiedCountryCode) заполнен  
в составе любых реквизитов, в его составе значение атрибута 
«идентификатор справочника (классификатора)» (атрибут codeListId) 
должно соответствовать значению «ВОИС ST.3» 
10 реквизит «Номер документа» (csdo:DocId) составе реквизита «Заявка 
на НМПТ Союза» (ipcdo:ApellationOfOriginApplicationDetails) должен 
быть заполнен 
11 реквизит «Дата поступления документа» (ipsdo:IPDocReceiptDate) 
составе реквизита «Заявка на НМПТ Союза (ходатайство, 
свидетельство)» ipcdo:ApellationOfOriginApplicationDetails) должен быть 
заполнен 
12 реквизит «Дата подачи заявки» (ipsdo:ApplicationReceiptDate) в составе 
реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» 
(ipcdo:ApellationOfOriginApplicationDetails) должен быть заполнен 
13 реквизит «Регистрационный номер заявки на НМПТ Союза» 
(ipsdo:ApellationOfOriginApplicationId)» (csdo:DocId) в составе реквизита 
«Заявка на НМПТ Союза» (ipcdo:ApellationOfOriginApplicationDetails) 
должен быть заполнен 
14 в составе реквизита «Национальное патентное ведомство» 
(ipcdo:PatentAuthorityDetails) должен быть заполнены реквизиты «Код 
страны» (csdo:UnifiedCountryCode) и «Наименование уполномоченного 
органа» (csdo:AuthorityName) 
15 значение реквизита «Признак ведомства подачи»  
(ipsdo:OriginOfficeIndicator) в составе реквизита «Национальное 
патентное ведомство» (ipcdo:PatentAuthorityDetails)должно 
соответствовать значению «1» – ведомство подачи 
16 в составе реквизита «Национальное патентное ведомство» 
(ipcdo:PatentAuthorityDetails) должен быть заполнен реквизит «Адрес» 
(ccdo:SubjectAddressDetails), в составе которого значение реквизита 
«Код вида адреса» (csdo:AddressKindCode) должно соответствовать 
значению «2» – «фактический адрес (адрес места нахождения или места 
жительства)»
