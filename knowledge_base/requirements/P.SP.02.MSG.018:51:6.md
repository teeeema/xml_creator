---
id: "P.SP.02.MSG.018:51:6"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.018"
requirement: "6"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 527
source_table: "Table 37, item 6"
source_item: "REQ 6 (Table 51)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.018:51:6

## Нормативное требование

если реквизит «Код страны» (csdo:UnifiedCountryCode) заполнен в составе любых реквизитов, в его составе значение атрибута «идентификатор справочника (классификатора)» (атрибут codeListId) должно соответствовать значению «ВОИС ST.3»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.026 → P.SP.02.TRN.016 → P.SP.02.MSG.018 → P.SP.02.MSG.018:51:6

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 527
- Printed page: 115
- Table/item: Table 37, item 6
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 51 item 6 via range 6-19 (PDF p.565)
- Inherited source chain: 37
- Source page: [[sources/OP22_P_SP_02/pages/page_527]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 51. Требования к заполнению реквизитов P.SP.02.MSG.018", "page": 565, "source_id": "22OP-RULE-P.SP.02.MSG.018-T51-6-19", "status": "CONFIRMED", "table": "51", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "6", "location": "Таблица 37. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 527, "source_id": "22OP-RULE-P.SP.02.MSG.003-T37-6", "status": "CONFIRMED", "table": "37", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["37"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
