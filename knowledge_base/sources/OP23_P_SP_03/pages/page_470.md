---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 470
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

70 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
    *.1.1. Имя 
(csdo:FirstName) 
имя физического лица M.SDE.00109 csdo:Name120Type (M.SDT.00055) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 120 
0..1 
    *.1.2. Отчество 
(csdo:MiddleName) 
отчество (второе или среднее 
имя) физического лица 
M.SDE.00111 csdo:Name120Type (M.SDT.00055) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 120 
0..1 
    *.1.3. Фамилия 
(csdo:LastName) 
фамилия физического лица M.SDE.00110 csdo:Name120Type (M.SDT.00055) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 120 
0..1 
   *.2. Наименование 
должности 
(csdo:PositionName) 
наименование должности 
сотрудника 
M.SDE.00127 csdo:Name120Type (M.SDT.00055) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 120 
0..1 
   *.3. Контактный реквизит 
(ccdo:CommunicationDetails) 
контактный реквизит 
должностного лица 
M.CDE.00003 ccdo:CommunicationDetailsType 
(M.CDT.00003) 
Определяется областями значений 
вложенных элементов 
0..*
