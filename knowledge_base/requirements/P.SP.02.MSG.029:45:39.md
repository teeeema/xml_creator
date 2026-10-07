---
id: "P.SP.02.MSG.029:45:39"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.029"
requirement: "39"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 728
source_table: "Table 45, item 39"
source_item: "REQ 39 (Table 45)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.029:45:39

## Нормативное требование

если в составе реквизита «Сведения о подписании документа» (ipcdo:SignatureDetails) заполнен реквизит «Сотрудник организации» (ipcdo:OfficerDetails), в его составе должны быть заполнены реквизиты «Фамилия» (csdo:LastName), «Имя» (csdo:FirstName) и «Наименование должности» (csdo:PositionName), а реквизит «Контактный реквизит» (ccdo:CommunicationDetails) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.003 → P.SP.02.TRN.024 → P.SP.02.MSG.029 → P.SP.02.MSG.029:45:39

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 728
- Printed page: 149
- Table/item: Table 45, item 39
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_728]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "39", "location": "Таблица 45", "page": 728, "source_id": "22OP-RULE-P.SP.02.MSG.029-T45-39", "status": "CONFIRMED", "table": "45", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "39", "location": "Таблица 45", "page": 728, "source_id": "22OP-RULE-P.SP.02.MSG.029-T45-39", "status": "CONFIRMED", "table": "45", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["45"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
