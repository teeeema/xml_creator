---
id: "P.SP.02.MSG.052:70:23"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.052"
requirement: "23"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 795
source_table: "Table 70, item 23"
source_item: "REQ 23 (Table 70)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.052:70:23

## Нормативное требование

в составе экземпляра реквизита «Сведения записи Единого реестра ТЗ Союза» (ipcdo:UnifiedRegisterRecordsDetails), содержащего сведения об аннулировании регистрации ТЗ Союза, в составе реквизита «Основание для аннулирования регистрации товарного знака Союза» (ipcdo:RegistrationCancellationDetails) должны быть заполнены реквизиты: «Код вида оснований для аннулирования регистрации товарного знака Союза» (ipsdo:CancellationRegistrationTrademarkCode); «Код вида решения по аннулированию регистрации товарного знака Союза» (ipsdo:SolutionCancellationRegistrationTrademarkCode)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.029 → P.SP.02.TRN.047 → P.SP.02.MSG.052 → P.SP.02.MSG.052:70:23

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 795
- Printed page: 216
- Table/item: Table 70, item 23
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_795]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "23", "location": "Таблица 70", "page": 795, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-23", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "23", "location": "Таблица 70", "page": 795, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-23", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["70"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
