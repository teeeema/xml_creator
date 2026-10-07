---
id: "P.SP.02.MSG.047:65:11"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.047"
requirement: "11"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 737
source_table: "Table 49, item 11"
source_item: "REQ 11 (Table 65)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.047:65:11

## Нормативное требование

в электронном документе (сведениях) должен быть заполнен 1 экземпляр реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), в составе которого значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «RH» – «правообладатель»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.024 → P.SP.02.TRN.042 → P.SP.02.MSG.047 → P.SP.02.MSG.047:65:11

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 737
- Printed page: 158
- Table/item: Table 49, item 11
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 65 item 11 via range 6-19 (PDF p.781)
- Inherited source chain: 49
- Source page: [[sources/OP22_P_SP_02/pages/page_737]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 65", "page": 781, "source_id": "22OP-RULE-P.SP.02.MSG.047-T65-6-19", "status": "CONFIRMED", "table": "65", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "11", "location": "Таблица 49", "page": 737, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-11", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
