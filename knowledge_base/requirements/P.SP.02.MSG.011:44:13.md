---
id: "P.SP.02.MSG.011:44:13"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.011"
requirement: "13"
structure: "R.IP.SP.02.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 515
source_table: "Table 34, item 13"
source_item: "REQ 13 (Table 44)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.011:44:13

## Нормативное требование

значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) должно соответствовать значению «AP» – «заявитель»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.019 → P.SP.02.TRN.009 → P.SP.02.MSG.011 → P.SP.02.MSG.011:44:13

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPPartyKindCode
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 515
- Printed page: 103
- Table/item: Table 34, item 13
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 44 item 13 via range 6-29 (PDF p.549)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_515]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 44. Требования к электронному документу (сведениям) P.SP.02.MSG.011", "page": 549, "source_id": "22OP-RULE-P.SP.02.MSG.011-T44-6-29", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "13", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 515, "source_id": "22OP-RULE-P.SP.02.MSG.001-13", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg011_014_end_to_end.py; P.SP.02_OP_22/tests/test_msg011_014_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg011_014_safe_mapping.py

## Gap

- Reason: OTHER_OPEN
- Missing information: No executable production rule for this expanded source row. Generic capability availability is not production integration.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
