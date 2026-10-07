---
id: "P.SP.02.MSG.039:57:29"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.039"
requirement: "29"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 721
source_table: "Table 44, item 29"
source_item: "REQ 29 (Table 57)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.039:57:29

## Нормативное требование

в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails) реквизит «Товар в соответствии с МКТУ» (ipcdo:GoodsBaseDetails) должен быть заполнен, и в его составе должны быть заполнены реквизиты: «Номер класса МКТУ» (ipsdo:GoodsClassCode); «Наименование класса МКТУ» (ipsdo:GoodsClassName); «Наименование товара (услуги)» (ipsdo:GoodsName)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.015 → P.SP.02.TRN.034 → P.SP.02.MSG.039 → P.SP.02.MSG.039:57:29

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 721
- Printed page: 142
- Table/item: Table 44, item 29
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 57 item 29 via range 6-29 (PDF p.758)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_721]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 57", "page": 758, "source_id": "22OP-RULE-P.SP.02.MSG.039-T57-6-29", "status": "CONFIRMED", "table": "57", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "29", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 721, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-29", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
