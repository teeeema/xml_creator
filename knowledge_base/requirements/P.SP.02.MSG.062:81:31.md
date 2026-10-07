---
id: "P.SP.02.MSG.062:81:31"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.062"
requirement: "31"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 819
source_table: "Table 81, item 31"
source_item: "REQ 31 (Table 81)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.062:81:31

## Нормативное требование

в составе реквизита «Сведения об обращении заинтересованного лица о несоответствии обозначения, заявленного на регистрацию в качестве товарного знака Союза, требованиям Договора о товарных знаках» (ipcdo:TrademarkClaimDetails), в составе реквизита «Заинтересованное лицо» (ipcdo:StakeholderDetails) должны быть заполнены следующие реквизиты: «Код страны» (csdo:UnifiedCountryCode); «Наименование субъекта» (csdo:SubjectName); «Краткое наименование субъекта» (csdo:SubjectBriefName); «Адрес» (ccdo:SubjectAddressDetails)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.009 → P.SP.02.TRN.053 → P.SP.02.MSG.062 → P.SP.02.MSG.062:81:31

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 819
- Printed page: 240
- Table/item: Table 81, item 31
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_819]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "31", "location": "Таблица 81", "page": 819, "source_id": "22OP-RULE-P.SP.02.MSG.062-T81-31", "status": "CONFIRMED", "table": "81", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "31", "location": "Таблица 81", "page": 819, "source_id": "22OP-RULE-P.SP.02.MSG.062-T81-31", "status": "CONFIRMED", "table": "81", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["81"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
