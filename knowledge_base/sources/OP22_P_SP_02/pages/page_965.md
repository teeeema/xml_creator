---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 965
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

143 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
  2.15.6. Признак возможности 
регистрации товарного знака 
Союза 
(ipsdo:TrademarkDecision
Indicator) 
признак, определяющий 
возможность регистрации 
товарного знака Союза: 
1 – регистрация товарного знака 
Союза возможна; 
0 – регистрация товарного знака 
Союза не возможна 
M.IP.SDE.00167 bdt:IndicatorType (M.BDT.00013) 
Одно из двух значений: «true» 
(истина) или «false» (ложь) 
0..1 
  2.15.7. Регистрационный номер 
заявки на товарный знак Союза 
(ipsdo:TrademarkApplicationId) 
регистрационный номер заявки 
на ТЗ Союза, препятствующий 
регистрации ТЗ Союза  
в отношении товара (услуги) 
M.IP.SDE.00065 ipsdo:ApplicationIdType 
(M.IP.SDT.00016) 
Нормализованная строка символов. 
Шаблон: \d{4}/(AM|BY|KG|KZ|RU)-
\d{6} 
0..* 
  2.15.8. Регистрационный номер 
товарного знака Союза 
(ipsdo:TrademarkId) 
регистрационный номер ТЗ 
Союза, препятствующий 
регистрации ТЗ Союза  
в отношении товара (услуги) 
M.IP.SDE.00068 ipsdo:TrademarkCertificateIdType 
(M.IP.SDT.00504) 
Нормализованная строка символов. 
Шаблон: \d{4}/(AM|BY|KG|KZ|RU)-
\d{6} 
0..* 
  2.15.9. Регистрационный номер 
НМПТ Союза 
(ipsdo:ApellationOfOrigin
EAEUId) 
регистрационный номер НМПТ 
Союза, препятствующий 
регистрации ТЗ Союза  
в отношении товара (услуги) 
M.IP.SDE.00048 ipsdo:ApellationOfOriginEAEUIdType 
(M.IP.SDT.00500) 
Нормализованная строка символов. 
Шаблон: \d{4}/(AM|BY|KG|KZ|RU)-
\d{6} 
0..*
