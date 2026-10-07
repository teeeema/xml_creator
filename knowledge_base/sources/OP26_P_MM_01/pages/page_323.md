---
source_document: "26_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/26_ОП.pdf"
source_sha256: "a15cc6c946b35145e58304b7e3621ea76241f510e2202bbaf8912b4f8b0715e6"
pdf_page: 323
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

322 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн.  
2. Сведения о регистрации 
лекарственного препарата 
(hccdo:DrugRegistrationDetails) 
сведения о регистрации 
лекарственного препарата 
M.HC.CDE.00028 hccdo:DrugRegistrationDetailsType 
(M.HC.CDT.00025) 
Определяется областями значений 
вложенных элементов 
1..* 
 2.1. Порядковый номер 
регистрационного удостоверения 
лекарственного препарата 
(hcsdo:RegistrationNumberId) 
порядковый номер 
регистрационного 
удостоверения лекарственного 
препарата 
M.HC.SDE.00672 hcsdo:RegistrationNumberIdType 
(M.HC.SDT.00629) 
Нормализованная строка символов. 
Шаблон: \d{6} 
0..1 
 2.2. Сведения о регистрации 
лекарственного препарата в 
государстве-члене 
(hccdo:DrugCountryRegistration
Details) 
сведения о регистрации 
лекарственного препарата в 
государстве-члене 
M.HC.CDE.00457 hccdo:DrugCountryRegistrationDetails
Type (M.HC.CDT.00457) 
Определяется областями значений 
вложенных элементов 
1..* 
 2.2.1. Код страны 
(csdo:UnifiedCountryCode) 
кодовое обозначение страны, в 
которой регистрируется 
лекарственный препарат 
M.SDE.00162 csdo:UnifiedCountryCodeType 
(M.SDT.00112) 
Значение двухбуквенного кода страны 
в соответствии со справочником 
(классификатором), идентификатор 
которого определен в атрибуте 
«Идентификатор справочника 
(классификатора)». 
Шаблон: [A-Z]{2} 
1
