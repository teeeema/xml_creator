---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 748
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

169 
 
Код 
требования 
Формулировка требования 
30 реквизит «Доказательства различительной способности обозначения» 
(ipcdo:NamingAbilityProofDetails) должен быть заполнен 
31 в составе реквизита «Заявка на товарный знак Союза (ходатайство, 
жалоба)» (ipcdo:TrademarkApplicationDetails) реквизиты: 
«Национальная заявка на регистрацию товарного знака» 
(ipcdo:TrademarkNationalApplicationDetails),  
«Сведения об изменении заявителя» (ipcdo:ApplicantChangeDetails), 
«Жалоба» (ipcdo:ComplaintDetails), 
«Ответ на жалобу заявителя на решение национального патентного 
ведомства» (ipcdo:ApplicantComplainResponseDetails), 
«Сведения об обращении заинтересованного лица о несоответствии 
обозначения, заявленного на регистрацию в качестве товарного знака 
Союза, требованиям Договора о товарных знаках» 
(ipcdo:TrademarkClaimDetails) не заполняются 
32 реквизит «Отказ в регистрации объекта интеллектуальной 
собственности» (ipcdo:RefusalDetails) не заполняется 
33 в составе реквизита «Технологические характеристики записи общего 
ресурса» (ccdo:ResourceItemStatusDetails) реквизит «Начальная дата  
и время» (csdo:StartDateTime) заполняется обязательно 
34 в составе реквизита «Технологические характеристики записи общего 
ресурса» (ccdo:ResourceItemStatusDetails) реквизит «Конечная дата  
и время» (csdo:EndDateTime) не заполняется 
35 реквизит «Сведения о подписании документа» (ipcdo:SignatureDetails) 
должен быть заполнен, и в его составе если реквизит «Сотрудник 
организации» (ipcdo:OfficerDetails) заполнен, то реквизит «ФИО» 
(ccdo:FullNameDetails), непосредственно подчиненный реквизиту 
«Сведения о подписании документа» (ipcdo:SignatureDetails),  
не заполняется 
36 если в составе реквизита «Сведения о подписании документа» 
(ipcdo:SignatureDetails) реквизит «ФИО» (ccdo:FullNameDetails), 
непосредственно подчиненный реквизиту «Сведения о подписании 
документа» (ipcdo:SignatureDetails), заполнен, то реквизит «Сотрудник 
организации» (ipcdo:OfficerDetails) не заполняется 
37 если в составе реквизита «Сведения о подписании документа»  
(ipcdo:SignatureDetails) заполнен реквизит «Сотрудник организации» 
(ipcdo:OfficerDetails), в его составе должны быть заполнены реквизиты 
«Фамилия» (csdo:LastName), «Имя» (csdo:FirstName) и «Наименование 
должности» (csdo:PositionName), а реквизит «Контактный реквизит» 
(ccdo:CommunicationDetails) не заполняется
