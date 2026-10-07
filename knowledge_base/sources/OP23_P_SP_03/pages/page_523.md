---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 523
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

123 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
  2.12.1. Наименование субъекта 
(csdo:SubjectName) 
наименование или фамилия, 
имя, отчество (при наличии) 
адресата 
M.SDE.00224 csdo:Name300Type (M.SDT.00056) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 300 
0..1 
  2.12.2. Адрес 
(ccdo:SubjectAddressDetails) 
адрес для ведения переписки M.CDE.00058 ccdo:SubjectAddressDetailsType 
(M.CDT.00064) 
Определяется областями значений 
вложенных элементов 
0..* 
   *.1. Код вида адреса 
(csdo:AddressKindCode) 
кодовое обозначение вида 
адреса 
M.SDE.00192 csdo:AddressKindCodeType 
(M.SDT.00162) 
Значение кода в соответствии со 
справочником видов адресов. 
Мин. длина: 1. 
Макс. длина: 20 
0..1 
   *.2. Код страны 
(csdo:UnifiedCountryCode) 
кодовое обозначение страны M.SDE.00162 csdo:UnifiedCountryCodeType 
(M.SDT.00112) 
Значение двухбуквенного кода страны 
в соответствии со справочником 
(классификатором), идентификатор 
которого определен в атрибуте 
«Идентификатор справочника 
(классификатора)». 
Шаблон: [A-Z]{2} 
0..1
