---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 977
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

155 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
   *.2. Код вида решения по 
аннулированию регистрации 
товарного знака Союза 
(ipsdo:SolutionCancellation
RegistrationTrademarkCode) 
признак решения по 
аннулированию регистрации 
товарного знака Союза 
M.IP.SDE.00525 ipsdo:SolutionCancellationRegistration
TrademarkCodeType (M.IP.SDT.00514) 
Нормализованная строка символов. 
Шаблон: \d{2} 
0..1 
   *.3. Новый регистрационный 
номер товарного знака Союза 
(ipsdo:TrademarkNewId) 
новый регистрационный номер 
товарного знака Союза, который 
является номером свидетельства 
на товарный знак Союза  
в отношении части товаров 
M.IP.SDE.00526 ipsdo:TrademarkCertificateIdType 
(M.IP.SDT.00504) 
Нормализованная строка символов. 
Шаблон: \d{4}/(AM|BY|KG|KZ|RU)-
\d{6} 
0..1 
   *.4. Сведения о заявителе 
(ipcdo:ApplicantV2Details) 
сведения о заинтересованном 
лице или заявителе, подавшем 
обращение 
M.IP.CDE.00509 ipcdo:ApplicantV2DetailsType 
(M.IP.CDT.00509) 
Определяется областями значений 
вложенных элементов 
1 
    *.4.1. Наименование 
организации 
(csdo:OrganizationName) 
полное наименование 
юридического лица согласно 
учредительному документу 
M.SDE.00022 csdo:Name300Type (M.SDT.00056) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 300 
0..* 
    *.4.2. Код страны 
(csdo:CountryCode) 
кодовое обозначение страны M.SDE.00001 csdo:CountryCodeType (M.SDT.00001) 
Значение двухбуквенного кода  
в соответствии с классификатором 
стран мира, применяемым согласно 
Решению Комиссии Таможенного 
союза от 20 сентября 2010 г. № 378. 
Шаблон: [A-Z]{2} 
0..1
