---
id: "P.SP.02.MSG.045:63:30"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.045"
requirement: "30"
structure: "R.IP.SP.02.002"
status: "OPEN_NORMATIVE_AMBIGUITY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 776
source_table: "Table 63, item 30"
source_item: "REQ 30 (Table 63)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_NORMATIVE_AMBIGUITY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.045:63:30

## Нормативное требование

если значение реквизита «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode), «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) в составе реквизита реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» соответствует значению «Ходатайство о внесении в заявку на регистрацию товарного знака, знака обслуживания Евразийского экономического союза изменений, касающихся сведений о заявителе и связанных с передачей или переходом права на заявку на регистрацию товарного знака, знака обслуживания Евразийского экономического союза», а значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению значению «AS» – «правопреемник» то в составе реквизита «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails) должна быть хотя бы одна запись, у которой значения реквизитов «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode), «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) соответствуют значению вида документа «Другой документ о передаче (переходе) права на заявку на товарный знак (знак обслуживания) Евразийского экономического союза»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_NORMATIVE_AMBIGUITY

## Trace

OP22 → P.SP.02.PRC.022 → P.SP.02.TRN.040 → P.SP.02.MSG.045 → P.SP.02.MSG.045:63:30

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPPartyKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 776
- Printed page: 197
- Table/item: Table 63, item 30
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_776]]

## Project state

- Status: OPEN_NORMATIVE_AMBIGUITY
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "30", "location": "Таблица 63", "page": 776, "source_id": "22OP-RULE-P.SP.02.MSG.045-T63-30", "status": "CONFIRMED", "table": "63", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "30", "location": "Таблица 63", "page": 776, "source_id": "22OP-RULE-P.SP.02.MSG.045-T63-30", "status": "CONFIRMED", "table": "63", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["63"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg045_end_to_end.py; P.SP.02_OP_22/tests/test_msg045_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg045_safe_mapping.py

## Gap

- Reason: OPEN_NORMATIVE_AMBIGUITY
- Missing information: Transfer-document semantic role/scope requires clarification and classifier identification; no normative approximation.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: An authoritative normative clarification resolves the ambiguity; the selected interpretation is traced to that source and regression-tested.
