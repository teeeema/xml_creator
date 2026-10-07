# OP26 / P.MM.01 — detailed source conflicts

Status: **READ-ONLY AUDIT**. Primary source: `/Users/tema/Documents/Work/Документы_xml/26_ОП.pdf`. No production/KB code was modified.

All five historical conflicts are confirmed. For MSG.023/024, the decisive structure is **R.HC.MM.01.002 Table 13, PDF 415–421 (printed 414–420)**. That table contains only EDocHeader, UnifiedCountryCode, ApplicationId, RegistrationNumberId, DocId, DocName, DrugRegistrationFileCode/Name, DocCreationDate, DocAgreementIndicator, AuthorityDrugConditionalRegistrationIndicator, PdfBinaryText and AnyDetails. It does **not** declare `DrugAttributeEnumText`, `AttributeKindCode` or `AttributeKindName`. Similar names appearing later in the PDF belong to other structures and cannot be imported into R.HC.MM.01.002 by assumption.

## Conflict 1: OP26.P_MM_01.P.MM.01.MSG.002.REQ.022

- **Canonical requirement:** `OP26.P_MM_01.P.MM.01.MSG.002.REQ.022`
- **Message:** `P.MM.01.MSG.002`
- **Filling table:** Table 19 item 22, PDF 219 / printed 218. The filling rule says `hcsdo:ChildJuvenileIndicator` must not be populated.
- **Structure side:** R.HC.MM.01.001 Table 10, PDF 351 / printed 350, fields `*.2.3.2` and `*.2.3.3`. The structure declares separate `hcsdo:ChildIndicator` and `hcsdo:JuvenileIndicator`; `ChildJuvenileIndicator` is not the declared field.
- **Conflict:** the filling rule addresses a field/attribute set that the declared structure does not expose under the same normative structure.
- **Why automatic choice is unsafe:** choosing a replacement field would alter the normative mapping without source authority.
- **What is needed:** Obtain official correction/clarification or revised XSD identifying the intended field.
- **Possible technical option:** NON-NORMATIVE: treat the reference as an alias to `JuvenileIndicator`, or as a combined semantic over ChildIndicator+JuvenileIndicator.
- **Why it is not normative:** The PDF does not state either mapping, so choosing one can change the rule meaning.
- **Normative status:** `UNRESOLVED_SOURCE_CONFLICT`

## Conflict 2: OP26.P_MM_01.P.MM.01.MSG.023.REQ.004

- **Canonical requirement:** `OP26.P_MM_01.P.MM.01.MSG.023.REQ.004`
- **Message:** `P.MM.01.MSG.023`
- **Filling table:** Table 21 item 4, PDF 298 / printed 297. If `DrugAttributeEnumText` is filled, `AttributeKindCode` or `AttributeKindName` must be filled.
- **Structure side:** R.HC.MM.01.002 Table 13, PDF 415–421 / printed 414–420. The declared structure contains no `DrugAttributeEnumText` and no `AttributeKindCode`/`AttributeKindName`.
- **Conflict:** the filling rule addresses a field/attribute set that the declared structure does not expose under the same normative structure.
- **Why automatic choice is unsafe:** choosing a replacement field would alter the normative mapping without source authority.
- **What is needed:** Obtain corrected filling table or revised R.HC.MM.01.002 XSD/structure.
- **Possible technical option:** NON-NORMATIVE: add an alias/virtual field layer matching a similarly named construct from another structure.
- **Why it is not normative:** Cross-structure borrowing is not authorized by the R.HC.MM.01.002 structure definition.
- **Normative status:** `UNRESOLVED_SOURCE_CONFLICT`

## Conflict 3: OP26.P_MM_01.P.MM.01.MSG.023.REQ.005

- **Canonical requirement:** `OP26.P_MM_01.P.MM.01.MSG.023.REQ.005`
- **Message:** `P.MM.01.MSG.023`
- **Filling table:** Table 21 item 5, PDF 298 / printed 297. `AttributeKindCode` or `AttributeKindName` inside `DrugAttributeEnumText` must correspond to “Номер документа основания”.
- **Structure side:** R.HC.MM.01.002 Table 13, PDF 415–421 / printed 414–420. The element/attributes referenced by the filling rule are absent from the declared message structure.
- **Conflict:** the filling rule addresses a field/attribute set that the declared structure does not expose under the same normative structure.
- **Why automatic choice is unsafe:** choosing a replacement field would alter the normative mapping without source authority.
- **What is needed:** Obtain official correction/clarification defining the intended target field(s).
- **Possible technical option:** NON-NORMATIVE: map the semantic to another available document attribute after external confirmation.
- **Why it is not normative:** No such mapping is stated in the normative source.
- **Normative status:** `UNRESOLVED_SOURCE_CONFLICT`

## Conflict 4: OP26.P_MM_01.P.MM.01.MSG.024.REQ.006

- **Canonical requirement:** `OP26.P_MM_01.P.MM.01.MSG.024.REQ.006`
- **Message:** `P.MM.01.MSG.024`
- **Filling table:** Table 22 item 6, PDF 300 / printed 299. If `DrugAttributeEnumText` is filled, one of `AttributeKindCode` or `AttributeKindName` must be filled.
- **Structure side:** R.HC.MM.01.002 Table 13, PDF 415–421 / printed 414–420. The target element and both attributes are absent from R.HC.MM.01.002.
- **Conflict:** the filling rule addresses a field/attribute set that the declared structure does not expose under the same normative structure.
- **Why automatic choice is unsafe:** choosing a replacement field would alter the normative mapping without source authority.
- **What is needed:** Obtain corrected source or revised schema/structure.
- **Possible technical option:** NON-NORMATIVE: introduce an adapter/alias for the missing construct.
- **Why it is not normative:** The adapter would invent structure not declared for this message.
- **Normative status:** `UNRESOLVED_SOURCE_CONFLICT`

## Conflict 5: OP26.P_MM_01.P.MM.01.MSG.024.REQ.007

- **Canonical requirement:** `OP26.P_MM_01.P.MM.01.MSG.024.REQ.007`
- **Message:** `P.MM.01.MSG.024`
- **Filling table:** Table 22 item 7, PDF 300 / printed 299. If `AttributeKindCode` is “другое”, `AttributeKindName` is mandatory.
- **Structure side:** R.HC.MM.01.002 Table 13, PDF 415–421 / printed 414–420. Neither the referenced attribute context nor `DrugAttributeEnumText` exists in the declared structure.
- **Conflict:** the filling rule addresses a field/attribute set that the declared structure does not expose under the same normative structure.
- **Why automatic choice is unsafe:** choosing a replacement field would alter the normative mapping without source authority.
- **What is needed:** Obtain official correction/clarification or revised XSD.
- **Possible technical option:** NON-NORMATIVE: alias the condition to a similarly named attribute from another data model.
- **Why it is not normative:** The source provides no authority for that alias.
- **Normative status:** `UNRESOLVED_SOURCE_CONFLICT`

