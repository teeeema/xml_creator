"""Stage 3 proof: source grammar, real classifier snapshots and guarded GUI metadata."""
import copy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.core.errors import ProcessPackageValidationError
from eaeu_xml.process_packages import ProcessPackageLoader,GenerationMode
from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator,RuleStatus
from v130_runtime_support import PACKAGE,CLASSIFIER_VALUES,catalogs,sample_values,provider

ROOT=PACKAGE.parents[2]
REPORT=ROOT/'codex_reports/OP26_P_MM_01/V130_STAGE3'
sys.path.insert(0,str(PACKAGE/'tools'))
from rule_patterns import bind_local


class Stage3Tests(unittest.TestCase):
    def test_country_snapshot_is_complete_versioned_and_matches_every_official_page(self):
        snapshots=json.loads((REPORT/'sources/nsi_acquisition.json').read_text())
        complete=[r for r in snapshots if r['status']=='COMPLETE_OFFICIAL_SNAPSHOT']
        self.assertEqual(len(complete),8)
        for row in complete:
            with self.subTest(code=row['nsi_code']):
                records=[]
                for call in row['calls']:
                    path=ROOT/call['artifact']
                    self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),call['sha256'])
                    if '.page_' in path.name:records.extend(json.loads(path.read_text()))
                self.assertEqual(len(records),row['expected_count'])
                self.assertEqual({r['data']['Code'] for r in records},CLASSIFIER_VALUES[row['nsi_code']])
                self.assertTrue(all(r['status']=='actual' for r in records))
                self.assertEqual(row['publication_status'],'published')
        self.assertIn('RU',CLASSIFIER_VALUES['2021']);self.assertNotIn('ZZ',CLASSIFIER_VALUES['2021'])
        self.assertEqual(len(CLASSIFIER_VALUES['2021']),249)

    def test_corrupt_or_duplicate_snapshots_fail_closed(self):
        good=json.loads((PACKAGE/'classifiers/2021.json').read_text())
        with TemporaryDirectory() as folder:
            path=Path(folder);file=path/'one.json'
            for mutation in ({'complete':False},{'values':'RU'},{'expected_count':1},{'publication_status':'draft'}):
                with self.subTest(mutation=mutation):
                    file.write_text(json.dumps(good|mutation))
                    with self.assertRaises(ProcessPackageValidationError):ProcessPackageLoader.load_classifier_values(path)
            file.write_text(json.dumps(good));(path/'two.json').write_text(json.dumps(good))
            with self.assertRaises(ProcessPackageValidationError):ProcessPackageLoader.load_classifier_values(path)

    def test_classifier_predicate_is_not_pass_without_dataset(self):
        rule=dict(kind='field_constraint',operation='CLASSIFIER',classifier_ref='2021',target='Country',ancestors=[])
        self.assertEqual(StructuredRuleEvaluator().evaluate(rule,{'Country':'RU'}).status,RuleStatus.NOT_EVALUATED_EXTERNAL_REFERENCE)
        evaluator=StructuredRuleEvaluator(CLASSIFIER_VALUES)
        self.assertEqual(evaluator.evaluate(rule,{'Country':'RU'}).status,RuleStatus.PASS)
        self.assertEqual(evaluator.evaluate(rule,{'Country':'ZZ'}).status,RuleStatus.FAIL)

    def test_field_classifier_rejects_wrong_code_via_existing_provider(self):
        ss,rr,mm=catalogs();m=mm['P.MM.01.MSG.001'];s=ss[m.structure_id]
        values=sample_values(s,m,rr[m.message_code])
        rule=next(r for r in rr[m.message_code].structured_rules if r.get('operation')=='CLASSIFIER' and r.get('classifier_ref')=='2021')
        path=rule['target']
        # Exercise declared field lookup using the same source-confirmed MSG binding.
        s=replace(s,fields=tuple(replace(f,classifier_ref='2021') if f.path==path else f for f in s.fields))
        values[path]='ZZ'
        result=provider(rr).validate_body(m,s,values,mode=GenerationMode.TEST)
        self.assertTrue(any(i.code=='CLASSIFIER_VALUE_INVALID' and i.field_path==path for i in result.issues))

    def test_quote_conjunction_and_genitive_cardinality_are_compiled(self):
        s=json.loads((PACKAGE/'structures/R.HC.MM.01.001/1.3.0.yaml').read_text())
        rules=json.loads((PACKAGE/'message_rules/P.MM.01.MSG.001.yaml').read_text())['business_rules']
        for number,operation in [('3','REQUIRED'),('4','FORBIDDEN'),('5','CARDINALITY')]:
            row=next(r for r in rules if r['source_requirement_code']==number)
            atoms,reason=bind_local(row,s)
            self.assertIsNone(reason);self.assertEqual(atoms[0]['operation'],operation)
        wrong=copy.deepcopy(next(r for r in rules if r['source_requirement_code']=='3'))
        wrong['requirement']=wrong['requirement'].replace('csdo:StartDateTime','hcsdo:StartDateTime')
        self.assertFalse(bind_local(wrong,s)[0])

    def test_uniqueness_and_order_are_scoped_to_each_actual_root(self):
        values={'Root':[{},{}],'Root/Countries':[[{},{}],[{}]],'Root/Countries/Code':[['RU','BY'],['RU']]}
        rule=dict(kind='field_constraint',operation='UNIQUE',target='Root/Countries/Code',ancestors=['Root'])
        evaluator=StructuredRuleEvaluator();self.assertEqual(evaluator.evaluate(rule,values).status,RuleStatus.PASS)
        values['Root/Countries/Code'][0]=['RU','RU']
        self.assertEqual(evaluator.evaluate(rule,values).status,RuleStatus.FAIL)
        rule.update(operation='POSITIONAL_VALUES',first_value='01',other_value='02')
        values['Root/Countries/Code']=[['01','02'],['01']]
        self.assertEqual(evaluator.evaluate(rule,values).status,RuleStatus.PASS)
        values['Root/Countries/Code'][1]=['02']
        self.assertEqual(evaluator.evaluate(rule,values).status,RuleStatus.FAIL)

    def test_read_only_draft_availability_never_changes_legacy_application_engine(self):
        with TemporaryDirectory() as directory:
            app=EaeuXmlApplication(ROOT,drafts_root=Path(directory))
            first=app._engine('P.MM.01');editions=app.describe_process_editions('P.MM.01')
            self.assertEqual(first.package.profile.process_version,'1.1.0')
            draft=next(r for r in editions if r['version']=='1.3.0')
            self.assertFalse(draft['available']);self.assertEqual(draft['block_code'],'PROCESS_VERSION_NOT_READY')
            self.assertIs(first,app._engine('P.MM.01'))
            self.assertEqual(len(first.package.messages),28)

    def test_raw_unicode_is_preserved_separately_from_normalized_xml_tokens(self):
        raw=json.loads((PACKAGE/'structures/source_inventory.json').read_text())['structures']
        ss,_,_=catalogs();count=0
        for source in raw:
            for row,field in zip(source['fields_source_rows'],ss[source['structure_id']].fields,strict=True):
                original=next(c for c in row if c)
                count+='\u200c' in original
                self.assertFalse(any('\u200c' in (v or '') for v in (field.xml_name,field.namespace_prefix)))
                if field.xml_name:self.assertIn(field.xml_name,original.replace('\u200c',''))
        self.assertEqual(count,708)
