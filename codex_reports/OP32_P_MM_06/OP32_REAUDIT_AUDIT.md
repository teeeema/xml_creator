# OP32 / P.MM.06 — полный повторный re-audit

**Baseline date:** 2026-10-06  
**Status:** COMPLETE_WITH_DOCUMENTED_BLOCKERS  
**Package:** `P.MM.06_OP_32`  
**Primary source:** `/Users/tema/Documents/Work/Документы_xml/32_ОП.pdf`  
**PDF pages:** 212  
**Normative act:** Решение Коллегии ЕЭК от 30.08.2016 №92 «О технологических документах, регламентирующих информационное взаимодействие при реализации средствами интегрированной информационной системы внешней и взаимной торговли общего процесса “Формирование, ведение и использование единого реестра медицинских изделий, зарегистрированных в рамках Евразийского экономического союза”».  
**Document edition:** с изменениями Решений Коллегии ЕЭК от 19.09.2017 №120 и от 28.02.2023 №19.  
**Process:** `P.MM.06`, version **1.1.0** (PDF p.5, point 6).

## Scope restored from PDF

- Participants: **7 total** = `P.ACT.001` (Комиссия) + `P.MM.06.ACT.001–006`.
- Operations: **46** = `P.MM.06.OPR.001–046`. Current package has **44** and omits normative `OPR.007` and `OPR.008`.
- Procedures: **15**.
- Transactions: **15**.
- Messages: **24**.
- Process-specific structures: **5** (`R.HC.MM.06.001–005`), plus shared `R.006` and `R.007`.

`OPR.007` and `OPR.008` are not reserved gaps: PDF pp.28–32 explicitly defines **Проверка возможности опубликования сведений в едином реестре** and **Опубликование сведений о регистрации медицинского изделия**, both inside `P.MM.06.PRC.002`. Their absence in `operations.yaml` is a package catalog gap; this audit does not modify production data.

## Structures / XSD

- `R.006` — уведомление о результате обработки; version `Y.Y.Y`; root `{urn:EEC:R:ProcessingResultDetails:vY.Y.Y}ProcessingResultDetails`; expected XSD `EEC_R_ProcessingResultDetails_vY.Y.Y.xsd`; PDF p.161; local XSD **NOT FOUND**.
- `R.007` — состояние актуализации общего ресурса; version `Y.Y.Y`; root `{urn:EEC:R:ResourceStatusDetails:vY.Y.Y}ResourceStatusDetails`; expected XSD `EEC_R_ResourceStatusDetails_vY.Y.Y.xsd`; PDF p.164; local XSD **NOT FOUND**.
- `R.HC.MM.06.001` — сведения о регистрации медицинских изделий; version `1.1.0`; root `{urn:EEC:R:HC:MM:06:MedicalProductRegistrationDetails:v1.1.0}MedicalProductRegistrationDetails`; expected XSD `EEC_R_HC_MM_06_MedicalProductRegistrationDetails_v1.1.0.xsd`; PDF p.168; local XSD **NOT FOUND**.
- `R.HC.MM.06.002` — сведения о рассмотрении экспертного заключения; version `1.1.0`; root `{urn:EEC:R:HC:MM:06:MedicalProductRegistrationExpertReportDetails:v1.1.0}MedicalProductRegistrationExpertReportDetails`; expected XSD `EEC_R_HC_MM_06_MedicalProductRegistrationExpertReportDetails_v1.1.0.xsd`; PDF p.189; local XSD **NOT FOUND**.
- `R.HC.MM.06.003` — документ, содержащийся в регистрационном досье или оформленный при его рассмотрении; version `1.1.0`; root `{urn:EEC:R:HC:MM:06:MedicalProductRegistrationDocContentDetails:v1.1.0}MedicalProductRegistrationDocContentDetails`; expected XSD `EEC_R_HC_MM_06_MedicalProductRegistrationDocContentDetails_v1.1.0.xsd`; PDF p.194; local XSD **NOT FOUND**.
- `R.HC.MM.06.004` — сведения о номере регистрационного удостоверения на медицинское изделие; version `1.1.0`; root `{urn:EEC:R:HC:MM:06:MedicalProductRegistrationNumberRequestDetails:v1.1.0}MedicalProductRegistrationNumberRequestDetails`; expected XSD `EEC_R_HC_MM_06_MedicalProductRegistrationNumberRequestDetails_v1.1.0.xsd`; PDF p.201; local XSD **NOT FOUND**.
- `R.HC.MM.06.005` — сведения о виде медицинских изделий; version `1.1.0`; root `{urn:EEC:R:HC:MM:06:MedicalProductCodeTransformationDetails:v1.1.0}MedicalProductCodeTransformationDetails`; expected XSD `EEC_R_HC_MM_06_MedicalProductCodeTransformationDetails_v1.1.0.xsd`; PDF p.204; local XSD **NOT FOUND**.

Recursive search found **0 `.xsd` files** both under `/Users/tema/Documents/Work/Документы_xml/**` and the repository. The PDF proves expected schema filenames, but the schema bytes are absent. The PDF also states imported namespaces as `urn:EEC:M:...:vX.X.X` and `urn:EEC:M:HC:...:vZ.Z.Z`; `version_profiles/current.yaml` preserves those placeholders. Thus root QName is proven for `R.HC.MM.06.001–005`, while exact leaf Clark QNames are not.

## Classifiers

PDF pp.21–23 defines the classifier catalog:

- P.CLS.009 — единицы измерения
- P.CLS.019 — страны мира / ISO 3166-1
- P.CLS.024 — языки / ISO 639-1
- P.CLS.054 — организационно-правовые формы
- P.CLS.064 — номенклатура медицинских изделий ЕАЭС
- P.MM.06.CLS.001 — виды документов, оформляемых при рассмотрении досье
- P.MM.06.CLS.002 — виды документов регистрационного досье
- P.MM.06.CLS.003 — статусы регистрационных удостоверений
- P.MM.06.CLS.004 — статусы хода рассмотрения заявления
- P.MM.06.CLS.005 — виды элементов документов

No machine-readable classifier payloads were found in the primary normative directory. Requirements that require membership/semantic code mapping are therefore `OPEN_CLASSIFIER`. A `codeListId` literal pointing to the country classifier is not itself treated as requiring the payload when the classifier identifier is derivable from Table 9.

## Requirements

The old report counted **178** rows. Re-reading the PDF shows that Table 16 for `MSG.012` contains **2**, not 11, requirements and Table 25 for `MSG.024` contains **1**, not 8. The previous parser had consumed text from the following normative documents. Correct raw normative rows = **162**.

Six compound rows contain independent obligations and were atomized conservatively (two registry-name rows split into three comparisons each; MSG.002 row 5 into two required fields; row 40 into contact-presence and phone-value assertions; row 45 into presence and member-state comparison; MSG.015 row 7 into PDF presence and PDF-content assertions). Final atomic requirements = **170**. OR/XOR alternatives and predicates that must hold on the same external record remain one atomic semantic requirement.

Strict `IMPLEMENTED_CONFIRMED` = **0**. All 14 OP32 `message_rules/*.yaml` files contain zero `structured_rules`, zero `business_rules`, zero `fixed_values`, and zero `field_usage`, so the old **108 FULLY_MAPPABLE/executable** number was not production implementation evidence.

Open gaps = **170**:

- `OPEN_ENGINE`: **2**
- `OPEN_PRODUCTION_MAPPING`: **0**
- `OPEN_CLASSIFIER`: **59**
- `OPEN_EXTERNAL_REGISTRY`: **11**
- `OPEN_NORMATIVE_AMBIGUITY`: **1**
- `OPEN_SOURCE_CONFLICT`: **0**
- `OPEN_MISSING_STRUCTURE`: **0**
- `OPEN_MISSING_NORMATIVE_DATA`: **97**
- `OTHER_OPEN`: **0**

## Engine recheck

The shared engine has materially advanced: `condition.any`, `for_each`, filtered selectors, positional selectors, selection cardinality, cross-instance comparison, typed DATETIME and aggregate comparison are present. The previous **35 `ENGINE_UNSUPPORTED` OR** gaps are stale as engine blockers. They are reclassified according to the remaining real dependency (mostly missing exact QName namespace data or classifier data).

Two engine capabilities are still absent for this OP32 baseline: regex/string-pattern matching required by the e-mail rule and semantic inspection of PDF binary content required by the expert-report rule.

## QName result

- Historical hint before the old completion pass: approximately **175 unresolved**.
- Immediate old final audit later claimed **0 unresolved** among its 70 missing-data rows, but it stored prefixes such as `hcsdo:` without proving concrete `vZ.Z.Z` namespace versions.
- New exact requirement-level QName resolved: **0 / 170**.
- New exact QName still unresolved: **170 / 170** because concrete imported model namespace versions/XSD are absent.
- QName source conflicts: **0**.
- Missing structure documents: **0**; the structure tables exist in the PDF. The blocker is missing exact imported namespace/model data, classified as `OPEN_MISSING_NORMATIVE_DATA` unless a stronger classifier/external/engine/ambiguity blocker applies.

## Normative ambiguity

Table 14 requirement 47 literally says: `...то если реквизит ... заполняется обязательно`. The extra `если` makes the consequence grammatically ambiguous. This audit does not silently rewrite it and classifies it `OPEN_NORMATIVE_AMBIGUITY`.

## Old vs new

- Old report total: **178**; new atomic total: **170**.
- Old gaps: **70**; new gaps: **170** under the strict implementation criterion.
- Old engine gaps: **35**; all **35** old OR blockers are now supported by the engine and reclassified.
- Net gap increase: **+100**. This is not a one-to-one ID delta because 16 phantom rows were removed and 8 atomic requirements were added while old mappability claims were downgraded to open until production evidence exists.

## Verification

- OP32 package tests: **8 passed**.
- Relevant engine tests: **53 passed, 5 subtests passed**.
- OP22 regression: **3103 passed**.
- OP23 baseline: **148 failed, 117 passed, 27 subtests passed**; failures are dominated by the pre-existing/parallel `Unknown process: P.SP.03` registration/discovery issue and were not modified in this audit.
- OP26 baseline: **3 failed, 84 passed, 83 subtests passed**; observed failures include pre-existing artifact/session-restore expectations and `message_id` restoration.
- `eaeu_xml/tests`: **1 failed, 368 passed, 62240 subtests passed**; existing failure is `SessionRestoreTests.test_mutual_obligations_signal_history_restores_then_advances` with `KeyError: 'message_id'`.
- Full suite: **222 failed, 3636 passed, 3 errors, 50633 subtests passed**; failures are dominated by the pre-existing/parallel OP23 registration/discovery issue plus the existing P.MM.01/session-restore issue.
- Requirement arithmetic: **PASS** (`170 = 0 implemented + 170 open`).
- Open-reason arithmetic: **PASS** (`2 + 0 + 59 + 11 + 1 + 0 + 0 + 97 + 0 = 170`).
- Traceability completeness: **PASS** for all 170 atomic requirements.
- Duplicate canonical requirement IDs: **0**.

## Delivery blockers / next step

1. Obtain the official XSD set or concrete base/healthcare model versions replacing `X.X.X`/`Z.Z.Z`; re-resolve exact leaf QNames and paths.
2. Obtain machine-readable classifier datasets and versions for classifier-dependent rules.
3. Resolve Table 14 requirement 47 from an official corrected source/clarification.
4. Only after those items, build the SAFE production batches. Current safe mapping count is **0**.

This session did not change OP32 production rules, shared engine, GUI, OP22, OP23, OP26, or OP49 files.
