---
id: "P.SP.02.MSG.010:43:5"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.010"
requirement: "5"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 547
source_table: "Table 43, item 5"
source_item: "REQ 5 (Table 43)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.010:43:5

## Нормативное требование

ipcdo:IPEntityStatusDetails должен быть заполнен; csdo:StatusCode = «02», codeListId не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.018 → P.SP.02.TRN.008 → P.SP.02.MSG.010 → P.SP.02.MSG.010:43:5

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 547
- Printed page: 135
- Table/item: Table 43, item 5
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_547]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 43. Требования к электронному документу (сведениям) P.SP.02.MSG.010", "page": 547, "source_id": "22OP-RULE-P.SP.02.MSG.010-T43-5", "status": "CONFIRMED", "table": "43", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 43. Требования к электронному документу (сведениям) P.SP.02.MSG.010", "page": 547, "source_id": "22OP-RULE-P.SP.02.MSG.010-T43-5", "status": "CONFIRMED", "table": "43", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["43"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
