---
id: "P.SP.02.MSG.006:40:10"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.006"
requirement: "10"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 514
source_table: "Table 34, item 10"
source_item: "REQ 10 (Table 40)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.006:40:10

## Нормативное требование

если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) заполнен в составе любых реквизитов, то в его составе значение реквизита «Код вида связи» (csdo:CommunicationChannelCode) должно соответствовать одному из следующих значений: «TE», «EM» или «FX», в соответствии с перечнем видов средств (каналов) связи, утвержденным Решением Коллегии Комиссии от 6 декабря 2022 г. № 192

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.010 → P.SP.02.TRN.005 → P.SP.02.MSG.006 → P.SP.02.MSG.006:40:10

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
- Table/item: Table 34, item 10
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 40 item 10 via range 6-29 (PDF p.540)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_514]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 40. Требования к электронному документу (сведениям) P.SP.02.MSG.006", "page": 540, "source_id": "22OP-RULE-P.SP.02.MSG.006-T40-6-29", "status": "CONFIRMED", "table": "40", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "10", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 514, "source_id": "22OP-RULE-P.SP.02.MSG.001-10", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
