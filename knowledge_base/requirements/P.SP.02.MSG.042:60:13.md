---
id: "P.SP.02.MSG.042:60:13"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.042"
requirement: "13"
structure: "R.IP.SP.02.002"
status: "OPEN_NORMATIVE_AMBIGUITY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 716
source_table: "Table 44, item 13"
source_item: "REQ 13 (Table 60)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_NORMATIVE_AMBIGUITY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.042:60:13

## Нормативное требование

значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) должно соответствовать значению «AP» – «заявитель»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_NORMATIVE_AMBIGUITY

## Trace

OP22 → P.SP.02.PRC.019 → P.SP.02.TRN.037 → P.SP.02.MSG.042 → P.SP.02.MSG.042:60:13

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPPartyKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 716
- Printed page: 137
- Table/item: Table 44, item 13
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 60 item 13 via range 6-29 (PDF p.766)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_716]]

## Project state

- Status: OPEN_NORMATIVE_AMBIGUITY
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 60", "page": 766, "source_id": "22OP-RULE-P.SP.02.MSG.042-T60-6-29", "status": "CONFIRMED", "table": "60", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "13", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 716, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-13", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg042_end_to_end.py; P.SP.02_OP_22/tests/test_msg042_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg042_safe_mapping.py

## Gap

- Reason: OPEN_NORMATIVE_AMBIGUITY
- Missing information: Normative scope remains ambiguous; current capture/inventory does not authorize a guessed executable rule.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: An authoritative normative clarification resolves the ambiguity; the selected interpretation is traced to that source and regression-tested.
