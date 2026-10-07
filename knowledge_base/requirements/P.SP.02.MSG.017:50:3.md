---
id: "P.SP.02.MSG.017:50:3"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.017"
requirement: "3"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 563
source_table: "Table 50, item 3"
source_item: "REQ 3 (Table 50)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.017:50:3

## Нормативное требование

В ipcdo:IPEntityStatusDetails csdo:EventDate обязателен; csdo:StatusCode = «03», codeListId не заполняется.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.025 → P.SP.02.TRN.015 → P.SP.02.MSG.017 → P.SP.02.MSG.017:50:3

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 563
- Printed page: 151
- Table/item: Table 50, item 3
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_563]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 50", "page": 563, "source_id": "22OP-RULE-P.SP.02.MSG.017-T50-3", "status": "CONFIRMED", "table": "50", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 50", "page": 563, "source_id": "22OP-RULE-P.SP.02.MSG.017-T50-3", "status": "CONFIRMED", "table": "50", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["50"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
