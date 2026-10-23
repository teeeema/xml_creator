# P.SP.02.MSG.001 — effective field policy implementation

Target: `P.SP.02.TRN.001 / P.SP.02.MSG.001 / R.IP.SP.02.002`.

## Result

- Table 34 requirements captured in production message rules: **39**.
- Requirements represented by the declarative message-field policy: **39/39**.
- Presentation fields in R.IP.SP.02.002: **404**.
- Fields with an effective policy: **404**.
- Policy distribution: REQUIRED=20, OPTIONAL=145, FORBIDDEN=147, FIXED=16, CONDITIONAL=76.

## Architecture

`StructureDefinition + MessageFieldPolicyDefinition -> MessageFieldPolicyResolver -> FieldView -> GUI/controller/generation trust boundaries`. The structure remains the source of field identity, datatype and multiplicity. The message dataset overlays only message-specific usage semantics. No field was removed from the structure.

The loader reads optional `message_field_policies/*.yaml`. Because only `P.SP.02.MSG.001` has a dataset, messages without a dataset continue through the legacy form and generation path.

## Runtime behavior

- FORBIDDEN fields stay in the structure but are hidden in the form and removed from draft/test/generation value maps before validation or serialization.
- FIXED fields are visible, read-only and forced to the normative value at the application trust boundary. Conditional fixed attributes are materialized only when their containing field/group is present.
- REQUIRED fields are marked in the form and missing required leaves receive `MESSAGE_POLICY_REQUIRED` in addition to existing production validation.
- CONDITIONAL fields stay visible and editable with human-readable condition text. Unresolved classifier/source branches are not auto-selected and receive no fabricated value.
- MSG.002 has no message-specific dataset and remains on the legacy path.

## Normative uncertainty preserved

`IPDocKindCode/IPDocKindName` remain conditional because the authoritative Decision No. 92 classifier payload is absent. REQ.013 remains instance-specific because AP/PA/RE share one flat path. REQ.027 retains its source conflict. REQ.030 retains the source/structure conflict for `InconsistencyText`; the prohibition stated inside `GoodsBaseDetails` is not projected onto the structurally different top-level path. Decision No. 184 classifier logic and external registry/uniqueness checks are not invented.

## Presentation

The field-info panel keeps the four base sections (`Имя реквизита`, `Описание реквизита`, `Тип данных`, `Множитель`) and adds only `Правило заполнения в MSG.001`. Unicode noncharacters are sanitized in presentation text only; source definitions are unchanged.
