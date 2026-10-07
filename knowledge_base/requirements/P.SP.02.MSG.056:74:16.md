---
id: "P.SP.02.MSG.056:74:16"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.056"
requirement: "16"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 806
source_table: "Table 74, item 16"
source_item: "REQ 16 (Table 74)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.056:74:16

## Нормативное требование

в составе реквизита «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails) реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.035 → P.SP.02.TRN.050 → P.SP.02.MSG.056 → P.SP.02.MSG.056:74:16

## XML

- Structure: R.IP.SP.03.003
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 806
- Printed page: 227
- Table/item: Table 74, item 16
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_806]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "16", "location": "Таблица 74", "page": 806, "source_id": "22OP-RULE-P.SP.02.MSG.056-T74-16", "status": "CONFIRMED", "table": "74", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "16", "location": "Таблица 74", "page": 806, "source_id": "22OP-RULE-P.SP.02.MSG.056-T74-16", "status": "CONFIRMED", "table": "74", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["74"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
