---
id: "P.SP.02.MSG.044:62:17"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.044"
requirement: "17"
structure: "R.IP.SP.02.002"
status: "OPEN_SOURCE_CONFLICT"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 717
source_table: "Table 44, item 17"
source_item: "REQ 17 (Table 62)"
qname_status: "CONFLICT"
implementation_status: "OPEN_SOURCE_CONFLICT"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.044:62:17

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) должен быть заполнен 1 экземпляр реквизита «Полное наименование субъекта c указанием вида представления сведений и кода языка» (ipsdo:IPSubjectName), в составе которого значение атрибута «код вида представления наименования» (атрибут nameRepresentationKindCode) должно соответствовать значению «OR» – «сведения, представленные на исходном (оригинальном) языке» и атрибут «код языка» (атрибут languageCode) должен быть заполнен

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_SOURCE_CONFLICT

## Trace

OP22 → P.SP.02.PRC.021 → P.SP.02.TRN.039 → P.SP.02.MSG.044 → P.SP.02.MSG.044:62:17

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:TrademarkApplicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 717
- Printed page: 138
- Table/item: Table 44, item 17
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 62 item 17 via range 6-29 (PDF p.772)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_717]]

## Project state

- Status: OPEN_SOURCE_CONFLICT
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 62", "page": 772, "source_id": "22OP-RULE-P.SP.02.MSG.044-T62-6-29", "status": "CONFIRMED", "table": "62", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "17", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 717, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-17", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg044_end_to_end.py; P.SP.02_OP_22/tests/test_msg044_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg044_safe_mapping.py

## Gap

- Reason: OPEN_SOURCE_CONFLICT
- Missing information: MSG044 captured source_refs identify Table58/physical760 instead of current Table62; no production rule for this requirement.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: A higher-priority authoritative source resolves the conflicting values; provenance is recorded and the conflicting mapping is replaced with the confirmed one.
