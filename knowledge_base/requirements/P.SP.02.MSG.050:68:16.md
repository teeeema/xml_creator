---
id: "P.SP.02.MSG.050:68:16"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.050"
requirement: "16"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 739
source_table: "Table 49, item 16"
source_item: "REQ 16 (Table 68)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.050:68:16

## Нормативное требование

реквизит «Товар в соответствии с МКТУ» (ipcdo:GoodsBaseDetails) должен быть заполнен, и в его составе должны быть заполнены реквизиты: «Номер класса МКТУ» (ipsdo:GoodsClassCode); «Наименование класса МКТУ» (ipsdo:GoodsClassName); «Наименование товара (услуги)» (ipsdo:GoodsName); «Признак возможности регистрации товарного знака Союза» (ipsdo:TrademarkDecisionIndicator); «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.027 → P.SP.02.TRN.045 → P.SP.02.MSG.050 → P.SP.02.MSG.050:68:16

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 739
- Printed page: 160
- Table/item: Table 49, item 16
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 68 item 16 via range 6-19 (PDF p.789)
- Inherited source chain: 49
- Source page: [[sources/OP22_P_SP_02/pages/page_739]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 68", "page": 789, "source_id": "22OP-RULE-P.SP.02.MSG.050-T68-6-19", "status": "CONFIRMED", "table": "68", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "16", "location": "Таблица 49", "page": 739, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-16", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
