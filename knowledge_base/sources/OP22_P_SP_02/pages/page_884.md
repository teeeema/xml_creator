---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 884
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

62 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
 2.19. Вид регистрации ТЗ 
(ipsdo:TrademarkRegistrationCode) 
код вида решения о регистрации 
или об отказе в регистрации 
товарного знака Союза 
M.IP.SDE.00510 ipsdo:TrademarkRegistrationCodeType 
(M.IP.SDT.00507) 
Нормализованная строка символов. 
Шаблон: \d{2} 
0..1 
 2.20. Национальная заявка на 
регистрацию товарного знака 
(ipcdo:TrademarkNational
ApplicationDetails) 
сведения о национальной заявке 
на регистрацию товарного знака 
M.IP.CDE.00111 ipcdo:TrademarkNationalApplication
DetailsType (M.IP.CDT.00179) 
Определяется областями значений 
вложенных элементов 
0..* 
  2.20.1. Код страны 
(csdo:UnifiedCountryCode) 
страна регистрации 
национальной заявки 
M.SDE.00162 csdo:UnifiedCountryCodeType 
(M.SDT.00112) 
Значение двухбуквенного кода страны 
в соответствии со справочником 
(классификатором), идентификатор 
которого определен в атрибуте 
«Идентификатор справочника 
(классификатора)». 
Шаблон: [A-Z]{2} 
0..1 
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
  2.20.2. Номер национальной 
заявки 
(ipsdo:NationalApplicationId) 
регистрационный номер заявки 
в национальном реестре 
товарных знаков 
M.IP.SDE.00138 csdo:Id20Type (M.SDT.00092) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 20 
0..1
