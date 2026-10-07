---
source_document: "49_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/49_ОП.pdf"
source_sha256: "81f82f343650ea19bb293ef7f45d86c57e9195e0cef315e4d190ab47e6d8bae8"
pdf_page: 130
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

22 
 
Код требования Формулировка требования 
 
30 
 
если существует реквизит «Сведения о суммах распределенных ввозных 
таможенных пошлин, приостановленных к перечислению» 
(ds01cdo:StopTransferDistributedDutyDetails), имеющий индикатор «Признак 
общей суммы» (ds01sdo:TotalAmountIndicator) со значением «1», то должен 
быть хотя бы один реквизит «Сведения о суммах распределенных ввозных 
таможенных пошлин, приостановленных к перечислению» 
(ds01cdo:StopTransferDistributedDutyDetails), имеющий индикатор «Признак 
общей суммы» (ds01sdo:TotalAmountIndicator) со значением «0» 
 
31 
 
для реквизита «Сведения о суммах распределенных ввозных таможенных 
пошлин, приостановленных к перечислению» 
(ds01cdo:StopTransferDistributedDutyDetails), имеющего индикатор «Признак 
общей суммы» (ds01sdo:TotalAmountIndicator) со значением «1», не должно 
быть заполнено значение реквизита «Код страны» (csdo:CountryCode) 
 
32 
 
для реквизита «Сведения о суммах распределенных ввозных таможенных 
пошлин, приостановленных к перечислению» 
(ds01cdo:StopTransferDistributedDutyDetails), имеющего индикатор «Признак 
общей суммы» (ds01sdo:TotalAmountIndicator) со значением «0», должно 
быть заполнено значение реквизита «Код страны» (csdo:CountryCode) 
 
33 
 
если для реквизита «Сведения о суммах распределенных ввозных 
таможенных пошлин, приостановленных к перечислению» 
(ds01cdo:StopTransferDistributedDutyDetails) реквизит «Признак общей 
суммы» (ds01sdo:TotalAmountIndicator) имеет значение «1», то значение 
реквизита «Суммы распределенных ввозных таможенных пошлин, 
приостановленные к перечислению» 
(ds01sdo:StopTransferDistributedDutyAmount) должно быть равно сумме всех 
значений реквизитов «Суммы распределенных ввозных таможенных 
пошлин, приостановленные к перечислению» 
(ds01sdo:StopTransferDistributedDutyAmount), указанных в реквизите 
«Сведения о суммах распределенных ввозных таможенных пошлин, 
приостановленных к перечислению» 
(ds01cdo:StopTransferDistributedDutyDetails) с индикатором «Признак общей 
суммы» (ds01sdo:TotalAmountIndicator) со значением «0» 
 
34 
 
для реквизита «Суммы распределенных ввозных таможенных пошлин, 
приостановленные к перечислению» 
(ds01sdo:StopTransferDistributedDutyAmount) должно быть указано значение 
атрибута «Код валюты» (атрибут currencyCode)
