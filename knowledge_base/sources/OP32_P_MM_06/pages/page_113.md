---
source_document: "32_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/32_ОП.pdf"
source_sha256: "db38b2912b9db998ffbad6775674428d878f47917f8d9faeaeed9ccfb73c0901"
pdf_page: 113
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

22  
если реквизит "Сведения о регистрационном удостоверении 
медицинского изделия" 
(hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то 
реквизит "Код класса потенциального риска медицинского изделия" 
(hcsdo:RiskClassCode) заполняется обязательно  
23  
если реквизит "Сведения о регистрационном удостоверении 
медицинского изделия" 
(hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то 
реквизит "Инструкция по применению медицинского изделия" 
(hcsdo:UserGuidePdfBinaryText) заполняется обязательно  
24  
если реквизит "Сведения о регистрационном удостоверении 
медицинского изделия" 
(hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то 
реквизит "Изображение маркировки медицинского изделия" 
(hcsdo:ImageMarkingPdfBinaryText) заполняется обязательно  
25  
если значение реквизита "Код статуса регистрационного 
удостоверения медицинского изделия" 
(hcsdo:MedicalProductRegistrationCertificateStatusCode) не 
соответствует значению "действует", то реквизит "Дата" 
(csdo:EventDate) в составе реквизита "Сведения о регистрационном 
удостоверении медицинского изделия" 
(hccdo:MedicalProductRegistrationCertificateDetails) заполняется 
обязательно  
26  
если реквизит "Сведения о регистрационном удостоверении 
медицинского изделия" 
(hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то в 
составе реквизита "Сведения о производителе медицинского изделия" 
(hccdo:MedicalProductManufacturingAuthorizationHolderDetails) 
реквизит "Наименование хозяйствующего субъекта" 
(csdo:BusinessEntityName) заполняется обязательно  
27  
если значение реквизита "Код статуса регистрационного 
удостоверения медицинского изделия" 
(hcsdo:MedicalProductRegistrationCertificateStatusCode) не равно 
значению "аннулировано", то реквизит "Дата истечения срока 
действия документа" (csdo:DocValidityDate) не заполняется  
28  
если реквизит "Сведения о регистрационном удостоверении 
медицинского изделия" 
(hccdo:MedicalProductRegistrationCertificateDetails) заполнен, то 
должен быть заполнен один из реквизитов "Код статуса 
регистрационного удостоверения медицинского изделия" 
(hcsdo:MedicalProductRegistrationCertificateStatusCode) или 
"Наименование статуса регистрационного удостоверения 
медицинского изделия" 
(hcsdo:MedicalProductRegistrationCertificateStatusName)  
29  
в сведениях о регистрации медицинских изделий, хранящихся в 
Комиссии, должны содержаться сведения с таким же значением 
реквизита "Номер заявления на регистрацию медицинского изделия" 
(hcsdo:MedicalProductApplicationId), в которых реквизит "Конечная 
дата и время" (csdo:EndDateTime) не заполнен, а также меньшим 
значением реквизита "Начальная дата и время" (csdo:StartDateTime)
