# Universal registry refactor report

Date: 2026-08-27

## 1. Baseline

The handoff baseline was 273 tests / 905 subtests. The supplied checkout currently
contains 185 pre-existing discoverable `unittest` methods; this difference predates
Stage C and no test was deleted, skipped or weakened. After six Stage C tests the
complete local suite contains 191 tests and passes.

## 2–4. Added classes and APIs

- `ProcessRegistry(processes_root)` indexes valid direct-child packages.
- `list_processes()` lists packages; `get_process(code, version=None)` obtains one.
- `StructureResolver().resolve(process=package, structure_code=code, version=version)`
  resolves an explicitly versioned structure.
- Typed errors cover unknown/duplicate processes and missing structure versions.
- `ProcessPackageLoader.load(Path)` remains compatible.

## 5–6. Local/shared rules and collisions

Shared definitions live at `shared/structures/<code>/<version>.yaml` and are parsed
by the canonical `ProcessPackageLoader.load_structures()` parser. The existing profile
selection may specify `source: local` or `source: shared`. Version is mandatory and
is never inferred. An identical local/shared `(structure_code, version)` without an
explicit source fails with `AMBIGUOUS_STRUCTURE_SOURCE`.

## 7. Added tests

`tests/test_universal_registry.py` adds six tests covering two arbitrary processes,
unknown code/version, duplicate codes, shared reuse by two processes, collision and
both explicit source choices, mandatory version, many MSG to one structure,
MessageDefinition/StructureDefinition separation, and one MSG used by two TRN.

## 8. P.MM.01-dependent tests

The audit found `test_process_packages.py`, `test_session_snapshot.py`,
`test_session_restore.py`, and `test_gui_session_controls.py`. They were not moved:
the current `pyproject.toml` discovers only `eaeu_xml/tests`, so moving them would
change discovery/coverage. This remains technical debt.

## 9–10. XML and session regression

The complete suite passed unchanged. A focused 86-test / 11-subtest run covered XML,
application, file input, snapshots, restore, retry and process packages. Namespaces,
root, field order, attributes, cardinality, EDocId/EDocRefId, BinaryText and boolean
paths remain covered. No serializer, Body provider, XML fixture, session schema or
lifecycle code changed.

## 11. Hardcode scan

`P.MM.01`, `P.DS.01`, `P.TEST.01`, `P.MM.01.MSG` and `P.MM.01.TRN` have zero matches
in production Python below `src/eaeu_xml`. Synthetic codes occur only in tests.

## 12. Final test counts

- Complete macOS/wx-capable run: 191 tests, all passed.
- Headless pytest excluding three wx-importing modules: 178 tests / 839 subtests passed.
- Focused XML/session/process/registry regression: 86 tests / 11 subtests passed.

## 13. Changed files

- `src/eaeu_xml/core/errors.py`
- `src/eaeu_xml/process_packages/{models,loader,registry,resolver,__init__}.py`
- `tests/test_universal_registry.py`
- `project_memory/{CURRENT_STATE,CHANGELOG,DECISIONS,UNIVERSAL_REGISTRY_REFACTOR_REPORT}.md`

## 14. Intentionally unchanged

No P.DS.01, P.MM.01 normative data, structure moves, XML output, GUI, SOAP/Decision
No. 5 logic, session lifecycle, retry, XSD validation, Body-validator split, facade
split or public TransactionDefinition rename.

## 15. Remaining technical debt

- Process-package and runtime models both expose `TransactionDefinition`; application
  sites correctly use `RuntimeTransactionDefinition`. No incorrect import was found.
- P.MM.01 integration tests remain in the universal test directory pending a safe
  discovery redesign.
- Duplicate process codes are conflicts; the optional version argument filters the
  registered package but does not yet define a multi-directory version layout.
- Shared catalogs contain infrastructure only; no existing R.* was moved.
