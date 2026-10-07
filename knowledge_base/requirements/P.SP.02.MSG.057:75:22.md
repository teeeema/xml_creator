---
id: "P.SP.02.MSG.057:75:22"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.057"
requirement: "22"
structure: "R.IP.SP.03.003"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 808
source_table: "Table 75, item 22"
source_item: "REQ 22 (Table 75)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.057:75:22

## Нормативное требование

если значение реквизита реквизит «Признак подтверждения уплаты пошлины» (ipsdo:DutyPaymentIndicator) соответствует значению «ложь (false)», значение реквизита «Сумма платежа» (csdo:PaymentAmount) должно быть заполнено и содержать значение, большее, чем «0»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.035 → P.SP.02.TRN.050 → P.SP.02.MSG.057 → P.SP.02.MSG.057:75:22

## XML

- Structure: R.IP.SP.03.003
- QName: ipsdo:DutyPaymentIndicator
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:DutyPaymentIndicator

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 808
- Printed page: 229
- Table/item: Table 75, item 22
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_808]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.057.T75.REQ.22
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 75", "page": 808, "source_id": "22OP-RULE-P.SP.02.MSG.057-T75-22", "status": "CONFIRMED", "table": "75", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "22", "location": "Таблица 75", "page": 808, "source_id": "22OP-RULE-P.SP.02.MSG.057-T75-22", "status": "CONFIRMED", "table": "75", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["75"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg057_end_to_end.py; P.SP.02_OP_22/tests/test_msg057_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg057_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
