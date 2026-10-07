---
id: "P.SP.02.MSG.046:64:9"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.046"
requirement: "9"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 779
source_table: "Table 64, item 9"
source_item: "REQ 9 (Table 64)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.046:64:9

## Нормативное требование

если в составе реквизита «Сведения о подписании документа» (ipcdo:SignatureDetails) заполнен реквизит «Сотрудник организации» (ipcdo:OfficerDetails), в его составе должны быть заполнены реквизиты «Фамилия» (csdo:LastName), «Имя» (csdo:FirstName) и «Наименование должности» (csdo:PositionName), а реквизит «Контактный реквизит» (ccdo:CommunicationDetails) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.023 → P.SP.02.TRN.041 → P.SP.02.MSG.046 → P.SP.02.MSG.046:64:9

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 779
- Printed page: 200
- Table/item: Table 64, item 9
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_779]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "9", "location": "Таблица 64", "page": 779, "source_id": "22OP-RULE-P.SP.02.MSG.046-T64-9", "status": "CONFIRMED", "table": "64", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "9", "location": "Таблица 64", "page": 779, "source_id": "22OP-RULE-P.SP.02.MSG.046-T64-9", "status": "CONFIRMED", "table": "64", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["64"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
