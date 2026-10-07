---
id: "P.SP.02.MSG.007:41:18"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.007"
requirement: "18"
structure: "R.IP.SP.02.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 516
source_table: "Table 34, item 18"
source_item: "REQ 18 (Table 41)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.007:41:18

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель» и, если в составе реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName) значение атрибута «код языка» (атрибут languageCode) соответствует значению «RU», второй экземпляр реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.014 → P.SP.02.TRN.006 → P.SP.02.MSG.007 → P.SP.02.MSG.007:41:18

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ipsdo:IPSubjectName
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 516
- Printed page: 104
- Table/item: Table 34, item 18
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 41 item 18 via range 6-29 (PDF p.542)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_516]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 41. Требования к электронному документу (сведениям) P.SP.02.MSG.007", "page": 542, "source_id": "22OP-RULE-P.SP.02.MSG.007-T41-6-29", "status": "CONFIRMED", "table": "41", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "18", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 516, "source_id": "22OP-RULE-P.SP.02.MSG.001-18", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OTHER_OPEN
- Missing information: No executable production rule for this expanded source row. Generic capability availability is not production integration.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
