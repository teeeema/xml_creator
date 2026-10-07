---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 779
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

200 
 
Код 
требования 
Формулировка требования 
4 в составе реквизита «Национальная заявка на регистрацию товарного 
знака» (ipcdo:TrademarkNationalApplicationDetails) должны быть 
заполнены реквизиты: 
«Код страны» (csdo:UnifiedCountryCode); 
«Номер национальной заявки» (ipsdo:NationalApplicationId); 
«Дата подачи национальной заявки»  
(ipsdo:NationalApplicationReceiptDate) 
5 в составе экземпляра реквизита «Сведения записи Единого реестра ТЗ 
Союза» (ipcdo:UnifiedRegisterRecordsDetails) в составе реквизита 
«Сведения о статусном состоянии» (ipcdo:IPEntityStatusDetails) реквизит 
«Дата» (csdo:EventDate) должен быть заполнен, значение реквизита 
«Код статуса» (csdo:StatusCode) должно соответствовать значению 
«06» – «аннулированный ТЗ Союза преобразован в национальную 
заявку», а атрибут «идентификатор справочника (классификатора)» 
(атрибут codeListId) в составе реквизита «Код статуса» (csdo:StatusCode) 
не заполняется 
6 в составе реквизита «Сведения записи Единого реестра ТЗ Союза» 
(ipcdo:UnifiedRegisterRecordsDetails) реквизит «Конечная дата и время» 
(csdo:EndDateTime) должен быть заполнен 
7 реквизит «Сведения о подписании документа» (ipcdo:SignatureDetails) 
должен быть заполнен, и в его составе если реквизит «Сотрудник 
организации» (ipcdo:OfficerDetails) заполнен, то реквизит «ФИО» 
(ccdo:FullNameDetails), непосредственно подчиненный реквизиту 
«Сведения о подписании документа» (ipcdo:SignatureDetails),  
не заполняется 
8 если в составе реквизита «Сведения о подписании документа» 
(ipcdo:SignatureDetails) реквизит «ФИО» (ccdo:FullNameDetails), 
непосредственно подчиненный реквизиту «Сведения о подписании 
документа» (ipcdo:SignatureDetails), заполнен, то реквизит «Сотрудник 
организации» (ipcdo:OfficerDetails) не заполняется 
9 если в составе реквизита «Сведения о подписании документа»  
(ipcdo:SignatureDetails) заполнен реквизит «Сотрудник организации» 
(ipcdo:OfficerDetails), в его составе должны быть заполнены реквизиты 
«Фамилия» (csdo:LastName), «Имя» (csdo:FirstName) и «Наименование 
должности» (csdo:PositionName), а реквизит «Контактный реквизит» 
(ccdo:CommunicationDetails) не заполняется 
 
76. Требования к заполнению реквизитов электронных документов 
(сведений) «Сведения о ТЗ Союза из Единого реестра ТЗ Союза»
