---
id: "P.SP.02.MSG.053:71:25"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.053"
requirement: "25"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 800
source_table: "Table 71, item 25"
source_item: "REQ 25 (Table 71)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.053:71:25

## Нормативное требование

если в составе реквизита «Сведения о подписании документа» (ipcdo:SignatureDetails) реквизит «ФИО» (ccdo:FullNameDetails), непосредственно подчиненный реквизиту «Сведения о подписании документа» (ipcdo:SignatureDetails), заполнен, то реквизит «Сотрудник организации» (ipcdo:OfficerDetails) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.030 → P.SP.02.TRN.048 → P.SP.02.MSG.053 → P.SP.02.MSG.053:71:25

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 800
- Printed page: 221
- Table/item: Table 71, item 25
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_800]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "25", "location": "Таблица 71", "page": 800, "source_id": "22OP-RULE-P.SP.02.MSG.053-T71-25", "status": "CONFIRMED", "table": "71", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "25", "location": "Таблица 71", "page": 800, "source_id": "22OP-RULE-P.SP.02.MSG.053-T71-25", "status": "CONFIRMED", "table": "71", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["71"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
