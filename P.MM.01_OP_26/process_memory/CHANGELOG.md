# Changelog

## Unified local audit of remaining diagnostics — 2026-08-25

- Added `P_MM_01_REMAINING_NORMATIVE_DIAGNOSTICS_AUDIT.md` with source-traced,
  human-readable findings for conflicts, R.006/R.007, classifiers and MSG.014.R2.
- Retained every blocker/warning; no production/package/XML/session/GUI change
  and no external search.

## Local audit of NORMATIVE_CONFLICT-001 through -005 — 2026-08-25

- Added `NORMATIVE_CONFLICTS_001_005_AUDIT.md`, based solely on the local
  Decision No. 68 PDF, existing source references, package metadata and tests.
- Confirmed the five source/structure mismatches as real conflicts, not proven
  edition/profile/model/mapping or placeholder errors.
- Recorded `NOT_ENOUGH_LOCAL_EVIDENCE` for every corrective decision; retained
  the blocks on MSG.002, MSG.023 and MSG.024.
- No production rules, structures, profiles, Decision No. 5 code, serializer,
  session persistence, artifacts or GUI were changed; no web search was used.

## Conditional rules coverage — 2026-08-25

- Добавлен `CONDITIONAL_RULES_REPORT.md` и reproducible generator.
- Подтверждено: 133 conditional usages, 0 machine-evaluable, 133 unresolved.
- Structured Guide/Markdown показывают условие и отсутствие автоматической проверки.
- P.MM.01 normative MessageRules, structures, policies, conflicts и XML generation не изменялись.

## Participant addressing audit — 2026-08-24

- Confirmed Decision No. 68 table 1 participant codes `P.ACT.001` and
  `P.MM.01.ACT.001`; rejected synthetic `EEC.ACT.001`/`RU.ACT.001` codes.
- Added six source-traced process participants and participant endpoints for
  all 19 transactions.
- Regenerated all reference XML with addresses built from process metadata.
- Confirmed that R.007 `bdt:DateTimeType` cites ISO 8601 but the local source
  does not impose a mandatory timezone offset.

## TEST placeholder E2E reclassification — 2026-08-24

- Kept the version profile and normative catalog unchanged.
- Reclassified 43 branches: 37 VERSION_PLACEHOLDER_TEST, 3 NORMATIVE_CONFLICT,
  3 INITIAL_MESSAGE_BLOCKED by those initiating conflicts.
- TRN.004 request/response and accessible R.006 branches now complete SOAP in
  TEST with literal Y.Y.Y/X.X.X; STRICT remains unresolved.

## Local JSON drafts — 2026-08-24

- Added P.MM.01 integration coverage for MSG.007 roundtrip/regeneration, a large
  form and an unresolved MSG.005 draft without bypassing its generation block.
- No normative structures, rules or versions were changed.

## Typed diagnostic presentation — 2026-08-24

- Verified generic presentation for VERIFIED MSG.007, TEST_ONLY MSG.001,
  unresolved MSG.005 and normative-conflict MSG.002.
- Verified nine automatically derived Process Issues entries with source and
  affected-message details; no package or normative data was changed.

## GUI large-form usability smoke — 2026-08-24

- Verified revised Data/XML tabs with resolved TRN.005/MSG.007 and blocked
  TRN.004/MSG.005 on macOS wxPython 4.3.1.
- Verified human EDocHeader caption and technical QName help without normative
  package changes.

## Generic GUI integration — 2026-08-24

- Verified generic GUI-controller discovery and presentation for P.MM.01.
- Covered blocked R.007, normative-conflict MSG.002, TEST_ONLY MSG.001 and the
  resolved TRN.005/MSG.007 form without adding process-specific GUI logic.

## Universal application-facade integration — 2026-08-24

- Verified discovery of P.MM.01, 19 transaction DTOs and all 43 message branches.
- Verified public facade results for resolved, classifier-only, unresolved and
  normative-conflict messages plus Decision No. 5 request/response correlation.
- Added no normative catalog changes or P.MM.01-specific engine behavior.

## All-transactions E2E classification — 2026-08-24

- Derived a 43-branch verification matrix mechanically from all 19 transaction
  definitions, including every initiating message and every response branch.
- Classified STRICT and TEST execution independently: 14 `VERIFIED_SOAP`,
  9 `TEST_ONLY`, 17 unresolved structure versions and 3 normative conflicts.
- Added 23 deterministic SOAP examples, 20 source-traced blocked reports, a
  machine-readable matrix test and generic notification/mutual-obligation
  state-machine regressions.
- Preserved the focused TRN.004–006 suite and artifacts; made no engine,
  architecture or normative catalog change.

## TRN.004-.006 end-to-end verification — 2026-08-24

- Verified catalog, Action, Body, Header, SOAP and request/response correlation
  for resolved branches of TRN.005 and TRN.006.
- Verified that TRN.004 R.007 and alternative MSG.009 R.006 branches remain
  blocked by `UNRESOLVED_STRUCTURE_VERSION` without inferred versions.
- Added four deterministic SOAP reference XML files, three source-traced
  blocked reports and data-driven regression tests.

## Final MessageRule conflict classification — 2026-08-24

- Searched every conflicting identifier through the complete Decision No. 68
  and visually checked rule pages 219, 298 and 300 plus structure tables 10 and 13.
- Confirmed five internal normative contradictions, not extraction errors or
  version mismatches, as `NORMATIVE_CONFLICT-001` through `-005`.
- Added explicit runtime blocking for MSG.002, MSG.023 and MSG.024 without
  blocking unaffected messages.
- Set package status to `BODY_MODEL_CONFIRMED_WITH_EXTERNAL_CONFLICTS`.

## Interpretation audit — 2026-08-24

- Visually audited table 10 page continuations and representative pages of the
  other requisite tables against the original PDF.
- Corrected extraction loss in all cardinality cells, wrapped XML names and
  compound attribute names; all 555 paths are now unique and field ambiguity is zero.
- Classified 64 classifier-backed fields as `NEEDS_EXTERNAL_SOURCE` without
  blocking structural serialization.
- Reduced unresolved MessageRules from 33 to five genuine
  source/structure-identifier conflicts; classified one registry lookup rule as
  an external dependency.
- Added reason-coded interpretation reporting and regression tests.

## Normative Body import and generic execution — 2026-08-24

- Rechecked tables 4, 7, 10, 13, 16, 19, 22 and 25 in the local Decision No. 68 PDF.
- Represented all 555 requisite rows with row-level source references, hierarchy,
  order, cardinality, datatype text, classifiers and element/attribute kind.
- Imported 201 rows from the 16 actual message-specific rule tables.
- Preserved 169 field rows and 33 message-rule rows as explicit normative
  interpretation work rather than guessing.
- Verified generic Body validation/serialization and Decision No. 5 SOAP
  integration on resolved `R.HC.MM.01.004`.

## Per-structure version profile — 2026-08-20

- Converted every structure profile entry to its own `active_version` mapping.
- Left `R.006` and `R.007` explicitly unresolved (`null`).
- Confirmed that unresolved base structures do not block resolved healthcare
  structures or package validation.
- Added resolver and regression tests; no normative structure or Body logic was
  changed.

## Normative catalog — 2026-08-20

- Accepted Decision No. 68 as `PRIMARY_PROCESS_NORMATIVE_SOURCE` following the
  corrected requirement.
- Added 19 PRC, 57 standalone OPR, 19 TRN, 28 MSG and 8 structure definitions.
- Added transaction patterns, operation/message links, timeouts, retry,
  authorization and signature metadata.
- Indexed 16 message-specific rule tables and every structure requisite table.
- Added source traceability with document sections, tables/items and pages.
- Replaced the incorrect Decision No. 120 analysis with `DECISION_68_ANALYSIS.md`.
- Kept Body, physical XSD, classifiers, GUI and transport unimplemented.

## Source audit — 2026-08-20

- Inspected the only PDF supplied in `normative_sources/` without modifying it.
- Identified it as Decision No. 68 dated 19 April 2022, amending Decision
  No. 122; recorded its SHA-256 and 465-page extent.
- Confirmed that the requested Decision No. 120 is absent.
- Recorded `BLOCKED_SOURCE_MISMATCH`; deliberately did not populate the
  Decision No. 120 catalog from a different act.
- Did not add Body code, XSD, classifiers, SOAP instances or runtime features.

## Skeleton — 2026-08-20

- Created the external P.MM.01 process-package catalog.
- Recorded `NEEDS_NORMATIVE_SOURCES` and intentionally left all normative definition lists empty.
# 2026-08-24 — FieldInputPolicy

- Добавлен source-traced `field_input_policies.yaml`.
- Зафиксированы policies EDocHeader, response Body correlation и UpdateDateTime MSG.006.
- Добавлен полный MSG-context report и P.MM.01 regression coverage.
- Mappings, version profile и нормативные конфликты не изменялись.
# 2026-08-24 — separate UI policy

- Добавлен `ui_input_policies.yaml` для process-level overrides.
- EDocDateTime явно оставлен нормативно unresolved, но в UI вводится пользователем (`MANUAL_OVERRIDE`).
- Сформирован полный `UI_INPUT_POLICY_REPORT.md` по 28 MSG и 2960 usages.
- Normative field policies, mappings, MessageRules, structures, versions и conflicts не изменялись.
# 2026-08-24 — official messages guide

- Добавлены `P_MM_01_MESSAGES_GUIDE.md` и `GUIDE_GENERATION_REPORT.md`, генерируемые из structured guide API.
- Добавлены полные Body trees/tables, examples, source traceability и conflict warnings для MSG.001–MSG.028.
- Исправлен отдельный UI presentation bug: response-only UpdateDateTime больше не показывается в MSG.005. Normative structures/rules/policy не менялись.
# 2026-08-24 — guide quality improvement

- Перегенерирована Сводка с безопасными datatype/documentation/classifier examples.
- Business identifiers больше не показываются как UUID без подтверждения.
- Добавлены example origins, no-example reasons и полный аудит 132 unresolved UI usages.
- Normative structures, MessageRules, field_input_policies, mappings, versions и conflicts не изменялись; ui_input_policies также не менялся.
# 2026-08-24 — large form filtering regression

- Добавлены P.MM.01 tests для MSG.001 counts, DocName search, hierarchy и performance.
- Проверены small MSG.005, nested/repeatable MSG.019 и нормативно конфликтный MSG.002.
- Нормативные структуры, MessageRules, policies, profiles и XML generation не изменялись.
# 2026-08-25 — complete MSG.001–MSG.028 rules audit

- Audited both applicable section IX blocks in the local Decision No. 68 PDF.
- Added `message_rules_audit.yaml` with dedicated source references for every message.
- Confirmed 16 YAML-backed message tables and 12 intentional no-table cases; no empty YAML files were added.
- Recorded both applicable tables for MSG.019 and MSG.020.
# 2026-08-25 — assisted input UX

- Added a project UI override for editable EDocId with generic `GENERATE_IDENTIFIER` capability.
- Audited all former READ_ONLY and all temporal usages in `EDITABLE_AUTO_FIELDS_AUDIT.md`.
- Kept FieldInputPolicy, structures, MessageRules, profiles, participants, conflicts and XML serialization unchanged.
- Verified TRN.004 MSG.005 assisted identifier/datetime input and MSG.006 external UpdateDateTime behaviour.
# 2026-08-25 — user acceptance

- Added `GUI_USER_ACCEPTANCE_REPORT.md` with scenario, field, category, severity, expected/actual and status for every issue.
- Verified request/response correlation, notification semantics, mutual-obligation branches, classifier fallback, XML/clipboard/save, Guide, filters and draft roundtrip.
- Kept normative blockers MSG.002/023/024 unchanged and explicitly classified them as expected behaviour.

# 2026-08-25 — binary and boolean UX

- Audited 53 unique binary usages; generic datatype-driven file selection covers all.
- Added draft/base64, MIME, filter and Да/Нет regressions without normative changes.
- Left TransactionSession recovery and accepted/expected issues unchanged.

# 2026-08-25 — session persistence audit

- Audited draft/session boundary and Decision №5 correlation persistence.
- Designed a separate versioned snapshot, validator, Continue and Open-as-new UX.
- Did not implement restore because current history lacks state/event evidence required for safe P.MM.01 continuation.

# 2026-08-25 — session snapshot storage v1

- Added separate strict JSON snapshot persistence without changing Body drafts.
- Verified P.MM.01 TRN.004 IDs/Actions/history plus generic retry, notification, signal and fault records.
- Kept GUI Continue disabled and legacy draft restore forbidden.

# 2026-08-25 — unified session lifecycle and restore

- Added current-package compatibility and state/correlation replay before runtime acceptance.
- Proved TRN.004 next response, retry continuation, notification and TRN.008 signals.
- Kept GUI Continue/Open as new unimplemented and legacy drafts non-restorable.
# 2026-08-25 — responsive GUI layout

- Audited MainFrame, notebook, selectors, dynamic form, validation and action bars.
- Added wrapping action/filter bars and two-axis form access at narrow widths.
- Passed real macOS wx resize regression without changing P.MM.01 normative data,
  session lifecycle, drafts or XML generation.
# 2026-08-25 — GUI transaction session controls

- Added separate session snapshot open/save and typed RESTORABLE-only Continue.
- Added explicit Body draft selection for create-new semantics.
- Passed real wx restart/correlation, invalid snapshot and responsive layout scenarios.
- Kept P.MM.01 normative data, Decision №5 and XML/Body semantics unchanged.
# 2026-08-25 — restored session final XML audit

- Added semantic XML parsing for continuous/restored response and fresh restart.
- Verified Header correlation, Action, namespaces, signal, Fault and notification.
- Recorded missing EDocId→EDocRefId persistence and retry XML payload blockers.
- Left core, snapshot schema, ProcessPackage and serializer unchanged.
# 2026-08-25 — message artifact persistence

- Added atomic snapshot+artifact bundle, immutable Body payload round-trip and integrity checks.
- Added P.MM.01 source-traced EDocId→EDocRefId recovery and retry XML after restart.
- Kept Body draft, SOAP correlation and unrelated normative blockers separate.
