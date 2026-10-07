---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 442
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

42 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
  2.10.3. Контактный реквизит 
(ccdo:CommunicationDetails) 
контактные реквизиты адресата M.CDE.00003 ccdo:CommunicationDetailsType 
(M.CDT.00003) 
Определяется областями значений 
вложенных элементов 
0..* 
   *.1. Код вида связи 
(csdo:CommunicationChannel
Code) 
кодовое обозначение вида 
средства (канала) связи 
(телефон, факс, электронная 
почта и др.) 
M.SDE.00014 csdo:CommunicationChannelCodeV2
Type (M.SDT.00163) 
Значение кода в соответствии  
с перечнем видов средств (каналов) 
связи. 
Мин. длина: 1. 
Макс. длина: 20 
0..1 
   *.2. Наименование вида связи 
(csdo:CommunicationChannel
Name) 
наименование вида средства 
(канала) связи (телефон, факс, 
электронная почта и др.) 
M.SDE.00093 csdo:Name120Type (M.SDT.00055) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 120 
0..1 
   *.3. Идентификатор канала 
связи 
(csdo:CommunicationChannel
Id) 
последовательность символов, 
идентифицирующая канал связи 
(указание номера телефона, 
факса, адреса электронной 
почты и др.) 
M.SDE.00015 csdo:CommunicationChannelIdType 
(M.SDT.00015) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 1000 
1..* 
 2.11. НМПТ Союза 
(ipcdo:ApellationOfOriginDetails) 
сведения о НМПТ Союза M.IP.CDE.00031 ipcdo:ApellationOfOriginDetailsType 
(M.IP.CDT.00021) 
Определяется областями значений 
вложенных элементов 
0..1
