---
id: "P.SP.02.MSG.006:40:14"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.006"
requirement: "14"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 515
source_table: "Table 34, item 14"
source_item: "REQ 14 (Table 40)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.006:40:14

## Нормативное требование

в электронном документе (сведениях) «Сведения о заявке, ходатайстве для прохождения процедур регистрации ТЗ Союза» (R.IP.SP.02.002) должен быть заполнен 1 экземпляр реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), в составе которого значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.010 → P.SP.02.TRN.005 → P.SP.02.MSG.006 → P.SP.02.MSG.006:40:14

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 515
- Printed page: 103
- Table/item: Table 34, item 14
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 40 item 14 via range 6-29 (PDF p.540)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_515]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 40. Требования к электронному документу (сведениям) P.SP.02.MSG.006", "page": 540, "source_id": "22OP-RULE-P.SP.02.MSG.006-T40-6-29", "status": "CONFIRMED", "table": "40", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "14", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 515, "source_id": "22OP-RULE-P.SP.02.MSG.001-14", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
