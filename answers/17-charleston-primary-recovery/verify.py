#!/usr/bin/env python3
"""Offline verifier; reads package and optional retained report directory, never fetches URLs."""
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BASE='https://rspace.library.cofc.edu/iiif/'
EXACT=BASE+'lcdl129141JPEG1jpg/manifest'
NEARBY=BASE+'lcdl129143JPEG1jpg/manifest'
WILDCARD=BASE+'%2A129141%2A/manifest'
HASH='7c981bfa48feb24abdf81e56e17c5f70a2b39aeb11e8664f0b67abaeee26a96c'

def require(ok,msg):
    if not ok: raise ValueError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def check_file(raw,spec):
    require(len(raw)==spec['bytes'] and sha(raw)==spec['sha256'],'File length/hash mismatch')
def check_exact(raw):
    require(len(raw)==5484 and sha(raw)==HASH,'Exact manifest bytes/hash changed')
    m=json.loads(raw)
    require(m['@id']==EXACT and m['@type']=='sc:Manifest','Complete manifest identity mismatch')
    require(m['label']=='View in Magnolia Cemetery','Document label mismatch')
    return m
def identity(m):
    canvas=m['sequences'][0]['canvases'][0];image=canvas['images'][0]['resource']
    field=lambda label:next(x['value'][0]['@value'] for x in m['metadata'] if x['label']==label)
    return dict(manifest_id=m['@id'],label=m['label'],description=m['description'],catalog_date=field('Date'),catalog_date_basis='Source metadata Date; not manifest publication or acquisition',contributing_institution=field('Contributing Institution'),license=m['license'],canvas_id=canvas['@id'],width=canvas['width'],height=canvas['height'],image_id=image['@id'],image_service_id=image['service']['@id'])
def check_history(raw,receipts):
    require(len(receipts)==3,'Expected two exact and one wildcard receipt')
    expected=['37c153c8-a72a-42f2-b183-d36052a0234d','d7cba212-4cc3-4c58-85c1-4a1846969d03','8c45dd93-439f-4e73-9e2a-d5f3b8d2e99c']
    require([r['report_id'] for r in receipts]==expected,'Report identifier mismatch')
    for r in receipts[:2]:
        require(r['submitted_url']==r['observed_request_url']==EXACT,'Exact historical request target mismatch')
        require(r['reported_status']=='200' and r['reported_response_bytes']==len(raw) and r['reported_response_sha256']==sha(raw),'Historical reported response correspondence failed')
        require(r['reported_body_inline'] is None,'Historical body scope changed')
    r=receipts[2]
    require(r['submitted_url']==r['observed_request_url']==WILDCARD,'Wildcard target rewritten')
    require(r['reported_response_bytes']==0 and r['reported_response_sha256']==sha(b'') and r['reported_body_inline'] is None,'Wildcard promoted to readable object')
def verify_receipt_files(receipts,directory):
    for r in receipts:
        raw=gzip.decompress((directory/(r['report_id']+'.json.gz')).read_bytes())
        require(sha(raw)==r['provider_json_sha256'] and len(raw)==r['provider_json_bytes'],'Original provider JSON hash/length mismatch')
        a=json.loads(raw);h=a['http'][r['http_index']];d=h['response']['data']
        require(a['report_id']==r['report_id'] and a['date']==r['report_date'],'Original report clock/ID mismatch')
        require(a['url']['schema']+'://'+a['url']['addr']==r['submitted_url'],'Original submitted URL mismatch')
        require(h['url']['schema']+'://'+h['url']['addr']==r['observed_request_url'] and h['date']==r['observed_request_date'],'Original request URL/clock mismatch')
        require(h['response']['status_code']==r['reported_status'] and d['size']==r['reported_response_bytes'] and d['sha256']==r['reported_response_sha256'] and d['mime_type']==r['reported_mime_type'] and d['data']==r['reported_body_inline'],'Original response fields mismatch')
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--receipt-dir',type=Path);parser.add_argument('--negative-controls',action='store_true');args=parser.parse_args()
    manifest=json.loads((ROOT/'manifest.json').read_text());files={}
    for name,spec in manifest['files'].items():
        path=(ROOT/name).resolve();require(path.is_relative_to(ROOT),'Manifest escaped package');files[name]=path.read_bytes();check_file(files[name],spec)
    raw=files['evidence/manifest-lcdl129141.json'];exact=check_exact(raw)
    nearby=json.loads(files['evidence/manifest-lcdl129143.json'])
    require(nearby['@id']==NEARBY and nearby['label']=='View on South Battery','Nearby identity mismatch')
    identities=json.loads(files['evidence/identity.json']);require(identities==[identity(exact),identity(nearby)],'Parsed identity does not match literal manifests')
    require(identities[0]['image_service_id']=='https://iiif.library.cofc.edu/iiif/2/205927' and identities[1]['image_service_id']=='https://iiif.library.cofc.edu/iiif/2/205929','Separate image resource IDs mismatch')
    require(identities[0]['catalog_date']==identities[1]['catalog_date']=='1893','Catalog metadata date mismatch')
    require(files['evidence/wildcard-response.bin']==b'','Wildcard response contains unexpected data')
    receipts=json.loads(files['evidence/historical-receipts.json']);check_history(raw,receipts)
    caps=json.loads(files['evidence/captures.json'])
    for c in caps:check_file(files[c['path']],c)
    require([c['url'] for c in caps]==[EXACT,NEARBY,WILDCARD],'Current complete capture URLs mismatch')
    if args.receipt_dir:verify_receipt_files(receipts,args.receipt_dir)
    result=dict(status='PASS',evidence_files=len(files),exact_manifest_bytes=len(raw),historical_reported_hash_matches=2,distinct_nearby_manifest=True,wildcard_empty=True,original_receipt_files_verified=3 if args.receipt_dir else 0,scope='Current manifest bytes match historical provider-reported response hashes. Historical inline bodies are absent. Without --receipt-dir, verifies retained scalar declarations, not extraction from omitted provider JSON.')
    if args.negative_controls:
        tests=[]
        def rejected(name,fn):
            try:fn()
            except (ValueError,KeyError,TypeError):tests.append(name)
            else:raise ValueError('Control unexpectedly accepted: '+name)
        rejected('altered current body',lambda:check_exact(raw.replace(b'129141',b'129142',1)))
        rejected('nearby substituted for exact',lambda:check_exact(files['evidence/manifest-lcdl129143.json']))
        r=copy.deepcopy(receipts);r[0]['reported_response_sha256']='0'*64;rejected('altered historical response hash',lambda:check_history(raw,r))
        r=copy.deepcopy(receipts);r[1]['observed_request_url']=NEARBY;rejected('nearby historical target falsely joined',lambda:check_history(raw,r))
        r=copy.deepcopy(receipts);r[2]['reported_response_bytes']=5484;rejected('wildcard promoted to exact body',lambda:check_history(raw,r))
        rejected('same-length file tamper',lambda:check_file(b'X'+raw[1:],manifest['files']['evidence/manifest-lcdl129141.json']))
        result['negative_controls_rejected']=tests
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,OSError,StopIteration) as e:
        print(json.dumps({'status':'FAIL','error':str(e)}));raise SystemExit(1)
