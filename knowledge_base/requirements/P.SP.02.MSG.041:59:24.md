---
id: "P.SP.02.MSG.041:59:24"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.041"
requirement: "24"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 720
source_table: "Table 44, item 24"
source_item: "REQ 24 (Table 59)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.041:59:24

## Нормативное требование

в составе реквизита «Адрес для переписки» (ipcdo:CorrespondenceAddressDetails) в составе реквизита «Адрес» (ccdo:SubjectAddressDetails) значение реквизита «Код страны» (csdo:UnifiedCountryCode) должно соответствовать одному из следующих значений: «AM», «BY», «KZ», «KG» или «RU»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.018 → P.SP.02.TRN.036 → P.SP.02.MSG.041 → P.SP.02.MSG.041:59:24

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 720
- Printed page: 141
- Table/item: Table 44, item 24
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 59 item 24 via range 6-29 (PDF p.763)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_720]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 59", "page": 763, "source_id": "22OP-RULE-P.SP.02.MSG.041-T59-6-29", "status": "CONFIRMED", "table": "59", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "24", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 720, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-24", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
