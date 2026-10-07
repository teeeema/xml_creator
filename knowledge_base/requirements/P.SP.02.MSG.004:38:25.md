---
id: "P.SP.02.MSG.004:38:25"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.004"
requirement: "25"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 519
source_table: "Table 34, item 25"
source_item: "REQ 25 (Table 38)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.004:38:25

## Нормативное требование

в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails) реквизит «Товарный знак Союза» (ipcdo:TrademarkDetails) должен быть заполнен, и в его составе должны быть заполнены реквизиты: «Описание товарного знака Союза» (ipcdo:TMDescriptionDetails); «Код вида товарного знака» (ipsdo:TrademarkKindCode); «Наименование вида товарного знака» (ipsdo:TrademarkKindName); «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.008 → P.SP.02.TRN.003 → P.SP.02.MSG.004 → P.SP.02.MSG.004:38:25

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 519
- Printed page: 107
- Table/item: Table 34, item 25
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 38 item 25 via range 6-29 (PDF p.533)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_519]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 38. Требования к электронному документу (сведениям) P.SP.02.MSG.004", "page": 533, "source_id": "22OP-RULE-P.SP.02.MSG.004-6-29", "status": "CONFIRMED", "table": "38", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "25", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 519, "source_id": "22OP-RULE-P.SP.02.MSG.001-25", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
