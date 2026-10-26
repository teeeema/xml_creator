"""Read-only acquisition via the public NSI portal endpoints used by its JS app.

Only ES NSI codes printed in the normative catalog are queried. Date is explicit;
all downloaded pages, passports, totals and hashes are retained. No inferred IDs.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,re,hashlib,datetime
R=Path(__file__).resolve().parents[4];D=R/'codex_reports/OP26_P_MM_01/V130_STAGE3';P=R/'P.MM.01_OP_26/versions/1.3.0'
DATE='2026-10-23';BASE='https://nsi.eaeunion.org/portal/api';OUT=D/'sources/nsi';OUT.mkdir(parents=True,exist_ok=True)

def request(url,file,payload=None):
    args=['curl','--fail','--silent','--show-error','--max-time','20','-L',url,'-o',str(file)]
    if payload is not None:args+=['-H','Content-Type: application/json','--data-binary',json.dumps(payload)]
    run=subprocess.run(args,capture_output=True,text=True)
    result=dict(url=url,method='POST_READ' if payload is not None else 'GET',request=payload,exit_code=run.returncode,error=run.stderr,
        retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    if run.returncode==0:
        result.update(artifact=str(file.relative_to(R)),sha256=hashlib.sha256(file.read_bytes()).hexdigest())
        try:return result,json.loads(file.read_text())
        except ValueError:result['error']='NON_JSON_RESPONSE'
    return result,None

refs=json.loads((P/'classifier_references.yaml').read_text())['classifiers']
entries=[]
for c in refs:
    ids=re.findall(r'код (?:классификатора|справочника) в ЕС НСИ «([^»]+)»',c['description'])
    if len(ids)==1:entries.append((c,ids[0]))

def acquire(pair):
    c,code=pair;calls=[];result=dict(CLS=c['classifier_code'],nsi_code=code,name=c['name'],status='NOT_RETRIEVED',calls=calls)
    meta_call,meta=request(f'{BASE}/registries/get-by-code-n-date?code={code}&date={DATE}',OUT/(code+'.passport.json'));calls.append(meta_call)
    if not meta:return result
    result.update(title=meta.get('data',{}).get('TitleName'),version_id=meta.get('versionId'),effective_from=meta.get('dateTimeFrom'),
                  effective_to=meta.get('dateTimeTo'),publication_status=meta.get('status'),authority_status=meta.get('authorityStatus'),snapshot_date=DATE)
    if meta.get('status')!='published':result['status']='NOT_PUBLISHED';return result
    body=dict(date=DATE,filter=[],sort=[])
    total_call,total=request(f'{BASE}/dictionaries/{code}/get-list-data-total',OUT/(code+'.total.json'),body);calls.append(total_call)
    if total is None:return result
    count=total if isinstance(total,int) else total.get('byFilterCount',total.get('totalCount'))
    result['expected_count']=count
    if not isinstance(count,int) or not 0<count<=20000:result['status']='METADATA_ONLY_UNSUPPORTED_COUNT';return result
    data=[];offset=0
    while offset<count:
        call,page=request(f'{BASE}/dictionaries/{code}/get-list-data',OUT/(code+f'.page_{offset}.json'),dict(body,offset=offset,limit=1000));calls.append(call)
        if not isinstance(page,list) or not page:result['status']='INCOMPLETE_PAGES';return result
        data.extend(page);offset+=len(page)
    if len(data)!=count or len({r['id'] for r in data})!=count:result['status']='COUNT_OR_ID_CONFLICT';return result
    values=[r.get('data',{}).get('Code') for r in data]
    if any(not isinstance(v,str) or not v for v in values):result['status']='METADATA_ONLY_NON_FLAT_CODES';return result
    if len(values)!=len(set(values)):result['status']='DUPLICATE_CODE_CONFLICT';return result
    result.update(status='COMPLETE_OFFICIAL_SNAPSHOT',count=len(data),values=values)
    return result

results=list(ThreadPoolExecutor(4).map(acquire,entries))
(D/'sources/nsi_acquisition.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
for x in results:print(x['nsi_code'],x['status'],x.get('expected_count'),x.get('title'))
