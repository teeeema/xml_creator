"""Report known implementation gaps without turning imported rows into runtime proof."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REPORT = ROOT / 'codex_reports/OP26_P_MM_01/V130_COMPLETION'
PACKAGE = ROOT / 'P.MM.01_OP_26/versions/1.3.0'
rows = []


def add(identifier, entity, explanation, missing, criterion, refs=(), status='NOT_TESTED', path=None, structure=None, evidence=None):
    rows.append({'gap_id': identifier, 'op': 'P.MM.01', 'entity': entity,
        'structure': structure, 'qname': None, 'path': path, 'source_refs': list(refs),
        'implementation_state': status, 'explanation': explanation, 'missing_or_conflicting': missing,
        'action': 'Remain blocked until closure criterion is evidenced' if status != 'PASS' else 'Fixed in readiness/loader/registry/engine; regression exercised',
        'verification_evidence': evidence, 'closure_criterion': criterion, 'status': status,
        'verdict': 'Подтверждено' if status == 'PASS' else 'Недостаточно данных'})


for identifier, entity, explanation in (
    ('GATE-01', 'Registry', 'Cached version bypassed a revoked readiness passport.'),
    ('GATE-02', 'Engine', 'An engine loaded before revocation could still generate bodies.'),
    ('GATE-03', 'Loader', 'Direct loading did not match passport process identity and profile version.'),
    ('GATE-04', 'Loader', 'Relocating a package outside versions/ bypassed its draft passport.'),
    ('GATE-05', 'Version selector', 'Version manifests could link to legacy files or redirect the versions directory.'),
    ('GATE-06', 'Profile', 'active_profile accepted a path outside its profile directory.'),
    ('GATE-07', 'Registry', 'Non-string unhashable versions raised cache TypeError instead of a domain error.'),
):
    add(identifier, entity, explanation, None, 'Regression test passes and legacy stays selectable',
        status='PASS', evidence='eaeu_xml/tests/test_op26_version_selection.py; verification/regression.xml')

for identifier, entity, missing, criterion in (
    ('EXT-01', 'All structures', 'Official XSD payload/import/include dependency closure not retrieved; rseds.eaeunion.org timed out in browser, web and curl.', 'Obtain official schema bundle; verify origin, hashes, includes/imports and schema validation for positive/negative XML.'),
    ('EXT-02', 'R.006/R.007 and model imports', 'Y.Y.Y/X.X.X/Z.Z.Z are source parameters, not identified production versions.', 'Identify authoritative versions and namespace URIs in the official registry/model packages.'),
    ('EXT-03', 'Classifiers', '47 classifier references are descriptions, not authoritative datasets with versions/lifecycle.', 'Retrieve and verify applicable authoritative datasets; exercise accepted/rejected and obsolete codes.'),
    ('IMPL-01', 'Rules/policies', '481 scoped source requirement rows are not compiled executable rules; input/UI policies remain empty.', 'Interpret requirements and inherited ranges; wire predicates/policies to verified paths and prove positive/negative runtime behavior.'),
    ('IMPL-02', 'Application/GUI/session persistence', 'Version selection exists in engine/registry only; application/GUI still uses the legacy selection path.', 'After model closure, select edition throughout form generation/session save/restore without mixing data; actual GUI E2E proof.'),
    ('AUDIT-01', 'Semantic delta', 'delta.json proves membership; retained IDs and complete field/requirement semantic equivalence remain unreviewed.', 'Source review of every retained object, field and requirement with old/new text and executable trace.'),
    ('AUDIT-02', 'Source completeness', 'No exhaustive official amendment-history export through 2026-10-23; 12/2025 is a discovered additional amendment lead.', 'Verify full official change chain and applicability of all earlier/later amendments, including accession rules.'),
    ('AUDIT-03', 'PDF vs Word', 'Word extraction is reproducible; every row has not been independently reconciled with the signed PDF. Some PDF page matches are ambiguous.', 'Resolve all Word/PDF differences and ambiguous row/page locators against PDF, preserving source conflicts.'),
    ('TEST-01', 'OP35.1', 'OP35.1 package/tests absent from this target branch.', 'Recover an authorized actual package and execute its regression; do not infer results from another checkout.'),
    ('TEST-02', 'Combined Qt suite', 'Combined baseline aborted in fixed_font_family/test_validation_page_qml.py; isolated Qt modules pass.', 'Resolve pre-existing Qt application lifecycle/order interaction and rerun the single combined command.'),
):
    add(identifier, entity, 'Production acceptance is not established.', missing, criterion,
        status='SOURCE_BLOCKED' if identifier.startswith('EXT') else 'NOT_TESTED',
        evidence='FINAL_REPORT.md; verification; source_inventory.json')

for path in sorted((PACKAGE / 'message_rules').glob('*.yaml')):
    data = json.loads(path.read_text())
    for index, requirement in enumerate(data['business_rules'], 1):
        add(f"REQ-{data['message_code']}-{index:03}", data['message_code'],
            'Requirement text imported with regulation scope; runtime behavior is unproven.',
            'Verified paths, contextual predicate, external-registry/correlation dependencies as applicable.',
            'Source interpretation and positive/negative evaluator plus serialized XML proof for this exact scoped row.',
            requirement['source_refs'], structure=data['structure_id'], evidence=requirement['rule_id'])

for field in json.loads((REPORT / 'field_inventory.json').read_text()):
    add(f"FIELD-{field['structure_id']}-{field['source_row_index']:04}", 'FIELD',
        'Source datatype and cardinality preserved; executable path/QName binding is unresolved.',
        'Model namespace version, hierarchy/path interpretation (including wildcard rows and attributes), facets and classifier binding.',
        'Trace source row to exact QName/path with official model/XSD and verify cardinality, ordering, repeatable-parent alignment.',
        field['source_refs'], structure=field['structure_id'], evidence=f"field_inventory.json row {field['source_row_index']} in {field['structure_id']}")

(REPORT / 'gap_register.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n')
print('Gaps:',len(rows),'closed:',sum(r['status']=='PASS' for r in rows))
