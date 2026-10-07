---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 469
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

69 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн. 
   а) код формата данных 
(атрибут mediaTypeCode) 
кодовое обозначение формата 
данных 
– csdo:MediaTypeCodeType 
(M.SDT.00147) 
Значение кода в соответствии со 
справочником форматов данных. 
Мин. длина: 1. 
Макс. длина: 255 
0..1 
 2.15. Признак согласия на 
обработку представленных 
сведений 
(ipsdo:ConsentToDataProcessing
Indicator) 
возможные значения элемента: 
0 – не дано согласие на 
обработку сведений; 
1 – дано согласие на обработку 
сведений 
M.IP.SDE.00501 bdt:IndicatorType (M.BDT.00013) 
Одно из двух значений: «true» 
(истина) или «false» (ложь) 
0..1 
 2.16. Сведения о подписании 
документа 
(ipcdo:SignatureDetails) 
совокупность сведений  
о подписании документа 
M.IP.CDE.00500 ipcdo:SignatureDetailsType 
(M.IP.CDT.00501) 
Определяется областями значений 
вложенных элементов 
0..* 
  2.16.1. Дата документа 
(csdo:DocCreationDate) 
дата подписания документа M.SDE.00045 bdt:DateType (M.BDT.00005) 
Обозначение даты в соответствии с 
ISO 8601 
1 
  2.16.2. Сотрудник организации 
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
