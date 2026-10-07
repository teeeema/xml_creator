---
id: "P.SP.02.MSG.031:49:23"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.031"
requirement: "23"
structure: "R.010"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 740
source_table: "Table 49, item 23"
source_item: "REQ 23 (Table 49)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.031:49:23

## Нормативное требование

если в составе реквизита «Сведения о подписании документа» (ipcdo:SignatureDetails) реквизит «ФИО» (ccdo:FullNameDetails), непосредственно подчиненный реквизиту «Сведения о подписании документа» (ipcdo:SignatureDetails), заполнен, то реквизит «Сотрудник организации» (ipcdo:OfficerDetails) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.026 → P.SP.02.MSG.031 → P.SP.02.MSG.031:49:23

## XML

- Structure: R.010
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 740
- Printed page: 161
- Table/item: Table 49, item 23
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_740]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "23", "location": "Таблица 49", "page": 740, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-23", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "23", "location": "Таблица 49", "page": 740, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-23", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
