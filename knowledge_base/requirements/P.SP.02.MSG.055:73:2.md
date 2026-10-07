---
id: "P.SP.02.MSG.055:73:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.055"
requirement: "2"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 801
source_table: "Table 72, item 2"
source_item: "REQ 2 (Table 73)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.055:73:2

## Нормативное требование

в составе реквизита «Национальное патентное ведомство» (ipcdo:PatentAuthorityDetails) должен быть заполнен реквизит «Наименование уполномоченного органа» (csdo:AuthorityName)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.033 → P.SP.02.TRN.049 → P.SP.02.MSG.055 → P.SP.02.MSG.055:73:2

## XML

- Structure: R.IP.SP.03.003
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 801
- Printed page: 222
- Table/item: Table 72, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 73 item 2 via range 1-6 (PDF p.803)
- Inherited source chain: 72
- Source page: [[sources/OP22_P_SP_02/pages/page_801]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1-6", "location": "Таблица 73", "page": 803, "source_id": "22OP-RULE-P.SP.02.MSG.055-T73-1-6", "status": "CONFIRMED", "table": "73", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 72", "page": 801, "source_id": "22OP-RULE-P.SP.02.MSG.054-T72-2", "status": "CONFIRMED", "table": "72", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["72"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
