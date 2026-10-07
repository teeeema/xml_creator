---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 480
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

80 
 
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
  2.8.2. Регистрационный номер 
НМПТ Союза 
(ipsdo:ApellationOfOrigin
EAEUId) 
регистрационный номер НМПТ, 
присвоенный ведомством 
подачи 
M.IP.SDE.00048 ipsdo:ApellationOfOriginEAEUIdType 
(M.IP.SDT.00500) 
Нормализованная строка символов. 
Шаблон: \d{4}/(AM|BY|KG|KZ|RU)-
\d{6} 
0..1 
  2.8.3. Дата регистрации объекта 
интеллектуальной 
собственности 
(ipsdo:RegistrationDate) 
дата регистрации НМПТ Союза 
ведомством подачи 
M.IP.SDE.00058 bdt:DateType (M.BDT.00005) 
Обозначение даты в соответствии  
с ISO 8601 
0..1 
  2.8.4. Дата опубликования 
сведений об объекте 
интеллектуальной 
собственности 
(ipsdo:PublicationDate) 
дата опубликования сведений  
о НМПТ Союза ведомством 
подачи 
M.IP.SDE.00503 bdt:DateType (M.BDT.00005) 
Обозначение даты в соответствии  
с ISO 8601 
0..1
