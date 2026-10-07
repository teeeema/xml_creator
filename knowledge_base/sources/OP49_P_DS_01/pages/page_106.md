---
source_document: "49_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/49_ОП.pdf"
source_sha256: "81f82f343650ea19bb293ef7f45d86c57e9195e0cef315e4d190ab47e6d8bae8"
pdf_page: 106
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

53 
 
Код требования Формулировка требования 
 
22 
 
если существует реквизит «Сведения о суммах распределенных ввозных 
таможенных пошлин, перечисленных на счета» 
(ds01cdo:TransferDistributedDutyDetails), имеющий индикатор «Признак 
общей суммы» (ds01sdo:TotalAmountIndicator) со значением «1», то должен 
быть хотя бы один реквизит «Сведения о суммах распределенных ввозных 
таможенных пошлин, перечисленных на счета» 
(ds01cdo:TransferDistributedDutyDetails), имеющий индикатор «Признак 
общей суммы» (ds01sdo:TotalAmountIndicator) со значением «0» 
 
23 
 
для реквизита «Сведения о суммах распределенных ввозных таможенных 
пошлин, перечисленных на счета» (ds01cdo:TransferDistributedDutyDetails), 
имеющего индикатор «Признак общей суммы» 
(ds01sdo:TotalAmountIndicator) со значением «1», не должно быть заполнено 
значение реквизита «Код страны» (csdo:CountryCode) 
 
24 
 
для реквизита «Сведения о суммах распределенных ввозных таможенных 
пошлин, перечисленных на счета» (ds01cdo:TransferDistributedDutyDetails), 
имеющего индикатор «Признак общей суммы» 
(ds01sdo:TotalAmountIndicator) со значением «0», должно быть заполнено 
значение реквизита «Код страны» (csdo:CountryCode) 
 
25 
 
если для реквизита «Сведения о суммах распределенных ввозных 
таможенных пошлин, перечисленных на счета» 
(ds01cdo:TransferDistributedDutyDetails) реквизит «Признак общей суммы» 
(ds01sdo:TotalAmountIndicator) имеет значение «1», то значение реквизита 
«Суммы распределенных ввозных таможенных пошлин, перечисленные на 
счет» (ds01sdo:TransferDistributedDutyAmount) должно быть равно сумме 
всех значений реквизитов «Суммы распределенных ввозных таможенных 
пошлин, перечисленные на счет» (ds01sdo:TransferDistributedDutyAmount), 
указанных в реквизите «Сведения о суммах распределенных ввозных 
таможенных пошлин, перечисленных на счета» 
(ds01cdo:TransferDistributedDutyDetails) с индикатором «Признак общей 
суммы» (ds01sdo:TotalAmountIndicator) со значением «0» 
 
26 
 
для реквизита «Суммы распределенных ввозных таможенных пошлин, 
перечисленные на счет» (ds01sdo:TransferDistributedDutyAmount) значение 
атрибута «Код валюты» (атрибут currencyCode) должно соответствовать 
буквенному коду валюты того государства-члена, код которого указан в 
реквизите «Код страны, предоставившей информацию» 
(ds01sdo:ReportCountryCode)
