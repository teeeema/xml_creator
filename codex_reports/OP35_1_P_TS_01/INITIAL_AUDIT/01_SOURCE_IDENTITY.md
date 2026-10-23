# OP35.1 / P.TS.01 — Source identity

STATUS: CONFIRMED_WITH_EXPLICIT_GAPS

## Scope

- Allowed normative source: `/Users/tema/Documents/Work/Документы_xml/35.1 ОП.pdf`.
- Scope is limited to the part concerning the unified register of issued conformity certificates and registered declarations of conformity.
- This audit does not import facts from other parts of common process No. 35 or from other OPs.
- PDF pages: 99.
- SHA256: `9ae968eb3fda852c1d0e7581782edc5aab09bc93c5feff770fb2ced01376f69e`.

## Decision and revision identity

- Base act: Decision of the Board of the Eurasian Economic Commission No. 39 dated 10 May 2016.
- The title on PDF page 1 is specifically about technological documents for the common process in the part concerning the unified register of issued conformity certificates and registered declarations of conformity.
- PDF page 1 lists amendments: No. 9 dated 24 January 2017, No. 127 dated 26 September 2017, No. 176 dated 19 December 2023, and No. 109 dated 23 September 2024.
- The Rules and the interaction regulations are explicitly marked as being in the edition of Decision No. 109 dated 23 September 2024 (for example PDF pages 3, 10 and 21).
- Therefore `REVISION_IDENTITY = CONFIRMED: Decision No. 109 dated 23.09.2024`.

## Effective-date boundary

- PDF page 2, clause 3 of Decision No. 39 states that Decision No. 39 enters into force after 180 calendar days from the date of its official publication.
- The actual calendar date cannot be derived from this PDF alone without the official-publication date.
- The effective date of Decision No. 109 / the current 2024 revision is not stated in the allowed PDF evidence inspected for this audit.
- `CURRENT_REVISION_EFFECTIVE_DATE = NOT_CONFIRMED_BY_ALLOWED_SOURCE`.

## Process identity

- Full process name: `Формирование и ведение единых реестров выданных или принятых документов об оценке соответствия требованиям технических регламентов Евразийского экономического союза (технических регламентов Таможенного союза)`.
- Scope qualifier: the part concerning the unified register of issued conformity certificates and registered declarations of conformity.
- Process code: `P.TS.01`.
- Process version: `2.0.0`.
- Evidence: PDF page 5, clauses 5–6.

## Decision No. 5 / integration-header boundary

The PDF explicitly references Decision of the Board of the EEC No. 5 dated 27 January 2015, `Об утверждении Правил электронного обмена данными в интегрированной информационной системе внешней и взаимной торговли`, among the governing acts (for example PDF pages 4, 11 and 22).

The concrete integration-related rule confirmed by this PDF is narrower:

- PDF page 14, clause 12: when one role may be performed by several common-process participants, the logical address additionally includes the identifier of the Member State authority or its authorized organization in accordance with clause 52 of the Rules approved by Decision No. 5.
- PDF page 15: that authority/organization identifier is selected in accordance with the reference list named in section VII of the interaction Rules.

This PDF does not itself establish concrete values for `wsa:Action`, `wsa:To`, `wsa:ReplyTo`, `wsa:From`, `wsa:FaultTo`, `wsa:MessageID`, `wsa:RelatesTo`, `int:ProcedureID`, `int:ConversationID`, `TrackID`, `AcceptTime`, or an Action URI for `P.TS.01`. None of those values are imported from OP22 or another OP in this audit.

`INTEGRATION_HEADER_STATUS = PARTIAL_SOURCE_REFERENCE_ONLY`

## Message-catalog boundary

Table 4 on PDF pages 19–20 confirms 11 message codes:

`P.TS.01.MSG.001`, `.002`, `.003`, `.007`, `.008`, `.009`, `.010`, `.011`, `.012`, `.013`, `.014`.

`P.TS.01.MSG.004`, `.005`, and `.006` are not confirmed by table 4 and were not found as message codes in the searchable text of the allowed PDF during this audit. They are therefore not reconstructed or inferred.

- `SOURCE_CONFIRMED_MESSAGES_TOTAL = 11`
- `UNINVENTED_CODE_GAPS = 004,005,006`

## Structure/material boundary relevant to implementability

PDF page 29 lists five structures: `R.004`, `R.006`, `R.007`, `R.TR.TS.01.001`, and `R.TR.TS.01.002`.

- `R.004`, `R.006`, and `R.007` use placeholder version `Y.Y.Y` in the normative description.
- `R.TR.TS.01.001` is version `1.0.3`, namespace `urn:EEC:R:TR:TS:01:ConformityDocsRegistryDetails:v1.0.3`, root `ConformityDocsRegistryDetails`, XSD filename `EEC_R_TR_TS_01_ConformityDocsRegistryDetails_v1.0.3.xsd` (PDF page 44).
- `R.TR.TS.01.002` is version `1.0.0`, namespace `urn:EEC:R:TR:TS:01:ConformityDocsRegistryRequestDetails:v1.0.0`, root `ConformityDocsRegistryRequestDetails`, XSD filename `EEC_R_TR_TS_01_ConformityDocsRegistryRequestDetails_v1.0.0.xsd` (PDF page 90).
- The concrete domain structures import model namespaces whose versions are represented as `X.X.X` and `Z.Z.Z` (PDF pages 44–45 and 90–91).
- The PDF names XSD files but does not contain executable XSD schema files. Under the constraint to work only with this PDF, XSD material is therefore not available for implementation proof.

`IMPLEMENTATION_SOURCE_STATUS = PARTIAL`

