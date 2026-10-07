---
source_document: "5 решение.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/5 решение.pdf"
source_sha256: "84987769629e0285eca4bad36f39f0e2fd38980301c0ecb21e2fbfa0447f5592"
pdf_page: 49
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

4. Структура и реквизитный состав сигнала -подтверждения "Принято в обработку" 
приведены в таблице 4. 
  
  
Таблица 4 
   
СТРУКТУРА И РЕКВИЗИТНЫЙ СОСТАВ  
СИГНАЛА-ПОДТВЕРЖДЕНИЯ "ПРИНЯТО В ОБРАБОТКУ" 
   
Элемент  Тип данных  Описание  Кратность  
sgn:ProcessingReceipt  sgn:ProcessingReceiptType  
оборачивающий элемент 
сигнала-подтверждения 
"Принято в обработку"  
   
   sgn:SignalId  sgn:EDocIdType  идентификатор сигнала  1  
   sgn:DateTime  sgn:DateTimeType  
дата и время 
формирования сигнала-
подтверждения "Принято 
в обработку"  
1  
  
5. Структура и реквизитный состав сигнала-исключения "Ошибка" приведены в таблице 5. 
  
  
Таблица 5 
   
СТРУКТУРА И РЕКВИЗИТНЫЙ СОСТАВ  
СИГНАЛА-ИСКЛЮЧЕНИЯ "ОШИБКА" 
   
Элемент  Тип данных  Описание  Кратность  
sgn:ValidationError  sgn:ValidationErrorType  
оборачивающий элемент 
сигнала-исключения 
"Ошибка"  
   
   sgn:SignalId  sgn:EDocIdType  идентификатор сигнала-
исключения "Ошибка"  1  
   sgn:DateTime  sgn:DateTimeType  
дата и время 
формирования сигнала-
исключения "Ошибка"  
1  
   sgn:Error  sgn:ErrorType  оборачивающий элемент  1..*  
      sgn:Code  sgn:ErrorCodeType  кодовое обозначение 
ошибки  1  
      sgn:Description  sgn:StringType  обозначение ошибки в 
текстовой форме  1  
      sgn:Details  sgn:StringType  детализированные 
сведения об ошибке  0..1
