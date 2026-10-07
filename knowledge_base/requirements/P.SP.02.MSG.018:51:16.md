---
id: "P.SP.02.MSG.018:51:16"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.018"
requirement: "16"
structure: "R.IP.SP.02.007"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 529
source_table: "Table 37, item 16"
source_item: "REQ 16 (Table 51)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.018:51:16

## Нормативное требование

реквизит «Товар в соответствии с МКТУ» (ipcdo:GoodsBaseDetails) должен быть заполнен, и в его составе должны быть заполнены реквизиты: «Номер класса МКТУ» (ipcdo:GoodsClassCode); «Наименование класса МКТУ» (ipsdo:GoodsClassName); «Наименование товара (услуги)» (ipsdo:GoodsName); «Признак возможности регистрации товарного знака Союза» (ipsdo:TrademarkDecisionIndicator); «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.026 → P.SP.02.TRN.016 → P.SP.02.MSG.018 → P.SP.02.MSG.018:51:16

## XML

- Structure: R.IP.SP.02.007
- QName: ipcdo:GoodsBaseDetails; ipcdo:GoodsClassCode; ipsdo:GoodsClassName; ipsdo:GoodsName; ipsdo:TrademarkDecisionIndicator; ipsdo:TrademarkApplicationId
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 529
- Printed page: 117
- Table/item: Table 37, item 16
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 51 item 16 via range 6-19 (PDF p.565)
- Inherited source chain: 37
- Source page: [[sources/OP22_P_SP_02/pages/page_529]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: P.SP.02.MSG.018.T51.REQ.6_19; P.SP.02.MSG.018.T51.REQ.6_19
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 51. Требования к заполнению реквизитов P.SP.02.MSG.018", "page": 565, "source_id": "22OP-RULE-P.SP.02.MSG.018-T51-6-19", "status": "CONFIRMED", "table": "51", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "16", "location": "Таблица 37. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 529, "source_id": "22OP-RULE-P.SP.02.MSG.003-T37-16", "status": "CONFIRMED", "table": "37", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["37"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OTHER_OPEN
- Missing information: Only SAFE_PARTIAL/partial production fragments exist; whole requirement is not certified. No extra normative interpretation performed.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
