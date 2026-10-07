---
id: "P.SP.02.MSG.053:71:23"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.053"
requirement: "23"
structure: "R.IP.SP.02.007"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 800
source_table: "Table 71, item 23"
source_item: "REQ 23 (Table 71)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.053:71:23

## Нормативное требование

значение реквизита «Дата истечения срока действия документа» (csdo:DocValidityDate), непосредственно подчиненного реквизиту «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), для которого не найдено соответствия в составе экземпляров реквизита «Дата истечения срока действия документа» (csdo:DocValidityDate), непосредственно подчиненных реквизиту «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails) в составе информационных ресурсах национального патентного ведомства, содержащих сведения о ТЗ Союза, должно быть больше, чем значения остальных реквизитов «Дата истечения срока действия документа» (csdo:DocValidityDate), непосредственно подчиненных реквизиту «Сведения записи Единого реестра ТЗ Союза» в составе сообщения

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.030 → P.SP.02.TRN.048 → P.SP.02.MSG.053 → P.SP.02.MSG.053:71:23

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
- Table/item: Table 71, item 23
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_800]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "23", "location": "Таблица 71", "page": 800, "source_id": "22OP-RULE-P.SP.02.MSG.053-T71-23", "status": "CONFIRMED", "table": "71", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "23", "location": "Таблица 71", "page": 800, "source_id": "22OP-RULE-P.SP.02.MSG.053-T71-23", "status": "CONFIRMED", "table": "71", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["71"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg053_end_to_end.py; P.SP.02_OP_22/tests/test_msg053_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg053_safe_mapping.py

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Full condition needs external/current or previous registry/resource state unavailable in message XML.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
