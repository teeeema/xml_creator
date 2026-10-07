---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 484
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

84 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
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
 2.9. Сведения о праве 
использования НМПТ Союза 
(ipcdo:ApellationOfOrigin
EAEURightDetails) 
сведения о праве использования 
НМПТ Союза, предоставляемые 
согласно соответствующему 
свидетельству 
M.IP.CDE.00502 ipcdo:ApellationOfOriginEAEURight
DetailsType (M.IP.CDT.00502) 
Определяется областями значений 
вложенных элементов 
0..1 
  2.9.1. Регистрационный номер 
свидетельства о праве 
использования НМПТ Союза 
(ipsdo:ApellationOfOrigin
EAEUCertificateId) 
регистрационный номер 
свидетельства о праве 
использования НМПТ Союза, 
присвоенный ведомством 
подачи 
M.IP.SDE.00504 ipsdo:ApellationOfOrigin
EAEUCertificateIdType 
(M.IP.SDT.00505) 
Нормализованная строка символов. 
Шаблон: \d{4}/(AM|BY|KG|KZ|RU)-
\d{6}/\d{2} 
0..1 
  2.9.2. Дата истечения срока 
действия документа 
(csdo:DocValidityDate) 
дата истечения срока действия 
свидетельства о праве 
использования НМПТ Союза 
M.SDE.00052 bdt:DateType (M.BDT.00005) 
Обозначение даты в соответствии  
с ISO 8601 
0..1
