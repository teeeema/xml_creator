---
source_document: "26_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/26_ОП.pdf"
source_sha256: "a15cc6c946b35145e58304b7e3621ea76241f510e2202bbaf8912b4f8b0715e6"
pdf_page: 402
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

401 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн.  
 2.5.8. Идентификатор 
налогоплательщика 
(csdo:TaxpayerId) 
идентификатор хозяйствующего 
субъекта в реестре 
налогоплательщиков страны 
регистрации налогоплательщика 
M.SDE.00025 csdo:TaxpayerIdType (M.SDT.00025) 
Значение идентификатора в 
соответствии с правилами, принятыми 
в стране регистрации 
налогоплательщика. 
Мин. длина: 1. 
Макс. длина: 20 
0..1 
 2.5.9. Код причины постановки на 
учет 
(csdo:TaxRegistrationReasonCode) 
код, идентифицирующий 
причину постановки 
хозяйствующего субъекта на 
налоговый учет в Российской 
Федерации 
M.SDE.00030 csdo:TaxRegistrationReasonCodeType 
(M.SDT.00030) 
Нормализованная строка символов. 
Шаблон: \d{9} 
0..1 
 2.5.10. Адрес 
(ccdo:AddressV4Details) 
адрес хозяйствующего субъекта M.CDE.00076 ccdo:Addre ssDetailsV4Type 
(M.CDT.00079) 
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
кодовое обозначение страны M.SDE.00162 csdo:Unified CountryCodeType 
(M.SDT.00112) 
Значение двухбуквенного кода страны 
0..1
