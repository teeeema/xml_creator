# OP23 B1 <= 5 MB Capability Review

STATUS: **ENGINE CAPABILITY MISSING; normative limit confirmed; implementation intentionally not performed.**

## Requirements

- `P.SP.03.MSG.023.REQ.019` — CONFIRMED normative source: `ОП_23.pdf`, P.SP.03 1.0.0, **page 286, Table 27, item 19**. It requires `csdo:DocBinaryText`, restricts `@mediaTypeCode`, and states that the binary-text document size must not exceed **5 Мб**.
- `P.SP.03.MSG.024.REQ.019` — CONFIRMED by `ОП_23.pdf`, **page 287, Table 28**, which states that requirements 1–19 correspond to Table 27 requirements 1–19. The live rule also links back to Table 27 item 19.

The live rules correctly remain `mapping_status: PARTIAL`: they enforce `DocBinaryText` presence and the allowed `mediaTypeCode` set, but contain no binary-size assertion. Existing `test_msg023_024_req019_binary_document_real_xml` covers only `missing` and `media_type` mutations.

## Current engine capability

`R.IP.SP.03.003` identifies `csdo:DocBinaryText` as `csdo:BinaryTextType (M.SDT.00143)` and describes it as a finite sequence of binary octets (bytes), but the structure definition contains no max-size facet for this field.

The XML extractor currently stores scalar element content as XML text (`child.text`). It does not base64-decode `DocBinaryText`. The datatype validator has no `BinaryTextType`/base64-binary branch. Its generic `max_length` facet, when present, applies `len(text)` to the lexical XML text; that is not decoded payload byte length.

The structured rules engine can compare already extracted scalar values, counts, dates, decimals, cardinalities, and cross-instance values, but it has no transform/operator for base64 decoding or decoded binary byte length.

Therefore the current parser + evaluator **cannot prove the normative <=5 MB binary payload limit correctly**. A test that only measures the Base64 string length would be synthetic proof of the wrong invariant.

## Minimal future engine change

A production change is needed, but it should be a **generic binary-size primitive**, not an OP23/message-specific exception. The responsible layer should decode/validate the binary lexical value according to its datatype and expose/check decoded octet length; the rules layer can then express a maximum byte length for the normative rule. Both MSG.023 and MSG.024 can reuse that primitive.

No implementation is made in this task.

## Unit/threshold caution

The cited OP23 text confirms the limit as **"5 Мб"**, but the inspected OP23 rule/structure data do not define an exact byte constant (`5,000,000` versus `5,242,880`) for this requirement. Do not hard-code a conversion from the wording alone. Before implementation, confirm the unit semantics from the authoritative datatype/schema/normative source or another explicit EAEU definition.

An unrelated OP22 structure uses a lexical maximum of `6990507` for a different picture datatype described with a 5 Мб limit. That is not normative evidence for OP23 `csdo:BinaryTextType` and must not be copied into this rule.

## Decision

```text
B1_5MB_ENGINE_CAPABILITY: MISSING_GENERIC_DECODED_BINARY_BYTE_LENGTH_PRIMITIVE
B1_5MB_IMPLEMENTATION_NEEDED: YES_GENERIC_ENGINE_PRIMITIVE_PLUS_RULE_MAPPING_AND_BOUNDARY_TESTS
B1_5MB_NORMATIVE_EVIDENCE: CONFIRMED_OP23_P286_TABLE27_ITEM19_AND_P287_TABLE28_INHERITANCE; EXACT_BYTE_MULTIPLIER_UNRESOLVED
```
