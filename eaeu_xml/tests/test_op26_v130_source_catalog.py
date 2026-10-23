"""Evidence integrity for source-only catalogs; never a production acceptance test."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'P.MM.01_OP_26/versions/1.3.0'
REPORT = ROOT / 'codex_reports/OP26_P_MM_01/V130_COMPLETION'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


class Op26SourceCatalogTests(unittest.TestCase):
    def test_every_message_and_transaction_reference_resolves_inside_edition(self):
        procedures = {x['procedure_code'] for x in read(PACKAGE / 'procedures.yaml')['procedures']}
        operations = {x['operation_code'] for x in read(PACKAGE / 'operations.yaml')['operations']}
        messages = {x['message_code'] for x in read(PACKAGE / 'messages.yaml')['messages']}
        used_messages, used_procedures = set(), set()
        for transaction in read(PACKAGE / 'transactions.yaml')['transactions']:
            self.assertIn(transaction['procedure_code'], procedures)
            self.assertIn(transaction['initiating_operation'], operations)
            self.assertIn(transaction['responding_operation'], operations)
            used_procedures.add(transaction['procedure_code'])
            used_messages.update((transaction['initiating_message'], *transaction['response_messages']))
        self.assertEqual(used_messages, messages)
        self.assertEqual(used_procedures, procedures)
        self.assertEqual((len(procedures), len(operations), len(messages)), (28, 84, 41))

    def test_transaction_001_no_longer_returns_application_number(self):
        transactions = {x['transaction_code']: x for x in read(PACKAGE / 'transactions.yaml')['transactions']}
        self.assertEqual(transactions['P.MM.01.TRN.001']['response_messages'], ['P.MM.01.MSG.004'])
        self.assertIn('P.MM.01.MSG.013', transactions['P.MM.01.TRN.023']['response_messages'])

    def test_latest_classifier_amendment_is_applied_without_claiming_dataset(self):
        data = read(PACKAGE / 'classifier_references.yaml')
        codes = {x['classifier_code'] for x in data['classifiers']}
        self.assertNotIn('P.MM.01.CLS.009', codes)
        self.assertNotIn('P.MM.01.CLS.010', codes)
        self.assertTrue({'P.MM.01.CLS.028', 'P.MM.01.CLS.029'} <= codes)
        self.assertFalse(data['datasets_available'])
        self.assertFalse(any(p.is_file() and not p.name.startswith('.') for p in (PACKAGE / 'classifiers').iterdir()))

    def test_structure_versions_and_removed_structure_follow_source(self):
        inventory = read(PACKAGE / 'structures/source_inventory.json')['structures']
        ids = {s['structure_id'] for s in inventory}
        self.assertEqual(len(ids), 7)
        self.assertNotIn('R.HC.MM.01.002', ids)
        self.assertEqual(sum(len(s['fields_source_rows']) for s in inventory), 710)
        for s in inventory:
            self.assertEqual(s['declared_version'], 'Y.Y.Y' if s['structure_id'] in ('R.006', 'R.007') else '1.3.0')
        profile = read(PACKAGE / 'version_profiles/current.yaml')
        self.assertIsNone(profile['models']['base'])
        self.assertIsNone(profile['models']['healthcare'])

    def test_requirements_remain_explicitly_non_executable_and_scoped(self):
        files = list((PACKAGE / 'message_rules').glob('*.yaml'))
        self.assertEqual(len(files), 33)
        count = 0
        for path in files:
            data = read(path)
            source_ids = {r['rule_id'] for r in data['business_rules']}
            self.assertTrue(all(r.get('source_row_id') in source_ids for r in data['structured_rules']))
            for rule in data['business_rules']:
                self.assertEqual(rule['interpretation_status'], 'NOT_EXECUTABLE_SOURCE_TEXT')
                self.assertTrue(rule['source_refs'])
                count += 1
        self.assertEqual(count, 481)
        first = read(PACKAGE / 'message_rules/P.MM.01.MSG.001.yaml')['business_rules']
        self.assertTrue(any(r['source_requirement_code'] == '87' and r['source_refs'][0]['source_id'] == 'SRC-PMM01-77' for r in first))

    def test_amended_inherited_range_handles_source_typographic_dash(self):
        rules = read(PACKAGE / 'message_rules/P.MM.01.MSG.002.yaml')['business_rules']
        inherited = next(r for r in rules if r['source_requirement_code'] == '3-87')
        self.assertIn('3-87 таблицы 26', inherited['requirement'])
        self.assertEqual(inherited['source_refs'][0]['source_id'], 'SRC-PMM01-77')

    def test_archived_sources_match_recorded_hashes(self):
        hashes = read(REPORT / 'sources/sha256.json')
        for filename, expected in hashes.items():
            self.assertEqual(hashlib.sha256((REPORT / 'sources' / filename).read_bytes()).hexdigest(), expected)

    def test_migration_remains_blocked(self):
        status = read(PACKAGE / 'migration_status.json')
        self.assertEqual(status['state'], 'DRAFT_NOT_READY')
        self.assertIs(status['promotion_allowed'], False)
        self.assertIs(status['active_in_application'], False)


if __name__ == '__main__':
    unittest.main()
