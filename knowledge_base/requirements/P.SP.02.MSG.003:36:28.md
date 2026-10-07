---
id: "P.SP.02.MSG.003:36:28"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.003"
requirement: "28"
structure: "R.010"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 520
source_table: "Table 34, item 28"
source_item: "REQ 28 (Table 36)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.003:36:28

## Нормативное требование

значение реквизита «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) должно соответствовать одному из следующих значений: «1» – «товарный знак является коллективным»; «0» – «товарный знак не является коллективным»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.002 → P.SP.02.MSG.003 → P.SP.02.MSG.003:36:28

## XML

- Structure: R.010
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 520
- Printed page: 108
- Table/item: Table 34, item 28
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 36 item 28 via range 6-29 (PDF p.525)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_520]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 36. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 525, "source_id": "22OP-RULE-P.SP.02.MSG.003-T36-6-29", "status": "CONFIRMED", "table": "36", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "28", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 520, "source_id": "22OP-RULE-P.SP.02.MSG.001-28", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
