---
source_document: "ОП_22.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf"
source_sha256: "99b2e82a9eb65a5e996bee2200262623aead907e77db067c556f4e3575410bd3"
pdf_page: 881
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

59 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
 2.17. Признак согласия на 
обработку представленных 
сведений 
(ipsdo:ConsentToDataProcessing
Indicator) 
возможные значения элемента: 
0 – не дано согласие  
на обработку сведений; 
1 – дано согласие на обработку 
сведений 
M.IP.SDE.00501 bdt:IndicatorType (M.BDT.00013) 
Одно из двух значений: «true» 
(истина) или «false» (ложь) 
0..1 
 2.18. Сведения о подписании 
документа 
(ipcdo:SignatureDetails) 
информация о подписании 
документа 
M.IP.CDE.00500 ipcdo:SignatureDetailsType 
(M.IP.CDT.00501) 
Определяется областями значений 
вложенных элементов 
0..* 
  2.18.1. Дата документа 
(csdo:DocCreationDate) 
дата подписания документа M.SDE.00045 bdt:DateType (M.BDT.00005) 
Обозначение даты в соответствии  
с ISO 8601 
1 
  2.18.2. Сотрудник организации 
(ipcdo:OfficerDetails) 
информация о сотруднике 
организации, уполномоченном 
на подписание документа 
M.IP.CDE.00039 ccdo:OfficerDetailsType 
(M.CDT.00031) 
Определяется областями значений 
вложенных элементов 
0..* 
   *.1. ФИО 
(ccdo:FullNameDetails) 
фамилия, имя, отчество M.CDE.00029 ccdo:FullNameDetailsType 
(M.CDT.00016) 
Определяется областями значений 
вложенных элементов 
1 
    *.1.1. Имя 
(csdo:FirstName) 
имя физического лица M.SDE.00109 csdo:Name120Type (M.SDT.00055) 
Нормализованная строка символов. 
Мин. длина: 1. 
Макс. длина: 120 
0..1
