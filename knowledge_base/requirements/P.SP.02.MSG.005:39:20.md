---
id: "P.SP.02.MSG.005:39:20"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.005"
requirement: "20"
structure: "R.IP.SP.02.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 517
source_table: "Table 34, item 20"
source_item: "REQ 20 (Table 39)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.005:39:20

## Нормативное требование

если в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «AP» – «заявитель», то в составе реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails) в составе реквизита «Адрес» (ccdo:SubjectAddressDetails) значение реквизита «Код вида адреса» (csdo:AddressKindCode) должно соответствовать значению «2» – «фактический адрес (адрес места нахождения или места жительства)»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.009 → P.SP.02.TRN.004 → P.SP.02.MSG.005 → P.SP.02.MSG.005:39:20

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode; ccdo:SubjectAddressDetails; csdo:AddressKindCode
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 517
- Printed page: 105
- Table/item: Table 34, item 20
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 39 item 20 via range 6-29 (PDF p.536)
- Inherited source chain: 34
- Source page: [[sources/OP22_P_SP_02/pages/page_517]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 39. Требования к электронному документу (сведениям) P.SP.02.MSG.005", "page": 536, "source_id": "22OP-RULE-P.SP.02.MSG.005-T39-6-29", "status": "CONFIRMED", "table": "39", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "20", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 517, "source_id": "22OP-RULE-P.SP.02.MSG.001-20", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg005_end_to_end.py; P.SP.02_OP_22/tests/test_msg005_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg005_safe_mapping.py

## Gap

- Reason: OTHER_OPEN
- Missing information: No executable production rule for this expanded source row. Generic capability availability is not production integration.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
