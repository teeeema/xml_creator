---
id: "P.SP.02.MSG.021:54:13"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.021"
requirement: "13"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 529
source_table: "Table 37, item 13"
source_item: "REQ 13 (Table 54)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.021:54:13

## Нормативное требование

в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) в составе реквизита «Адрес» (ccdo:SubjectAddressDetails) значение реквизита «Код вида адреса» (csdo:AddressKindCode) должно соответствовать значению «2» – «фактический адрес (адрес места нахождения или места жительства)»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.030 → P.SP.02.TRN.019 → P.SP.02.MSG.021 → P.SP.02.MSG.021:54:13

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 529
- Printed page: 117
- Table/item: Table 37, item 13
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 54 item 13 via range 6-19 (PDF p.575)
- Inherited source chain: 37
- Source page: [[sources/OP22_P_SP_02/pages/page_529]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 54", "page": 575, "source_id": "22OP-RULE-P.SP.02.MSG.021-T54-6-19", "status": "CONFIRMED", "table": "54", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "13", "location": "Таблица 37. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 529, "source_id": "22OP-RULE-P.SP.02.MSG.003-T37-13", "status": "CONFIRMED", "table": "37", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["37"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
