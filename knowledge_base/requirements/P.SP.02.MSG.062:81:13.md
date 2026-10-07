---
id: "P.SP.02.MSG.062:81:13"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.062"
requirement: "13"
structure: "R.IP.SP.02.002"
status: "OPEN_NORMATIVE_AMBIGUITY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 818
source_table: "Table 81, item 13"
source_item: "REQ 13 (Table 81)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_NORMATIVE_AMBIGUITY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.062:81:13

## Нормативное требование

значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) должно соответствовать значению «AP» – «заявитель»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_NORMATIVE_AMBIGUITY

## Trace

OP22 → P.SP.02.PRC.009 → P.SP.02.TRN.053 → P.SP.02.MSG.062 → P.SP.02.MSG.062:81:13

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPPartyKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 818
- Printed page: 239
- Table/item: Table 81, item 13
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_818]]

## Project state

- Status: OPEN_NORMATIVE_AMBIGUITY
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 81. Требования к заполнению реквизитов структуры данных R.IP.SP.02.002 при передаче сведений об обращении о несоответствии заявки на товарный знак Союза требованиям Договора (P.SP.02.MSG.062)", "page": 818, "source_id": "22OP-RULE-P.SP.02.MSG.062-T81-6-29", "status": "CONFIRMED", "table": "81", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 81. Требования к заполнению реквизитов структуры данных R.IP.SP.02.002 при передаче сведений об обращении о несоответствии заявки на товарный знак Союза требованиям Договора (P.SP.02.MSG.062)", "page": 818, "source_id": "22OP-RULE-P.SP.02.MSG.062-T81-6-29", "status": "CONFIRMED", "table": "81", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["81"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg062_end_to_end.py; P.SP.02_OP_22/tests/test_msg062_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg062_safe_mapping.py

## Gap

- Reason: OPEN_NORMATIVE_AMBIGUITY
- Missing information: Normative scope remains ambiguous; current capture/inventory does not authorize a guessed executable rule.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: An authoritative normative clarification resolves the ambiguity; the selected interpretation is traced to that source and regression-tested.
