---
id: "P.SP.02.MSG.045:63:32"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.045"
requirement: "32"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 776
source_table: "Table 63, item 32"
source_item: "REQ 32 (Table 63)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.045:63:32

## Нормативное требование

в составе эреквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails), содержащего измененные сведения о заявке на ТЗ Союза, в составе реквизита «Сведения о статусном состоянии» (ipcdo: ipcdo:IPEntityStatusDetails) должны быть заполнены реквизиты: «Дата» (csdo:EventDate); «Номер документа» (csdo:DocId); «Дата поступления документа» (ipsdo:IPDocReceiptDate); «Описание» (csdo:DescriptionText)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.022 → P.SP.02.TRN.040 → P.SP.02.MSG.045 → P.SP.02.MSG.045:63:32

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 776
- Printed page: 197
- Table/item: Table 63, item 32
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_776]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 63", "page": 776, "source_id": "22OP-RULE-P.SP.02.MSG.045-T63-32", "status": "CONFIRMED", "table": "63", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 63", "page": 776, "source_id": "22OP-RULE-P.SP.02.MSG.045-T63-32", "status": "CONFIRMED", "table": "63", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["63"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
