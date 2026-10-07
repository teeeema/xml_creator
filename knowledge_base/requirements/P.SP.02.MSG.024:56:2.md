---
id: "P.SP.02.MSG.024:56:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.024"
requirement: "2"
structure: "R.IP.SP.02.008"
status: "OPEN_SOURCE_CONFLICT"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 577
source_table: "Table 56, item 2"
source_item: "REQ 2 (Table 56)"
qname_status: "CONFLICT"
implementation_status: "OPEN_SOURCE_CONFLICT"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.024:56:2

## Нормативное требование

ipcdo:AccompanyingDocumentsDetails и ipsdo:ApellationOfOriginApplicationId не заполняются.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_SOURCE_CONFLICT

## Trace

OP22 → P.SP.02.PRC.032 → P.SP.02.TRN.021 → P.SP.02.MSG.024 → P.SP.02.MSG.024:56:2

## XML

- Structure: R.IP.SP.02.008
- QName: ipcdo:AccompanyingDocumentsDetails; ipsdo:ApellationOfOriginApplicationId
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:AccompanyingDocumentsDetails; ipsdo:ApellationOfOriginApplicationId

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 577
- Printed page: 165
- Table/item: Table 56, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_577]]

## Project state

- Status: OPEN_SOURCE_CONFLICT
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 56", "page": 577, "source_id": "22OP-RULE-P.SP.02.MSG.024-T56-2", "status": "CONFIRMED", "table": "56", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 56", "page": 577, "source_id": "22OP-RULE-P.SP.02.MSG.024-T56-2", "status": "CONFIRMED", "table": "56", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["56"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg024_end_to_end.py; P.SP.02_OP_22/tests/test_msg024_safe_mapping.py

## Gap

- Reason: OPEN_SOURCE_CONFLICT
- Missing information: PDF ApellationOfOriginApplicationId has no exact production StructureDefinition path.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: A higher-priority authoritative source resolves the conflicting values; provenance is recorded and the conflicting mapping is replaced with the confirmed one.
