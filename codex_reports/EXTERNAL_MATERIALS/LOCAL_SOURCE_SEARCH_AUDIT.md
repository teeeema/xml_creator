# LOCAL SOURCE SEARCH AUDIT — OP26 external materials

## Scope

Recursive read-only search root: `/Users/tema/Documents/Work/Документы_xml`. Search was performed before declaring materials absent. Knowledge Base and OP26 audit reports were read-only inputs.

## File/extension inventory relevant to the request

- PDF: **7** — `26_ОП.pdf`, `32_ОП.pdf`, `35.1_ОП.pdf`, `49_ОП.pdf`, `5 решение.pdf`, `ОП_22.pdf`, `ОП_23.pdf`.
- DOC: **2** — `120 решене.doc`, `5 решение.doc`.
- DOCX: **4** — one GIS DTC requirements document and three OP22 report documents.
- Markdown: **13** (including OP26 explanatory notes).
- XSD: **0**.
- XML: **0**.
- ZIP/RAR/7z: **0**; therefore there were no local archives whose inner file list could contain hidden XSD/XML payloads.

## Filename/term search

Searched recursively for names/terms including: `R.006`, `R.007`, `R.HC.MM.01.*`, exact declared XSD names, `P.CLS.019`, `classifier`, `классификатор`, `справочник`, `registry`, `реестр`, `model`, `common model`, `base model`, `healthcare model`, `68`, `122`, `измен`, `поправ`, `corrig`, `редакц`.

Relevant filename hits:
- `/Users/tema/Documents/Work/Документы_xml/26_ОП.pdf` — primary official source used for OP26.
- `XML/ГИС_ИШ/ОП 26/Структура R.006 — «Уведомление о результате обработки».md` — explanatory/local note, not XSD.
- `XML/ГИС_ИШ/ОП 26/Структура R.007 — «Состояние актуализации общего ресурса».md` — explanatory/local note, not XSD.
- `XML/ГИС_ИШ/ОП 26/Решение №68.md` — explanatory/local note, not an alternate official PDF/corrigendum.

DOC/DOCX content was also checked with macOS `textutil` for the relevant identifiers/terms. No OP26 XSD/classifier payload/registry contract was found. The GIS DTC document contains generic XML-schema/SМЭВ material and is unrelated to the requested EAEU OP26 payloads. The three OP22 DOCX files are audit/report material and are not normative payloads.

## What was found

### XSD declarations in the primary PDF
The PDF declares eight schema filenames/identities: R.006, R.007, R.HC.MM.01.001, .002, .003, .004, .006, .007. The exact structure/version/namespace/pages are recorded in `EXTERNAL_MATERIALS_REQUEST_MANIFEST.md`. The bytes of those XSDs are not present locally.

### Imported namespace declarations
The OP26 source directly declares `ccdo`/`csdo` imports for R.006/R.007 and `ccdo`/`hccdo`/`hcsdo`/`csdo` for the healthcare structures. All model namespace versions remain `vX.X.X`. Exact imported schema filenames and schemaLocation values are not in the audited tables.

### P.CLS.019 identity
`26_ОП.pdf` PDF 39 / printed 38 / Table 10 confirms `P.CLS.019`, “классификатор стран мира”, and says it contains country names and codes according to ISO 3166-1. No machine-readable payload, applicable edition/version or effective date was found locally.

## What was NOT found

- Any `.xsd` file: **NOT FOUND**.
- Any `.xml` payload: **NOT FOUND**.
- Any ZIP/RAR/7z package: **NOT FOUND**.
- Concrete R.006 version replacing `Y.Y.Y`: **NOT FOUND**.
- Concrete R.007 version replacing `Y.Y.Y`: **NOT FOUND**.
- Concrete base-model version replacing `X.X.X`: **NOT FOUND**.
- Concrete healthcare-model version replacing `X.X.X`: **NOT FOUND**.
- Machine-readable official P.CLS.019 payload/version/effective date: **NOT FOUND**.
- Unified-registry authoritative API/schema/contract/offline snapshot spec: **NOT FOUND**.
- Revised XSD/corrigendum resolving the five source conflicts: **NOT FOUND**.
- Alternate OP26 PDF/corrigendum containing a complete Table 19 item 84: **NOT FOUND**.

## Table 19 item 84 verification

Two independent checks agree:

1. **Knowledge Base source extraction:** item 84 ends at `«...обязательны для заполнения и»`, then item 85 begins.
2. **Visual inspection of the original PDF:** rendered and inspected PDF pages 230 and 231. On PDF 230 / printed 229, item 84 visibly ends at the same phrase and item 85 starts immediately in the next row. On PDF 231 / printed 230, the top of the page continues item 87; there is no continuation of item 84. Temporary page renders were deleted after inspection.

Conclusion: this is present in the local published source itself, not an extraction-only truncation.

## Alternate edition / corrigendum search

The normative directory contains only one OP26 PDF (`26_ОП.pdf`). Filename search for Decision 68/122, amendments/corrections/corrigenda found only the local explanatory note `Решение №68.md`; no second official OP26 edition or correction PDF was present.

## Shared benefit check (without re-auditing OP22/OP23/OP49)

KB indexes show the same `R.006` is used by:
- OP22: `P.SP.02.MSG.002`, `P.SP.02.MSG.025`;
- OP23: `P.SP.03.MSG.002`, `P.SP.03.MSG.020`;
- OP49: `P.DS.01.MSG.003`.

Therefore obtaining the concrete R.006 release/XSD and its base-model imports has a **SHARED BENEFIT** for OP22/OP23/OP49. No equivalent shared benefit for the OP26 healthcare XSDs, R.007, P.CLS.019, registry contract, OP26 source conflicts or item 84 was proven for those three processes.

## Optional official web discovery

Internet access was available. Targeted searches were restricted to official EEC/EAEU domains and exact identifiers/filenames. No exact official schema payload/model package/P.CLS.019 payload/registry contract/corrigendum was confirmed. An official EEC-hosted Decision No. 79 PDF from 30 June 2017 surfaced contextual use of `P.CLS.019`, but it is not the missing classifier payload/version for OP26 and was rejected as a match.

Result: `CONFIRMED_MATCH=0`; suitable `CANDIDATE_ONLY=0`.

## Reproducibility notes

Commands used included recursive `find` by extension/name, `rg` over KB/source extracts and audit CSVs, `textutil -convert txt -stdout` for DOC/DOCX term checks, and temporary `pdftoppm` renders for item 84 visual verification. No source/normative file was edited.
