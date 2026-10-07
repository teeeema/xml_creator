---
id: "P.SP.02.MSG.053:71:22"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.053"
requirement: "22"
structure: "R.IP.SP.02.007"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 800
source_table: "Table 71, item 22"
source_item: "REQ 22 (Table 71)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.053:71:22

## Нормативное требование

в составе записи в информационных ресурсах национального патентного ведомства, содержащих сведения о ТЗ Союза, у которой значение реквизита «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId) совпадает со значением реквизита «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId), значения реквизитов «Дата истечения срока действия документа» (csdo:DocValidityDate), непосредственно подчиненных реквизиту «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails) должны совпадать со значениями реквизитов «Дата истечения срока действия документа» (csdo:DocValidityDate), непосредственно подчиненных реквизиту «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails)в составе сообщения за исключением одного значения

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.030 → P.SP.02.TRN.048 → P.SP.02.MSG.053 → P.SP.02.MSG.053:71:22

## XML

- Structure: R.IP.SP.02.007
- QName: csdo:DocValidityDate
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:UnifiedRegisterRecordsDetails/csdo:DocValidityDate

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 800
- Printed page: 221
- Table/item: Table 71, item 22
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_800]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 71", "page": 800, "source_id": "22OP-RULE-P.SP.02.MSG.053-T71-22", "status": "CONFIRMED", "table": "71", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 71", "page": 800, "source_id": "22OP-RULE-P.SP.02.MSG.053-T71-22", "status": "CONFIRMED", "table": "71", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["71"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg053_end_to_end.py; P.SP.02_OP_22/tests/test_msg053_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg053_safe_mapping.py

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Full condition needs external/current or previous registry/resource state unavailable in message XML.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
