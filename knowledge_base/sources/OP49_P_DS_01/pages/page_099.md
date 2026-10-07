---
source_document: "49_ОП.pdf"
source_path: "/Users/tema/Documents/Work/Документы_xml/49_ОП.pdf"
source_sha256: "81f82f343650ea19bb293ef7f45d86c57e9195e0cef315e4d190ab47e6d8bae8"
pdf_page: 99
extraction_method: "pypdf 6.19.0"
extraction_status: "OK"
generated_by: "knowledge_base/tools/build_kb.py"
---

46 
 
Код требования Формулировка требования 
 
36 
 
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
 
37 
 
для реквизита «Суммы распределенных ввозных таможенных пошлин, 
приостановленные к перечислению» 
(ds01sdo:StopTransferDistributedDutyAmount) значение атрибута «Код 
валюты» (атрибут currencyCode) должно соответствовать буквенному коду 
валюты того государства-члена, код которого указан в реквизите «Код 
страны, предоставившей информацию» (ds01sdo:ReportCountryCode) 
 
38 
 
для реквизита «Суммы поступлений на счета в иностранной валюте» 
(ds01sdo:TotalExternalRevenueDistributedDutyAmount) значение атрибута 
«Код валюты» (атрибут currencyCode) должно соответствовать буквенному 
коду валюты того государства-члена, код которого указан для реквизита 
«Сведения о суммах поступлений на счета в иностранной валюте» 
(ds01cdo:ExternalRevenueDistributedDutyDetails) 
 
39 
 
для реквизита «Доходы от распределения ввозных таможенных пошлин» 
(ds01sdo:ExternalRevenueDistributedDutyAmount) значение атрибута «Код 
валюты» (атрибут currencyCode) должно соответствовать буквенному коду 
валюты того государства-члена, код которого указан для реквизита 
«Сведения о суммах поступлений на счета в иностранной валюте» 
(ds01cdo:ExternalRevenueDistributedDutyDetails) 
 
40 
 
для реквизита «Суммы поступивших процентов за просрочку» 
(ds01sdo:DefaultInterestAmount) значение атрибута «Код валюты» (атрибут 
currencyCode) должно соответствовать буквенному коду валюты того 
государства-члена, код которого указан для реквизита «Сведения о суммах 
поступлений на счета в иностранной валюте» 
(ds01cdo:ExternalRevenueDistributedDutyDetails)
