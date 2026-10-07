---
id: "P.SP.02.MSG.054:72:5"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.054"
requirement: "5"
structure: "R.IP.SP.03.003"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 802
source_table: "Table 72, item 5"
source_item: "REQ 5 (Table 72)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.054:72:5

## Нормативное требование

при отсутствии справочника видов юридически значимых действий при регистрации, правовой охране и использовании товарных знаков Союза, знаков обслуживания Союза и НМПТ Союза в составе ресурсов единой системы нормативно-справочной информации Союза, реквизит «Код вида юридически значимого действия» (ipsdo:IPLegalActionKindCode) не заполняется, а реквизит «Наименование вида юридически значимого действия» (ipsdo:IPLegalActionKindName) должен быть заполнен и должен соответствовать значению, соответствующему одному из следующих видов документов: «Экспертиза обозначения, заявленного на регистрацию в качестве товарного (коллективного) знака Союза (если регистрация испрашивается для одного - трех классов МКТУ) (уплата пошлины в каждое национальное патентное ведомство)»; «Экспертиза обозначения, заявленного на регистрацию в качестве товарного (коллективного) знака Союза (если регистрация испрашивается более чем для трех классов МКТУ) (уплата пошлины в каждое национальное патентное ведомство)»; «Регистрация товарного (коллективного) знака Союза и выдача свидетельства на товарный (коллективный) знак Союза»; «Продление срока действия исключительного права на товарный (коллективный) знак Союза (оплата в каждое национальное патентное ведомство)»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.033 → P.SP.02.TRN.049 → P.SP.02.MSG.054 → P.SP.02.MSG.054:72:5

## XML

- Structure: R.IP.SP.03.003
- QName: ipsdo:IPLegalActionKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPLegalActionKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 802
- Printed page: 223
- Table/item: Table 72, item 5
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_802]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.054.T72.REQ.5.PRESENCE; P.SP.02.MSG.054.T72.REQ.5.VALUE
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 72", "page": 802, "source_id": "22OP-RULE-P.SP.02.MSG.054-T72-5", "status": "CONFIRMED", "table": "72", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 72", "page": 802, "source_id": "22OP-RULE-P.SP.02.MSG.054-T72-5", "status": "CONFIRMED", "table": "72", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["72"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg054_end_to_end.py; P.SP.02_OP_22/tests/test_msg054_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg054_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
