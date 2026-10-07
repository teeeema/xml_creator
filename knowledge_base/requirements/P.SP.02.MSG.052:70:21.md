---
id: "P.SP.02.MSG.052:70:21"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.052"
requirement: "21"
structure: "R.IP.SP.02.007"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 795
source_table: "Table 70, item 21"
source_item: "REQ 21 (Table 70)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.052:70:21

## Нормативное требование

в составе экземпляра реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), содержащего сведения об аннулировании регистрации ТЗ Союза, должен быть заполнен реквизит «Начальная дата и время» (csdo:StartDateTime), и значение реквизита «Начальная дата и время» (csdo:StartDateTime) в составе этого экземпляра сведений записи из состава информационных ресурсах национального патентного ведомства, содержащих сведения о ТЗ Союза, должно быть меньше, чем значение реквизита «Начальная дата и время» (csdo:StartDateTime) в составе экземпляра реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), содержащего сведения о регистрации нового ТЗ Союза

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.029 → P.SP.02.TRN.047 → P.SP.02.MSG.052 → P.SP.02.MSG.052:70:21

## XML

- Structure: R.IP.SP.02.007
- QName: ipcdo:UnifiedRegisterRecordsDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:UnifiedRegisterRecordsDetails

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 795
- Printed page: 216
- Table/item: Table 70, item 21
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_795]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "21", "location": "Таблица 70", "page": 795, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-21", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "21", "location": "Таблица 70", "page": 795, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-21", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["70"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg052_end_to_end.py; P.SP.02_OP_22/tests/test_msg052_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg052_safe_mapping.py

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Date/set relationship needs previous union resource state; current XML cannot supply that state.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
