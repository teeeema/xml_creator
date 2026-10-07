---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 288
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

122 
 
Таблица 29 
Требования к заполнению реквизитов электронных документов 
(сведений) «Запрос сведений из национальных разделов Единого 
реестра НМПТ Союза» (R.IP.SP.03.007), передаваемых в сообщении 
«Запрос файла прилагаемого документа» (P.SP.03.MSG.025) 
Код 
требования 
Формулировка требования 
1 реквизиты «Дата и время обновления» (csdo:UpdateDateTime) 
и «Код страны» (csdo:UnifiedCountryCode) не заполняется 
2 если заполнен реквизит «Регистрационный номер заявки на НМПТ» 
Союза» (ipsdo:ApellationOfOriginApplicationId), реквизиты 
«Регистрационный номер НМПТ Союза» 
(ipsdo:ApellationOfOriginEAEUId), «Регистрационный номер 
свидетельства о праве использования НМПТ Союза» 
(ipsdo:ApellationOfOriginEAEUCertificateId) не заполняются 
3 если заполнен реквизит «Регистрационный номер свидетельства о праве 
использования НМПТ Союза» 
(ipsdo:ApellationOfOriginEAEUCertificateId), реквизиты 
«Регистрационный номер НМПТ Союза» 
(ipsdo:ApellationOfOriginEAEUId) и «Регистрационный номер заявки 
на НМПТ» Союза» (ipsdo:ApellationOfOriginApplicationId) 
не заполняются 
4 если заполнен реквизит «Регистрационный номер НМПТ Союза» 
(ipsdo:ApellationOfOriginEAEUId), реквизиты «Регистрационный номер 
свидетельства о праве использования НМПТ Союза» 
(ipsdo:ApellationOfOriginEAEUCertificateId) и «Регистрационный номер 
заявки на НМПТ» Союза» (ipsdo:ApellationOfOriginApplicationId) 
не заполняются 
5 в составе электронного документа (сведений) должен быть заполнен 
реквизит «Прилагаемый документ» 
(ipcdo:AccompanyingDocumentsDetails) 
6 в составе реквизита «Прилагаемый документ» 
(ipcdo:AccompanyingDocumentsDetails) реквизиты «Документ в бинарном 
формате» (csdo:DocBinaryText) и «Наименование вида документа, 
используемого в сфере интеллектуальной собственности» 
(ipsdo:IPDocKindName) не заполняются 
7 в составе реквизита «Прилагаемый документ» 
(ipcdo:AccompanyingDocumentsDetails) должен быть заполнены реквизит 
«Код вида документа, используемого в сфере интеллектуальной 
собственности» (ipsdo:IPDocKindCode)
