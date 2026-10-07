---
id: "P.SP.02.MSG.015:48:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.015"
requirement: "4"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 560
source_table: "Table 48, item 4"
source_item: "REQ 4 (Table 48)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.015:48:4

## Нормативное требование

В ipcdo:TrademarkNationalApplicationDetails должны быть заполнены csdo:UnifiedCountryCode, ipsdo:NationalApplicationId, ipsdo:NationalApplicationReceiptDate.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.023 → P.SP.02.TRN.013 → P.SP.02.MSG.015 → P.SP.02.MSG.015:48:4

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 560
- Printed page: 148
- Table/item: Table 48, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_560]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 48", "page": 560, "source_id": "22OP-RULE-P.SP.02.MSG.015-T48-4", "status": "CONFIRMED", "table": "48", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 48", "page": 560, "source_id": "22OP-RULE-P.SP.02.MSG.015-T48-4", "status": "CONFIRMED", "table": "48", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["48"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
