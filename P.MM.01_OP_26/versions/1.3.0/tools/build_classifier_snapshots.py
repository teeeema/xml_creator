"""Build offline indexes only from complete, hash-verified public NSI responses."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parents[1];R=P.parents[2]
source=R/'codex_reports/OP26_P_MM_01/V130_STAGE3/sources/nsi_acquisition.json'
for row in json.loads(source.read_text()):
    if row['status']!='COMPLETE_OFFICIAL_SNAPSHOT':continue
    records=[]
    for call in row['calls']:
        path=R/call['artifact']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==call['sha256']
        if '.page_' in path.name:records.extend(json.loads(path.read_text()))
    assert len(records)==row['expected_count']==len(row['values'])
    assert len({r['id'] for r in records})==len(records)
    assert all(r['status']=='actual' for r in records)
    assert [r['data']['Code'] for r in records]==row['values']
    data=dict(format='EAEU_CLASSIFIER_SNAPSHOT_V1',classifier_refs=[row['nsi_code'],row['CLS']],snapshot_date=row['snapshot_date'],
        official_version_id=row['version_id'],title=row['title'],publication_status=row['publication_status'],authority_status=row['authority_status'],
        effective_from=row['effective_from'],effective_to=row['effective_to'],complete=True,expected_count=row['expected_count'],values=row['values'],sources=row['calls'])
    (P/'classifiers'/(row['nsi_code']+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(row['nsi_code'],len(records),'verified records')
