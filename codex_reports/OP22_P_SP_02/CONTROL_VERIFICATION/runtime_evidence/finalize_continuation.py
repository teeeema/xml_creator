"""Consolidate current evidence. Does not run or alter product code/tests."""
import csv
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.application import EaeuXmlApplication

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
REPORT = OUT.parent


def main():
    app = EaeuXmlApplication(ROOT)
    read = lambda name: json.loads((OUT / name).read_text())
    c3 = read('continuation_case03.json')
    extras = read('continuation_case04_case15.json')
    op22 = read('op22_cases_05_06_11_12_13_15.json')
    other = read('op26_op23_B_case07_case08_case14_evidence.json')
    op49 = read('op49_case09_case10_evidence.json')
    assert c3['result'] == 'PASS' and extras['04']['result'] == 'SOURCE_BLOCKED'
    assert extras['15']['result'] == 'PASS'
    with (REPORT / 'CONTROL_CASES.csv').open(newline='') as f:
        reader = csv.DictReader(f)
        columns, old = reader.fieldnames, list(reader)
    rows = old[:2]  # Preserve the two user-confirmed cases without execution.
    cases = []

    def add(n, title, process, trn, msg, req, source, policy, runtime, positive, negative, evidence, result='PASS', reason='Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.'):
        engine = app._engine(process)
        trn_code = process + '.TRN.' + trn
        msg_code = process + '.MSG.' + msg
        transaction = engine.transactions[trn_code]
        assert msg_code in (transaction.initiating_message, *transaction.response_messages)
        row = dict(zip(columns, [f'CV-{n:02}', title, 'OP' + {'P.SP.02':'22','P.SP.03':'23','P.MM.01':'26','P.DS.01':'49'}[process],
                               transaction.procedure_code, trn_code, msg_code, req, source, policy, runtime,
                               '; '.join(positive + negative), result, reason]))
        rows.append(row)
        cases.append({'case_id': row['case_id'], 'evidence_json': evidence,
                      'positive_xml': positive, 'negative_xml': negative,
                      'result': result, 'executed_on': '2026-10-23'})

    add(3, 'OP22 confirmed Code/Name branch', 'P.SP.02', '022', '027', 'P.SP.02.MSG.027.T57.REQ.2; REQ.3 inactive in current classifier revision',
        'ОП_22.pdf pp.578-579 T57 REQ2-3; 92 решение.pdf p.15 / 148 решение.pdf p.4: 07365',
        'Code FIXED07365 readonly; Name FORBIDDEN; explicit policy and scoped structured rule; no legacy fixed_values default',
        'positive PASS; wrong/missing Code, both and legacy Name-only FAIL exact T57.REQ.2; application sanitization checked',
        ['cv03_positive.xml'], ['cv03_' + s + '.xml' for s in ('wrong_code','both','missing_code','legacy_name_only')], 'continuation_case03.json')
    add(4, 'OP22 STILL_EXTERNAL legal-action classifier branch', 'P.SP.02', '049', '054', 'P.SP.02.MSG.054.T72.REQ.4; REQ.5.PRESENCE; REQ.5.VALUE',
        'ОП_22.pdf pp.801-802 T72 REQ4-5; authoritative publication state and code payload not identified locally',
        'Code/Name have no unconditional resolver policy; no invented fixed code',
        'real form/resolver/validator executed; Name branch valid; bad/missing Name and both rejected; unverified Code-only locally accepted',
        ['cv04_name_branch.xml'], ['cv04_' + s + '.xml' for s in ('bad_name','missing_name','both','unverified_code_only')],
        'continuation_case04_case15.json', 'SOURCE_BLOCKED', extras['04']['reason'])
    add(5, 'OP22 MSG054 root-level DocId', 'P.SP.02', '049', '054', 'P.SP.02.MSG.054.T72.REQ.7.DOC_ID',
        'ОП_22.pdf p.803 T72 REQ7', 'root csdo:DocId FORBIDDEN/hidden; nested paths not forbidden by this root rule',
        'positive valid; adding exact-QName root DocId fails T72.REQ.7.DOC_ID',
        ['cv05_msg054_positive.xml'], ['cv05_msg054_forbidden_root.xml'], 'op22_cases_05_06_11_12_13_15.json')
    add(6, 'OP22 MSG056 nested DocId', 'P.SP.02', '050', '056', 'P.SP.02.MSG.056.T74.REQ.18',
        'ОП_22.pdf p.807 T74 REQ18', 'IPPaymentDetails/AccompanyingDocumentsDetails/csdo:DocId REQUIRED; root DocId FORBIDDEN',
        'positive valid; remove attached document DocId: exact REQ18 fails',
        ['cv06_msg056_positive.xml'], ['cv06_msg056_missing_nested_id.xml'], 'op22_cases_05_06_11_12_13_15.json')
    req26 = 'OP26.P_MM_01.P.MM.01.MSG.001.REQ.034'
    for n, title in ((7,'OP26 fixed classifier ID'), (14,'FIXED value protected against raw XML tampering')):
        add(n, title, 'P.MM.01', '001', '001', req26,
            '26_ОП.pdf p.213 REQ34; p.39 P.CLS.019',
            'DrugRegistrationDetails/DrugCountryRegistrationDetails/UnifiedCountryCode/@codeListId FIXED P.CLS.019 readonly',
            'positive serialized attribute P.CLS.019; raw XML changed to P.CLS.999 fails REQ034',
            ['op26_op23_B_case07_positive.xml'], ['op26_op23_B_case14_negative_raw_xml_tamper.xml'], 'op26_op23_B_case07_case08_case14_evidence.json')
    add(8, 'OP23 message-specific REQUIRED/FORBIDDEN', 'P.SP.03', '001', '001', 'P.SP.03.MSG.001.REQ.010; REQ.014; REQ.043',
        'ОП_23.pdf p.342 T16 REQ10/14; p.350 REQ43', 'Application DocId and AuthorityName REQUIRED; ConsentToDataProcessingIndicator FORBIDDEN',
        'positive valid; missing DocId/AuthorityName and added Consent fail exact corresponding rules',
        ['op26_op23_B_case08_positive.xml'], ['op26_op23_B_case08_negative_' + s + '.xml' for s in ('missing_docid','missing_authority','forbidden_consent')], 'op26_op23_B_case07_case08_case14_evidence.json')
    for n, title in ((9,'OP49 structured selection cardinality'), (10,'Contextual rule not statically projected')):
        add(n, title, 'P.DS.01', '001', '001', 'P.DS.01.MSG.001.R002; R003 (T10 REQ2-3)',
            '49_ОП.pdf p.79 T10 REQ2-3', 'where DailyInfoIndicator scopes cardinality; owner and indicator have no unconditional resolver entry',
            'one true passes; duplicate true fails R002; true+false fails R003; false-only fails R002/R003; real form/resolver checked',
            ['op49_case09_generated_positive.xml'], ['op49_case09_' + s + '.xml' for s in ('duplicate_true','add_forbidden_false','replace_daily_with_false')], 'op49_case09_case10_evidence.json')
    add(11, 'Repeatable owner and exact XML path', 'P.SP.02', '023', '028', 'P.SP.02.MSG.028.T44.REQ.33',
        'ОП_22.pdf p.722 T44 REQ33; p.879 T10 row2.16.4',
        'ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId REQUIRED per owner',
        'two XML owners extract [DOCUMENT-1,DOCUMENT-2]; missing second child extracts [DOCUMENT-1,None] and fails exact REQ33',
        ['cv11_msg028_two_documents.xml'], ['cv11_msg028_second_document_missing_id.xml'], 'op22_cases_05_06_11_12_13_15.json')
    add(12, 'Structure OPTIONAL / Message REQUIRED', 'P.SP.02', '050', '056', 'P.SP.02.MSG.056.T74.REQ.18',
        'ОП_23.pdf p.565 T13 row8.10.4: 0..1; ОП_22.pdf p.807 T74 REQ18',
        'nested DocId structure min0; form/resolver REQUIRED within accompanying-document owner',
        'positive valid; missing nested DocId fails REQ18', ['cv06_msg056_positive.xml'], ['cv06_msg056_missing_nested_id.xml'], 'op22_cases_05_06_11_12_13_15.json')
    add(13, 'Structure ALLOWED / Message FORBIDDEN', 'P.SP.02', '049', '054', 'P.SP.02.MSG.054.T72.REQ.7.DOC_ID',
        'ОП_23.pdf p.542 T13 row7: 0..1; ОП_22.pdf p.803 T72 REQ7',
        'root DocId permitted by structure min0; form/resolver FORBIDDEN in message',
        'positive absent root valid; adding root fails exact message REQ7.DOC_ID', ['cv05_msg054_positive.xml'], ['cv05_msg054_forbidden_root.xml'], 'op22_cases_05_06_11_12_13_15.json')
    add(15, 'Additional contextual rule from OP23', 'P.SP.03', '001', '001', 'P.SP.03.MSG.001.REQ.021.or_language',
        'ОП_23.pdf p.344 T16 REQ21', 'IPPartyKindCode AP + IPSubjectName representation OR requires languageCode; contextual rule absent from static req IDs',
        'positive actual XML PASS; deleting languageCode from AP/OR name fails REQ021.or_language',
        ['cv15_op23_positive.xml'], ['cv15_op23_missing_language.xml'], 'continuation_case04_case15.json')
    rows.sort(key=lambda row: row['case_id'])
    cases.sort(key=lambda case: case['case_id'])
    assert len(rows) == 15 and sum(r['result'] == 'PASS' for r in rows) == 14
    assert sum(r['result'] == 'SOURCE_BLOCKED' for r in rows) == 1
    assert all(r['result'] in ('PASS','SOURCE_BLOCKED') for r in rows)
    with (REPORT / 'CONTROL_CASES.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    current_files = sorted({name for c in cases for name in c['positive_xml'] + c['negative_xml']})
    retained = ['MSG005_VALID_CODE.xml','MSG005_REJECT_CODE_AND_NAME.xml','MSG005_REJECT_UNKNOWN_CODE.xml',
                'MSG001_STANDARD.xml','MSG001_CONFLICTING_USER_FIELDS.xml']
    manifest = {}
    for name in current_files + retained:
        path = OUT / name
        raw = path.read_bytes()
        manifest[name] = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
                          'root_qname': ET.fromstring(raw).tag,
                          'origin': 'retained_user_confirmed' if name in retained else 'executed_2026-10-23'}
    summary = {'TOTAL':15,'PASS':14,'FAIL':0,'SOURCE_BLOCKED':1,'NOT_EXECUTED':0,
               'STATUS':'COMPLETE','status_scope':'Control verification executed; external source dependency remains open.',
               'ACTUAL_XML_PROOFS':{'confirmed_cases':14,'partial_source_blocked_cases':1,
                                    'current_unique_files':len(current_files),'retained_unique_files':len(retained)},
               'TESTS':{'passed':435,'scope':'MSG027-030 end_to_end/safe_mapping/repeatable_xml plus test_continuation.py',
                        'full_suite':'NOT RUN: focused scope; no shared engine change'},
               'DIFF_CHECK':'PASS','cases':cases,'xml_manifest':manifest}
    (OUT / 'continuation_final_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    table = '\n'.join(f"| {r['case_id']} | {r['op']} / {r['trn']} / {r['msg']} | {r['requirement']} | {r['result']} |" for r in rows)
    sections = []
    for row in rows[2:]:
        case = next(c for c in cases if c['case_id'] == row['case_id'])
        links = ', '.join(f'[{name}](runtime_evidence/{name})' for name in case['positive_xml'] + case['negative_xml'])
        sections.append(f"### {row['case_id']} — {row['requested_case']}\n\n"
                        f"{row['prc']} / {row['trn']} / {row['msg']}\n\n"
                        f"REQ: `{row['requirement']}`. Source: {row['normative_source']}.\n\n"
                        f"Form / resolver: {row['local_classifier_or_policy']}.\n\n"
                        f"Validator / positive-negative: {row['runtime_proof']}.\n\n"
                        f"Result: **{row['result']}**. {row['reason']}\n\n"
                        f"Evidence: [{case['evidence_json']}](runtime_evidence/{case['evidence_json']}); XML: {links}.\n")
    text = f'''# CONTROL_VERIFICATION — 2026-10-23

TOTAL=15
PASS=14
FAIL=0
SOURCE_BLOCKED=1
NOT_EXECUTED=0
ACTUAL_XML_PROOFS=14 confirmed cases (2 retained); 1 partial external case; {len(current_files)} current + {len(retained)} retained unique XML files
TESTS=435 passed
DIFF_CHECK=PASS
STATUS=COMPLETE — control execution complete; the external source dependency in CV-04 remains open.

PASS applies only to the named control/REQ, not whole-message or whole-process normative certification.
CV-01 (MSG005/07360) and CV-02 (MSG001/07220) retain their existing user-confirmed PASS and artifacts. They were not rerun.
Their existing CSV identities are preserved. All 13 continuation controls were actually executed.
SOURCE_BLOCKED in CV-04 is about an identified external reference payload/publication state, not missing old case definitions.

## ROOT_CAUSE

MSG027 T57 REQ2/3 used XML Code presence as a surrogate for classifier availability. This admitted an arbitrary Code and the obsolete Name-only fallback despite confirmed P.CLS.027 entry07365. The read-only audit reproduced this before edits: 2 failed / 3 passed / 5 deselected in the focused acceptance test. See [READ_ONLY_AUDIT.md](runtime_evidence/READ_ONLY_AUDIT.md).

## CHANGED_FILES

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.027.yaml`: current classifier-present scoped rule; forbidden Name; inactive fallback removed from executable rules while its normative source text is retained.
- `P.SP.02_OP_22/message_field_policies/P.SP.02.MSG.027.yaml`: explicit FIXED07365 / FORBIDDEN form and application policy.
- `P.SP.02_OP_22/tests/test_msg027_end_to_end.py`, `test_msg027_safe_mapping.py`, `test_msg027_repeatable_xml.py`: source-correct fixture and regressions, including wrong/missing Code, Code+Name, obsolete fallback and nested collisions.
- `knowledge_base/decisions/CONTROL_VERIFICATION_2026_10_23.md`: source/evidence note.
- This CSV/report and focused scripts/JSON/XML under `runtime_evidence/`: reproducible control proof.
- `graphify-out/`: required AST refresh. graph.json/report updated; HTML remains stale because 5214 communities exceed its 5000-node rendering limit.

## IMPLEMENTATION

Use existing scoped structured rules and explicit message field policies; no new engine abstraction or other OP change. The legacy `fixed_values` map remains empty for MSG027: validation supplies its defaults before rule evaluation and would conceal a missing raw XML Code. Actual value enforcement belongs to the structured rule, while the application policy fixes form input. Current tests prove both sanitization and independent raw XML rejection.

## NORMATIVE_BASIS

CONFIRMED for the selected passing controls, bounded to the listed local authoritative source documents and exact requirements. Original PDF text, physical page numbers and SHA256 were checked in [continuation_sources.json](runtime_evidence/continuation_sources.json); no historical audit is used as normative proof.

CV-04: UNKNOWN / BLOCKED_BY_SOURCE for authoritative publication state and allowed code membership of the named legal-action reference. No code or classifier identifier was invented. Local Name-branch behavior is evidence of implementation only.

| Case | OP / TRN / MSG | Exact REQ | Result |
|---|---|---|---|
{table}

## VERIFICATION

Final command actually executed (435 passed in 17.75s):

```bash
PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q \\
  P.SP.02_OP_22/tests/test_msg0{{27,28,29,30}}_{{end_to_end,safe_mapping,repeatable_xml}}.py \\
  codex_reports/OP22_P_SP_02/CONTROL_VERIFICATION/runtime_evidence/test_continuation.py --tb=short
```

The expanded 12 test paths were supplied explicitly in the executed command; brace expansion above denotes the identical file set. 435 includes 13 acceptance gates; one gate verifies an executed, evidence-backed SOURCE_BLOCKED result, so green tests do not turn CV-04 into PASS. All XML is serialized, reparsed, extracted and validated by the real package validator. The manifest includes actual QName, size and SHA256 in [continuation_final_summary.json](runtime_evidence/continuation_final_summary.json).

Body generation uses GenerationMode.TEST and local version placeholders where applicable. These are actual XML body proofs, not official XSD validation, complete integration-envelope proof, external-registry validation or production certification. OP49 selected rules pass even though message validation is_complete=False for unrelated unimplemented rules. OP26 fixed codeListId proof does not certify the missing full classifier payload.

`git diff --check`: exit0. Untracked new text files checked separately. Diff reviewed against session baseline; 538 product-file hashes show only four existing MSG027 files changed, plus the new MSG027 policy. Other OP packages and shared engine unchanged: [continuation_scope_check.json](runtime_evidence/continuation_scope_check.json). No commit or push.

`graphify update .`: exit0; AST graph/report refreshed. HTML rendering limitation above remains. Full regression: NOT RUN, because correction is confined to MSG027; nearest MSG027–030 regression and the selected cross-OP controls were executed.

## Controls 3–15

''' + '\n'.join(sections) + '''
## REMAINING_ISSUES

- CV-04: obtain an authoritative legal-action reference payload and its publication state for the applicable revision to close membership/branch selection. Local XML probes are complete; normative closure is blocked.
- Out of selected control scope: read-only audit also confirmed MSG004/07320 enforcement gaps; MSG004 is not a valid STILL_EXTERNAL case. Its existing baseline evidence is retained; no MSG004 change was included in this correction.
- Existing unrelated working-tree modifications are preserved. No whole-repository or production PASS is claimed.
'''
    (REPORT / 'CONTROL_VERIFICATION_FINAL.md').write_text(text)
    print('Consolidated:', {k:summary[k] for k in ('TOTAL','PASS','FAIL','SOURCE_BLOCKED','NOT_EXECUTED','STATUS')})
    print('XML files:',len(current_files),'current +',len(retained),'retained')


if __name__ == '__main__':
    main()
