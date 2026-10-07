---
id: "P.SP.02.MSG.031:49:14"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.031"
requirement: "14"
structure: "R.010"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 738
source_table: "Table 49, item 14"
source_item: "REQ 14 (Table 49)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.031:49:14

## Нормативное требование

в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) должны быть заполнены следующие реквизиты: «Изображение товарного знака» (ipsdo:TrademarkPicture); «Описание товарного знака Союза» (ipcdo:TMDescriptionDetails); «Наименование вида товарного знака» (ipsdo:TrademarkKindName); «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.026 → P.SP.02.MSG.031 → P.SP.02.MSG.031:49:14

## XML

- Structure: R.010
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 738
- Printed page: 159
- Table/item: Table 49, item 14
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_738]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "14", "location": "Таблица 49", "page": 738, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-14", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "14", "location": "Таблица 49", "page": 738, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-14", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
