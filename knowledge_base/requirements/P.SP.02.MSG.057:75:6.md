---
id: "P.SP.02.MSG.057:75:6"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.057"
requirement: "6"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 802
source_table: "Table 72, item 6"
source_item: "REQ 6 (Table 75)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.057:75:6

## Нормативное требование

реквизит «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId) должен быть заполнен

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.035 → P.SP.02.TRN.050 → P.SP.02.MSG.057 → P.SP.02.MSG.057:75:6

## XML

- Structure: R.IP.SP.03.003
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 802
- Printed page: 223
- Table/item: Table 72, item 6
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 75 item 6 via range 1-19 (PDF p.807)
- Inherited source chain: 74 -> 72
- Source page: [[sources/OP22_P_SP_02/pages/page_802]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1-19", "location": "Таблица 75", "page": 807, "source_id": "22OP-RULE-P.SP.02.MSG.057-T75-1-19", "status": "CONFIRMED", "table": "75", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "6", "location": "Таблица 72", "page": 802, "source_id": "22OP-RULE-P.SP.02.MSG.054-T72-6", "status": "CONFIRMED", "table": "72", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["74", "72"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
