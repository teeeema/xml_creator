---
id: "P.SP.02.MSG.028:44:23"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.028"
requirement: "23"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 719
source_table: "Table 44, item 23"
source_item: "REQ 23 (Table 44)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.028:44:23

## Нормативное требование

в составе реквизита «Адрес для переписки» (ipcdo:CorrespondenceAddressDetails) в составе реквизита «Адрес» (ccdo:SubjectAddressDetails) значение реквизита «Код вида адреса» (csdo:AddressKindCode) должно соответствовать значению «3» – «почтовый адрес (адрес для ведения переписки)»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.002 → P.SP.02.TRN.023 → P.SP.02.MSG.028 → P.SP.02.MSG.028:44:23

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 719
- Printed page: 140
- Table/item: Table 44, item 23
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_719]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "23", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 719, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-23", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "23", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 719, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-23", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
