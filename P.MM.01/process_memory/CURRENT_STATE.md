# Current state

## Unified audit of remaining diagnostics — 2026-08-25

All five conflicts, R.006, R.007, unavailable classifier datasets and
`P.MM.01.MSG.014.R2` were audited solely against workspace material. The
conflicts remain real conflicts; R.006/R.007 are missing concrete evidence,
classifier data is identity-unresolved/dataset-missing, and R2 needs external
registry evidence. No warning or blocker was removed. See
`P_MM_01_REMAINING_NORMATIVE_DIAGNOSTICS_AUDIT.md`.

## Local audit of five normative conflicts — 2026-08-25

`NORMATIVE_CONFLICT-001` through `-005` were re-audited only against local
materials. The supplied Decision No. 68 PDF and its existing source-traced
records prove each source/structure mismatch, but contain no correction,
applicable replacement, alias, or version-transition rule that can select a
safe implementation. All five are therefore retained as
`REAL_NORMATIVE_CONFLICT`; resolution is `NOT_ENOUGH_LOCAL_EVIDENCE`.
MSG.002, MSG.023 and MSG.024 remain blocked with `NORMATIVE_CONFLICT`.
No production/package/XML/session/GUI logic changed. See
`NORMATIVE_CONFLICTS_001_005_AUDIT.md`.

## Conditional rules audit — 2026-08-25

P.MM.01 содержит 133 conditional field usages в 12 MSG. Machine-readable source/operator/value/effect metadata отсутствует: machine-evaluable 0, unresolved 133. Все условия остаются видимыми и annotated; dynamic behaviour не создано из русского текста. MSG.001: 17/0/17. Нормативные конфликты MSG.002, MSG.023 и MSG.024 сохраняют приоритет. Подробности: `CONDITIONAL_RULES_REPORT.md`.

GUI/application layer supports local JSON drafts, atomic manual save, dirty-state,
debounced autosave and recovery. Draft loading revalidates against the current
P.MM.01 form; blocked generation statuses remain enforced.

`R.006` and `R.007` retain `active_version: null`. In TEST they use their own
normative `Y.Y.Y` definitions and imported `X.X.X` namespaces; STRICT remains
`UNRESOLVED_STRUCTURE_VERSION`. All active healthcare structures also retain
their concrete root versions but their imported model namespaces still carry
`X.X.X`, so their current output is likewise `VERSION_PLACEHOLDER_TEST`.

- package code: `P.MM.01`
- status: `BODY_MODEL_CONFIRMED_WITH_EXTERNAL_CONFLICTS`
- process version: `1.1.0`
- procedures: 19
- operations: 57
- participants: 6 source-traced definitions
- transactions: 19
- messages: 28
- structures: 8
- message-rule indexes: 16
- classifiers: `NOT_AVAILABLE`
- XSD: `NOT_AVAILABLE`
- normative Body rows: 555 / 555 represented
- executable message-rule tables: 16 (201 rows represented)
- field interpretations: 491 verified, 64 external dependencies, 0 unresolved
- message-rule interpretations: 195 verified, 1 external dependency, 5 internal normative conflicts, 0 unresolved

The package passes loader and cross-reference validation. Active versions are
selected independently per structure. `R.006` and `R.007` have
`active_version: null` and return `UNRESOLVED_STRUCTURE_VERSION` on concrete
resolution without blocking the six resolved subject-area structures. The
generic Body engine is integrated. `R.HC.MM.01.004` serialization and a
Decision No. 5 SOAP end-to-end path are verified. Ambiguous rows are blocked as
external classifier dependencies. The five remaining MessageRules are confirmed internal source/structure
conflicts. MSG.002, MSG.023 and MSG.024 fail explicitly with
`NORMATIVE_CONFLICT`; other messages remain independent. Physical XSD and
classifiers remain absent and the package is not production-ready.

Addressing was re-audited against Decision No. 5 paragraphs 30–34 and 45–54
and Decision No. 68 table 1/pages 6–8. Commission is participant `P.ACT.001`
in fixed segment `EEC`; the competent member-state authority is participant
`P.MM.01.ACT.001` in an ISO alpha-2 national segment (`RU` only in current test
data). All 19 transactions now bind source-defined initiator/respondent
participants. TRN.004 MSG.005 uses To
`EAEU://EEC/CP/P.MM.01/P.ACT.001` and ReplyTo
`EAEU://RU/CP/P.MM.01/P.MM.01.ACT.001`; MSG.006 reverses the endpoints and
correlates to MSG.005.

Catalog-driven E2E classification covers all 19 transactions and every one of
their 43 initiating/response branches: 37 `VERSION_PLACEHOLDER_TEST`, 3
`NORMATIVE_CONFLICT` and 3 `INITIAL_MESSAGE_BLOCKED`. The 37 generated
SOAP examples and 6 blocked reports are stored under
`examples/all_transactions/`; the earlier seven focused TRN.004–006 artifacts
remain under `examples/p_mm_01/`. Notification and mutual-obligation behavior
is verified against the generic Decision No. 5 state machine. No runtime
timers, transport, authentication or signature enforcement was added.

`ALL_TRANSACTIONS_E2E_CLASSIFIED = true`

The universal engine application facade now discovers this package from an
explicit processes root and exposes all 19 transactions and 43 branches as
GUI-safe DTOs. P.MM.01 integration tests cover typed unresolved/conflict
results, classifier `TEST_ONLY` warnings, full SOAP generation and a correlated
request/response session. No process-specific facade logic was added.

The generic wx GUI discovers P.MM.01 without hardcoding and its controller
verifies visible unresolved/conflict blockers, classifier `TEST_ONLY` warning,
the seven-root-field MSG.007 form and successful facade validation/generation.

The revised wx notebook UI passed a real macOS smoke: TRN.005/MSG.007 test data
validated and generated SOAP on the XML tab; TRN.004/MSG.005 remained visibly
blocked on the Data tab. `EDocHeader` is shown as `Заголовок электронного
документа`, with `ccdo:EDocHeader` retained only in field help.

Generic facade issue aggregation currently reports nine P.MM.01 diagnostics:
two unresolved structure versions, five individual normative conflicts, one
external-classifier warning and one delegated external-source warning. The GUI
shows seven blocking and two warning items without process-specific logic.
# Field input policy audit (2026-08-24)

Классифицированы все 2960 field usages во всех 28 MSG-контекстах. Подтверждено: AUTO_FIXED 56, AUTO_GENERATED 28, CLASSIFIER 356, CORRELATION 11, EXTERNAL_SYSTEM 1, CONDITIONAL 133; UNRESOLVED 1831; structural containers 544. Подробности: `FIELD_INPUT_POLICY_REPORT.md`.
# UI input policy audit (2026-08-24)

Normative `UNRESOLVED_INPUT_POLICY` не изменён: 1831. Project UI classification делает формы пригодными для заполнения: 2184 USER_INPUT, 95 READ_ONLY, 1 EXTERNAL_SYSTEM, 539 GROUP, 9 HIDDEN, 132 UNRESOLVED_UI_POLICY. Полный список всех usages и origin: `UI_INPUT_POLICY_REPORT.md`.
# Messages guide complete (2026-08-24)

`P_MM_01_MESSAGES_GUIDE.md` покрывает 28/28 MSG и 2960/2960 field usages. Описания: 2960/2960; examples: 2202/2960; sources: 2960/2960; unresolved UI: 132; normative conflicts: 5. Точечное presentation-исправление: UpdateDateTime скрыт в request MSG.005, но остаётся EXTERNAL_SYSTEM в response MSG.006. Текущие UI counts: USER_INPUT 2183, HIDDEN 10; normative unresolved 1831.
# Guide quality improvement complete (2026-08-24)

Examples: 2202 → 2393; without examples: 758 → 567. Origins: FIXED 56, CLASSIFIER 356, DATATYPE 1089, PROJECT_DOCUMENTATION 892, UNAVAILABLE 567. UNRESOLVED_UI_POLICY остаётся 132; UI policy changes 0. Подробный аудит: `GUIDE_QUALITY_IMPROVEMENT_REPORT.md`.
# 2026-08-24 — large form presentation

Универсальный GUI поддерживает presentation-only фильтры и поиск без изменения P.MM.01 normative package. Для MSG.001 подтверждено отображение: ALL 401, REQUIRED 168, USER_FIELDS 398; Facade summary manual fields = 307. MSG.005, MSG.019 и конфликтный MSG.002 проходят generic filter regression. Значения, repeatable items и validation сохраняются в полном BodyValues. wx smoke: `WX_LARGE_FORM_FILTER_SMOKE_OK`.
# MessageRules audit (Decision No. 68)

All 28 messages are explicitly classified: 16 have separate normative rule tables and corresponding non-empty YAML files; 12 have no separate table and intentionally have no YAML. `NEEDS_VERIFICATION = 0`. See `MESSAGE_RULES_AUDIT.md`.
# Editable automatic fields audit (2026-08-25)

The complete 95-item READ_ONLY baseline was classified. Current presentation totals: AUTO_ONLY 56, AUTO_ASSISTED_EDITABLE 28, CORRELATION_ONLY 11, EXTERNAL_SYSTEM 1, OTHER 0. EDocId is editable with an IdentifierService-backed generator in all 28 messages. InfEnvelopeCode/EDocCode remain fixed read-only, EDocRefId remains correlation read-only, and MSG.006 UpdateDateTime remains external-system-only. There are 233 DATE/TIME/DATETIME usages. See `EDITABLE_AUTO_FIELDS_AUDIT.md`.
# GUI user acceptance (2026-08-25)

TRN.004, TRN.005, TRN.011, TRN.008 and MSG.001 passed real wx acceptance. All five required markers were produced. Two HIGH generic GUI bugs were fixed; two MEDIUM design issues remain documented (transaction-session restoration from drafts and binary-file input UX). Performance remained below 0.2 seconds for every measured single operation. Full details: `GUI_USER_ACCEPTANCE_REPORT.md`.

# Binary and minor UX (2026-08-25)

53/53 unique `csdo:BinaryTextType` usages receive the generic file picker; 115
boolean usages display Да/Нет. Embedded base64 survives draft restore without a
source path. UAT-004/UAT-005 fixed; UAT-003 session recovery remains unchanged.
See `BINARY_AND_MINOR_UX_REPORT.md`.

# Transaction session persistence audit (2026-08-25)

Current P.MM.01 drafts are not safe session snapshots. Request/response IDs
alone cannot restore notification, TRN.008/TRN.012 mutual obligations, retry or
timeout state. Automatic restore remains disabled. Recommended design and
prerequisites: `TRANSACTION_SESSION_PERSISTENCE_AUDIT.md`.

# Session snapshot v1 implemented (2026-08-25)

Отдельный versioned `*.eaeusession.json` storage реализован и покрывает TRN.004
request/response history. Legacy drafts сохраняют `SESSION_RESTART_REQUIRED`.
Automatic restore и GUI Continue отсутствуют; storage-only этап требовал
unified application TransactionEngine lifecycle, реализованный последующим
этапом ниже. См. `TRANSACTION_SESSION_SNAPSHOT_IMPLEMENTATION.md`.

# Runtime restore implemented (2026-08-25)

Unified lifecycle и strict snapshot→runtime restore реализованы без GUI.
TRN.004 сохраняет request IDs и создаёт корректный новый response; TRN.008
восстанавливает signal history/state. Legacy draft restore запрещён. Future GUI
может использовать только `RESTORABLE`; timing/mismatch выдаются без session.
См. `TRANSACTION_SESSION_RESTORE_IMPLEMENTATION.md`.
# Responsive GUI layout (2026-08-25)

Универсальный GUI больше не обрезает правую часть формы при narrow resize:
action/filter controls переносятся, FormPanel доступен по обеим осям, длинные
summary texts повторно оборачиваются. Real macOS wx regression прошёл на
`700x560` и при последующем увеличении. P.MM.01 package и session/XML semantics
не менялись. См. `GUI_RESPONSIVE_LAYOUT_IMPLEMENTATION.md`.
# GUI transaction session controls (2026-08-25)

Open/Continue/Save Session и Open-as-new через отдельный Body draft реализованы.
Continue использует только typed RESTORABLE result и exact restored runtime.
Real macOS wx acceptance доказал сохранение ProcedureID, ConversationID,
historical MessageID/history и корректный новый response MessageID/RelatesTo.
Legacy draft restore запрещён. См. `GUI_TRANSACTION_SESSION_CONTROLS_IMPLEMENTATION.md`.
# Restored session final XML audit (2026-08-25)

TRN.004 fresh restart→restore→MSG.006 final XML proves preserved SOAP IDs,
correct new MessageID/RelatesTo/Action, namespaces and history. Signal, Fault and
notification XML also pass. Production continuation remains NO: previous
request EDocId is absent after restore, so GUI cannot source response EDocRefId;
retry XML payload reconstruction is also unavailable. См.
`RESTORED_SESSION_XML_END_TO_END_AUDIT.md`.
# Message artifact persistence (2026-08-25)

Bundle persistence now preserves request EDocId and original retry Body after
restart. TRN.004 restored response has EDocRefId from artifact; retry XML has a
fresh SOAP header and original Body. Session-persistence readiness is YES only;
P.MM.01 overall production readiness remains blocked by unrelated normative/XSD
items. See `MESSAGE_ARTIFACT_PERSISTENCE_IMPLEMENTATION.md`.
