---
id: "P.SP.03.MSG.005.REQ.001"
op: "OP23"
process: "P.SP.03"
message: "P.SP.03.MSG.005"
requirement: "001"
structure: "R.IP.SP.03.001"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF"
source_document: "ОП_23.pdf"
source_pages: 374
source_table: "Таблица 19. Требования к электронному документу (сведениям) P.SP.03.MSG.005; item 1"
source_item: ""
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.03.MSG.005.REQ.001

## Нормативное требование

в электронном документе (сведениях) должно быть заполнено 2 экземпляра реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» (ipcdo:ApellationOfOriginApplicationDetails), содержащих соответственно изменяемые сведения о заявке на НМПТ Союза и сведения о заявке на НМПТ Союза, содержащие информацию об отказе в регистрации и (или) предоставлении права использования НМПТ Союза или о том, что заявка на НМПТ Союза считается отозванной (далее - измененные сведения о заявке на НМПТ Союза), в составе которых должны совпадать значения реквизитов: «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) (в случае заполнения этого реквизита в экземплярах реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» (ipcdo:ApellationOfOriginApplicationDetails)); «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) (в случае заполнения этого реквизита в экземплярах реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» (ipcdo:ApellationOfOriginApplicationDetails)); «Номер документа» (csdo:DocId); «Дата поступления документа» (ipsdo:IPDocReceiptDate); «Дата подачи заявки» (ipsdo:ApplicationReceiptDate); «Регистрационный номер заявки на НМПТ Союза» (ipsdo:ApellationOfOriginApplicationId); «Код страны» (csdo:UnifiedCountryCode) в составе реквизита «Национальное патентное ведомство» (ipcdo:PatentAuthorityDetails); «Наименование обозначения НМПТ» (ipsdo:ApellationOfOriginName; «Регистрационный номер НМПТ Союза»; (ipsdo:ApellationOfOriginEAEUId) (в случае заполнения этого реквизита в экземплярах реквизита «Заявка на НМПТ Союза (ходатайство, свидетельство)» (ipcdo:ApellationOfOriginApplicationDetails)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Требование проверяется исполняемым OP23 structured rule; положительный XML проходит, отрицательный даёт ожидаемый rule ID.

## Trace

OP23 → P.SP.03.PRC.004 → P.SP.03.TRN.004 → P.SP.03.MSG.005 → P.SP.03.MSG.005.REQ.001

## XML

- Structure: R.IP.SP.03.001
- QName: ipcdo:ApellationOfOriginApplicationDetails; ipsdo:IPDocKindCode; ipsdo:IPDocKindName; csdo:DocId; ipsdo:IPDocReceiptDate; ipsdo:ApplicationReceiptDate; ipsdo:ApellationOfOriginApplicationId; csdo:UnifiedCountryCode; ipcdo:PatentAuthorityDetails; ipsdo:ApellationOfOriginName; ipsdo:ApellationOfOriginEAEUId
- Namespace: MISSING / UNRESOLVED
- Path: UNCONFIRMED_NOT_MAPPED

## Source

- Document: ОП_23.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 374
- Printed page: 85
- Table/item: Таблица 19. Требования к электронному документу (сведениям) P.SP.03.MSG.005; item 1
- Evidence level: CONFIRMED_PDF
- Source page: [[sources/OP23_P_SP_03/pages/page_374]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.03.MSG.005.REQ.001.cardinality;P.SP.03.MSG.005.REQ.001.ip_doc_kind_code;P.SP.03.MSG.005.REQ.001.ip_doc_kind_name;P.SP.03.MSG.005.REQ.001.doc_id;P.SP.03.MSG.005.REQ.001.receipt_date;P.SP.03.MSG.005.REQ.001.application_date;P.SP.03.MSG.005.REQ.001.application_id;P.SP.03.MSG.005.REQ.001.authority_country;P.SP.03.MSG.005.REQ.001.origin_name;P.SP.03.MSG.005.REQ.001.origin_id
- Wiring: 23OP-RULE-P.SP.03.MSG.005-1;23OP-TRN-P-SP-03-TRN-004;23OP-PRC-P-SP-03-PRC-004
- Positive test: PASS — real XML extracted and accepted by production validator
- Negative test: PASS — real XML violation produces matching STRUCTURED_RULE_FAILED
- Runtime proof: P.SP.03_OP_23/tests/test_b1_production.py (message-specific/parametrized real-XML regression)

## Gap

- Reason: Production structured rule wired; positive and negative real XML accepted/rejected by production validator.
- Missing information: None for the implemented local check.
- Required action: Maintain regression coverage.
- Closure criterion: SATISFIED: production rule, runtime wiring, positive and negative XML proof.
