---
id: "P.SP.02.MSG.004:38:7"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.004"
requirement: "7"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 514
source_table: "Table 34, item 7"
source_item: "REQ 7 (Table 38)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.004:38:7

## Нормативное требование

если реквизит «Код страны» (csdo:UnifiedCountryCode) заполнен в составе любых реквизитов, то значение атрибута «идентификатор справочника (классификатора)» (атрибут codeListId) в его составе должно соответствовать значению «ВОИС ST.3»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.008 → P.SP.02.TRN.003 → P.SP.02.MSG.004 → P.SP.02.MSG.004:38:7

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 514
- Printed page: 102
- Table/item: Table 34, item 7
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 38 item 7 via range 6-29 (PDF p.533)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_514]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 38. Требования к электронному документу (сведениям) P.SP.02.MSG.004", "page": 533, "source_id": "22OP-RULE-P.SP.02.MSG.004-6-29", "status": "CONFIRMED", "table": "38", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "7", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 514, "source_id": "22OP-RULE-P.SP.02.MSG.001-7", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
