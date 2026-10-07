---
id: "P.SP.02.MSG.031:48:30"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.031"
requirement: "30"
structure: "R.010"
status: "OPEN_SOURCE_CONFLICT"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 734
source_table: "Table 48, item 30"
source_item: "REQ 30 (Table 48)"
qname_status: "CONFLICT"
implementation_status: "OPEN_SOURCE_CONFLICT"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.031:48:30

## Нормативное требование

в составе реквизита «Товар в соответствии с МКТУ» (ipcdo:GoodsBaseDetails) реквизит «Регистрационный номер заявки на товарный знак Союза» (ipsdo:TrademarkApplicationId), реквизит «Описание основания для отказа в регистрации товарного знака Союза в отношении товара» (ipsdo:TrademarkRegRefusalReasonText), реквизит «Описание несоответствия» (ipsdo:InconsistencyText) должны быть заполнены

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_SOURCE_CONFLICT

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.026 → P.SP.02.MSG.031 → P.SP.02.MSG.031:48:30

## XML

- Structure: R.010
- QName: ipsdo:InconsistencyText
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:InconsistencyText

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 734
- Printed page: 155
- Table/item: Table 48, item 30
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_734]]

## Project state

- Status: OPEN_SOURCE_CONFLICT
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "30", "location": "Таблица 48", "page": 734, "source_id": "22OP-RULE-P.SP.02.MSG.031-T48-30", "status": "CONFIRMED", "table": "48", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "30", "location": "Таблица 48", "page": 734, "source_id": "22OP-RULE-P.SP.02.MSG.031-T48-30", "status": "CONFIRMED", "table": "48", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["48"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg031_end_to_end.py; P.SP.02_OP_22/tests/test_msg031_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg031_rule_execution.py; P.SP.02_OP_22/tests/test_msg031_safe_mapping.py

## Gap

- Reason: OPEN_SOURCE_CONFLICT
- Missing information: Source/StructureDefinition owner or QName conflict retained; see source refs and original gap notes.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: A higher-priority authoritative source resolves the conflicting values; provenance is recorded and the conflicting mapping is replaced with the confirmed one.
