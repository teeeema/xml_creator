# P.MM.06 Blocker Register

## Critical

| ID | Category | Description | Requirements | Required evidence | Workaround |
|---|---|---|---:|---|---|
| B-QNAME | XML_MAPPING | 175 unresolved and 4 ambiguous nodes | 152 | authoritative XSD/XML mapping | PARTIAL only; XML production remains blocked |
| B-XSD | XSD | XSD references known, files absent | 162 | authoritative XSD files/imports | PARTIAL only; XML production remains blocked |
| B-R006 | SHARED_STRUCTURE | R.006 definition and Y.Y.Y unresolved | 0 | authoritative R.006 package/version | PARTIAL only; XML production remains blocked |
| B-R007 | SHARED_STRUCTURE | R.007 definition and Y.Y.Y unresolved | 0 | authoritative R.007 package/version | PARTIAL only; XML production remains blocked |
| B-VERSION | VERSION | X.X.X/Y.Y.Y/Z.Z.Z unresolved | 162 | authoritative version profile | PARTIAL only; XML production remains blocked |
| B-ATTRIBUTE | ATTRIBUTE | codeListId/codeListVersionId/media owners unresolved | 26 | authoritative owner/path mapping | PARTIAL only; XML production remains blocked |

## Non-critical

| ID | Category | Description | Requirements | Required evidence | Workaround |
|---|---|---|---:|---|---|
| B-CLASSIFIER | CLASSIFIER | references known, datasets absent | 24 | authoritative datasets/versions | YES for independent catalog/semantic layers |
| B-ACTOR | ACTOR | ACT.004 has no proven operation/transaction link | 0 | authoritative linkage or catalog-only confirmation | YES for independent catalog/semantic layers |
| B-OPR | OPERATION | OPR.007/.008 absent from normative tables | 0 | authoritative gap explanation | YES for independent catalog/semantic layers |
| B-EXTERNAL | EXTERNAL_REFERENCE | storage/register checks require external state | 7 | runtime external-reference contract | YES for independent catalog/semantic layers |
