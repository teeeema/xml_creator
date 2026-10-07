# OP23 CLASSIFIER EVIDENCE RECOVERY

## Result

Baseline classifier blockers: **44**. Resolved by newly recovered local official evidence: **0**. Remaining baseline classifier blockers: **44**.

A separate review of `R.IP.SP.03.003` found **6 additional requirements outside the supplied 102-blocker baseline** (`MSG.021/.022/.023 REQ.004/.005`) whose branch depends on the state of the Union NSI reference resource and whose exact `ipsdo` namespace still lacks official XSD proof. They remain non-executable.

## Official local evidence

- `/Users/tema/Documents/Work/Документы_xml/ОП_23.pdf`, SHA-256 `438611a5c16d2d699df244768d167a59ea0c020039853a44845346d96366fa1d`, is the only OP23 PDF found in the primary normative directory.
- PDF page 38 contains the normative reference to Commission Board Decision of **27 July 2021 No. 92** for the classifier used by intellectual-property document kinds.
- OP23 filling requirements condition `ipsdo:IPDocKindCode` / `ipsdo:IPDocKindName` behavior on whether the relevant document kind is present in that classifier.
- OP23 structure page 564 identifies `ipsdo:IPDocKindCode` as `M.IP.SDE.00007`, type `ipsdo:IPDocKindCodeType (M.IP.SDT.00009)`, pattern `\d{5}`, and says its value comes from the classifier of document kinds used in intellectual property. `ipsdo:IPDocKindName` is also present.
- OP23 structure pages 541–542 identify `ipsdo:IPLegalActionKindCode` (`M.IP.SDE.00505`, `M.IP.SDT.00506`) and `ipsdo:IPLegalActionKindName` (`M.IP.SDE.00506`). Page 542 requires a `codeListId` attribute for the legal-action code.
- OP23 page 282 makes the legal-action pair conditional on whether the corresponding reference resource is included in the Union unified normative-reference-information system.

## Evidence fields requested

| Evidence item | Recovery result |
|---|---|
| Decision No. 92 reference | **CONFIRMED** in OP23 PDF |
| Classifier ID for the Decision No. 92 document-kind classifier | **NOT FOUND / UNKNOWN** locally |
| Classifier dataset/version | **NOT FOUND / UNKNOWN** |
| Effective date of the applicable classifier dataset | **NOT FOUND / UNKNOWN** |
| `codeListId` attribute existence | **CONFIRMED structurally** where declared; this does not reveal its normative value |
| Actual `codeListId` value for the relevant classifier/reference resource | **NOT FOUND / UNKNOWN** |
| Machine-readable payload | **NOT FOUND** |
| Complete values/code-to-name mapping | **NOT FOUND** |
| Union NSI resource status / inclusion state applicable to validation | **NOT FOUND / UNKNOWN** |

The local KB classifier index contains other classifier IDs, but it does not provide a confirmed ID or machine-readable payload for the Decision No. 92 intellectual-property document-kind classifier. Audit-derived reports that merely name Decision No. 92 are not treated as payload evidence.

## IPDocKindCode / IPDocKindName

All **44** supplied classifier blockers remain open. OP23 gives conditional semantics and examples/explicit literals in individual requirements, but those fragments are not a complete official classifier snapshot and are not used to reconstruct one.

Baseline requirement IDs:

- `P.SP.03.MSG.001.REQ.004`
- `P.SP.03.MSG.001.REQ.005`
- `P.SP.03.MSG.003.REQ.004`
- `P.SP.03.MSG.003.REQ.005`
- `P.SP.03.MSG.003.REQ.048`
- `P.SP.03.MSG.003.REQ.049`
- `P.SP.03.MSG.004.REQ.004`
- `P.SP.03.MSG.004.REQ.005`
- `P.SP.03.MSG.005.REQ.004`
- `P.SP.03.MSG.005.REQ.005`
- `P.SP.03.MSG.005.REQ.049`
- `P.SP.03.MSG.005.REQ.050`
- `P.SP.03.MSG.006.REQ.008`
- `P.SP.03.MSG.006.REQ.009`
- `P.SP.03.MSG.006.REQ.034`
- `P.SP.03.MSG.006.REQ.035`
- `P.SP.03.MSG.007.REQ.008`
- `P.SP.03.MSG.007.REQ.009`
- `P.SP.03.MSG.007.REQ.034`
- `P.SP.03.MSG.007.REQ.035`
- `P.SP.03.MSG.008.REQ.008`
- `P.SP.03.MSG.008.REQ.009`
- `P.SP.03.MSG.009.REQ.004`
- `P.SP.03.MSG.009.REQ.005`
- `P.SP.03.MSG.010.REQ.004`
- `P.SP.03.MSG.010.REQ.005`
- `P.SP.03.MSG.010.REQ.053`
- `P.SP.03.MSG.010.REQ.054`
- `P.SP.03.MSG.011.REQ.004`
- `P.SP.03.MSG.011.REQ.005`
- `P.SP.03.MSG.012.REQ.004`
- `P.SP.03.MSG.012.REQ.005`
- `P.SP.03.MSG.012.REQ.053`
- `P.SP.03.MSG.012.REQ.054`
- `P.SP.03.MSG.013.REQ.008`
- `P.SP.03.MSG.013.REQ.009`
- `P.SP.03.MSG.013.REQ.037`
- `P.SP.03.MSG.013.REQ.038`
- `P.SP.03.MSG.014.REQ.008`
- `P.SP.03.MSG.014.REQ.009`
- `P.SP.03.MSG.014.REQ.037`
- `P.SP.03.MSG.014.REQ.038`
- `P.SP.03.MSG.015.REQ.004`
- `P.SP.03.MSG.015.REQ.005`

## IPLegalActionKindCode / IPLegalActionKindName

The following requirements are additional blockers outside the supplied baseline 102:

- `P.SP.03.MSG.021.REQ.004`
- `P.SP.03.MSG.021.REQ.005`
- `P.SP.03.MSG.022.REQ.004`
- `P.SP.03.MSG.022.REQ.005`
- `P.SP.03.MSG.023.REQ.004`
- `P.SP.03.MSG.023.REQ.005`

They must **not** be declared executable from the current material. The PDF confirms the field names/types and conditional NSI semantics, but it does not provide the applicable NSI resource state/effective date or an official XSD that proves the exact `ipsdo` namespace binding.

## Closure evidence still required

An official machine-readable classifier/reference-resource release (or equivalent authoritative export/contract) must identify the dataset, version/effective date, `codeListId`, complete values, and NSI lifecycle/status. For `R.IP.SP.03.003`, the official XSD/import set is also required to prove the exact namespace binding before execution is claimed.
