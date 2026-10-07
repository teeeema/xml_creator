---
source_document: "26_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/26_ОП.pdf"
source_sha256: "a15cc6c946b35145e58304b7e3621ea76241f510e2202bbaf8912b4f8b0715e6"
pdf_page: 340
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

339 
 
Имя реквизита Описание реквизита Идентификатор Тип данных Мн.  
 *.3. Сведения о макете упаковки 
лекарственного препарата 
(hccdo:DrugPackageLayout
Details) 
сведения о макете упаковки 
лекарственного препарата 
M.HC.CDE.00413 hccdo:DrugPackageLayoutDetailsType 
(M.HC.CDT.00280) 
Определяется областями значений 
вложенных элементов 
0..* 
 *.3.1. Порядковый номер 
(csdo:ObjectOrdinal) 
порядковый номер фрагмента 
документа 
M.SDE.00148 csdo:Ordinal3Type (M.SDT.00105) 
Целое неотрицательное число в 
десятичной системе счисления. 
Макс.кол-во цифр: 3 
0..1 
 *.3.2. Код вида макета 
упаковки лекарственного 
препарата 
(hcsdo:DrugPackageLayoutKind
Code) 
кодовое обозначение вида 
макета упаковки лекарственного 
препарата 
M.HC.SDE.00629 hcsdo:DrugPackageLayoutKindCode
Type (M.HC.SDT.00628) 
Нормализованная строка символов 
1 
 *.3.3. Дата документа 
(csdo:DocCreationDate) 
дата подписания, утверждения 
или регистрации документа 
M.SDE.00045 bdt:DateType (M.BDT.00005) 
Обозначение даты в соответствии с 
ГОСТ ИСО 8601–2001 
0..1 
 *.3.4. Документ в формате 
PDF 
(hcsdo:PdfBinaryText) 
документ в формате PDF M.HC.SDE.00326 csdo:BinaryTex tType (M.SDT.00143) 
Конечная последовательность 
двоичных октетов (байтов) 
0..1
