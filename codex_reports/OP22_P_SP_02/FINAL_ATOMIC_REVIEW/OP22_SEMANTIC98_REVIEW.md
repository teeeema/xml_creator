# OP22 SEMANTIC98 primary-source review

## Result

- Target: **98** `SEMANTIC_REVIEW_REQUIRED` requirements.
- Primary normative attribution reconstructed: **98/98**.
- `ATOMIC_SOURCE_CONFIRMED`: **98/98**.
- `ATOMIC_SOURCE_NOT_PROVABLE`: **0**.
- `SOURCE_AMBIGUOUS`: **0**.
- `SOURCE_CONFLICT`: **0**.
- Newly strict-closed from this set: **0**.

The original `ОП_22.pdf` identifies the atomic normative item for every reviewed row through an explicit same-code inheritance statement plus the corresponding exact base-table item. This resolves the atomic **source attribution** question without promoting range evidence by itself.

Strict closure is still not available for these 98 rows. The existing proof machinery requires a target-attributable executable component: the component must carry either the exact current-table item source reference or a `CONFIRMED` exact inherited item reference. For all 98 rows, `prove_aggregated_requirement(...)` currently returns `NO_ATOMIC_SOURCE_LINK` with zero strict atomic components. The aggregate runtime can show PASS→FAIL, but it cannot assign that negative proof to the reviewed canonical atom.

Therefore all 98 are `ATOMIC_SOURCE_CONFIRMED` at the normative-source layer and remain open at the strict proof/linkage layer. No production file was changed to manufacture that linkage.

## Primary-source findings

- Table 34 family: **75** rows. The original PDF provides exact atomics for the reviewed items (13-22, 26, 27 as applicable), while the derived message tables explicitly state same-code inheritance to Table 34.
- Table 37 family: **5** rows. Items 16/18/19 are textually identifiable in the primary PDF; the affected aggregates still lack an exact target-attributable executable component for the reviewed canonical rows.
- Table 44 family: **7** rows. Later message tables explicitly inherit the same requirement codes from Table 44; the source atomics are confirmed while strict executable attribution remains absent.
- Table 49 family: **7** rows. Item 19 is explicit in the original PDF (collective-mark charter/regulation accompanying document), but Table 65-71 executable rule sets stop before a target-attributable item-19 component.
- Table 72 family: **4** rows. Items 4/5 are explicit conditional legal-action-kind requirements. Table 74/75 inheritance is traceable, but executable components for 4/5 are absent.

### Table 57 extraction issue resolved

The early `P.SP.02.MSG.027` Table 57 continuation was visually inspected in the original PDF. PDF page 579 explicitly states that REQ 6-29 correspond to Table 34 REQ 6-29 and that the requirement codes in Tables 34 and 57 coincide. The earlier text-extraction gap is therefore **not** `SOURCE_AMBIGUOUS`.

### Table 34 item 27 visual check

PDF page 520 was visually inspected. Item 27 is a conditional requirement for trademark-kind values 140/150/160/170/180 and requires the trademark-image and colour-description requisites named by the table. The suspicious prior text rendering was an extraction issue, not a source conflict.

## Production/proof boundary

Representative current-state checks:

- `P.SP.02.MSG.003` target items 13-22, 26, 27 are normatively traceable through Table 36 -> Table 34, while the current executable inherited source refs cover other Table 34 atomics; none of these target atoms has an accepted exact executable source link.
- `P.SP.02.MSG.044` target items 13, 16-20, 26 have confirmed source inheritance but no strict target-attributable executable component.
- `P.SP.02.MSG.047`-`053` item 19 has exact normative inheritance to Table 49 item 19, but the current executable target-attributable components cover through item 18.
- `P.SP.02.MSG.056`/`057` items 4/5 have exact normative inheritance to Table 72, but the current executable component lists omit 4/5.

No production, engine, KB, or message-rule file was changed. No new proof test was added because none of the 98 has the target-attributable executable linkage required to turn its aggregate PASS→FAIL evidence into canonical strict proof.

Full row-by-row evidence is in `OP22_ATOMIC_SOURCE_119_MATRIX.csv`.
