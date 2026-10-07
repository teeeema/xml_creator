---
id: "P.SP.02.MSG.048:66:9"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.048"
requirement: "9"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 737
source_table: "Table 49, item 9"
source_item: "REQ 9 (Table 66)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.048:66:9

## Нормативное требование

если реквизит «Контактный реквизит» (ccdo:CommunicationDetails) заполнен в составе любых реквизитов, в его составе значение реквизита «Код вида связи» (csdo:CommunicationChannelCode) должно соответствовать одному из следующих значений: «TE», «EM» или «FX», в соответствии с перечнем видов средств (каналов) связи, утвержденным Решением Коллегии Комиссии от 6 декабря 2022 г. № 192

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.025 → P.SP.02.TRN.043 → P.SP.02.MSG.048 → P.SP.02.MSG.048:66:9

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 737
- Printed page: 158
- Table/item: Table 49, item 9
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 66 item 9 via range 6-19 (PDF p.784)
- Inherited source chain: 49
- Source page: [[sources/OP22_P_SP_02/pages/page_737]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 66", "page": 784, "source_id": "22OP-RULE-P.SP.02.MSG.048-T66-6-19", "status": "CONFIRMED", "table": "66", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "9", "location": "Таблица 49", "page": 737, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-9", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
