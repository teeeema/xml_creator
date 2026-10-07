---
id: "P.SP.02.MSG.001:34:30"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.001"
requirement: "30"
structure: "R.IP.SP.02.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 520
source_table: "Table 34, item 30"
source_item: "REQ 30 (Table 34)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.001:34:30

## Нормативное требование

в составе реквизита «Товар в соответствии с МКТУ» (ipcdo:GoodsBaseDetails) реквизиты: «Признак возможности регистрации товарного знака Союза» (ipsdo:TrademarkDecisionIndicator), «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId), «Регистрационный номер НМПТ Союза» (ipsdo:ApellationOfOriginEAEUId), «Описание основания для отказа в регистрации товарного знака Союза в отношении товара» (ipsdo:TrademarkRegRefusalReasonText), «Описание несоответствия» (ipsdo:InconsistencyText) не заполняются

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.001 → P.SP.02.TRN.001 → P.SP.02.MSG.001 → P.SP.02.MSG.001:34:30

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:GoodsBaseDetails; ipsdo:TrademarkDecisionIndicator; ipsdo:TrademarkApplicationId; ipsdo:ApellationOfOriginEAEUId; ipsdo:TrademarkRegRefusalReasonText; ipsdo:InconsistencyText
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 520
- Printed page: 108
- Table/item: Table 34, item 30
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_520]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: P.SP.02.MSG.001.REQ.030
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "30", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 520, "source_id": "22OP-RULE-P.SP.02.MSG.001-30", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "30", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 520, "source_id": "22OP-RULE-P.SP.02.MSG.001-30", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg001_structured_rules.py

## Gap

- Reason: OTHER_OPEN
- Missing information: Only SAFE_PARTIAL/partial production fragments exist; whole requirement is not certified. No extra normative interpretation performed.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
