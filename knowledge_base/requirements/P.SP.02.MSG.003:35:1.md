---
id: "P.SP.02.MSG.003:35:1"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.003"
requirement: "1"
structure: "R.010"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 523
source_table: "Table 35, item 1"
source_item: "REQ 1 (Table 35)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.003:35:1

## Нормативное требование

электронный документ (сведения) «Обобщенная структура электронного документа (сведений)» (R.010) должен включать в себя один экземпляр электронного документа (сведений) «Сведения о заявке, ходатайстве для прохождения процедур регистрации ТЗ Союза» (R.IP.SP.02.002) либо один экземпляр электронного документа (сведений) «Сведения о ТЗ Союза из Единого реестра ТЗ Союза» (R.IP.SP.02.007)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.002 → P.SP.02.MSG.003 → P.SP.02.MSG.003:35:1

## XML

- Structure: R.010
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 523
- Printed page: 111
- Table/item: Table 35, item 1
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_523]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 35. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 523, "source_id": "22OP-RULE-P.SP.02.MSG.003-T35-1", "status": "CONFIRMED", "table": "35", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "1", "location": "Таблица 35. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 523, "source_id": "22OP-RULE-P.SP.02.MSG.003-T35-1", "status": "CONFIRMED", "table": "35", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["35"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
