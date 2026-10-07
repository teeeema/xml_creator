---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 447
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

47 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
    а) идентификатор 
справочника 
(классификатора) 
(атрибут codeListId) 
обозначение справочника 
(классификатора),  
в соответствии с которым 
указан код 
– csdo:ReferenceDataIdType 
(M.SDT.00091) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 20 
1 
   *.2. Описание 
географического объекта или 
его границ 
(ipsdo:GeographicRegion
DescriptionText) 
описание места происхождения 
(производства) товара (границ 
географического объекта, для 
которого характерны 
определенные природные 
условия и (или) людские 
факторы) 
M.IP.SDE.00023 ipsdo:GeographicRegionDescriptionText
Type (M.IP.SDT.00503) 
Строка символов. 
Мин. длина: 1. 
Макс. длина: 4000 
1 
    а) код вида описания 
географического объекта 
(атрибут geographicRegion
DescriptionKindCode) 
кодовое обозначение вида 
описания географического 
объекта 
– csdo:Code2Type (M.SDT.00170) 
Нормализованная строка символов. 
Длина: 2 
0..1 
 2.12. Сведения о национальной 
регистрации НМПТ 
(ipcdo:ApellationOfOriginNational
RegistrationDetails) 
информация о национальной 
регистрации НМПТ 
M.IP.CDE.00131 ipcdo:ApellationOfOriginNational
RegistrationDetailsType 
(M.IP.CDT.00223) 
Определяется областями значений 
вложенных элементов 
0..*
