---
id: "P.SP.02.MSG.020:53:26"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.020"
requirement: "26"
structure: "R.IP.SP.02.007"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 572
source_table: "Table 53, item 26"
source_item: "REQ 26 (Table 53)"
qname_status: "UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.020:53:26

## Нормативное требование

При отсутствии указанного вида документа IPDocKindCode не заполняется, IPDocKindName заполняется нормативным наименованием.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.029 → P.SP.02.TRN.018 → P.SP.02.MSG.020 → P.SP.02.MSG.020:53:26

## XML

- Structure: R.IP.SP.02.007
- QName: UNRESOLVED: see canonical source row
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 572
- Printed page: 160
- Table/item: Table 53, item 26
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_572]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: P.SP.02.MSG.020.T53.REQ.26
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "26", "location": "Таблица 53", "page": 572, "source_id": "22OP-RULE-P.SP.02.MSG.020-T53-26", "status": "CONFIRMED", "table": "53", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "26", "location": "Таблица 53", "page": 572, "source_id": "22OP-RULE-P.SP.02.MSG.020-T53-26", "status": "CONFIRMED", "table": "53", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["53"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg020_end_to_end.py; P.SP.02_OP_22/tests/test_msg020_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg020_safe_mapping.py

## Gap

- Reason: OTHER_OPEN
- Missing information: Only SAFE_PARTIAL/partial production fragments exist; whole requirement is not certified. No extra normative interpretation performed.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
