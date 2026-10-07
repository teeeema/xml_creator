---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 885
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

63 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
  2.20.3. Дата подачи 
национальной заявки 
(ipsdo:NationalApplicationReceipt
Date) 
дата подачи заявки  
на регистрацию товарного знака 
в национальном реестре 
M.IP.SDE.00118 bdt:DateType (M.BDT.00005) 
Обозначение даты в соответствии  
с ISO 8601 
0..1 
  2.20.4. Дата приоритета 
товарного знака 
(ipsdo:PriorityDate) 
дата приоритета, указанная  
в национальной заявке  
на регистрацию товарного знака 
M.IP.SDE.00050 bdt:DateType (M.BDT.00005) 
Обозначение даты в соответствии  
с ISO 8601 
0..1 
 2.21. Сведения об изменении 
заявителя 
(ipcdo:ApplicantChangeDetails) 
сведения об изменении 
заявителя 
M.IP.CDE.00215 ipcdo:ApplicantChangeDetailsType 
(M.IP.CDT.00216) 
Определяется областями значений 
вложенных элементов 
0..1 
  2.21.1. Основание для 
изменения сведений о заявителе 
(ipsdo:ApplicantChangeBasis
Code) 
код причины изменения 
сведений о заявителе 
M.IP.SDE.00001 ipsdo:ApplicantChangeBasisCodeType 
(M.IP.SDT.00105) 
Значение кода в соответствии  
с перечнем причин изменения 
сведений о заявителе при внесении 
изменений в заявку на регистрацию 
товарного знака Евразийского 
экономического союза. 
Шаблон: \d{2} 
0..1
