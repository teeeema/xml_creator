---
id: "P.SP.02.MSG.019:52:10"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.019"
requirement: "10"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 528
source_table: "Table 37, item 10"
source_item: "REQ 10 (Table 52)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.019:52:10

## Нормативное требование

в составе реквизита «Национальное патентное ведомство» (ipcdo:PatentAuthorityDetails) должны быть заполнены реквизиты: «Код страны» (csdo:UnifiedCountryCode); «Наименование уполномоченного органа» (csdo:AuthorityName); «Краткое наименование уполномоченного органа» (csdo:AuthorityBriefName)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.027 → P.SP.02.TRN.017 → P.SP.02.MSG.019 → P.SP.02.MSG.019:52:10

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 528
- Printed page: 116
- Table/item: Table 37, item 10
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 52 item 10 via range 6-19 (PDF p.568)
- Inherited source chain: 37
- Source page: [[sources/OP22_P_SP_02/pages/page_528]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 52", "page": 568, "source_id": "22OP-RULE-P.SP.02.MSG.019-T52-6-19", "status": "CONFIRMED", "table": "52", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "10", "location": "Таблица 37. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 528, "source_id": "22OP-RULE-P.SP.02.MSG.003-T37-10", "status": "CONFIRMED", "table": "37", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["37"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
