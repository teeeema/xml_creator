---
id: "P.SP.02.MSG.009:42:32"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.009"
requirement: "32"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 545
source_table: "Table 42, item 32"
source_item: "REQ 32 (Table 42)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.009:42:32

## Нормативное требование

csdo:EndDateTime должен быть заполнен

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.017 → P.SP.02.TRN.007 → P.SP.02.MSG.009 → P.SP.02.MSG.009:42:32

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 545
- Printed page: 133
- Table/item: Table 42, item 32
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_545]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 42. Требования к электронному документу (сведениям) P.SP.02.MSG.009", "page": 545, "source_id": "22OP-RULE-P.SP.02.MSG.009-T42-32", "status": "CONFIRMED", "table": "42", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 42. Требования к электронному документу (сведениям) P.SP.02.MSG.009", "page": 545, "source_id": "22OP-RULE-P.SP.02.MSG.009-T42-32", "status": "CONFIRMED", "table": "42", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["42"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
