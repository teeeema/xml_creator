---
id: "P.SP.02.MSG.030:46:33"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.030"
requirement: "33"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 730
source_table: "Table 46, item 33"
source_item: "REQ 33 (Table 46)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.030:46:33

## Нормативное требование

реквизит «Признак согласия на обработку представленных сведений» (ipsdo:ConsentToDataProcessingIndicator)) должен быть заполнен и его значение должно соответствовать одному из следующих значений: «1» – «согласие на обработку сведений представлено»; «0» – «согласие на обработку сведений не представлено»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.004 → P.SP.02.TRN.025 → P.SP.02.MSG.030 → P.SP.02.MSG.030:46:33

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 730
- Printed page: 151
- Table/item: Table 46, item 33
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_730]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "33", "location": "Таблица 46", "page": 730, "source_id": "22OP-RULE-P.SP.02.MSG.030-T46-33", "status": "CONFIRMED", "table": "46", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "33", "location": "Таблица 46", "page": 730, "source_id": "22OP-RULE-P.SP.02.MSG.030-T46-33", "status": "CONFIRMED", "table": "46", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["46"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
