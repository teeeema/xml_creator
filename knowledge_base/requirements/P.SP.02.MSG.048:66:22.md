---
id: "P.SP.02.MSG.048:66:22"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.048"
requirement: "22"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 784
source_table: "Table 66, item 22"
source_item: "REQ 22 (Table 66)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.048:66:22

## Нормативное требование

в составе реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), реквизит «Конечная дата и время» (csdo:EndDateTime) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.025 → P.SP.02.TRN.043 → P.SP.02.MSG.048 → P.SP.02.MSG.048:66:22

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 784
- Printed page: 205
- Table/item: Table 66, item 22
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_784]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 66", "page": 784, "source_id": "22OP-RULE-P.SP.02.MSG.048-T66-22", "status": "CONFIRMED", "table": "66", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 66", "page": 784, "source_id": "22OP-RULE-P.SP.02.MSG.048-T66-22", "status": "CONFIRMED", "table": "66", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["66"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
