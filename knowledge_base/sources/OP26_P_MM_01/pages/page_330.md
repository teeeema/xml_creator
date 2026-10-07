---
source_document: "26_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/26_ОП.pdf"
source_sha256: "a15cc6c946b35145e58304b7e3621ea76241f510e2202bbaf8912b4f8b0715e6"
pdf_page: 330
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

329 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн.  
 *.9. Признак выдачи нового 
регистрационного 
удостоверения 
(hcsdo:NewRegistration
CertificateIndicator) 
признак, определяющий выдачу 
нового регистрационного 
удостоверения: 1 – выдано 
новое регистрационное 
удостоверение; 0 – не выдано 
новое регистрационное 
удостоверение 
M.HC.SDE.00523 bdt:IndicatorType (M.BDT.00013) 
Одно из двух значений: «true» 
(истина) или «false» (ложь) 
0..1 
 *.10. Дата 
(csdo:EventDate) 
дата подтверждения 
регистрации (перерегистрации) 
M.SDE.00131 bdt:DateType (M.BDT.00005) 
Обозначение даты в соответствии с 
ГОСТ ИСО 8601–2001 
0..1 
 *.11. Сведения об особом 
условии регистрации 
лекарственного препарата 
(hccdo:DrugRegistrationSpecial
ConditionDetails) 
сведения об особом условии 
регистрации лекарственного 
препарата 
M.HC.CDE.00404 hccdo:DrugRegistrationSpecial
ConditionDetailsType 
(M.HC.CDT.00505) 
Определяется областями значений 
вложенных элементов 
0..* 
 *.11.1. Код вида особого 
условия регистрации 
лекарственного препарата 
(hcsdo:DrugUsageRestriction
KindCode) 
кодовое обозначение вида 
особого условия регистрации 
лекарственного препарата 
M.HC.SDE.00598 hcsdo:DrugUsageRestrictionKindCode
Type (M.HC.SDT.00099) 
Нормализованная строка символов 
0..1 
 *.11.2. Наименование вида 
особого условия регистрации 
лекарственного препарата 
(hcsdo:DrugUsageRestriction
KindName) 
наименование вида особого 
условия регистрации 
лекарственного препарата 
M.HC.SDE.00772 csdo:Name500Type (M.SDT.00134) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 500 
0..1
