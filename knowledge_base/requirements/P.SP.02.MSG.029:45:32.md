---
id: "P.SP.02.MSG.029:45:32"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.029"
requirement: "32"
structure: "R.IP.SP.02.002"
status: "OPEN_SOURCE_CONFLICT"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 552
source_table: "Table 45, item 32"
source_item: "REQ 32 (Table 45)"
qname_status: "CONFLICT"
implementation_status: "OPEN_SOURCE_CONFLICT"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.029:45:32

## Нормативное требование

ipsdo:TrademarkApplicationId заполняется для обеих заявок; для ранее поданной должна существовать активная запись со статусом «01»/«02» и совпадающим номером, для выделенной записи с таким номером существовать не должно

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_SOURCE_CONFLICT

## Trace

OP22 → P.SP.02.PRC.003 → P.SP.02.TRN.024 → P.SP.02.MSG.029 → P.SP.02.MSG.029:45:32

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:InconsistencyText
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipsdo:InconsistencyText

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 552
- Printed page: 140
- Table/item: Table 45, item 32
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_552]]

## Project state

- Status: OPEN_SOURCE_CONFLICT
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 45", "page": 726, "source_id": "22OP-RULE-P.SP.02.MSG.029-T45-32", "status": "CONFIRMED", "table": "45", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 45. Требования к электронному документу (сведениям) P.SP.02.MSG.012", "page": 552, "source_id": "22OP-RULE-P.SP.02.MSG.012-T45-32", "status": "CONFIRMED", "table": "45", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["45"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg029_end_to_end.py; P.SP.02_OP_22/tests/test_msg029_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg029_safe_mapping.py

## Gap

- Reason: OPEN_SOURCE_CONFLICT
- Missing information: Source/StructureDefinition owner or QName conflict retained; see source refs and original gap notes.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: A higher-priority authoritative source resolves the conflicting values; provenance is recorded and the conflicting mapping is replaced with the confirmed one.
