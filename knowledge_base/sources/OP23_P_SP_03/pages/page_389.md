---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 389
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

100 
 
Код 
требования 
Формулировка требования 
30 если реквизит «Код страны» (csdo:UnifiedCountryCode) заполнен 
в составе любых реквизитов, в его составе значение атрибута 
«идентификатор справочника (классификатора)» (атрибут codeListId) 
должно соответствовать значению «ВОИС ST.3» 
31 в составе любых экземпляров реквизита «Сведения записи Единого 
реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails) 
реквизит «Прилагаемый документ» 
(ipcdo:AccompanyingDocumentsDetails) не заполняется 
32 в составе реквизита «Сведения о статусном состоянии» 
(ipcdo:IPStatusDetails) должны быть заполнены реквизиты: 
«Дата» (csdo:EventDate); 
«Номер документа» (csdo:DocId); 
«Дата поступления документа» (ipsdo:IPDocReceiptDate); 
«Описание» (csdo:DescriptionText) 
33 если в экземплярах реквизита «Сведения записи Единого реестра НМПТ 
Союза» (ipcdo:ApellationOfOriginRegisterItemDetails) значение реквизита 
«Код вида записи общего информационного ресурса» 
(ipsdo:ResourceItemKindCode) соответствует значению «RH» – «сведения 
о праве использования НМПТ Союза», то в составе экземпляра реквизита 
«Сведения записи Единого реестра НМПТ Союза» 
(ipcdo:ApellationOfOriginRegisterItemDetails), содержащего измененные 
сведения Единого реестра НМПТ Союза, в составе реквизита «Сведения 
о статусном состоянии» (ipcdo:IPEntityStatusDetails) реквизит «Дата» 
(csdo:EventDate) должен быть заполнен, значение реквизита «Код 
статуса» (csdo:StatusCode) должно соответствовать значению 
«11» – «право использования НМПТ Союза действует (внесены 
изменения)», а атрибут «идентификатор справочника (классификатора)» 
(атрибут codeListId) в составе реквизита «Код статуса» (csdo:StatusCode) 
не заполняется
