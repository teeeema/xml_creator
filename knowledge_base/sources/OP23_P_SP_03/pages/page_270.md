---
source_document: "ОП_23.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf"
source_sha256: "438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d"
pdf_page: 270
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

104 
 
Код 
требования 
Формулировка требования 
национальной регистрации НМПТ» 
(ipcdo:ApellationOfOriginNationalRegistrationDetails), то для каждого 
такого экземпляра реквизита «Сведения о национальной регистрации 
НМПТ» (ipcdo:ApellationOfOriginNationalRegistrationDetails) должно 
выполняться правило: в информационных ресурсах национального 
патентного ведомства, содержащих сведения о НМПТ, 
зарегистрированных до вступления в силу Договора, должна 
содержаться запись, в составе которой значение реквизита «Код вида 
записи общего информационного ресурса» (ipsdo:ResourceItemKindCode) 
соответствует значению «RN» – «сведения о праве использования 
национального НМПТ», «Код статуса» (csdo:StatusCode) соответствует 
значению «31» – «предоставлено право использования НМПТ Союза», 
реквизит «Конечная дата и время» (csdo:EndDateTime) в составе 
реквизита «Технологические характеристики записи общего ресурса» 
(ccdo:ResourceItemStatusDetails) не заполнен, а совокупность значений 
реквизитов «Код страны» (csdo:UnifiedCountryCode) и 
«Регистрационный номер свидетельства» (ipsdo:CertificateId) в составе 
реквизита «Сведения о национальной регистрации НМПТ» 
(ipcdo:ApellationOfOriginNationalRegistrationDetails) совпадает со 
значением соответствующих реквизитов в составе представляемых 
сведений 
25 в составе любых экземпляров реквизита «Сведения записи Единого 
реестра НМПТ Союза» (ipcdo:ApellationOfOriginRegisterItemDetails) 
в составе реквизита «Национальное патентное ведомство» 
(ipcdo:PatentAuthorityDetails) должны быть заполнены реквизиты: 
«Код страны» (csdo:UnifiedCountryCode); 
«Наименование уполномоченного органа» (csdo:AuthorityName); 
«Адрес» (ccdo:SubjectAddressDetails), в составе которого значение 
реквизита «Код вида адреса» (csdo:AddressKindCode) должно 
соответствовать значению «2» – «фактический адрес (адрес места 
нахождения или места жительства)» 
26 значение реквизита «Признак ведомства подачи»  
(ipsdo:OriginOfficeIndicator) в составе реквизита «Национальное 
патентное ведомство» (ipcdo:PatentAuthorityDetails) должно 
соответствовать значению «1» – ведомство подачи 
27 если реквизит « Адрес» (ccdo:SubjectAddressDetails) заполнен в составе 
любых реквизитов, в его составе должны быть заполнены реквизиты 
«Код вида адреса» (csdo:AddressKindCode)», «Код страны» 
(csdo:UnifiedCountryCode), «Город» (csdo:CityName), «Улица» 
(csdo:StreetName) и «Номер дома» (csdo:BuildingNumberId)
