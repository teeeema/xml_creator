---
id: "P.SP.02.MSG.041:59:12"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.041"
requirement: "12"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 716
source_table: "Table 44, item 12"
source_item: "REQ 12 (Table 59)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.041:59:12

## Нормативное требование

в составе реквизита «Национальное патентное ведомство» (ipcdo:PatentAuthorityDetails) должен быть заполнен реквизит «Наименование уполномоченного органа» (csdo:AuthorityName) и должен быть заполнен реквизит «Адрес» (ccdo:SubjectAddressDetails), в составе которого значение реквизита «Код вида адреса» (csdo:AddressKindCode) должно соответствовать значению «2» – «фактический адрес (адрес места нахождения или места жительства)»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.018 → P.SP.02.TRN.036 → P.SP.02.MSG.041 → P.SP.02.MSG.041:59:12

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 716
- Printed page: 137
- Table/item: Table 44, item 12
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 59 item 12 via range 6-29 (PDF p.763)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_716]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 59", "page": 763, "source_id": "22OP-RULE-P.SP.02.MSG.041-T59-6-29", "status": "CONFIRMED", "table": "59", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "12", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 716, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-12", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
