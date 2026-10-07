---
id: "P.SP.02.MSG.006:40:17"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.006"
requirement: "17"
structure: "R.IP.SP.02.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 516
source_table: "Table 34, item 17"
source_item: "REQ 17 (Table 40)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.006:40:17

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должен быть заполнен 1 экземпляр реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName), в составе которого значение атрибута «код вида представления наименования» (атрибут nameRepresentationKindCode) должно соответствовать значению «OR» – «сведения, представленные на исходном (оригинальном) языке» и атрибут «код языка» (атрибут languageCode) должен быть заполнен

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.010 → P.SP.02.TRN.005 → P.SP.02.MSG.006 → P.SP.02.MSG.006:40:17

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
- Table/item: Table 34, item 17
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 40 item 17 via range 6-29 (PDF p.540)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_516]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 40. Требования к электронному документу (сведениям) P.SP.02.MSG.006", "page": 540, "source_id": "22OP-RULE-P.SP.02.MSG.006-T40-6-29", "status": "CONFIRMED", "table": "40", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "17", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 516, "source_id": "22OP-RULE-P.SP.02.MSG.001-17", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg006_010_end_to_end.py; P.SP.02_OP_22/tests/test_msg006_010_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg006_010_safe_mapping.py

## Gap

- Reason: OTHER_OPEN
- Missing information: No executable production rule for this expanded source row. Generic capability availability is not production integration.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
