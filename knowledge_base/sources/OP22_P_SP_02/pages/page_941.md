---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 941
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

119 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
   *.9. Номер дома 
(csdo:BuildingNumberId) 
обозначение дома, корпуса, 
строения 
M.SDE.00011 csdo:Id50Type (M.SDT.00093) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 50 
0..1 
   *.10. Номер помещения 
(csdo:RoomNumberId) 
обозначение офиса или 
квартиры 
M.SDE.00012 csdo:Id20Type (M.SDT.00092) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 20 
0..1 
   *.11. Почтовый индекс 
(csdo:PostCode) 
почтовый индекс предприятия 
почтовой связи 
M.SDE.00006 csdo:PostCodeType (M.SDT.00006) 
Нормализованная строка символов. 
Шаблон: [A-Z0-9][A-Z0-9 -]{1,8}[A-
Z0-9] 
0..1 
   *.12. Номер абонентского 
ящика 
(csdo:PostOfficeBoxId) 
номер абонентского ящика на 
предприятии почтовой связи 
M.SDE.00013 csdo:Id20Type (M.SDT.00092) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 20 
0..1 
  2.11.6. Признак ведомства 
подачи 
(ipsdo:OriginOfficeIndicator) 
признак, определяющий, 
является ли национальное 
патентное ведомство 
ведомством подачи 
M.IP.SDE.00523 bdt:IndicatorType (M.BDT.00013) 
Одно из двух значений: «true» 
(истина) или «false» (ложь) 
1 
 2.12. Адрес для переписки 
(ipcdo:CorrespondenceAddress
Details) 
информация об адресе для 
переписки 
M.IP.CDE.00007 ipcdo:CorrespondenceAddressDetails
Type (M.IP.CDT.00005) 
Определяется областями значений 
вложенных элементов 
0..1
