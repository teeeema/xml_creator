---
id: "P.SP.02.MSG.020:53:18"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.020"
requirement: "18"
structure: "R.IP.SP.02.007"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 530
source_table: "Table 37, item 18"
source_item: "REQ 18 (Table 53)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.020:53:18

## Нормативное требование

если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) соответствует значению «1» – «товарный знак является коллективным», то должен быть заполнен хотя бы 1 экземпляр реквизита «Участник отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipcdo:IPPartyDetails), в составе которого значение реквизита «Код вида участника отношений в сфере регистрации и использования прав на объекты интеллектуальной собственности» (ipsdo:IPPartyKindCode) соответствует значению «UE» – «лицо, имеющее право использования коллективного знака Союза»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.029 → P.SP.02.TRN.018 → P.SP.02.MSG.020 → P.SP.02.MSG.020:53:18

## XML

- Structure: R.IP.SP.02.007
- QName: ipcdo:TrademarkDetails; ipsdo:CollectiveMarkIndicator; ipcdo:IPPartyDetails; ipsdo:IPPartyKindCode
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 530
- Printed page: 118
- Table/item: Table 37, item 18
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 53 item 18 via range 6-19 (PDF p.570)
- Inherited source chain: 37
- Source page: [[sources/OP22_P_SP_02/pages/page_530]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: P.SP.02.MSG.020.T53.REQ.6_19
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 53", "page": 570, "source_id": "22OP-RULE-P.SP.02.MSG.020-T53-6-19", "status": "CONFIRMED", "table": "53", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "18", "location": "Таблица 37. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 530, "source_id": "22OP-RULE-P.SP.02.MSG.003-T37-18", "status": "CONFIRMED", "table": "37", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["37"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg020_end_to_end.py; P.SP.02_OP_22/tests/test_msg020_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg020_safe_mapping.py

## Gap

- Reason: OTHER_OPEN
- Missing information: Only SAFE_PARTIAL/partial production fragments exist; whole requirement is not certified. No extra normative interpretation performed.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
