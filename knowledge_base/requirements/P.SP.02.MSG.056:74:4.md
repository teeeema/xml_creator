---
id: "P.SP.02.MSG.056:74:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.056"
requirement: "4"
structure: "R.IP.SP.03.003"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 802
source_table: "Table 72, item 4"
source_item: "REQ 4 (Table 74)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.056:74:4

## Нормативное требование

при включении справочника видов юридически значимых действий при регистрации, правовой охране и использовании товарных знаков Союза, знаков обслуживания Союза и наименований мест происхождения товаров Союза в состав ресурсов единой системы нормативно-справочной информации Союза, реквизит «Код вида юридически значимого действия» (ipsdo:IPLegalActionKindCode) должен быть заполнен и должен соответствовать значению, соответствующему одному из следующих видов документов: «Экспертиза обозначения, заявленного на регистрацию в качестве товарного (коллективного) знака Союза (если регистрация испрашивается для одного - трех классов МКТУ) (уплата пошлины в каждое национальное патентное ведомство)»; «Экспертиза обозначения, заявленного на регистрацию в качестве товарного (коллективного) знака Союза (если регистрация испрашивается более чем для трех классов МКТУ) (уплата пошлины в каждое национальное патентное ведомство)»; «Регистрация товарного (коллективного) знака Союза и выдача свидетельства на товарный (коллективный) знак Союза»; «Продление срока действия исключительного права на товарный (коллективный) знак Союза (оплата в каждое национальное патентное ведомство)», а реквизит «Наименование вида юридически значимого действия» (ipsdo:IPLegalActionKindName) не заполняется

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.035 → P.SP.02.TRN.050 → P.SP.02.MSG.056 → P.SP.02.MSG.056:74:4

## XML

- Structure: R.IP.SP.03.003
- QName: ipsdo:IPDocKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:PatentAuthorityDetails/ipsdo:IPDocKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 802
- Printed page: 223
- Table/item: Table 72, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 74 item 4 via range 1-6 (PDF p.804)
- Inherited source chain: 72
- Source page: [[sources/OP22_P_SP_02/pages/page_802]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "1-6", "location": "Таблица 74", "page": 804, "source_id": "22OP-RULE-P.SP.02.MSG.056-T74-1-6", "status": "CONFIRMED", "table": "74", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 72", "page": 802, "source_id": "22OP-RULE-P.SP.02.MSG.054-T72-4", "status": "CONFIRMED", "table": "72", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["72"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg056_end_to_end.py; P.SP.02_OP_22/tests/test_msg056_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg056_safe_mapping.py

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Full condition needs external/current or previous registry/resource state unavailable in message XML.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
