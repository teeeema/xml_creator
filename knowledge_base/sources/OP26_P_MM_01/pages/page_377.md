---
source_document: "26_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/26_ОП.pdf"
source_sha256: "a15cc6c946b35145e58304b7e3621ea76241f510e2202bbaf8912b4f8b0715e6"
pdf_page: 377
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

376 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн.  
 *.11.1. Код вида связи 
(csdo:CommunicationChannel
Code) 
кодовое обозначение вида 
средства (канала) связи 
(телефон, факс, электронная 
почта и др.) 
M.SDE.00014 csdo:CommunicationChannelCodeV2
Type (M.SDT.00163) 
Значение кода в соответствии со 
справочником видов связи. 
Мин. длина: 1. 
Макс. длина: 20 
0..1 
 *.11.2. Наименование вида 
связи 
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
 *.11.3. Идентификатор канала 
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
 *.12. Сведения о 
производственной площадке 
(hccdo:ManufacturingArea
Details) 
сведения о производственной 
площадке 
M.HC.CDE.00268 hccdo:ManufacturingAreaDetailsType 
(M.HC.CDT.00250) 
Определяется областями значений 
вложенных элементов 
0..* 
 *.12.1. Сведения о 
хозяйствующем субъекте 
(hccdo:BusinessEntityExpanded
Details) 
сведения о хозяйствующем 
субъекте 
M.HC.CDE.00136 hccdo:BusinessEntityExpandedDetails
Type (M.HC.CDT.00108) 
Определяется областями значений 
вложенных элементов 
0..1
