# Decision No. 68 analysis

## Source identity

Primary process source: `normative_sources/err_22042022_68_doc.pdf`, Decision
of the Collegium of the Eurasian Economic Commission dated 19 April 2022
No. 68, "On Amendments to Decision ... dated 25 October 2016 No. 122".

SHA-256: `a15cc6c946b35145e58304b7e3621ea76241f510e2202bbaf8912b4f8b0715e6`.
The source has 465 pages and remains unchanged.

## Process map

- page 6, table 1: process `P.MM.01`, version `1.1.0`;
- pages 19–157: procedure and operation catalog (19 PRC, 57 OPR);
- pages 158–244: interaction regulation between member-state authorities and
  the Commission, including TRN.001–.008 and .017–.019;
- pages 245–300: interaction regulation between member-state authorities,
  including TRN.009–.016;
- pages 177–179 and 265–266: two message lists, together defining 28 MSG;
- pages 180–205 and 267–285: individual transaction parameter tables;
- pages 208–244 and 287–301: message-specific filling requirements;
- pages 307–308, table 1: registry of eight structures;
- pages 308–457: structure metadata, imports and requisite tables.

## Structure versions

The process version is not propagated to structures. `R.006` and `R.007` use
the normative placeholder `Y.Y.Y`, whose value is delegated to the base-model
version. `R.HC.MM.01.001`, `.002`, `.003`, `.004` and `.006` explicitly use
`1.1.0`; `R.HC.MM.01.007` explicitly uses `1.0.0`.

## Catalog boundary

All PRC, OPR, TRN, MSG and structure metadata are transferred. Structure
requisite tables and message-rule tables are indexed by source page/table.
Their field-level transfer now represents 555/555 requisite rows and 201
message-rule rows. The generic engine serializes confirmed definitions, while
ambiguous items remain explicit and non-executable. Physical XSD, classifier
datasets and transport behavior are not implemented.

## Interpretation audit

The original 169 field flags were extraction artifacts, not 169 source
ambiguities. Visual layout and page text show that PDF extraction omitted
single-character multiplicity cells, split XML identifiers across lines/pages,
and truncated compound attribute names. After correction: 491 field rows are
verified, 64 depend only on external classifier datasets, and zero field rows
remain ambiguous. Five message rules retain explicit source/structure
identifier conflicts; one additional rule references external registry state.

Full-document search and visual audit established that the five remaining
identifier conflicts are printed in the original pages. The conflicting names
have no same-structure definition, alias, transition note or alternate-version
declaration in Decision No. 68. They are classified as internal normative
conflicts `NORMATIVE_CONFLICT-001` through `-005`, not repaired by similarity.
