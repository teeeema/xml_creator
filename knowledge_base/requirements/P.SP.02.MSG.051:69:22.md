---
id: "P.SP.02.MSG.051:69:22"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.051"
requirement: "22"
structure: "R.IP.SP.02.007"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 792
source_table: "Table 69, item 22"
source_item: "REQ 22 (Table 69)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.051:69:22

## Нормативное требование

если в составе реквизита «Сведения о подписании документа» (ipcdo:SignatureDetails) заполнен реквизит «Сотрудник организации» (ipcdo:OfficerDetails), в его составе должны быть заполнены реквизиты «Фамилия» (csdo:LastName), «Имя» (csdo:FirstName) и «Наименование должности» (csdo:PositionName), а реквизит «Контактный реквизит» (ccdo:CommunicationDetails) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.028 → P.SP.02.TRN.046 → P.SP.02.MSG.051 → P.SP.02.MSG.051:69:22

## XML

- Structure: R.IP.SP.02.007
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 792
- Printed page: 213
- Table/item: Table 69, item 22
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_792]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 69", "page": 792, "source_id": "22OP-RULE-P.SP.02.MSG.051-T69-22", "status": "CONFIRMED", "table": "69", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 69", "page": 792, "source_id": "22OP-RULE-P.SP.02.MSG.051-T69-22", "status": "CONFIRMED", "table": "69", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["69"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
