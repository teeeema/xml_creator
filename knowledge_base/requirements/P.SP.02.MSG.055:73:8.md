---
id: "P.SP.02.MSG.055:73:8"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.055"
requirement: "8"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 803
source_table: "Table 73, item 8"
source_item: "REQ 8 (Table 73)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.055:73:8

## Нормативное требование

в составе реквизита «Сведения о пошлине за осуществление юридически значимых действий» (ipcdo:IPPaymentDetails) реквизиты «Дата и время» (csdo:EventDateTime), «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) и «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails) не заполняются

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.033 → P.SP.02.TRN.049 → P.SP.02.MSG.055 → P.SP.02.MSG.055:73:8

## XML

- Structure: R.IP.SP.03.003
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 803
- Printed page: 224
- Table/item: Table 73, item 8
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_803]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "8", "location": "Таблица 73", "page": 803, "source_id": "22OP-RULE-P.SP.02.MSG.055-T73-8", "status": "CONFIRMED", "table": "73", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "8", "location": "Таблица 73", "page": 803, "source_id": "22OP-RULE-P.SP.02.MSG.055-T73-8", "status": "CONFIRMED", "table": "73", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["73"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
