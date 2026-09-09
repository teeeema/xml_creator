# P.DS.01 — D1 catalog import report

Источник: `49_OP_CODEX/49_OP_CODEX.md`, первичный нормативный источник — `49_OP_CODEX/49_OP.pdf`.

## Inventory

- PROCESS: `P.DS.01`, version `1.0.0`.
- PRC: 7.
- OPR: 21.
- Participants/ACT: 3 (`P.ACT.001`, `P.DS.01.ACT.001`, `P.DS.01.ACT.002`).
- TRN: 7.
- MSG: 6.
- Unique structures: `R.006/Y.Y.Y`, `R.FP.DS.01.001/1.0.0`, `R.FP.DS.01.003/1.0.0`.
- Imported fields: `R.FP.DS.01.001` — 36; `R.FP.DS.01.003` — 15.

## TRN → MSG

| TRN | Initiating | Response |
|---|---|---|
| TRN.001 | MSG.001 | MSG.003 |
| TRN.002 | MSG.002 | MSG.003 |
| TRN.003 | MSG.002 | MSG.003 |
| TRN.004 | MSG.004 | MSG.003 |
| TRN.005 | MSG.005 | MSG.003 |
| TRN.006 | MSG.005 | MSG.003 |
| TRN.007 | MSG.006 | MSG.003 |

## MSG → R.*

| MSG | Structure | Version |
|---|---|---|
| MSG.001 | R.FP.DS.01.001 | 1.0.0 |
| MSG.002 | R.FP.DS.01.001 | 1.0.0 |
| MSG.003 | R.006 | Y.Y.Y |
| MSG.004 | R.FP.DS.01.003 | 1.0.0 |
| MSG.005 | R.FP.DS.01.001 | 1.0.0 |
| MSG.006 | R.FP.DS.01.001 | 1.0.0 |

## Procedures

`P.DS.01.PRC.001` through `P.DS.01.PRC.007` are present; names and references are in `procedures.yaml`.

## Operations

`P.DS.01.OPR.001` through `P.DS.01.OPR.021` are present; names, executor roles and references are in `operations.yaml`.

## Message-specific rules

Separate tables were identified for MSG.001, MSG.002, MSG.004, MSG.005 and MSG.006. Their rule files are present with `HAS_SEPARATE_RULE_TABLE`. MSG.003 has `NO_SEPARATE_RULE_TABLE`.

The detailed field rows are intentionally not imported at D1 because the structure field tables require a complete verified field map; no fabricated fields were added.

## Unresolved and missing evidence

- `R.006` version is the normative placeholder `Y.Y.Y`.
- Imported model namespaces use the normative placeholder `X.X.X`.
- No concrete process/domain model versions are supplied beyond those placeholders.
- XSD validation is not implemented in D1.1; structures remain marked `NEEDS_XSD`.
- Structure fields are imported from tables 7 and 10. Nested detail tables inside complex elements are not expanded beyond the rows explicitly present in those tables.
- `csdo:UnifiedCountryCode` is preserved as `csdo:UnifiedCountryCodeType`; it was not replaced with `csdo:CountryCode`.
- Message-specific table content is kept separate in `message_rules/`; the current import records table ownership and source references without inventing unparsed field paths.
- No normative value for guaranteed delivery was found; it remains `null`.
- No separate normative participant ACT code beyond the three listed participants was invented.

## PDF cross-checks

The Markdown was used for extraction. The following PDF page/table locations were checked against the primary PDF where structure/table layout mattered: participant table 1 (pages 5–6), procedure table 2 (pages 9–10), transaction mappings (pages 62–64 and 116–117), message table 3 (pages 65–66 and 118), transaction parameter tables 4–8 (pages 67–76 and 119–122), structure tables 1–3, 5–6 and 8–10 (pages 146–190), and message rule tables 10–14 (pages 83–96).

## Loader conflicts and core changes

No `eaeu_xml` files were changed. The current loader contract accepts the package and the explicit local `R.006/Y.Y.Y` definition. `R.006` was not copied from P.MM.01; its metadata comes from 49 ОП.

## Tests

The D1 test covers package loading, registry discovery, code uniqueness, cross-references, structure selection and message-rule ownership. Full test results are reported after execution.
