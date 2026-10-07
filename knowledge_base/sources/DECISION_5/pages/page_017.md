---
source_document: "5 решение.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/5 решение.pdf"
source_sha256: "84987769629e0285eca4bad36f39f0e2fd38980301c0ecb21e2fbfa0447f5592"
pdf_page: 17
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

soap:Sender wsa:InvalidAddressingHeader 
используется согласно правилам, 
определенным спецификацией 
WS-Addressing 1.0–Binding, со 
следующими ограничениями: 
значения Subsubcode не 
используются ошибка типа 
wsa:DuplicateMessageID 
не формируется и не 
отправляется  
soap:Sender wsa:MessageAddressingHeaderRequired 
используется согласно правилам, 
определенным спецификацией 
WS-Addressing 1.0–Binding  
soap:Sender wsa:DestinationUnreachable 
используется согласно правилам, 
определенным спецификацией 
WS-Addressing 1.0–Binding  
soap:Sender wsa:ActionNotSupported 
используется согласно правилам, 
определенным спецификацией 
WS-Addressing 1.0–Binding  
soap:Sender int:InvalidHeader 
отсутствует один или несколько 
специализированных заголовков 
интегрированной системы  
soap:Receiver wsa:EndpointUnavailable 
используется согласно правилам, 
определенным спецификацией 
WS-Addressing 1.0–Binding, со 
следующим ограничением: при 
реализации электронного обмена 
данными в рамках общих 
процессов элемент wsa:RetryAfter 
использоваться не должен  
soap:Receiver int:InternalError 
при обработке сообщения 
произошла непредвиденная 
ошибка  
soap:Sender int:DataError 
полученные данные прикладного 
уровня имеют неверную 
структуру  
  
75. Элемент soap:Text должен содержать текстовое описание ошибки. 
Каждый элемент soap:Text должен содержать языковой идентификатор xml:lang, 
формируемый согласно спецификации XML 1.0. 
В случае если в технологическом сообщении об ошибке присутствует набор элементов 
soap:Text, каждый из указанных элементов должен содержать языковой идентификатор 
xml:lang, отличный от идентификаторов других элементов soap:Text. 
В технологическом сообщении об ошибке должен присутствовать хотя бы один элемент 
soap:Text, содержимое которого представлено на русском языке, а языковой идентификатор 
xml:lang должен содержать значение ru.
