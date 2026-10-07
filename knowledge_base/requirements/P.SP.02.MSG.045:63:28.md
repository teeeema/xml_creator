---
id: "P.SP.02.MSG.045:63:28"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.045"
requirement: "28"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 721
source_table: "Table 44, item 28"
source_item: "REQ 28 (Table 63)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.045:63:28

## Нормативное требование

значение реквизита «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) должно соответствовать одному из следующих значений: «1» – «товарный знак является коллективным»; «0» – «товарный знак не является коллективным»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.022 → P.SP.02.TRN.040 → P.SP.02.MSG.045 → P.SP.02.MSG.045:63:28

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 721
- Printed page: 142
- Table/item: Table 44, item 28
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 63 item 28 via range 6-29 (PDF p.775)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_721]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 63", "page": 775, "source_id": "22OP-RULE-P.SP.02.MSG.045-T63-6-29", "status": "CONFIRMED", "table": "63", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "28", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 721, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-28", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
