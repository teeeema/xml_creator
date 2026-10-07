---
id: "P.SP.02.MSG.047:65:24"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.047"
requirement: "24"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 782
source_table: "Table 65, item 24"
source_item: "REQ 24 (Table 65)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.047:65:24

## Нормативное требование

если в составе реквизита «Сведения о подписании документа» (ipcdo:SignatureDetails) реквизит «ФИО» (ccdo:FullNameDetails), непосредственно подчиненный реквизиту «Сведения о подписании документа» (ipcdo:SignatureDetails), заполнен, то реквизит «Сотрудник организации» (ipcdo:OfficerDetails) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.024 → P.SP.02.TRN.042 → P.SP.02.MSG.047 → P.SP.02.MSG.047:65:24

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 782
- Printed page: 203
- Table/item: Table 65, item 24
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_782]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "24", "location": "Таблица 65", "page": 782, "source_id": "22OP-RULE-P.SP.02.MSG.047-T65-24", "status": "CONFIRMED", "table": "65", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "24", "location": "Таблица 65", "page": 782, "source_id": "22OP-RULE-P.SP.02.MSG.047-T65-24", "status": "CONFIRMED", "table": "65", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["65"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
