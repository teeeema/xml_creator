# OP23 XSD RECOVERY

## Result

Baseline XSD/missing-structure blocker: **1** (`P.SP.03.MSG.025.REQ.006`). Resolved: **0**. Remaining: **1**.

## Required chain

- Message requirement: `P.SP.03.MSG.025.REQ.006`
- Structure: `R.IP.SP.03.007`
- Declared schema filename: `EEC_R_IP_SP_03_ApellationOfOriginRegisterRequestDetails_v1.0.0.xsd`
- Required imported/common-model type: `M.IP.CDT.00003 / ipcdo:IPDocDetailsType`
- Relevant container: `ipcdo:AccompanyingDocumentsDetails`

OP23 PDF page 573 confirms `ipcdo:AccompanyingDocumentsDetails` with type `ipcdo:IPDocDetailsType (M.IP.CDT.00003)` and its document-kind children. This proves the PDF-level structure description, but it does not supply the XSD namespace/import bindings needed for exact QName proof.

## Recursive primary-directory search

Root: `/Users/tema/Documents/Work/Документы_xml`

- Total files: **48**
- XSD: **0**
- XML: **0**
- ZIP: **0**
- RAR: **0**
- 7z: **0**
- OP23 PDFs: **1**

No archive exists locally whose contents could hide the requested XSD/XML package. The exact declared XSD filename and `M.IP.CDT.00003` occur only as textual references in project structure/KB/report metadata; no matching XSD bytes were found. A workspace scan also found **0 `.xsd` files**.

## Why the blocker remains

The PDF table is sufficient to know the intended conceptual type and field names, but not to prove the exact namespace URI/version, `xs:import` target, imported schema file, or the complete content model for `IPDocDetailsType`. Reconstructing those from PDF rows would create an inferred schema and is not normative evidence.

`P.SP.03.MSG.025.REQ.006` therefore remains **BLOCKED_BY_SOURCE** until the official `R.IP.SP.03.007` XSD plus the imported model module containing `M.IP.CDT.00003` are available.
