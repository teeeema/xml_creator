---
source_document: "26_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/26_ОП.pdf"
source_sha256: "a15cc6c946b35145e58304b7e3621ea76241f510e2202bbaf8912b4f8b0715e6"
pdf_page: 334
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

333 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн.  
 2.2.5. Сведения об изменяемом 
регистрационном удостоверении 
на лекарственный препарат 
(hccdo:DrugRegistrationCertificate
ChangeDetails) 
сведения об изменяемом 
регистрационном 
удостоверении на 
лекарственный препарат 
M.HC.CDE.00135 hccdo:DrugRegistrationCertificate
ChangeDetailsType (M.HC.CDT.00109) 
Определяется областями значений 
вложенных элементов 
0..* 
 *.1. Номер регистрационного 
удостоверения 
(hcsdo:RegistrationCertificateId) 
номер регистрационного 
удостоверения 
M.HC.SDE.00045 csdo:Id50Type (M.SDT.00093) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 50 
1 
 *.2. Дата документа 
(csdo:DocCreationDate) 
дата регистрации 
лекарственного препарата 
референтным государством или 
государством признания 
M.SDE.00045 bdt:DateType (M.BDT.00005) 
Обозначение даты в соответствии с 
ГОСТ ИСО 8601–2001 
1 
 *.3. Дата внесения изменения 
(hcsdo:DocExtensionDate) 
дата внесения изменений 
(переоформления) в 
регистрационное удостоверение 
лекарственного препарата 
M.HC.SDE.00070 bdt:DateType (M.BDT.00005) 
Обозначение даты в соответствии с 
ГОСТ ИСО 8601–2001 
1 
 2.2.6. Сведения об изменении, 
вносимом в регистрационное 
досье на лекарственный препарат 
(hccdo:DrugApplicationChange
Details) 
сведения об изменении, 
вносимом в регистрационное 
досье на лекарственный 
препарат 
M.HC.CDE.00811 hccdo:DrugApplicationChangeDetails
Type (M.HC.CDT.00676) 
Определяется областями значений 
вложенных элементов 
0..*
