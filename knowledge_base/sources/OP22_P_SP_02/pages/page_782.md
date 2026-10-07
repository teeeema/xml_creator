---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 782
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

203 
 
Код 
требования 
Формулировка требования 
22 в составе экземпляра реквизита «Сведения записи Единого реестра  
ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails) реквизит  
«Конечная дата и время» (csdo:EndDateTime) не заполняется 
23 реквизит «Сведения о подписании документа» (ipcdo:SignatureDetails) 
должен быть заполнен, и в его составе если реквизит «Сотрудник 
организации» (ipcdo:OfficerDetails) заполнен, то реквизит «ФИО» 
(ccdo:FullNameDetails), непосредственно подчиненный реквизиту 
«Сведения о подписании документа» (ipcdo:SignatureDetails),  
не заполняется 
24 если в составе реквизита «Сведения о подписании документа» 
(ipcdo:SignatureDetails) реквизит «ФИО» (ccdo:FullNameDetails), 
непосредственно подчиненный реквизиту «Сведения о подписании 
документа» (ipcdo:SignatureDetails), заполнен, то реквизит «Сотрудник 
организации» (ipcdo:OfficerDetails) не заполняется 
25 если в составе реквизита «Сведения о подписании документа»  
(ipcdo:SignatureDetails) заполнен реквизит «Сотрудник организации» 
(ipcdo:OfficerDetails), в его составе должны быть заполнены реквизиты 
«Фамилия» (csdo:LastName), «Имя» (csdo:FirstName) и «Наименование 
должности» (csdo:PositionName), а реквизит «Контактный реквизит» 
(ccdo:CommunicationDetails) не заполняется 
 
77. Требования к заполнению реквизитов электронных документов 
(сведений) «Сведения о ТЗ Союза из Единого реестра ТЗ Союза» 
(R.IP.SP.02.007), передаваем ых в сообщении «Сведения  
о преобразовании ТЗ Союза в коллективный знак Союза» 
(P.SP.02.MSG.048), приведены в таблице 66.
