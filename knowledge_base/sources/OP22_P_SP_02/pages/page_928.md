---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 928
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

106 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
 3.2. Описание 
(csdo:DescriptionText) 
описание причин для отказа M.SDE.00002 csdo:Text4000Type (M.SDT.00088) 
Строка символов. 
Мин. длина: 1. 
Макс. длина: 4000 
1..* 
4. Технологические характеристики 
записи общего ресурса 
(ccdo:ResourceItemStatusDetails) 
совокупность сведений о записи 
единого реестра товарных 
знаков Союза 
M.CDE.00032 ccdo:ResourceItemStatusDetailsType 
(M.CDT.00033) 
Определяется областями значений 
вложенных элементов 
1 
 4.1. Период действия 
(ccdo:ValidityPeriodDetails) 
период действия записи общего 
ресурса (реестра, перечня, базы 
данных) 
M.CDE.00033 ccdo:PeriodDetailsType (M.CDT.00026) 
Определяется областями значений 
вложенных элементов 
0..1 
  4.1.1. Начальная дата и время 
(csdo:StartDateTime) 
начальная дата и время M.SDE.00133 bdt:DateTimeType (M.BDT.00006) 
Обозначение даты и времени  
в соответствии с ISO 8601 
0..1 
  4.1.2. Конечная дата и время 
(csdo:EndDateTime) 
конечная дата и время M.SDE.00134 bdt:DateTimeType (M.BDT.00006) 
Обозначение даты и времени  
в соответствии с ISO 8601 
0..1 
 4.2. Дата и время обновления 
(csdo:UpdateDateTime) 
дата и время обновления записи 
общего ресурса (реестра, 
перечня, базы данных) 
M.SDE.00079 bdt:DateTimeType (M.BDT.00006) 
Обозначение даты и времени  
в соответствии с ISO 8601 
0..1
