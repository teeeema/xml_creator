# OP26 runtime6 review

## Root cause

`R.HC.MM.01.002` stores `DrugRegistrationFileCode`, `DrugRegistrationFileName`, `PdfBinaryText`, and `AnyDetails` at the document root. The six production rules were executable, but the generic matrix fixture did not materialize a valid local branch for MSG.023/024. No shared `rules_engine` defect was found.

## Cases

| Requirement | Before | Fix | After |
|---|---|---|---|
| MSG.023.REQ.001 | FAIL | fixture uses `DrugRegistrationFileCode=0401` | PASS |
| MSG.023.REQ.006 | FAIL | fixture materializes `PdfBinaryText` | PASS |
| MSG.023.REQ.009 | FAIL | same valid file-code branch | PASS |
| MSG.024.REQ.003 | FAIL | fixture materializes `PdfBinaryText` | PASS |
| MSG.024.REQ.008 | FAIL | fixture uses an allowed file-code branch | PASS |
| MSG.024.REQ.010 | FAIL | fixture uses normative allowed code `0101` | PASS |

`MSG.024.REQ.009` was also corrected from the unproven `99` literal to `0199`, explicitly listed as «Другое» by Table 22 item 10 on PDF page 301.

## Verification

- Focused SAFE52/runtime6 suite: **99 passed**.
- Related E2E/regression suite: **32 passed, 64 subtests passed**.
- Full OP26 suite: **192 passed, 83 subtests passed**.
- Runtime6 fixed: **6**; blocked: **0**; remaining: **0**.
