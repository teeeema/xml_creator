---
id: "P.SP.02.MSG.003:37:15"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.003"
requirement: "15"
structure: "R.010"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 529
source_table: "Table 37, item 15"
source_item: "REQ 15 (Table 37)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.003:37:15

## Нормативное требование

в составе реквизита «Описание товарного знака Союза» (ipcdo:TMDescriptionDetails) должны быть заполнены следующие реквизиты: «Описание» (csdo:DescriptionText); «Описание элемента товарного знака Союза» (ipcdo:TMElementDetails), в составе которого должны быть заполнены следующие реквизиты: «Код изобразительного элемента товарного знака» (ipsdo:TrademarkCFECode); «Обозначение» (csdo:DesignationName); «Перевод словесного элемента обозначения» (ipsdo:TMLocalizedName); «Транслитерация словесного элемента обозначения» (ipsdo:TMTransliterationName)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.002 → P.SP.02.MSG.003 → P.SP.02.MSG.003:37:15

## XML

- Structure: R.010
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 529
- Printed page: 117
- Table/item: Table 37, item 15
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_529]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "15", "location": "Таблица 37. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 529, "source_id": "22OP-RULE-P.SP.02.MSG.003-T37-15", "status": "CONFIRMED", "table": "37", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "15", "location": "Таблица 37. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 529, "source_id": "22OP-RULE-P.SP.02.MSG.003-T37-15", "status": "CONFIRMED", "table": "37", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["37"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
