# OP35.1 / P.TS.01 — PRC.002 source recovery

PRC002_TABLE_ACTUALLY_PRESENT: NO

## Confirmed source facts

- `P.TS.01.PRC.002` is explicitly named on PDF page 8 of `35.1 ОП.pdf` as the procedure for obtaining information from a national part of the unified register.
- The separate regulation for interaction between authorized bodies confirms the PRC.002 participants on PDF pages 23-24: requesting authorized body `P.TS.01.ACT.003` and responding authorized body `P.TS.01.ACT.002`.
- On PDF page 25, clause 12 states that the transaction execution scheme is shown in Figure 2 and that Table 2 provides the relation between operations, intermediate/resulting states and common-process transactions.
- Immediately after clause 12 on PDF page 25, the file starts the next approved document: the Description of formats and structures. Figure 2 and Table 2 for this regulation are absent from this local PDF copy.

## Recovery conclusion

This is a source-content gap in the available consolidated PDF, not a text-extraction failure. There is no hidden Table 2 in the local copy to recover by changing extraction tooling.

The exact missing normative material is the complete official text/revision of the Regulation on information interaction between authorized bodies of Member States for this common process, approved under Decision of the EEC Collegium No. 39 of 10.05.2016, containing the Figure 2 / Table 2 referenced by clause 12 for the procedure `P.TS.01.PRC.002`.

The clause points to Figure 2 and Table 2 in the same regulation; it does not identify another external document that contains them. Therefore the required recovery action is to obtain a complete official copy/version of that regulation rather than infer the missing rows.

## Values that remain unresolved

- OPR list for `P.TS.01.PRC.002`: UNRESOLVED_SOURCE_GAP
- TRN list for `P.TS.01.PRC.002`: UNRESOLVED_SOURCE_GAP
- MSG list for `P.TS.01.PRC.002`: UNRESOLVED_SOURCE_GAP
- `P.TS.01.TRN.003`: NOT SOURCE-CONFIRMED and must not be invented from numbering.
- `P.TS.01.MSG.004`-`.006`: NOT SOURCE-CONFIRMED and must not be invented from numbering.

No production/test/GUI/KB change is justified from this gap alone.
