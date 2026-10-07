# KB Schema v1.0 Design

## Canonical model

`SOURCE → KNOWLEDGE → PROJECT_STATE` remains the architectural boundary. Canonical entity files live under `knowledge_base/data/`; generated indexes live under `knowledge_base/indexes/`. Existing Markdown/source notes are retained.

All canonical `*.yaml` files use JSON syntax, which is a valid YAML 1.2 subset. This gives deterministic stdlib serialization without adding PyYAML. Unknown scalar values are `null`; known-empty collections are `[]`.

## Timestamp policy

Canonical entities do not embed build timestamps. They reference `data/project_state/current.json`, the only timestamped canonical project-state output, so repeated builds do not rewrite thousands of entity files.

## Evidence policy

Normative and project-state evidence remain distinct. `CONFIRMED_PRODUCTION` and `CONFIRMED_RUNTIME` are never promoted to normative proof. OP32 atomic QName remains independent from structure-root QName.

## Schemas

JSON Schema documents are in `knowledge_base/schemas/` with `schema_version = "1.0"`. Custom deterministic validation enforces cross-entity invariants that JSON Schema alone cannot prove.
