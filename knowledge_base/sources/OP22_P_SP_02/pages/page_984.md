---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 984
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

162 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
 2.24. Технологические 
характеристики записи общего 
ресурса 
(ccdo:ResourceItemStatusDetails) 
совокупность технологических 
сведений о записи общего 
ресурса 
M.CDE.00032 ccdo:ResourceItemStatusDetailsType 
(M.CDT.00033) 
Определяется областями значений 
вложенных элементов 
1 
  2.24.1. Период действия 
(ccdo:ValidityPeriodDetails) 
период действия записи общего 
ресурса (реестра, перечня, базы 
данных) 
M.CDE.00033 ccdo:PeriodDetailsType (M.CDT.00026) 
Определяется областями значений 
вложенных элементов 
0..1 
   *.1. Начальная дата и время 
(csdo:StartDateTime) 
начальная дата и время M.SDE.00133 bdt:DateTimeType (M.BDT.00006) 
Обозначение даты и времени  
в соответствии с ISO 8601 
0..1 
   *.2. Конечная дата и время 
(csdo:EndDateTime) 
конечная дата и время M.SDE.00134 bdt:DateTimeType (M.BDT.00006) 
Обозначение даты и времени  
в соответствии с ISO 8601 
0..1 
  2.24.2. Дата и время обновления 
(csdo:UpdateDateTime) 
дата и время обновления записи 
общего ресурса (реестра, 
перечня, базы данных) 
M.SDE.00079 bdt:DateTimeType (M.BDT.00006) 
Обозначение даты и времени  
в соответствии с ISO 8601 
0..1
