---
id: "P.SP.02.MSG.049:67:17"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.049"
requirement: "17"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 739
source_table: "Table 49, item 17"
source_item: "REQ 17 (Table 67)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.049:67:17

## Нормативное требование

в составе реквизита «Товар в соответствии с МКТУ» (ipcdo:GoodsBaseDetails) реквизиты: «Регистрационный номер товарного знака Союза» (ipsdo:TrademarkId); «Регистрационный номер НМПТ Союза» (ipsdo:ApellationOfOriginEAEUId); «Описание основания для отказа в регистрации товарного знака Союза в отношении товара» (ipsdo:TrademarkRegRefusalReasonText) не заполняются

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.026 → P.SP.02.TRN.044 → P.SP.02.MSG.049 → P.SP.02.MSG.049:67:17

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
- Table/item: Table 49, item 17
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 67 item 17 via range 6-19 (PDF p.786)
- Inherited source chain: 49
- Source page: [[sources/OP22_P_SP_02/pages/page_739]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 67", "page": 786, "source_id": "22OP-RULE-P.SP.02.MSG.049-T67-6-19", "status": "CONFIRMED", "table": "67", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "17", "location": "Таблица 49", "page": 739, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-17", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
