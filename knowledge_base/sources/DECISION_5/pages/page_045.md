---
source_document: "5 решение.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/5 решение.pdf"
source_sha256: "84987769629e0285eca4bad36f39f0e2fd38980301c0ecb21e2fbfa0447f5592"
pdf_page: 45
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

            journ:MessageID  xs:anyURI  
заголовок wsa:MessageID, 
содержащий идентификатор 
сообщения  
1  
            journ:RelatesTo  xs:anyURI  
заголовок wsa:RelatesTo, 
содержащий ссылочный 
идентификатор сообщения  
0..1  
            journ:ConversationID  xs:anyURI  
заголовок int:ConversationID, 
содержащий идентификатор 
экземпляра процедуры 
общего процесса  
0..1  
            journ:MessageType  xs:string  тип сообщения  1  
            journ:Receipt    информация о квитанции 
доверенной третьей стороны  0..1  
               journ:DocumentRef  xs:string  идентификатор электронного 
документа  1  
               journ:ReceiptId  xs:string  идентификатор квитанции 
доверенной третьей стороны  1  
               journ:IsValid  xs:boolean  
результат проверки 
электронной цифровой 
подписи (электронной 
подписи) в электронном 
документе  
1  
               journ:ErrorCode  xs:string  
код ошибки при проверке 
электронной цифровой 
подписи (электронной 
подписи) в электронном 
документе  
0..1  
               journ:ReasonText  xs:string  
причина ошибки при 
проверке электронной 
цифровой подписи 
(электронной подписи) в 
электронном документе  
0..1  
         journ:OperationDt  xs:dateTime  дата операции  1  
         journ:TrackID xs:anyURI  
технологический 
уникальный идентификатор 
сообщения  
1  
         journ:AcceptTime  xs:dateTime  
дата и время приема 
сообщения интеграционным 
шлюзом  
1  
         journ:Source xs:string  наименование системы – 
источника сообщения  1  
         journ:Receiver xs:string  наименование системы – 
приемника сообщения  1  
         journ:Status  xs:string  статус обработки  1  
         journ:Msg  xs:string  сообщение в точке 
журналирования  1  
         journ:ErrorTxt  xs:string  ошибка обработки  
(при наличии)  0..1  
         journ:ErrorCode  xs:string  код ошибки обработки  0..1
