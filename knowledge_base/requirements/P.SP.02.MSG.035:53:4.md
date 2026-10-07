---
id: "P.SP.02.MSG.035:53:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.035"
requirement: "4"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 570
source_table: "Table 53, item 4"
source_item: "REQ 4 (Table 53)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.035:53:4

## Нормативное требование

Для нового ТЗ Союза EventDate заполнен, StatusCode = «01», codeListId не заполняется.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.011 → P.SP.02.TRN.030 → P.SP.02.MSG.035 → P.SP.02.MSG.035:53:4

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 570
- Printed page: 158
- Table/item: Table 53, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_570]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 53", "page": 750, "source_id": "22OP-RULE-P.SP.02.MSG.035-T53-4", "status": "CONFIRMED", "table": "53", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 53", "page": 570, "source_id": "22OP-RULE-P.SP.02.MSG.020-T53-4", "status": "CONFIRMED", "table": "53", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["53"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
