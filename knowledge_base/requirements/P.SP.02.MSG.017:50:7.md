---
id: "P.SP.02.MSG.017:50:7"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.017"
requirement: "7"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 528
source_table: "Table 37, item 7"
source_item: "REQ 7 (Table 50)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.017:50:7

## Нормативное требование

если реквизит «Адрес» (ccdo:SubjectAddressDetails) заполнен в составе любых реквизитов, в его составе должны быть заполнены реквизиты «Код вида адреса» (csdo:AddressKindCode)», «Код страны» (csdo:UnifiedCountryCode), «Город» (csdo:CityName), «Улица» (csdo:StreetName) и «Номер дома» (csdo:BuildingNumberId)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.025 → P.SP.02.TRN.015 → P.SP.02.MSG.017 → P.SP.02.MSG.017:50:7

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 528
- Printed page: 116
- Table/item: Table 37, item 7
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 50 item 7 via range 6-19 (PDF p.564)
- Inherited source chain: 37
- Source page: [[sources/OP22_P_SP_02/pages/page_528]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 50", "page": 564, "source_id": "22OP-RULE-P.SP.02.MSG.017-T50-6-19", "status": "CONFIRMED", "table": "50", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "7", "location": "Таблица 37. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 528, "source_id": "22OP-RULE-P.SP.02.MSG.003-T37-7", "status": "CONFIRMED", "table": "37", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["37"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
