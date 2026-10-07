---
source_document: "49_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/49_ОП.pdf"
source_sha256: "81f82f343650ea19bb293ef7f45d86c57e9195e0cef315e4d190ab47e6d8bae8"
pdf_page: 156
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

15 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
2. Код страны, предоставившей 
информацию 
(ds01sdo:ReportCountryCode) 
кодовое обозначение страны, 
предоставившей информацию 
M.DS.01.SDE.000
17 
csdo:UnifiedCountryCodeType 
(M.SDT.00112) 
Значение двухбуквенного кода из 
классификатора стран мира, 
определенного атрибутом 
«Идентификатор классификатора». 
Шаблон: [A-Z]{2} 
1 
 а) Идентификатор 
классификатора 
(атрибут codeListId) 
обозначение классификатора, в 
соответствии с которым указан 
код 
– csdo:ReferenceDataIdType 
(M.SDT.00091) 
Нормализованная строка символов, не 
содержащая символов разрыва строки 
(#xA) и табуляции (#x9). 
Мин. длина: 1. 
Макс. длина: 20 
1 
3. Отчет о зачислении и 
распределении сумм ввозных 
таможенных пошлин 
(ds01cdo:ChargedDistributedDuty
ReportDetails) 
информация из отчета о 
зачислении и распределении 
сумм ввозных таможенных 
пошлин 
M.DS.01.CDE.000
09 
ds01cdo:ChargedDistributedDutyReport
DetailsType (M.DS.01.CDT.00010) 
Определяется областями значений 
вложенных элементов 
1..*
