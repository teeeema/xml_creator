---
source_document: "5 решение.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/5 решение.pdf"
source_sha256: "84987769629e0285eca4bad36f39f0e2fd38980301c0ecb21e2fbfa0447f5592"
pdf_page: 44
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

информационного 
взаимодействия  
               journ:Version  xs:string  версия общего процесса  1  
               journ:ProcedureCode  xs:string  
код процедуры согласно 
регламенту 
информационного 
взаимодействия  
1  
               journ:TransactionCode  xs:string  
код транзакции общего 
процесса согласно 
регламенту 
информационного 
взаимодействия  
1  
               journ:MessageCode  xs:string  
код сообщения согласно 
регламенту 
информационного 
взаимодействия  
1  
            journ:Action xs:anyURI  
заголовок wsa:Action, 
идентифицирующий 
содержимое сообщения  
1  
            journ:Routing    информация о маршруте 
сообщения  1  
               journ:To xs:anyURI  
заголовок wsa:To, 
содержащий сведения о 
получателе  
1  
                  @Segment  xs:string  сегмент получателя  1  
               journ:ReplyTo  xs:anyURI  
заголовок 
wsa:ReplyTo/wsa:Address, 
содержащий сведения о 
логическом адресе 
отправителя, на который 
должно быть направлено 
сообщение-ответ  
0..1  
               journ:From xs:anyURI  
заголовок 
wsa:From/wsa:Address, 
содержащий сведения о 
логическом адресе 
отправителя, на который не 
может быть направлено 
сообщение-ответ  
0..1  
               journ:FaultTo  xs:anyURI  
заголовок 
wsa:FaultTo/wsa:Address, 
содержащий сведения о 
логическом адресе 
отправителя, на который 
должно быть направлено 
сообщение-ответ c ошибкой  
0..1  
               journ:FromSegment  xs:anyURI  
сегмент-источник сообщения 
(заполняется на основе 
адреса From или ReplyTo)  
1
