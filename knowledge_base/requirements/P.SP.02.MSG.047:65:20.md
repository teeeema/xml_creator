---
id: "P.SP.02.MSG.047:65:20"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.047"
requirement: "20"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 781
source_table: "Table 65, item 20"
source_item: "REQ 20 (Table 65)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.047:65:20

## Нормативное требование

в составе реквизита «Сведения о преобразовании объекта интеллектуальной собственности в другой объект интеллектуальной собственности» (ipcdo:TransformationDetails) должны быть заполнены реквизиты: «Наименование вида преобразования объекта интеллектульной собственности» (ipsdo:TransformationKindName); «Регистрационный номер объекта интеллектуальной собственности» (ipsdo:IPObjectId); Дата (csdo:EventDate)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.024 → P.SP.02.TRN.042 → P.SP.02.MSG.047 → P.SP.02.MSG.047:65:20

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 781
- Printed page: 202
- Table/item: Table 65, item 20
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_781]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "20", "location": "Таблица 65", "page": 781, "source_id": "22OP-RULE-P.SP.02.MSG.047-T65-20", "status": "CONFIRMED", "table": "65", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "20", "location": "Таблица 65", "page": 781, "source_id": "22OP-RULE-P.SP.02.MSG.047-T65-20", "status": "CONFIRMED", "table": "65", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["65"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
