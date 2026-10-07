---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 895
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

73 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
    *.11.11. Почтовый индекс 
(csdo:PostCode) 
почтовый индекс предприятия 
почтовой связи 
M.SDE.00006 csdo:PostCodeType (M.SDT.00006) 
Нормализованная строка символов. 
Шаблон: [A-Z0-9][A-Z0-9 -]{1,8}[A-
Z0-9] 
0..1 
    *.11.12. Номер 
абонентского ящика 
(csdo:PostOfficeBoxId) 
номер абонентского ящика на 
предприятии почтовой связи 
M.SDE.00013 csdo:Id20Type (M.SDT.00092) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 20 
0..1 
   *.12. Контактный реквизит 
(ccdo:CommunicationDetails) 
контактный реквизит субъекта M.CDE.00003 ccdo:CommunicationDetailsType 
(M.CDT.00003) 
Определяется областями значений 
вложенных элементов 
0..* 
    *.12.1. Код вида связи 
(csdo:Communication
ChannelCode) 
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
    *.12.2. Наименование вида 
связи 
(csdo:Communication
ChannelName) 
наименование вида средства 
(канала) связи (телефон, факс, 
электронная почта и др.) 
M.SDE.00093 csdo:Name120Type (M.SDT.00055) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 120 
0..1
