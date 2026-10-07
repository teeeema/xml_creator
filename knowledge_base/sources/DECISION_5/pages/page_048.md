---
source_document: "5 решение.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/5 решение.pdf"
source_sha256: "84987769629e0285eca4bad36f39f0e2fd38980301c0ecb21e2fbfa0447f5592"
pdf_page: 48
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

2. При описании структуры и реквизитного состава сигналов-подтверждений и сигналов-
исключений используются базовые типы данных, приведенные в таблице 2. 
  
  
Таблица 2 
   
БАЗОВЫЕ ТИПЫ ДАННЫХ 
   
Наименование  Описание  
sgn:EDocIdType 
идентификатор документа, являющийся UUID в соответствии 
со стандартом ISO/IEC 9834-8:2005. Строка символов с 
шаблоном [0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-
fA-F]{4}-[0-9a-fA-F]{12}  
sgn:DateTimeType 
дата по григорианскому календарю и время в формате 
стандарта ISO 8601 "Dataelements and interchange formats – 
Information interchange – Representation of dates and types"  
sgn:ErrorCodeType кодовое обозначение ошибки контроля. Строка от 1 до 255 
символов  
sgn:StringType произвольная информация в текстовой форме. Строка 
произвольной длины  
  
3. Структура и реквизитный состав сигнала -подтверждения"Получено" приведены в 
таблице 3. 
  
  
Таблица 3 
   
СТРУКТУРА И РЕКВИЗИТНЫЙ СОСТАВ СИГНАЛА-ПОДТВЕРЖДЕНИЯ 
"ПОЛУЧЕНО" 
   
Элемент  Тип данных  Описание  Кратность  
sgn:DeliveryReceipt  sgn:DeliveryReceiptType  
оборачивающий 
элемент сигнала-
подтверждения 
"Получено"  
   
   sgn:SignalId  sgn:EDocIdType  идентификатор сигнала  1  
   sgn:DateTime  sgn:DateTimeType  
дата и время 
формирования 
сигнала-
подтверждения 
"Получено"  
1
