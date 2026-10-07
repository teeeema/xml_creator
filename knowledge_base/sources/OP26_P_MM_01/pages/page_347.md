---
source_document: "26_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/26_ОП.pdf"
source_sha256: "a15cc6c946b35145e58304b7e3621ea76241f510e2202bbaf8912b4f8b0715e6"
pdf_page: 347
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

346 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн.  
 *.2. Наименование 
лекарственной формы 
(hcsdo:DosageFormName) 
наименование лекарственной 
формы 
M.HC.SDE.00874 csdo:Name500Type (M.SDT.00134) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 500 
0..1 
 *.3. Дополнительные признаки 
лекарственной формы 
(hccdo:DosageFormAdditional
FeaturesDetails) 
сведения о дополнительных 
признаках лекарственной 
формы 
M.HC.CDE.00325 hccdo:DosageFormAdditionalFeatures
DetailsType (M.HC.CDT.00587) 
Определяется областями значений 
вложенных элементов 
0..1 
 *.3.1. Признак дозированности 
лекарственной формы 
(hcsdo:DosedIndicator) 
признак, определяющий 
дозированность лекарственной 
формы: 1 – лекарственная 
форма дозирована; 0 –
 лекарственная форма не 
дозирована 
M.HC.SDE.00243 bdt:IndicatorType (M.BDT.00013) 
Одно из двух значений: «true» 
(истина) или «false» (ложь) 
0..1 
 *.3.2. Признак применимости 
лекарственного препарата у 
детей 
(hcsdo:ChildIndicator) 
признак, определяющий 
применимость лекарственного 
препарата у детей: 1 –
 применяется у детей; 0 – не 
применяется у детей 
M.HC.SDE.00244 bdt:IndicatorType (M.BDT.00013) 
Одно из двух значений: «true» 
(истина) или «false» (ложь) 
0..1
